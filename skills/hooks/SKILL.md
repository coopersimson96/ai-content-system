---
name: hooks
description: >
  Generate high-converting short-form video hooks and scripts for any niche.
  Uses 12 proven frameworks with documented viral performance data, a 100-point
  4-dimension grading rubric, and outlier content principles. Includes pre-flight
  checks for triple-stacked hooks, Zeigarnik open-loops, outcome-over-audience
  framing, and B/A vs open-loop framework choice. Triggers on: "hooks", "hook
  variations", "write me a hook", "TikTok hook", "Reels hook", "Shorts hook".
argument-hint: "[topic/product] for [audience]" or describe what you're creating content about
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebSearch
---

# Short-Form Video Hook & Script Generator

Generate copy-paste-ready hooks and full scripts for TikTok, Reels, and YouTube Shorts. Grounded in 12 proven frameworks, a hard scoring rubric, and the retention principles documented across hundreds of posted scripts.

---

## Step 1: Parse the Input

Extract from `$ARGUMENTS`:

1. **TOPIC** - What is the content about?
2. **AUDIENCE** - Who is the target viewer?
3. **PLATFORM** - TikTok, Reels, Shorts, or all? (default: all)
4. **TONE** - Professional, casual/raw, humorous, educational? (default: casual/raw)
5. **ANGLE** - Any specific angle? (e.g., pain point, before/after, confession)
6. **FORMAT** - Hook variations only, full scripts, or both? (default: both)

If TOPIC is missing, ask:

> What's the content about and who's it for?

If only TOPIC is provided, infer a reasonable AUDIENCE and proceed. Don't over-ask.

---

## Step 2: Select and Apply Hook Frameworks

You have **12 proven hook frameworks**. For each piece of content, generate **3 hook variations** using different frameworks. Choose the 3 most relevant to the topic. Don't force-fit frameworks that don't match.

### Framework Selection Rules

- **Pain Point** is the default driver. Use whenever the topic involves a specific frustration.
- **Curiosity Gap** works for nearly any topic. Reliable fallback.
- **Negative Delta / "Tired of seeing"** is the strongest opener for "you're doing this wrong" angles. Promote when the topic has visible social proof making the viewer feel left behind.
- **Contrarian** works best when challenging common assumptions ("you don't need X").
- **Unexpected Confession** is strong for personal-story openers and walkthrough scripts.
- **"This Cost Me Thousands"** only when real dollar amounts or consequences exist.
- **Question / Challenge** when the topic naturally calls out a behavior the viewer is guilty of.
- **Outcome > audience callouts.** Never write a hook that names a job/role being killed ("UGC creators are cooked", "designers are done"). Reframe around the OUTCOME that's now possible. Tool/process kills work ("Claude killed Premiere Pro"). Role kills get throttled by the algorithm because only the affected role watches.
- **Proof-First reads like a guru pitch.** Default to Pain Point, Negative Delta, Curiosity Gap, or Confession. Use Proof-First only when (a) no other framework fits, AND (b) there's a hard dollar/metric anchor from real research, AND (c) you note in grading commentary why it was the only viable fit.
- **Never use the same 3 frameworks for consecutive scripts.** Vary the combinations.

### Library Hook Examples (optional)

Before generating, check if your config (see `config-templates/notion-content-config.json.example`) has `inspiration_data_source_id`. If so, query the Inspiration Library for hooks matching the selected frameworks (Type = `Hook Example`, Performance Tier IN [Outlier, Strong], limit 2 per framework). Use returned Hook Text alongside the templates below. If 0 results or config missing, proceed silently with templates only.

### The 12 Hook Frameworks

---

### 1. Curiosity Gap / Open Loop
**Why it works:** Opens a knowledge gap the brain compulsively needs to close. 70%+ of viral videos use this in the first 3 seconds.
**Documented performance:** "Did you know..." template: 22M+ views. "Have you heard about..." template: 13M+ views, 83% higher comment rates.

**Templates:**
- "I'm about to show you something that [industry] doesn't want you to know."
- "Here's what [experts/pros] use but never share publicly..."
- "Nobody's talking about this, but [surprising claim]..."
- "I found out why [common problem] keeps happening. And it's not what you think."
- "[Number] things about [topic] that will change how you [action]."
- "Did you know that [surprising fact]..."
- "Have you heard about [thing]..."

**Best for:** Educational content, reveals, insider knowledge, myth-busting.

---

