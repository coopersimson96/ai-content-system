# Visual Brief — `05-visual-brief.md` template

This file is the **source of truth** for every later slide prompt. After it's filled, copy the "locked spec block" at the bottom verbatim into every slide-N prompt.

---

## Carousel title
[from intake]

## Style skin
[field-manual / your-custom-skin-name]

## Format
- Source aspect: 3:4 (1080×1440)
- Final aspect: 4:5 (1080×1350) after `crop_to_4x5.py`
- Outer margin: 80px

## Palette
| Role | Hex |
|---|---|
| Background | `#XXXXXX` |
| Primary text | `#XXXXXX` |
| Accent | `#XXXXXX` |
| Dark panel bg | `#XXXXXX` |
| Inverse text | `#XXXXXX` |
| Other | |

## Typography
- **Display headline:** [family + size at 1080×1440 + tracking + weight]
- **Body / support:** [family + size + line-height]
- **Metadata corners:** [family + size + tracking]
- **Buttons / pills:** [family + size]

## Background + texture
[bg color + grid spec (lines, color, spacing) + paper texture if any]

## Layout grid
- Outer margin: [px]
- Inner grid: [px]
- Headline placement: [top/middle/full-bleed]
- Diagram placement: [bottom/right/inset]

## Recurring motifs
- [ ] [motif 1 — e.g. brand mark, asterisk, evidence panel]
- [ ] [motif 2]
- [ ] [motif 3]
- Placement rules: [where each motif appears, how often]

## Header / footer system
```
top-left:    [text]                  top-right:   [text]
                                      [section label]

bottom-left: [text]                   bottom-right: [text]
```

## Visual references (from inspiration board)
- **Reference 1 — [filename or link]** → assigned job: typography & hierarchy
  - Borrow: [list]
  - Do not copy: [list]
- **Reference 2 — [...]** → assigned job: layout & spacing
  - Borrow: [list]
  - Do not copy: [list]
- **Reference 3 — [...]** → assigned job: colour, texture, mood
  - Borrow: [list]
  - Do not copy: [list]
- (Reference 4 if needed → pacing & carousel structure)

## Source assets
[from `04-asset-list.md` — for each: logo / screenshot / doc + status (have / TBD)]

## Forbidden
- [list — pulled from the chosen style-skin reference]

## Locked spec block (copy verbatim into every slide prompt)

```
STYLE: [skin name].
Background: [bg color hex] [+ grid/texture spec].
Type: [display family + size + color hex + behavior]; [body family + size + color hex].
Recurring motifs: [list with placement rules].
Header/footer metadata in [type spec]: [exact format string].
Format: 3:4, 1080x1440. [margin spec]. High readability.
Mood: [3-word mood descriptor].
```

(Pull this block straight from the matching `references/style-*.md` file's image-prompt block, then customize palette/motifs to this carousel.)
