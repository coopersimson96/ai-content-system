---
name: hooks
description: Generate high-converting short-form video hooks and scripts for any niche. Uses 10 proven frameworks with documented viral performance data, visual direction tags, and outlier content principles. Grounded in real research.
argument-hint: "[topic/product] for [audience]" or describe what you're creating content about
context: conversation
---

# Short-Form Video Hook & Script Generator

Generate copy-paste-ready hooks and full scripts for TikTok, Reels, and YouTube Shorts — grounded in proven frameworks from research across 16K+ social media engagements, 49 X posts (24K+ likes), 10 Reddit threads, 25+ web sources, and analysis of 10+ outlier creators (Feb 2026).

---

## Step 1: Parse the User's Input

Extract from `$ARGUMENTS`:

1. **TOPIC** — What is the content about? (e.g., "AI for business owners", "fitness for beginners", "SaaS scheduling tool")
2. **AUDIENCE** — Who is the target viewer? (e.g., "business owners", "founders", "freelancers", "general audience")
3. **PLATFORM** — TikTok, Reels, Shorts, or all? (default: all)
4. **TONE** — Professional, casual/raw, humorous, educational? (default: casual/raw)
5. **ANGLE** — Any specific angle? (e.g., "pain point about wasting time", "before/after transformation", "confession style")
6. **FORMAT** — Hook variations only, full scripts, or both? (default: both)

**If TOPIC is missing or unclear**, ask:

> What's the content about and who's it for?
>
> Example: `/hooks AI tools for small business owners`

**If only TOPIC is provided**, infer a reasonable AUDIENCE and proceed. Don't over-ask.

---

## Step 2: Select and Apply Hook Frameworks

You have **10 proven hook frameworks** in your arsenal. For each piece of content, generate **3 hook variations** using different frameworks. Choose the 3 most relevant frameworks for the topic — don't force-fit frameworks that don't match.

### FRAMEWORK SELECTION RULES

- **Proof-First** should appear in at least 40% of scripts — highest documented performance (4-7x more impressions)
- **Pain Point** should appear whenever the topic involves a specific frustration
- **Curiosity Gap** works for nearly any topic — use as a reliable fallback
- **Contrarian** works best when challenging common assumptions ("you don't need X")
- **"This Cost Me Thousands"** only when real dollar amounts or consequences exist
- **Never use the same 3 frameworks for consecutive scripts** — vary the combinations

### LIBRARY HOOK EXAMPLES (before generating)

Before generating hooks, check if `~/.config/notion-content/config.json` has `inspiration_data_source_id`. If so:

1. For each selected framework, query the Inspiration Library using `notion-search` with `data_source_url` set to `collection://{inspiration_data_source_id}` for hooks matching that framework
2. Filter: Type = `Hook Example`, Hook Framework = [selected framework], Performance Tier IN [Outlier, Strong], limit 2 per framework
3. Use returned Hook Text as concrete examples alongside the hardcoded templates below
4. Tag any hook adapted from a library entry with "(Library)" in internal notes for transparency
5. **Fallback:** If 0 results or config missing, proceed silently with hardcoded templates only

### THE 10 HOOK FRAMEWORKS (ranked by documented performance)

---

### 1. Curiosity Gap / Open Loop
**Why it works:** Opens a knowledge gap the brain compulsively needs to close. 70%+ of viral videos use this in the first 3 seconds. Most-cited framework across all sources.
**Documented performance:** "Did you know..." template: 22M+ views. "Have you heard about..." template: 13M+ views, 83% higher comment rates.
**Sources:** @signulll 13.4K likes, CreatorsJet, OpusClip, Buffer, VirVid.ai

**Templates:**
- "I'm about to show you something that [industry] doesn't want you to know."
- "Here's what [experts/pros] use but never share publicly..."
- "Nobody's talking about this, but [surprising claim]..."
- "I found out why [common problem] keeps happening. And it's not what you think."
- "[Number] things about [topic] that will change how you [action]."
- "Did you know that [surprising fact]..." *(22M+ views documented)*
- "Have you heard about [thing]..." *(13M+ views documented)*

**Best for:** Educational content, reveals, insider knowledge, myth-busting

---

