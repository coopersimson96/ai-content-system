---
name: topic-researcher
description: Find outlier content ideas for short-form video. Multi-angle research, dedup, scored topic cards with approval workflow. Works for any niche.
argument-hint: "find topics" or "10 topic ideas" or "topics about AI for restaurants"
context: conversation
---

# Topic Researcher — Outlier Content Idea Finder

Find scored, deduplicated topic ideas for short-form video content. Multi-angle research surfaces outlier ideas for review before any scripts get written.

---

## Content Filter — ENFORCED ON ALL TOPICS

Every topic MUST pass this filter before being included. No exceptions.

### Niche Scope

<!-- CONFIGURE YOUR NICHE: Replace YOUR_NICHE_DESCRIPTION below with your specific niche and content focus.
     Examples:
     - "AI use cases for business owners, built with Claude Code, ChatGPT, or general AI assistants"
     - "Fitness and nutrition tips for busy professionals"
     - "Real estate investing strategies for first-time investors"
     - "SaaS product demos and software tutorials"
     - "Personal finance and budgeting for millennials"
-->

**YOUR NICHE:** YOUR_NICHE_DESCRIPTION

Only surface topics that fit within your configured niche above. If no niche is configured, ask the user what their content niche is before proceeding.

### Topic Quality Gate

Every topic must be:
1. **Clearly definable** — You can explain the entire workflow in under 60 seconds.
2. **Solves a real problem** — Backed by a real person's complaint/frustration from research. No hypothetical "wouldn't it be cool if" topics.
3. **Buildable on camera** — The viewer can watch you build or use it in a screen recording. If it can't be demonstrated, it's not a topic.
4. **Niche-aligned** — Fits within the configured niche scope above.

---

## Opening

When invoked with no arguments or just `/topic-researcher`:

> What kind of topics are you looking for?
>
> I can:
> - **Find topics** — outlier content ideas scored for viral potential
> - **Industry-specific** — topics for specific verticals or audiences
> - **Trending tools** — what's blowing up on Product Hunt, X, Reddit right now
>
> Just say "find me 10 topics" or "topics about [your niche]" to get started.

If `$ARGUMENTS` is provided, parse it for:
- **COUNT** — how many topics (default: 10)
- **INDUSTRY** — specific vertical to focus on (optional)
- **ANGLE** — specific research angle to emphasize (optional)

Skip the greeting and start researching immediately.

---

## Step 1: Multi-Angle Research

Run 6 research angles to surface diverse topic ideas. Don't just search one query — cast a wide net.

### Research Angles

| # | Angle | What to Search |
|---|---|---|
| 1 | Pain Points | Common tasks in the niche that are manual, time-consuming, or frustrating |
| 2 | Builds / Demos | Things people are building, creating, or demonstrating in this space |
| 3 | Case Studies / ROI | Real results, time saved, money saved, before/after transformations |
| 4 | Experiments | "I tried X" posts — experiments and tests with real outcomes |
| 5 | Competitor Creators | Other creators making content in this niche — what's getting engagement |
| 6 | Industry-Specific | Niche-specific workflows, tools, or use cases (rotate sub-niches) |

### Execution

**Batch 1 — `last30days.py` broad sweep (angles 1-3):**

```bash
python3 ~/.claude/skills/last30days/scripts/last30days.py "{NICHE KEYWORDS}" --emit=compact 2>&1
```

**Batch 2 — Targeted WebSearch (angles 4-6):**

Run 3 WebSearch calls:

1. **Experiments:** `"{niche keywords}" results OR "I tried" OR experiment workflow` (blocked_domains: reddit.com, x.com, twitter.com)
2. **Competitor Creators:** `"{niche keywords}" creator content viral tips` (blocked_domains: reddit.com, x.com, twitter.com)
3. **Industry-Specific:** `"{niche keywords}" {INDUSTRY OR sub-niche} use case workflow` (blocked_domains: reddit.com, x.com, twitter.com)

If the user specifies an industry filter, weight angle 6 heavily — run 2 industry-specific searches instead of 1.

### Post-Research Filter

After gathering raw results, apply the **Content Filter** (above) to every potential topic. Discard anything that doesn't fit the configured niche. Reframe surviving topics through the niche lens where possible.

