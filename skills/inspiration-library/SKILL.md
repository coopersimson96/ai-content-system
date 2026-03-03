---
name: inspiration-library
description: Save, browse, and manage your Inspiration Library — a living knowledge base of viral hooks, creator patterns, script formats, and content research. Includes library health checks and research scoring. Queryable during content creation.
argument-hint: "save this as inspiration" or "show my library" or "library health" or "how's my library"
context: conversation
---

# Inspiration Library Manager

Manages the Inspiration Library database in Notion — a growing reference of hooks, creator patterns, viral templates, and research findings that feed into your content creation workflow.

---

## Setup Check

On every invocation:

1. Read `~/.config/notion-content/config.json` to get `inspiration_data_source_id`
2. If missing, tell the user:
   > Inspiration Library isn't set up. The database needs to be created first.

Store the data source ID for all operations.

---

## Intent Detection

Parse `$ARGUMENTS` and detect what the user wants:

### Save Entry
**Trigger:** "save this", "add to library", "bookmark this", "save as inspiration", context from a previous conversation (transcript, research finding, hook, creator pattern)

**Action:**
1. Parse the current conversation context to extract:
   - **Title** — descriptive name for the entry
   - **Type** — auto-infer from context: transcript → `Transcript`, creator analysis → `Creator Pattern`, hook → `Hook Example`, research data → `Research Finding`, script format → `Script Format`, carousel/slides → `Carousel Example`
   - **Platform** — infer from context or ask if unclear
   - **Hook Framework** — match to one of: `Curiosity Gap`, `Proof-First`, `Pain Point`, `Contrarian`, `This Cost Me Thousands`, `Unexpected Confession`, `Question Hook`, `Pattern Interrupt`, `Before vs After`, `Test / Experiment`
   - **Performance Tier** — `Outlier` (3x+ median, 100K+ views), `Strong` (above-avg with metrics), `Reference` (useful, no metrics), `Untested` (no data)
   - **Source** — `Creator Analysis`, `Research`, `Transcript`, `My Content`, `Manual`
   - **Source URL** — if a URL exists in context
   - **Creator Handle** — @handle if present
   - **Topic Tags** — infer from content, use existing tags when possible: `AI Tools`, `Business Automation`, `Productivity`, `Tutorial`, `Social Proof`. New tags are fine.
   - **Engagement Metric** — any numbers: views, likes, revenue, growth
   - **Hook Text** — the actual hook/template if applicable
   - **Notes** — any additional context worth preserving. **For Carousel Example entries**, Notes MUST include: slide count, design style (gradient/flat/textured/photo), color palette, text density (heavy/medium/light), photo vs graphic, typography style, and any distinctive layout patterns

2. **Aim for under 3 questions before creating.** Auto-infer as much as possible. Only ask when truly ambiguous (e.g., Type could be multiple things, or Performance Tier is unclear).

3. Show the user what you're about to save:
   > Saving to Inspiration Library:
   > - **Title:** {title}
   > - **Type:** {type} | **Tier:** {tier}
   > - **Hook Text:** "{hook_text}"
   > - **Tags:** {tags}
   >
   > Good to save?

4. Create the Notion page using `notion-create-pages` with `data_source_id` from config:
   - Set `date:Date Added:start` to today's date (ISO-8601)
   - If there's substantial context (full transcript, detailed breakdown), put it in the page body
   - Properties only get the compact data

5. Confirm: "Saved: {Title} ({Type}, {Tier})"

---

### Browse / Query
**Trigger:** "show my library", "browse", "inspiration on [topic]", "what hooks do I have for [framework]", "show [type] entries", "library"

**Action:**
1. Use `notion-search` with `data_source_url` set to `collection://{inspiration_data_source_id}` to find matching entries
2. For topic queries, search by the topic keyword
3. For type/framework/tier queries, search and filter the results

**Output format — compact list:**
```
INSPIRATION LIBRARY ({filter context}):

[1] "{Hook Text or Title}" — @{creator} | {Type} | {Tier} | {Engagement Metric}
[2] "{Hook Text or Title}" — @{creator} | {Type} | {Tier} | {Engagement Metric}
...

{N} entries found. Say "show me #N" for full details.
```

If user asks for full details on a specific entry, fetch the page and show all properties + page body content.

---

### Manual Add
**Trigger:** "add [URL] to library", "save this link", URL + "inspiration" or "library"

**Action:**
1. If the URL is a video (TikTok, Instagram, YouTube, X, Facebook):
   - Offer: "Want me to pull the transcript first? I can extract the hook and key patterns."
   - If yes, use the `/transcript` skill flow (read `~/.claude/skills/transcript/skill.md`), then save with Type=`Transcript`, Source=`Transcript`
   - Auto-extract: Hook Text = first spoken line, Creator Handle from URL
2. If non-video URL: save as Type=`Research Finding`, Source=`Manual`
3. Follow the same save flow as above

---