### 2. Proof-First / Results Hook
**Why it works:** Leads with evidence/outcome, then explains how. Establishes credibility immediately. Gets 4-7x more impressions when paired with 65%+ 3-second retention.
**Documented performance:** @timdanilovhi earned $1K-$7K per Short using this framework consistently across 70+ videos. @seergioo_gil got 12M views from 4 Shorts using result-first openings.
**Sources:** @timdanilovhi 355 likes, @maubaron 375 likes, r/Instagram 320→17K post, OpusClip, Shortimize

**Templates:**
- "I [achieved result] in [timeframe]. Here's exactly how."
- "This [tool/method] took us from [before state] to [after state]."
- "[Specific number/metric]. That's what happened when I [did thing]."
- "My [client/friend/colleague] [achieved result] using this one [trick/method/tool]."
- "[Result]. [Result]. [Result]. All from one [change/tool/habit]."

**Best for:** Case studies, tutorials, product demos, authority-building, outcome-focused content

---

### 3. Pain Point Hook
**Why it works:** Speaks directly to what the audience is frustrated about. Resonates instantly because it mirrors their daily experience. Scripts rooted in real audience complaints outperform hypothetical topics.
**Documented performance:** "3 mistakes everyone makes about X" template: 2x engagement vs generic advice hooks. "Top 3 shocking facts" template: 6M+ views.
**Sources:** MarketingBlocks, SendShort, VirVid.ai, multiple web sources

**Templates:**
- "If you're still [painful manual process] in 2026 — we need to talk."
- "Struggling with [specific problem]? Here's the fix."
- "The #1 reason [audience] fail at [goal]? [Pain point]."
- "How much time did you waste on [task] this week? Be honest."
- "[Pain point] is costing you [money/time/customers]. Here's how to stop it."
- "3 mistakes everyone makes about [topic]..." *(2x engagement documented)*

**Best for:** Problem-aware audiences, how-to content, product introductions, relatable content

---

### 4. Contrarian / Bold Statement
**Why it works:** Creates cognitive dissonance — challenges what the viewer assumes is true. Forces a pause because the brain wants to resolve the contradiction.
**Sources:** r/SocialMediaMarketing 14 comments, CreatorsJet, SendShort, OpusClip

**Templates:**
- "Stop doing [common thing]. Do this instead."
- "[Common advice] is actually terrible advice. Here's why."
- "Everyone says [popular opinion]. They're wrong."
- "[Common practice] is keeping you [stuck/broke/behind]. Here's what works."
- "The worst thing you can do for [goal] is [thing everyone does]."

**Best for:** Hot takes, challenging norms, positioning as authority, educational content

---

### 5. The Unexpected Confession
**Why it works:** Feels personal and exclusive — mimics insider knowledge. Triggers curiosity because people are wired to lean in when someone shares something "they shouldn't."
**Sources:** CreatorsJet, Retiplex, AikenHouse

**Templates:**
- "I probably shouldn't share this, but..."
- "I've been doing [thing] for [time] and nobody noticed. Here's how."
- "I'm embarrassed it took me this long to figure this out."
- "OK I wasn't going to post this but [reason]..."
- "This is the [thing] I wish someone told me [timeframe] ago."

**Best for:** Personal stories, behind-the-scenes, insider tips, building trust and relatability

---

### 6. "This Cost Me Thousands"
**Why it works:** Personal stakes + financial/emotional consequences = high engagement. People lean in when real money or real consequences are on the line.
**Sources:** CreatorsJet, @slic_media

**Templates:**
- "This one mistake cost me $[amount]. Don't repeat it."
- "I was spending $[amount] a [time period] on [thing] until I found this."
- "This mistake nearly [ruined/cost/destroyed] my [business/project/reputation]."
- "I wasted [time/money] on [thing] before I figured out [solution]."
- "The most expensive lesson I learned about [topic]: [lesson]."

**Best for:** Cautionary tales, money-saving tips, business advice, building trust through vulnerability

---

### 7. Pattern Interrupt (Visual + Audio)
**Why it works:** Hijacks attention *before* conscious decision-making occurs. Exploits the brain's wiring to notice anything that breaks expected flow.
**Sources:** r/AI_UGC_Marketing, @maubaron 375 likes, OpusClip, Brandefy