### 2. Proof-First / Results Hook
**Why it works:** Leads with evidence/outcome, then explains how. Establishes credibility immediately. Gets 4-7x more impressions when paired with 65%+ 3-second retention.
**Caveat:** Reads like a guru pitch. Use sparingly.

**Templates:**
- "I [achieved result] in [timeframe]. Here's exactly how."
- "This [tool/method] took us from [before state] to [after state]."
- "[Specific number/metric]. That's what happened when I [did thing]."
- "My [client/friend/colleague] [achieved result] using this one [trick/method/tool]."

**Best for:** Case studies, tutorials, product demos, outcome-focused content.

---

### 3. Pain Point Hook
**Why it works:** Speaks directly to what the audience is frustrated about. Resonates instantly because it mirrors their daily experience.
**Documented performance:** "3 mistakes everyone makes about X" template: 2x engagement vs generic advice hooks. "Top 3 shocking facts" template: 6M+ views.

**Templates:**
- "If you're still [painful manual process] in 2026 - we need to talk."
- "Struggling with [specific problem]? Here's the fix."
- "The #1 reason [audience] fail at [goal]? [Pain point]."
- "How much time did you waste on [task] this week? Be honest."
- "[Pain point] is costing you [money/time/customers]. Here's how to stop it."

**Best for:** Problem-aware audiences, how-to content, product introductions.

---

### 4. Contrarian / Bold Statement
**Why it works:** Creates cognitive dissonance. Forces a pause because the brain wants to resolve the contradiction.

**Templates:**
- "Stop doing [common thing]. Do this instead."
- "[Common advice] is actually terrible advice. Here's why."
- "Everyone says [popular opinion]. They're wrong."
- "[Common practice] is keeping you [stuck/broke/behind]. Here's what works."
- "The worst thing you can do for [goal] is [thing everyone does]."

**Best for:** Hot takes, challenging norms, positioning as authority.

---

### 5. The Unexpected Confession
**Why it works:** Feels personal and exclusive. Triggers curiosity because people lean in when someone shares something "they shouldn't."

**Templates:**
- "I probably shouldn't share this, but..."
- "I've been doing [thing] for [time] and nobody noticed. Here's how."
- "I'm embarrassed it took me this long to figure this out."
- "OK I wasn't going to post this but [reason]..."
- "This is the [thing] I wish someone told me [timeframe] ago."

**Best for:** Personal stories, behind-the-scenes, building trust.

---

### 6. "This Cost Me Thousands"
**Why it works:** Personal stakes plus financial/emotional consequences. People lean in when real money is on the line.

**Templates:**
- "This one mistake cost me $[amount]. Don't repeat it."
- "I was spending $[amount] a [time period] on [thing] until I found this."
- "This mistake nearly [ruined/cost/destroyed] my [business/project]."
- "I wasted [time/money] on [thing] before I figured out [solution]."

**Best for:** Cautionary tales, money-saving tips, business advice.

---

### 7. Pattern Interrupt (Visual + Audio)
**Why it works:** Hijacks attention before conscious decision-making. Exploits the brain's wiring to notice anything that breaks expected flow.

**Templates:**
- *[Abrupt camera movement / unexpected prop / sound effect]* + bold text overlay with core claim
- *[Split screen: old way vs new way]* + "Same task. Different century."
- *[Show the end result FIRST]* + "This took me [short time]. Here's what I did."
- *[Hand slam / Post-It reveal / glitch cut]* + "[Bold claim]"
- *[Start mid-action or mid-sentence]* - no intro, no warm-up

**Best for:** Energy-driven content, demos, transformation reveals. Works even silent.

---

### 8. Before vs After / Transformation
**Why it works:** Visually satisfying. Outperforms specifically on Reels because it aligns with the platform's aspirational culture.

**Templates:**
- *[Show messy before state]* -> *[Cut to clean after state]*
- "[Before metric] vs [After metric]. Same [person/business]. One change."
- "What [task] looked like before: [pain]. What it looks like now: [ease]."
- *[Side-by-side comparison]* + "Left: [time ago]. Right: today."
- "6 months ago I was [struggling state]. Now I [thriving state]. Here's the one thing I changed."

**Best for:** Visual content, product demos, fitness, design, workflow improvements.

---

### 9. Question Hook
**Why it works:** Creates information gaps the brain wants to close. Best when hyper-specific to audience pain.

