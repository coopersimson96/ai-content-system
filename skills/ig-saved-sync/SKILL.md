---
name: ig-saved-sync
version: 1.0.0
description: Sync Instagram saved posts to Notion Inspiration Library with AI analysis
type: standalone-script
env_vars:
  - IG_USERNAME
  - IG_PASSWORD
  - COLLECTION_NAME
  - NOTION_TOKEN
  - NOTION_DB_ID
dependencies:
  - instagrapi
  - yt-dlp
  - openai-whisper
  - claude (CLI)
---

# Instagram Saved → Notion Inspiration Library

Automatically syncs posts from an Instagram saved collection into a Notion Inspiration Library database. Each post gets transcribed (if it's a reel), analyzed by Claude Haiku for hook frameworks and structural patterns, and saved with full metadata.

This runs as a background daemon. You save content on Instagram. It shows up in your Inspiration Library, analyzed and tagged, without you doing anything.

## Permissions

**What it accesses:**
- Your Instagram saved collections (read-only, via instagrapi)
- Your Notion Inspiration Library database (write: creates pages)
- Claude Haiku API (for content analysis, ~$0.01/post)
- yt-dlp + Whisper (local, for reel transcription)

**What it does NOT do:**
- Post, like, comment, or follow on Instagram
- Delete or modify existing Notion pages
- Access any Instagram data beyond your saved collections
- Store credentials anywhere except the local `.env` file

## Prerequisites

1. **Instagram account** with a saved collection containing content you want to analyze
2. **Notion integration** with access to your Inspiration Library database
3. **Claude Code** installed (`npm install -g @anthropic-ai/claude-code`)
4. **Python 3.10+** with pip

## Setup

### 1. Install Dependencies

```bash
cd ~/ai-content-system/skills/ig-saved-sync
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```
IG_USERNAME=your_username
IG_PASSWORD=your_password
COLLECTION_NAME=AI to emulate
NOTION_TOKEN=ntn_your_token
NOTION_DB_ID=your_database_id
```

**Finding your Notion database ID:** Open your Inspiration Library in the browser. The URL looks like `notion.so/your-workspace/abc123def456?v=...`. The `abc123def456` part (32 hex characters) is your database ID.

### 3. First Run (Interactive)

Run status check first to verify everything connects:

```bash
python3 ig-saved-sync.py status
```

Expected output:

```
Instagram Saved Sync — Status
========================================

IG Username: your_username
Collection: AI to emulate
Notion DB: abc123de...
Processed posts: 0

Testing Instagram login...
  IG login: OK
  Collection 'AI to emulate': FOUND
  Posts in collection: 47
  Unprocessed: 47

Testing Notion API...
  Notion DB: OK (Inspiration Library)
```

If your account has 2FA enabled, the first login will prompt for a code. Run `status` interactively to establish the session, then automated runs will reuse it.

### 4. Test With a Single Post

```bash
python3 ig-saved-sync.py backfill --limit 1
```

Check your Notion database. You should see one new entry with:
- Title (descriptive, from Claude analysis)
- Hook text and framework classification
- Performance tier (Outlier/Strong/Reference/Untested)
- Topic tags
- Structural notes
- Caption and transcript in the page body

## Commands

### `run` — Incremental Sync

```bash
python3 ig-saved-sync.py run
```

Processes only new posts added since the last run. Skips anything already in the processed state file. This is what the daily automation runs.

### `backfill` — Import Existing Posts

```bash
python3 ig-saved-sync.py backfill
python3 ig-saved-sync.py backfill --limit 10
python3 ig-saved-sync.py backfill --no-analyze
```

Options:
- `--limit N` — Only process N posts (useful for testing or rate limit concerns)
- `--no-analyze` — Skip Claude analysis, use basic metadata only (faster, cheaper)

### `status` — Check Connections

```bash
python3 ig-saved-sync.py status
```

Verifies Instagram login, collection access, and Notion API connectivity. Shows how many posts are processed vs unprocessed.

## Architecture

```
Instagram Saved Collection
      │
      ▼
┌─────────────┐     ┌──────────────┐     ┌────────────┐
│ Fetch Posts  │────▶│  Transcribe  │────▶│  Analyze   │
│ instagrapi   │     │  yt-dlp +    │     │  Claude    │
│              │     │  whisper     │     │  Haiku     │
└─────────────┘     └──────────────┘     └─────┬──────┘
                                                │
                                                ▼
                                         ┌────────────┐
                                         │   Notion   │
                                         │ Inspiration│
                                         │  Library   │
                                         └────────────┘
```

**Flow per post:**
1. **Fetch** — instagrapi pulls the post metadata (caption, engagement, creator, URL)
2. **Transcribe** — For reels/videos under 90s, yt-dlp downloads audio, Whisper transcribes locally
3. **Analyze** — Claude Haiku receives caption + transcript + metrics, returns structured JSON
4. **Save** — Creates a Notion page with all properties + caption/transcript in the body

If transcription fails, analysis still runs using caption + metadata only. If analysis fails, a basic fallback entry is created from the raw metadata.

## Analysis Output

Each post gets classified into:

| Field | Example |
|-------|---------|
| `title` | "Contrarian ChatGPT Usage Pattern" |
| `type` | Hook Example, Creator Pattern, Script Format, Carousel Example |
| `hook_text` | "Stop using ChatGPT like this..." |
| `hook_framework` | Curiosity Gap, Proof-First, Pain Point, Contrarian, etc. |
| `performance_tier` | Outlier (100K+ views), Strong (10K+), Reference, Untested |
| `tags` | ["AI Tools", "Tutorial", "Productivity"] |
| `notes` | "Opens with contrarian statement. Rapid demo of wrong vs right." |

## Automation

### macOS (launchd)

Copy the template and customize:

```bash
cp launchd-template.plist ~/Library/LaunchAgents/com.user.ig-saved-sync.plist
```

Edit the path in the plist to match your install location, then load it:

```bash
launchctl load ~/Library/LaunchAgents/com.user.ig-saved-sync.plist
```

This runs the sync daily at 11pm. Check logs at `/tmp/ig-saved-sync-stderr.log`.

To stop:
```bash
launchctl unload ~/Library/LaunchAgents/com.user.ig-saved-sync.plist
```

### Linux (cron)

```bash
crontab -e
```

Add:
```
0 23 * * * cd ~/ai-content-system/skills/ig-saved-sync && python3 ig-saved-sync.py run
```

## State Management

The script tracks which posts have been processed in `state/processed.json`. Each entry maps an Instagram media PK to its Notion page ID and sync timestamp.

This means:
- Running `run` multiple times is safe. It skips already-processed posts.
- If you delete a Notion page, the script won't recreate it (it still shows as processed).
- To reprocess a post, remove its entry from `state/processed.json`.
- To start fresh, delete `state/processed.json` entirely.

Session data (Instagram login cookies) is stored in `state/session.json`. This avoids re-authentication on each run. Sessions typically last 2-4 weeks before needing a refresh.

## Security

- All credentials are stored in `.env` (never committed to git)
- Instagram session cookies are in `state/session.json` (local only)
- Claude analysis uses `--max-budget-usd 0.05` per call (cost cap)
- The script uses `--permission-mode bypassPermissions` for Claude since it only needs text analysis (no file access, no tools)
- No data is sent anywhere except Notion and the Claude API
- `.env`, `state/`, and `logs/` should all be in your `.gitignore`

## Troubleshooting

**"2FA required but running non-interactively"**
Run `python3 ig-saved-sync.py status` in a terminal to refresh the session with 2FA.

**"Collection not found"**
The collection name in `.env` must match exactly (case-sensitive). Run `status` to see available collection names.

**"Notion API error 400"**
Usually means a property name in the script doesn't match your database. Check that your Inspiration Library has these properties: Title, Type, Source, Platform, Date Added, Source URL, Creator Handle, Performance Tier, Engagement Metric, Topic Tags, Hook Framework, Hook Text, Notes.

**Transcription fails silently**
Make sure `yt-dlp` and `whisper` are installed. Test with: `python3 -m yt_dlp --version` and `python3 -m whisper --help`.

**Rate limiting from Instagram**
Increase `RATE_LIMIT_SECONDS` in `.env`. Default is 5 seconds between posts. For backfills, it uses 10 seconds. If you're getting blocked, try 15-20.