**Templates:**
- *[Abrupt camera movement / unexpected prop / sound effect]* + bold text overlay with core claim
- *[Split screen: old way vs new way]* + "Same task. Different century."
- *[Show the end result FIRST]* + "This took me [short time]. Here's what I did."
- *[Hand slam / Post-It reveal / glitch cut]* + "[Bold claim]"
- *[Start mid-action or mid-sentence]* — no intro, no warm-up

**Best for:** Energy-driven content, demos, transformation reveals, content without verbal hooks. Works even silent.

---

### 8. Before vs After / Transformation
**Why it works:** Visually satisfying, shows value promise instantly. Outperforms specifically on Instagram Reels because it aligns with the platform's aspirational culture.
**Sources:** CreatorsJet, SendShort, AlmCorp

**Templates:**
- *[Show the messy before state]* → *[Cut to clean after state]*
- "[Before metric] vs [After metric]. Same [person/business]. One change."
- "What [task] looked like before: [pain]. What it looks like now: [ease]."
- *[Side-by-side comparison]* + "Left: [time ago]. Right: today."
- "6 months ago I was [struggling state]. Now I [thriving state]. Here's the one thing I changed."

**Best for:** Visual content, product demos, personal growth, fitness, design, workflow improvements

---

### 9. Question Hook
**Why it works:** Leverages curiosity psychology — creates information gaps the brain compulsively wants to close. Works best when hyper-specific to the audience's pain.
**Sources:** @vidIQ 631+229 likes, OpusClip, Brandefy

**Templates:**
- "Why do some [audience members] [succeed] while others [fail]?"
- "What if I told you [surprising fact about their daily reality]?"
- "Can you [do simple thing]? Then you can [do impressive thing]. Here's proof."
- "How many hours a [time period] do you spend on [task]? What if it was zero?"
- "What do [successful people] all have in common? It's not [obvious thing]."

**Best for:** Educational content, addressing knowledge gaps, engaging pain-point-aware audiences

---

### 10. Test / Experiment Hook
**Why it works:** Creates curiosity through relatability + suspense. The "what happened" structure creates an open loop.
**Sources:** r/contentcreation 50+ videos analyzed, PlayPlay, HeyOrca

**Templates:**
- "I tried [thing] for [time period]. Here's what happened."
- "Watch what happens when I [do unexpected thing]."
- "I tested [number] different [things] to see which one actually works."
- "I gave [tool/method] to [person] with zero experience. The results surprised me."
- "What happens when you [apply concept] to [unexpected context]?"

**Best for:** Product reviews, tutorials, curiosity-driven content, building suspense

---

## Step 3: Script Structure

Every script follows the universal **Hook → Body → Teach → Punch → CTA** structure, battle-tested across 118K+ viral videos.

### Visual Direction Tags

**Every full script MUST include these tags:**

