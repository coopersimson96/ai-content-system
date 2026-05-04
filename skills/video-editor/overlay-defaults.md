# Overlay Defaults — Frosted Glass + Karaoke Pill

The visual and technical defaults for short-form video overlays. Apply on the FIRST render of any new build. These survived eight rounds of iteration on a real reel - skip the back-and-forth and ship them from the start.

Override only when a specific video calls for something different.

---

## The frosted glass card (universal overlay container)

```css
.frosted-card {
  background: rgba(255, 122, 26, 0.62);    /* orange brand tint, solid enough for white text */
  backdrop-filter: blur(20px) saturate(1.2);
  -webkit-backdrop-filter: blur(20px) saturate(1.2);
  border: 1.5px solid rgba(255, 255, 255, 0.32);
  border-radius: 32px;
  box-shadow:
    inset 0 1.5px 0 rgba(255, 255, 255, 0.5),     /* inner top highlight */
    inset 0 -1px 0 rgba(0, 0, 0, 0.12),
    0 22px 56px rgba(0, 0, 0, 0.42),               /* drop shadow */
    0 0 38px rgba(255, 122, 26, 0.28);             /* outer brand glow */
}
```

- Orange tint at `#ff7a1a` / 0.62 alpha. This is the default - change to your brand color in `style-guides/BRAND.md.example` and override the alpha if the new color reads differently against white text.
- `backdrop-filter: blur(20px)` preserves the frosted feel while keeping cards readable.
- Border-radius 32px on cards, 22px on smaller pills.

---

## Text inside cards

- **All text is white** (`#ffffff`). No tinted text inside the card.
- **Hard drop shadow** for elevation off the orange:
  - Body: `1.5px 1.5px 0 rgba(0,0,0,0.92), 0 4px 14px rgba(0,0,0,0.45)`
  - Headlines (60px+): `2px 2px 0 rgba(0,0,0,0.92), 0 6px 22px rgba(0,0,0,0.45)`
  - XL CTAs: `3px 3px 0 rgba(0,0,0,0.92), 0 8px 28px rgba(0,0,0,0.5)`
- SVG icons get matching drop-shadow filters: `filter: drop-shadow(1.5px 1.5px 0 rgba(0,0,0,0.92))`

The hard drop shadow is what makes white text readable on the warm orange backdrop. Without it, edges blur into the tint.

---

## Karaoke captions (single pill)

```css
.karaoke-pill {
  background: rgba(195, 175, 230, 0.94);   /* light purple */
  color: #1f3a2c;                          /* near-black forest green */
  font-family: 'Inter', sans-serif;
  font-weight: 900;
  font-size: 78px;
  padding: 14px 32px;
  border-radius: 22px;
  letter-spacing: -0.015em;
  line-height: 1.0;
  box-shadow:
    0 0 0 1.5px rgba(255, 255, 255, 0.42),
    0 6px 22px rgba(195, 175, 230, 0.4),
    0 16px 44px rgba(0, 0, 0, 0.32);
}
```

- Position: chest level, `top: 1380px` on a 1080×1920 canvas.
- **One pill only.** The pill's text content updates per word. Pill fades out during gaps longer than 180ms.
- Light purple `rgba(195, 175, 230, 0.94)` reads as "complementary" against the orange overlay - it doesn't compete for attention.

### Caption sync offset

```js
const KARAOKE_LEAD = -0.03;  // fire 30ms before transcript word.start
```

Tested as the right offset for a single mp4 with `data-has-audio="true"`. Negative leads earlier than the word; positive trails it. `-0.03` reads as "in sync" while `0` reads as slightly late (browser frame timing) and `-0.10` reads as too early.

---

## Audio + video setup (the only pattern that survives lint)

```html
<video id="speaker-video" src="assets/edited.mp4"
       data-has-audio="true"
       data-start="0" data-duration="X" data-track-index="0"></video>
```

- **Single mp4 with `data-has-audio="true"`.**
- **NO `muted` attribute.** Lint will flag muted + data-has-audio as a conflict.
- **NO sibling `<audio>` element.** Splitting audio out causes ~25ms phase delay (AAC priming silence at packet start) heard as audible echo or apparent caption drift.

This is the only pattern that lints clean AND plays cleanly. See `render-contract-gotchas.md` section 1.

---

## Per-video brand override

The orange-frosted-glass treatment is the default. Specific videos can override the palette - one project might go sage, another might go cobalt blue, another might want the glass to drop tint entirely.

When overriding:

1. Set new color tokens at `:root` level in your project's `index.html`
2. Update both the `frosted-card` background tint AND the outer glow to match
3. Re-test text legibility - if white-on-tint is fighting, increase the tint alpha or darken the drop shadow
4. Karaoke pill color can stay light purple; it works against most warm backgrounds

---

## How to apply

1. Use the `templates/build_index.py` pattern - Python script templates HTML and inlines karaoke JSON via `__WORDS_JSON__` substitution.
2. Read `templates/index.html.template` for the full CSS + GSAP shape.
3. Don't relitigate these defaults unless the user asks for something specific. The orange frosted glass + light-purple karaoke pill is the starting state, every time.
