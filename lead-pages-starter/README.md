# Lead Pages Starter

A ready-to-deploy landing page system for lead capture. Built with Astro + Tailwind + Vercel. Captures leads to Notion.

## How It Works

1. Add a `.md` file to `src/content/resources/` with your guide/cheatsheet details
2. Push to GitHub — Vercel auto-deploys
3. Visitors enter name + email → lead saved to Notion → PDF revealed

## Quick Start

### 1. Fork or copy this directory to a new GitHub repo

```bash
cp -r ~/ai-content-system/lead-pages-starter ~/my-lead-pages
cd ~/my-lead-pages
git init && git add -A && git commit -m "Initial commit"
```

### 2. Push to GitHub

```bash
gh repo create my-lead-pages --private --push --source=.
```

### 3. Connect to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repo
3. Framework: Astro (auto-detected)
4. Add environment variables:
   - `NOTION_API_KEY` — your Notion integration token
   - `NOTION_LEADS_DB_ID` — your Notion leads database ID
5. Deploy

### 4. Create Notion Leads Database

Create a database in Notion with these properties:
- **Name** (title)
- **Email** (email)
- **Resource** (select)

### 5. Add Resources

Create `.md` files in `src/content/resources/`:

```markdown
---
title: "Your Guide Title"
headline: "Compelling Headline"
subtitle: "What the reader gets"
pdfUrl: "https://drive.google.com/your-pdf-link"
valueProps:
  - "Value prop 1"
  - "Value prop 2"
  - "Value prop 3"
ctaText: "Get the Free Guide"
previewDescription: "One sentence summary"
pages: 3
type: "guide"
---

## What's Inside

Your sales copy here...
```

Push to trigger a deploy. Your page will be live at `your-domain.vercel.app/your-guide-title`.

## Customization

- **Colors:** Edit `tailwind.config.mjs` — change the `accent` color to match your brand
- **Footer:** Edit `src/layouts/ResourceLayout.astro`
- **Form fields:** Edit the layout to add/remove form fields

## Without Notion

The lead capture endpoint gracefully handles missing Notion config — it still shows the resource. You can use this without Notion and add it later.
