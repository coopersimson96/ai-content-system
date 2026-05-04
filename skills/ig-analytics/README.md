# IG Analytics

Hourly Instagram analytics pipeline that tells you which posts over-performed and why - automatically, every day, in your own database and Notion view.

## What you get

- **Hourly cron** pulls per-post insights (reach, views, watch time, skip rate, interactions) from the Meta Graph API
- **Time-series storage** in Supabase so you can chart growth curves, not just latest snapshots
- **Notion mirror** - one row per post, latest values always fresh
- **Daily Claude routine** classifies every post into Outlier / Average / Underperformer / Untested with a 2-3 sentence note explaining why
- **Tier classification** uses NTILE(5) against your own median, so the bar rises as your account grows

## What it costs

- Vercel: free tier covers the hourly cron easily
- Supabase: free tier covers ~6 months of data for a typical creator account
- Notion: free, just need an integration token
- Anthropic API: ~$0.50/month for the daily assess routine on a 100-post account
- Meta Graph API: free, but you need an Instagram Business or Creator account linked to a Facebook Page

## How to use it

1. Read `SKILL.md` end-to-end. The setup walkthrough is in 6 phases (Meta app, Supabase, Notion, env vars, Vercel deploy, daily routine).
2. Run `supabase/migrations/init.sql` against your Supabase project.
3. Copy `config-templates/.env.example` to `.env.local`, fill in your values.
4. Run `scripts/smoke-test.ts` to verify your Graph API token works.
5. Run `scripts/backfill-90-days.ts` once to seed the database with history.
6. Deploy to Vercel. The cron starts running on the next hour.
7. Schedule the daily Claude routine using the prompt at `prompts/creative-director-routine.md`.

## File map

```
ig-analytics/
├── SKILL.md                    # full setup walkthrough + architecture + troubleshooting
├── README.md                   # this file
├── lib/
│   ├── instagram-analytics.ts  # Graph API helpers (per-post + account-level)
│   ├── supabase.ts             # service-role admin client
│   ├── cadence.ts              # decide hourly vs daily vs skip per post
│   └── notion-analytics.ts     # Notion mirror (upsert + grapheme truncation)
├── api/
│   └── cron/sync-analytics/route.ts   # the hourly cron handler
├── scripts/
│   ├── smoke-test.ts                  # verify Graph API works
│   ├── backfill-90-days.ts            # one-shot historical pull
│   ├── refresh-account-daily.ts       # re-fetch account-level data
│   ├── remirror-notion.ts             # re-push Supabase → Notion after schema changes
│   └── assess-performance.ts.template # daily Claude routine (rename to .ts after filling vars)
├── supabase/
│   └── migrations/init.sql            # 4 tables + 2 views, run once
├── prompts/
│   └── creative-director-routine.md   # system prompt for assess-performance
└── config-templates/
    ├── .env.example                   # every var with placeholder + comment
    ├── vercel.json                    # cron registration
    └── package.json.example           # minimal deps
```

## Customizing for your niche

The prompt in `prompts/creative-director-routine.md` uses three template variables: `{{CREATOR_NAME}}`, `{{CREATOR_NICHE}}`, `{{CREATOR_AUDIENCE}}`. Set them as env vars before running the assess script. Specific niche descriptions produce dramatically better notes - spend 5 minutes on these.

## Limits

- Long-lived Meta tokens expire every 60 days. There's no auto-refresh in the Business flow. Set a calendar reminder.
- Per-post `follows` / `profile_visits` are GONE for REELS as of v22+. The pipeline already excludes them, but if Meta deprecates more, update `REEL_METRICS` in `lib/instagram-analytics.ts`.
- Account-level `follower_count` and `reach` time-series only return last-30-days. The pipeline chunks calls into 30-day windows automatically.
