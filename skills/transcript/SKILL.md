---
name: transcript
description: Extract transcripts from any video URL — YouTube, TikTok, Instagram, X, Facebook, or direct file links. Also fetches metadata (title, author, stats). Supports batch transcripts, translation, and YouTube search.
argument-hint: "[video URL]" or "playlist [URL]" or "translate [URL] to [language]" or "search [topic] on YouTube"
context: conversation
---

# Transcript Extractor — SupaData API

Extract transcripts from any video platform with one command. Paste a URL, get the transcript.

---

## Config

- **API key file:** `~/.config/supadata/.env` (contains `SUPADATA_API_KEY=...`)
- **Base URL:** `https://api.supadata.ai/v1`
- **Auth header:** `x-api-key: <key>`

Before making API calls, read the key:
```bash
SUPADATA_API_KEY=$(grep SUPADATA_API_KEY ~/.config/supadata/.env | cut -d= -f2)
```

Use this variable in all curl commands below.

---

## Input Parsing

Extract from user input or `$ARGUMENTS`:

1. **URL** — The video/content URL
2. **MODE** — What the user wants:
   - **transcript** (default) — Get transcript + metadata for a single URL
   - **batch** — Get transcripts for a playlist, channel, or list of URLs
   - **translate** — Get transcript translated to a target language (YouTube only)
   - **search** — Search YouTube for videos, then optionally get transcripts
   - **metadata-only** — Just get metadata (title, stats, author) without transcript
3. **LANGUAGE** — Target language if translating (ISO 639-1 code, e.g., "es", "fr", "de")
4. **FORMAT** — `text` (plain text, default) or `timestamped` (chunks with timestamps)

**If no URL provided**, ask:

> What video do you want the transcript for? Paste the URL.
>
> Supported: YouTube, TikTok, Instagram, X/Twitter, Facebook, or any direct video/audio file URL.

**If only a URL is provided**, default to transcript + metadata, plain text format. Don't over-ask.

---

## Platform Detection

Detect the platform from the URL to route correctly:

| URL Pattern | Platform |
|---|---|
| `youtube.com`, `youtu.be`, `youtube.com/shorts/`, `youtube.com/live/` | YouTube |
| `tiktok.com`, `vm.tiktok.com` | TikTok |
| `instagram.com/reel/`, `instagram.com/p/`, `instagram.com/tv/` | Instagram |
| `twitter.com`, `x.com` | X/Twitter |
| `facebook.com`, `m.facebook.com` | Facebook |
| `.mp4`, `.webm`, `.mp3`, `.wav`, `.flac`, `.m4a`, `.ogg`, `.mpeg` | Direct File |
| `youtube.com/playlist`, playlist ID | YouTube Playlist |
| `youtube.com/@`, `youtube.com/channel/` | YouTube Channel |
| Everything else (non-video URL) | Web page → use `/web/scrape` fallback |

---

## Single Transcript Extraction

This is the primary flow — one URL, one transcript.

### Step 1: Fetch Metadata

```bash
SUPADATA_API_KEY=$(grep SUPADATA_API_KEY ~/.config/supadata/.env | cut -d= -f2)
URL="THE_VIDEO_URL"
curl -s -H "x-api-key: $SUPADATA_API_KEY" \
  "https://api.supadata.ai/v1/metadata?url=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$URL', safe=''))")"
```

Display a header with the metadata:
```
**{title}**
{author} · {platform} · {duration} · {views} views · {likes} likes
Published: {date}
```

### Step 2: Fetch Transcript

**For YouTube URLs**, use the dedicated YouTube endpoint (more features):
```bash
SUPADATA_API_KEY=$(grep SUPADATA_API_KEY ~/.config/supadata/.env | cut -d= -f2)
curl -s -H "x-api-key: $SUPADATA_API_KEY" \
  "https://api.supadata.ai/v1/youtube/transcript?url=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$URL', safe=''))")&text=true"
```

**For all other platforms** (TikTok, Instagram, X, Facebook, files), use the universal endpoint:
```bash
SUPADATA_API_KEY=$(grep SUPADATA_API_KEY ~/.config/supadata/.env | cut -d= -f2)
curl -s -H "x-api-key: $SUPADATA_API_KEY" \
  "https://api.supadata.ai/v1/transcript?url=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$URL', safe=''))")&text=true"
```

### Step 3: Handle Async Jobs

If the API returns HTTP 202 with a `jobId`, the transcript is being generated asynchronously (common for non-YouTube platforms and long videos):

```bash
# Poll every 5 seconds until complete
curl -s -H "x-api-key: $SUPADATA_API_KEY" \
  "https://api.supadata.ai/v1/transcript/$JOB_ID"
```

Poll until `status` is `completed` or `failed`. Max 12 attempts (60 seconds).

### Step 4: Display and Save

Show the full transcript in the conversation.