**Templates:**
- "Why do some [audience members] [succeed] while others [fail]?"
- "What if I told you [surprising fact about their daily reality]?"
- "Can you [do simple thing]? Then you can [do impressive thing]. Here's proof."
- "How many hours a [time period] do you spend on [task]? What if it was zero?"

**Best for:** Educational content, addressing knowledge gaps.

---

### 10. Test / Experiment Hook
**Why it works:** Curiosity through relatability and suspense. The "what happened" structure creates an open loop.

**Templates:**
- "I tried [thing] for [time period]. Here's what happened."
- "Watch what happens when I [do unexpected thing]."
- "I tested [number] different [things] to see which one actually works."
- "I gave [tool/method] to [person] with zero experience. The results surprised me."

**Best for:** Product reviews, tutorials, suspense-driven content.

---

### 11. Question / Challenge Hook
**Why it works:** Puts the viewer on the spot. Demands self-reflection or issues a dare. Pairs naturally with Pain Point.

**Templates:**
- "Be honest - when's the last time you [did painful manual task]? What if I told you it takes 2 minutes now?"
- "I challenge you to try this for one week. If it doesn't save you [time/money], I'll eat my words."
- "Can you actually explain what your [tool/agency/employee] does for you? Or are you just paying and hoping?"
- "How long are you going to keep doing [manual thing] before you let AI handle it?"

**Best for:** Topics where the audience knows they're guilty of a behavior. The challenge must feel earned, backed by a real solution.

---

### 12. Negative Delta / Contrast Pivot
**Why it works:** Instead of just showing the positive outcome (0 to +100), you first take the viewer negative ("most people are doing it wrong") then pivot with "but" to the solution. Doubles the emotional range. The word "but" creates the pivot that makes the payoff feel twice as large.
**Documented performance:** Chris Chung studied 1,832 viral reels and found the top 1% use this negative-to-positive delta pattern.

**Templates:**
- "[Audience] [do painful thing] every single time. But you only need to [solution] once. Here's how."
- "Most people [wrong approach]. But if you [right approach], [specific result]."
- "[Common behavior] is wasting your [time/money]. But it's only because [reframe]. Let me show you."

**"Tired of seeing" variant (strongest for non-technical audiences):**
- "If you're tired of seeing people [achieve result] but every time you try, [specific pain 1] or [specific pain 2]. It's not you. You're just missing [number] [free tools/steps]. Let me show you."

**Why this variant works:** "Tired of seeing" implies built-up frustration. Dual specific pains make the viewer nod twice. "It's not you" shifts blame from viewer to tools. The numbered resolution removes the cost objection immediately.

**Best for:** Educational content, tool demos, "you're doing it wrong" angles. Pairs naturally with Proof-First.

---

## Step 2.4: Pre-flight Checklist (Mandatory Before Grading)

Four yes/no checks every hook must pass before grading. Failures get rewritten, not graded. These cover retention principles the verbal rubric cannot measure.

**1. Triple-stack alignment (sec 0).** Do the text overlay, visual hook, and verbal hook all carry the same core claim at second 0? The April 2026 IG algorithm collapsed signal to hook retention plus skip rate. If the three layers diverge, retention drops below 50% and distribution dies.
- Check: the `[TEXT OVERLAY: ...]` line, the first `[SCREEN: ...]` tag, and the SELECTED hook line. Same claim, or rewrite.

**2. Outcome > audience callout.** Does the hook name a job/role being killed? If yes, reframe around the OUTCOME the viewer can now achieve. Tool/process kills work ("Claude killed Premiere Pro"). Role kills get throttled.
- Bad: "Designers are done." Good: "You can now ship a full design system from one prompt."

**3. Open-loop / Zeigarnik tease.** Is the kicker teased or revealed? Hooks that resolve in the first sentence get scrolled. Hooks that open a loop force completion.
- Listicles: tease the surprising item ("the 5th is the most underrated").
- Tutorials: lead with outcome but withhold mechanism until the body.
- Confessions: put the resolution at the end, not the middle.

**4. Inspo-not-structure.** If inspired by a specific reel/post, does this hook copy the inspo's flow or phrasing? Use inspo for TOPIC and ANGLE only. Rewrite from your own perspective with your own personal experience and use cases.

**Output requirement:** Print a 4-row PASS/FAIL checklist before the grading table. Fix any failures and re-run before grading.

