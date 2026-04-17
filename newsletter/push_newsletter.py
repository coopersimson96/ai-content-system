#!/usr/bin/env python3
"""
Push newsletter HTML drafts to Beehiiv and schedule them.

Uses Playwright to create blank posts, then the internal dashboard API
to set content (tiptap_state), subject lines, and scheduling.

Why Playwright + internal API instead of the public API:
Beehiiv's public API requires an Enterprise plan for POST /posts. This script
works around that by creating the blank post via the UI (allowed on free plans)
and setting metadata via the internal dashboard API (same JWT the browser uses).

If you use a different email platform with a full public API (Mailchimp,
ConvertKit, Brevo), replace this script with direct API calls - you won't
need Playwright.

Usage:
    python3 push_newsletter.py                # push all unpushed drafts
    python3 push_newsletter.py --dry          # preview only
    python3 push_newsletter.py --limit 1      # push just the first one
    python3 push_newsletter.py --start-date 2026-04-17
    python3 push_newsletter.py --cleanup      # delete broken drafts
"""

import json
import os
import sys
import time
import argparse
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

DRAFTS_DIR = Path(__file__).parent / "drafts"
BEEHIIV = "https://app.beehiiv.com"
STATE_DIR = "/tmp/beehiiv-playwright-state"

# Load Beehiiv publication ID from .env
load_dotenv(Path(__file__).parent / ".env")
PUB_ID = os.environ.get("BEEHIIV_PUBLICATION_ID", "").replace("pub_", "")
if not PUB_ID:
    print("ERROR: BEEHIIV_PUBLICATION_ID missing from .env. Run setup first.", file=sys.stderr)
    sys.exit(1)

# Subjects you've already sent - the script skips these so you don't resend.
# Add to this set manually OR leave empty and track via your platform's UI.
ALREADY_SENT = set()


def load_drafts():
    """Load local draft metadata and HTML files."""
    drafts = []
    for jf in sorted(DRAFTS_DIR.glob("sf*.json")):
        meta = json.loads(jf.read_text())
        subject = meta.get("subject") or (meta.get("subject_lines", [None])[0]) or ""
        if subject in ALREADY_SENT:
            continue
        html_path = DRAFTS_DIR / (jf.stem + ".html")
        if not html_path.exists():
            continue
        preview = meta.get("preview") or meta.get("preview_text") or ""
        title = meta.get("title") or meta.get("script_title") or jf.stem
        drafts.append({
            "html": html_path.read_text(),
            "subject": subject,
            "preview": preview,
            "title": title,
            "file": jf.name,
        })
    return drafts


def html_to_paragraphs(html_content):
    """Extract text paragraphs from email HTML for typing into the WYSIWYG editor.

    Beehiiv posts use TipTap paragraph nodes, NOT HTML Snippets. This function
    extracts readable text from the rendered HTML so it can be typed into the editor.
    """
    import re

    body = re.search(r'<body[^>]*>(.*)</body>', html_content, re.DOTALL)
    html = body.group(1) if body else html_content

    # Remove style tags
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    # Convert <br> to newline
    html = re.sub(r'<br\s*/?>', '\n', html)
    # Convert <strong> to **
    html = re.sub(r'<strong>(.*?)</strong>', r'**\1**', html)
    # Convert links: <a href="url">text</a> -> [text](url)
    html = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', html)
    # Convert <hr> to ---
    html = re.sub(r'<hr[^>]*>', '---', html)

    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)

    clean_paras = []
    for p in paragraphs:
        text = re.sub(r'<[^>]+>', '', p).strip()
        if text:
            clean_paras.append(text)

    return clean_paras