Save to file:
```bash
# Filename: ~/ai-content-system/output/transcripts/{platform}-{sanitized-title}-transcript.md
```

The saved file should include:
```markdown
# {Title}
**{Author}** · {Platform} · {Duration} · {Views} views
**URL:** {original URL}
**Extracted:** {date}

---

{full transcript text}
```

---

## Timestamped Format

If user asks for timestamps, use `text=false` in the API call. The response returns chunks:

```json
[{"text": "chunk text", "offset": 0, "duration": 5000, "lang": "en"}]
```

Format as:
```
[0:00] chunk text
[0:05] next chunk
```

---

## Translation (YouTube Only)

When user asks to translate a transcript:

```bash
SUPADATA_API_KEY=$(grep SUPADATA_API_KEY ~/.config/supadata/.env | cut -d= -f2)
curl -s -H "x-api-key: $SUPADATA_API_KEY" \
  "https://api.supadata.ai/v1/youtube/transcript/translate?url=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$URL', safe=''))")&lang=$LANG_CODE&text=true"
```

Note: Translation takes 20+ seconds and costs 30 credits/minute. Warn the user about the higher cost if the video is long.

Common language codes: `es` (Spanish), `fr` (French), `de` (German), `pt` (Portuguese), `ja` (Japanese), `ko` (Korean), `zh` (Chinese), `ar` (Arabic), `hi` (Hindi), `it` (Italian).

---

## Batch Transcripts (YouTube Only)

For playlists, channels, or multiple videos:

```bash
source ~/.config/supadata/.env
# For a playlist:
curl -s -X POST -H "x-api-key: $SUPADATA_API_KEY" -H "Content-Type: application/json" \
  -d '{"playlistId": "$PLAYLIST_URL", "text": true, "limit": 10}' \
  "https://api.supadata.ai/v1/youtube/transcript/batch"

# For a channel:
curl -s -X POST -H "x-api-key: $SUPADATA_API_KEY" -H "Content-Type: application/json" \
  -d '{"channelId": "$CHANNEL_URL", "text": true, "limit": 10}' \
  "https://api.supadata.ai/v1/youtube/transcript/batch"

# For multiple video IDs:
curl -s -X POST -H "x-api-key: $SUPADATA_API_KEY" -H "Content-Type: application/json" \
  -d '{"videoIds": ["id1", "id2", "id3"], "text": true}' \
  "https://api.supadata.ai/v1/youtube/transcript/batch"
```

Then poll for results:
```bash
curl -s -H "x-api-key: $SUPADATA_API_KEY" \
  "https://api.supadata.ai/v1/youtube/batch/$JOB_ID"
```

Save each transcript as a separate file in `~/ai-content-system/output/transcripts/batch-{topic}/`.

---

## YouTube Search → Transcript

When user wants to find and transcribe videos on a topic:

```bash
SUPADATA_API_KEY=$(grep SUPADATA_API_KEY ~/.config/supadata/.env | cut -d= -f2)
curl -s -H "x-api-key: $SUPADATA_API_KEY" \
  "https://api.supadata.ai/v1/youtube/search?query=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY', safe=''))")"
```

Show the results and ask which video(s) to transcribe. Then run the single transcript flow for each selected video.

---

## Web Page Fallback

If the URL is not a video platform, fall back to web scraping:

```bash
SUPADATA_API_KEY=$(grep SUPADATA_API_KEY ~/.config/supadata/.env | cut -d= -f2)
curl -s -H "x-api-key: $SUPADATA_API_KEY" \
  "https://api.supadata.ai/v1/web/scrape?url=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$URL', safe=''))")"
```

Returns the page content as markdown. Useful for blog posts, articles, docs.

---

## Error Handling

| HTTP Code | Meaning | Action |
|---|---|---|
| 200 | Success | Display transcript |
| 202 | Async job started | Poll with jobId until complete |
| 206 | No transcript available | Tell user: "No captions available for this video. The video may be too short, have no speech, or captions are disabled." |
| 400 | Bad request | Check URL format |
| 401 | Invalid API key | Tell user to check `~/.config/supadata/.env` |
| 402 | Out of credits | Tell user to check their SupaData plan |
| 404 | Video not found | Tell user: "Video not found — it may be private, deleted, or the URL is wrong." |
| 429 | Rate limited | Wait 10 seconds, retry once |

---

## Follow-Up Behavior

After showing a transcript, offer relevant next steps based on context:

- **"Summarize this"** → Summarize the key points from the transcript
- **"Extract the main arguments"** → Pull out structured takeaways
- **"Get another video"** → Ready for the next URL
- **"Get the whole playlist"** → Switch to batch mode
- **"Translate to [language]"** → Use translation endpoint (YouTube only)

If the user is working on content (e.g., came from `/content-master`), proactively suggest how the transcript could inform their scripts.