```
PRE-FLIGHT CHECKLIST
[ ] 1. Triple-stack aligned
[ ] 2. Outcome-framed (no role kill)
[ ] 3. Open-loop teased
[ ] 4. Inspo for topic only
```

---

## Step 2.5: Hook Grading (MANDATORY before shipping)

**Every hook variation gets scored on a 100-point rubric before it ships.** This prevents subjectively picking weak hooks that "feel good" but underperform. A scored comparison table appears in the conversation for every hook output.

### The 4-Dimension Rubric (25 points each)

**1. Scroll Stop (0-25)** - Do the first 5 words stop the scroll?
- 23-25: Command verb / dollar-authority lead / cognitive dissonance at word 1 ("Stop...", "You need to...", "Enterprise clients pay six figures...")
- 18-22: Strong curiosity opener, recognizable pattern ("Most people don't know this but...", "I don't think X meant to release this.")
- 13-17: Standard opener, no pattern interrupt ("Here's how to...", "Today I'll...")
- 0-12: Generic or hookless ("So recently I...", "Let me tell you...")

**2. Word Economy (0-25)** - Info density per word
- 23-25: <=20 words
- 19-22: 21-30 words
- 14-18: 31-40 words
- 0-13: 41+ words

**3. Pattern Interrupt (0-25)** - Fresh verb choice and structure
- 23-25: Sensational verb + cognitive dissonance ("leaked", "dropped", "gave away", "pay X for free")
- 18-22: Sensational verb but recognizable structure ("just dropped", "just leaked")
- 13-17: Neutral verbs ("released", "announced", "launched")
- 0-12: Corporate language ("introduces", "unveils", "brings us")

**4. Authority Pack (0-25)** - Credibility per word
- 23-25: 2-3 specific authority signals (named brand + specific number + specific group)
- 18-22: 2 authority signals with at least one specific
- 13-17: 1 authority signal
- 0-12: Vague authority ("experts say", "many people", "the pros")

### Benchmark Anchors (for calibration)

| Hook | Tier | Score |
|---|---|---|
| "You need to pay attention because Claude is giving away a free AI certification that Deloitte is paying thousands of employees just to get" (Raycfu) | Outlier | 95 |
| "3 Hidden resources you don't want to miss" (@harshhhgautam, 2.47M views) | Outlier | 92 |
| "Github name is in the pinned comment" (@tenfoldmarc, 438K views) | Outlier | 88 |
| "Stop typing random prompts into Claude and hoping for the best" (@mattymoe.ai) | Strong | 84 |

At grading time, query the Inspiration Library (if configured) for Performance Tier = Outlier, Type = Hook Example, topic-matched, for fresher benchmarks.

### Tier Gates (Hard Rules)

- **88-100 (Outlier):** Ship it.
- **78-87 (Strong):** Ship it. Note weakest dimension for future.
- **68-77 (Above Average):** Iterate one more round. Target the weakest dimension.
- **<68:** REJECT. Do not ship. Rewrite and re-grade.

### Common Weakening Patterns (Flag These)

| Weakness | Fix |
|---|---|
| Soft verbs: "released", "announced", "introduces", "launched" | Replace with "leaked", "dropped", "gave away", "just dropped" |
| Vague authority: "enterprise clients", "big companies", "top experts" | Replace with "Fortune 500", "Deloitte", "YC founders", named brands |
| Awkward repetition: "users use", "follow followers" | Restructure |
| Softener phrases: "for this training", "for this course" | Cut them |
| Corporate language: "leverage", "utilize", "empower" | Replace with plain-English verbs |
| Missing specific number | Add one: "Fortune 500", "six figures", "10 rules" |

### Iteration Heuristic (When Below Tier Gate)

- **Word Economy < 18:** Cut to <=30 words. Target repeating info.
- **Pattern Interrupt < 18:** Swap soft verbs. Swap vague authority for specific names.
- **Authority Pack < 18:** Add a specific named entity, number, or group.
- **Scroll Stop < 18:** Try a command verb opener ("Stop", "Watch", "You need to") or lead with a dollar/authority anchor.

### Conversational Glue Rule

Pure-staccato hooks score 92-93 on the rubric but read robotic when spoken. Add light glue (subjects, "and got back" connectors, verbs on fragments) for natural delivery. Trades 1-2 Word Economy points but stays in Outlier tier. Verbal cadence beats absolute Word Economy when filming.

### B/A vs Open-Loop Framework Choice

