# Editorial Magazine Motion Style — Deconstruction

> Reference reels:
> - Reel A (53s, 1080×1920) — full-frame talking head, single editorial reveal
> - Reel B (77s, 720×1280) — top editorial / bottom talking head split (hooded creator, podcast mic)
> - Reel C (84s, 720×1280) — top Notion templates / bottom kitchen-counter speaker
>
> Format: 9:16 vertical, 1080×1920 native (some sources 720×1280), 30fps
> Genre: Editorial / "newsletter on screen" — magazine-styled UI overlays + naturally-graded podcast-style speaker
> Working alias for this aesthetic: **Editorial Split** — print-magazine layouts stacked above an unkeyed, naturally-lit talking head, with italic-serif single-word captions

This is a deconstruction of three reels into a reusable motion-graphics playbook. The goal is *not* one-to-one recreation — it is to extract the **visual DNA** so the same discipline can be applied to your scripts via Hyperframes without copying any single source.

---

## 0 · The 10 Laws (memorize)

1. **The frame is a magazine spread, not a screen.** Every B-roll beat is composed as if it were a page from a print quarterly — masthead lines, drop-cap-scale headlines, italic emphasis pairs, thin black hairline rules under titles, generous margins. CSS chrome, gradient buttons, and "tech UI" cues are forbidden unless they appear *inside* a screenshot card. The page itself is paper.
2. **Hard horizontal split, never picture-in-picture.** When the speaker is on screen *and* an editorial layout is on screen, the frame is sliced cleanly in half (top 50-55% editorial, bottom 45-50% speaker). No floating cards over face, no PiP window, no green-screen comp. The split is the format's load-bearing wall.
3. **Black is the bezel; cream/white is the page.** The edges of the frame (top bar, bottom bar, sometimes side margins) are pure black `#000`. The editorial card itself is warm-paper cream `#efece0` to `#f3eee2` or pure white `#fdfdfd`. The contrast between black bezel and paper page is what gives every shot its "pulled from a magazine" register.
4. **The speaker is naturally graded, never desaturated.** Unlike sage-stack, the talking head retains real warmth: tungsten kitchen lamps, plants, framed art on the wall, a Røde mic, hoodie, a real keyboard with RGB. The "I just sat down to film this" energy is the entire trust device. No filters, no grading LUTs, no vignettes on the speaker plate.
5. **Two type voices, never three.** Voice A is a wide classical display serif (Caslon Display / Eames Century Modern / Tiempos Headline) used UPRIGHT for headlines and labels. Voice B is the *same family in italic*, used for single-word emphasis inside captions and headline pairs. There is no third sans-serif for body text on the page — body uses Voice A regular at small size.
6. **Single-word captions in italic serif, centered, white on transparent.** The spoken-word karaoke layer is one word at a time, in Voice B italic, ~52-64px, pure white `#ffffff`, with a soft 8px black drop shadow for legibility over the speaker plate. No pill background, no all-caps, no sans-serif. (Exception: reel A uses white-on-black-pill all-caps for hook lines — see Section 5.4.)
7. **Numbered rows are the spine of every list.** Every enumerated beat uses a tight grid of `[01] [serif word] [grey one-line subtitle] [thin colored underline rule]`. Numerals are italic serif at 32px, words are upright serif at 44-56px, subtitles are 13-14px tracked-out small caps grey, underlines are 1.5-2px solid in the brand accent.
8. **One row in every list breaks the rule.** When a numbered list shows N rows, exactly ONE row gets a different-colored underline (chartreuse vs. orange, lime vs. red) to flag the "exception", "winner", or "answer". This is the format's signature beat — it earns the emphasis by making the rest of the rows uniform.
9. **Pacing is breath, not whip.** Each editorial spread holds for 2.5-4.0s — twice as long as a hard-cut comedy reel, almost twice as long as sage-stack's average beat. The viewer is being given *time to read*. Transitions are crossfades or whitewash flashes, never directional whips, never blur streaks.
10. **The accent color is allowed exactly ONE job per scene.** The neon-lime / chartreuse / hot-orange accent never decorates — it does work. It either underlines the row that breaks the rule, or boxes a single word the speaker is about to land on, or fills a single CTA button. If the accent is on screen for decoration, the format breaks.

---

## 1 · Reference Timeline (reel B, 77s, beat-by-beat)

This is the cleanest example of the split format.

