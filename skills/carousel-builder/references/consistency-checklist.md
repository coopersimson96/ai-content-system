# Carousel Consistency Checklist

Run this **after all slides are generated**, before posting. Lay them out together as a set and check every box. Save findings to `08-consistency-check.md`.

## Copy

- [ ] One sharp idea threads through every slide
- [ ] No slide tries to say two things at once
- [ ] Hook is clear within 2 seconds (~10 words max in the headline)
- [ ] CTA names a specific keyword and a specific reward
- [ ] Each slide advances the story (no dead slides)
- [ ] No filler words ("just", "really", "actually") in the headlines

## Visual system

- [ ] Same type family across every slide (no surprise serifs / sans switches)
- [ ] Headline scale is consistent — no slide is dramatically bigger or smaller than the rest unless intentional
- [ ] Margins are consistent across all slides
- [ ] Palette holds: primary text color, accent color, and background color match the locked anchor on every slide
- [ ] Texture (grid, paper grain) is consistent and at the same intensity
- [ ] Footer / header metadata system is identical on every slide (correct slide number, correct labels)
- [ ] Recurring motifs (mascot, asterisk, evidence panels) appear when the brief says they should — and don't randomly appear when they shouldn't

## Slide rhythm

- [ ] Slide 1 stops scroll (clear hook, dominant headline)
- [ ] Slide 2 creates context, tension, or proof
- [ ] Middle slides teach or prove (one idea each)
- [ ] Penultimate slide summarizes value or sets up the CTA
- [ ] Final slide gives **one** clear action (not three)

## Asset integrity

- [ ] Every logo shown is real and accurately rendered (no AI-hallucinated logos)
- [ ] Every screenshot is real or clearly stylized (no fake UI passing as real)
- [ ] No random extra words inserted by the model
- [ ] All text on every slide is readable at thumb-scroll size
- [ ] No invented stats, dates, or quotes

## Style-skin compliance

Check against your locked spec block in `05-visual-brief.md`. For each rule in your skin's reference file (e.g. `style-field-manual.md` or your custom skin):

- [ ] Background hex matches on every slide
- [ ] Primary text hex matches on every slide
- [ ] Accent hex matches and shows up on every slide
- [ ] Recurring motifs appear per spec (not too often, not missing)
- [ ] Forbidden elements are absent (no emoji, no banned fonts, no fake screenshots, etc.)
- [ ] Corner metadata system intact on every slide

## The fix protocol

For each weak slide identified, write a regen note in this format:

```
Slide N — [graphic type] — issue
KEEP: [what's working — be specific]
CHANGE: [the single thing to fix]
DO NOT TOUCH: [what must survive the regen]
```

Run the regen via `edit_image` (not `generate_image`) using the locked anchor as the source URL. **Never regenerate the whole carousel** — only the slides flagged here.
