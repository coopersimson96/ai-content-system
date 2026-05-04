# Build Your Own Style Guide

How to deconstruct a creator's reel format into a reusable archetype. Use this when none of the three shipped archetypes (`sage-stack`, `editorial-magazine`, `screen-face-split`) fit your script's vibe.

The goal is not one-to-one recreation - it's extracting the **visual DNA** so you can apply the same discipline to your own scripts without copying any single source.

---

## 1. Pick a creator whose aesthetic you want to study

Watch through their last 10-20 reels. Look for:

- A consistent visual format that survives across multiple posts
- 3-5 reels that share the same grammar (top-half mode rotation, caption treatment, transition style)
- Something distinctive enough that a viewer would say "that's a [creator] video" within 2 seconds

If a creator's aesthetic varies post-to-post, pick a different creator. Inconsistency means there's no archetype to extract.

**Minimum sample:** 3-5 reels in the same format. Less than 3 and you can't tell what's the format vs. what's a one-off creative choice.

---

## 2. Download reference reels

Use `yt-dlp` (or any platform-specific downloader) to save the reference reels:

```bash
mkdir -p style-guides/<your-archetype-slug>/sources/<reel-id>
yt-dlp -o "style-guides/<your-archetype-slug>/sources/<reel-id>/source.%(ext)s" \
  "https://www.instagram.com/reel/<reel-id>/"
```

Save each reel under its own `sources/<reel-id>/` folder. Don't commit `source.mp4` files unless you have rights to the source - keep them gitignored if redistributing the deconstruction.

---

## 3. Extract frames

Pull frames every 0.5s into a `frames/` directory so you can see the structure at a glance:

```bash
cd style-guides/<your-archetype-slug>/sources/<reel-id>
mkdir frames
ffmpeg -i source.mp4 -vf "fps=2,scale=540:960" -q:v 2 frames/dense_%03d.jpg
```

Or pull 5 percentile frames (start, 25%, mid, 75%, end) for a quick overview:

```bash
DUR=$(ffprobe -v 0 -show_entries format=duration -of csv=p=0 source.mp4)
for pct in 5 25 50 75 95; do
  T=$(echo "$DUR * $pct / 100" | bc -l)
  ffmpeg -ss $T -i source.mp4 -frames:v 1 -q:v 2 "frames/p${pct}.jpg"
done
```

---

## 4. Identify recurring patterns

Open the frames in a grid view (Finder column view, or any image grid tool). Walk through them looking for what repeats.

Categories to label per beat:

- **Hook treatment** — how does the video open? Bold headline card? Object metaphor? Speaker first?
- **Body sections** — how is the script divided visually? Hard cuts? Numbered list? Magazine spreads?
- **Transitions** — whip-blurs? Crossfades? Hard cuts? Black-bezel breaths?
- **Typography** — how many type voices? Serif or sans? All-caps captions or italic-serif?
- **Color** — what's the dominant palette? Where does the accent color appear?
- **Sound design** — music bed? Pad? Pure VO?
- **Audience cues** — what does the speaker look like (chest-up, mic visible, naturally graded)? What's the CTA pattern (comment X, sign up, follow)?

Write notes inline as you go. The goal is to spot patterns that appear in 3+ of your reference reels - those are the archetype's load-bearing elements.

---

## 5. Write `STYLE_DECON.md`

Use the same 10-section structure as the shipped archetypes:

```
# <Archetype Name> Motion Style — Deconstruction

> Reference reels: [URLs and lengths]
> Format: 9:16 vertical, [resolution], [fps], [length range]
> Genre: [what kind of content this serves]
> Working alias: [memorable name]

## 0 · The 10 Laws (memorize)
1. [Most distinctive move]
2. [Second-most distinctive move]
... 10 total

## 1 · The Reference Timeline
[beat-by-beat table from one of your reference reels]

## 2 · The Visual Vocabulary
### 2.1 Backgrounds
### 2.2 Type System
### 2.3 Color Story
### 2.4 Motion Vocabulary
### 2.5 Transition Catalog

## 3 · Signature Element Recipes
[copy-paste-able CSS/HTML for the 2-3 highest-leverage elements]

## 4 · Motion Patterns
### 4.1 Transition library
### 4.2 Easing rules
### 4.3 The most-used transition recipe

## 5 · The Speaker Treatment
[grading, framing, why it matters]

## 6 · Repeatable Beat Grammar
[the N-beat atom you can clone]

## 7 · Hyperframes Implementation Recipes
[composition shell, section header, signature element]

## 8 · Brand Adaptation
[how to apply your BRAND.md, what overrides the archetype demands]

## 9 · Pre-flight Checklist
[10-15 binary checks before claiming a video matches this style]

## 10 · Open Questions
[things you'll need more reference data to confirm]
```

