# Refinement Prompt — for the locked anchor or weak slides

Use this when:
- The user picks an anchor variant but wants tweaks before locking.
- The consistency check flags a weak slide that needs targeted regen.

The cardinal rule of refinement: **always tell the model what to KEEP, what to CHANGE, and what NOT TO TOUCH.** Otherwise it'll change everything and you lose the parts that were already working.

---

## Refinement template

```
Refine the attached slide image.

KEEP (these elements are working — preserve exactly):
- [item 1, be specific — e.g. "the headline typography family and tracking"]
- [item 2 — e.g. "the cream paper texture and grid"]
- [item 3 — e.g. "the corner metadata system"]

CHANGE (these specific things need adjustment):
- [single specific change — e.g. "make the headline 30% larger and shift left margin to 60px"]
- [optional second change — e.g. "remove the secondary support line under the headline"]

DO NOT TOUCH (do not modify these even subtly):
- [item 1 — e.g. "the brand mark position and size"]
- [item 2 — e.g. "the accent color flip on the highlight word"]
- [item 3 — e.g. "the handle in the bottom-left"]

Keep the format at 3:4 (1080x1440).
Render only the existing text — do not add or change wording.
```

## Refinement language that works

Good (specific, observable):
- "Make the headline larger and more dominant."
- "Reduce the clutter and keep one strong focal point."
- "Make the typography feel less generic, more premium."
- "Increase the accent saturation by 15%."
- "Move the brand mark from bottom-right to upper-right."

Bad (vague, model-guesses):
- "Make it look better."
- "Make it pop more."
- "Cleaner."
- "Less AI-looking."
- "More premium."

If a refinement note feels vague when reading it back, rewrite it with a number, a position, or a specific element reference.

## How to call

```
mcp__kie-image__edit_image
  prompt: <the refinement prompt above>
  input_urls: ["<downloadUrl of the slide being refined>"]
  aspect_ratio: "3:4"
  nsfw_checker: false
```

If the slide isn't yet uploaded to kie storage, run `mcp__kie-image__upload_image` on it first to get the `downloadUrl`.