### Extract from Results

For each potential topic, extract:
- **Topic idea** — one-line video concept
- **Angle** — which of the 6 angles it came from
- **Tool** — specific tool involved (if any)
- **Pain** — the problem it solves
- **Proof** — specific numbers, stats, before/after data
- **Source** — Reddit thread, X post, article URL
- **Engagement** — upvotes, likes, comments, views

---

## Step 2: Deduplication

Before scoring, check both Notion databases to flag topics already covered.

### Query Script Library

Read `~/.config/notion-content/config.json` to get `script_library_db_id`. If present:

Use `notion-search` with:
- `data_source_url`: `collection://{script_library_db_id}`
- Search for broad topic keywords
- Extract: Script Title + Topic from results

If config missing, skip silently.

### Query Inspiration Library

Read `~/.config/notion-content/config.json` to get `inspiration_data_source_id`. If present:

Use `notion-search` with:
- `data_source_url`: `collection://{inspiration_data_source_id}`
- Search for broad topic keywords
- Extract: Title + Topic Tags from results

If config missing, skip silently.

### Flagging

Compare each discovered topic against both databases:
- If a topic substantially overlaps with an existing script or inspiration entry, mark it `COVERED`
- Do NOT auto-discard covered topics — let the user decide
- A topic is "covered" if the same tool + same pain point + same angle already exists

---

## Step 3: Outlier Scoring

Score each topic on 5 dimensions (1-5 stars each). Only present topics scoring 3+ stars overall.

| Dimension | Weight | 5-star = | 1-star = |
|---|---|---|---|
| Engagement | 30% | Multiple high-engagement posts (Reddit 100+, X 500+) | Single low-engagement mention |
| Specificity | 25% | Named tool + named use case + specific numbers | Generic vague topic |
| Freshness | 15% | Trending in last 7 days | 30+ days old, widely covered |
| Proof Availability | 15% | Screenshot-ready demo, specific stats, before/after | Abstract, no visual proof |
| Competition Gap | 15% | No major creators covering this angle | Already saturated |

### Scoring Formula

```
Weighted Score = (Engagement x 0.30) + (Specificity x 0.25) + (Freshness x 0.15) + (Proof x 0.15) + (Competition Gap x 0.15)
```

Round to one decimal. Convert to star display (e.g., 4.2 = four filled stars + partial).

---

## Step 3.5: Deep Research — 5 Angles Per Topic (AUTOMATIC)

**This step runs automatically after scoring.** For every topic that scores 3+ stars, run deep research to surface 5 distinct script angles. This makes each topic card significantly richer and gives the user real options for how to approach the script.

### Why This Step Exists

One topic can become 5 completely different videos depending on the angle. Deep research finds the best angle by looking at what's actually resonating online for each topic.

### Execution

For each topic that passed scoring, run **2 targeted WebSearch calls**:

1. **Angle discovery:** `"{topic keywords}" script OR video OR content angle approach 2026` (blocked_domains: reddit.com, x.com, twitter.com)
2. **Proof mining:** `"{tool from topic}" results OR "saved me" OR "before and after" OR case study` (blocked_domains: reddit.com, x.com, twitter.com)

**To keep speed reasonable:** Run searches for all topics in parallel (not sequentially). If there are 10 topics, that's 20 WebSearch calls — run them all at once.

### The 5 Angle Framework

For each topic, generate exactly 5 angles using this framework. Not every angle will be strong for every topic — that's fine. Rate each angle 1-3 strength dots (three dots = strongest) so the user can see which ones have the most potential.

| Angle | What It Is | Best When |
|---|---|---|
| **1. Proof-First** | Lead with the result/number. Show the outcome before explaining how. | Strong stats, dollar amounts, or time-saved numbers exist in research |
| **2. Step-by-Step Tutorial** | Walk through the build/workflow on camera. | The workflow is clearly definable and can be demoed in under 60 seconds |
| **3. Challenge / Experiment** | Frame it as a test with an unknown outcome. | There's a bold claim to test, or a common assumption to challenge |
| **4. Myth-Buster / Contrarian** | Challenge the conventional wisdom. | There's a popular belief that the research contradicts |
| **5. Industry / Niche Remix** | Narrow the audience to a specific sub-niche. | The topic can be applied to a specific industry with tailored examples |

