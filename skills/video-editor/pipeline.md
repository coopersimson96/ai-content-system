# Pipeline — End-to-End

The full record-to-render pipeline for a 9:16 short-form video. Six steps, each owned by a different tool, glued together through the file system.

## Project layout

Every video is a self-contained folder under `video-projects/<your-slug>/`:

```
video-projects/<your-slug>/
├── index.html              # generated composition
├── build_index.py          # generator (templates HTML + inlines JSON)
├── words-compact.json      # transcript chunks (input to generator)
├── MOTION_PLAN.md          # beat-by-beat plan
├── compositions/           # sub-compositions if you split scenes
├── assets/
│   ├── raw.mov             # phone recording (gitignored)
│   ├── edited.mp4          # trimmed take with audio embedded
│   ├── transcript.json     # word-level timestamps from Hyperframes
│   └── brand-tokens.css    # CSS variables for your palette
├── renders/                # output MP4s (gitignored)
├── hyperframes.json        # CLI config
└── meta.json               # project id, dimensions, fps
```

Always run the CLI from inside the project folder. The CLI reads `hyperframes.json` and `meta.json` from the current directory.

---

## Step 1 — Record

Shoot one continuous take on your phone. Frame chest-up. Mic visible (lavalier or shotgun). Speak naturally. If you flub a line, restate and keep going - you'll cut the bad takes in the next step.

Save as `assets/raw.mov`. Don't pre-edit. Don't trim in your phone's gallery app. The cleaner the source, the cleaner the trim.

---

## Step 2 — Trim

Use the `video-use` skill to remove filler words, dead air, retakes, and breath gaps. Talk to it conversationally:

> "Cut every 'um' and 'uh', remove pauses longer than 0.4s, and drop the false start at 0:08."

Output: `assets/edited.mp4`. One continuous H.264 file with audio still in the same container.

If you need to re-encode manually (raw codec issues, weird HDR profile, non-standard fps):

```bash
ffmpeg -i raw.mov \
  -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  assets/edited.mp4
```

**Important:** keep audio inside the mp4 container. Splitting audio into a sibling `.m4a` file produces a ~25ms phase delay heard as echo in the final render. See `render-contract-gotchas.md` section 1.

---

## Step 3 — Transcribe

Word-level timestamps drive everything downstream - karaoke captions sync to them, motion-plan beat detection uses them to align graphics to spoken phrases.

```bash
npx hyperframes transcribe assets/edited.mp4 --model small.en --json \
  > assets/transcript.json
```

Compact the output for embedding. The schema groups words into chunks (one chunk per spoken phrase, ~5 words each). See `templates/words-compact.json.example` for an example chunk.

---

## Step 4 — Compose

This is where you write the motion graphics. The work has three sub-stages:

### 4a. Pick an archetype

Read `style-guides/README.md` and pick the archetype whose format and grammar fit your script.

- **sage-stack** for list-style scripts with 3+ enumerated items
- **editorial-magazine** for essays / framework explanations / curated breakdowns
- **screen-face-split** for live tool demos or ad-register hooks
- Or build your own - see `style-guides/BUILD_YOUR_OWN.md`

### 4b. Plan the beats

Copy `templates/MOTION_PLAN.md.template` to your project as `MOTION_PLAN.md`. Walk through your transcript and assign one pattern per beat from your archetype's `patterns.json`. Each beat row names the time range, the spoken transcript, the intent (hook / list-preview / claim / etc.), the matching pattern, and any params the pattern needs.

The plan is for humans. It catches structural problems before you write HTML.

### 4c. Build index.html

Copy `templates/build_index.py` and `templates/index.html.template` into your project. The build script inlines the compact words JSON into the HTML via a `__WORDS_JSON__` placeholder - lets you edit the HTML structure without ever pasting transcript data into it.

Run the script after every CSS or HTML edit:

```bash
python3 build_index.py
```

This is the pattern that survives lint and renders deterministically.

---

## Step 5 — Preview

Before any render, eyeball the live composition:

```bash
cd video-projects/<your-slug>
npx hyperframes lint              # fix all errors before previewing
npx hyperframes preview           # opens http://localhost:3002 with hot reload
```

Lint walls that block first preview:

1. **Audio echo** from split files - keep audio embedded in the mp4
2. **Video nested in timed wrapper** - put `data-start` on either the wrapper OR the video, not both
3. **Missing media id** - every `<video>` and `<audio>` needs an `id`
4. **Overlapping clips on same track** - bump `data-track-index` on conflicting clips

Full diagnoses and fixes in `render-contract-gotchas.md`.

Hot reload picks up edits without a restart. Iterate freely on the live preview before paying any render cost.

---

## Step 6 — Render

Two render qualities you'll use:

```bash
# Fast iteration (CRF 28, ~30s for a 60s reel)
npx hyperframes render --quality draft --output renders/draft.mp4

# Visually lossless 1080p (CRF 18, ~2 min for a 60s reel)
npx hyperframes render --quality standard --output renders/final.mp4
```

After draft, do a visual verification pass:

1. Pull one frame per scene at its hero moment via `ffmpeg -ss <t> -i renders/draft.mp4 -frames:v 1 ...`
2. Open every PNG and confirm no cropped face, no text overflow, no scene landing on the wrong word, captions readable, all transitions clean
3. Re-render if anything is wrong. Never let a "successful" render with a broken frame ship.

Then run `--quality standard` for the final.

---

## Pacing the loop

For a 60-second reel:

| Step | Wall time | Tools |
|------|-----------|-------|
| 1. Record | ~5 min (one or two takes) | phone |
| 2. Trim | ~5 min | `video-use` |
| 3. Transcribe | ~30 sec | `hyperframes transcribe` |
| 4. Compose | ~30-60 min for first build, ~10 min for revisions | text editor + `build_index.py` |
| 5. Preview | continuous during step 4 | `hyperframes preview` |
| 6. Render | ~2 min | `hyperframes render` |

First build is the expensive one. Revisions are cheap once the composition exists.
