---
name: content-scripting
description: Full content production workflow — research real pain points, apply outlier content patterns, write short-form video scripts with hook variations, group into series. Also handles script refreshes and rewrites using Inspiration Library data.
argument-hint: "[topic] for [audience]" or "rewrite [file]" or "refresh SF #3" or "research + write [number] scripts about [topic]"
context: conversation
---

# Short-Form Video Script Production System

Full workflow from research to publish-ready scripts for TikTok, Reels, and YouTube Shorts. Every script is grounded in real audience pain, scored against an outlier content checklist derived from 10+ documented viral creators, and structured using proven hook frameworks from 16K+ social media engagements.

**This is NOT a generic content generator.** Every script must be rooted in a real problem a real person expressed online. No hypothetical topics.

---

## Step 1: Parse the User's Input

Extract from `$ARGUMENTS`:

1. **TOPIC** — The content niche (e.g., "AI for business owners", "fitness for beginners", "SaaS product demos")
2. **AUDIENCE** — Target viewer (e.g., "small business owners", "founders", "freelancers")
3. **COUNT** — How many scripts? (default: 10)
4. **PLATFORM** — TikTok, Reels, Shorts, or all? (default: all)
5. **TONE** — Professional, casual/raw, humorous, educational? (default: casual/raw)
6. **MODE** — What the user wants:
   - **"research + write"** (default) — Full workflow: research pain points, then write scripts
   - **"write from [pain points]"** — User provides pain points, skip research
   - **"rewrite [file]"** — Take existing scripts and apply outlier framework + hook variations
   - **"add hooks to [file]"** — Keep existing scripts, just add 3 hook variations each
   - **"refresh SF #N"** — Fetch existing script from Notion, generate fresh variations using new library data
   - **"new hooks for SF #N"** — Lightweight hook swap only, keep everything else

**If TOPIC is missing**, ask:

> What's the content about and who's it for?
>
> Example: `/scripts AI automation for small business owners`
> Example: `/scripts rewrite "My Content.md"`

**If only TOPIC is provided**, infer AUDIENCE and proceed. Don't over-ask.

---

## Step 2: Research Real Pain Points

**CRITICAL: Skip this step ONLY if the user provides their own pain points or an existing file to rewrite.**

### Why This Step Exists

Scripts based on real complaints from real people outperform hypothetical topics every time. The audience sees the hook and thinks "that's literally me" because it IS literally them — their exact words, their exact frustration.

### Research Process

Use the `/last30days` skill or manual research to find burning problems:

**Search queries to run (adapt to TOPIC):**

1. Reddit: `{TOPIC} frustration OR "waste time" OR "hate doing" OR "manual process" OR "how do I automate"` in relevant subreddits
2. X/Twitter: `{TOPIC} pain point OR complaint OR "wish there was" OR "spent hours" OR "waste of time"`
3. Web: `{TOPIC} biggest challenges survey`, `{TOPIC} time-consuming tasks`, `{TOPIC} automation opportunities`

**What to extract from each source:**
- The **exact quote** or paraphrase of the complaint
- **Engagement metrics** (upvotes, likes, comments) — higher = more people feel this pain
- **Specificity** — "I spend 3 hours routing technicians" beats "scheduling is hard"
- **Dollar/time amounts** — real numbers make scripts credible

### Pain Point Scoring

Rank discovered pain points by:

| Signal | Weight | Why |
|---|---|---|
| Engagement (upvotes/likes) | HIGH | More people = bigger audience for this topic |
| Specificity (exact numbers/scenarios) | HIGH | Specific = relatable = better hooks |
| Solvability (can AI actually fix this?) | HIGH | Script must deliver a real solution |
| Freshness (posted recently) | MEDIUM | Recency = currently top of mind |
| Cross-platform appearance | MEDIUM | Shows up on Reddit AND X = universal pain |

**Output: A ranked list of {COUNT} pain points, each with:**
- One-line summary
- Source + engagement data
- The specific AI solution

**Show this list to the user before writing scripts.** Get confirmation or let them swap topics.

---

## Step 3: Apply the Outlier Content Checklist

Every script MUST pass ALL 12 checks before being included in the final output. This checklist is derived from documented outlier creators:

