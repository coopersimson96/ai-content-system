# Slide N Prompt — anchored to locked slide 1

Use this for every slide after the anchor is locked. Generate **one slide per call.** Never batch.

Tool: `mcp__kie-image__edit_image` (after `upload_image` on the locked anchor).
Aspect ratio: `"3:4"` (crop after).

---

## Step 1 — upload anchor (do this once per session)

```
mcp__kie-image__upload_image
  file_path: "<carousel-folder>/images/anchor-locked.png"
  upload_path: "carousels"
```

Save the returned `downloadUrl`. Reuse it for every slide in this carousel.

## Step 2 — build the slide prompt

```
Create slide [N] of an Instagram carousel.

This carousel uses a locked visual anchor (slide 1 of the same carousel) attached as the source image. Match the anchor exactly on:
- typography family, size, weight, tracking
- spacing and margins
- color treatment (palette and accent)
- background and texture
- recurring motifs
- header/footer metadata system
- visual hierarchy and mood

DO NOT REINVENT THE STYLE. Stay in the same visual family as the anchor.

SLIDE ROLE:
[from 02-slide-copy.md — e.g. "Sauce / non-obvious unlock"]

GRAPHIC TYPE:
[from 03-graphic-plan.md — e.g. "Prompt box" or "Stack diagram" or "Evidence teardown"]

EXACT TEXT TO RENDER (render only this text, do not add any other words):
- Headline: "[from 02-slide-copy.md]"
- Highlight word(s) in accent color: "[...]"
- Support line: "[...]"
- Bottom note: "[...]"
- Slide counter (top-right corner): "[N] / [TOTAL]"
- Section label (top-left corner): "[from 02-slide-copy.md role]"

[paste the LOCKED SPEC BLOCK from 05-visual-brief.md here verbatim]

GRAPHIC INSTRUCTIONS:
[Specific to the chosen graphic type. Examples:]
- For Prompt box: "Render a dark rounded card centered in the lower 60% of the slide. Inside: monospace text in the inverse text color, with the keyword 'ROLE:' highlighted in the accent color."
- For Stack diagram: "Render five rectangles connected by + symbols, each labelled per the headline content. Use the exact label words: [list]."
- For Evidence teardown: "Render a white card with thin accent-color border on the right side, containing the source screenshot at [position]. Add overlay callouts numbered #1 and #2 over [specific UI elements]."
- For CTA poster: "Render the CTA pill button [pill text] in accent color, with SAVE and SHARE pills next to it. Brand mark / footer per spec."

ASSETS REQUIRED:
[from 04-asset-list.md — list any logo or screenshot the slide needs, with the exact filename or "TBD — leave a placeholder rectangle labelled '[asset name]'"]

RULES:
- Render only the exact text above. Do not add random words.
- All text must be legible at thumb-scroll size.
- Do not invent logos or fake screenshots. If an asset is TBD, leave a placeholder rectangle with the asset name in small caps.
- The slide must look like it belongs to the same carousel as the anchor.
- Format: 3:4 vertical (1080x1440). Same margins and grid as the anchor.
```

## Step 3 — call edit_image

```
mcp__kie-image__edit_image
  prompt: <the prompt you just built>
  input_urls: ["<downloadUrl from Step 1>"]
  aspect_ratio: "3:4"
  nsfw_checker: false
```

## Step 4 — crop and append

1. Move the result from your kie output folder to `images/slide-N.png`.
2. Run `python3 scripts/crop_to_4x5.py images/slide-N.png`.
3. Append the slide prompt + image path to `07-slide-prompts.md`.
4. Move to slide N+1. Do not skip the per-slide append.