### Score Research
**Trigger:** "score this research", "analyze these findings", "which ones should I save", "best findings", "curate"

**Action:**
When research output exists in the conversation (from `/last30days` or any research), score each finding on 5 dimensions:

| Dimension | What to Check |
|---|---|
| **Engagement** | Upvotes/likes relative to platform norms. Reddit 100+ = strong, 500+ = outlier. X 50+ = strong, 500+ = outlier. |
| **Specificity** | Has exact numbers, dollar amounts, timeframes? |
| **Cross-Platform** | Appears on multiple platforms? |
| **Freshness** | Posted in last 30 days? |
| **Library Gap** | No existing library entry covers this topic? (Query library to check.) |

Rate each finding 0-5 stars total. Show ranked output:

```
RESEARCH SCORING:

[1] ★★★★★ "{quote}" — {engagement}, {source}
    → {why it scored high}. SAVE AS: {entry type}
[2] ★★★★☆ "{quote}" — {engagement}, {source}
    → {assessment}. SAVE AS: {entry type}
[3] ★★★☆☆ "{quote}" — {engagement}, {source}
    → {assessment}. Not library-worthy yet.

PATTERNS: "{theme}" cluster ({N} findings)

RECOMMENDED SAVES: {N} entries. Save them?
```

If user confirms, save qualifying entries using the standard Save Entry flow.

---

### Library Health Check
**Trigger:** "library health", "how fresh is my library", "what's stale", "audit my library", "coverage gaps"

**Action:**
1. Query ALL entries from the Inspiration Library (up to 50 results)
2. Analyze and report:

```
LIBRARY HEALTH:

Freshness: {N}/{total} entries added in last 30 days
Coverage gaps: Missing entries for {topics with 0 entries}
Tier balance: {N} Outlier, {N} Strong, {N} Reference, {N} Untested
Framework gaps: {frameworks with <2 examples}
Stale (never used, 60+ days old): {N} entries

ACTIONS:
- {specific recommendation}
- {specific recommendation}
```

**Analysis dimensions:**
- **Age** — entries by Date Added, flag anything 90+ days with no Last Used
- **Coverage** — Topic Tags distribution vs common content topics
- **Tiers** — warn if >50% are Reference/Untested
- **Frameworks** — flag any of the 10 hook frameworks with <2 examples
- **Stale** — entries with no Last Used date AND Date Added > 60 days ago

---

### Stats
**Trigger:** "how's my library", "library stats", "stats", "how many entries"

**Action:**
1. Query all entries from the inspiration library
2. Compile and show:

```
INSPIRATION LIBRARY STATS:

Total entries: {N}

By Type:
- Hook Example: {n}
- Creator Pattern: {n}
- Script Format: {n}
- Transcript: {n}
- Research Finding: {n}
- Carousel Example: {n}
- Other: {n}

By Performance Tier:
- Outlier: {n}
- Strong: {n}
- Reference: {n}
- Untested: {n}

Top Hook Frameworks:
- {framework}: {n} entries
- {framework}: {n} entries
...

Most-used Topic Tags:
- {tag}: {n} entries
...

Last added: {date} — "{title}"
Last used in scripts: {date} — "{title}"
```

---

## Query Modes (for other skills)

When other skills query this library during content creation, they should use these modes:

### Mode 1: Property-Only (default during script creation)
Returns: Title, Type, Hook Framework, Engagement Metric, Hook Text. **For carousel queries**, also return Notes field (contains style data needed for remix generation).
Max 5 results. ~250 tokens total.

**Compact injection format:**
```
INSPIRATION LIBRARY ({filter context}):
[1] "{Hook Text}" — @{creator} | {Tier} | {Engagement Metric}
[2] "{Hook Text}" — @{creator} | {Tier} | {Engagement Metric}
```

### Mode 2: Summary (research phase)
Up to 10 entries, properties only. For supplementing research output.

### Mode 3: Full Page (on-demand only)
Full page body content. Only when user explicitly asks "show me the transcript for X" or "full details on X". **Never auto-loaded during script creation.**

---

## Conversation Style

- **Quick and direct.** "Saved: Harper Carroll series pattern (Creator Pattern, Outlier)" — not a paragraph about what you did.
- **Auto-infer aggressively.** If context makes Type, Tier, and Tags obvious, don't ask. Just show what you're saving and let them correct.
- **Max 2 clarifying questions.** If you need more than that, save what you can and note the gaps.
- **Compact output.** Library browse results should be scannable, not walls of text.

---

## Opening (No Arguments)

If invoked without arguments:

> What do you need?
>
> I can:
> - **Save** — "save this as inspiration" (uses current context)
> - **Browse** — "show hooks for Proof-First" or "inspiration on AI tools"
> - **Add URL** — "add [URL] to library" (optionally pulls transcript)
> - **Score research** — "which findings should I save?"
> - **Health check** — "how fresh is my library?"
> - **Stats** — "how's my library"
>
> Or just tell me what you're looking at.
