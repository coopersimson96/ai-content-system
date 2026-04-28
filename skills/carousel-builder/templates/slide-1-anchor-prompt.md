# Slide 1 Anchor Prompt — 3 variants

Run this **three times** with the same copy. Generate three visually distinct cover concepts. Save as `images/anchor-v1.png`, `-v2.png`, `-v3.png`. Show the user, wait for them to lock one.

Tool: `mcp__kie-image__generate_image`
Aspect ratio: `"3:4"` (kie has no 4:5 — crop after with `scripts/crop_to_4x5.py`).

---

## Prompt template

```
Create slide 1 of an Instagram carousel — the cover hook slide.

CAROUSEL TOPIC:
[insert sharp idea from 01-strategy.md]

AUDIENCE:
[insert audience]

SLIDE GOAL:
Stop the scroll and make people swipe.

EXACT TEXT TO RENDER ON SLIDE (render only this text, do not add any other words):
- Headline: "[insert headline from 02-slide-copy.md]"
- Highlight word(s) flip to accent color: "[insert highlight word(s)]"
- Support line: "[insert support line]"
- Bottom note: "[insert bottom note]"

[paste the LOCKED SPEC BLOCK from 05-visual-brief.md here verbatim]

VISUAL REFERENCE BORROW / DO NOT COPY:
Borrow from references: typography hierarchy, spacing, colour treatment, texture, visual pacing, layout logic, graphic components.
Do not copy: exact text, exact branding, exact graphics, exact compositions.

VARIANT INSTRUCTIONS (apply ONE per generation):
- Variant A — [concept name, e.g. "Field manual cover"]: [1-line layout description, e.g. "headline dominates 70% of canvas, mascot in lower-right corner, dark panel callout for support line"]
- Variant B — [concept name, e.g. "Stack-card cover"]: [1-line description, e.g. "headline upper-third, three labelled cards bottom-third, no mascot"]
- Variant C — [concept name, e.g. "Evidence cover"]: [1-line description, e.g. "headline left-half, source proof panel right-half"]

RULES:
- Render only the exact text above.
- Do not add random words, decorative words, or "lorem ipsum"-style filler.
- All text must be legible at thumb-scroll size.
- Make this variant visually distinct from the other two — different composition, different motif emphasis.
- Do not copy any reference image directly.
- Format: 3:4 vertical (1080x1440). Generous outer margin per spec.
- Designed but not corporate. Editorial. High readability.
```

## How to call

For each variant A / B / C:

1. Fill in the prompt with the right **VARIANT INSTRUCTIONS** line for that letter.
2. Call `mcp__kie-image__generate_image` with `aspect_ratio: "3:4"` and the filled prompt.
3. Move/copy the resulting file from `~/Documents/kie_generated/` (or wherever your kie MCP saves) to `images/anchor-v1.png` (or v2/v3) inside the carousel folder.
4. Run `python3 scripts/crop_to_4x5.py images/anchor-v1.png` to produce the cropped preview.

## Stop point

After all three are generated, write them to `06-anchor-options.md` with image paths and layout descriptions, then **pause and ask the user to lock one** (or request refinement).

Do not proceed to slide 2 until the anchor is locked.