- **[FACE]** — Talking head, camera on creator
- **[SCREEN]** — Screen recording showing the actual tool/prompt/output (the #1 format for educational content)
- **[TEXT OVERLAY: ...]** — Bold on-screen text (required — 85% watch without sound)

Alternate between [FACE] and [SCREEN] every 2-4 seconds in the body to maintain retention.

### Tone Principles (from Outlier Creator Analysis)

- **Anti-hype by default.** No "AI will change everything." No overselling. Every claim should be grounded in a specific person's real experience. Calm, realistic framing builds trust and outperforms hype. (Harper Carroll grew 2K → 200K with this exact approach.)
- **One tool, one problem per script.** Never cram multiple tools or multiple problems into one video. Solve ONE thing clearly. (Pattern confirmed across Harper Carroll, Rachel Woods, and Riley Brown.)
- **Specific numbers beat vague claims.** "3 hours → 5 minutes" beats "saves you time." "$7 per invoice → $0.20" beats "reduces costs." Always use exact figures when available.
- **Real examples > generic advice.** A bakery owner's story beats "businesses can use AI for content." Specificity = relatability.

### Platform Timing Guidelines

| Platform | Hook Window | Energy Level | Total Length Sweet Spot |
|---|---|---|---|
| TikTok | 2 seconds MAX | 20% higher than normal | 15-30 seconds |
| Reels | 3 seconds | Polished but authentic | 15-45 seconds (under 30 for new audiences) |
| Shorts | 3-5 seconds | Structured storytelling | 15-35 seconds |

### Script Template

```
**[TEXT OVERLAY: {Bold, short text that captures the core claim}]**

**HOOK A ({Framework Name}):**
{The spoken/on-screen hook — must land within 2-3 seconds}

**HOOK B ({Different Framework Name}):**
{Alternative hook for A/B testing}

**HOOK C ({Different Framework Name}):**
{Third variation for A/B testing}

**BODY:**
{[SCREEN] and [FACE] tagged. Core content — deliver value, show the problem, demonstrate the solution. Scene changes every 2-4 seconds.}

**TEACH:**
{The insight, lesson, or proof. Real examples > generic advice.}

**PUNCH:**
{Memorable closing line — quotable, shareable, hits hard.}

**CAPTION:** {Short, punchy caption with CTA + hashtags}
```

---

## Step 4: Output Format

When generating hooks/scripts, use this format:

```
# {NUMBER} Hooks for: {TOPIC} → {AUDIENCE}
Platform: {PLATFORM} | Tone: {TONE}

---

## SCRIPT {N} — {Title}

**[TEXT OVERLAY: {Bold text}]**

**HOOK A ({Framework}):**
{Hook text}

**HOOK B ({Framework}):**
{Hook text}

**HOOK C ({Framework}):**
{Hook text}

**BODY:**
{Body text with [FACE] and [SCREEN] tags}

**TEACH:**
{Teach text}

**PUNCH:**
{Punch text}

**CAPTION:** {Caption text}

---
```

---

## Step 5: Production Tips (Always Include)

After all scripts, include:

```
## Production Tips

### Filming
- **Silent-first**: 85% watch without sound. Every hook needs bold on-screen captions.
- **3-second rule**: 71% of viewers decide in first 3s. If they don't stop, nothing else matters.
- **Triple-layer hooks**: Visual + text + audio together. All three = almost guaranteed scroll-stop.
- **Screen recordings are mandatory** for educational/tutorial content. Show the actual tool, prompt, or output. This is the #1 format for educational content across all top creators analyzed.
- **Raw > polished**: Authentic content performs 60% better than overproduced. Film on your phone. Don't overthink lighting.
- **Scene changes every 2-4 seconds** — alternate [FACE] and [SCREEN] to maintain retention.

### Testing
- **A/B test hooks, not videos**: Film one video, record 3 different opening hooks, post separately, measure retention.
- **Track 3-second retention**: Videos with 65%+ 3-second retention get 4-7x more impressions.
- **Track completion rate**: 40-50% retention at end of video needed to trigger viral push on TikTok.
- **Intent before hook** (from Reddit r/SocialMediaMarketing, 14 comments): Before optimizing hooks, audit the video's intent — learn, feel, or act? If intent is unclear, no hook saves it.

### Platform Tuning
- **TikTok** → Raw energy, trending sounds, personality-driven. Hook lands in first WORD.
- **Reels** → Slightly polished, transformation/POV hooks outperform. Aspirational. Under 30s for new audiences.
- **Shorts** → Structured storytelling OK, completion rate is king, searchable titles matter.

### Posting
- **"Comment [WORD]" CTAs** — drive DMs → newsletter → community. 3-5x more DMs than generic CTAs.
- **Series format** — group related scripts into 3-5 video series. Series grew Harper Carroll from 2K → 200K followers in 3 weeks. Viewers binge series.
- **Post series scripts 1-2 days apart** — close enough for momentum, spaced enough to avoid fatigue.
```

---

## Step 6: Offer to Go Deeper

End with:

```
---
Want me to:
- Write a full word-for-word teleprompter script for any of these?
- Generate more hooks with a different angle?
- Adapt these for a specific platform?
- Rewrite existing scripts with hook variations?
- Build a full content batch with /content-scripting (research + outlier scoring + series)?

Just tell me what you need.
```

---

## FOLLOW-UP BEHAVIOR

**If user says "write a full script for #X"** (or any number):
- Write a complete word-for-word script with exact timing markers (e.g., [0:00-0:03])
- Include [FACE] and [SCREEN] visual direction for every moment
- Include on-screen text/caption suggestions for each section
- Include 3 hook variations using different frameworks
- Include a suggested post caption

**If user says "more hooks" or "different angle":**
- Generate more hooks using different frameworks or different angles
- Ask what angle if not specified: pain point, aspirational, humor, authority, before/after, confession, contrarian

**If user provides existing scripts to rewrite:**
- Keep the BODY, TEACH, PUNCH, and CAPTION intact
- Replace/add hook variations using the 10 frameworks above
- Label each hook with its framework name
- Choose frameworks that best match the content's topic and tone
- Add [FACE] and [SCREEN] tags if missing
- Add [TEXT OVERLAY] if missing

**If user provides new topic/audience:**
- Start fresh with the new context

**If user asks about strategy or best practices:**
- Answer from the baked-in research — don't run new searches
- Key stats to reference:
  - 85% watch without sound
  - 71% of viewers decide in first 3 seconds whether to keep watching
  - 70%+ of viral videos have strong hooks in first 3 seconds
  - Videos with 65%+ 3-second retention get 4-7x more impressions
  - 40-50% end-of-video retention triggers viral push on TikTok
  - Authentic content performs 60% better than overproduced
  - Scene changes every 2-4 seconds maintain retention
  - "Did you know..." hooks: 22M+ views documented
  - "Have you heard about..." hooks: 13M+ views, 83% higher comments
  - "3 mistakes everyone makes..." hooks: 2x engagement
  - Series format: grew Harper Carroll 2K → 200K in 3 weeks
  - One hook format repeated with tweaks: 60M views (@ogilichev)
  - Proof-First framework: $1K-$7K per Short across 70+ videos (@timdanilovhi)
  - Universal script structure: Hook → Problem → Solution → CTA (tested across 118K+ viral videos)

---

## RESEARCH SOURCES (baked in)

This skill is grounded in research from Feb 2026:

### Hook Frameworks
- **Reddit** (4 threads, 23 upvotes, 18 comments): r/SocialMediaMarketing, r/Instagram, r/contentcreation, r/AI_UGC_Marketing
- **X** (14 posts, 16,433 likes, 1,497 reposts): @signulll (13.4K likes — viral formula exposé), @timdanilovhi (355 likes — $1K-7K/Short framework), @vidIQ (860 combined likes — Shorts formulas), @maubaron (375 likes — reaction hook format), @slic_media (hook testing framework)
- **Web** (10+ pages): CreatorsJet (7 frameworks), OpusClip (5 core formulas + metrics), VirVid.ai (10 viral templates), SendShort (14 TikTok hooks), MarketingBlocks (50+ templates), Buffer, Brandefy (psychology of hooks), vidIQ (18 Shorts hooks)

### Outlier Creator Patterns
- **Creators analyzed**: Harper Carroll (2K→200K in 3 weeks, 400K in 13 months), Matt Wolfe (857K subs, 65.5M views), Vaibhav Sisinty (1M Instagram), Riley Brown, Rachel Woods, Rowan Cheung, Liam Ottley, Igor Pogany, Noe Varner, The AI Advantage
- **X** (35 posts, 8K+ likes): @seergioo_gil (12M views from 4 Shorts), @linaa_ai (11.7M views/$16.7K), @heyfionaai (22M/12M/11M per video), @ogilichev (60M views from one hook format), @wanneracademy (outlier scoring method)
- **Viral templates with documented metrics**: "Did you know..." (22M+ views, 70%+ completion), "Top 3 shocking facts" (6M+), "3 mistakes everyone makes" (2x engagement), "Have you heard about..." (13M+, 83% higher comments)

### 9 Creator Content Patterns (from deep analysis)
1. **Translator positioning** — Bridge between complex tech and normal people
2. **Series explosion** — Group content into themed series of 3-5 videos
3. **Content cadence** — Post 5-7x/week minimum for algorithmic momentum
4. **Show-don't-tell screen recording** — Screen recordings > talking about tools
5. **Anti-hype tone** — Calm, realistic framing beats hype every time
6. **One tool, one problem** — Never cram multiple solutions into one video
7. **Viral format copying** — Find a format that works, repeat with tiny tweaks
8. **Hook archetype matching** — Match framework to content type
9. **Education → newsletter → course funnel** — Content → followers → CTA → DMs → email → product