### Angle Card Format

For each topic, append the 5 angles below the Script Preview:

```
Angles:
1. ●●● PROOF-FIRST: "I replaced my $3K/mo agency with a free tool — here are the results"
   → Key proof: [specific stat]. Screen: [what you'd show]. Why strong: [1 sentence].
2. ●● TUTORIAL: "How to set up your own audit in 4 minutes"
   → Steps: [3-step summary]. Screen: [what you'd show]. Why strong: [1 sentence].
3. ●●● CHALLENGE: "I gave this tool 7 days to outperform my agency. Here's who won."
   → Setup: [the challenge framing]. Payoff: [what the result reveals]. Why strong: [1 sentence].
4. ● MYTH-BUSTER: "Your agency doesn't want you to see this free tool"
   → Myth: [the assumption]. Reality: [what research shows]. Why strong: [1 sentence].
5. ●● NICHE REMIX: "If you run a restaurant, this tool was made for you"
   → Niche: [industry]. Tailored proof: [industry-specific stat]. Why strong: [1 sentence].
```

### Enrichment from Deep Research

Use the WebSearch results to fill in each angle with **real data**:
- **Proof-First** — find the strongest stat, dollar amount, or time-saved number
- **Tutorial** — find existing tutorials or walkthroughs to identify the clearest 3-step flow
- **Challenge** — find "I tried X" posts or experiment-style content for framing inspiration
- **Myth-Buster** — find contrarian takes or common misconceptions about the topic
- **Niche Remix** — find industry-specific applications, stats, or case studies

If deep research surfaces a new angle that doesn't fit the 5-framework but is clearly strong (e.g., a trending meme format, a news hook, a celebrity endorsement), add it as a **Bonus Angle** with a note on why it's worth considering.

### Strength Rating Guide

- ●●● = Strong proof exists, clear visual demo, high engagement signal from research
- ●● = Decent framing but proof is weaker or demo is less visual
- ● = Possible but would need more creative work to make it land

---

## Step 4: Topic Cards

Present topics as ranked cards, highest score first.

### Card Format

```
TOPIC #1 ★★★★★ (4.8)
Title: [one-line video title idea]
Angle: [proof-first / pain point / tutorial / experiment / case study]
Tool: [specific tool if applicable]
Workflow: [1-2 sentence step-by-step — what you'd build or do on camera]
Pain: [problem it solves]
Proof: [specific number/stat from research]
Source: [Reddit thread, X post, etc.]
Why it works: [1 sentence]
Status: NEW or COVERED

Script Preview:
- [Beat 1: Hook — what you'd say/show in the first 3 seconds]
- [Beat 2: Problem — the pain point you're calling out]
- [Beat 3: Solution — what you build or demo on screen]
- [Beat 4: Proof — the specific result or number that lands]
- [Beat 5: CTA — what you tell them to do next]
```

The Script Preview gives a quick feel for what the final video would actually be. Each bullet is a "beat" — roughly one scene or moment in the video. This helps the user decide whether the topic has enough substance to become a full script before approving it.

### Auto-Push to Notion

**Immediately after presenting topic cards**, push ALL topics to the Script Library as Ideas/Topics if Notion is configured. Do not wait for approval — push them right away so they appear on the board.

Read `~/.config/notion-content/config.json` to get `script_library_db_id`. If present:

Use `notion-create-pages` with:
- `data_source_id`: value of `script_library_db_id` from config
- For each topic card, create a page with:
  - **Script Title** = the topic card Title
  - **Status** = `Ideas/Topics`
  - **Topic** = user-specified topic or niche
  - **Notes** = Compact summary: `Score: {score} | Angle: {angle} | Tool: {tool} | Workflow: {workflow}`
  - **Pain Point Source** = the Source URL/reference from the topic card
  - **Page content** = Script Preview (5 beats) + the 5 Angles from deep research, formatted as shown in Step 3.5

If config missing, skip silently and just present the cards.

Track the Notion page URL returned for each topic — you'll need it for approval/rejection.

### Presentation

After pushing to Notion (or if Notion not configured), show the cards and summary:

