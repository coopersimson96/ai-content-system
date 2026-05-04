---
name: content-scripting
description: >
  Full content production workflow. Research real pain points, apply outlier
  content patterns, write short-form video scripts with hook variations
  (graded against the 100-point rubric in `/hooks`), group into series. Also
  handles script refreshes and rewrites using Inspiration Library data.
  Triggers on: "write scripts", "content batch", "rewrite script", "refresh
  script #N", "research and write".
argument-hint: "[topic] for [audience]" or "rewrite [file]" or "refresh #N" or "research + write [number] scripts about [topic]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebSearch
---

# Short-Form Video Script Production System

Full workflow from research to publish-ready scripts for TikTok, Reels, and YouTube Shorts. Every script is grounded in real audience pain, scored against an outlier content checklist, and structured using the proven hook frameworks from `/hooks`.

**This is NOT a generic content generator.** Every script must be rooted in a real problem a real person expressed online. No hypothetical topics.

---

## Step 1: Voice Check (Mandatory - Do Not Skip)

**Before writing any new script, run a voice check on your two most recent posted scripts.** No exceptions. This is a hard gate, not a suggestion.

### Why this is mandatory

Voice evolves between scripts. The patterns from a script written months ago are different from last week. Writing from memory or from this skill template produces stale, off-voice work that you'll have to manually rewrite. A voice check reads the actual most recent posted scripts and outputs the current patterns: hook structure, section labels, screen direction style, face interjection rhythm, closing line, caption opener, CTA word. These patterns inform every section of the new script.

### What a voice check is

A voice check is a script (you write it once, then reuse it) that grades your two most recent posted scripts against a fixed pattern checklist. The output appears in the conversation BEFORE any new script content. If it doesn't appear, the voice check was skipped.

A simple version:
1. Pull the last 2 scripts marked `Status = Posted` from your script library.
2. Extract: hook structure, section label format, screen tag format, face interjection count and length, closing line pattern, caption opener, CTA word style.
3. Print as a single block. New script must match.

### Workflow (run this BEFORE writing)

