#!/usr/bin/env python3
"""Instagram Saved → Notion Inspiration Library Sync.

Pulls posts from an Instagram saved collection and syncs them
to the Notion Inspiration Library with Claude Haiku analysis.
"""

import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

# --- Config ---
SCRIPT_DIR = Path(__file__).parent

# Load .env manually (no external deps beyond instagrapi)
ENV_FILE = SCRIPT_DIR / ".env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip())

IG_USERNAME = os.environ.get("IG_USERNAME", "")
IG_PASSWORD = os.environ.get("IG_PASSWORD", "")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "AI to emulate")
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
NOTION_DB_ID = os.environ.get("NOTION_DB_ID", "")
RATE_LIMIT_SECONDS = int(os.environ.get("RATE_LIMIT_SECONDS", "5"))
BACKFILL_RATE_LIMIT = int(os.environ.get("BACKFILL_RATE_LIMIT", "10"))
MAX_REEL_DURATION = int(os.environ.get("MAX_REEL_DURATION", "90"))
SYSTEM_PROMPT_FILE = SCRIPT_DIR / "system-prompt.txt"
STATE_DIR = SCRIPT_DIR / "state"
STATE_DIR.mkdir(exist_ok=True)
PROCESSED_FILE = STATE_DIR / "processed.json"
SESSION_FILE = STATE_DIR / "session.json"
WORKING_DIR = SCRIPT_DIR.parent

# --- Logging ---
LOG_DIR = SCRIPT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "ig-saved-sync.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("ig-saved-sync")


# --- Instagram Client ---

class IGClient:
    """Wraps instagrapi with session persistence and rate limiting."""

    def __init__(self):
        from instagrapi import Client
        self.cl = Client()
        self.cl.delay_range = [1, 3]

    def login(self):
        """Login with session reuse. Falls back to fresh login with 2FA support."""
        if SESSION_FILE.exists():
            try:
                self.cl.load_settings(SESSION_FILE)
                self.cl.login(IG_USERNAME, IG_PASSWORD)
                self.cl.get_timeline_feed()  # validate session
                log.info("Logged in via saved session")
                return
            except Exception as e:
                log.warning(f"Saved session failed ({e}), doing fresh login")
                SESSION_FILE.unlink(missing_ok=True)

        try:
            self.cl.login(IG_USERNAME, IG_PASSWORD)
        except Exception as e:
            if "two-factor" in str(e).lower() or "Two-factor" in str(e):
                if not sys.stdin.isatty():
                    raise RuntimeError(
                        "2FA required but running non-interactively. "
                        "Run 'python3 ig-saved-sync.py status' manually first to refresh session."
                    )
                # Extract 2FA identifier and request SMS
                two_factor_info = self.cl.last_json.get("two_factor_info", {})
                two_factor_id = two_factor_info.get("two_factor_identifier")
                log.info(f"2FA required (identifier: {two_factor_id})")

                # Explicitly request SMS be sent
                try:
                    self.cl.private_request(
                        "accounts/send_two_factor_login_sms/",
                        {
                            "two_factor_identifier": two_factor_id,
                            "username": IG_USERNAME,
                            "device_id": self.cl.android_device_id,
                            "guid": self.cl.uuid,
                            "_csrftoken": self.cl.token,
                        },
                    )
                    log.info("SMS code requested successfully")
                except Exception as sms_err:
                    log.warning(f"SMS request failed ({sms_err}), code may already be sent")

                code = input("Enter the 2FA code from your phone: ").strip()

                # Call two_factor_login directly
                from uuid import uuid4
                logged = self.cl.private_request(
                    "accounts/two_factor_login/",
                    {
                        "verification_code": code,
                        "two_factor_identifier": two_factor_id,
                        "username": IG_USERNAME,
                        "phone_id": self.cl.phone_id,
                        "device_id": self.cl.android_device_id,
                        "guid": self.cl.uuid,
                        "_csrftoken": self.cl.token,
                        "trust_this_device": "1",
                        "waterfall_id": str(uuid4()),
                        "verification_method": "1",
                    },
                    login=True,
                )
                self.cl.authorization_data = self.cl.parse_authorization(
                    self.cl.last_response.headers.get("ig-set-authorization")
                )
                if logged:
                    self.cl.login_flow()
                    self.cl.last_login = time.time()
            else:
                raise
        self.cl.dump_settings(SESSION_FILE)
        log.info("Login successful, session saved")

    def get_collection_medias(self):
        """Get all media from the named saved collection."""
        collections = self.cl.collections()
        target = None
        for c in collections:
            if c.name == COLLECTION_NAME:
                target = c
                break

        if not target:
            available = [c.name for c in collections]
            raise RuntimeError(
                f"Collection '{COLLECTION_NAME}' not found. "
                f"Available: {available}"
            )

        log.info(f"Found collection '{COLLECTION_NAME}' (id={target.id})")
        medias = self.cl.collection_medias(target.id)
        log.info(f"Fetched {len(medias)} medias from collection")
        return medias

    def extract_metadata(self, media) -> dict:
        """Extract relevant metadata from an instagrapi Media object."""
        media_type = "Reel" if media.media_type == 2 and media.product_type == "clips" else \
                     "Video" if media.media_type == 2 else \
                     "Carousel" if media.media_type == 8 else "Image"

        # Build the post URL
        code = media.code
        url = f"https://www.instagram.com/p/{code}/" if code else ""
        if media_type == "Reel" and code:
            url = f"https://www.instagram.com/reel/{code}/"

        creator = media.user.username if media.user else ""
        caption = media.caption_text or ""

        # Engagement metrics
        likes = media.like_count or 0
        comments = media.comment_count or 0
        views = 0
        if hasattr(media, "view_count") and media.view_count:
            views = media.view_count
        elif hasattr(media, "play_count") and media.play_count:
            views = media.play_count

        # Duration for reels
        duration = 0
        if hasattr(media, "video_duration") and media.video_duration:
            duration = int(media.video_duration)

        # Video URL for transcription
        video_url = ""
        if media.media_type == 2 and media.video_url:
            video_url = str(media.video_url)

        engagement_str = []
        if views:
            engagement_str.append(f"{views:,} views")
        if likes:
            engagement_str.append(f"{likes:,} likes")
        if comments:
            engagement_str.append(f"{comments:,} comments")

        return {
            "pk": str(media.pk),
            "code": code,
            "url": url,
            "content_type": media_type,
            "creator": creator,
            "caption": caption[:2000],
            "likes": likes,
            "comments": comments,
            "views": views,
            "duration": duration,
            "video_url": video_url,
            "engagement_str": ", ".join(engagement_str) if engagement_str else "No metrics",
            "taken_at": media.taken_at.isoformat() if media.taken_at else "",
        }