- **Harper Carroll** — 2K → 200K Instagram followers in 3 weeks. Calm, educational, series-based. One video = 250K followers.
- **Matt Wolfe** — 857K YouTube subscribers, 65.5M total views. Hooks in first 15-30s, open-ended titles.
- **@ogilichev** — 60M views from repeating one hook format with tiny tweaks across 3 accounts.
- **@timdanilovhi** — 70+ Shorts earning $1K-$7K each using the same ideation framework.
- **@seergioo_gil** — 12M views from 4 Shorts by copying a proven viral format.

### Library Lookup (before scoring)

Before applying the checklist, check if `~/.config/notion-content/config.json` has `inspiration_data_source_id`. If so:

1. Query the Inspiration Library using `notion-search` with `data_source_url` set to `collection://{inspiration_data_source_id}` for the current topic
2. Filter for: Type IN [Hook Example, Creator Pattern], Performance Tier IN [Outlier, Strong], limit 5 results
3. Format as compact injection block and treat as additional examples alongside the hardcoded patterns below:

```
INSPIRATION LIBRARY ({topic}):
[1] "{Hook Text}" — @{creator} | {Tier} | {Engagement Metric}
[2] "{Hook Text}" — @{creator} | {Tier} | {Engagement Metric}
```

4. **Fallback:** If 0 results or config missing, proceed silently with hardcoded patterns only
5. Track which library entries were referenced (for Last Used update after push)

### THE 12-POINT OUTLIER CHECKLIST

For every script, verify:

- [ ] **1. Hook lands in under 3 seconds** — 71% of viewers decide in first 3s whether to keep watching
- [ ] **2. Specific real-world proof** — Exact numbers, dollars, hours from real people. No vague claims. "3 hours → 5 minutes" not "saves you time"
- [ ] **3. One tool, one problem** — Each script solves exactly ONE pain with ONE clear solution. Never cram multiple tools or problems into one video.
- [ ] **4. Show-don't-tell** — Every script includes [SCREEN] cues showing the actual prompt, tool, or output. Screen recordings are the #1 format for educational content.
- [ ] **5. Result first, method second** — Lead with the outcome. Proof-First hooks get 4-7x more impressions when paired with 65%+ 3-second retention.
- [ ] **6. Relatable pain from real people** — The topic came from an actual complaint (Reddit post, X thread, forum), not a hypothetical scenario.
- [ ] **7. Anti-hype tone** — No "AI will change everything." No overselling. Every claim is grounded in a specific person's real experience. Realistic framing builds trust.
- [ ] **8. Series-ready** — Scripts are grouped into themed series of 3-5. Series format grew Harper Carroll 100x. Viewers binge series.
- [ ] **9. Works silent** — 85% watch without sound. Every hook has bold text overlay. Every key point has on-screen text.
- [ ] **10. Under 35 seconds** — Sweet spot is 25-35 seconds. Under 30s for new audiences. Speed implies simplicity — if it can be shorter, make it shorter.
- [ ] **11. Scene changes every 2-4 seconds** — Alternate between [FACE] (talking head) and [SCREEN] (screen recording) to maintain retention.
- [ ] **12. CTA builds funnel** — "Comment [WORD]" format on relevant scripts. Drives DMs → newsletter → community.

**If a script fails any check, rewrite it until it passes.**

---

## Step 4: Select Hook Frameworks

You have **10 proven hook frameworks** with documented performance data. For each script, generate **3 hook variations** using different frameworks. Choose the 3 most relevant — don't force-fit.

### THE 10 HOOK FRAMEWORKS

**Tier 1 — Highest documented performance:**

#### 1. Curiosity Gap / Open Loop
Opens a knowledge gap the brain compulsively needs to close. 70%+ of viral videos use this. "Did you know..." template alone: 22M+ views documented.

**Templates:**
- "I'm about to show you something that [industry] doesn't want you to know."
- "Here's what [experts/pros] use but never share publicly..."
- "Nobody's talking about this, but [surprising claim]..."
- "I found out why [common problem] keeps happening. And it's not what you think."

#### 2. Proof-First / Results Hook
Leads with evidence/outcome. Gets 4-7x more impressions with strong retention. @timdanilovhi earned $1K-7K per Short using this framework consistently.