1. Find the 2 most recent script library entries with `Status: Posted`. Skip pages still in Scripts/Filming/Editing - those are unposted.
2. Extract the script content (Google Doc URL, raw text, whatever you have).
3. Run the voice check, output the patterns.
4. THEN write the new script, matching:
   - Hook structure (the SELECTED hook format from the most recent script)
   - Section labels (use the same casing/formatting as recent posts)
   - Screen direction style (matches the `[SCREEN - description]` format you've been using)
   - Face interjection rhythm (mid-script reframes - how many, how long)
   - Closing line pattern
   - Caption opener (one-sentence punch matching their current rhythm)
   - CTA word style (single word, ALL CAPS)

### Failure modes

- **No recent posted scripts:** This is the first script in the series. Skip Step 1 and use the patterns documented in Step 8 below.
- **Library/source unavailable:** Ask the user for the most recent posted script directly. Do not write the script without voice context.

If you write a script without showing voice check output in the conversation, you skipped Step 1.

---

## Step 2: Parse the Input

Extract from `$ARGUMENTS`:

1. **TOPIC** - The content niche
2. **AUDIENCE** - Target viewer
3. **COUNT** - How many scripts? (default: 10)
4. **PLATFORM** - TikTok, Reels, Shorts, or all? (default: all)
5. **TONE** - Professional, casual/raw, humorous, educational? (default: casual/raw)
6. **MODE** - What the user wants:
   - **"research + write"** (default) - Full workflow: research pain points, then write scripts
   - **"write from [pain points]"** - User provides pain points, skip research
   - **"rewrite [file]"** - Take existing scripts and apply outlier framework + hook variations
   - **"add hooks to [file]"** - Keep existing scripts, just add 3 hook variations each
   - **"refresh #N"** - Fetch existing script, generate fresh variations using new library data
   - **"new hooks for #N"** - Lightweight hook swap only

If TOPIC is missing, ask. Otherwise infer AUDIENCE and proceed.

---

## Step 3: Research Real Pain Points

**Skip this step ONLY if the user provides their own pain points or an existing file to rewrite.**

### Why This Step Exists

Scripts based on real complaints from real people outperform hypothetical topics every time. The audience sees the hook and thinks "that's literally me" because it IS literally them.

### Research Process

Use `/last30days` or manual research:

**Search queries (adapt to TOPIC):**
1. Reddit: `{TOPIC} frustration OR "waste time" OR "hate doing" OR "manual process" OR "how do I automate"`
2. X/Twitter: `{TOPIC} pain point OR complaint OR "wish there was" OR "spent hours" OR "waste of time"`
3. Web: `{TOPIC} biggest challenges survey`, `{TOPIC} time-consuming tasks`, `{TOPIC} automation opportunities`

**Extract from each source:**
- Exact quote or paraphrase of the complaint
- Engagement metrics (upvotes, likes, comments)
- Specificity (exact numbers/scenarios)
- Dollar/time amounts

### Pain Point Scoring

| Signal | Weight | Why |
|---|---|---|
| Engagement | HIGH | More people = bigger audience |
| Specificity | HIGH | Specific = relatable = better hooks |
| Solvability | HIGH | Script must deliver a real solution |
| Freshness | MEDIUM | Recency = currently top of mind |
| Cross-platform | MEDIUM | Reddit AND X = universal pain |

**Output:** A ranked list of {COUNT} pain points, each with one-line summary, source + engagement, and the specific solution. Show this list before writing scripts.

---

## Step 4: Apply the Outlier Content Checklist

Every script MUST pass ALL 12 checks before being included in the final output.

### Library Lookup (before scoring)

If your config (`config-templates/notion-content-config.json.example`) has `inspiration_data_source_id`, query the Inspiration Library for: Type IN [Hook Example, Creator Pattern], Performance Tier IN [Outlier, Strong], limit 5. Format as compact injection block. Fallback: proceed silently with hardcoded patterns only.

### The 12-Point Outlier Checklist

- [ ] **1. Hook lands in under 3 seconds** - 71% decide in first 3s
- [ ] **2. Specific real-world proof** - Exact numbers, dollars, hours. "3 hours -> 5 minutes" not "saves you time"
- [ ] **3. One tool, one problem** - Each script solves exactly ONE pain with ONE clear solution
- [ ] **4. Show-don't-tell** - Every script includes [SCREEN] cues showing the actual prompt, tool, or output
- [ ] **5. Result first, method second** - Lead with the outcome
- [ ] **6. Relatable pain from real people** - Topic came from an actual complaint, not a hypothetical
- [ ] **7. Anti-hype tone** - No "AI will change everything." Realistic framing builds trust
- [ ] **8. Series-ready** - Scripts grouped into themed series of 3-5
- [ ] **9. Works silent** - 85% watch without sound. Every hook has bold text overlay
- [ ] **10. 40-55 seconds** - Sweet spot. Body 120-180 words max
- [ ] **11. Scene changes every 2-4 seconds** - Alternate [FACE] and [SCREEN]
- [ ] **12. CTA builds funnel** - "Comment [WORD]" format drives DMs -> newsletter -> community

If a script fails any check, rewrite it.

---

## Step 5: Select Hook Frameworks

The 12 hook frameworks, templates, and selection rules live in the `hooks` skill. **Read `hooks/SKILL.md` Step 2 inline before generating hooks.** It is the single source of truth. Do not duplicate the framework list here.

For each script, generate **3-4 variations** using different frameworks. Mark one as SELECTED before grading (Step 7).

### Content-scripting-specific overrides

These stack on top of the framework selection rules in `/hooks`:

- For series scripts, default to **Curiosity Gap, Pain Point, or Negative Delta** for the SELECTED hook. These match the typical series voice ("Is it possible to X? Of course it is. You just need [one thing]"), which is itself an open-loop hook.
- After selecting frameworks, query the Inspiration Library (if configured) for concrete examples per framework.

---

## Step 6: Pre-flight Checklist (Mandatory Before Grading)

The 4 yes/no checks are documented in `hooks/SKILL.md` Step 2.4. **Read that section inline.** Don't grade until all four pass:

```
PRE-FLIGHT CHECKLIST
[ ] 1. Triple-stack aligned (text + visual + verbal carry same claim at sec 0)
[ ] 2. Outcome-framed (no job/role kill)
[ ] 3. Open-loop teased (kicker not revealed)
[ ] 4. Inspo for topic only (not copying structure)
```

The 4 checks at a glance:
- **Triple-stack:** the `[TEXT OVERLAY: ...]`, the first `[SCREEN: ...]`, and the SELECTED hook line carry the same claim at second 0.
- **Outcome > audience:** no job/role kills. Reframe around outcome.
- **Open-loop:** kicker is teased, never revealed in the hook.
- **Inspo for topic only:** if inspired by a specific reel/post, write in your own voice with your own personal experience. Don't copy flow or section order.

Print the checklist before the grading table. Fix failures, then re-run the checklist before grading hooks.

---

## Step 7: Hook Grading (Mandatory Before Selecting SELECTED)

The full 100-point 4-dimension rubric, benchmark anchors, tier gates, common weakening patterns, and iteration heuristic are defined in `hooks/SKILL.md` Step 2.5. **Read that section inline before grading.** Do not duplicate the rubric here.

### Content-scripting-specific additions

After selecting the highest-scoring hook as SELECTED:

1. **Store the score in your library.** Write the final score to your script library row's `Hook Score` property (number type). This builds the dataset for future rubric calibration against actual view performance.
2. **Flag visual-layer trade-offs explicitly.** The verbal-only rubric can't measure visual show-don't-tell. If a 90-point hook has visual before/after baked in (e.g., "from this [SCREEN: messy] to this [SCREEN: clean]") and a 93-point alternative is verbal-only, the 90 likely wins in distribution. Note the trade-off in the SELECTED line.
3. **Skip Proof-First by default.** Reads like a guru pitch. Only use when (a) no other framework fits AND (b) there's a hard dollar/metric anchor from real research AND (c) you explicitly justify the choice in grading commentary.

### Failure mode

If you write a script without showing the hook grading table in the conversation, you skipped Step 7. The grading table appears before the script body, not after.

---

## Step 8: Voice & Density Rules (CRITICAL)

These rules override everything else about script writing. If a script violates them, it is wrong.

The current series-brand patterns (title overlay format, section labels, opening structure, closing line) come from the voice check (Step 1) - not from this file. Don't hardcode patterns here. The rules below govern prose density and feature-vs-outcome framing inside whatever voice the voice check identified.

1. **Each section = 1-3 sentences MAX.** If a section has 4+ sentences, it's too long. Cut it.

2. **Never list features.** Do NOT write "generate, edit, restore, icons, patterns, diagrams, and storyboards." Instead write the RESULT: "create visual assets like a top level designer." The viewer doesn't care about the feature list. They care about what it does for them.

3. **No technical jargon in the script body.** No "MCP server." No "model versions." No "4K output." No "multi-turn editing." Hand it off in plain language. Technical details go in the hand-raiser PDF; the video sells the outcome.

4. **Use emotional shortcuts.** "Here's the cheatcode" / "like a top level designer" / "this is so powerful because" / "I even used this to..." This is how real people talk about tools they love. Feature specs are how documentation reads.

5. **Conversational glue between sections.** "Now here's the..." / "Of course it is" / "this is going to give claude..." / "So now..." - natural transitions, not formal ones. Never "Here's why this matters." or "Let me explain."

6. **Face interjections reframe in BENEFIT terms.** After showing something on screen (install, demo), cut to face and say ONE sentence about why it matters. Example: showed a tool on screen, then face: "I use this every day to break down competitor content and steal hooks from viral videos."

7. **Close is direct, no setup.** Pick the pattern by script type:

   **Walkthrough / listicle (default - dual-CTA stack):**
   > "Save this video and send it to anyone who [pain]. And if you want my breakdown on how to do this yourself comment [WORD], or if you want to copy my exact system click the link in my bio."

   The two CTAs don't compete. Comment WORD = "I'm interested but want a free sample first" (warm). Bio link = "I'm sold" (hot). Order matters: comment first (warm), bio link second (hot). Reversed feels salesy.

   **Short reactive / one-off (single-CTA fallback):**
   > "Save this video and if you want [specific thing] comment [WORD] and I'll send it to you."

   **Either way:** do NOT stack 3+ value props before the CTA. Two CTAs is the cap. Anti-pattern: stacking 3+ CTAs ("comment X, DM me, link in bio, also visit my website").

8. **Comma-separated examples over formatted lists.** "hero images for website, carousels for your content, images for blog posts or even ad creative" - NOT separate sentences for each use case.

9. **Total script body should be 120-180 words.** If it exceeds 200 words, cut until it hurts, then cut more.

10. **When in doubt, read it out loud at speaking pace.** If any section takes more than 8 seconds to say, it's too long. The entire script should take 40-55 seconds to speak naturally.

**IMPORTANT:** Always run the voice check. These documented patterns may be outdated. The voice check ensures you're matching your CURRENT voice, not a snapshot from weeks ago.

---

## Step 9: Script Structure

Every script follows the **evolved walkthrough format**: Title Overlay -> Hook (face) -> Series Branding -> Numbered Steps (screen) -> Close (face + CTA). The walkthrough IS the content.

### Visual Direction Tags

- **[FACE]** - Talking head, camera on creator
- **[SCREEN]** - Screen recording showing the actual tool/prompt/output

**Default split: 75% [SCREEN], 25% [FACE].** Face appears for the hook, a brief mid-walkthrough interjection, and the close.

**Text overlays go in a separate section at the bottom of each script** (not inline). This keeps the script body clean and readable as a filming guide.

### Platform Timing

| Platform | Hook Window | Total Length | Energy |
|---|---|---|---|
| TikTok | 2 seconds MAX | 25-45 seconds | 20% higher than normal |
| Reels | 3 seconds | 35-55 seconds | Casual but fast |
| Shorts | 3-5 seconds | 35-55 seconds | Structured storytelling |

### Script Template

```
# Script #{N} - {Title}

**Platform:** TikTok / Reels / Shorts | **Target:** {length} seconds | **Tone:** {Tone}
**Style Reference:** {Creator or style inspiration}
**Inspiration:** {Outlier creator(s) with view/like/comment counts}
**CTA WORD:** {WORD}

---

**HOOK A ({Framework Name}):**
**[FACE]** {Hook text}

**HOOK B ({Framework Name}):**
**[FACE]** {Alternative}

**HOOK C ({Framework Name}):**
**[FACE]** {Third variation}

**HOOK D ({Framework Name} -- SELECTED):**
**[FACE]** {The hook you'd film first}

PRE-FLIGHT CHECKLIST
[ ] 1. Triple-stack aligned
[ ] 2. Outcome-framed
[ ] 3. Open-loop teased
[ ] 4. Inspo for topic only

| Variation | Words | Scroll | Economy | Interrupt | Authority | Total | Tier |
|---|---|---|---|---|---|---|---|
| A | ... | ... | ... | ... | ... | ... | ... |

SELECTED: D - {reason}

---

**SCRIPT (Hook D version):**

{Title overlay text - bold claim}

**[FACE]** {Hook}

Welcome back to day {N} of the {Series Name}.

{SECTION NAME} **[SCREEN -- {what's on screen}]**
{1-2 sentences MAX. Direct, casual, action-oriented.}

[FACE]
{ONE sentence reframing the above in benefit terms.}

{SECTION NAME} **[SCREEN -- {what's on screen}]**
{1-3 sentences MAX. Show the thing, name the outcome.}

{SECTION NAME} **[SCREEN -- {what's on screen}]**
{Comma-separated examples. 1-2 sentences.}

**[FACE]** {Close - dual-CTA stack for walkthroughs/listicles, single-CTA fallback for short reactive content. See Voice & Density Rule 7.}

---

**CAPTION:**
{Line 1: Bold claim or hook - one sentence, punchy}
{Line 2 (OPTIONAL): One supporting detail. Skip if hook is strong enough alone.}

{Blank line, then CTA: Comment "[WORD]" for the [deliverable]}

{5 hashtags on their own line. Always exactly 5.}

---

**TEXT OVERLAYS:**
- [0:00] **{Title overlay - bold claim}**
- [0:02] {Supporting line}
- [0:05] **Step 1: {action}**
- [0:07] {Detail}
- [0:10] **Step 2: {action}**
- [0:13] {Detail}
- [0:21] **Step 3: {action}**
- [0:31] All from ONE {prompt/command/tool}
- [0:34] **Comment {WORD} for {deliverable}**

---

**THUMBNAIL OVERLAY OPTIONS:**
1. "{Bold statement}" ({visual description})
2. "{Alternative}" ({visual description})
3. "{Third option}" ({visual description})

---

**VISUAL DIRECTION:**
- {Screen/face ratio}
- {Title overlay style and placement}
- {Setup demo guidance}
- {Pacing reference}
- {Energy direction}

---

**PRODUCTION NOTES:**

### Why This Script Works
{3-5 bullets explaining what makes this script effective.}

### What We Have That The Inspo Didn't
{2-4 bullets on the specific edge over the inspiration.}

### Filming
{Script-specific filming instructions, timing breakdown.}

---

**CTA WORD:** {WORD}
```

### Script Template Rules

- **The full walkthrough IS the script.** Write it as one continuous voiceover.
- **Title overlay opens the video.** A bold claim appears as text on screen before/during the hook.
- **3-5 hooks, mark one as SELECTED.** The selected hook is what the walkthrough uses.
- **Face for hook + close + one mid-walkthrough interjection.** ~70-75% screen, ~25-30% face.
- **Each section is 1-3 sentences. Period.**
- **Never list features or specs in the script body.**
- **120-180 word target for the script body** (hook through close, excluding metadata/production notes).
- **Always include thumbnail overlay options and visual direction.**

### Text Overlay Rules
- Timestamps are approximate - adjust to actual pacing
- Every section should have at least one overlay (85% watch silent)
- Keep each overlay to 5-8 words max
- The first overlay [0:00] should appear immediately and match the core claim
- Overlays every 2-3 seconds
- Use overlays to reinforce key numbers, results, and the CTA

---

## Step 10: Group Into Series

After writing all scripts, organize them into themed series of 3-5 scripts each.

### Why Series Matter

- Series create binge behavior: viewers watch one and seek out the rest
- Algorithm rewards accounts that keep viewers on-platform longer
- Series give you a posting cadence: "Day 1 of [series name]" builds anticipation

### Series Naming Format

```
**"[Series Name]"** series: #{N}, #{N}, #{N}, #{N}
```

Choose series names that work as hashtags, sound like a mini-course, and are specific enough to set expectations.

---

## Step 11: Output Format

```
# {TOPIC} - {COUNT} Short-Form Video Scripts
### Built from {N} real pain points sourced from {sources summary}
### Every script scored against the 12-Point Outlier Content Checklist
### Style: Screen-first rapid walkthrough | Hook (3 variations) -> Walkthrough -> Result -> CTA

---
```

Output all scripts using the template from Step 9. Each script is self-contained.

After all scripts:

```
## Series Groupings

- **"[Series Name]"** series: #{list}
```

---

## Step 12: Generate Pipeline Assets (Optional)

After scripts are written, you can extend each script into a full content pipeline. Each of these is a separate skill in your library:

- **Hand raiser PDF** (`hand-raiser`) - lead magnet (guide, cheatsheet, checklist) for each script
- **Carousel** (`carousel-builder`) - Instagram carousel from the script
- **Blog post** (`blog-write`) - 1,500-2,000 word SEO article from the script
- **Newsletter** (`newsletter`) - email draft from the script content
- **Written posts** - X thread, LinkedIn post, Facebook post

Run them as needed.

---

## Follow-up Behavior

**If user says "write a teleprompter script for #X":**
- Write exact word-for-word with timing markers (e.g., [0:00-0:03], [0:03-0:08])
- Include exact on-screen text for each section
- Include 3 hook variations + grading table
- Include suggested post caption: 2-3 short punchy sentences max

**If user says "more scripts" or "add more":**
- Research additional pain points
- Write new scripts that don't overlap
- Add to series groupings

**If user provides an existing file to rewrite:**
- Read the file
- Identify which scripts pass the 12-point checklist
- Rewrite failing scripts to pass all 12
- Add 3 hook variations + grading
- Add [SCREEN] and [FACE] tags if missing
- Group into series

**If user provides pain points directly:**
- Skip research
- Score each pain point for viability
- Write scripts for the viable ones

**If user says "refresh #N" or "new version of #N":**
1. Fetch the original from your script library
2. Query Inspiration Library for new entries (Performance Tier IN [Outlier, Strong], added after the script was created)
3. If library entries have video Source URLs, offer to pull transcripts via `/transcript`
4. Generate 2-3 variations:
   - **Hook Refresh** - same body, 3 brand new hooks
   - **Angle Shift** - same pain point, different approach
   - **Full Rewrite** - only if 3+ new library entries exist
5. Show diff (old vs new), cite which library entries inspired each change
6. Offer to save as next script number

**If user says "new hooks for #N":**
1. Fetch original
2. Query Inspiration Library for Hook Examples matching topic
3. Generate 3 new hooks using different frameworks than the originals
4. Run pre-flight + grading
5. Show old vs new side by side

**If user asks about strategy:**
- 85% watch without sound
- 71% decide in first 3 seconds
- 65%+ 3-second retention = 4-7x more impressions
- Authentic content performs 60% better than overproduced
- Series format drives binge behavior
- Scene changes every 2-4 seconds maintain retention
- "Comment [WORD]" CTAs drive 3-5x more DMs than generic CTAs