When the script has a real visual transformation AND the CTA aligns with a clear mechanism anchor (one prompt, one tool, one command), choose **Before/After**. The mechanism anchor IS the comment magnet, so the open loop is implied.

When there's no natural mechanism AND the body has binge structure (listicle, multi-step reveal), choose **Open-Loop**. Tease the kicker, never resolve in the hook.

Don't stack both: an open-loop hook on top of a B/A body fights itself.

### Visual Hook Scoring (Separate Layer)

The 4-dimension verbal rubric cannot score visual show-don't-tell. Hooks with `from this [SCREEN: messy] to this [SCREEN: clean]` baked into sec 0 outperform higher-scoring verbal-only alternatives. When ranking, factor visual layer in separately:

- Verbal hook tier (88+, 78-87, 68-77, <68)
- Visual hook bonus (+5 if a real before/after or scroll-stopping screen lands at sec 0)

A 90-verbal hook with strong visual beats a 93-verbal hook that's a static talking head.

### Overlay Text Must Match Spoken Hook

Recurring failure mode: the spoken hook is a personal confession but the [0:00] text overlay flips to plural role-kill ("UGC creators are cooked"). The overlay gets graded on the same outcome-over-audience rule as the spoken hook. Same claim across spoken + overlay + first screen, or rewrite.

### Mandatory Output Format

After generating variations, show a scored comparison table like this:

```
| Variation | Words | Scroll | Economy | Interrupt | Authority | Total | Tier |
|---|---|---|---|---|---|---|---|
| A | 22 | 19 | 20 | 22 | 23 | 84 | Strong |
| B | 17 | 22 | 24 | 22 | 22 | 90 | Outlier |
```

Recommend the highest-scoring variation as SELECTED (factoring in the visual bonus). If you override the top score for a vibe reason or visual layer, flag the trade-off explicitly.

**Failure mode:** If hooks ship without a scored comparison table, the grading step was skipped.

---

## Step 3: Script Structure

Every script follows the universal **Hook -> Body -> Teach -> Punch -> CTA** structure.

### Visual Direction Tags