```
{N} topics found. {M} new, {K} overlap with existing scripts.
All {N} topics pushed to Script Library → Ideas/Topics column.

What next?
- "approve 1, 3, 5" — keep these, remove the rest
- "approve all" — keep everything
- "reject 2, 4" — remove specific topics
- "modify 2" — adjust angle/framing before deciding
- "more topics" — run another research pass
- "save" — save these results to a file
```

---

## Step 5: Approval Workflow

### Approve

When user says "approve 1, 3, 5" (or similar):
1. Confirm the selected topics
2. **Delete rejected topics from Notion** (if Notion configured) — use `notion-update-page` or the Notion API to archive/delete the pages for any topic NOT in the approved list
3. **Save approved topics to memory** — append to `~/.claude/content-system/approved-topics.md` (create if it doesn't exist). Format:
   ```
   ## Approved {date}
   - **{Title}** — {Angle} | {Tool} | {Pain} | Score: {score}
   ```
   This file builds a pattern of what the user gravitates toward, reinforcing future topic generation.
4. Tell the user: "{N} approved, {M} removed from board."
5. Offer: "Ready to write scripts for these? Say 'write scripts' to start."

### Approve All

When user says "approve all":
1. Keep all topics in Notion
2. Save all to memory file
3. Offer script handoff

### Reject

When user says "reject 2, 4" (or similar):
1. **Delete those pages from Notion** (if configured) — remove from Script Library entirely
2. Do NOT save rejected topics to memory
3. Show updated count: "{N} remaining in Ideas/Topics."

### Modify

When user says "modify 2" (or similar):
1. Show the topic card
2. Ask what to change (angle, tool, framing)
3. Update the card and re-score
4. **Update the Notion page** with the modified title/notes (if configured)
5. Add back to the approved list if user confirms

### More Topics

When user says "more topics":
1. Run another research pass with different search queries
2. Deduplicate against already-shown topics AND existing Ideas/Topics in Notion
3. Present new cards and push new topics to Notion

### Save

When user says "save":
1. Save all topic cards to `~/ai-content-system/output/topic-research-{YYYY-MM-DD}.md`
2. Include scores, sources, and approval status
3. Tell the user the file path

---

## Memory Layer — Topic Preferences

The file `~/.claude/content-system/approved-topics.md` acts as a reinforcement layer.

### How It Works

- Every approved topic gets appended with its angle, tool, pain point, and score
- Every rejected topic is NOT saved — absence is signal
- Over time, this file builds a profile of what the user wants:
  - Which angles they prefer (proof-first vs tutorial vs experiment)
  - Which tools they gravitate toward
  - Which pain points resonate
  - What score threshold they actually approve at

### Using the Memory

**Before scoring topics**, read `~/.claude/content-system/approved-topics.md` if it exists. Use the patterns to:
1. **Boost scores** for topics matching approved patterns (preferred angles, tools, pain types)
2. **Lower scores** for topics similar to ones that were previously rejected (if a pattern emerges)
3. **Mention the pattern** to the user: "Based on your history, you tend to approve [proof-first builds]. Scored accordingly."

This makes each research pass smarter than the last.

---

## Step 6: Handoff to Content-Scripting

When user says "write scripts" after approving topics:

1. Format approved topics as pain points:
   - One-line summary of each topic
   - Source + engagement data
   - The specific solution

2. Read `~/.claude/skills/content-scripting/skill.md`

3. Start at **Step 3** (Outlier Checklist) with:
   - **TOPIC** = user-specified topic or niche
   - **AUDIENCE** = user-specified audience
   - Pain points = the approved topic cards formatted as pain points

4. Follow content-scripting from Step 3 onward — the research is already done.

---

## State Management

Track throughout the conversation:

```
RESEARCH_STATUS: [not started | in progress | complete]
TOPICS_FOUND: [count]
TOPICS_APPROVED: [list of approved topic numbers]
TOPICS_REJECTED: [list of rejected topic numbers]
TOPICS_COVERED: [list of covered topic numbers]
INDUSTRY_FILTER: [if specified]
NOTION_PAGES: [map of topic number → Notion page ID/URL — needed for deletion]
```

**CRITICAL:** Always track the Notion page URL/ID returned when creating pages. Without this, you cannot delete rejected topics.
