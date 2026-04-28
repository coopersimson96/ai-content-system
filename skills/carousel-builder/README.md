# Carousel Builder

A Claude Code skill that turns a reel script (or any rough content) into a publish-ready Instagram carousel using the **reference-first workflow** and the kie.ai gpt-image-2 MCP for image generation.

## What this skill does

- Forces you to write the **copy first**, before any image generation
- Builds a locked **visual brief** that every slide inherits
- Generates **3 distinct slide-1 anchors**, then waits for you to pick one
- Generates the rest of the slides **one at a time**, each anchored to slide 1
- Runs a **consistency check** at the end and only regenerates weak slides

This is the antidote to the "make me a 6-slide carousel about X" failure mode where every slide looks like it came from a different brand.

## What this skill needs

| Thing | Why |
|---|---|
| Claude Code | the skill runs as a Claude Code skill |
| **kie.ai gpt-image-2 MCP** | for actual image generation (steps 7–9) |
| Python 3 + Pillow | for the 3:4 → 4:5 crop script |

Steps 1–6 (copy, plan, brief) work without the MCP. Image steps require it.

## Quick start

```bash
# 1) Install the kie.ai MCP (sign up at kie.ai for an API key)
npm install -g kie-image-mcp

# 2) Add the MCP to your Claude Code config
#    See https://kie.ai docs for the exact JSON snippet

# 3) Install Pillow for the crop script
python3 -m pip install Pillow

# 4) In Claude Code, invoke the skill:
#    "build me a carousel from this script: ..."
```

## File map

```
skills/carousel-builder/
├── SKILL.md                          # Claude Code entry point — read this first
├── README.md                         # this file
├── references/
│   ├── workflow-8-steps.md           # the why behind the workflow
│   ├── style-field-manual.md         # the one shipping style skin (reference)
│   ├── build-your-own-skin.md        # how to build your own skin from a design board
│   ├── graphic-decision-tree.md      # 8 graphic types and when to use each
│   └── consistency-checklist.md      # final QA pass before posting
├── templates/
│   ├── intake.md                     # filled into 01-strategy.md
│   ├── slide-copy.md                 # filled into 02-slide-copy.md
│   ├── visual-brief.md               # filled into 05-visual-brief.md
│   ├── slide-1-anchor-prompt.md      # 3-variant cover prompt
│   ├── slide-N-prompt.md             # anchored slide prompt
│   ├── refinement-prompt.md          # KEEP / CHANGE / DO NOT TOUCH template
│   └── consistency-check.md          # filled into 08-consistency-check.md
└── scripts/
    ├── new_carousel.py               # scaffold a new carousel folder from templates
    └── crop_to_4x5.py                # crop 1080x1440 → 1080x1350 for IG
```

## Hard rules (don't break these)

1. **Copy before pixels.** Slide copy is finished before any image is generated.
2. **Three anchors, then stop.** The skill always pauses after generating 3 slide-1 variants, waits for you to lock one.
3. **One slide at a time after the anchor.** Never batch.
4. **No invented assets.** Logos, UI screenshots, and product shots must be real or left as `TBD` placeholders.
5. **Lock the visual spec.** Every slide 2..N prompt copies the brief's palette/type/grid/motif block verbatim.
6. **Regen only the weak.** The consistency check flags them; everything else stays.

## License

Same license as the parent repo.
