# Consistency Check — `08-consistency-check.md` template

Run after all slides are generated. Read `references/consistency-checklist.md`. Lay all slides side-by-side mentally (or open the cropped finals from `images/final/`).

---

## Strongest slides
- Slide [N]: [why it's working — be specific]
- Slide [N]: [why it's working]

## Weak slides — regen plan

### Slide [N] — [graphic type] — [issue summary]

**KEEP (preserve exactly):**
- [specific element]
- [specific element]

**CHANGE (single targeted fix):**
- [the one thing to fix, specific]

**DO NOT TOUCH:**
- [specific element]
- [specific element]

**Regen call:**
```
mcp__kie-image__edit_image
  prompt: <built from refinement template using the KEEP / CHANGE / DO NOT TOUCH above>
  input_urls: ["<downloadUrl of this slide>"]
  aspect_ratio: "3:4"
```

### Slide [N] — ...

(repeat per weak slide)

---

## Cross-carousel issues (apply to all slides)

If everything looks roughly right but the carousel as a whole is off, check:

- [ ] Type scale drifts — any slide significantly bigger or smaller than the rest?
- [ ] Palette drift — does any slide have a stray color outside the brief?
- [ ] Texture drift — is the grid/paper texture stronger or weaker on any slide?
- [ ] Footer/header metadata drift — wrong slide number, missing handle, wrong section label?
- [ ] Motif drift — mascot/asterisk/evidence panel appearing where it shouldn't, or missing where it should?

Note any cross-carousel issues here. They usually indicate a problem with the locked spec block; tighten the brief and regen the affected slides.

---

## Final approval

- [ ] All weak slides regenerated and re-cropped to 1080×1350.
- [ ] All cropped finals exported to `images/final/`.
- [ ] Carousel is publish-ready.
