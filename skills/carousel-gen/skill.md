---
name: carousel-gen
description: "Instagram carousel generator. Pure HTML/CSS rendering via Playwright. Tech-editorial design system with warm cream backgrounds, mixed typography, and hand-drawn annotation aesthetic. Reads content briefs, applies hook frameworks, renders publish-ready 1080x1350 slides. Triggers on: /carousel, /plan-carousel, /execute-carousels, /carousel-setup, carousel, create carousel, make carousel, Instagram carousel."
argument-hint: "[topic, brief, or command]"
---

# Carousel Generator

## First-Time Setup Required

Before generating your first carousel, run `/carousel-setup` to configure your brand identity. This creates `brand.json` which controls your handle, colors, fonts, and CTA format across all carousels.

## Commands

| Command | What It Does |
|---------|-------------|
| `/carousel [topic]` | Full pipeline: plan content, render slides, open in Preview |
| `/plan-carousel [topic]` | Content only: write slide plan for review before rendering |
| `/execute-carousels` | Batch render queued carousels |
| `/carousel-setup` | First-time setup: configure brand, colors, fonts, handle |

## Project Paths

- **Project root:** `~/Desktop/AI Projects/carousel-gen/`
- **HTML template:** `templates/greg-style.html`
- **Fonts:** `fonts/`
- **Renderer:** `scripts/render.py`
- **Screenshot tool:** `scripts/screenshot.py`
- **Logo assets:** `assets/logos/`
- **Output:** `output/{slug}/`
- **Brand config:** `brand.json`

---

## /carousel-setup - First-Time Brand Setup

**Run this before generating any carousels.** It creates `brand.json` with your brand identity.

### Questions to ask the user:

**Brand Identity**
1. **What is your Instagram handle?** (e.g., @your.handle)
2. **What is your brand or creator name?**
3. **What niche/industry are you in?** (AI/tech, fitness, business, marketing, design, etc.)