# --- Notion Client ---

class NotionClient:
    """Direct Notion API client using urllib."""

    BASE = "https://api.notion.com/v1"
    VERSION = "2022-06-28"

    def __init__(self, token: str, database_id: str):
        self.token = token
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": self.VERSION,
        }

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        url = f"{self.BASE}{path}"
        data = json.dumps(body).encode() if body else None
        req = Request(url, data=data, headers=self.headers, method=method)
        try:
            with urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except HTTPError as e:
            error_body = e.read().decode()
            log.error(f"Notion API {e.code}: {error_body[:500]}")
            raise RuntimeError(f"Notion API error {e.code}: {error_body[:200]}")

    def create_page(self, properties: dict, children: list | None = None) -> dict:
        """Create a new page in the Inspiration Library."""
        body = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
        }
        if children:
            body["children"] = children
        return self._request("POST", "/pages", body)

    def append_blocks(self, page_id: str, children: list) -> dict:
        """Append block children to a page body."""
        return self._request("PATCH", f"/blocks/{page_id}/children", {"children": children})

    def build_properties(self, data: dict) -> dict:
        """Build Inspiration Library properties from analysis data."""
        props = {
            "Title": {"title": [{"text": {"content": _trunc(data.get("title", "Untitled"), 200)}}]},
            "Type": {"select": {"name": data.get("type", "Hook Example")}},
            "Source": {"select": {"name": "Instagram Saved"}},
            "Platform": {"multi_select": [{"name": "Instagram"}]},
            "Date Added": {"date": {"start": datetime.now(timezone.utc).strftime("%Y-%m-%d")}},
        }

        if data.get("source_url"):
            props["Source URL"] = {"url": data["source_url"]}
        if data.get("creator"):
            props["Creator Handle"] = {"rich_text": [{"text": {"content": f"@{data['creator']}"}}]}
        if data.get("performance_tier"):
            props["Performance Tier"] = {"select": {"name": data["performance_tier"]}}
        if data.get("engagement_str"):
            props["Engagement Metric"] = {"rich_text": [{"text": {"content": _trunc(data["engagement_str"], 200)}}]}
        if data.get("tags"):
            props["Topic Tags"] = {"multi_select": [{"name": t} for t in data["tags"][:10]]}
        if data.get("hook_framework"):
            props["Hook Framework"] = {"select": {"name": data["hook_framework"]}}
        if data.get("hook_text"):
            props["Hook Text"] = {"rich_text": [{"text": {"content": _trunc(data["hook_text"], 2000)}}]}
        if data.get("notes"):
            props["Notes"] = {"rich_text": [{"text": {"content": _trunc(data["notes"], 2000)}}]}

        return props


