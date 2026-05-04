# Third-party attribution

The `video-editor` skill is a **thin workflow wrapper** around the upstream Hyperframes framework. The heavy lifting - composition primitives, timeline registration, render engine, transcribe and TTS pipelines, registry blocks - is all done by Hyperframes itself.

## Hyperframes

**Author:** Nate Herkai / HeyGen
**Upstream repo:** https://github.com/heygen-com/hyperframes
**Documentation:** https://hyperframes.heygen.com/introduction
**License:** see upstream repo

Hyperframes provides:

- The HTML composition format (`data-composition-id`, `data-start`, `data-duration`, `data-track-index`)
- The `npx hyperframes` CLI (`init`, `add`, `lint`, `preview`, `render`, `transcribe`, `tts`, `doctor`, `compositions`, `catalog`)
- The render engine that turns timed HTML compositions into deterministic MP4s
- The registry of 38 blocks (data-chart, flowchart, whip-pan, cinematic-zoom, glitch, light-leak, app-showcase, logo-outro, etc.) and 3 components (grain-overlay, shimmer-sweep, grid-pixelate-wipe)
- Word-level transcription via Whisper integration
- On-device TTS via Kokoro-82M

## Skills you'll need installed alongside this one

These are upstream Hyperframes skills (not part of `video-editor`). Install via the Hyperframes repo or whichever skill registry you're using:

| Skill | What it does |
|-------|-------------|
| `hyperframes` | Authoring and editing compositions, captions, TTS, audio-reactive animation, transitions |
| `hyperframes-cli` | Wraps the CLI commands - init, lint, preview, render, transcribe, tts, doctor |
| `hyperframes-registry` | Installing catalog blocks and components into your project |
| `gsap` | GSAP animation reference - timelines, easing, stagger, plugins, performance |
| `website-to-hyperframes` | Turning a URL into a composition (separate flow from the `video-editor` workflow) |

If you also use the `claude-design-hyperframes` skill, that's a Claude Design specific variant of `hyperframes` - same upstream attribution.

## What `video-editor` adds on top

This skill does NOT reimplement any of the above. It documents:

- A six-step pipeline (record → trim → transcribe → compose → preview → render) that wraps the Hyperframes CLI
- Three style archetypes (sage-stack, editorial-magazine, screen-face-split) with their own pattern libraries
- A frosted-glass + karaoke-pill overlay default that survived eight rounds of iteration
- Templates for the build script, transcript schema, motion plan, and HTML structure
- A guide to building your own style archetypes

All credit for the underlying framework goes to the Hyperframes team. This wrapper is a workflow on top.

## Other tools mentioned

- **`video-use`** - conversational video editor (transcribe, cut, color grade, generate overlay animations, burn subtitles). Used for step 2 (trim) of the pipeline. Standalone skill.
- **`ffmpeg`** - public-domain video toolkit. Used for re-encoding and frame extraction.
- **`yt-dlp`** - public-domain video downloader. Mentioned in `style-guides/BUILD_YOUR_OWN.md` for downloading reference reels.
- **GSAP** - GreenSock Animation Platform. The animation library Hyperframes uses internally. Already referenced via the `gsap` skill above.