Keep the file long enough to be useful, short enough that you'd actually re-read it before starting a new build. The shipped archetypes run 400-700 lines.

---

## 6. Encode patterns into `patterns.json`

The `patterns.json` file is a machine-readable library that the motion-plan flow uses to match script beats to visual patterns. Schema:

```json
{
  "archetype_id": "your-archetype-slug",
  "version": "0.1.0",
  "version_date": "YYYY-MM-DD",
  "description": "One paragraph essence",
  "duration_range_s": [30, 90],
  "brand_spec": "../BRAND.md",
  "style_decon": "./STYLE_DECON.md",
  "fits_script_when": [
    "criterion 1",
    "criterion 2"
  ],
  "does_not_fit_when": [
    "criterion 1",
    "criterion 2"
  ],
  "default_fallback_pattern_id": "caption-only-default",
  "patterns": [
    {
      "id": "kebab-case-pattern-id",
      "name": "Human-readable pattern name",
      "description": "1-3 lines on what the pattern does",
      "scene_type": "hook | list-preview | section-header | tool-reveal | concept-demo | list-item | claim | proof | transition | cta | closer | caption-only",
      "unique_per_video": false,
      "duration_s": [min, max],
      "position": {
        "constraint": "anywhere | first-N-seconds | last-N-seconds | after-pattern",
        "value": "optional N seconds or pattern_id"
      },
      "trigger": {
        "script_signal": "human-language criterion the LLM evaluates",
        "regex_hint": "optional regex for transcript pre-filter"
      },
      "brand_tokens": ["--token-1", "--token-2"],
      "hyperframes": {
        "blocks": ["registry-block-slugs"],
        "html_template": "templates/your-pattern.html",
        "css_template": "templates/your-pattern.css",
        "js_template": "templates/your-pattern.js"
      },
      "params": {
        "param_name": {
          "type": "string | number | boolean | color-token | url | asset-path",
          "default": "optional",
          "description": "what this param controls",
          "required": true
        }
      },
      "examples": [
        {
          "reel": "<reel-id>",
          "timestamp": "X.X-Y.Ys",
          "note": "why this is a good example"
        }
      ]
    }
  ],
  "open_questions": [
    "things you'll resolve in v0.2"
  ]
}
```

Each pattern is one reusable visual move. Aim for 8-15 patterns total - enough to cover the archetype's full range without becoming unwieldy.

The shipped archetypes' `patterns.json` files (`sage-stack/patterns.json`, etc.) are good references. Read at least one before writing yours.

---

## 7. Test by building a short composition

Pick a script and consciously borrow 3+ patterns from your new guide. Build it as a video using the standard pipeline:

1. Record your script
2. Trim with `video-use`
3. Transcribe
4. Plan beats in `MOTION_PLAN.md` using YOUR new archetype's patterns
5. Build `index.html` from the patterns
6. Lint, preview, render

If the result feels at home next to your reference reels, the archetype is real. If it feels off, your patterns aren't capturing what makes the format work - go back to step 4 and watch the reference reels again.

---

## 8. Iterate after seeing renders

After your first render, walk through:

- Which patterns landed? Bump their version, add params if needed.
- Which patterns flopped? Either fix the recipe or retire the pattern.
- What's missing? If a beat fell back to `caption-only` because nothing matched, that's a pattern gap - add a new pattern entry to cover it.

Bump `version` in `patterns.json` and update `version_date` whenever you add, retire, or substantially edit a pattern.

After 5-10 videos in the new archetype, you'll have enough signal to know whether it's a real archetype worth keeping or a one-off creative choice that doesn't generalize.

---

## Tips

- **Don't write JSON by hand for every pattern.** A small Python or Node script can scaffold a new pattern entry from a template, leaving you to fill in the description, trigger, and params.
- **Cross-reference between archetypes.** If your new archetype's transition library reuses sage-stack's whip-blur, point at it via `"blocks": ["whip-pan"]` and link to sage-stack's recipe in your STYLE_DECON.
- **Resist over-fitting.** A pattern that fires once across all your reference reels probably isn't a pattern - it's a one-time creative choice. Wait for a second example before promoting it.
- **Open questions are honest.** The shipped archetypes all have an "Open Questions" section listing things that need more reference data. Yours should too.