def _trunc(text: str, limit: int) -> str:
    """Truncate text to Notion's rich_text limit."""
    if len(text) <= limit:
        return text
    return text[:limit - 3] + "..."


# --- State Manager ---

class StateManager:
    """Tracks processed media PKs to avoid duplicates."""

    def __init__(self, path: Path):
        self.path = path
        self._data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text())
            except (json.JSONDecodeError, OSError):
                log.warning("Corrupt state file, starting fresh")
        return {"processed": {}}

    def _save(self):
        self.path.write_text(json.dumps(self._data, indent=2))

    def is_processed(self, pk: str) -> bool:
        return pk in self._data["processed"]

    def mark_processed(self, pk: str, notion_page_id: str):
        self._data["processed"][pk] = {
            "notion_page_id": notion_page_id,
            "synced_at": datetime.now(timezone.utc).isoformat(),
        }
        self._save()

    @property
    def count(self) -> int:
        return len(self._data["processed"])


# --- Transcription ---

def transcribe_reel(video_url: str, duration: int) -> str:
    """Download reel audio via yt-dlp and transcribe with whisper."""
    if duration > MAX_REEL_DURATION:
        log.info(f"Skipping transcription: duration {duration}s > {MAX_REEL_DURATION}s limit")
        return ""

    import tempfile
    audio_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            audio_path = f.name

        # Download audio with yt-dlp
        dl_cmd = [
            sys.executable, "-m", "yt_dlp",
            "-f", "bestaudio",
            "-o", audio_path,
            "--no-playlist", "--quiet",
            "--no-check-certificates",
            video_url,
        ]
        result = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            log.warning(f"yt-dlp failed: {result.stderr[:200]}")
            return ""

        # Find the actual downloaded file (yt-dlp may add extension)
        downloaded = None
        for ext in [".mp3", ".m4a", ".webm", ".mp4", ""]:
            candidate = Path(audio_path + ext) if ext else Path(audio_path)
            if candidate.exists() and candidate.stat().st_size > 0:
                downloaded = candidate
                break
        if not downloaded:
            base = Path(audio_path)
            for f in base.parent.glob(f"{base.stem}*"):
                if f.stat().st_size > 0:
                    downloaded = f
                    break
        if not downloaded:
            log.warning("No audio file found after download")
            return ""

        # Transcribe with whisper
        whisper_cmd = [
            sys.executable, "-m", "whisper",
            str(downloaded),
            "--model", "tiny",
            "--language", "en",
            "--output_format", "txt",
            "--output_dir", tempfile.gettempdir(),
        ]
        result = subprocess.run(whisper_cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            log.warning(f"Whisper failed: {result.stderr[:200]}")
            return ""

        # Read transcript
        txt_path = Path(downloaded).with_suffix(".txt")
        if not txt_path.exists():
            txt_path = Path(tempfile.gettempdir()) / (downloaded.stem + ".txt")
        if txt_path.exists():
            transcript = txt_path.read_text().strip()
            txt_path.unlink(missing_ok=True)
            log.info(f"Transcribed {len(transcript)} chars")
            return transcript[:3000]

        return ""
    except subprocess.TimeoutExpired:
        log.warning("Transcription timed out")
        return ""
    except Exception as e:
        log.warning(f"Transcription error: {e}")
        return ""
    finally:
        if audio_path:
            Path(audio_path).unlink(missing_ok=True)


# --- Claude Haiku Analysis ---

def analyze_post(metadata: dict, transcript: str = "") -> dict:
    """Call Claude Haiku to analyze an IG post and return structured data."""
    system_prompt = SYSTEM_PROMPT_FILE.read_text()

    # Build the analysis input
    parts = [
        f"Content Type: {metadata['content_type']}",
        f"Creator: @{metadata['creator']}",
        f"URL: {metadata['url']}",
        f"Engagement: {metadata['engagement_str']}",
        f"Posted: {metadata.get('taken_at', 'Unknown')}",
    ]
    if metadata["caption"]:
        parts.append(f"Caption:\n{metadata['caption'][:1500]}")
    if transcript:
        parts.append(f"Transcript:\n{transcript[:1500]}")

    message = "\n\n".join(parts)

    cmd = [
        "claude",
        "-p", message,
        "--system-prompt", system_prompt,
        "--output-format", "json",
        "--permission-mode", "bypassPermissions",
        "--max-budget-usd", "0.05",
        "--no-session-persistence",
        "--model", "claude-haiku-4-5-20251001",
        "--allowedTools", "",
    ]

    # Unset CLAUDECODE env var to avoid nested session error
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=45,
            cwd=str(WORKING_DIR),
            env=env,
        )
    except subprocess.TimeoutExpired:
        log.error("Claude timed out")
        raise RuntimeError("Claude analysis timed out")

    if result.returncode != 0:
        log.error(f"Claude stderr: {result.stderr[:500]}")
        raise RuntimeError(f"Claude exited {result.returncode}: {result.stderr[:200]}")

    # Parse output
    try:
        data = json.loads(result.stdout)
        text = data.get("result", result.stdout)
    except json.JSONDecodeError:
        text = result.stdout

    text = str(text).strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        log.error(f"Failed to parse Claude JSON: {text[:300]}")
        raise RuntimeError(f"Invalid JSON from Claude: {text[:200]}")


