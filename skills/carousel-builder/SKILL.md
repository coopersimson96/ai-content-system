---
name: carousel-builder
description: Use when creating Instagram carousels from a reel script, handout, PDF, article, or rough idea. Triggers on "carousel", "Instagram carousel", "IG carousel", "turn this script into slides", "build a carousel", "make slides for IG", "anchor slide", "visual brief". Runs the reference-first workflow (copy → brief → 3 anchor variants → locked anchor → matched slides one at a time → consistency check) and generates real images via the kie.ai gpt-image-2 MCP. Skip for plain captions or non-designed multi-slide posts.
argument-hint: paste a script + style skin + slide count + CTA
---

# Carousel Builder

Turn a script + handout into a publish-ready Instagram carousel using the **reference-first workflow** and the kie.ai gpt-image-2 MCP.

## The non-negotiable rule

**Never batch-generate the whole carousel.**

The model is not the problem. The brief is. Write the copy first. Build the visual brief. Generate three slide-1 anchors. Wait for the user to lock one. Then build the rest, one slide at a time, anchored to slide 1.

If you ever feel the urge to "just generate all 6 slides at once," stop. That's the failure mode this skill exists to prevent.

## Prerequisites

This skill depends on the **kie.ai gpt-image-2 MCP**. Install it before running this skill:

- Sign up at https://kie.ai and grab an API key
- Install the MCP server (Node 18+): `npm install -g kie-image-mcp`
- Add to your Claude Code MCP config with your API key

Without the MCP, the image-generation steps will fail. Steps 1–6 (copy + brief) still work without it.

## Inputs you need

Read `templates/intake.md` for the full schema. Minimum:
- **script** (the reel/post the carousel is based on)
- **style skin** (`field-manual` ships with this skill; build your own per `references/build-your-own-skin.md`)
- **slide count** (6–9)
- **CTA + keyword**
- **handout/source material** (optional but strongly recommended)
- **required source assets** (logos, screenshots — call them out)

If anything blocks progress, ask one concise follow-up. Otherwise proceed with reasonable defaults.

## Output location

Every carousel gets its own folder. Default root is `~/carousels/` but you can pass `--root` to `scripts/new_carousel.py` to put them anywhere.

```
~/carousels/YYYY-MM-DD-slug/
  01-strategy.md          # sharp idea, audience, promise
  02-slide-copy.md        # exact text per slide
  03-graphic-plan.md      # graphic type per slide (uses references/graphic-decision-tree.md)
  04-asset-list.md        # logos, screenshots, source refs to gather
  05-visual-brief.md      # full brief from templates/visual-brief.md
  06-anchor-options.md    # 3 slide-1 prompts + generated images
  07-slide-prompts.md     # locked spec + per-slide prompts (filled after anchor lock)
  08-consistency-check.md # final QA
  images/
    anchor-v1.png, anchor-v2.png, anchor-v3.png
    anchor-locked.png
    slide-2.png ... slide-N.png
    final/                # post-cropped 1080x1350 deliverables
```

Use `python3 scripts/new_carousel.py "<title>"` to scaffold the folder.

## The 9-step process (run in order, don't skip)

### 1. Intake
Capture or infer everything in `templates/intake.md`. Save to `01-strategy.md` later. If the user pasted a script, extract topic + audience automatically.

### 2. Extract one sharp idea
Reduce the script to **one specific point**. Not a topic, a thesis.
- Bad: "AI prompting"
- Best: "Anthropic's own prompting playbook says strong prompts are structured: role + examples + don'ts"

Write it to `01-strategy.md` with: sharp idea, audience promise, why it matters, intended action.

### 3. Write the slide copy first
**Don't open the image generator yet.** Use `templates/slide-copy.md`. Each slide gets:
- slide number + role (hook / problem / sauce / rule / formula / CTA)
- headline (the big text)
- support line (1–2 lines under)
- optional bottom note (corner metadata, e.g. "01 / 06", "SWIPE →")
- visual purpose (what this slide should *show*)

Default 6-slide arc: Hook → Problem → Sauce → Anchor rule → Formula → CTA.
Default 8-slide arc: Hook → Source → Point 1 → Point 2 → Point 3 → Formula → What's missing → CTA.

Save to `02-slide-copy.md`.

### 4. Pick a graphic type per slide
For each slide, choose a graphic type from `references/graphic-decision-tree.md`:
proof card · prompt box · before/after · stack diagram · checklist grid · evidence teardown · CTA poster · oversized typography poster.

Save to `03-graphic-plan.md`.

### 5. Build the asset list
List every external asset the carousel needs: logos, product screenshots, official docs, source articles. Mark each as **needed** (must source) or **on hand** (user provided).

**Never invent logos, fake UI, or fake screenshots.** If the user can't provide them, mark the asset as TBD and proceed without it on that slide.

Save to `04-asset-list.md`.

