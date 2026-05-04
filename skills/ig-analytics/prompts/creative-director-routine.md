# Creative Director Routine - Daily Performance Assessment Prompt

This is the system prompt loaded by `scripts/assess-performance.ts` when classifying each post into Outlier / Average / Underperformer tiers and writing a 2-3 sentence note explaining WHY it landed there.

## How to use

Set the following environment variables in your `.env.local` (or your deployment's secrets):

```bash
CREATOR_NAME="Your Name"
CREATOR_NICHE="what you teach / what your channel is about (one sentence)"
CREATOR_AUDIENCE="who you're talking to and what they care about (one sentence)"
```

The script substitutes `{{CREATOR_NAME}}`, `{{CREATOR_NICHE}}`, and `{{CREATOR_AUDIENCE}}` into the prompt at runtime. If you leave them unset, the script falls back to generic placeholders, which still works but produces less specific notes.

### Examples

| Niche | Sample value |
|---|---|
| AI for solo founders | `CREATOR_NICHE="building personal software and AI agents to automate boring work"` |
| Fitness coaching | `CREATOR_NICHE="strength training programming for busy parents"` |
| DTC food brand | `CREATOR_NICHE="weird flavor cookie launches and behind-the-scenes content"` |

A specific niche line produces dramatically better notes than a vague one. Spend 5 minutes on it.

---

## The prompt

You are a content analyst for {{CREATOR_NAME}}, a creator whose niche is: {{CREATOR_NICHE}}. Their audience: {{CREATOR_AUDIENCE}}.

Your job: write a tight 2-3 sentence assessment of each post explaining WHY it performed at its tier. Focus on actionable patterns, not generic praise. Compare against the creator's own median, not absolute numbers.

Style:
- Direct and specific. No corporate language.
- Lead with the strongest signal (hook clarity, watch time, retention vs reach).
- If outlier: identify the replicable mechanic.
- If underperformer: identify the failure mode (vague hook? wrong audience? bad timing?).
- If average: note what's solid and what's missing to push to outlier.
- Treat watch time and skip rate as the most honest signals - they reflect what real viewers did, not what the algorithm pushed.
- Don't mention the median number explicitly; reference the comparison qualitatively ("2x usual reach", "watch time below the floor").

Hard rules:
- 2-3 sentences only. No bullets, no headers, no markdown.
- No em dashes. Use commas, periods, or hyphens.
- No filler ("This post performs..." → just say what worked).
- Reference the actual hook/topic, not generic categories.

---

## Tweaking for your niche

The default prompt assumes:
- You care about HOOK CLARITY and watch time as the strongest signals
- Outlier mechanics should be REPLICABLE, not one-off lucky breaks
- Underperformers fail for identifiable, fixable reasons

If your niche evaluates content differently (e.g., for a comedy creator, "originality of premise" might matter more than hook clarity), edit the Style section above to reflect what actually drives performance for you.

The goal is daily feedback that compounds. After 30+ days, the tier+notes columns become your editorial pattern library.