def api_call(page, method, path, data=None):
    """Make an authenticated internal API call via the browser's JWT."""
    return page.evaluate("""(args) => {
        const [method, path, data, pubId] = args;
        const token = localStorage.getItem('token');

        const xhr = new XMLHttpRequest();
        const sep = path.includes('?') ? '&' : '?';
        xhr.open(method, path + sep + 'publication_id=' + pubId, false);
        xhr.setRequestHeader('Authorization', 'Bearer ' + token);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('x-current-publication-id', pubId);
        if (data) {
            xhr.send(JSON.stringify(data));
        } else {
            xhr.send();
        }

        let result;
        try { result = JSON.parse(xhr.responseText); } catch(e) { result = xhr.responseText; }
        return { status: xhr.status, data: result };
    }""", [method, path, data, PUB_ID])


def create_blank_post(page):
    """Create a blank post via Playwright UI and return its ID.

    Records existing draft IDs before clicking, then detects the new one after.
    """
    page.goto(f"{BEEHIIV}/posts", wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    existing = api_call(page, "GET", "/api/v2/posts?status=draft&per_page=50")
    existing_ids = set()
    if existing["status"] == 200:
        posts_list = existing["data"] if isinstance(existing["data"], list) else existing["data"].get("data", existing["data"].get("posts", []))
        existing_ids = {p["id"] for p in posts_list}

    page.locator('button:has-text("Start writing")').first.click(timeout=5000)
    time.sleep(3)
    page.locator('text="Blank draft"').first.click(timeout=5000)
    time.sleep(5)

    resp = api_call(page, "GET", "/api/v2/posts?status=draft&per_page=50")
    if resp["status"] != 200:
        return None

    posts = resp["data"] if isinstance(resp["data"], list) else resp["data"].get("data", resp["data"].get("posts", []))
    for p in posts:
        if p["id"] not in existing_ids:
            return p["id"]

    if posts:
        return posts[0]["id"]
    return None


def push_post(page, draft, send_utc):
    """Push a single newsletter draft to Beehiiv and schedule it."""

    post_id = create_blank_post(page)
    if not post_id:
        return False, "Failed to create blank post"

    page.goto(f"{BEEHIIV}/posts/{post_id}/edit?step=compose",
              wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)

    # Set title
    try:
        title_ta = page.locator('textarea[class*="editor-title"]').first
        title_ta.wait_for(state="visible", timeout=10000)
        title_ta.fill(draft["title"])
        time.sleep(0.5)
    except Exception as e:
        return False, f"Failed to set title: {e}"

    # Type email body as WYSIWYG text
    paragraphs = html_to_paragraphs(draft["html"])
    try:
        editor = page.locator('[contenteditable="true"]').first
        editor.click()
        time.sleep(0.3)
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        time.sleep(0.3)

        for i, para in enumerate(paragraphs):
            if i > 0:
                page.keyboard.press("Enter")
                time.sleep(0.05)
            page.keyboard.type(para, delay=1)
            time.sleep(0.05)

        time.sleep(3)
    except Exception as e:
        return False, f"Failed to type content: {e}"

    # Set subject + preview via internal API
    patch1 = api_call(page, "PATCH", f"/api/v2/posts/{post_id}", {
        "post": {
            "web_title": draft["title"],
            "email_subject_line": draft["subject"],
            "email_preview_text": draft["preview"],
        }
    })
    if patch1["status"] != 200:
        return False, f"Failed to set metadata: {patch1['status']}"

    # Set scheduled_at
    api_call(page, "PATCH", f"/api/v2/posts/{post_id}", {
        "post": {"scheduled_at": send_utc}
    })

    # Confirm schedule via UI
    page.goto(f"{BEEHIIV}/posts/{post_id}/edit?step=review",
              wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)

    for popup_text in ["Got It!", "Remind me later"]:
        try:
            page.locator(f'button:has-text("{popup_text}")').first.click(timeout=1500)
            time.sleep(0.5)
        except Exception:
            pass

    page.locator('button:has-text("Schedule")').first.click(timeout=5000)
    time.sleep(3)

    try:
        page.locator('text="Schedule for later"').first.click(timeout=2000)
        time.sleep(1)
    except Exception:
        pass

    publish_btn = page.locator('button:has-text("Publish on")')
    if publish_btn.count() > 0:
        publish_btn.first.click(timeout=5000)
    else:
        return False, "No 'Publish on' button found in schedule dialog"

    time.sleep(3)

    try:
        page.locator('button:has-text("Close")').first.click(timeout=3000)
        time.sleep(1)
    except Exception:
        pass

    return True, post_id


def cleanup_broken(page):
    """Delete broken posts (HTML as title, empty content)."""
    resp = api_call(page, "GET", "/api/v2/posts?status=draft&per_page=50")
    if resp["status"] != 200:
        print(f"  Error listing drafts: {resp['status']}")
        return

    posts = resp["data"] if isinstance(resp["data"], list) else resp["data"].get("data", resp["data"].get("posts", []))

    resp2 = api_call(page, "GET", "/api/v2/posts?status=confirmed&per_page=50")
    if resp2["status"] == 200:
        confirmed = resp2["data"] if isinstance(resp2["data"], list) else resp2["data"].get("data", resp2["data"].get("posts", []))
        posts.extend(confirmed)

    broken = []
    for p in posts:
        title = p.get("web_title") or p.get("title") or ""
        subject = p.get("email_subject_line") or p.get("subject_line") or ""
        is_broken = (
            title.startswith("<!DOCTYPE") or
            title.startswith("<") or
            subject.startswith("<!DOCTYPE") or
            title.strip() in ["New post", ""]
        )
        if is_broken:
            broken.append(p)

    print(f"  Found {len(broken)} broken posts to delete")
    for p in broken:
        pid = p["id"]
        title = (p.get("web_title") or p.get("title") or "")[:40]
        del_resp = api_call(page, "DELETE", f"/api/v2/posts/{pid}")
        ok = del_resp["status"] in [200, 204]
        print(f"    {'OK' if ok else 'FAIL'} Deleted {pid[:15]}... ({title})")


def main():
    parser = argparse.ArgumentParser(description="Push newsletters to Beehiiv")
    parser.add_argument("--dry", action="store_true", help="Preview only")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of posts")
    parser.add_argument("--start-date", help="Start date YYYY-MM-DD (default: today)")
    parser.add_argument("--cleanup", action="store_true", help="Delete broken posts")
    args = parser.parse_args()

    drafts = load_drafts()
    start = date.today()
    if args.start_date:
        start = date.fromisoformat(args.start_date)

    if args.limit:
        drafts = drafts[:args.limit]

    print(f"\n{'[DRY RUN] ' if args.dry else ''}{'CLEANUP' if args.cleanup else f'Pushing {len(drafts)} emails'}:\n")

    if not args.cleanup:
        for i, d in enumerate(drafts):
            send = start + timedelta(days=i)
            print(f"  {send.strftime('%a %b %d')}  |  {d['subject']}")

    if args.dry:
        return

    print("\nLaunching browser...\n")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            STATE_DIR,
            headless=False,
            viewport={"width": 1400, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        page.goto(f"{BEEHIIV}/posts", wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)

        if args.cleanup:
            cleanup_broken(page)
            ctx.close()
            return

        success = 0
        for i, draft in enumerate(drafts):
            send = start + timedelta(days=i)
            send_utc = f"{send.strftime('%Y-%m-%d')}T13:00:00Z"  # 9 AM EST = 1 PM UTC

            print(f"  [{i+1}/{len(drafts)}] {send.strftime('%a %b %d')} - {draft['subject']}", flush=True)

            try:
                ok, result = push_post(page, draft, send_utc)
                if ok:
                    print(f"    OK Created + scheduled (post_id: {result})")
                    success += 1
                else:
                    print(f"    FAIL {result}")
            except Exception as e:
                print(f"    ERROR: {str(e)[:80]}")

            time.sleep(2)

        print(f"\nDone! {success}/{len(drafts)} emails pushed and scheduled.")
        ctx.close()


if __name__ == "__main__":
    main()
