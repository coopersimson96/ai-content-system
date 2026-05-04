# Sage-Stack Motion Style — Deconstruction

> Reference reel: an Instagram Reel by Greg Isenberg titled "AI agent stack" (~49s, 9:16 vertical, 720x1280, 30fps)
> Genre: Talking-head + B-roll motion graphics, AI/tech explainer, "5-layer breakdown"
> Working alias for this aesthetic: **Sage Stack** - desaturated talking head + sage-green 3D cards with chrome sheen

This is a deconstruction of one specific reel into a reusable motion-graphics playbook. The goal is *not* one-to-one recreation — it is to extract the **visual DNA** so it can be applied to your scripts via Hyperframes without copying the source.

---

## 0 · The 10 Laws (memorize)

1. **The talking head is grayscale; the graphics are sage.** This is the single biggest stylistic move in the source reel. The speaker is desaturated to near-monochrome with only a faint cool wash on skin. All saturation in the frame is reserved for branded B-roll (sage cards, logo colors). Reading order is enforced by color: your eye goes to color first, face second. **Note:** under your own brand you may invert this (see Section 8 — naturally graded speaker is the modern-creator default).
2. **Sage green owns the whole world.** One dominant brand hue (~`#7AC4A8` mid, `#3F6B58` deep, `#A8D9C2` highlight) acts as background, surface, and text accent across every scene. Color discipline = identity.
3. **Every card is a 3D physical object.** Cards are not flat CSS rectangles - they are rendered with depth, beveled edges, drop shadows, and a *diagonal chrome shimmer* from upper-right to lower-left. They look like injection-molded plastic chips, not UI surfaces.
4. **One idea per beat, ~2.5s average.** The 49s reel runs ~20 distinct beats (intro hook, 5 layer reveals × 2-3 sub-beats each, outro CTA). Slower than a hard-cut comedy reel but still kinetic. Each beat lands ONE label.
5. **Numbers structure everything.** A "1, 2, 3, 4, 5" stack opens the reel and recurs. The viewer is told upfront: "this is a five-part breakdown." Listicle scaffolding is the trust device that earns attention for the whole 49s.
6. **Type does the heavy lifting.** Two voices: a chunky **dark-green Recoleta-style serif** for nouns/structure ("Ops Brain", "Outbound", "First, the...") and a **sage italic display script** for emphasis/qualifiers ("agent harness", "distribution", "full"). The italic is always sage; the upright is always near-black green.
7. **Whip-blur, never hard-cut.** Every transition between B-roll beats uses a directional motion blur — most often a vertical or diagonal swipe with chromatic-aberration fringing on the leading edge. The cut is hidden inside the blur. Hard cuts only happen between speaker shots and graphic shots, never between two graphic shots.
8. **Speaker stays put; graphics orbit him.** The talking head is locked centered, mid-zoom, mic visible bottom-right. Graphics enter the frame around him (above, beside, in-front-of-face) and exit by whip-blur. He doesn't move; the world rearranges around him.
9. **Real product logos, not mockups.** Cursor, Perplexity, Exa, Firecrawl, Obsidian, Notion, Instantly all appear with their actual brand marks - rendered as 3D app icons or floating logos. Specificity earns credibility. Generic placeholder UI would tank the whole vibe.
10. **End on a CTA that names the engagement action.** "comment 'AI Stack'" — explicit, two words, in the dominant type system. The closer is not "subscribe" or "follow" — it's a comment-bait phrase that maps to algorithmic distribution.

---

## 1 · The Reference Timeline (49s, beat-by-beat)