**Templates:**
- "I [achieved result] in [timeframe]. Here's exactly how."
- "This [tool/method] took us from [before state] to [after state]."
- "[Specific number/metric]. That's what happened when I [did thing]."

#### 3. Pain Point Hook
Mirrors the audience's daily frustration. "3 mistakes everyone makes about X" template: documented 2x engagement vs generic advice.

**Templates:**
- "If you're still [painful manual process] in 2026 — we need to talk."
- "How much time did you waste on [task] this week? Be honest."
- "[Pain point] is costing you [money/time/customers]. Here's how to stop it."

**Tier 2 — Strong performers:**

#### 4. Contrarian / Bold Statement
Challenges assumptions. Forces a pause because the brain wants to resolve the contradiction.

**Templates:**
- "Stop doing [common thing]. Do this instead."
- "[Common advice] is actually terrible advice. Here's why."
- "Everyone says [popular opinion]. They're wrong."

#### 5. "This Cost Me Thousands"
Personal stakes + financial consequences = high engagement. People lean in when real money is on the line.

**Templates:**
- "This one mistake cost me $[amount]. Don't repeat it."
- "I was spending $[amount] a [time period] on [thing] until I found this."

#### 6. The Unexpected Confession
Feels personal and exclusive. Triggers curiosity when someone shares something "they shouldn't."

**Templates:**
- "I probably shouldn't share this, but..."
- "I'm embarrassed it took me this long to figure this out."

#### 7. Question Hook
Creates information gaps. "Have you heard about..." template: 13M+ views, 83% higher comment rates.

**Templates:**
- "How many hours a [time period] do you spend on [task]? What if it was zero?"
- "What do [successful people] all have in common? It's not [obvious thing]."

**Tier 3 — Situational:**

#### 8. Pattern Interrupt (Visual + Audio)
Hijacks attention before conscious decision-making. Works even silent.

**Templates:**
- *[Show the end result FIRST]* + "This took me [short time]. Here's what I did."
- *[Split screen: old way vs new way]* + "Same task. Different century."

#### 9. Before vs After / Transformation
Visually satisfying, shows value instantly. Outperforms specifically on Instagram Reels.

**Templates:**
- "[Before metric] vs [After metric]. Same [person/business]. One change."
- *[Side-by-side comparison]* + "Left: [time ago]. Right: today."

#### 10. Test / Experiment Hook
"What happened" structure creates an open loop. Great for product demos.

**Templates:**
- "I tried [thing] for [time period]. Here's what happened."
- "I tested [number] different [things] to see which one actually works."