def build_fallback_analysis(metadata: dict) -> dict:
    """Build a minimal analysis when Claude is skipped (--no-analyze mode)."""
    content_type = metadata["content_type"]
    type_map = {"Reel": "Hook Example", "Video": "Hook Example",
                "Carousel": "Hook Example", "Image": "Hook Example"}

    # Infer performance tier from engagement
    views = metadata.get("views", 0)
    likes = metadata.get("likes", 0)
    if views >= 100000 or likes >= 10000:
        tier = "Outlier"
    elif views >= 10000 or likes >= 1000:
        tier = "Strong"
    else:
        tier = "Reference"

    caption = metadata.get("caption", "")
    hook_text = caption.split("\n")[0][:200] if caption else ""
    title = f"@{metadata['creator']} — {content_type}"

    return {
        "title": title,
        "type": type_map.get(content_type, "Hook Example"),
        "hook_text": hook_text,
        "hook_framework": "",
        "tags": ["AI Tools"],
        "performance_tier": tier,
        "notes": f"Auto-imported from '{COLLECTION_NAME}' collection (no analysis)",
    }


# --- Processing Pipeline ---

def process_single(
    metadata: dict,
    notion: NotionClient,
    state: StateManager,
    do_analyze: bool = True,
    do_transcribe: bool = True,
    rate_limit: int = RATE_LIMIT_SECONDS,
):
    """Process a single IG post: transcribe → analyze → create Notion page."""
    pk = metadata["pk"]

    if state.is_processed(pk):
        log.info(f"Skipping {pk} (@{metadata['creator']}) — already processed")
        return False

    log.info(f"Processing {pk}: @{metadata['creator']} ({metadata['content_type']})")

    # Transcribe reels
    transcript = ""
    if do_transcribe and metadata["content_type"] in ("Reel", "Video") and metadata["video_url"]:
        dl_url = metadata["url"] if metadata["url"] else metadata["video_url"]
        transcript = transcribe_reel(dl_url, metadata["duration"])

    # Analyze with Claude or use fallback
    if do_analyze:
        try:
            analysis = analyze_post(metadata, transcript)
        except Exception as e:
            log.error(f"Analysis failed for {pk}: {e}")
            analysis = build_fallback_analysis(metadata)
    else:
        analysis = build_fallback_analysis(metadata)

    # Merge metadata into analysis
    analysis["source_url"] = metadata["url"]
    analysis["creator"] = metadata["creator"]
    analysis["engagement_str"] = metadata["engagement_str"]

    # Build Notion properties and create page
    props = notion.build_properties(analysis)

    # Build page body with caption + transcript
    children = []
    if metadata["caption"]:
        children.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "Caption"}}],
            },
        })
        caption = metadata["caption"]
        for i in range(0, len(caption), 2000):
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": caption[i:i+2000]}}],
                },
            })

    if transcript:
        children.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "Transcript"}}],
            },
        })
        for i in range(0, len(transcript), 2000):
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": transcript[i:i+2000]}}],
                },
            })

    try:
        page = notion.create_page(props, children if children else None)
        page_id = page["id"]
        state.mark_processed(pk, page_id)
        title = analysis.get("title", "Untitled")
        log.info(f"Created Notion page: {title} (pk={pk})")
        return True
    except Exception as e:
        log.error(f"Failed to create Notion page for {pk}: {e}")
        return False
    finally:
        time.sleep(rate_limit)


# --- CLI Commands ---

