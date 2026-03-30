# Carousel Generator

Instagram carousel generator that produces publish-ready 1080x1350 slides from plain text descriptions. Pure HTML/CSS rendering via Playwright - no design tools needed.

## What It Does

You describe what your carousel should say. Claude Code builds the slide config, renders pixel-perfect PNGs, and opens them in Preview. Every slide uses your brand colors, fonts, and handle automatically.

The design system is a tech-editorial aesthetic: warm cream backgrounds, paper grain texture, mixed typography (bold sans-serif headlines + serif italic accents), and professional component layouts (code blocks, card grids, bar charts, logo rows, numbered lists).

## Quick Start

### 1. Install dependencies

```bash
# Playwright (required for rendering)
pip3 install playwright
playwright install chromium

# Pillow (only needed if using visual + text composite mode)
pip3 install Pillow
```

### 2. Download fonts

```bash
cd ~/Desktop/AI\ Projects/carousel-gen
python3 scripts/setup_fonts.py
```

This downloads Montserrat, DM Sans, Source Serif Pro, JetBrains Mono, Inter, and Playfair Display from Google Fonts into the `fonts/` directory.

### 3. Set up your brand

Run `/carousel-setup` in Claude Code. It asks you a series of questions about your brand and creates `brand.json`. Or copy the example and fill it in manually:

```bash
cp brand.json.example brand.json
```

Then edit `brand.json` with your details:

```json
{
  "handle": "@your.handle",
  "brand_name": "Your Brand Name",
  "niche": "your industry or content niche",
  "accent_colors": {
    "primary": "#2D7DD2",
    "secondary": "#E63946"
  },
  "background_tone": "#F2F0EB",
  "cta_format": "comment_keyword",
  "max_slides": 5
}
```

### 4. Create your first carousel

```
/carousel 5 time management tips for remote workers
```

Claude Code will:
1. Read your brand.json for handle, colors, and preferences
2. Plan a 5-slide carousel with the DISRUPTION > STAKES > MECHANISM > PROOF > BRIDGE arc
3. Show you the plan and wait for your approval
4. Render all slides as PNGs
5. Open them in Preview

## Brand Configuration Reference

Every field in `brand.json` explained:

| Field | What It Controls | Example |
|-------|-----------------|---------|
| `handle` | Your @ shown in slide footer | `@your.handle` |
| `brand_name` | Used in CTA slides and captions | `Your Brand` |
| `niche` | Helps Claude pick relevant hooks and examples | `AI tools` |
| `accent_colors.primary` | Main highlight color for keywords, borders, charts | `#2D7DD2` |
| `accent_colors.secondary` | Alternate color for variety across carousels | `#E63946` |
| `background_tone` | Slide background color | `#F2F0EB` |
| `typography.headline` | Headline font family | `Montserrat` |
| `typography.body` | Body text font family | `DM Sans` |
| `cta_format` | How your CTA slide works | `comment_keyword` |
| `cta_template` | CTA text with {keyword} placeholder | `Comment {keyword} below` |
| `max_slides` | Default slide count (3-8) | `5` |
| `hook_preference` | Default hook framework | `curiosity_gap` |
| `content_depth` | Teaser (need full guide) or full tutorial | `teaser` |
| `auto_open_preview` | Open rendered slides in Preview automatically | `true` |

### Accent Color Options

Pick colors that match your brand. Some tested combinations:

- **Blue** (#2D7DD2) - trustworthy, tech, professional
- **Red** (#E63946) - urgent, bold, attention-grabbing
- **Orange** (#FF6B35) - energetic, creative, warm
- **Mint** (#7FB685) - calm, growth, wellness
- **Coral** (#E8836B) - friendly, approachable, lifestyle
- **Lavender** (#9B8FE8) - creative, premium, unique
- **Amber** (#E8B86B) - warm, luxury, business

### Background Tone Options

- **Cream** (#F2F0EB) - warm editorial, default
- **Beige** (#EDE8DF) - slightly darker, cozy
- **Light gray** (#F0F0ED) - cooler, more minimal
- **Blush** (#F5EBE8) - warm pink tint

### CTA Format Options

- `comment_keyword` - "Comment KEYWORD below" (requires ManyChat or similar)
- `follow` - "Follow @handle for more"
- `link_in_bio` - "Link in bio for the full guide"
- `save` - "Save this for when you need it"
- `custom` - Uses your `cta_template` string exactly

### Hook Preference Options

- `contrarian` - "You're doing it wrong" frame
- `pain_point` - Lead with the problem
- `curiosity_gap` - "Most people don't know" softener
- `proof_first` - "I did X in Y timeframe"
- `news` - "[Tool] just changed everything"

## Component Types

These are the building blocks available in config.json slides:

- **numbered_list** - Ordered items with title + description, accent number badges
- **card_grid** - 2-3 column grid of cards (white, colored accent border, or dark)
- **card** - Single standalone card
- **code_block** - Dark terminal block with syntax coloring
- **screenshot** - Image container with border and shadow
- **bar_chart** - Horizontal bar chart with labels and values
- **flow** - Step diagram (horizontal or vertical) with arrows
- **stats_row** - Big number callouts with labels
- **logo_row** - Product logos with labels
- **sticky_note** - Yellow callout note
- **cta** - Call-to-action with keyword box
- **divider** - Horizontal line
- **spacer** - Vertical spacing (sm/md/lg)

## File Structure

```
carousel-gen/
  brand.json              # Your brand config (created by /carousel-setup)
  brand.json.example      # Template to copy
  skill.md                # Skill definition for Claude Code
  DESIGN-SYSTEM.md        # Visual layer art direction guide
  CAROUSEL-GUIDE.md       # Content strategy and hook frameworks
  README.md               # This file
  templates/
    greg-style.html       # Main rendering template
    text-overlay.html     # Text-only overlay template (for composite mode)
  scripts/
    render.py             # Main renderer (config.json -> PNG slides)
    composite.py          # Visual + text layer compositor
    screenshot.py         # URL screenshot capture tool
    setup_fonts.py        # Font downloader
    capture_carousels.py  # Instagram reference capture tool
  presets/
    tech-editorial.json   # Visual preset for Nano Banana prompts
  fonts/                  # Downloaded Google Fonts (created by setup_fonts.py)
  assets/logos/           # Product logos for logo_row components
  references/             # Style reference screenshots
  examples/
    example-config.json   # Example carousel config
  output/                 # Generated carousels (one folder per carousel)
```

## Rendering Modes

### Mode 1: Pure HTML/CSS (Default)

Uses `render.py` with `greg-style.html` template. All visual elements (cards, charts, code blocks, logos) are rendered directly in HTML/CSS. Best for most carousels.

```bash
python3 scripts/render.py --config output/my-carousel/config.json
```

### Mode 2: Visual + Text Composite

Uses Nano Banana MCP to generate artistic visual layers, then overlays text via `composite.py`. Best for cover slides or when you want hand-drawn annotation aesthetics.

```bash
python3 scripts/composite.py --config output/my-carousel/config.json
```

Requires visual PNGs in `output/{slug}/visuals/visual-01.png` etc.

## Adding Product Logos

When your carousel mentions a specific product, use the real logo:

1. Search for the logo via `logo_search` MCP or download from the product's press kit
2. Save to `assets/logos/product-name.png` (or .svg)
3. Reference in config.json: `{"type": "logo_row", "logos": [{"path": "assets/logos/product-name.png", "label": "Product"}]}`

## Capturing Style References

Find Instagram carousels you like and capture them as design references:

```bash
python3 scripts/capture_carousels.py https://www.instagram.com/p/ABC123/ https://www.instagram.com/p/DEF456/
```

Screenshots save to `references/` and can be used as visual direction input for Nano Banana.
