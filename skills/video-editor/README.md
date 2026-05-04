# video-editor

A 9:16 short-form video pipeline built on top of Hyperframes. Record on your phone, trim the filler, transcribe to word-level timestamps, compose motion graphics in HTML, preview live, render an MP4.

This is a **workflow wrapper** - the heavy lifting is done by the upstream Hyperframes framework (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `gsap`). See `THIRD_PARTY.md` for attribution.

## What you get

- A six-step pipeline from raw phone recording to rendered MP4
- Three style archetypes (`sage-stack`, `editorial-magazine`, `screen-face-split`) - each a complete motion-graphics playbook with its own pattern library
- A frosted-glass + karaoke-pill overlay default that's survived real iteration
- Templates for the build script, transcript schema, and beat-by-beat motion plan
- A guide to deconstructing your own reference reels into a new archetype

## Quick start

1. Install the upstream Hyperframes skills (`hyperframes`, `hyperframes-cli`, `gsap`, etc.)
2. Install `video-use` for conversational trimming
3. Copy `templates/build_index.py` and `templates/MOTION_PLAN.md.template` into a new project folder
4. Read `SKILL.md` for the full walkthrough

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Frontmatter + full walkthrough |
| `pipeline.md` | Detailed end-to-end pipeline |
| `motion-philosophy.md` | The 11 motion laws |
| `overlay-defaults.md` | The frosted-glass + karaoke pill aesthetic |
| `render-contract-gotchas.md` | Four lint walls + fixes |
| `templates/build_index.py` | Generic HTML builder that inlines transcript JSON |
| `templates/words-compact.json.example` | Transcript schema example |
| `templates/index.html.template` | Structural HTML reference |
| `templates/MOTION_PLAN.md.template` | Beat-by-beat plan template |
| `style-guides/README.md` | How to use style guides |
| `style-guides/BRAND.md.example` | Brand spec template |
| `style-guides/BUILD_YOUR_OWN.md` | How to deconstruct a reference reel |
| `style-guides/sage-stack/` | List-explainer archetype |
| `style-guides/editorial-magazine/` | Magazine-spread archetype |
| `style-guides/screen-face-split/` | Hard-split tool-demo archetype |
| `THIRD_PARTY.md` | Hyperframes attribution |
