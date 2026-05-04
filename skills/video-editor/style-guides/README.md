# Style Guides

Reusable visual / motion deconstructions of reference reel formats. Each subfolder contains a complete style guide for a specific aesthetic, with a markdown deconstruction (`STYLE_DECON.md`) and a machine-readable pattern library (`patterns.json`).

## How to use

When starting a new video project, pick the closest-matching style guide and read its `STYLE_DECON.md` before brainstorming. Each guide follows the same structure (10 Laws → Timeline → Visual Vocabulary → Type System → Color Story → Motion Patterns → Recipes → Pre-flight) so they slot directly into the Hyperframes authoring loop.

Apply the **format** (grammar, pacing, structure) but swap the **brand** (palette, type, accent colors) to match your own spec - see `BRAND.md.example` for the brand template, and each archetype's "Brand Adaptation" section for archetype-specific overrides.

## Available guides

| Guide | Format | One-line essence |
|-------|--------|------------------|
| [sage-stack](./sage-stack/STYLE_DECON.md) | 9:16, ~50s, list explainer | Talking head + sage 3D chrome cards, two-voice serif typography, numbered cascade opener, whip-blur transitions, comment-keyword CTA |
| [editorial-magazine](./editorial-magazine/STYLE_DECON.md) | 9:16, 50-90s, magazine-style explainer | Print-quarterly layouts stacked above a naturally-graded talking head, italic-serif single-word captions, numbered rows with one-row color-break flagging the exception |
| [screen-face-split](./screen-face-split/STYLE_DECON.md) | 9:16, 30-220s, hybrid ad/tutorial | Hard horizontal split: top half rotates between screen recording / bold headline card / custom dashboard; bottom half is a continuous naturally-graded talking head. Bold-sans captions with single-word color emphasis |

## When to use which

- **sage-stack** - script enumerates a list of tools / concepts (3+), needs design polish, "comment X" CTA, list-style breakdown
- **editorial-magazine** - script reads like an essay or framework explanation, needs editorial credibility, slower per-beat dwell time, magazine-style chapter framing
- **screen-face-split** - script demonstrates a tool live (screen recording is essential), or it's an ad where a bold headline + product surface + talking head all need to coexist in the same frame

## Adding a new guide

When none of the three fit your script, deconstruct a creator whose aesthetic you admire into a fourth archetype. Full walkthrough in [`BUILD_YOUR_OWN.md`](./BUILD_YOUR_OWN.md).

The new guide goes in a fresh subfolder:

```
style-guides/<your-archetype-slug>/
├── STYLE_DECON.md      # the deconstruction (follow the 10-section structure)
├── patterns.json       # machine-readable pattern library
└── sources/            # reference reel frames (gitignored if heavy)
    └── <reel-id>/
        ├── source.mp4  # the reference reel (DO NOT commit if it's not yours)
        └── frames/     # extracted stills
```

Then add a row to the table above and a "When to use" entry.

## Brand spec

`BRAND.md.example` is the template for your project's brand spec. Fork it and fill in your own palette / type / texture. Each archetype's `STYLE_DECON.md` defers to your brand spec for color and type, owning only the format and grammar.
