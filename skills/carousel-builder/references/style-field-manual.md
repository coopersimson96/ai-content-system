# Style Skin — Field Manual (reference)

A complete reference skin showing what a "locked visual spec" looks like end-to-end. **Treat this as a reference, not a default.** Build your own skin per `build-your-own-skin.md` so your carousels look like *yours*, not like everyone else who installed this skill.

The vibe: AI lab notebook. Operating system. Technical zine. Field manual you'd find in a back-room engineering office.

## Palette (exact hex)

| Role | Hex | Usage |
|---|---|---|
| Background | `#F2EDE4` | warm off-white, grid-paper base |
| Grid lines | `#E1D9CA` | very subtle 32px grid |
| Primary text | `#1A1A1A` | near-black for headlines and body |
| Accent | `#D97A5A` | muted orange for emphasis words, badges, CTA buttons |
| Dark panel | `#1A1A1A` | reverse-out cards (white text on near-black) |
| Inverse text | `#F2EDE4` | text inside dark panels |
| Tag bg | `#FFFFFF` | rounded "INSTALL" / "PROMPTS" buttons |

Never use pure white `#FFF` for the page bg. Always the warm cream `#F2EDE4`.
Never use pure black `#000` for text. Always near-black `#1A1A1A`.

## Typography

- **Display headline:** geometric sans-serif with monospace-inspired wide letter spacing. Reference family: "JetBrains Mono", "IBM Plex Mono", or a similar editorial mono. Size: ~120pt at 1080×1440 source.
- **Highlight words within headline:** flip to the orange `#D97A5A` mid-sentence (e.g. "Claude **lies** to you").
- **Body / support line:** monospace at ~28pt, near-black, generous line-height.
- **Metadata corners:** small caps mono at ~16pt with `·` separators (e.g. `#01 · COVER · YOUR PROJECT / 06`).
- **Buttons / tags:** small caps mono on white pill buttons with thin borders.

## Layout grid

- Format: 3:4 source (1080×1440) → cropped to 4:5 final (1080×1350).
- 80px outer margin all sides.
- 32px grid (light cream lines, barely visible).
- Top corners: section label (left) · slide counter (right).
- Bottom corners: handle `@your.handle` (left) · `SWIPE →` or `NEXT →` (right).
- Big headlines break across multiple lines and may overflow the implied baseline by design.

## Recurring motifs

- **Your brand mark / mascot** — small (~96px tall), placed in unexpected corners. Pick something simple and consistent (an icon, a wordmark, a pixel-art creature, a glyph). It becomes the silent signature across every slide.
- **Code-style cards** — white rounded rectangles with thin border, label in top-left (e.g. `▲ ASK IT`), then code-block-style content inside.
- **Dark panel callouts** — full-width black rectangle with cream text for the "punchline" of a slide.
- **Pill buttons** — `[INSTALL] [PROMPTS] [DOCS]` clusters at the bottom.
- **Hairline rules** — 1px charcoal lines under metadata or above CTAs.

## Header / footer system (every slide)

```
top-left:    #NN · SECTION             top-right:   PROJECT NAME / TOTAL
                                        (or NN / TOTAL)

bottom-left: @your.handle               bottom-right: SWIPE →  /  NEXT →  /  — END —
```

Slide 1 uses `#01 · COVER` and `SWIPE`. Final slide uses `#NN · CTA` and `— END —`.

## Forbidden

- glossy SaaS gradients
- generic stock illustrations or 3D icons
- emoji
- pure white backgrounds
- centered text walls
- generic sans-serif (Inter, Roboto, Helvetica)
- more than 3 fonts on one slide
- random "AI-generated" words in the image
- mocked-up screenshots that don't actually exist

## Borrow from references

When showing reference images, always state:

> Borrow: cream grid background, accent-flip headline treatment, mono type, dark panel callouts, pill buttons, corner metadata, brand-mark placement.
> Do not copy: exact text, exact compositions, the original creator's wording.

## Image-prompt block (paste into every slide prompt for this skin)

```
STYLE: Field Manual.
Background: warm off-white #F2EDE4 with subtle 32px cream grid #E1D9CA.
Type: editorial monospace, near-black #1A1A1A, wide tracking, oversized headline.
Highlight words switch to muted orange #D97A5A inline.
Recurring motifs: small pixel-art brand mark, dark #1A1A1A panel callouts with #F2EDE4 text, white rounded code cards with thin borders, small pill buttons.
Corner metadata in small caps mono: section label top-left, slide counter top-right, @your.handle bottom-left, "SWIPE →" / "NEXT →" / "— END —" bottom-right.
Format: 3:4, 1080x1440. Generous 80px outer margin. High readability.
Mood: AI lab notebook, technical zine, designed but not corporate.
```

Customize the palette, mascot, and handle for your brand before using this verbatim.