**Visual Style**
4. **Pick your primary accent color:** Red (#E63946), Blue (#2D7DD2), Orange (#FF6B35), Mint (#7FB685), Coral (#E8836B), Lavender (#9B8FE8), or provide a hex code
5. **Pick a secondary accent color:** (for variety across carousels)
6. **What background tone do you prefer?**
   - Cream (#F2F0EB) - warm, editorial (default)
   - Beige (#EDE8DF) - slightly darker, cozy
   - Light gray (#F0F0ED) - cooler, more minimal
   - Blush (#F5EBE8) - warm pink tint

**Typography**
7. **Headline font preference:**
   - Montserrat 800 (bold, geometric - default)
   - Plus Jakarta Sans (modern, clean)
   - Or specify a Google Font name

**Content & CTA**
8. **What's your typical CTA?**
   - Comment keyword for DM (requires ManyChat or similar)
   - Follow for more content
   - Link in bio
   - Save this for later
9. **How actionable should carousels be?**
   - Teaser: enough to understand, need to engage for full guide
   - Full tutorial: someone could follow the steps from the carousel alone
10. **Max slide count preference?** (3-5, 5-8, no limit)

**Asset Sources (optional)**
11. **Do you have existing brand logos/assets?** Point to a folder to copy into `assets/logos/`
12. **Do you have reference carousels you like?** Provide Instagram URLs to capture as style references

### After collecting answers:

1. Create `brand.json` with all settings
2. Run `python3 scripts/setup_fonts.py` to download fonts
3. Generate a test slide to verify the look
4. Show the test slide for approval

### brand.json Schema

```json
{
  "handle": "@your.handle",
  "brand_name": "Your Brand",
  "niche": "your niche",
  "accent_colors": {
    "primary": "#2D7DD2",
    "secondary": "#E63946",
    "tertiary": "#FF6B35"
  },
  "background_tone": "#F2F0EB",
  "typography": {
    "headline": "Montserrat",
    "body": "DM Sans",
    "accent": "Source Serif Pro",
    "code": "JetBrains Mono"
  },
  "cta_format": "comment_keyword",
  "cta_template": "Comment {keyword} below and I'll send it to you.",
  "lead_magnet_platform": "direct_download",
  "max_slides": 5,
  "hook_preference": "curiosity_gap",
  "content_depth": "teaser",
  "auto_open_preview": true
}
```

---

## Architecture: Pure HTML/CSS Rendering

All slides are rendered as complete HTML pages via Playwright at 1080x1350px. No AI-generated visual layers required. This gives pixel-perfect control over typography, layout, screenshots, code blocks, charts, and logos.

**Rendering command:**
```bash
python3 scripts/render.py --config output/{slug}/config.json
```

---

## /carousel [topic] - Full Pipeline

### Step 1: Load Brand Config
Read `brand.json` to get the user's handle, accent colors, fonts, CTA format, and content preferences. If `brand.json` doesn't exist, prompt the user to run `/carousel-setup` first.

### Step 2: Plan Content
If given a topic, research it and structure from scratch.

Every carousel follows a 5-slide narrative arc:

| Slide | Name | Job | Emotional Shift |
|-------|------|-----|-----------------|
| 1 | **DISRUPTION** (Cover) | Break the scroll. Create information gap. | "Wait, what?" |
| 2 | **STAKES** | Why should I care? Connect to a problem I already have. | "This affects ME" |
| 3 | **MECHANISM** | How it actually works. Specific steps, not vague. | "I could do this" |
| 4 | **PROOF** | Evidence it works. Numbers, use cases, results. | "This is real" |
| 5 | **BRIDGE** (CTA) | Convert attention to action. | "I need that" |

### Step 3: Apply Hook Rules
- Anchor on a specific number or claim - never vague
- Split into headline + subheadline - punchline keyword in accent color serif italic
- Each hook works standalone for cold scrollers (Triple Hook Framework)
- Use `*keyword*` markup to highlight the punchline in accent color

### Step 4: Identify Visual Assets
For each slide, determine:
- **Product logos:** Any product mentioned MUST have its real logo. Use `logo_search` MCP or web search. Never use placeholder icons.
- **Screenshots:** Real screenshots via `scripts/screenshot.py`
- **Code blocks:** Real commands from the content

### Step 5: Present Plan (Wait for Approval)
Present the slide-by-slide plan with:
- Hook headline + subheadline for slide 1
- Content summary for each slide
- Visual asset list
- Accent color from brand.json (or ask for override)

Wait for approval before generating.

### Step 6: Capture Assets
```bash
python3 scripts/screenshot.py "URL" -o output/{slug}/assets/screenshot-name.png
```

### Step 7: Build Config + Render
Write `output/{slug}/config.json`, then render:
```bash
python3 scripts/render.py --config output/{slug}/config.json
```

Slides auto-open in Preview (if `auto_open_preview` is true in brand.json).

---

## Config.json Schema

```json
{
  "slug": "my-carousel-topic",
  "handle": "@your.handle",
  "accent_color": "#2D7DD2",
  "slides": [
    {
      "number": 1,
      "cover": true,
      "pre_header": "TOPIC LABEL",
      "headline": "Hook headline with *accent keyword*",
      "headline_size": "54px",
      "body": "Subheadline explaining the hook.",
      "components": []
    },
    {
      "number": 2,
      "label": "STEP LABEL",
      "headline": "Content headline with *accent*",
      "headline_size": "44px",
      "body": "Body text explaining this slide.",
      "components": [
        {"type": "numbered_list", "items": [
          {"title": "Title with *accent keyword*", "desc": "Description."}
        ]},
        {"type": "card_grid", "cards": [
          {"icon": "emoji", "title": "Card Title", "body": "Card body", "style": "colored|dark"}
        ]},
        {"type": "code_block", "title": "Label:", "code": "$ command here"},
        {"type": "screenshot", "path": "assets/screenshot.png"},
        {"type": "bar_chart", "bars": [{"label": "Week 1", "width": "25%", "value": "2,400"}]},
        {"type": "flow", "vertical": true, "steps": [{"text": "Step", "subtitle": "Details"}]},
        {"type": "stats_row", "stats": [{"number": "10K+", "label": "Subscribers"}]},
        {"type": "logo_row", "logos": [{"path": "assets/logos/product.png", "label": "Name"}]},
        {"type": "cta", "keyword": "KEYWORD", "subtitle": "I'll DM you the guide."},
        {"type": "card", "icon": "emoji", "title": "Title", "body": "Body", "style": "dark"},
        {"type": "sticky_note", "text": "Callout text"},
        {"type": "divider"},
        {"type": "spacer", "size": "md"}
      ]
    }
  ]
}
```

### Text Markup
- `*keyword*` - accent color serif italic (punchline highlight)
- `**keyword**` - bold
- `==keyword==` - highlighted background
- `__keyword__` - underline with accent color

---

## Design System Rules

### Typography
- **Headlines:** Montserrat 800 (bold, geometric) - configurable in brand.json
- **Body text:** DM Sans (clean, readable)
- **Accent keywords:** Source Serif Pro Bold Italic in accent color
- **Code blocks:** JetBrains Mono on dark (#1E1E2E) background
- **Labels:** DM Sans 600, uppercase, letter-spaced

### Layout
- **Canvas:** 1080 x 1350px (4:5 Instagram portrait)
- **Background:** Configurable via brand.json (default #F2F0EB off-white with paper grain texture)
- **Content MUST fill 100% of slide vertically.** No blank space below 60% mark.
- **50px top/bottom padding**

### Cover Slides
- Centered layout with pre-header pill + massive headline + subheadline
- Headline takes ~50% of slide height
- Pre-header in bordered pill with accent color

### Content Slides
- Left-aligned with step label at top
- Headline in Montserrat 800 with one accent keyword
- Components fill remaining space

### Color System
- Accent colors configured in brand.json (primary, secondary, tertiary)
- Background: configurable (cream, beige, light gray, blush)
- Text: #1A1A1A (headlines), #333 (body), #555 (secondary), #888 (labels)

### Visual Asset Rules
- **HARD RULE:** When mentioning a specific product, MUST use the real logo. Never placeholders.
- Real screenshots of tools referenced in content
- Product logos stored in `assets/logos/`

---

## Hook Framework Rules

Choose your preferred framework in brand.json or pick per-carousel:

1. **Contrarian / "You're doing it wrong"** - strong for tool/explainer content
2. **Pain Point / Confusion Callout** - relatable problem opening
3. **Proof-First with negative list** - for results content ("didn't write, didn't build")
4. **"Most people don't know" softener** - gentler curiosity gap
5. **Curiosity Gap** - "X things I wish I knew about [topic]"
6. **Split headline + subheadline** - punchline in accent color, explanation below

Every hook anchors on a specific number or claim. Never vague.

---

## Content Flow Rules

1. Slide 2 ALWAYS leads with pain before showing the solution
2. Specific > General - use concrete numbers, not vague claims
3. Real example prompts in quotes as body text
4. Each slide ends with unresolved tension that makes the next slide necessary
5. CTA references the value prop clearly

---

## Hard Rules (Never Break These)

1. Content MUST fill 100% of slide vertically. No dead white space.
2. When mentioning a product, MUST use the real logo. Never placeholders.
3. Handle comes from brand.json. Always include it in the footer.
4. No em dashes. Use commas, periods, or hyphens.
5. Max slide count from brand.json (default 5, max 8).
6. Info box titles: 35px bold, one accent keyword, body text below.
7. Cover slides: centered, headline ~50% of slide, pre-header pill above.
8. Every numbered list title gets one `*accent keyword*` highlight.
9. Delete previous slide versions before rendering new ones.
10. Auto-open slides in Preview after rendering (if brand.json allows).

---

## /plan-carousel [topic] - Content Only

Run Steps 1-5 from /carousel (load brand, plan content, apply hooks, identify assets, present plan).
No rendering. For review only.

## /execute-carousels - Batch Render

Process all config.json files in output/ that haven't been rendered yet. Render each one and open slides.
