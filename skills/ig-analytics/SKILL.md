---
name: ig-analytics
description: >
  Hourly Instagram analytics pipeline that pulls per-post and account-level
  insights from the Meta Graph API into Supabase, mirrors live values into a
  Notion dashboard, and runs a daily Claude routine that classifies each post
  into Outlier/Average/Underperformer tiers with a 2-3 sentence "why" note.
  Built for content creators who want feedback that compounds, not a vanity
  follower counter. Triggers on "ig analytics", "instagram analytics",
  "performance dashboard", "content analytics pipeline", "instagram graph api",
  "outlier post detection", "tier classification", "creator analytics".
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# IG Analytics - Per-Post Performance Pipeline

A hands-off content analytics rig for Instagram creators. Hourly cron pulls fresh insights, daily Claude routine grades every post against your own median, you wake up to a Notion view that tells you which post over-performed and why.

## What it does

- Pulls per-post metrics (reach, views, watch time, skip rate, total interactions, etc.) from the Meta Graph API on an hourly cron
- Stores time-series snapshots in Supabase so you can chart growth curves, not just latest values
- Mirrors the latest snapshot into a Notion "Content Analytics" database, one row per post
- Once a day, runs a Claude routine that classifies every post into Outlier / Average / Underperformer / Untested via NTILE(5) on views, then writes a 2-3 sentence note explaining WHY each one landed there
- Optional: links analytics rows to a separate Script Library DB by matching Instagram Post URL, so you can correlate hooks/topics to outcomes

## Why it exists

The Instagram-native dashboard shows "good views, bad follows" at the account level and not much else per-post. Once a post is older than 14 days, Insights goes cold.

If you want to actually learn from your content - which hook formats outperform, what your true median looks like, which posts are flukes vs replicable mechanics - you need your own data store and your own classifier. This is that.

The system is built around three principles:

1. **Compare each post to YOUR median, not the platform's**. A 50K-view post means nothing without context. A 50K-view post when your median is 8K is a 6x outlier you should reverse-engineer.
2. **Watch time and skip rate are the most honest signals**. Reach is what the algorithm gave you. Watch time is what real viewers did.
3. **Tier classification is permanent, hindsight changes**. NTILE re-runs daily, so as new posts come in, older posts may shift tiers. The Claude note explains why TODAY.

## Architecture

```
                      ┌──────────────────────────────┐
                      │   Meta Graph API (v25.0)     │
                      │   per-media insights         │
                      │   account-level daily        │
                      └──────────────┬───────────────┘
                                     │ hourly
                                     ▼
                      ┌──────────────────────────────┐
                      │  Vercel cron                 │
                      │  /api/cron/sync-analytics    │
                      └──────────────┬───────────────┘
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                     ▼
        ┌──────────────────┐                  ┌──────────────────┐
        │   Supabase       │   best-effort    │     Notion       │
        │   (source of     │ ───── mirror ──▶ │   Content        │
        │   truth)         │                  │   Analytics DB   │
        └────────┬─────────┘                  └──────────────────┘
                 │
                 │ daily
                 ▼
        ┌──────────────────┐
        │  scripts/        │
        │  assess-         │   classify + write notes
        │  performance.ts  │ ◀──── Claude API
        └──────────────────┘
```

## Setup walkthrough

### Phase 1: Meta app + Instagram Business Account + long-lived token

You need an Instagram **Business** or **Creator** account linked to a Facebook Page. Personal IG accounts can't read insights via the Graph API.

1. **Create a Meta developer app**: go to https://developers.facebook.com/apps/, click "Create App", pick "Other" as app type, then "Business" as use case. Note your `App ID` and `App Secret`.

2. **Add the Instagram Graph API product** to your app. In the dashboard, "Add Product" → "Instagram Graph API".

3. **Link your IG Business account to a Facebook Page**. In the Instagram app, go to Settings → Account → Switch to Professional Account, then link to a Page you own.

