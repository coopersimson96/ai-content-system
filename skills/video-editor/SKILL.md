---
name: video-editor
description: >
  9:16 short-form video pipeline using Hyperframes - record, trim, transcribe,
  compose, preview, render. Workflow wrapper around the upstream Hyperframes
  framework. Triggers on: "edit a short", "make a reel", "vertical video",
  "9:16 video", "TikTok video", "Instagram Reel", "Hyperframes video",
  "talking head + motion graphics".
allowed-tools:
  - Read
  - Write
  - Bash
context: conversation
---

# video-editor — 9:16 short-form video pipeline

A workflow wrapper around the Hyperframes framework. You record a talking-head clip on your phone, trim out filler, transcribe to word-level timestamps, compose motion graphics in HTML, preview in a browser, then render an MP4. The skill ships three style archetypes you can apply to any script and a brand spec you override with your own colors and type.

## Prerequisites

- **Node and npm** for running `npx hyperframes ...`
- **ffmpeg** for re-encoding source recordings and pulling poster frames
- The `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, and `gsap` skills installed (these come from upstream - see `THIRD_PARTY.md`)
- The `video-use` skill for conversational trimming of the raw recording
- `npx hyperframes doctor` should pass before you start

## Pipeline overview

```
┌──────────────────────┐
│  1. Record on phone  │
│   raw.mov (1080×1920)│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  2. Trim filler      │
│   /video-use → cuts  │
│   ffmpeg → edited.mp4│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  3. Transcribe       │
│  npx hyperframes     │
│  transcribe → JSON   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  4. Compose HTML     │
│  build_index.py      │
│  + style guide       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  5. Preview          │
│  npx hyperframes     │
│  preview (port 3002) │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  6. Render           │
│  --quality draft     │
│  → standard          │
└──────────────────────┘
```

## Six-step walkthrough

### 1. Record

Shoot a single take on your phone. Speak naturally, mistakes and all. Frame chest-up with the mic visible. Save as `assets/raw.mov` inside a fresh project folder under `video-projects/<your-slug>/`.

### 2. Trim

Use the `video-use` skill to cut filler words, dead air, retakes, and breath gaps. Output is `assets/edited.mp4` - one continuous H.264 file with audio still embedded. Re-encode if needed:

```bash
ffmpeg -i raw.mov -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 192k -movflags +faststart assets/edited.mp4
```

### 3. Transcribe

Word-level timestamps drive the karaoke caption track and the motion-plan beat detection.

```bash
npx hyperframes transcribe assets/edited.mp4 --model small.en --json \
  > assets/transcript.json
```

Compact the output for embedding into HTML. See `templates/words-compact.json.example` for the schema.

### 4. Compose

Pick a style archetype (sage-stack, editorial-magazine, or screen-face-split). Read its `STYLE_DECON.md` for grammar, motion vocabulary, and color rules. Read `overlay-defaults.md` for the default frosted-glass + karaoke pill aesthetic. Use `templates/build_index.py` as the generator - it inlines the transcript JSON into a single `index.html`. Use `templates/MOTION_PLAN.md.template` to plan beats before you write any HTML.

### 5. Preview

```bash
cd video-projects/<your-slug>
npx hyperframes lint    # fix errors before previewing
npx hyperframes preview # opens http://localhost:3002 with hot reload
```

Iterate on the live composition. See `render-contract-gotchas.md` for the four lint walls that block a first preview.

### 6. Render

```bash
npx hyperframes render --quality draft --output renders/draft.mp4
# review the draft, then:
npx hyperframes render --quality standard --output renders/final.mp4
```

Pull frames at hero moments and visually verify before declaring done. Lint passing is not the same as design working.

## The three style archetypes

Each archetype is a deconstruction of a real-world reel format into a reusable motion-graphics playbook. Pick one per project. Don't mix archetypes within a single video.

- **sage-stack** - 9:16 list-explainer with 3D chrome cards, two-voice serif typography, numbered cascade opener, whip-blur transitions, comment-keyword CTA. For tool/concept lists. Read `style-guides/sage-stack/STYLE_DECON.md`.
- **editorial-magazine** - hard top-bottom split with magazine-styled top and naturally-graded talking head bottom, italic-serif single-word captions, numbered rows with one-row color-break. For essays and curated breakdowns. Read `style-guides/editorial-magazine/STYLE_DECON.md`.
- **screen-face-split** - hard horizontal split, top half rotates between screen recording / bold headline / custom dashboard, bottom half is a continuous naturally-graded speaker, bold-sans captions with single-word color emphasis. For tool demos and ad-style content. Read `style-guides/screen-face-split/STYLE_DECON.md`.

If none of the three fit, build your own. See `style-guides/BUILD_YOUR_OWN.md`.

## Overlay defaults

The frosted orange-glass card + light-purple karaoke pill aesthetic is the default for any short-form video. It survived eight rounds of iteration. Apply on the first render, override only when a specific video calls for something else. Full spec in `overlay-defaults.md`.

## Render contract

Hyperframes has a strict render contract. Four lint errors block first preview every time - audio echo from split files, video nested in a timed wrapper, missing media id, and overlapping clips on the same track. The fixes are short. Read `render-contract-gotchas.md` before authoring any audio/video element.

## Build your own style guide

Three archetypes won't cover everything. To deconstruct a creator's reel into a reusable archetype, follow `style-guides/BUILD_YOUR_OWN.md` - download reference reels, extract frames, identify recurring patterns, write the deconstruction, encode patterns into JSON.