def cmd_run():
    """Incremental sync — process only new posts."""
    log.info("=== Starting incremental sync ===")
    ig = IGClient()
    ig.login()

    notion = NotionClient(NOTION_TOKEN, NOTION_DB_ID)
    state = StateManager(PROCESSED_FILE)

    medias = ig.get_collection_medias()
    new_count = 0
    skip_count = 0

    for media in medias:
        metadata = ig.extract_metadata(media)
        if state.is_processed(metadata["pk"]):
            skip_count += 1
            continue
        success = process_single(metadata, notion, state, rate_limit=RATE_LIMIT_SECONDS)
        if success:
            new_count += 1

    log.info(f"=== Sync complete: {new_count} new, {skip_count} skipped, {state.count} total ===")


def cmd_backfill(limit: int = 0, no_analyze: bool = False):
    """Import all existing posts from the collection."""
    log.info(f"=== Starting backfill (limit={limit or 'all'}, analyze={'no' if no_analyze else 'yes'}) ===")
    ig = IGClient()
    ig.login()

    notion = NotionClient(NOTION_TOKEN, NOTION_DB_ID)
    state = StateManager(PROCESSED_FILE)

    medias = ig.get_collection_medias()
    if limit:
        medias = medias[:limit]

    processed = 0
    skipped = 0
    failed = 0

    for i, media in enumerate(medias):
        metadata = ig.extract_metadata(media)
        log.info(f"[{i+1}/{len(medias)}] @{metadata['creator']} — {metadata['content_type']}")

        if state.is_processed(metadata["pk"]):
            skipped += 1
            continue

        success = process_single(
            metadata, notion, state,
            do_analyze=not no_analyze,
            rate_limit=BACKFILL_RATE_LIMIT,
        )
        if success:
            processed += 1
        else:
            failed += 1

    log.info(f"=== Backfill complete: {processed} new, {skipped} skipped, {failed} failed, {state.count} total ===")


def cmd_status():
    """Print sync stats and verify connections."""
    print("Instagram Saved Sync — Status")
    print("=" * 40)

    # Check config
    print(f"\nIG Username: {IG_USERNAME}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Notion DB: {NOTION_DB_ID[:8]}..." if NOTION_DB_ID else "Notion DB: NOT SET")

    # Check state
    state = StateManager(PROCESSED_FILE)
    print(f"Processed posts: {state.count}")

    # Test IG login
    print("\nTesting Instagram login...")
    try:
        ig = IGClient()
        ig.login()
        print("  IG login: OK")

        collections = ig.cl.collections()
        names = [c.name for c in collections]
        if COLLECTION_NAME in names:
            print(f"  Collection '{COLLECTION_NAME}': FOUND")
            medias = ig.get_collection_medias()
            print(f"  Posts in collection: {len(medias)}")
            unprocessed = sum(1 for m in medias if not state.is_processed(str(m.pk)))
            print(f"  Unprocessed: {unprocessed}")
        else:
            print(f"  Collection '{COLLECTION_NAME}': NOT FOUND")
            print(f"  Available: {names}")
    except Exception as e:
        print(f"  IG login: FAILED — {e}")

    # Test Notion
    print("\nTesting Notion API...")
    try:
        notion = NotionClient(NOTION_TOKEN, NOTION_DB_ID)
        result = notion._request("GET", f"/databases/{NOTION_DB_ID}")
        db_title = result.get("title", [{}])[0].get("plain_text", "Unknown")
        print(f"  Notion DB: OK ({db_title})")
    except Exception as e:
        print(f"  Notion DB: FAILED — {e}")

    print()


# --- Main ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ig-saved-sync.py <run|backfill|status>", file=sys.stderr)
        print("  run              Incremental sync (new posts only)", file=sys.stderr)
        print("  backfill         Import all existing posts", file=sys.stderr)
        print("    --limit N      Only process N posts", file=sys.stderr)
        print("    --no-analyze   Skip Claude analysis (faster)", file=sys.stderr)
        print("  status           Check connections and stats", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "run":
            cmd_run()
        elif command == "backfill":
            limit = 0
            no_analyze = "--no-analyze" in sys.argv
            for i, arg in enumerate(sys.argv):
                if arg == "--limit" and i + 1 < len(sys.argv):
                    limit = int(sys.argv[i + 1])
            cmd_backfill(limit=limit, no_analyze=no_analyze)
        elif command == "status":
            cmd_status()
        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            sys.exit(1)
    except KeyboardInterrupt:
        log.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        log.error(f"Unhandled error in {command}: {e}", exc_info=True)
        sys.exit(1)