4. **Get a short-lived user access token** with `instagram_basic`, `instagram_manage_insights`, `pages_show_list`, `pages_read_engagement` scopes via the Graph API Explorer (https://developers.facebook.com/tools/explorer/).

5. **Exchange it for a long-lived (60-day) token**:
   ```bash
   curl "https://graph.facebook.com/v25.0/oauth/access_token?grant_type=fb_exchange_token&client_id=$APP_ID&client_secret=$APP_SECRET&fb_exchange_token=$SHORT_LIVED_TOKEN"
   ```

6. **Find your Page ID**:
   ```bash
   curl "https://graph.facebook.com/v25.0/me/accounts?access_token=$LONG_LIVED_TOKEN"
   ```
   Save the numeric `id` for the page linked to your IG account.

7. **Find your Instagram Business Account ID** (optional, the pipeline derives this at runtime):
   ```bash
   curl "https://graph.facebook.com/v25.0/$PAGE_ID?fields=instagram_business_account&access_token=$LONG_LIVED_TOKEN"
   ```

The token expires every 60 days. Set a calendar reminder or write a refresh job. There is no auto-refresh in the Graph API for page tokens linked via the Business flow.

### Phase 2: Supabase project + run migration

1. Create a project at https://supabase.com/dashboard. Pick the region closest to where your Vercel app deploys.

2. Open the SQL editor and paste in the contents of `supabase/migrations/init.sql`. Run it. This creates the 4 tables and 2 views with RLS enabled.

3. From your project's API settings, grab:
   - `Project URL` → `SUPABASE_URL`
   - `service_role` key → `SUPABASE_SERVICE_ROLE_KEY` (NEVER expose this to the browser)

The migration enables RLS with NO policies, so the service_role key bypasses everything and the anon key has zero access. That's intentional - your raw analytics shouldn't be web-readable. If you build a public dashboard, add explicit SELECT policies.

### Phase 3: Notion Content Production Hub

1. Create an internal integration at https://www.notion.so/my-integrations. Save the secret as `NOTION_TOKEN`.

2. Create a new database called "Content Analytics" with these properties (column types matter):

   | Property | Type |
   |---|---|
   | Caption Excerpt | Title |
   | IG Media ID | Text |
   | IG URL | URL |
   | Posted At | Date |
   | Media Type | Select |
   | Media Product Type | Select |
   | Latest Reach | Number |
   | Latest Views | Number |
   | Latest Likes | Number |
   | Latest Comments | Number |
   | Latest Shares | Number |
   | Latest Saves | Number |
   | Latest Total Interactions | Number |
   | Avg Watch Time (s) | Number |
   | Total Watch Time (s) | Number |
   | Skip Rate | Number |
   | Snapshot Count | Number |
   | First Seen At | Date |
   | Last Synced At | Date |
   | Deleted At | Date |
   | Performance Tier | Select (options: Outlier, Average, Underperformer, Untested) |
   | Performance Notes | Text |
   | Tier Assessed At | Date |
   | Notes Assessed At | Date |
   | Notes Model | Text |

3. Share the database with your integration ("..." menu → Connections → add your integration).

4. Get the **datasource ID** (NOT the database ID). Notion's API moved to a datasources model:
   ```bash
   curl -H "Authorization: Bearer $NOTION_TOKEN" \
        -H "Notion-Version: 2025-09-03" \
        "https://api.notion.com/v1/databases/$DB_ID/data_sources"
   ```
   The `id` of the first data_source is your `NOTION_ANALYTICS_DATASOURCE`.

5. (Optional) If you keep a separate Script Library DB and want analytics rows to auto-link, add an "Instagram Post URL" property (URL type) and "IG Media ID" property (Text) on it, then set `NOTION_SCRIPT_DATASOURCE` to its datasource ID.

### Phase 4: Env vars

Copy `config-templates/.env.example` to `.env.local` at the root of your Next.js app. Fill in every value flagged REQUIRED. Pay extra attention to the three creator-context vars:

```bash
CREATOR_NAME="Your Name"
CREATOR_NICHE="one specific sentence"
CREATOR_AUDIENCE="one specific sentence"
```

Vague values produce vague Claude notes. Specific values produce notes you'll actually act on.

### Phase 5: Deploy to Vercel + cron

1. Push the project to a Vercel-connected GitHub repo.

2. Add every env var from `.env.local` to your Vercel project's "Environment Variables" panel. Pick "Production" + "Preview" + "Development" so cron jobs and local dev both work.

3. Generate a cron secret:
   ```bash
   openssl rand -base64 32
   ```
   Set it as `CRON_SECRET` in Vercel. The route handler verifies the `Authorization: Bearer ${CRON_SECRET}` header on every cron call so randos can't trigger your sync.

4. The included `vercel.json` registers an hourly cron at `0 * * * *`. Vercel reads this on deploy.

5. Run the one-shot 90-day backfill ONCE locally before flipping the cron live, or you'll start with empty history:
   ```bash
   node --env-file=.env.local --experimental-strip-types --no-warnings scripts/backfill-90-days.ts
   ```
   This takes ~2 minutes for a 90-day account at 1 req/sec throttle.

### Phase 6: Daily Claude routine

The daily Creative Director routine reads `ig_media_tiered`, generates a 2-3 sentence note per post via Claude, and writes back to Supabase + Notion. You can run it three ways:

**Option A: Manual** - just run it when you remember.
```bash
node --env-file=.env.local --experimental-strip-types --no-warnings scripts/assess-performance.ts
```

**Option B: Vercel cron** - add a second entry to `vercel.json`:
```json
{
  "path": "/api/cron/assess",
  "schedule": "0 13 * * *"
}
```
Then add a thin `/api/cron/assess/route.ts` that imports and runs the assess logic. Useful if you want fully autonomous operation.

**Option C: Claude Code routine (recommended)** - schedule a Claude Code routine that:
1. Reads `prompts/creative-director-routine.md` as its system prompt (with your CREATOR_* vars filled in)
2. Calls the assess script
3. Reads the Notion Content Analytics DB and writes you a one-screen morning brief

The third option is the most useful because Claude can also pattern-match across posts ("your last 3 outliers all started with a 2-second face-to-camera punch") instead of just rating them in isolation.

Use `/loop` or `/schedule` in Claude Code to wire it up.

## Daily usage

Once the system's running, the Notion Content Analytics view is your source of truth. Sort by `Tier Assessed At` descending, filter to `Performance Tier = Outlier`, and read the notes. That's your daily editorial review in 5 minutes.

When a post's tier changes (e.g., a slow-burner that started Average and crossed into Outlier on day 8), the assess routine regenerates the note. Set `manual_notes_override = true` on the row in Supabase if you wrote a note yourself and don't want it overwritten.

## Troubleshooting

**Token expired (HTTP 190)**: long-lived tokens last 60 days. Re-exchange via the curl in Phase 1.5. Future-proof by writing a tiny refresh job that exchanges the existing long-lived token for a fresh one (yes, you can extend without re-auth as long as the token is still valid).

**Per-media insights returning 400 with "metric does not support this type"**: Meta has been deprecating per-media metrics aggressively. As of v22+, `clips_replays_count`, `ig_reels_aggregated_all_plays_count`, `follows`, `profile_visits`, `profile_activity`, and `navigation` are all gone for REELS. The pipeline already excludes them. If a new metric breaks, remove it from `REEL_METRICS` in `lib/instagram-analytics.ts`.

**Account-level metrics returning empty**: account `follower_count` and `reach` time-series only return last-30-days. The pipeline chunks calls into 30-day windows automatically. If you see gaps, run `scripts/refresh-account-daily.ts` to re-fetch.

**Notion writes failing silently**: check that the integration is shared with the database. Also check property names match exactly - "IG URL" vs "ig_url" matters. Use `scripts/remirror-notion.ts` to re-push everything from Supabase after fixing.

**Notion `length should be ≤ 2000` error on emoji-heavy captions**: the `truncateCaption` helper in `lib/notion-analytics.ts` uses `Intl.Segmenter` for grapheme counting, which handles this. If you see the error anyway, lower the `maxGraphemes` default from 80 to 60.

**RLS errors on the dashboard**: the migration sets `security_invoker = true` on the views and enables RLS on tables. The service_role key (which the cron uses) bypasses RLS. If you build a client-side dashboard with the anon key and queries return empty, that's expected - add explicit SELECT policies for whatever you want exposed.

## Tier classification logic

Tiers are computed in the `ig_media_tiered` view, not in code. That way you can re-tune the math without redeploying:

```sql
case
  when posted_at >= now() - interval '48 hours' then 'untested'
  when ntile_bucket = 5 then 'outlier'      -- top 20% by views
  when ntile_bucket = 1 then 'underperformer'  -- bottom 20% by views
  else 'average'                             -- middle 60%
end
```

Posts under 48h old are always Untested - reach hasn't matured. Tiers are computed against ALL non-deleted posts older than 48h, so as your account grows, your bar rises automatically.

If you want a different split (e.g., top 10% as outliers), edit the `ntile(5)` and the bucket comparisons in `supabase/migrations/init.sql`.

## Constraints (Meta API deprecations)

The Graph API has been aggressively pruning per-post metrics since 2024. Verified-deprecated for REELS as of v25.0:

- `follows` (per-post) - GONE
- `profile_visits` (per-post) - GONE
- `profile_activity` (per-post) - GONE
- `navigation` (per-post) - GONE
- `clips_replays_count` - REMOVED in v22+
- `ig_reels_aggregated_all_plays_count` - REMOVED in v22+
- `content_views` - FEED-only, never worked for REELS

For the account level:
- `follower_count` time-series only returns last 30 days
- `reach` time-series only returns last 30 days
- Both must be chunked into ≤30-day call windows

The pipeline accounts for all of these. If Meta deprecates more (they will), update `REEL_METRICS` and `FEED_METRICS` in `lib/instagram-analytics.ts`.

Reference: https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights
