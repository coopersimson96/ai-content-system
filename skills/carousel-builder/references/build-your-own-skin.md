# Build Your Own Style Skin

The shipped `style-field-manual.md` is a reference. To make carousels that look like *yours*, build your own skin. This is the same process used to build the field-manual skin.

The whole idea: instead of telling the model "make it look modern", you give it a **locked visual spec** with hex codes, type names, motif rules, and corner systems — so every slide in every carousel inherits the same visual DNA.

## Step 1 — Build a design board

Pull 6–12 visual references that share a feeling. Sources:

- Instagram saves (carousels you keep coming back to)
- Pinterest boards (editorial design, posters, book covers, brand systems)
- Magazine spreads (especially Apartamento, IT'S NICE THAT, Wired, MIT Tech Review, Eye)
- Brand identity systems on Are.na or itsnicethat.com
- Screenshots of websites you find beautiful
- Album covers, movie posters

Keep them in one folder. Name them `ref-01.png`, `ref-02.png`, etc.

**Trim ruthlessly.** 6–12 images is enough. Twenty is too many — the visual signal gets diluted.

## Step 2 — Name the vibe in one sentence

Look at your board. What is the *feeling* across all the references? Not "minimalist", not "modern" — those are useless. Try:

- "AI lab notebook found in a back-room engineering office"
- "Forensic dossier with editorial blow-up typography"
- "Creator-education swipe file"
- "Brutalist sports-page front cover"
- "Soft Scandinavian magazine spread"
- "Y2K teen magazine collage"

If you can't name it in one sentence, your board isn't tight enough. Trim more.

## Step 3 — Extract the hard specs

Open your board side-by-side with a fresh `references/style-XXX.md` file (copy `style-field-manual.md` as a starting point). Fill in each section using only what you can *observe* in your references — not what you imagine.

### Palette

Eyedrop the actual hex values from your references. Pick 4–7 colors:
- 1 background
- 1 primary text (rarely pure black — usually #0A0A0A or #1A1A1A)
- 1 accent (the one bright color that pops on every slide)
- 1 dark panel (for reverse-out cards)
- 1 inverse text (the color *inside* the dark panel)
- 1 secondary accent (optional)

Write down what each color is used for. **Never** describe a color as "warm" or "cool" — write the hex.

### Typography

For each typographic role, name a **specific font family** (or 2–3 close substitutes the model can pick from):
- **Display headline** — the giant text on slide 1. Examples: "Druk Wide Condensed", "Anton", "PP Editorial New", "JetBrains Mono", "Söhne Breit"
- **Body / support** — the small text under the headline
- **Metadata corners** — the tiny labels in the corners
- **Buttons / pills** — small-caps tags

Spec the **size** at 1080×1440 source (e.g. "120pt", "220–280pt", "16pt small caps"). Spec the **tracking** (tight, normal, wide). Spec which words flip to the accent color.

### Background + texture

- Pure color, gradient (max one tonal step), or texture (paper grain, grid, noise, dots)?
- If grid: spacing, line color, line opacity
- If paper: scanned grain, subtle vignette, none

### Layout grid

- Outer margin in pixels
- Inner grid spacing
- Where the headline lives (top, full-bleed, left-half)
- Where diagrams live (bottom third, right side, inset card)

### Recurring motifs

The 3–5 elements that show up across multiple slides and become the silent signature:
- A mascot or icon
- An asterisk, bullet, or glyph
- An evidence-panel framing system
- A pill-button cluster
- A corner monogram

Spec **where** and **how often** each appears. Some show up on every slide. Some only on slide 1 + CTA.

### Header / footer system

The exact text in each corner of every slide. This is the most important consistency lever. Example:

```
top-left:    #NN · SECTION         top-right:   PROJECT / TOTAL
bottom-left: @your.handle           bottom-right: SWIPE →  /  — END —
```

### Forbidden

What this skin should *never* contain. Be specific:
- "no gradients beyond a single tonal step"
- "no Inter, Roboto, or Helvetica"
- "no emoji"
- "no centered ragged-text"
- "no fabricated screenshots"

### Borrow / Do not copy

For each reference in your board, write the borrow / do-not-copy split:

```
Reference 03 (some-creator's carousel):
  Borrow: oversized condensed headline scale, monogram corners, page-number bar
  Do not copy: their handle, their exact phrasing, their logo
```

## Step 4 — Write the image-prompt block

This is the chunk you'll paste into every slide prompt verbatim. Build it last, after every section above is filled. Pattern:

```
STYLE: [name your skin].
Background: [hex] [+ texture/grid spec].
Type: [display family + size + color hex + behavior]; [body family + size + color hex].
Recurring motifs: [comma-separated list with placement rules].
Header/footer metadata in [type spec]: [exact format string].
Format: 3:4, 1080x1440. [margin spec]. High readability.
Mood: [3-word mood descriptor that matches your one-sentence vibe].
```

This block is the locked visual DNA. Once it works on slide 1, **never change it across the rest of the carousel.**

## Step 5 — Test on one carousel before adopting

Run the full skill workflow on one real script using your new skin. Pay attention to:

- Did all 3 anchor variants stay in your visual family, or did one drift?
- Does slide 6 look like it belongs in the same carousel as slide 1?
- Are the corner metadata + motifs consistent across slides?

If something drifts, the spec is too loose. Tighten the image-prompt block — usually by adding more specific motif placement rules or pinning the type family harder.

## Step 6 — Document forbidden patterns

After running 2–3 carousels with the skin, you'll spot patterns the model keeps adding that you don't want. Add them to the `Forbidden` section. The skin gets sharper over time.

## Useful prompts when you're stuck

- "Pick the 3 references on my board that share the strongest typography. Name what they have in common in 2 sentences."
- "What's the *single* visual element on every reference in my board? That's probably the motif you should pull forward."
- "If I had to describe this board to a designer in 6 words, what would I say?"
- "What do all my references *not* have? Add those things to forbidden."

## Result

A `references/style-yourbrand.md` file that any future carousel can lock to. New carousels start by reading this one file and pasting the image-prompt block into every slide prompt — and they all come out looking like the same brand.