### 6. Build the visual brief
Pick a style skin. The skill ships with `references/style-field-manual.md` as a reference. To build your own skin from inspiration boards, follow `references/build-your-own-skin.md`.

Fill `templates/visual-brief.md` with:

- format: 3:4 source (1080×1440) → cropped to 4:5 final (1080×1350)
- exact palette (hex)
- typography direction
- background + texture
- layout grid + margins
- recurring motifs (your brand mark, asterisk, evidence panels, etc.)
- footer/header metadata system
- forbidden elements
- the **borrow / do not copy** split for any visual references

Save to `05-visual-brief.md`. **This file is the source of truth for every later prompt.**

### 7. Generate 3 slide-1 anchor variants
Use `templates/slide-1-anchor-prompt.md`. Same copy across all three; visually distinct concepts.

Run via `mcp__kie-image__generate_image`:
- aspect_ratio: `"3:4"` (kie doesn't support 4:5 directly)
- save the three result paths to `images/anchor-v1.png`, `-v2.png`, `-v3.png`
- crop each to 1080×1350 with `scripts/crop_to_4x5.py` for preview

Write the three prompts and image paths to `06-anchor-options.md`.

**STOP. Show the user the three anchors. Wait for them to pick one (or request refinement).** Do not proceed to step 8 until the anchor is locked.

### 8. Refine and lock the anchor
The user picks v1/v2/v3. If they ask for refinement, use `templates/refinement-prompt.md` — call out **what to keep, what to change, what not to touch**. Run `edit_image` (after `upload_image` on the chosen variant) until locked.

Save the final to `images/anchor-locked.png`.

### 9. Generate slides 2..N, one at a time, anchored
For each subsequent slide:

1. Call `mcp__kie-image__upload_image` on `images/anchor-locked.png` → get `downloadUrl`.
2. Build the prompt from `templates/slide-N-prompt.md`. Inject:
   - the locked visual spec block from `05-visual-brief.md` (palette, type, grid, motifs verbatim)
   - the slide's exact copy from `02-slide-copy.md`
   - the chosen graphic type from `03-graphic-plan.md`
3. Call `mcp__kie-image__edit_image` with the anchor `downloadUrl` and the prompt. aspect_ratio: `"3:4"`.
4. Crop with `scripts/crop_to_4x5.py`.
5. Append to `07-slide-prompts.md`.

Generate **one slide per call**. Never batch.

### 10. Consistency check
Read `references/consistency-checklist.md`. Lay out all slides mentally as a set. Identify:
- weak slides (wrong type scale, off palette, low readability, off-brand)
- strongest slides
- exact regeneration notes for the weak ones (what to keep / change / not touch)

Save to `08-consistency-check.md`. **Only regenerate weak slides** — never the whole set.

## Style skins

This skill ships with one reference skin so you can see how a complete style spec looks:

| Skin | Reference |
|---|---|
| **Field Manual** (warm cream + accent + monospace) | `references/style-field-manual.md` |

To build your own skin from an inspiration board (Pinterest pulls, Figma boards, screenshots of carousels you admire), follow `references/build-your-own-skin.md`. That doc walks you through the exact "design board ingestion" process the field-manual skin was built from.

## Image generation tooling

- **Aspect ratio:** always pass `"3:4"` to kie.ai. Crop to 1080×1350 with `scripts/crop_to_4x5.py` after generation. The script trims equally from top/bottom by default.
- **Anchor → matched slides:** use `upload_image` to push `anchor-locked.png` to kie.ai (3-day TTL) and reuse the same `downloadUrl` for every later slide in the same session.
- **Text fidelity:** kie.ai gpt-image-2 renders text well, but reinforce in every prompt: *"render only the exact text below. do not add random words. all text must be legible at small sizes."*
- **Forbidden in prompts:** generic descriptors like "modern", "clean", "professional". Be specific: hex codes, type names, layout grid units, motif placement.

## Hard rules

1. **Copy before pixels.** No image generation before `02-slide-copy.md` is complete.
2. **Three anchors, then stop.** Never auto-proceed past step 7. Always wait for anchor lock.
3. **One slide at a time after the anchor.** No batching.
4. **No invented assets.** Logos, screenshots, UI must be real or marked TBD.
5. **Lock the visual spec.** Every slide 2..N prompt copies the brief's palette/type/grid/motif block verbatim.
6. **Regen only the weak.** Consistency check identifies them; everything else stays.

## Default deliverable when invoked

When a user fires this skill, by step 7 you should have produced:

1. `01-strategy.md` — sharp idea
2. `02-slide-copy.md` — full slide copy
3. `03-graphic-plan.md` — graphic type per slide
4. `04-asset-list.md` — required source assets
5. `05-visual-brief.md` — locked visual spec
6. `06-anchor-options.md` — 3 slide-1 prompts + 3 generated images

Then **pause and ask the user to lock an anchor.** Steps 8–10 only run after that.