Every full script MUST include these tags:
- **[FACE]** - Talking head, camera on creator
- **[SCREEN]** - Screen recording showing the actual tool/prompt/output (the #1 format for educational content)
- **[TEXT OVERLAY: ...]** - Bold on-screen text (required - 85% watch without sound)

Alternate between [FACE] and [SCREEN] every 2-4 seconds in the body.

### Tone Principles

- **Anti-hype by default.** No "AI will change everything." Every claim should be grounded in a specific person's real experience.
- **One tool, one problem per script.** Never cram multiple tools or problems into one video.
- **Specific numbers beat vague claims.** "3 hours -> 5 minutes" beats "saves you time."
- **Real examples > generic advice.** A bakery owner's story beats "businesses can use AI."

### Platform Timing

| Platform | Hook Window | Energy Level | Total Length Sweet Spot |
|---|---|---|---|
| TikTok | 2 seconds MAX | 20% higher than normal | 15-30 seconds |
| Reels | 3 seconds | Polished but authentic | 15-45 seconds (under 30 for new audiences) |
| Shorts | 3-5 seconds | Structured storytelling | 15-35 seconds |

### Script Template

```
**[TEXT OVERLAY: {Bold, short text that captures the core claim}]**

**HOOK A ({Framework Name}):**
{The spoken/on-screen hook - must land within 2-3 seconds}

**HOOK B ({Different Framework Name}):**
{Alternative hook for A/B testing}

**HOOK C ({Different Framework Name}):**
{Third variation}

**BODY:**
{[SCREEN] and [FACE] tagged. Core content. Scene changes every 2-4 seconds.}

**TEACH:**
{The insight, lesson, or proof. Real examples > generic advice.}

**PUNCH:**
{Memorable closing line - quotable, shareable, hits hard.}

**CAPTION:**
{Line 1: Bold claim or hook - one sentence max}

{Comment "[WORD]" for the [deliverable]}

{5 hashtags: #ai #[topic] #[topic] #[category] #[category]}
```

### Dual CTA Stack

Default close for walkthrough/listicle scripts:

> "Save this video and send it to anyone who [pain]. And if you want my breakdown on how to do this yourself comment [WORD], or if you want to copy my exact system click the link in my bio."

The two CTAs don't compete. Comment WORD = "I'm interested but want a free sample first" (warm). Bio link = "I'm sold" (hot). Order matters: comment first (warm), bio link second (hot). Reversed feels salesy.

**Short reactive / one-off (single-CTA fallback):**

> "Save this video and if you want [specific thing] comment [WORD] and I'll send it to you."

Don't stack 3+ value props before the CTA. Two CTAs is the cap.

---

## Step 4: Output Format

```
# {NUMBER} Hooks for: {TOPIC} -> {AUDIENCE}
Platform: {PLATFORM} | Tone: {TONE}

---

## SCRIPT {N} - {Title}

**[TEXT OVERLAY: {Bold text}]**

**HOOK A ({Framework}):** {Hook text}
**HOOK B ({Framework}):** {Hook text}
**HOOK C ({Framework}):** {Hook text}

PRE-FLIGHT CHECKLIST
[ ] 1. Triple-stack aligned
[ ] 2. Outcome-framed (no role kill)
[ ] 3. Open-loop teased
[ ] 4. Inspo for topic only

| Variation | Words | Scroll | Economy | Interrupt | Authority | Total | Tier |
|---|---|---|---|---|---|---|---|
| A | ... | ... | ... | ... | ... | ... | ... |
| B | ... | ... | ... | ... | ... | ... | ... |
| C | ... | ... | ... | ... | ... | ... | ... |

SELECTED: {Variation} - {reason, including visual bonus if applicable}

**BODY:** {Body text with [FACE] and [SCREEN] tags}

**TEACH:** {Teach text}

**PUNCH:** {Punch text}

**CAPTION:**
{Line 1: Bold claim or hook - one sentence max}

{Comment "[WORD]" for the [deliverable]}

{5 hashtags}

---
```

---

## Step 5: Production Tips

### Filming
- **Silent-first:** 85% watch without sound. Every hook needs bold on-screen captions.
- **3-second rule:** 71% decide in first 3s. If they don't stop, nothing else matters.
- **Triple-stacked hooks:** Visual + text + verbal at second 0, all carrying the same claim.
- **Screen recordings are mandatory** for educational/tutorial content.
- **Raw > polished:** Authentic content performs 60% better than overproduced.
- **Scene changes every 2-4 seconds.**

### Testing
- **A/B test hooks, not videos:** Film one video, record 3 different opening hooks, post separately, measure retention.
- **Track 3-second retention:** Videos with 65%+ get 4-7x more impressions.
- **Track completion rate:** 40-50% retention at end of video triggers viral push on TikTok.

### Platform Tuning
- **TikTok:** Raw energy, trending sounds, personality-driven. Hook lands in first WORD.
- **Reels:** Slightly polished, transformation/POV hooks outperform. Under 30s for new audiences.
- **Shorts:** Structured storytelling OK, completion rate is king, searchable titles matter.

### Posting
- **"Comment [WORD]" CTAs** drive 3-5x more DMs than generic CTAs.
- **Series format:** Group related scripts into 3-5 video series. Viewers binge series.
- **Post series scripts 1-2 days apart** - close enough for momentum, spaced enough to avoid fatigue.

---

## Step 6: Offer to Go Deeper

End with:

> Want me to:
> - Write a full word-for-word teleprompter script for any of these?
> - Generate more hooks with a different angle?
> - Adapt these for a specific platform?
> - Build a full content batch with `/content-scripting` (research + outlier scoring + series)?

---

## Follow-up Behavior

**If user says "write a full script for #X":**
- Write a complete word-for-word script with timing markers (e.g., [0:00-0:03])
- Include [FACE] and [SCREEN] visual direction for every moment
- Include 3 hook variations using different frameworks
- Run the pre-flight checklist + grading rubric
- Include a suggested post caption

**If user says "more hooks" or "different angle":**
- Generate more hooks using different frameworks or angles
- Re-run the pre-flight + grading

**If user provides existing scripts to rewrite:**
- Keep the BODY, TEACH, PUNCH, and CAPTION intact
- Replace/add hook variations using the 12 frameworks
- Add [FACE] and [SCREEN] tags if missing
- Add [TEXT OVERLAY] if missing
- Run grading on new hooks

**If user asks about strategy:**
- 85% watch without sound
- 71% decide in first 3 seconds
- 65%+ 3-second retention = 4-7x more impressions
- 40-50% end-of-video retention triggers viral push
- Authentic content performs 60% better than overproduced
- Scene changes every 2-4 seconds
- Series format drives binge behavior
- Negative Delta technique: top 1% of 1,832 viral reels use it
