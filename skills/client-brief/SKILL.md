---
name: client-brief
description: Generate a 2-page interactive client proposal (brief + work plan) with SVG diagrams, accordion deliverables, architecture maps, ROI charts, and Vercel deployment.
argument-hint: "brief for [client name]" or "[client] content automation proposal"
context: conversation
---

# Client Brief Generator

Generate a polished, interactive 2-page client proposal deployed to Vercel. Each brief consists of a high-level pitch page (`index.html`) and a detailed work plan/proposal page (`workplan.html`).

## What It Does

Turn a discovery call transcript or project notes into a professional, interactive web-based proposal. No design tools needed. No PDF formatting headaches. Just run the skill and get a live URL you can send to clients.

Each brief includes:
- **Pitch page** (index.html) - Problem analysis, solution architecture, feature pipeline, ROI projections, implementation timeline
- **Work plan** (workplan.html) - Detailed deliverables with accordion cards, SVG diagrams per deliverable, architecture map, investment CTA

Every section has scroll-triggered animations, interactive SVG diagrams, and mobile-responsive layouts. Deployed to Vercel with noindex headers so it stays private.

---

## Setup

### Requirements
- Claude Code installed
- Vercel CLI (`npm i -g vercel`) for deployment
- Git installed

### Installation

```bash
# Clone to your Claude Code skills directory
cp -r client-brief ~/.claude/skills/client-brief
```

No API keys needed. The skill generates static HTML files that work by opening directly in a browser.

---

## Usage

### Quick Start

```
/client-brief "Acme Corp content automation proposal"
```

Or provide more context:

```
/client-brief
```
Then paste your discovery call transcript, project notes, or describe the project.

### What You'll Be Asked For

| Input | Required | Example |
|-------|----------|---------|
| Client/business name | Yes | Acme Corp |
| Client contact name | Yes | Jane Smith |
| Logo URL | No | CDN URL or skip |
| Business type & industry | Yes | SaaS, B2B marketing |
| What you're building | Yes | Content automation system |
| Target platforms | Yes | Instagram, TikTok, YouTube |
| Deliverables list | Yes | Title + 1-sentence summary each |
| Investment amount | Yes | $4,500 |
| Prepared by name + email | Yes | Your Name, you@email.com |
| Rollout phases | Yes | Count + brief description each |
| What client's team provides | Yes | Access, assets, brand guidelines |
| Future phase / upsell features | No | Premium add-ons |

If you provide a transcript or detailed notes, the skill extracts these automatically and confirms before generating.

---

## Configuration

### Theme Customization

The default color palette uses a clean, professional theme:

```javascript
// In the generated HTML's tailwind.config
colors: {
  cream: '#FAF9F6',        // Background
  charcoal: '#2D2D2D',     // Dark sections & text
  teal: '#2A9D8F',         // Primary accent
  copper: '#B87333',       // Secondary accent
}
```

To customize for your brand, edit these values in the `tailwind.config` block inside each generated HTML file. The skill uses Tailwind CDN, so any Tailwind color utility works.

### Font

Default: Inter (Google Fonts CDN). Change by editing the `<link>` tag and `fontFamily` in the tailwind config.

---

## Output Structure

```
~/Desktop/AI Projects/{kebab-client-name}-brief/
├── index.html      # High-level pitch page
├── workplan.html   # Detailed proposal with deliverables
└── vercel.json     # noindex deployment config
```

### Pitch Page (index.html) Sections

1. **Sticky nav** - Section links with active state tracking
2. **Hero** - Dark background, animated badge, stat cards, dual CTAs
3. **Problem: Time Audit** - Horizontal bar charts showing current time breakdown with automation priority badges
4. **Solution: Architecture** - 3-layer SVG diagram (dashboard, backend, data)
5. **Features: Content Pipeline** - Pipeline flow SVG + feature cards with time-saved badges
6. **ROI: Time Savings** - Before/after comparison + animated donut chart
7. **Phases: Implementation** - Vertical timeline with phase cards
8. **Deployment Steps** - 5-column numbered steps
9. **Footer** - Contact email

### Work Plan Page (workplan.html) Sections

1. **Logo banner** - Client logo (skipped if no URL)
2. **Hero** - Project info grid (prepared for/by, date, investment, scope)
3. **Deliverables** - Interactive accordion cards (one open at a time), each with inline SVG diagram
4. **Dashboard Preview** - 3 SVG wireframes showing the product in practice
5. **System Architecture** - Interactive node diagram with hover/tap tooltips
6. **Future Phase** - Dimmed expansion features
7. **Rollout Timeline** - Phase pills with descriptions
8. **What Your Team Provides** - Clean bullet list
9. **How We Work Together** - Communication and revision process
10. **Investment CTA** - Large card with amount and included items
11. **Footer** - Contact info

---

## Interactive Features

### Accordion Deliverables
Each deliverable is a clickable card that expands to show:
- Plain-language description of what it does and why it matters
- Inline SVG diagram specific to that deliverable
- "What's included" or "How it works" bullet list
- Optional callout box and wireframe preview

Only one card opens at a time to keep the page scannable.

### SVG Diagram Types
The skill selects the right diagram type per deliverable:

| Deliverable Type | Diagram Style |
|-----------------|---------------|
| Pipeline/process | Horizontal flow: boxes and arrows |
| UI feature | Wireframe card: content layouts, forms |
| Data sync/integration | Bidirectional arrows between systems |
| Analytics/reporting | Chart wireframe: bars, metrics, tabs |
| Content generation | Carousel/slide wireframes |
| Architecture/infra | Node map with connections |

### Scroll Animations
Every section uses IntersectionObserver for fade-up animations. Bar charts and donut charts animate on scroll entry.

### Architecture Tooltips
Desktop: hover to highlight connection lines and show tooltips. Mobile: tap to toggle.

---

## Deployment

The skill automatically:
1. Initializes a git repo in the project directory
2. Deploys to Vercel with `--prod --yes`
3. Returns live URLs for both pages

The `vercel.json` adds `X-Robots-Tag: noindex, nofollow` headers so client briefs stay private and out of search results.

---

## Design Rules

1. **No build step** - Tailwind CDN + vanilla JS only. Files work by opening in a browser.
2. **Mobile-first** - Every SVG uses `viewBox`, every layout stacks on mobile, touch targets are 44px minimum.
3. **Every deliverable gets an SVG diagram** - No exceptions. Visually explains how the feature works.
4. **Non-technical language** - The client is not a developer. No code references or tech jargon (unless the client is technical).
5. **noindex/nofollow** - Client briefs never appear in search results.
6. **Concrete numbers over vague claims** - "saves 16 hours/week" not "saves significant time."

---

## Tips

- **From a transcript**: Paste the full discovery call transcript. The skill extracts client needs, pain points, and project scope automatically.
- **Quick iteration**: Edit the generated HTML directly and refresh the browser. No build step needed.
- **Custom branding**: Swap the color palette in the tailwind config to match your agency's brand.
- **Multiple revisions**: Re-run the skill with updated inputs. It creates a fresh set of files each time.
- **Without Vercel**: The HTML files work locally. Just open in a browser and share via any static hosting.