#### 11. Question / Challenge Hook
Directly challenges the viewer to confront their own behavior or assumptions. Unlike the Question Hook (#7) which creates information gaps, this one puts the viewer on the spot — it demands self-reflection or issues a dare. Works best when the topic has a clear "you're probably doing this wrong" angle.

**Templates:**
- "Be honest — when's the last time you [did painful manual task]? What if I told you it takes 2 minutes now?"
- "I challenge you to try this for one week. If it doesn't save you [time/money], I'll eat my words."
- "Can you actually explain what your [tool/agency/employee] does for you? Or are you just paying and hoping?"
- "How long are you going to keep doing [manual thing] before you let AI handle it?"

**When to use:** Only when the topic naturally lends itself to calling out a behavior the viewer knows they're guilty of. The challenge must feel earned — backed by a real solution, not empty provocation. Pairs well with Proof-First (challenge → then show the proof) and Pain Point (challenge → then name the specific pain).

### Framework Selection Rules

- **Proof-First** should appear in at least 40% of scripts (highest documented performance)
- **Pain Point** should appear whenever the topic involves a specific frustration
- **Curiosity Gap** works for nearly any topic — use as a reliable fallback
- **Contrarian** works best when challenging common assumptions ("you don't need X")
- **"This Cost Me Thousands"** only when real dollar amounts exist in the research
- **Never use the same 3 frameworks for consecutive scripts** — vary the combinations

### Library Hook Examples (after selecting frameworks)

After selecting 3 frameworks per script, query the Inspiration Library for concrete examples:
- Search for: Type = `Hook Example`, Hook Framework = [each selected framework], Performance Tier IN [Outlier, Strong], limit 2 per framework
- Use returned Hook Text as additional template variants alongside the hardcoded templates above
- This gives you real-world proven hook text to draw from, not just generic templates

---

## Step 5: Script Structure

Every script follows a **screen-first rapid walkthrough** style: Hook → Walkthrough → Result → CTA. No formal "teach" or "punch" sections — the walkthrough IS the punch. The walkthrough IS the teach.

**Style reference:** @noevarner.ai — 319K views, 17.7K likes on a 31-second Claude Code tutorial. Ultra-casual, rapid-fire, screen-first.

### Visual Direction Tags

Use these inline tags to indicate camera direction:
- **[FACE]** — Talking head, camera on creator
- **[SCREEN]** — Screen recording showing the actual tool/prompt/output

**Default split: 90-95% [SCREEN], 5-10% [FACE].** Face appears at most twice — optionally at the hook and/or the close. The screen recording IS the content. Speed implies simplicity.

**Text overlays go in a separate section at the bottom of each script** (not inline). This keeps the script body clean and readable as a filming guide.

### Platform Timing

| Platform | Hook Window | Total Length | Energy |
|---|---|---|---|
| TikTok | 2 seconds MAX | 15-30 seconds | 20% higher than normal |
| Reels | 3 seconds | 25-35 seconds | Casual but fast |
| Shorts | 3-5 seconds | 25-35 seconds | Structured storytelling |

### Script Template

```
## SF #{N} - {Title}

**Platform:** {Platform} | **Target:** {length} seconds | **Tone:** {Tone description}
**Style Reference:** {Creator or style inspiration if applicable}

---

**HOOK A ({Framework Name}):**
[SCREEN] {Hook text — must land within 2-3 seconds}

**HOOK B ({Framework Name}):**
[SCREEN] {Alternative hook for A/B testing}

**HOOK C ({Framework Name}):**
[FACE] {Third variation — face hooks are the exception, not the default}

---

**SCRIPT (Hook A version — full walkthrough):**

[SCREEN] {Hook line repeated — this is the actual filming script}
[SCREEN] {Step 1 — show the action, narrate over it. "Open this. Type this."}
[SCREEN] {Step 2 — keep moving fast. No pauses, no reflections.}
[SCREEN] {Step 3 — show the tool working. Let the screen do the talking.}
[SCREEN] {Step 4 — show the result/output. This IS the payoff.}
[SCREEN] {Step 5 — show the final deliverable if there is one.}
[FACE] {Quick confident close — 1 sentence max. "You're welcome." / "That's it." / "Three minutes. Zero retainer."}

**CAPTION:** {Short caption — 1-2 sentences + CTA ("Comment [WORD] and I'll send you [specific thing]") + hashtags}

---

**TEXT OVERLAYS:**
[0:00] **{Bold hook text — the core claim}**
[0:03] {Step or action}
[0:06] {What the tool is doing}
[0:09] {Key stat or result}
[0:12] {Another result or proof point}
[0:15] {More results — keep stacking}
[0:20] {Final deliverable or transformation}
[0:25] **{Punchy close — mirrors the hook's energy}**

---

**Production Notes:**

### Why This Script Works
{2-3 bullets explaining what makes this specific script effective — reference the research source, the hook framework choice, and what makes it filmable.}

### Filming
{Script-specific filming instructions — what to screen record, where face appears, voiceover approach, cut style.}
```

### Script Template Rules

- **The full walkthrough IS the script.** Write it as one continuous voiceover you'd read while screen recording. No section headers during the walkthrough — just [SCREEN] and [FACE] tags with the actual words.
- **Hooks are listed separately above** the walkthrough for A/B testing, but the walkthrough itself uses Hook A as the opening by default.
- **One face moment max** during the walkthrough — at the close. The rest is screen recording with voiceover.
- **Speed over polish.** Write like you're showing a friend something cool, not delivering a lecture. "First do this. Then this. Now watch — it just does the whole thing by itself."
- **No filler transitions.** No "Now here's where it gets interesting" or "But wait, there's more." Just next step, next step, result.
- **Production Notes are per-script.** Each script gets its own notes explaining why it works and how to film it — not a generic section at the end of the batch.

### Text Overlay Rules
- Timestamps are approximate — adjust based on actual script pacing
- Every section of the script should have at least one overlay (85% watch silent)
- Keep each overlay to 5-8 words max — readable at a glance
- The first overlay [0:00] should appear immediately and match the core claim
- Overlays every 2-3 seconds (faster than before — matches rapid-fire pacing)
- Use overlays to reinforce key numbers, results, and the CTA

---

## Step 6: Group Into Series

After writing all scripts, organize them into **themed series of 3-5 scripts each**.

### Why Series Matter

- Harper Carroll's "10 Days of AI Basics" series grew her from 2K to 200K followers in 3 weeks
- Series create binge behavior — viewers watch one and seek out the rest
- Algorithm rewards accounts that keep viewers on-platform longer
- Series give you a posting cadence: "Day 1 of [series name]" builds anticipation

### Series Naming Format

```
**"[Series Name]"** series: SF #{N}, #{N}, #{N}, #{N}
```

Choose series names that:
- Work as hashtags
- Sound like a mini-course viewers want to complete
- Are specific enough to set expectations ("AI for Service Businesses" not "AI Tips")

---

## Step 7: Output Format

### Document Header

```
# {TOPIC} — {COUNT} Short-Form Video Scripts
### Built from {N} real pain points sourced from {sources summary}
### Every script scored against 12-Point Outlier Content Checklist
### Style: Screen-first rapid walkthrough | Hook (3 variations) → Walkthrough → Result → CTA

---
```

### Scripts

Output all scripts using the template from Step 5. Each script is self-contained — it includes its own hooks, full walkthrough, text overlays, and production notes.

### Series Groupings

After all scripts:

```
## Series Groupings

- **"[Series Name]"** series: SF #{list}
- **"[Series Name]"** series: SF #{list}
- ...
```

---

## Step 8: Offer Next Steps

End with:

```
---
Want me to:
- Write word-for-word teleprompter scripts for any of these?
- Generate more scripts for a different pain point?
- Create a posting calendar / content schedule?
- Research a new topic with /last30days and build a fresh batch?
- Rewrite any script with a different angle or tone?
- Refresh an existing script with new hooks from your library?
- Regenerate a hand raiser PDF with a different format?

Hand raisers have already been generated and uploaded for every script above.
Just tell me what you need.
```

**Update Library:** After push to production, if any Inspiration Library entries were referenced during script creation, update their `Last Used` date to today using `notion-update-page`.

**Auto-push (MANDATORY):** After writing any script — whether a full batch, a single script, or a one-off request — ALWAYS automatically push to ALL destinations without asking. Do not offer or prompt — just do it. Every step below is mandatory.

1. **Google Doc:** Save script to a temp file, then push via `cd ~/.claude/skills/scripts && python3 gdocs_push.py --title "SF #{N} - {Title}" --content-file "{TEMP_FILE}" --folder-id "{FOLDER_ID}"`. Read folder ID from `~/.config/gdocs/config.json`. Capture the doc URL from stdout.
2. **Hand Raiser PDF:** For EVERY script in the batch, auto-generate a hand raiser PDF.
   - Read the hand-raiser skill (`~/.claude/skills/hand-raiser/skill.md`) for the full flow
   - For each script: generate content JSON based on the script's topic/CTA/pain point → render PDF via `cd ~/.claude/skills/scripts && python3 pdf_generator.py --content-file "{JSON}" --output "~/ai-content-system/output/hand-raisers/SF{N}-{kebab-title}.pdf"` → upload to Drive via `cd ~/.claude/skills/scripts && python3 gdrive_upload.py --file "{PDF}" --subfolder "Hand Raisers"` → capture the Drive URL from stdout
   - Auto-detect PDF type per script (setup-guide for install scripts, cheatsheet for tips/commands, how-to-guide for tutorials, checklist for audits)
3. **Vercel Landing Page:** For EVERY script, create a lead-capture landing page for the hand raiser.
   - Create a resource markdown file at `~/ai-content-system/lead-pages/src/content/resources/{kebab-title}.md`
   - Frontmatter must match this schema exactly:
     ```yaml
     title: "{Script Title}"
     headline: "{Compelling headline matching the script's core promise}"
     subtitle: "{1-2 sentence description of what the PDF delivers}"
     pdfUrl: "{Google Drive URL of the hand raiser PDF from step 2}"
     valueProps:
       - "{Value prop 1 from the PDF content}"
       - "{Value prop 2}"
       - "{Value prop 3}"
       - "{Value prop 4 — include a real stat/number}"
     ctaText: "Get the Free Guide"
     previewDescription: "{1 sentence summary of the PDF for meta/preview}"
     pages: {page count of the PDF}
     type: "{one of: guide, cheatsheet, checklist, quick-reference, how-to-guide}"
     ```
   - After frontmatter, write 2-4 paragraphs of markdown body: "What's Inside" section with bold key points, plus a "Who this is for" section. Ground this in the script's pain point and CTA promise.
   - Commit and push: `cd ~/ai-content-system/lead-pages && git add src/content/resources/{kebab-title}.md && git commit -m "Add {title} landing page (SF #{N})" && git push origin master`
   - The live URL will be: `https://YOUR_VERCEL_DOMAIN/{kebab-title}`
4. **Notion:** Read `~/.config/notion-content/config.json` to get `script_library_db_id`. Create a page in Script Library using `notion-create-pages` with `data_source_id` set to the value of `script_library_db_id` from config. Include: Script Title, Status = `Scripts`, Topic, Script Number, Hook Framework A/B/C, Platform, Series, Batch, Google Doc URL (from step 1), Hand Raiser URL (Drive URL from step 2), Hand Raiser Page (Vercel URL from step 3), Pain Point Source, and Notes. Add Script Preview as page content.
5. **Report:** Tell the user all links after pushing:
   - Google Doc URL
   - Hand Raiser PDF (Drive URL)
   - Hand Raiser Landing Page (Vercel URL)
   - Notion confirmation

---

## FOLLOW-UP BEHAVIOR

**If user says "write a teleprompter script for #X":**
- Write exact word-for-word script with timing markers (e.g., [0:00-0:03], [0:03-0:08])
- Include exact on-screen text for each section
- Include visual direction for every moment (what to show, what to do)
- Include 3 hook variations
- Include suggested post caption and hashtags

**If user says "more scripts" or "add more":**
- Research additional pain points for the same topic
- Write new scripts that don't overlap with existing ones
- Add to the series groupings

**If user provides an existing file to rewrite:**
- Read the file
- Identify which scripts pass the outlier checklist and which don't
- Rewrite failing scripts to pass all 12 checks
- Add 3 hook variations to any script that only has 1 hook
- Add [SCREEN] and [FACE] tags if missing
- Group into series if not already grouped

**If user provides pain points directly:**
- Skip the research step
- Score each pain point against the outlier checklist for viability
- Write scripts for the viable ones
- Flag any that are too vague or unsolvable and suggest alternatives

**If user says "refresh SF #N" or "new version of #N":**
This is the library-aware refresh flow. Handle it inline:

1. **Fetch the original** — Read `~/.config/notion-content/config.json` to get `script_library_db_id`. Query Script Library by Script Number using `notion-search` with `data_source_url` set to `collection://{script_library_db_id}`. Get full page (properties + body).
2. **Query library for new inspiration** — Read config to get `inspiration_data_source_id`. Search Inspiration Library for:
   - Same Topic Tags as the script
   - Performance Tier IN [Outlier, Strong]
   - Prioritize entries added AFTER the script was created (newer = material the script couldn't have used)
   - Up to 10 results
3. **If library entries have video Source URLs**, offer to pull transcripts using `/transcript` skill (`~/.claude/skills/transcript/skill.md`) for deeper hook analysis.
4. **Generate 2-3 variations:**
   - **Hook Refresh** — same body/teach/punch, 3 brand new hooks from library examples
   - **Angle Shift** — same pain point, different approach inspired by a library Creator Pattern
   - **Full Rewrite** — only if 3+ new library entries exist since the original; same topic, completely new script
5. **Show diff** — clearly mark old vs new for each variation. Cite which library entries inspired each change.
6. **Offer to save** — if user picks a winner, push to Google Docs + Notion as next Script Number. Update Last Used on referenced library entries.

If no new library data exists since the script was created, say so: "No new library data since this script was written. Want me to rewrite it from scratch using the existing patterns instead?"

**If user says "new hooks for SF #N" (hook swap only):**
Lightweight version — only replace the 3 hooks:

1. Fetch original script from Script Library
2. Query Inspiration Library for Hook Examples matching the script's topic, Performance Tier IN [Outlier, Strong]
3. Generate 3 new hooks using different frameworks than the originals
4. Show old vs new side by side, cite library sources
5. If approved, update Notion page with new Hook Framework A/B/C values

**If user asks about strategy:**
- Answer from baked-in research — no new searches needed
- Key stats:
  - 85% watch without sound
  - 71% decide in first 3 seconds
  - 65%+ 3-second retention = 4-7x more impressions
  - Authentic content performs 60% better than overproduced
  - Series format grew Harper Carroll from 2K → 200K in 3 weeks
  - One hook format repeated with tweaks = 60M views (@ogilichev)
  - Proof-First hooks with specific numbers consistently outperform generic hooks
  - Scene changes every 2-4 seconds maintain retention
  - "Comment [WORD]" CTAs drive 3-5x more DMs than generic CTAs

---

## RESEARCH SOURCES (baked in)

This skill is grounded in research from Feb 2026:

### Hook Frameworks
- **Reddit** (4 threads, 23 upvotes, 18 comments): r/SocialMediaMarketing, r/Instagram, r/contentcreation, r/AI_UGC_Marketing
- **X** (14 posts, 16,433 likes, 1,497 reposts): @signulll (13.4K likes), @timdanilovhi (355 likes), @vidIQ (860 likes), @maubaron (375 likes), @slic_media
- **Web** (10+ pages): CreatorsJet, OpusClip, VirVid.ai, SendShort, MarketingBlocks, Buffer, Brandefy, vidIQ

### Outlier Content Patterns
- **Creators analyzed**: Harper Carroll (400K followers in 13 months), Matt Wolfe (857K subs, 65.5M views), Vaibhav Sisinty (1M Instagram), Riley Brown, Rachel Woods, Rowan Cheung, Liam Ottley, Igor Pogany, Noe Varner, The AI Advantage
- **X** (35 posts, 8K+ likes): @seergioo_gil (12M views), @linaa_ai (11.7M views/$16.7K), @heyfionaai (22M/12M/11M per video), @wanneracademy (outlier scoring method), @ogilichev (60M views)
- **Viral templates documented**: "Did you know..." (22M+ views), "Top 3 shocking facts" (6M+), "3 mistakes everyone makes" (2x engagement), "Have you heard about..." (13M+, 83% higher comments)
- **Outlier Score**: Views / Account Median Views. Filter: 3X+ multiplier, 100K+ views (from Shortimize + @wanneracademy)

### Pain Point Research (for "AI for business owners" topic)
- **Reddit** (6 threads, 171 upvotes, 106 comments): r/smallbusiness, r/Entrepreneur
- **X** (35 posts, 8K+ likes): @WorkflowWhisper, @businessbarista, @hamza_automates, @bprintco, @levelsio, @BrockHBriggs
- **Web** (15+ pages): BuildOps research, business automation surveys, SaaS case studies

### 9 Creator Content Patterns (from deep analysis)
1. **Translator positioning** — Position yourself as the bridge between complex tech and normal people
2. **Series explosion** — Group content into themed series (10 Days of X, AI Money Saver, etc.)
3. **Content cadence** — Post 5-7x/week minimum for algorithmic momentum
4. **Show-don't-tell screen recording** — Screen recordings of actual tools > talking about tools
5. **Anti-hype tone** — Calm, realistic framing beats hype. "This saved me 3 hours" not "THIS CHANGES EVERYTHING"
6. **One tool, one problem** — Never cram multiple solutions into one video
7. **Viral format copying** — Find a format that works, repeat it with tiny tweaks (60M views from one format)
8. **Hook archetype matching** — Match hook framework to content type (Proof-First for tutorials, Pain Point for awareness)
9. **Education → newsletter → course funnel** — Content drives followers, CTA drives DMs, DMs drive email list, email drives product
