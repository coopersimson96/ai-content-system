-- ================================================================
-- ig-analytics — initial Supabase schema
--
-- NOTE: This schema is reverse-engineered from the source code (the
-- `.from('table').insert/.upsert(...)` calls in src/lib/*.ts). It
-- creates the 4 tables + 2 views + RLS that the pipeline needs to
-- run. Column types are reasonable defaults but may differ slightly
-- from a battle-tested production deployment.
--
-- For the canonical version, run from your own deployed project:
--   supabase db dump --schema public --data-only=false > init.sql
-- and replace this file.
-- ================================================================

-- Instagram Analytics Pipeline - initial schema
--
-- 4 tables:
--   ig_media           - one row per IG post (the universe)
--   ig_media_snapshots - time-series of metric snapshots per post
--   ig_account_daily   - one row per UTC day of account-level metrics
--   ig_account_snapshots - rolling snapshots of total followers + media count
--
-- 2 views:
--   ig_media_latest - each post joined to its most recent snapshot
--   ig_media_tiered - same, plus NTILE(5) tier classification with median stats
--
-- RLS is ENABLED on all 4 tables with NO policies. The service_role key
-- (used by the cron + scripts) bypasses RLS entirely. The anon key has zero
-- read/write access to these tables - intentional, since the analytics data
-- is private. If you want to expose any of this to a public dashboard, add
-- explicit SELECT policies.

-- ============================================================
-- Tables
-- ============================================================

create table if not exists ig_media (
  id text primary key,                          -- IG media id from Graph API
  ig_url text,                                  -- permalink
  posted_at timestamptz not null,
  media_type text not null,                     -- IMAGE | VIDEO | CAROUSEL_ALBUM
  media_product_type text not null,             -- REELS | FEED | STORY
  caption text,
  thumbnail_url text,

  first_seen_at timestamptz not null default now(),
  last_synced_at timestamptz,
  deleted_at timestamptz,                       -- set when Graph API returns 404 (post deleted)

  -- Notion linkages (optional)
  notion_analytics_page_id text,
  notion_script_id text,

  -- Performance assessment (populated by scripts/assess-performance.ts)
  performance_tier text,                        -- outlier | average | underperformer | untested
  performance_notes text,                       -- 2-3 sentence Claude note
  tier_assessed_at timestamptz,
  notes_assessed_at timestamptz,
  notes_model text,                             -- e.g. "claude-sonnet-4-6" or "rule"
  manual_notes_override boolean not null default false  -- skip auto-regen if true
);

create index if not exists ig_media_posted_at_idx on ig_media (posted_at desc);
create index if not exists ig_media_deleted_at_idx on ig_media (deleted_at);

create table if not exists ig_media_snapshots (
  id uuid primary key default gen_random_uuid(),
  media_id text not null references ig_media(id) on delete cascade,
  captured_at timestamptz not null default now(),
  cadence text not null,                        -- hourly | daily | backfill

  reach bigint,
  views bigint,
  likes bigint,
  comments bigint,
  shares bigint,
  saves bigint,
  total_interactions bigint,
  avg_watch_time_ms bigint,
  total_play_time_ms bigint,
  reels_skip_rate numeric,
  reposts bigint
);

create index if not exists ig_media_snapshots_media_id_captured_at_idx
  on ig_media_snapshots (media_id, captured_at desc);

create table if not exists ig_account_daily (
  date date primary key,                        -- UTC date
  followers_gained bigint,                      -- net follower delta (from follower_count time-series)
  daily_reach bigint,
  daily_profile_views bigint,
  daily_accounts_engaged bigint,
  daily_total_interactions bigint,
  daily_views bigint,
  daily_website_clicks bigint,
  total_followers bigint,                       -- backfilled by sync (not in fetchAccountDailyRange)
  updated_at timestamptz not null default now()
);

create table if not exists ig_account_snapshots (
  id uuid primary key default gen_random_uuid(),
  captured_at timestamptz not null default now(),
  total_followers bigint not null,
  media_count bigint not null
);

create index if not exists ig_account_snapshots_captured_at_idx
  on ig_account_snapshots (captured_at desc);

-- ============================================================
-- Views
-- ============================================================
--
-- security_invoker = true so the views run with the caller's permissions
-- (so service_role bypasses RLS, anon hits RLS denial, exactly like the
-- underlying tables).

create or replace view ig_media_latest
with (security_invoker = true)
as
select
  m.id,
  m.ig_url,
  m.posted_at,
  m.media_type,
  m.media_product_type,
  m.caption,
  m.thumbnail_url,
  m.notion_script_id,
  m.notion_analytics_page_id,
  m.first_seen_at,
  m.last_synced_at,
  m.deleted_at,
  m.performance_tier,
  m.performance_notes,
  m.notes_assessed_at,
  m.manual_notes_override,
  s.captured_at as latest_snapshot_at,
  s.reach,
  s.views,
  s.likes,
  s.comments,
  s.shares,
  s.saves,
  s.total_interactions,
  s.avg_watch_time_ms,
  s.total_play_time_ms,
  s.reels_skip_rate,
  s.reposts
from ig_media m
left join lateral (
  select *
  from ig_media_snapshots s
  where s.media_id = m.id
  order by s.captured_at desc
  limit 1
) s on true
where m.deleted_at is null;

-- ig_media_tiered: classify each post into outlier / average / underperformer
-- via NTILE(5) on views, treating posts < 48h old as 'untested'. Includes
-- median stats (used in the assess-performance prompt for context).

create or replace view ig_media_tiered
with (security_invoker = true)
as
with mature as (
  select *
  from ig_media_latest
  where posted_at < now() - interval '48 hours'
    and views is not null
),
medians as (
  select
    percentile_cont(0.5) within group (order by views) as median_views,
    percentile_cont(0.5) within group (order by reach) as median_reach,
    percentile_cont(0.5) within group (order by total_interactions) as median_interactions,
    percentile_cont(0.5) within group (order by avg_watch_time_ms) as median_watch_ms
  from mature
),
ntiles as (
  select
    id,
    ntile(5) over (order by views) as bucket
  from mature
)
select
  l.id,
  l.ig_url,
  l.posted_at,
  l.media_type,
  l.media_product_type,
  l.caption,
  l.notion_script_id,
  l.performance_tier as stored_tier,
  l.performance_notes,
  l.notes_assessed_at,
  l.manual_notes_override,
  coalesce(l.views, 0) as views,
  l.reach,
  l.total_interactions,
  l.avg_watch_time_ms,
  l.reels_skip_rate,
  l.latest_snapshot_at,
  case
    when l.posted_at >= now() - interval '48 hours' then 'untested'
    when n.bucket = 5 then 'outlier'
    when n.bucket = 1 then 'underperformer'
    else 'average'
  end as computed_tier,
  med.median_views,
  med.median_reach,
  med.median_interactions,
  med.median_watch_ms
from ig_media_latest l
left join ntiles n on n.id = l.id
cross join medians med
where l.deleted_at is null;

-- ============================================================
-- Row-level security
-- ============================================================
-- Enable RLS on all 4 tables with NO policies. service_role bypasses RLS,
-- anon gets denied.

alter table ig_media enable row level security;
alter table ig_media_snapshots enable row level security;
alter table ig_account_daily enable row level security;
alter table ig_account_snapshots enable row level security;
