---
name: hand-raiser
description: Generate a hand raiser PDF lead magnet (1-5 pages) for any script or standalone topic. Renders a professional guide/cheatsheet/checklist, uploads to Google Drive, and links in Notion.
argument-hint: "SF #3" or "Claude Code setup guide" or "AI scheduling cheatsheet"
context: conversation
---

# Hand Raiser PDF Generator

Create professional 1-5 page PDF lead magnets — guides, cheatsheets, checklists, quick-references, or how-to guides. Every script produced gets a matching hand raiser. This is part of the production pipeline, not optional.

---

## Step 1: Parse Input

Extract from `$ARGUMENTS`:

1. **SCRIPT_REF** — A script reference like "SF #3", "#3", "script 3" → fetch from Notion
2. **STANDALONE_TOPIC** — A freeform topic like "Claude Code setup guide" → no Notion fetch needed
3. **PDF_TYPE** (optional) — One of: `setup-guide`, `cheatsheet`, `quick-reference`, `how-to-guide`, `checklist`. If not specified, auto-detect in Step 3.

If input is ambiguous, default to treating it as a script reference if it contains a number.

---

## Step 2: Fetch Script Context (if script ref)

If SCRIPT_REF is provided, query the Script Library:

1. Read `~/.config/notion-content/config.json` to get `script_library_db_id`
2. Use `notion-search` with `data_source_url` set to `collection://{script_library_db_id}` to find the script by number or title
3. Extract:
   - **Title** — Script title
   - **Topic** — Content topic
   - **CTA** — The "Comment [WORD]" CTA from the script caption
   - **Pain Point** — The core problem the script solves
   - **Google Doc URL** — Link to the full script for reference
4. If the script has a Google Doc URL, read the doc content to understand the full script for context

If STANDALONE_TOPIC, skip this step — use the topic directly.

---

## Step 3: Auto-Detect PDF Type

Based on the content, select the best PDF type:

| Content Signal | PDF Type | When |
|---|---|---|
| Setup/install/config steps | `setup-guide` | Script shows how to set up or install something |
| Quick tips, shortcuts, commands | `cheatsheet` | Script covers multiple quick tips or a tool's commands |
| Reference data, benchmarks, specs | `quick-reference` | Script references data the viewer would want to save |
| Step-by-step tutorial | `how-to-guide` | Script walks through a process |
| Audit, evaluation, requirements | `checklist` | Script involves checking/evaluating things |

**Default:** `how-to-guide` if unclear.

Tell the user what type was selected and why (one line).

---

## Step 4: Generate Content JSON

Create structured JSON content for the PDF. The JSON format is documented in `~/ai-content-system/scripts/pdf_generator.py`.

### Content Guidelines by Type

**setup-guide** (1-5 pages):
- Cover page with title + "What You'll Learn" bullets
- Prerequisites section
- Numbered steps with code blocks where relevant
- Tip boxes for common gotchas
- Resources section at the end

**cheatsheet** (1-3 pages):
- Cover page with title + quick summary
- Tables for commands/shortcuts/formulas
- Two-column layouts for quick scanning
- Tip boxes for pro tips
- Keep dense — max info per page

**quick-reference** (1-3 pages):
- Cover page with title
- Tables with benchmarks/data/specs
- Callout boxes for key thresholds
- Organized by category

**how-to-guide** (2-5 pages):
- Cover page with "What You'll Learn" bullets
- Numbered steps with descriptions
- Code blocks or screen instructions where relevant
- Tip boxes between sections
- Resources at the end

**checklist** (1-3 pages):
- Cover page with title + context
- Checklist items grouped by category
- Tip boxes for important notes
- Keep actionable — each item is a clear yes/no

### Content Rules
- **Ground in the script's content.** The PDF should deliver the value promised by the script's CTA.
- **No fluff.** Every section earns its space. If a page doesn't add value, cut it.
- **Actionable over informational.** The reader should be able to DO something with every page.
- **Include the script's CTA context.** If the script says "Comment GUIDE", the PDF should feel like the guide that was promised.
- **5 pages MAX.** Enforced by the PDF generator, but aim for the right length — a cheatsheet should be 1-2 pages, not 5.

### JSON Structure

Write the content as a JSON object and save to a temp file:

```json
{
    "type": "{pdf_type}",
    "title": "{Title}",
    "subtitle": "{Subtitle}",
    "subtitle_bullets": ["Bullet 1", "Bullet 2", "Bullet 3"],
    "footer_text": "Your Footer Text | 2026",
    "sections": [
        {"type": "section_title", "number": "01", "title": "Section Name"},
        {"type": "body", "text": "Paragraph text."},
        {"type": "bullets", "items": ["Item 1", "Item 2"]},
        {"type": "tip_box", "title": "Pro Tip", "text": "Tip text."},
        ...
    ]
}
```

Save to: `~/ai-content-system/output/hand-raisers/content-sf{N}.json`

For standalone topics: `~/ai-content-system/output/hand-raisers/content-{kebab-title}.json`

---

## Step 5: Render PDF

Run the PDF generator:

```bash
cd ~/ai-content-system/scripts && python3 pdf_generator.py --content-file "{CONTENT_JSON_PATH}" --output "{OUTPUT_PATH}"
```

**Output path:** `~/ai-content-system/output/hand-raisers/SF{N}-{kebab-title}.pdf`
- If script ref: `SF{N}-{kebab-title}.pdf` (e.g., `SF3-ai-scheduling-setup-guide.pdf`)
- If standalone: `{kebab-title}.pdf` (e.g., `claude-code-setup-guide.pdf`)

Verify the PDF was created and report page count.

---

## Step 6: Upload to Google Drive

```bash
cd ~/ai-content-system/scripts && python3 gdrive_upload.py --file "{PDF_PATH}" --subfolder "Hand Raisers"
```

Capture the shareable URL from stdout.

If upload fails (credentials issue, network error), still report the local PDF path and tell the user to upload manually.

---

## Step 7: Create Vercel Landing Page

Create a lead-capture landing page for the hand raiser at `~/ai-content-system/lead-pages/src/content/resources/{kebab-title}.md`.

### Frontmatter Schema

**Source of truth:** `~/ai-content-system/lead-pages/src/content.config.ts` — if in doubt, read this file to confirm required fields.

```yaml
title: "{Title}"
headline: "{Compelling headline matching the CTA promise}"
subtitle: "{1-2 sentence description of what the PDF delivers}"
pdfUrl: "{Google Drive URL from Step 6}"
valueProps:
  - "{Value prop 1 from the PDF content}"
  - "{Value prop 2}"
  - "{Value prop 3}"
  - "{Value prop 4 - include a real stat/number}"
ctaText: "Get the Free Guide"
previewDescription: "{1 sentence summary for meta/preview}"
pages: {page count}
type: "{one of: guide, cheatsheet, checklist, quick-reference, how-to-guide}"
```

### Body Content

After frontmatter, write 2-4 paragraphs:
- "What's Inside" section with bold key takeaways
- "Who this is for" section targeting the script's audience
- Ground everything in the script's pain point and CTA promise

### Pre-Deploy Build Check (REQUIRED)

Before committing, **always** run the Astro build to catch schema errors:

```bash
cd ~/ai-content-system/lead-pages && npx astro build 2>&1 | tail -20
```

If the build fails with `InvalidContentEntryDataError`, the frontmatter is missing required fields. Fix the `.md` file before proceeding.

**Do NOT commit and push a page that fails the build.** A broken build means Vercel won't deploy, and ALL landing pages stop working until it's fixed.

### Deploy

```bash
cd ~/ai-content-system/lead-pages && git add "src/content/resources/{kebab-title}.md" && git commit -m "Add {title} landing page (SF #{N})" && git push origin master
```

The live URL is: `https://YOUR_VERCEL_DOMAIN/{kebab-title}`

**Graceful failure:** If git push fails (network, auth), still report the local file path and the expected URL — the user can push manually.

---

## Step 8: Update Notion (if script ref)

If this hand raiser is for a Script Library entry:

1. Use `notion-update-page` to set **"Hand Raiser URL"** (Drive URL from Step 6) and **"Hand Raiser Page"** (Vercel URL from Step 7) on the script's Notion page
2. Both are URL type properties on the Script Library

**Graceful failure:** If either property doesn't exist, skip gracefully — still deliver all other outputs.

If standalone (no script ref), skip this step.

---

## Step 9: Report

Output a summary:

```
Hand Raiser Generated:
- Type: {pdf_type}
- Pages: {page_count}
- Local: {local_path}
- Drive: {drive_url}
- Landing Page: https://YOUR_VERCEL_DOMAIN/{kebab-title}
- Notion: {Updated / Skipped (standalone) / Property missing}
- CTA: "Comment {WORD} and I'll send you this {pdf_type}!"
```

The CTA line gives the user ready-to-use caption text for their video.

---

## Batch Mode

When called in a loop (e.g., from content-scripting's auto-push pipeline), accept multiple scripts efficiently:

1. Generate all content JSONs first
2. Render all PDFs
3. Upload all to Drive
4. Create all Vercel landing pages (one commit with all files, single push)
5. Update all Notion entries (Hand Raiser URL + Hand Raiser Page)
6. Report all links in a single summary table

This avoids repeated credential loading and API setup.

---

## Error Handling

- **fpdf2 not installed:** `pip3 install fpdf2` and retry
- **Google auth expired:** Credentials auto-refresh from token.json
- **Notion property missing:** Report gracefully, still deliver PDF + Drive link
- **Content too long:** PDF generator enforces 5-page max; warn if content was truncated
- **Missing script in Notion:** Tell user the script wasn't found, offer to create as standalone
