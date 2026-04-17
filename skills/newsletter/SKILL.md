---
name: newsletter
description: Generate newsletter email drafts from script content. Adaptive format selection (lesson, tool, essay, insight, tips, comparison) based on content type. Pushes drafts to your email platform and links back to your script library.
argument-hint: "SF #18" or "newsletter from my last script" or paste content inline
context: conversation
---

# Newsletter Email Generator

Converts short-form video scripts into newsletter emails using adaptive format selection. Reads script content, picks the best email template, generates HTML, and pushes to your email platform as a draft.

**Primary platform: Beehiiv.** This skill is built around Beehiiv because its free plan and API flexibility fit most creators starting out. **It works with other platforms too** (Mailchimp, ConvertKit/Kit, Substack, Brevo) with minor rewiring - see "Platform Flexibility" below.

---

## Setup Check

On every invocation:

1. Verify platform credentials: check `~/Desktop/AI Projects/newsletter/.env` has the expected keys (e.g. `BEEHIIV_API_KEY` and `BEEHIIV_PUBLICATION_ID` for Beehiiv, or the equivalent for your platform)
2. Verify modules exist: `~/Desktop/AI Projects/newsletter/beehiiv_api.py` (or your platform's equivalent) and `~/Desktop/AI Projects/newsletter/email_html.py`
3. Read your script library config (e.g., `~/.config/notion-content/config.json`) if you're pulling scripts from Notion
4. If anything is missing, tell the user and stop.

---

## Workflow

### Step 1: Parse Input

Accept one of:
- **Script reference:** `SF #N` (looks up in your Notion Script Library or equivalent)
- **Inline content:** pasted text with sections, steps, stats
- **Conversation context:** content from earlier in the conversation

### Step 2: Fetch Script Content

**Path A, Script reference (SF #N):**
1. Query your Notion Script Library (or equivalent database) for `SF #{N}`
2. Read the page body content
3. Also check for any related lead magnet PDF if your pipeline generates them
4. Extract: title, hook, walkthrough steps, CTA keyword, key stats, pain points

**Path B, Inline/context:**
1. Parse content from pasted text or conversation context
2. Extract title from context or ask for one

### Step 3: Analyze Content & Select Template

Count patterns in the script content to pick the best email format:

| Content Pattern | Template | When to Use |
|---|---|---|
| Step-by-step walkthrough, numbered process | `lesson` | How-to tutorials, setup guides |
| Tool name + setup instructions + before/after | `tool` | Tool reviews, demos, configurations |
| Problem statement + reframe + mental model | `essay` | Frameworks, strategies, perspectives |
| Numbers, stats, percentages, results | `insight` | Case studies, data-driven content |
| Multiple discrete tips, shortcuts, quick wins | `tips` | Listicles, quick-win roundups |
| Two options compared, pros/cons, before/after | `comparison` | Decision guides, vs-style content |

**Selection logic:**
1. Count step-by-step patterns (numbered steps, "Step 1", "First,", "Then,")
2. Count tool mentions (specific tool names, "install", "setup", "configure")
3. Count stats/numbers (percentages, dollar amounts, time saved)
4. Count comparison patterns ("vs", "compared to", "before/after", "old way/new way")
5. Count tip patterns ("tip:", "pro tip:", standalone short advice blocks)
6. If essay-like structure (problem -> insight -> application), select essay

Pick the template with the highest pattern count. Ties go to `lesson` (most versatile).

### Step 4: Generate Email Content

Use the selected template function from `email_html.py`:

```python
import sys
sys.path.insert(0, str(Path.home() / "Desktop/AI Projects/newsletter"))
from email_html import render_email, template_lesson, template_tool, template_essay, template_tips, template_insight, template_comparison
```

**Subject line rules:**
- 1-4 words, lowercase, curiosity-driven
- No clickbait, no ALL CAPS, no emojis
- Frame as personal insight, not announcement
- Examples: "the hidden mode", "i was wrong", "this tool though", "3 things about ai"

**Generate 3 subject line variants** for the user to pick from (or A/B test in their platform).

**Preview text rules:**
- Completes the subject line hook
- 40-90 characters
- Creates a "sentence bridge," where subject + preview reads as one thought

**Body content rules:**
- Use your platform's first-name merge tag. Beehiiv uses `{{first_name | there}}` (double curly braces). Mailchimp uses `*|FNAME|*`. ConvertKit uses `{{ subscriber.first_name }}`. Update `email_html.py` for your platform.
- Keep under 500 words (sweet spot for creator newsletters: 300-500)
- Single CTA link, not a button
- P.S. line for secondary CTA or social proof
- Include link to the relevant resource (landing page, carousel, or video)

**Resource URLs:**
- Main offer CTA (your community, course, product, etc.)
- Landing page for the specific lead magnet this script references
- Carousel link (if you have one)
- Video URL (if you have one)

Configure your URLs in an env file or as constants at the top of `email_html.py`. Never hard-code personal URLs into this skill's logic.

### Step 5: Save Email Locally

1. Save the generated HTML to `~/Desktop/AI Projects/newsletter/drafts/sf{N}-{slug}.html`
2. Save email metadata to `~/Desktop/AI Projects/newsletter/drafts/sf{N}-{slug}.json`:
   ```json
   {
     "sf_number": 18,
     "title": "SF #18 - Plan Mode",
     "template": "lesson",
     "subject": "the hidden mode",
     "preview": "most people never find it",
     "subject_variants": ["the hidden mode", "i found a hidden mode", "plan before you build"],
     "word_count": 342,
     "created": "2026-03-04T12:00:00"
   }
   ```
3. Open the HTML file in the browser so the user can preview it

### Step 6: Push to Email Platform + Schedule

**For Beehiiv:** The Beehiiv public API (v2) is Enterprise-only for post creation. Use the `push_newsletter.py` script which combines Playwright browser automation + internal dashboard API.

```bash
python3 ~/Desktop/AI\ Projects/newsletter/push_newsletter.py
```

This script:
1. Creates a blank post via Playwright UI (Start writing > Blank draft)
2. Types the email body as WYSIWYG text into the editor (paragraph-by-paragraph - NOT raw HTML)
3. Sets title, subject line, and preview text via the internal dashboard API (PATCH with JWT auth)
4. Sets the scheduled send date via API
5. Confirms the schedule via the UI's Review page (clicks Schedule > Schedule for later > Publish on {date})

Options:
- `--dry` - preview what would be pushed
- `--limit N` - push only the first N drafts
- `--start-date YYYY-MM-DD` - set the first send date (default: today)
- `--cleanup` - delete broken/junk draft posts

**Why WYSIWYG text, not HTML Snippet (Beehiiv-specific):** Working Beehiiv posts use TipTap paragraph nodes. HTML Snippet blocks require CodeMirror interaction which is fragile. The WYSIWYG approach is proven reliable.

**For Mailchimp / ConvertKit / Brevo / other platforms:** These have full public APIs that accept `POST /campaigns` (or equivalent) directly without Enterprise requirements. Replace `push_newsletter.py` with a direct API call using your platform's SDK. The `/newsletter` skill's output (HTML + metadata JSON) works with any platform - only the push script changes.

### Step 7: Link Back to Your Script Library

1. Find the page for `SF #{N}` in your script database
2. If a platform post URL is available, update the page with "Newsletter URL" property
3. If scheduled, append the send date to the page body (e.g. "Newsletter scheduled: Tuesday Mar 25, 2026 at 9:00 AM EST")
4. If no URL yet, append a note that the newsletter draft was generated

### Step 8: Report

```
NEWSLETTER GENERATED: SF #{N} - {Title}

Template: {template_name}
Subject: {subject_line}
Preview: {preview_text}
Words: {word_count}
Scheduled: {send_date} (or "Draft - manual scheduling needed" if auto-schedule failed)

Local: ~/Desktop/AI Projects/newsletter/drafts/sf{N}-{slug}.html
Preview: Opened in browser

Subject variants (for A/B testing):
  1. {subject_1}
  2. {subject_2}
  3. {subject_3}
```

---

## Template Reference

### `lesson` : Weekly Lesson (Justin Welsh model)
Best for: Step-by-step tutorials, setup guides, process walkthroughs

Structure:
1. Personal hook from script's pain point (1 sentence)
2. Bridge : why this matters to THEM (1 sentence)
3. N-step framework (3-5 steps, each with title + 2-sentence desc)
4. CTA to resource
5. Sign-off + P.S.

### `tool` : Tool Breakdown
Best for: Tool reviews, demos, setup guides, configurations

Structure:
1. "I found something" hook
2. Tool name + what it does + timeframe
3. Setup steps (numbered, 3-5 steps)
4. Before/after result
5. CTA to full walkthrough

### `essay` : Problem-Solution Essay (Dan Koe model)
Best for: Frameworks, mental models, strategic perspectives

Structure:
1. Opening with problem/pain from script hook
2. Common approach + why it fails
3. Core insight/reframe
4. Actionable steps to apply
5. CTA to guide/resource

### `tips` : Numbered Tips (James Clear inspired)
Best for: Listicles, quick wins, standalone advice

Structure:
1. "{N} things I learned about {topic} this week:"
2. Each tip: bold title + 2-sentence explanation
3. CTA to go deeper

### `insight` : Insight + Resource (Sahil Bloom model)
Best for: Stats, results, data-driven content, case studies

Structure:
1. Lead with stat/result
2. Common interpretation -> reframe
3. Implications (3 bullets)
4. CTA to free resource

### `comparison` : Comparison Breakdown
Best for: Decision guides, vs-style content, before/after

Structure:
1. "I see people argue about this" hook
2. Option A with bullet points
3. Option B with bullet points
4. Nuanced verdict
5. CTA to full breakdown

---

## Platform Flexibility

The template logic, writing rules, subject line rules, and welcome series structure are **platform-agnostic**. What changes per platform is only:

- **The API wrapper** (`beehiiv_api.py` becomes `mailchimp_api.py`, `convertkit_api.py`, etc.)
- **The push script** (`push_newsletter.py` uses the new wrapper)
- **The merge tag syntax** in `email_html.py` (one-line change per platform)

For quick swap-out help, run:

```
Read beehiiv_api.py and create the equivalent module for {Mailchimp / ConvertKit / Brevo}. Match the function signatures exactly so push_newsletter.py still works.
```

The minimum interface any platform wrapper needs:

- `create_draft(title, subject, preview, html_body)` -> returns post_id
- `schedule_post(post_id, send_at_utc)` -> schedules the send
- `list_posts(status, limit)` -> lists posts
- `subscribe(email, first_name, custom_fields)` -> adds subscribers
- `test_connection()` -> verifies credentials

---

## Conversation Style

- **No approval pauses.** Analyze content, select template, generate email, and push to your platform in one flow.
- **Direct and fast.** Show progress: "Reading SF #18..." / "Selecting template: lesson (5 steps detected)..." / "Generating email..." / "Pushing..." / "Done."
- **Show the email body** in a code block so the user can review before checking their platform.
- **Always generate 3 subject line variants.**