| Time | Beat | Top half (editorial) | Bottom half (speaker) | Caption layer |
|------|------|----------------------|----------------------|---------------|
| 0.0-2.0 | **Hook open** | Black bezel only — pure top half black | Speaker mid-shot, hood up, laughing, hands gesturing | Italic-serif single-word "absolutely" enters at 0.6s, holds 1.2s, fades |
| 2.0-4.5 | **Issue masthead** | Cream card slides in from top: small-caps masthead "ISSUE 03 · THE LOOP · APR 2026", thin black rule, then large headline pair | Speaker still talking, naturally graded | Word lands per syllable, italic serif, ~120ms stagger |
| 4.5-8.0 | **Headline reveal** | Same card now reads big serif: "Five **things** around a model" — "Five" + "around a model" upright, "things" italic emphasis | Speaker continues | Single-word caption swaps each spoken word |
| 8.0-11.5 | **Section label "PIECE 01 · THE LOOP"** | Card recomposes: small-caps section label top-left, larger upright serif word "Loop", grey one-line subtitle | Speaker animated, hands moving | "Loop" caption matches the on-page word for half a beat — meta moment |
| 11.5-16.0 | **Numbered list reveal (5 rows)** | Cream card holds 5 rows: 01 Loop / 02 Tools / 03 Memory / 04 Context / 05 Control. Each row underlined in lime `#c8d63a` | Speaker visible | Italic-serif word per spoken term lands as each row underlines |
| 16.0-18.5 | **The exception row** | Row 04 (or 05) underline changes from lime to **orange `#e85a1f`** with a soft 200ms crossfade. Tiny "↳ THE EXCEPTION" small-caps grey label appears beside it | Speaker leans in slightly | Caption "different" lands italic |
| 18.5-22.0 | **Code block (Geist Mono)** | Cream card now holds a light card-within-card: Geist Mono code block, no syntax highlighting, just dark-grey monospace on `#f8f6ee` | Speaker | Caption "five lines" italic |
| 22.0-26.0 | **App screenshot card** | Light Cursor / Claude Code window screenshot floats on the cream page, soft 16px drop shadow, slight rounded `border-radius: 14px` | Speaker | Caption "important emails" |
| 26.0-32.0 | **Process: 3-step numbered** | Three numbered cards stack vertically with circular blue numerals, "Step 1: Audit & Access / Step 2: Build & Connect / Step 3: QA & Launch" | Speaker (kitchen visible behind, plants, Røde mic) | Italic "sections" lands on the word "sections" being shown |
| 32.0-36.5 | **Diagram inset** | A small hand-style flowchart diagram ("comment → DM → tag → sequence") sits centered on cream, thin black strokes, italic labels | Speaker | Italic "that" |
| 36.5-42.0 | **Quote pull** | Massive italic serif pull-quote occupies the whole top half: *"It's not a tool. It's a teammate."* with attribution small-caps grey below | Speaker dwell | Caption fades, lets quote breathe |
| 42.0-48.0 | **Tablet mockup with carousel** | iPad-sized mockup shows a hand-drawn carousel slide ("BEST DAY TO POST?") with crayon bar chart, the row "the winner" highlighted lime | Speaker | "designs" italic |
| 48.0-54.0 | **Form / questionnaire UI** | Cream card with form fields ("What topic/niche", radio chips, slider, highlighter palette swatches at bottom) | Speaker (now in dark hoodie, evening lighting) | "totally" / "gives you" — italic |
| 54.0-60.0 | **Meta moment: agent screenshot** | "Start with context" panel from a design tool, soft pill buttons "Design System / Add screenshot / Attach codebase / Drag in a Figma file" | Speaker | "totally" |
| 60.0-66.0 | **Big stat card** | Single large numeral or short headline mid-page (e.g. "200/800 = 25%"), thin black hairline above and below | Speaker | Italic emphasis on stat word |
| 66.0-73.0 | **Closing piece label** | Section label "↳ GO DEEPER" small-caps grey, then a 3-row "what to do next" list with lime underlines | Speaker | Italic "exactly" |
| 73.0-77.0 | **Outro CTA** | Cream card reads (Voice A) "comment" + (Voice B italic) "*the loop*" centered, thin black hairline above and below | Speaker smiles, holds | Caption locks: comment "the loop" |

**Three-act structure** (longer than sage-stack — magazines are slower than reels):
- **Cover (0-8s):** Issue masthead + headline pair = "you are reading something curated"
- **Pieces (8-66s):** 4-6 numbered/labeled pieces, each ~7-12s, each with its own internal grammar (label → header → exhibit → caption beat)
- **Closer (66-77s):** "Go deeper" recap + comment-CTA in italic emphasis

Notice: each *piece* uses the same internal grammar (label → header → exhibit). That repeatability is what makes this format scalable to any script.

---

## 2 · The Visual Vocabulary

### 2.1 Backgrounds (in priority order)

| # | Background | Where it lives | How to build in Hyperframes |
|---|-----------|----------------|---------------------|
| 1 | **Black bezel + cream page** (split mode) | Every spread when speaker is also on screen | Top half: `background: #000`. Inside it, an inset cream card `background: #efece0; border-radius: 6px; margin: 32px 24px 0; box-shadow: 0 1px 0 rgba(0,0,0,.08), 0 24px 48px rgba(0,0,0,.35);`. Bottom half: nothing — the speaker `<video>` fills it directly, naturally graded. |
| 2 | **Full-screen cream page** (no speaker) | Spread-only beats (reel A mid-section) | Whole frame: `background: linear-gradient(180deg, #f3eee2 0%, #efece0 100%)`. Optional 1.5% paper grain via `grain-overlay` block at `opacity: 0.03`. |
| 3 | **Pure-black bezel hold** | Hook openers, transitions between spreads | Whole frame `#000`. Use as a 200-400ms breath beat between two spreads — the eye resets. |
| 4 | **Full-frame talking head** (reel A baseline) | When the script is reaction-led, no editorial overlay | Just the speaker `<video>` filling the entire frame, with white-on-black-pill caption blocks. No top crop. |
| 5 | **Red / colored magazine card** (rare hero moment) | Reel A reveal beat — the "free guide" card | Solid saturated card (red `#c41e1e` in source), small-caps masthead in white, oversized chunky white serif headline, white body text. Used max once per reel, signals the actual artifact being referenced. |
| 6 | **Print-paper texture overlay** | All cream pages, very subtle | A 4% opacity paper-fiber PNG over the cream layer. Skip for `grain-overlay` if no asset — they read similarly. |

The cream page reads as "newsletter / longform / editorial". The black bezel reads as "this is curated / framed / not random TikTok footage". Together they signal *publication* before the viewer parses a single word.