| Time | Beat | Layer | What's on screen | Engine |
|------|------|-------|------------------|--------|
| 0.0-1.5 | **Hook** | — | Speaker grayscale, sage 3D cube labeled "AI" hovering over mouth, slight rotation | Object metaphor: the topic |
| 1.5-3.0 | **List preview** | — | 5 sage cards numbered 1-5 cascade in diagonally from top-left to bottom-right, slight 3D tilt, chrome shimmer | "Here's what you're getting" |
| 3.0-6.5 | **Caption: "Here's the full agent stack"** | — | Same 5-card stack now showing icons; two-line caption underneath in serif + italic-script. Light-grid texture replaces solid bg | Hook payoff |
| 6.5-8.5 | **"First, the agent harness"** | 1 | Pure background, hero text only, dark-green serif ("First, the") + sage italic ("agent harness") with subtle warm-orange shadow halo | Section header |
| 8.5-11.0 | **Cursor reveal** | 1 | Speaker returns, 3D Cursor diamond logo floats top-right, label "Cursor" underneath. Faint sage tint creeps back into background | Tool name #1 |
| 11.0-14.5 | **Claude Code window** | 1 | Notes/list-style window slides in from right edge, titled "claude code – agent harness", listing main-agent / web-searcher / index-retriever / scraper-agent / data-normalizer / ops-planner / debugger / email-sender / slack-dispatcher with status dots. Coral-red highlighted band on "OPS BRAIN AI" group. | Tool name #2 + concept demo |
| 14.5-16.5 | **Whip transition → Search layer** | 2 | Vertical streak with chromatic fringing; dark search bar appears mid-frame with iridescent purple/orange/cyan border glow, magnifying glass icon, "Next" cursor | Section transition |
| 16.5-19.0 | **"Next is the search layer"** | 2 | Same search bar, text fully typed; two empty sage rounded-square cards appear below | Section header (typed-in-search-bar treatment) |
| 19.0-21.0 | **Perplexity + Exa** | 2 | Cards now hold the actual Perplexity and Exa logos (3D extruded white linework on sage), labels below in white serif | Tool reveals |
| 21.0-23.0 | **Perplexity flowchart + glass card** | 2 | Sage backdrop holds a Perplexity-branded architecture diagram (search → query → re-rank → vector index); a frosted-glass "liquid glass" card overlays it with corner-bracket frame and the caption "that go and find information..." sweeping in | Concept demo |
| 23.0-25.0 | **Folder-tab transition** | 3 | Horizontal sage backdrop; manila/cream file folders slide in from below with tabs labeled "web", "data", "layer"; Google homepage peeks behind the front folder | Section transition (folder metaphor) |
| 25.0-27.0 | **Speaker inside folder frame** | 3 | Speaker's headshot becomes a "document" inside the folder, with the folder-tab labels still visible above his head ("the web data layer") | Section header (speaker-as-document) |
| 27.0-29.0 | **Scraping JSON window** | 3 | Light-mode code window centered, JSON schema visible (`url`, `markdown`, `json`, `screenshot`), small "Scraping..." status pill bottom-right | Concept demo |
| 29.0-31.0 | **Firecrawl logo + Scrape/Crawl cards** | 3 | Firecrawl wordmark + flame icon centered; two stacked iOS-style URL-input cards beneath, modes "Scrape" and "Crawl"; orange action-button accent on second card | Tool reveal |
| 31.0-32.5 | **Firecrawl Extract** | 3 | Card recomposes: now showing "Extract" mode, single URL field with orange CTA arrow | Tool capability #2 |
| 32.5-35.0 | **"Ops Brain"** | 4 | Dark-green serif title appears above speaker; Obsidian (purple crystal) and Notion (N icon) 3D app icons drop in alongside title | Section header + tool reveal |
| 35.0-37.5 | **Context Notes card** | 4 | Sage 3D pebble-shaped surface appears front-camera; a black "Context Notes 02/03/2026" sub-card overlays it with sage type and tiny app icons in corners; whole assembly tilts and exits via whip-blur | Concept demo |
| 37.5-40.0 | **"Outbound"** | 5 | Speaker returns; dark-green serif "Outbound" appears above his head, slight orange-warm halo | Section header |
| 40.0-43.0 | **Find Clients (Instantly)** | 5 | Blue gradient card with "Find Clients ⚡ Instantly" headline and sample chat-prompt UI; tilts in 3D space with iridescent edge highlight | Tool reveal #1 |
| 43.0-45.5 | **Two-card distribution stack** | 5 | Blue Instantly card stays top; yellow gradient assistant card ("How can I assist you?") drops in below; caption "can be used for distribution" sweeps under in serif + italic | Use-case demo |
| 45.5-47.0 | **"how to turn this into"** | — | Speaker centered, three words appear at different scales/timings ("how" · "to turn" · "this" · "into"), staggered fall-in, sage and white | Outro setup |
| 47.0-48.7 | **CTA: comment "AI Stack"** | — | Speaker smiles, dark-green serif "comment" + white serif "AI Stack" in quotes, locked center-frame, hold to end | Engagement instruction |