### 2.2 Type System

**Two type voices, two roles. Never three.**

#### Voice A — "Display Serif Upright" (the page voice)
- Family: wide classical display serif. **Caslon Display**, **Eames Century Modern**, **Tiempos Headline**, **Reckless Neue**, or **Domaine Display** all read correctly. Swap candidates: **Fraunces** (variable, free), **Instrument Serif Bold**, or **Crimson Pro**. Avoid Playfair (too web-default) and avoid Recoleta (sage-stack's voice).
- Color: near-black `#0e0e0c` on cream pages; pure black `#000` on white cards
- Weight: Regular (400) for body, Bold (700) for headlines
- Tracking: `letter-spacing: -0.01em` on headlines, `0.0em` on body
- Use for: masthead lines (small-caps regular), headlines (bold), numbered-row words (regular), pull-quotes (regular italic at 64px+), CTA verbs ("comment")

#### Voice B — "Display Serif Italic" (the emphasis voice)
- Family: **same family as Voice A in italic**. Caslon Italic, Tiempos Italic, Fraunces Italic.
- Color: matches Voice A by default (near-black), OR shifts to brand accent for one beat per scene (see Section 2.3)
- Weight: Regular italic (400 italic)
- Use for: single-word captions over the speaker, the *italic emphasis word* inside a headline pair ("Five **things** around a model"), pull-quote text, attribution lines

#### Voice C — "UI Mono" (in-product overlays only)
- Family: **Geist Mono**, **JetBrains Mono**, or **Roboto Mono**
- Color: dark grey `#444` on light surfaces
- Use for: code blocks inside cream cards, transcript text inside fake UI screenshots
- Never used for narration captions or headlines. Lives only inside fake-UI screenshots.

#### Voice D — "Small-caps masthead" (a STYLE of Voice A, not a fourth family)
- Voice A regular, `text-transform: uppercase`, `letter-spacing: 0.18em`, `font-size: 11-13px`, color `#888`
- Use for: section labels ("ISSUE 03 · THE LOOP · APR 2026", "PIECE 01 · THE LOOP", "↳ GO DEEPER", "HOW IT WORKS")

#### Animation patterns (text reveals)
- **Headline pair (upright + italic):** upright word slides up 24px with 0.5s `power3.out`; italic emphasis enters 100ms later with `y: 18 → 0` and a 0.2s opacity fade. Stagger feels like the headline composing itself in real time.
- **Numbered row:** numeral fades in first (0.25s `power2.out`), then word slides up 12px (0.3s `power3.out`), subtitle fades (0.25s), underline scales from `scaleX: 0` left-anchored (0.45s `expo.out`). Total per-row: 0.6s. Cascade across 5 rows with 120ms stagger.
- **Single-word caption (italic serif over speaker):** scale from `0.96 → 1.0`, opacity `0 → 1`, no Y-translation. Duration: 0.18s `power2.out`. Out: 0.16s opacity-only fade. Locked between caption swaps so the eye stays planted.
- **Pull-quote:** the entire italic block fades in as one element with a 0.5s fade + a 4px Y-rise. No per-word stagger — it reads as "a magazine quote loaded onto the page".

All easings are **`power3.out` / `expo.out` / `power2.out`**. No `back.out`, no `elastic`, no `bounce`. The format is *editorial*, not *playful*.

### 2.3 Color Story (memorize the meanings)

| Color | Hex | Meaning | Where used |
|-------|-----|---------|------------|
| **Page cream** | `#efece0` (mid) / `#f3eee2` (light) / `#e8e3d2` (warm) | The paper itself | All editorial card backgrounds |
| **Page white** | `#fdfdfd` | Crisp white card variant (used in reel B Notion screenshots) | Software UI screenshots embedded in cream pages |
| **Ink near-black** | `#0e0e0c` | Headlines, body, numerals | All Voice A and B type on light pages |
| **Bezel black** | `#000000` | The cinema crop bars | Top + bottom of frame in split mode |
| **Mute grey** | `#7a7a76` | Small-caps mastheads, subtitles, attribution | Tracked-out tertiary type |
| **Hairline grey** | `#1a1a1a` at 1.5px | Thin rules under headlines | Section dividers, above/below pull quotes |
| **Lime / chartreuse accent** | `#c8d63a` (warm lime) / `#a4d932` (cooler) | The "default" row underline / highlight color | Numbered-row underlines, highlighter pen on key words |
| **Hot orange accent** | `#e85a1f` / `#f09025` | The "exception" row / the "winner" highlight | Exactly one row per list, exactly one CTA per scene |
| **Editorial red** | `#c41e1e` / `#a91a1a` | The hero "magazine cover" card | Used max once per reel as a pure attention-grab card |
| **Notion blue numerals** | `#3a7eed` | Numbered step badges (Step 1/2/3 circles) | When the embedded screenshot is from Notion |
| **Caption black-pill** | `rgba(0,0,0,0.92)` | White-on-black caption pill (reel A only) | Hook lines on full-frame talking head |
| **Caption white-shadow** | `#ffffff` text + 6px black shadow | Default italic-serif single-word caption | Over speaker bottom half |

**Discipline:** the page-cream + ink-near-black + speaker's natural color = 90% of every frame. The remaining 10% is exactly ONE accent per scene — lime for "the rule", orange for "the exception", red for "the artifact". Drop blue, green, or purple in for decoration and the format dissolves.

---

## 3 · Signature Element Recipes

The two highest-leverage elements: the **Editorial Card Shell** and the **Numbered Row**.

### 3.1 The Editorial Card Shell (the "magazine page" container)

```css
.editorial-card {
  background: #efece0;
  color: #0e0e0c;
  border-radius: 6px;
  padding: 56px 48px 48px;
  /* The thin internal margin gives "page" feel */
  font-family: 'Fraunces', 'Caslon Display', 'Tiempos Headline', Georgia, serif;
  font-feature-settings: 'liga' 1, 'kern' 1, 'onum' 1; /* old-style numerals */
  position: relative;
  isolation: isolate;
  /* Subtle paper depth */
  box-shadow:
    0 1px 0 rgba(0,0,0,.06),
    0 24px 48px rgba(0,0,0,.35),
    inset 0 0 80px rgba(0,0,0,.02);
}

/* Optional paper grain */
.editorial-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url('assets/paper-grain.png');
  background-size: 320px 320px;
  opacity: 0.04;
  mix-blend-mode: multiply;
  pointer-events: none;
  border-radius: inherit;
}

/* The masthead row */
.masthead {
  font-family: inherit;
  font-size: 12px;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: #7a7a76;
  margin-bottom: 24px;
}

/* The thin black rule under headlines */
.hairline {
  height: 1.5px;
  background: #1a1a1a;
  width: 100%;
  margin: 16px 0 24px;
  transform-origin: left center; /* for scaleX entrance */
}

/* The headline pair */
.headline {
  font-size: 88px;
  line-height: 1.02;
  letter-spacing: -0.015em;
  font-weight: 700;
  color: #0e0e0c;
}
.headline .italic {
  font-style: italic;
  font-weight: 400; /* italic should feel lighter than bold upright */
}
```

### 3.2 The Numbered Row (the format's signature beat)

```html
<ul class="numbered-list">
  <li class="row" style="--accent: #c8d63a">
    <span class="num">01</span>
    <span class="word">Loop</span>
    <span class="sub">one instruction at a time</span>
    <span class="rule"></span>
  </li>
  <li class="row" style="--accent: #c8d63a">
    <span class="num">02</span>
    <span class="word">Tools</span>
    <span class="sub">read, write, search, run</span>
    <span class="rule"></span>
  </li>
  <li class="row" style="--accent: #c8d63a">
    <span class="num">03</span>
    <span class="word">Memory</span>
    <span class="sub">what to remember between turns</span>
    <span class="rule"></span>
  </li>
  <li class="row" style="--accent: #e85a1f"> <!-- THE EXCEPTION -->
    <span class="num">04</span>
    <span class="word">Control</span>
    <span class="sub">when to stop, retry, escalate</span>
    <span class="rule"></span>
    <span class="tag">↳ THE EXCEPTION</span>
  </li>
</ul>
```

```css
.numbered-list { list-style: none; margin: 0; padding: 0; }
.row {
  display: grid;
  grid-template-columns: 64px 1fr auto;
  grid-template-rows: auto auto auto;
  column-gap: 20px;
  padding: 18px 0 14px;
  position: relative;
}
.num {
  grid-column: 1; grid-row: 1 / 3;
  font-style: italic;
  font-size: 30px;
  color: #7a7a76;
  align-self: end;
  font-feature-settings: 'onum' 1;
}
.word {
  grid-column: 2; grid-row: 1;
  font-size: 52px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: #0e0e0c;
  line-height: 1.0;
}
.sub {
  grid-column: 2; grid-row: 2;
  font-size: 13px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #7a7a76;
  margin-top: 6px;
}
.rule {
  grid-column: 1 / -1; grid-row: 3;
  height: 2px;
  background: var(--accent);
  margin-top: 14px;
  transform-origin: left center;
}
.tag {
  grid-column: 3; grid-row: 1;
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--accent);
  align-self: start;
}
```

```js
// Cascade entrance — number first, word, subtitle, rule scales in last
gsap.from('.row .num', { opacity: 0, duration: 0.25, ease: 'power2.out', stagger: 0.12 });
gsap.from('.row .word', { y: 14, opacity: 0, duration: 0.32, ease: 'power3.out', stagger: 0.12, delay: 0.08 });
gsap.from('.row .sub',  { opacity: 0, duration: 0.25, ease: 'power2.out', stagger: 0.12, delay: 0.16 });
gsap.from('.row .rule', { scaleX: 0, duration: 0.45, ease: 'expo.out', stagger: 0.12, delay: 0.22 });

// The exception row swap (cue this when the speaker hits the "but"/"except"/"unless")
const exceptionRow = document.querySelector('.row[data-exception]');
gsap.to(exceptionRow.querySelector('.rule'), {
  backgroundColor: '#e85a1f',
  duration: 0.3,
  ease: 'power2.out',
});
gsap.from(exceptionRow.querySelector('.tag'), {
  opacity: 0, x: -8, duration: 0.4, ease: 'expo.out', delay: 0.05,
});
```

The "exception swap" is the most copyable single moment in this whole format. It is one line of GSAP, but it is the moment the viewer feels they've been *taught something*. Use it on every list of ≥3 items.

### 3.3 Layout Grid (the whole-page math)

The cream page assumes an **8pt baseline grid** and a **6-column inner grid**. Think of every spread as:

```
┌─────────────────────────────────────────┐
│  [56px top inset]                       │
│  MASTHEAD · ISSUE · DATE       (12pt)   │
│  [hairline]                             │
│  [24px breath]                          │
│                                         │
│  HEADLINE that wraps to two lines       │
│  with *italic emphasis* inside it       │
│  [hairline]                             │
│  [32px breath]                          │
│                                         │
│  CONTENT BLOCK                          │
│   - numbered list, OR                   │
│   - pull quote, OR                      │
│   - app screenshot card, OR             │
│   - code block, OR                      │
│   - diagram                             │
│                                         │
│  [48px bottom inset]                    │
└─────────────────────────────────────────┘
```

Never put two content blocks on the same page. The point is dwell, not density.

---

## 4 · Motion Patterns

### 4.1 Transition library

| Transition | When to use | Hyperframes block |
|-----------|-------------|-------------------|
| **Black-bezel breath** | Between two editorial spreads | Just hold black for 200-400ms before next card slides in. Use a `<div>` clip on a high `data-track-index`, fade in/out at 0.15s. |
| **Cream-card slide-in from top** | Spread entry over the bezel | Card translates `y: -100% → 0` over 0.55s `expo.out`, with a parallax: the page content inside the card slides 24px slower, creating a slight reveal feel. |
| **Whitewash flash-through** | When a quote needs to "land hard" | `flash-through-white` block — a 0.25s blowout to white, next spread emerges from white. Use sparingly, max 1× per reel. |
| **Light-leak warm tint** | Major section break (Piece 01 → Piece 02) | `light-leak` block, warm amber `#f5a25e` tint, opacity 0.4, 0.5s pass. Reads like a film-camera flare. |
| **Crossfade page-to-page** | Within a section, between two related exhibits | Plain GSAP opacity crossfade, 0.4s `power2.inOut`. The simplest move. Use this 70% of the time. |
| **Hairline-rule-as-wipe** | Between numbered list and pull quote | The hairline scales from `scaleX: 1 → 0` right-to-left, dragging the content above it offstage. 0.6s `expo.in`. |
| **Speaker-hold while page swaps** | Inside the split format, when only the top changes | The bottom-half speaker `<video>` keeps playing untouched. Only the top card swaps via crossfade. The speaker is the format's continuity device. |

### 4.2 Easing rules

- Type entries: **`power3.out`** or **`expo.out`** (confident, not bouncy)
- Card entries: **`expo.out`** (page slides into place decisively)
- Card exits: **`power2.in`** or **`expo.in`** (decisive, not lingering)
- Crossfades: **`power2.inOut`** — the only `inOut` allowed
- Underline scale: **`expo.out`** (the underline "snaps" into place)
- Never `bounce`, `elastic`, `back.out` — those break the editorial register

### 4.3 The "dwell-then-swap" recipe (the most-used transition)

```js
// Each spread holds 3.5s before the next swap
const spread1 = document.querySelector('#piece-01');
const spread2 = document.querySelector('#piece-02');

gsap.timeline()
  // Spread 1 enters
  .from(spread1, { y: -50, opacity: 0, duration: 0.55, ease: 'expo.out' })
  // Internal beats (numbered list cascade, exception swap, etc.)
  .add(buildPiece1Internals(), '+=0.2')
  // Dwell: hold for breath
  .to({}, { duration: 1.4 })
  // Crossfade out
  .to(spread1, { opacity: 0, duration: 0.4, ease: 'power2.inOut' })
  // Bezel-only beat (pure black breath)
  .to({}, { duration: 0.25 })
  // Spread 2 enters
  .from(spread2, { y: -50, opacity: 0, duration: 0.55, ease: 'expo.out' });
```

Notice: there are no whip-blurs anywhere. The format's pacing comes from **dwell length**, not transition speed. Three minutes of editorial content can ride entirely on `power2.inOut` crossfades and still feel kinetic — because the reader is being given time to read.

---

## 5 · The Speaker Treatment (CRITICAL — half the style)

### 5.1 The grading

The speaker plate is **NOT graded**. This is the inverse of sage-stack. The kitchen lamp warmth, the plants, the framed art on the wall, the unbleached hoodie — all of it stays. The "creator just sat down at his kitchen counter to record this" energy is the entire trust device.

Apply ONLY:

```css
.speaker-video {
  /* Tiny color correction for consistency across plates — that's it */
  filter:
    saturate(1.02)        /* barely-perceptible nudge */
    contrast(1.03);       /* tiny lift to compensate for video compression */
}
```

**Do not apply:** vignette, bloom, desaturation, sepia tint, blur. The eye reads "real human, real environment" only when no filter is present.

### 5.2 Framing rules

- **Crop:** chest-up. Head occupies upper 35-45% of the bottom-half frame. In the split, the top of the head can crop into the cream-card edge — that's intentional, signals "the page is bigger than the camera".
- **Eyeline:** locked center-to-slightly-off. Speaker can glance away mid-thought. Don't punish natural eye drift.
- **Position:** centered horizontally. Hands in frame are encouraged — they read as "I'm explaining something I care about".
- **Background:** the speaker's actual room (kitchen, podcast desk, framed art, plants) is **intentionally retained**. Not blurred, not keyed out, not desaturated. The room is the credibility.
- **Audio gear visible:** a Røde shotgun or boom mic in frame (bottom-right or top-right) is a STYLE SIGNAL. It says "this person owns equipment / records seriously". Keep it in shot.
- **No b-roll cutaway hides the speaker entirely** — this format does not let the editorial top half eat the speaker. Even on full-spread beats (where the top half is the hero), the bottom half holds the speaker. The format is *literally a split*.

### 5.3 Caption layer over the speaker

Single-word italic-serif captions float over the speaker's torso, ~1/3 from top of the bottom half:

```css
.speaker-caption {
  font-family: 'Fraunces', 'Caslon Display', Georgia, serif;
  font-style: italic;
  font-weight: 400;
  font-size: 56px;
  color: #ffffff;
  text-shadow:
    0 2px 6px rgba(0,0,0,.55),
    0 0 14px rgba(0,0,0,.35);
  text-align: center;
  letter-spacing: -0.005em;
  position: absolute;
  left: 50%;
  top: 30%;          /* of the bottom-half clip */
  transform: translateX(-50%);
  white-space: nowrap;
}
```

```js
// Word swap — duration matches transcript word timestamps
function swapCaption(word, startTime, duration) {
  const el = document.querySelector('.speaker-caption');
  gsap.timeline()
    .set(el, { text: word, opacity: 0, scale: 0.96 }, startTime)
    .to(el, { opacity: 1, scale: 1, duration: 0.18, ease: 'power2.out' }, startTime)
    .to(el, { opacity: 0, duration: 0.16, ease: 'power2.in' }, startTime + duration - 0.16);
}
```

One word at a time, locked centered, italic serif, white. No karaoke highlight, no all-caps, no pill background, no per-word color rotation. The italic serif IS the brand voice.

### 5.4 The hook variant: white-on-black-pill (reel A)

When the script is *all* talking head (no top-half editorial), captions shift to a different style for the hook beats only:

```css
.hook-caption-pill {
  display: inline-block;
  background: rgba(0, 0, 0, 0.92);
  color: #ffffff;
  font-family: 'Inter', 'SF Pro Text', sans-serif;
  font-weight: 700;
  font-size: 48px;
  padding: 12px 22px;
  border-radius: 10px;
  letter-spacing: -0.01em;
  text-transform: none; /* sentence case for headlines */
}
```

This pill style is reserved for **hook lines** (the headline-on-screen at the open) and for the **comment CTA closer** (`comment "AGENT"`). Mid-video word-by-word captions stay italic-serif white. Don't mix the two within a single beat.

### 5.5 Why this treatment matters

The naturally-graded speaker is the format's anti-AI tell. Every other tech-explainer aesthetic on Instagram is heavily graded — desaturated, vignetted, color-shifted. By keeping the speaker plate completely raw, this format says "I am a human in my real kitchen who has actually thought about this", which is exactly the credibility move the editorial top half needs to land. If you grade the speaker, the format collapses into "another AI bro reel".

---

## 6 · Repeatable Beat Grammar (the format)

Every "piece" of the magazine uses the same internal four-beat structure:

```
[ Section Label ]            ~0.8–1.2s   small-caps grey, "PIECE 0X · TOPIC"
   ↓
[ Headline Pair ]            ~1.5–2.0s   upright + italic, hairline rule
   ↓
[ Exhibit ]                  ~3.0–5.0s   the actual thing (list / quote / screenshot / code)
   ↓
[ Caption Beat ]             ~1.0–1.5s   italic serif word over speaker as he names the takeaway
```

A 7-10 second "atom" you can clone N times for an N-piece magazine spread.

### Beat A — Section Label
- Small-caps masthead text in tracked-out grey
- Optional unicode arrow `↳` or middle-dot `·` separator
- Audio: speaker says the section name OR uses it as a turn signal ("okay, piece two...")

### Beat B — Headline Pair
- Big serif headline, two parts: structural words upright + emphasis word italic
- Thin black hairline rule below
- Audio: speaker is delivering the topic sentence

### Beat C — Exhibit
- One of: numbered list (5 rows max), pull quote, app screenshot card, code block, hand-drawn diagram, big-stat card, form mockup
- Lives inside the cream card with consistent margins
- Audio: speaker is giving the explanation; on-page content matches but doesn't duplicate

### Beat D — Caption Beat
- Single italic-serif word floats over speaker
- The word matches the *peak* of the explanation, not every word
- Often the same word appears on the top half AND in the bottom-half caption — meta-moment alignment

### Transition between pieces
- Always a black-bezel breath (200-400ms) OR a crossfade
- Never a whip, never a directional blur, never a hard cut between two cream cards
- Audio carries continuously; the visual breath is *visual only*

This grammar is what makes a 77-second reel feel "edited" rather than "filmed". You can apply it to any list-style script: "5 things about X", "the 4 pieces of Y", "3 ways to Z".

---

## 7 · Hyperframes Implementation Recipes

### 7.1 Composition shell (the 9:16 split-format template)

```html
<div id="editorial-split" data-composition-id="editorial-split"
     data-start="0" data-width="1080" data-height="1920">

  <!-- Bezel: pure black layer -->
  <div class="bezel-bg clip"
       data-start="0" data-duration="77" data-track-index="0"
       style="background:#000; width:100%; height:100%; position:absolute;"></div>

  <!-- Speaker plate: bottom 50% of frame, untreated -->
  <div class="speaker-wrapper clip"
       data-start="0" data-duration="77" data-track-index="1"
       style="position:absolute; left:0; top:960px; width:1080px; height:960px; overflow:hidden;">
    <video src="assets/speaker.mp4" muted style="width:100%; height:100%; object-fit:cover; object-position:center top;"></video>
  </div>

  <!-- Speaker captions: italic serif white, locked over torso -->
  <div class="speaker-caption-layer clip"
       data-start="0" data-duration="77" data-track-index="2"></div>

  <!-- Editorial spreads: top 50% of frame, swap via sub-compositions -->
  <template data-composition-src="compositions/cover.html"
            data-start="0" data-duration="8" data-track-index="3"></template>
  <template data-composition-src="compositions/piece-01-loop.html"
            data-start="8" data-duration="11" data-track-index="3"></template>
  <!-- ... -->

  <!-- Paper grain overlay, subtle -->
  <div class="grain-overlay clip"
       data-start="0" data-duration="77" data-track-index="4"
       style="opacity:0.04; mix-blend-mode:multiply;"></div>

</div>

<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });
  // Captions register per-word from transcript JSON
  loadCaptions('assets/transcript.json').forEach(({ word, start, duration }) => {
    tl.add(buildCaption(word, start, duration), start);
  });
  tl.set({}, {}, 77); // pad to full duration
  window.__timelines["editorial-split"] = tl;
</script>
```

### 7.2 Section header recipe (within a piece spread)

```html
<div class="piece-header">
  <div class="masthead">PIECE 01 · THE LOOP</div>
  <div class="hairline"></div>
  <h1 class="headline">
    One <span class="italic">instruction</span> at a time.
  </h1>
  <div class="hairline"></div>
</div>
```

```css
.piece-header { padding: 56px 48px 0; }
.masthead { font-family: 'Fraunces', serif; font-size: 12px; text-transform: uppercase; letter-spacing: 0.18em; color: #7a7a76; }
.hairline { height: 1.5px; background: #1a1a1a; margin: 16px 0 24px; transform-origin: left center; }
.headline { font-family: 'Fraunces', serif; font-size: 88px; line-height: 1.02; font-weight: 700; color: #0e0e0c; letter-spacing: -0.015em; margin: 0; }
.headline .italic { font-style: italic; font-weight: 400; }
```

```js
gsap.from('.piece-header .masthead', { y: 8, opacity: 0, duration: 0.4, ease: 'power3.out' });
gsap.from('.piece-header .hairline', { scaleX: 0, duration: 0.55, ease: 'expo.out' }, '-=0.25');
gsap.from('.piece-header .headline', { y: 14, opacity: 0, duration: 0.55, ease: 'power3.out' }, '-=0.2');
gsap.from('.piece-header .headline .italic', { x: -6, opacity: 0, duration: 0.5, ease: 'power3.out' }, '-=0.4');
```

### 7.3 Numbered cascade (the rule + exception list)

See section 3.2 above — the 5-row list with one-row-different-color is the highest-leverage template. Use it whenever a script enumerates ≥3 items AND has an "exception" or "winner" callout.

### 7.4 Speaker plate (untreated)

See section 5.1. Apply once at the workspace level (in `assets/speaker-plate.css`), then every project gets the look "for free."

### 7.5 Registry block mappings

When wiring real Hyperframes blocks to this style:
- **`flash-through-white`** → use 1× per reel for the pull-quote landing or the comment-CTA closer
- **`light-leak`** → warm amber tint between section breaks (Piece 01 → Piece 02)
- **`grain-overlay`** → always on at 0.04 opacity
- **`flowchart`** → for the "comment → DM → tag → sequence" hand-drawn diagram beat
- **`data-chart`** → for the "Best day to post?" bar chart card (style with crayon/sharpie variant)
- **`app-showcase`** → for the embedded Cursor/Claude/Notion/iPad mockup cards
- **`whip-pan`** → **DO NOT USE** in this format. Whip transitions break the editorial register.
- **`shimmer-sweep`** → **DO NOT USE**. Chrome-sheen reads as tech-flashy, not magazine.

### 7.6 Caption-layer renderer

```html
<!-- A single floating element whose text content + opacity we re-tween per word -->
<div class="speaker-caption">word</div>
```

```js
// Build a sub-timeline from a transcript JSON: [{word, start, end}, ...]
function buildCaptionTimeline(transcript) {
  const tl = gsap.timeline();
  const el = document.querySelector('.speaker-caption');
  transcript.forEach(({ word, start, end }) => {
    const dur = end - start;
    tl.set(el, { textContent: word }, start)
      .fromTo(el,
        { opacity: 0, scale: 0.96 },
        { opacity: 1, scale: 1, duration: 0.18, ease: 'power2.out' },
        start)
      .to(el, { opacity: 0, duration: 0.16, ease: 'power2.in' }, end - 0.16);
  });
  return tl;
}
```

---

## 8 · Brand Adaptation

See **[`../BRAND.md.example`](../BRAND.md.example)**. The format and grammar above stays as documented; all colors, type voices, and speaker treatment defer to your `BRAND.md`.

### 8.1 What stays the same (the format)
- Hard top-bottom 50/50 split (or full-frame talking head with pill captions for hook beats)
- Black bezel + cream/paper page on top
- Speaker NOT graded — naturally lit, real environment, audio gear visible
- Two type voices (display serif upright + same family italic), never three
- Single-word italic-serif white captions over speaker
- Numbered rows with one-row-color-break
- Section labels in tracked-out small-caps grey
- Hairline rules under every headline
- Crossfades + black-bezel breaths between spreads (NO whips)
- 2.5-4.0s dwell per spread

### 8.2 What gets swapped (the brand)

**Read `../BRAND.md.example` first** — it owns the palette and type. The mapping below is what's archetype-specific:

| Source reel element | Brand equivalent |
|---------------------|-------------------------|
| Cream paper `#efece0` | `--background-paper` (per BRAND.md) — keep the warmth |
| Default classical serif (Caslon/Tiempos/Eames) | Voice A from BRAND.md — classical display serif |
| Italic emphasis in near-black | Voice B from BRAND.md — same family italic in `--primary-mid` |
| **Lime / chartreuse `#c8d63a` row underline** | `--primary-mid` — replaces lime as the default row color. NO neon under most modern brands. |
| **Hot orange exception `#e85a1f`** | `--accent-warm` — keeps the warm exception color, slightly more muted |
| Code block monospace (Geist Mono) | Voice C from BRAND.md — Geist Mono / Roboto Mono / JetBrains Mono |
| Caption italic serif white over speaker | Stays italic-serif white per BRAND.md. Single emphasis word goes `--primary-mid`. |
| Editorial red hero card `#c41e1e` | `--accent-alert` for once-per-reel hero card, OR `--anchor-near-black` for an anchor moment |

The naturally-graded speaker treatment **stays.** Audiences are conditioned to expect either heavily graded reels OR low-effort phone footage — the "I sat down at my kitchen counter and thought about this" energy differentiates by being neither.

### 8.3 What does NOT translate
- **Don't desaturate the speaker.** This is the inverse of sage-stack. Desaturating breaks the format's entire credibility move.
- **Don't add gradient buttons, glassmorphism, or chrome-sheen cards.** Those belong to sage-stack / SaaS-promo aesthetics. This format is *paper*.
- **Don't put two exhibits on one spread.** Density is anti-editorial. One numbered list OR one pull quote OR one screenshot, never two.
- **Don't whip-transition between spreads.** Crossfades and black-bezel breaths only.
- **Don't use neon color in body type.** Body type stays near-black `#0e0e0c`.
- **Don't use sans-serif for headlines.** The serif IS the format. Switching to Inter/Montserrat for headlines is the format collapsing.
- **Don't pile decorative accents.** One accent color per scene, doing one job. Two is decoration. Decoration is anti-format.

### 8.4 When NOT to use this style at all
- Comedy / reaction reels — too slow, too curated
- Product-launch hype reels — needs energy this format doesn't carry
- Anything under 30 seconds — the dwell math doesn't support the format below 30s
- Anything where the speaker is in motion (walking-and-talking) — the split format requires a locked-down podcast/desk plate

---

## 9 · Pre-flight Checklist (run before claiming a video matches this style)

1. ☐ Frame has a **hard horizontal split at ~50%** OR is full-frame talking head with pill captions only — never PiP, never floating face-card
2. ☐ Top half has a **black bezel** (top edge) and a **cream/paper card** inset inside it
3. ☐ Speaker plate is **NOT graded** — natural color, real room, audio gear visible
4. ☐ All headlines use a **classical display serif** (Fraunces / Caslon / Tiempos), never Inter / Montserrat / Helvetica / Recoleta
5. ☐ Italic emphasis word is in the **same family as upright** (not Lucida, not Comic Sans Italic, not a different family)
6. ☐ Captions over speaker are **single-word italic-serif white**, centered, ~52-64px, no pill background
7. ☐ Numbered rows have **all four parts**: numeral, word, subtitle small-caps, color underline
8. ☐ Exactly **ONE row per list breaks the underline color** (lime → orange) for the exception/winner moment
9. ☐ Section labels are **tracked-out small-caps grey** (`letter-spacing: 0.18em`, `#7a7a76`)
10. ☐ Every headline has a **thin black hairline rule** above OR below it
11. ☐ Spreads dwell **2.5-4.0s** before swapping — count beats, divide duration, must fall in range
12. ☐ Transitions between spreads are **crossfade or black-bezel breath**, never whip / blur / zoom
13. ☐ Speaker `<video>` plays **continuously through spread swaps** (the bottom half never cuts when the top half does)
14. ☐ Accent color (lime / orange / cyan) appears at most **2× per scene**, never decoratively
15. ☐ Page layout has **breathing room** — generous margins, never two exhibits on one spread
16. ☐ Paper grain overlay is on at low opacity (~3-5%) for the entire duration
17. ☐ "What Would Editorial Magazine Do" gut check: does this clip feel like a paused page from a print quarterly with a podcast clip beneath it? If the answer is "no" because something feels too neon / too animated / too tech-UI, dial it back

---

## 10 · Open Questions (verify when more data is available)

- **Speaker pace** — both creators in the split-format videos appear to speak at ~140-160 wpm (slower than sage-stack). Confirm via transcript word-timestamps; this drives the per-word caption swap math.
- **Music bed** — the editorial register suggests no music or very low-amplitude lo-fi. Confirm by extracting audio and measuring under-VO RMS. If there's a bed, it's almost certainly under -28dB.
- **Transition timing** — the black-bezel breath between spreads looks like 200-400ms but couldn't measure precisely from frames. Confirm by frame-stepping in DaVinci or ffprobe.
- **Caption emphasis frequency** — italic captions appear to swap ~1 word per 600-900ms (not literally every word). Confirm whether the format uses *every* spoken word or just the *emphatic* ones (current read: emphatic only).
- **Top-half-only beats** — reel A spends most of its runtime as full-frame talking head with one editorial card revealed mid-reel. Need to confirm whether the editorial card is held for ~8s or just flashed.
- **Hand-drawn elements** — reel C's tablet-mockup carousel uses crayon/sharpie chart styles. Whether this is hand-drawn-rendered-as-asset or a Procreate screenshot affects how you'd build it (SVG vs. PNG).
- **Caption typography on speaker plate** — couldn't confirm whether the italic-serif font on the speaker captions is the same family as the headlines (likely yes — Fraunces / Tiempos). One transcript pull would resolve this.