**Five-act structure** (the rule of fives, not threes - because it's a 5-layer stack):
- **Hook (0-6s):** The cube + the numbered preview = the trust device
- **Layers 1-5 (6-45s):** Each layer = section header → tool reveal → concept demo (~7-8s per layer)
- **Outro (45-49s):** "how to turn this into..." → comment CTA

Notice: each layer beat has the **same internal grammar** (header → tool name → demo). That repeatability is what makes this format scalable.

---

## 2 · The Visual Vocabulary

### 2.1 Backgrounds (in priority order)

| # | Background | Where it lives | How to build in Hyperframes |
|---|-----------|----------------|---------------------|
| 1 | **Soft warm-gray gradient** | Most B-roll scenes (cards floating in space) | `radial-gradient(ellipse at 50% 30%, #f0ece5 0%, #c9c4bc 65%, #8a8680 100%)`. Slight vignette darkening lower-right. Add 1.5% film grain via `grain-overlay` component. |
| 2 | **Sage-green wash** | Layer-transition beats, "Ops Brain" / "Outbound" titles | `linear-gradient(180deg, #4a7565 0%, #6a9e88 60%, #4f7a68 100%)`. Always with a soft top-light highlight band. |
| 3 | **Faint perspective grid** | "Here's the full agent stack" beat | `repeating-linear-gradient(0deg, rgba(0,0,0,.04) 0 1px, transparent 1px 64px)` × 2 axes on top of warm-gray. Scale ~64px tile. |
| 4 | **Liquid-glass card overlay** | Perplexity flowchart beat | `<div>` with `background: rgba(255,255,255,.08); backdrop-filter: blur(18px) saturate(1.1); border: 1px solid rgba(255,255,255,.18); border-radius: 22px; box-shadow: inset 0 1px 0 rgba(255,255,255,.22), 0 30px 60px rgba(0,0,0,.18);` + corner brackets as separate inset SVGs. |
| 5 | **Speaker treatment** | All speaker scenes | Source reel: heavy desaturation. Modern-brand override: naturally graded - see Section 8 |
| 6 | **Folder-paper tab system** | Web Data Layer beat | Manila-cream folders (`#e8dcc1`) with tabbed top edges via `clip-path: polygon(...)` per folder, slight rotational stagger, soft drop shadow. |

### 2.2 Type System

**Two type families, two roles, never violated.**

#### Voice A — "Structural" (display serif, dark green, near-black)
- Family: chunky display serif. Recoleta, Caslon Display, or Playfair Display Bold all read correctly. Substitute Instrument Serif Bold or similar.
- Color: `#1f3a2c` (very dark forest green, almost black)
- Weight: Bold
- Treatment: subtle warm-orange/amber shadow offset 0px 1px 0px `#c8843a` — gives the type a "printed on warm paper" feel
- Use for: section headers ("Ops Brain", "Outbound"), structural words ("First, the", "Here's the", "comment"), CTA verbs

#### Voice B — "Emphasis" (italic script, sage)
- Family: italic display script. Recoleta Italic, Cooper BT Italic, or a warm-italic serif like Playfair Italic
- Color: `#6a9e88` to `#8fb8a3` (sage)
- Weight: Regular italic
- Treatment: same warm shadow, smaller scale than the structural words it sits next to
- Use for: emphasis words inside a header pair ("agent **harness**", "the **search layer**", "for **distribution**", "AI **Stack**")

#### Voice C — "UI Mono" (in-product overlays only)
- Family: SF Mono / JetBrains Mono / Geist Mono
- Color: dark gray on light surfaces (`#444`)
- Use for: code/JSON in the Scraping window, app sidebar text in Claude Code window
- Never used for narration captions. Lives only inside fake-UI screenshots.

#### Animation patterns (spoken-word reveal)
- **Section header pair:** structural word slides up 30px with 0.4s `power3.out`; italic emphasis follows 80ms later with the same motion. Stagger creates the "thought completing itself" feel.
- **CTA:** "comment" lands first; "AI Stack" lands 200ms later with a slight scale-from-0.92.
- **In-frame phrase:** ("how to turn this into") - each word lands separately at increasing y-positions, ~120ms stagger, varies sizes (32/48/40px). Feels handwritten, not animated.
- All text uses `expo.out` or `power3.out`. No bouncy springs. No rotate-in. The text feels confident, not playful.

### 2.3 Color Story (memorize the meanings)

| Color | Hex (approx) | Meaning | Where used |
|-------|--------------|---------|------------|
| **Sage mid** | `#6a9e88` | Brand hue / surfaces / emphasis type | Cards, italic captions, ambient washes |
| **Sage deep** | `#3f6b58` | Card edges / shadows / 3D depth | Bevels, text on light bg |
| **Sage light** | `#a8d9c2` | Highlights, chrome sheen on cards | Diagonal sweep on every card |
| **Forest near-black** | `#1f3a2c` | Structural type, anchoring | Headers, CTA verbs |
| **Warm cream** | `#f0ece5` | Background paper feel | All non-sage scenes |
| **Speaker gray** | desat `#666-#aaa` | The narrator's world (source-reel grading only) | Talking-head treatment |
| **Coral red** | `#e8a591` | "Active" / "alert" highlight | Ops Brain sidebar group, accent only |
| **Iridescent purple→cyan→amber** | gradient | Premium UI surfaces | Search-bar border (Perplexity scene) |
| **Hot orange** | `#e85a1f` | CTA buttons inside fake UI | Firecrawl arrow buttons only |
| **Brand-blue gradient** | `#3a7eed → #6c9aff` | Foreign-brand surfaces (Instantly) | Outbound section card |
| **Honey-yellow gradient** | `#f5d985 → #f0c060` | Foreign-brand surfaces (assistant card) | Outbound section second card |

**Discipline:** the sage-green family + warm-cream + speaker grading = 90% of every frame. The remaining 10% is foreign-brand color (orange Firecrawl, blue Instantly, yellow assistant) deployed *only when introducing the product the brand actually owns*. You don't drop blue or yellow in for decoration. They earn their place by being a real product surface.

---

## 3 · The Card System (the format DNA)

The Sage Card is the most copyable element. Every B-roll beat eventually reduces to a card.

### 3.1 The card recipe

```css
.sage-card {
  background: linear-gradient(135deg, #84b9a3 0%, #6a9e88 35%, #5a8a78 65%, #6a9e88 100%);
  border: 1px solid #4f7a68;
  border-radius: 14px;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.35),     /* top inner highlight */
    inset 0 -2px 4px rgba(0,0,0,.18),         /* bottom inner depth */
    0 12px 28px rgba(0,0,0,.22),              /* drop shadow */
    0 2px 6px rgba(0,0,0,.12);                /* contact shadow */
  position: relative;
  overflow: hidden;
}

/* The diagonal chrome shimmer — the signature move */
.sage-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    transparent 0%,
    transparent 30%,
    rgba(255,255,255,.28) 45%,
    rgba(255,255,255,.10) 55%,
    transparent 70%,
    transparent 100%
  );
  pointer-events: none;
}
```

The diagonal sheen is what makes the card read as a 3D rendered object instead of flat CSS. Without it, the card looks like a Bootstrap button. With it, it looks like an injection-molded chip.

### 3.2 Card animations (the four moves)

1. **Drop-in** (number cards, layer cards) — `y: -120, opacity: 0, rotateX: -25, scale: 0.9` → rest, `0.55s expo.out`, with `0.12s` stagger across siblings.
2. **Tilt-and-orbit** (single-card hero, e.g. Cursor logo card) — gentle continuous `rotateY` between -6° and +6° on a 4s sine loop. Keeps the card "alive" during dwell.
3. **Whip-exit** — `x: +600, y: -200, rotate: 12, opacity: 0, filter: 'blur(20px)'` over `0.35s power2.in`. Always paired with a chromatic-aberration streak overlay across the same frames.
4. **Stack-recompose** (Firecrawl Scrape → Crawl → Extract) — top card slides up 16px and fades to 0.5, new card grows from 0.94 to 1.0 underneath, both shift to recombine. ~0.6s total.

### 3.3 The number-card opener (recipe)

```html
<!-- 5 sage cards, cascading diagonally with stagger -->
<div class="card-stack">
  <div class="sage-card" style="--n: 1; --x: -120px; --y: -200px;">1</div>
  <div class="sage-card" style="--n: 2; --x: -60px; --y: -100px;">2</div>
  <div class="sage-card" style="--n: 3; --x: 0; --y: 0;">3</div>
  <div class="sage-card" style="--n: 4; --x: 60px; --y: 100px;">4</div>
  <div class="sage-card" style="--n: 5; --x: 120px; --y: 200px;">5</div>
</div>
```

```js
gsap.from('.sage-card', {
  y: '-=180',
  opacity: 0,
  rotateX: -28,
  scale: 0.88,
  duration: 0.55,
  ease: 'expo.out',
  stagger: 0.12,
});
// Once landed, the chrome shimmer starts to gently pan
gsap.to('.sage-card::before', {
  backgroundPosition: '200% 200%',
  duration: 6,
  ease: 'sine.inOut',
  repeat: -1,
  yoyo: true,
});
```

---

## 4 · Motion Patterns

### 4.1 Transition library

| Transition | When to use | Hyperframes block |
|-----------|-------------|-------------------|
| **Vertical whip-blur with chromatic fringe** | Between layer sections | `whip-pan` block, customize fringe color to amber/cyan/magenta |
| **Folder-tab slide-up** | Web Data Layer entry | Custom: 3 folders translate up from y=+800, stagger 80ms, slight tilt `rotateZ(-2deg)`, easing `back.out(1.4)` |
| **Card stack-recompose** | Tool capability switches (Scrape → Crawl → Extract) | See 3.2 |
| **Liquid-glass slide-in** | Concept overlay (Perplexity flowchart) | Glass card translates in from right with `x: +400, opacity: 0`, blur scales from 0 to 18px concurrently |
| **Speaker-cube-floating** | Hook | 3D cube `rotateY` + `rotateX` continuous loop, `y` 8px sine drift, no entry animation (just appears in scene) |
| **Title-with-shadow-orange-pop** | Section headers | Type starts at `y: +30, opacity: 0, scale: 0.96`; lands with `expo.out 0.4s`; warm-amber shadow appears 60ms after via separate text-shadow tween |

### 4.2 Easing rules

- Type entries: **`expo.out`** or **`power3.out`** (confident, not bouncy)
- Card entries: **`expo.out`** for big drops, **`back.out(1.4)`** only when a slight bounce reads as physical (folder tabs landing into a stack)
- Card exits: **`power2.in`** or **`expo.in`** with motion blur — exits should feel decisive
- Continuous idle motion: **`sine.inOut`** — the only place sine lives, for breathing/floating
- Never use `bounce`, `elastic`, or `circ` — those would break the "premium calm" register

### 4.3 The whip-blur recipe (the most-used transition)

```js
// Outgoing: whatever's leaving accelerates upward + blurs
const out = gsap.timeline()
  .to(currentScene, {
    y: -800,
    filter: 'blur(24px)',
    duration: 0.28,
    ease: 'power2.in',
  })
  .to('.streak-overlay', {  // a thin vertical streak with chromatic-aberration stripe
    opacity: 1,
    scaleY: 1.4,
    duration: 0.22,
    ease: 'power2.out',
  }, 0.06);

// Incoming: next scene rises into a cleared, lit frame
const in_ = gsap.timeline()
  .from(nextScene, {
    y: 600,
    filter: 'blur(20px)',
    duration: 0.36,
    ease: 'expo.out',
  });
```

The streak overlay is a 12px-wide vertical `<div>` with three side-by-side `linear-gradient` columns (red `rgba(232,90,31,.6)`, white `rgba(255,255,255,.9)`, cyan `rgba(80,180,200,.6)`) — the chromatic-aberration look without an actual shader.

---

## 5 · The Speaker Treatment (CRITICAL — this is half the style)

### 5.1 The grading

The source reel heavily processes the speaker. To replicate via a CSS filter on the `<video>` wrapper:

```css
.speaker-video {
  filter:
    saturate(0.18)        /* near-grayscale */
    contrast(1.12)        /* punchy */
    brightness(0.96)      /* slightly down */
    sepia(0.04);          /* tiny warm bias */
}
```

**Modern-creator override:** under most modern brands, the speaker is naturally graded (no filter). The desaturated treatment reads as "another AI bro reel" by 2026. Choose intentionally per `BRAND.md`.

### 5.2 Framing rules

- **Crop:** chest-up, head occupies upper 45% of frame, mic visible bottom-right
- **Eyeline:** locked center, never drifts
- **Position:** centered horizontally, head-anchor never moves
- **Background:** the speaker's actual room (shelving) is intentionally retained — *not* keyed out — but desaturated and slightly blurred (source reel) OR fully visible (modern override).
- **No b-roll cutaway hides the speaker entirely** — graphics overlay him or sit beside him; he is rarely off-screen for more than 2 seconds at a stretch.

### 5.3 Why this treatment matters

The grayscale-speaker / colorful-graphic split is the entire **reading hierarchy** in the source reel. It's how the editor controls where your eye goes. If you apply sage-green graphics over a *normally-graded* talking head, the graphics will fight the face for attention. Most modern creators solve this differently — by making the graphics 3D-rendered with depth, the graphics pop without needing the face to recede. Decide which strategy your brand commits to.

---

## 6 · The Repeatable Beat Grammar (the format)

This is the part you actually want to copy. Every layer in the reel uses the same internal three-beat structure:

```
[ Section Header ]            ~1.5–2.0s
   ↓
[ Tool Reveal ]               ~2.0–2.5s
   ↓
[ Concept Demo (UI/diagram) ] ~2.5–3.0s
```

A 7-second "atom" you can clone N times for an N-layer breakdown.

### Beat A — Section Header
- Speaker visible OR pure background
- Big serif title above/over speaker: `<dark-green-structural> + <sage-italic-emphasis>`
- Optional: 1-2 app icons drop in alongside the title
- Audio: speaker says the section name + a 4-8 word description

### Beat B — Tool Reveal
- B-roll only (no speaker)
- Tool's brand mark + name in white serif
- Either as a sage card with extruded white linework, or as a freestanding logo
- Audio: speaker says "I use [Tool] for [job]"

### Beat C — Concept Demo
- Fake-UI mockup of the tool in action (card with code, chat panel, dashboard)
- Light shadow, slight tilt (~3-5° rotateY), entry from below or right
- Speaker may return as a small layer behind/over it
- Audio: speaker says *what the tool does in one sentence*

### Transition between layers
- Always whip-blur (vertical or diagonal)
- 0.5-0.7s including exit + entry
- Audio carries continuously; the whip is *visual only*, no audio gap

This grammar is what makes the 49s feel "designed" rather than improvised. You can apply it to any list-style script: "5 ways to...", "3 tools that...", "the 4-step flow...".

---

## 7 · Hyperframes Implementation Recipes

### 7.1 Composition shell (the 9:16 sage-stack template)

```html
<div id="agent-stack" data-composition-id="agent-stack" data-start="0" data-width="1080" data-height="1920">
  <!-- Background layer -->
  <div class="bg-warm-gray clip" data-start="0" data-duration="49" data-track-index="0"></div>

  <!-- Grain overlay (always on) -->
  <div class="grain-overlay clip" data-start="0" data-duration="49" data-track-index="1"></div>

  <!-- Speaker video, masked + graded -->
  <div class="speaker-wrapper clip" data-start="0" data-duration="49" data-track-index="2">
    <video src="assets/speaker.mp4" muted></video>
  </div>

  <!-- Sub-compositions per beat -->
  <template data-composition-src="compositions/v01-hook.html"
            data-start="0" data-duration="6.5" data-track-index="3"></template>
  <template data-composition-src="compositions/v02-layer1-harness.html"
            data-start="6.5" data-duration="8" data-track-index="3"></template>
  <template data-composition-src="compositions/v03-layer2-search.html"
            data-start="14.5" data-duration="8.5" data-track-index="3"></template>
  <!-- ...etc through layer 5 + outro -->

  <!-- Karaoke captions -->
  <div class="captions clip" data-start="0" data-duration="49" data-track-index="4"></div>
</div>
```

### 7.2 Section header recipe

```html
<div class="section-header">
  <span class="structural">Ops</span>
  <span class="structural">&nbsp;Brain</span>
</div>
```

```css
.section-header {
  font-family: 'Recoleta', 'Instrument Serif', Georgia, serif;
  font-weight: 700;
  font-size: 96px;
  color: #1f3a2c;
  text-shadow: 0px 1px 0px #c8843a, 0 4px 12px rgba(0,0,0,.18);
  letter-spacing: -0.01em;
}

.structural { display: inline-block; }
.emphasis {
  display: inline-block;
  font-style: italic;
  color: #6a9e88;
  font-size: 0.92em;
}
```

```js
gsap.from('.section-header > span', {
  y: 30,
  opacity: 0,
  scale: 0.96,
  duration: 0.42,
  ease: 'expo.out',
  stagger: 0.08,
});
```

### 7.3 Numbered cascade opener

See section 3.3 above - the 5-card stack is the highest-leverage template. Use it whenever a script enumerates ≥3 things.

### 7.4 Speaker grading wrapper

See section 5.1. Apply once at the workspace level (in `assets/speaker-style.css`), then every project gets the look "for free."

### 7.5 Registry block mappings

When wiring real Hyperframes blocks to this style:
- **`whip-pan`** → use as the layer transition with custom amber/cyan fringe params
- **`grain-overlay`** → always on, opacity ~0.04
- **`light-leak`** → use sparingly between major sections, sage-tinted
- **`flowchart`** → for the Perplexity / agent-architecture diagrams
- **`app-showcase`** → for the Firecrawl Scrape/Crawl/Extract card stack
- **`logo-outro`** → adapt for the comment-CTA closer

---

## 8 · Brand Adaptation

See **[`../BRAND.md.example`](../BRAND.md.example)** — the brand template. The format and grammar above stays as documented; all colors, type voices, speaker treatment, and grain settings defer to your `BRAND.md`. Sage palette + warm cream + classical serifs is one possible default. Pick yours.

### Archetype-specific overrides

A few things that BRAND.md leaves to the format, and that this archetype prescribes:

- **Whip-blur transitions stay.** BRAND.md may allow hard cuts as a workspace default; sage-stack overrides to whip-blurs because they're the format's signature.
- **Sage 3D chrome cards** — the cards ARE BRAND.md's primary brand color rendered as 3D chrome via the recipe in section 3.1. Don't substitute a different hue for the whole archetype.
- **Speaker grading inversion vs. the source reel.** The Greg Isenberg reference desaturates the speaker. Under a modern-creator brand the speaker stays naturally graded (BRAND.md rule). The sage cards still pop because they're 3D-rendered, not because the face is faded. This is a deliberate fork from the source.

### What does NOT translate from the Greg reference

- **Don't desaturate the speaker** unless your brand explicitly calls for it. The Greg signature move reads dated by 2026.
- **Don't copy the "AI agent stack" content verbatim** — that's a one-shot creative. The repeatable thing is the grammar (header → tool reveal → demo, ~7s/layer), not the topic.
- **Don't lift Greg's specific font** if it's identifiably Recoleta. Use whatever Voice A serif your BRAND.md locks in.
- **Pick your own CTA keyword** — don't reuse "Comment 'AI Stack'."

---

## 9 · Pre-flight Checklist (run before claiming a video matches this style)

1. ☐ Talking head treatment matches your brand's grading rule (desaturated OR naturally graded - chosen consciously)
2. ☐ All graphic surfaces use the **brand hue** consistently (no random color injections)
3. ☐ Every B-roll card has the **diagonal chrome sheen** (not a flat fill)
4. ☐ Section headers use **two type voices** (structural + emphasis), never one
5. ☐ Italic emphasis word is **always the brand color**, never the structural color
6. ☐ Transitions between B-roll scenes are **whip-blur**, never hard cut
7. ☐ Talking-head ↔ B-roll transitions can hard-cut (this contrast is intentional)
8. ☐ Average beat is **2.0-2.8s** — count beats, divide duration, must fall in this range
9. ☐ A **numbered list** structures the whole video (cascade opener present)
10. ☐ Real product logos appear, not placeholder UI
11. ☐ Speaker stays **centered, locked, mic visible** for every speaker shot
12. ☐ Outro is a **comment-bait CTA in the structural type voice** (not a generic "follow")
13. ☐ Frame grain overlay is on for the entire duration at low opacity (~4%)
14. ☐ No bouncy/elastic easing — only `expo.out`, `power3.out`, `back.out(1.4)`, `sine.inOut`
15. ☐ "What Would Sage-Stack Do" gut check: would this clip feel at home next to the reference reel? If the answer is "no" because something feels too playful or too neon, dial it back

---

## 10 · Open Questions (verify when more data is available)

These are inferences that would need confirmation from audio transcription on the source reel:

- **Voice tone** — speaker pace + cadence likely "calm authoritative, not high-energy bro." Confirm via transcript.
- **Music bed** — whether there's a music underscore or pure VO. Reels in this aesthetic typically have a low-amplitude lo-fi bed.
- **Karaoke caption presence** — on-screen typography for *headlines* is clear, but full word-level karaoke captions need confirmation. Default assumption: yes, in a small white sans-serif at safe-zone-bottom.
- **Outro hold duration** — final CTA frame appears to hold ~1.5s. Want to confirm whether it extends to a full 2-3s for algorithm completion-rate optimization.
