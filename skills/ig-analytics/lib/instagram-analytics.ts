/**
 * Instagram Graph API helpers for the analytics sync pipeline.
 *
 * Phase 0 findings baked in:
 * - `follows`/`profile_visits`/`profile_activity`/`navigation` are NOT supported
 *   per-media for media_product_type=REELS as of 2024 deprecation. If your
 *   content is 100% reels, you don't need to request them.
 * - Per-media insights require `metric_type=total_value` (not period=day) on v22+.
 * - Time-series metrics (follower_count, reach) at the account level use
 *   period=day with since/until and return values[] with end_time.
 * - Account-level total_value metrics (profile_views, accounts_engaged,
 *   total_interactions, views, website_clicks) require metric_type=total_value
 *   AND period AND since/until. They return ONE total_value per call window;
 *   per-day breakdown requires one call per day.
 *
 * Time zone note: Meta returns time-series end_time as UTC-tagged strings (e.g.
 * `2026-04-19T07:00:00+0000`). For US-Pacific accounts that 7am UTC stamp is the
 * end of 2026-04-18 PT. We store the UTC date of `end_time` as our `date` key -
 * consistent within our DB, but off by ~7h vs. what Meta's UI shows.
 */

export const IG_API_VERSION = "v25.0";
const IG_API = `https://graph.facebook.com/${IG_API_VERSION}`;

// ---------- Types ----------

export interface IgMediaListItem {
  id: string;
  ig_url: string;
  posted_at: string; // ISO-8601 UTC
  media_type: string;
  media_product_type: string;
  caption: string | null;
  thumbnail_url: string | null;
}

export interface IgPerMediaMetrics {
  reach: number | null;
  views: number | null;
  likes: number | null;
  comments: number | null;
  shares: number | null;
  saves: number | null;
  total_interactions: number | null;
  avg_watch_time_ms: number | null;
  total_play_time_ms: number | null;
  reels_skip_rate: number | null;
  reposts: number | null;
}

export interface IgAccountDayData {
  date: string; // YYYY-MM-DD, UTC date of metric end_time
  followers_gained: number | null;
  daily_reach: number | null;
  daily_profile_views: number | null;
  daily_accounts_engaged: number | null;
  daily_total_interactions: number | null;
  daily_views: number | null;
  daily_website_clicks: number | null;
}

// ---------- Metric branching by product type ----------

// Verified working on v25.0 against a freshly-posted REELS media (2026-04-25).
// `clips_replays_count` and `ig_reels_aggregated_all_plays_count` were removed
// in v22+ and 400 the entire request if included. `content_views` is FEED-only.
const REEL_METRICS = [
  "reach",
  "views",
  "likes",
  "comments",
  "shares",
  "saved",
  "total_interactions",
  "ig_reels_avg_watch_time",
  "ig_reels_video_view_total_time",
  "reels_skip_rate",
  "reposts",
] as const;

const FEED_METRICS = [
  "reach",
  "views",
  "likes",
  "comments",
  "shares",
  "saved",
  "total_interactions",
] as const;

const PER_MEDIA_EMPTY: IgPerMediaMetrics = {
  reach: null,
  views: null,
  likes: null,
  comments: null,
  shares: null,
  saves: null,
  total_interactions: null,
  avg_watch_time_ms: null,
  total_play_time_ms: null,
  reels_skip_rate: null,
  reposts: null,
};

function getMetricsForProductType(productType: string): readonly string[] {
  return productType === "REELS" ? REEL_METRICS : FEED_METRICS;
}

// Graph API returns metrics as either {values: [{value, end_time}]} or
// {total_value: {value}}. Read whichever shape is present.
function readMetricValue(m: {
  values?: Array<{ value: number }>;
  total_value?: { value: number };
}): number | null {
  if (m?.total_value && typeof m.total_value.value === "number") {
    return m.total_value.value;
  }
  if (m?.values?.[0] && typeof m.values[0].value === "number") {
    return m.values[0].value;
  }
  return null;
}

export function isMediaGoneError(errorText: string): boolean {
  return /does not exist|missing permissions|Object with ID/i.test(errorText);
}

// ---------- API helpers ----------

export async function fetchInstagramAccount(): Promise<{
  id: string;
  username: string;
} | null> {
  const token = process.env.FACEBOOK_ACCESS_TOKEN;
  const pageId = process.env.FACEBOOK_PAGE_ID;
  if (!token || !pageId) return null;

  const resp = await fetch(
    `${IG_API}/${pageId}?fields=instagram_business_account{id,username}&access_token=${token}`,
  );
  if (!resp.ok) return null;
  const data = await resp.json();
  const ig = data.instagram_business_account;
  return ig ? { id: ig.id, username: ig.username } : null;
}

export async function fetchMediaList(
  igUserId: string,
  limit = 50,
  after?: string,
): Promise<{ items: IgMediaListItem[]; nextCursor: string | null }> {
  const token = process.env.FACEBOOK_ACCESS_TOKEN!;
  const params = new URLSearchParams({
    fields:
      "id,timestamp,caption,media_type,media_product_type,permalink,thumbnail_url",
    limit: String(limit),
    access_token: token,
  });
  if (after) params.set("after", after);

  const resp = await fetch(`${IG_API}/${igUserId}/media?${params}`);
  if (!resp.ok) {
    throw new Error(
      `fetchMediaList failed: ${resp.status} ${await resp.text()}`,
    );
  }
  const data = await resp.json();

  return {
    items: (data.data ?? []).map(
      (m: {
        id: string;
        timestamp?: string;
        caption?: string;
        media_type?: string;
        media_product_type?: string;
        permalink?: string;
        thumbnail_url?: string;
      }) => ({
        id: m.id,
        ig_url: m.permalink ?? "",
        posted_at: m.timestamp ?? "",
        media_type: m.media_type ?? "UNKNOWN",
        media_product_type: m.media_product_type ?? "FEED",
        caption: m.caption ?? null,
        thumbnail_url: m.thumbnail_url ?? null,
      }),
    ),
    nextCursor: data.paging?.cursors?.after ?? null,
  };
}

export async function fetchPerMediaMetrics(
  mediaId: string,
  productType: string,
): Promise<{ metrics: IgPerMediaMetrics; mediaGone: boolean }> {
  const token = process.env.FACEBOOK_ACCESS_TOKEN!;
  const metrics = getMetricsForProductType(productType);
  const url = `${IG_API}/${mediaId}/insights?metric=${metrics.join(",")}&metric_type=total_value&access_token=${token}`;

  try {
    const resp = await fetch(url);
    if (!resp.ok) {
      const text = await resp.text();
      const gone = isMediaGoneError(text);
      if (!gone) {
        console.warn(
          `[ig-analytics] insights ${mediaId} (${productType}) ${resp.status}: ${text.slice(0, 240)}`,
        );
      }
      return { metrics: PER_MEDIA_EMPTY, mediaGone: gone };
    }
    const data = await resp.json();
    const out: IgPerMediaMetrics = { ...PER_MEDIA_EMPTY };
    for (const m of data.data ?? []) {
      const v = readMetricValue(m);
      switch (m.name) {
        case "reach":
          out.reach = v;
          break;
        case "views":
          out.views = v;
          break;
        case "likes":
          out.likes = v;
          break;
        case "comments":
          out.comments = v;
          break;
        case "shares":
          out.shares = v;
          break;
        case "saved":
          out.saves = v;
          break;
        case "total_interactions":
          out.total_interactions = v;
          break;
        case "ig_reels_avg_watch_time":
          out.avg_watch_time_ms = v;
          break;
        case "ig_reels_video_view_total_time":
          out.total_play_time_ms = v;
          break;
        case "reels_skip_rate":
          out.reels_skip_rate = v;
          break;
        case "reposts":
          out.reposts = v;
          break;
      }
    }
    return { metrics: out, mediaGone: false };
  } catch (err) {
    console.error(`[ig-analytics] fetchPerMediaMetrics(${mediaId})`, err);
    return { metrics: PER_MEDIA_EMPTY, mediaGone: false };
  }
}

// Iterate dates from sinceDate (inclusive) to untilDate (exclusive) in UTC.
function* utcDateRange(
  sinceDate: string,
  untilDate: string,
): Generator<{ date: string; sinceUnix: number; untilUnix: number }> {
  const start = new Date(sinceDate + "T00:00:00Z");
  const end = new Date(untilDate + "T00:00:00Z");
  for (
    const d = new Date(start);
    d < end;
    d.setUTCDate(d.getUTCDate() + 1)
  ) {
    const sinceUnix = Math.floor(d.getTime() / 1000);
    const untilUnix = sinceUnix + 86400;
    yield { date: d.toISOString().slice(0, 10), sinceUnix, untilUnix };
  }
}

/**
 * Fetch account-level metrics for an arbitrary range of UTC days.
 * Returns one row per day in [sinceDate, untilDate).
 *
 * Cost: 1 series call (covers whole range, multi-day) + N total_value calls
 * (one per day in the range). For backfill of 90 days = ~91 calls.
 */
export async function fetchAccountDailyRange(
  igUserId: string,
  sinceDate: string, // "YYYY-MM-DD" UTC, inclusive
  untilDate: string, // "YYYY-MM-DD" UTC, exclusive
): Promise<IgAccountDayData[]> {
  const token = process.env.FACEBOOK_ACCESS_TOKEN!;

  const rangeSinceUnix = Math.floor(
    new Date(sinceDate + "T00:00:00Z").getTime() / 1000,
  );
  const rangeUntilUnix = Math.floor(
    new Date(untilDate + "T00:00:00Z").getTime() / 1000,
  );

  // 1. Time-series calls (follower_count + reach), chunked into 30-day windows.
  // Meta enforces "There cannot be more than 30 days (2592000 s) between since
  // and until" on these metrics, so we paginate by chunks.
  const seriesByDate = new Map<
    string,
    { followers_gained: number | null; daily_reach: number | null }
  >();

  const THIRTY_DAYS_S = 30 * 86400 - 1; // -1 to stay strictly under the limit
  for (
    let chunkStart = rangeSinceUnix;
    chunkStart < rangeUntilUnix;
    chunkStart += THIRTY_DAYS_S
  ) {
    const chunkEnd = Math.min(chunkStart + THIRTY_DAYS_S, rangeUntilUnix);
    const seriesResp = await fetch(
      `${IG_API}/${igUserId}/insights?metric=follower_count,reach&period=day&since=${chunkStart}&until=${chunkEnd}&access_token=${token}`,
    );
    if (!seriesResp.ok) {
      console.warn(
        `[ig-analytics] account series chunk ${chunkStart}..${chunkEnd} failed: ${seriesResp.status} ${await seriesResp.text().catch(() => "")}`,
      );
      continue;
    }
    const seriesData = await seriesResp.json();
    for (const metric of seriesData.data ?? []) {
      for (const v of metric.values ?? []) {
        const date = (v.end_time as string).slice(0, 10);
        const row = seriesByDate.get(date) ?? {
          followers_gained: null,
          daily_reach: null,
        };
        if (metric.name === "follower_count") {
          row.followers_gained = v.value ?? null;
        }
        if (metric.name === "reach") {
          row.daily_reach = v.value ?? null;
        }
        seriesByDate.set(date, row);
      }
    }
  }

  // 2. Total-value call per day for accurate per-day breakdown
  const out: IgAccountDayData[] = [];
  for (const { date, sinceUnix, untilUnix } of utcDateRange(
    sinceDate,
    untilDate,
  )) {
    const tvResp = await fetch(
      `${IG_API}/${igUserId}/insights?metric=profile_views,accounts_engaged,total_interactions,views,website_clicks&metric_type=total_value&period=day&since=${sinceUnix}&until=${untilUnix}&access_token=${token}`,
    );

    let pv: number | null = null;
    let ae: number | null = null;
    let ti: number | null = null;
    let vw: number | null = null;
    let wc: number | null = null;

    if (tvResp.ok) {
      const tvData = await tvResp.json();
      for (const m of tvData.data ?? []) {
        const v = m.total_value?.value ?? null;
        switch (m.name) {
          case "profile_views":
            pv = v;
            break;
          case "accounts_engaged":
            ae = v;
            break;
          case "total_interactions":
            ti = v;
            break;
          case "views":
            vw = v;
            break;
          case "website_clicks":
            wc = v;
            break;
        }
      }
    } else {
      console.warn(
        `[ig-analytics] total_value ${date} failed: ${tvResp.status}`,
      );
    }

    const series = seriesByDate.get(date) ?? {
      followers_gained: null,
      daily_reach: null,
    };

    out.push({
      date,
      followers_gained: series.followers_gained,
      daily_reach: series.daily_reach,
      daily_profile_views: pv,
      daily_accounts_engaged: ae,
      daily_total_interactions: ti,
      daily_views: vw,
      daily_website_clicks: wc,
    });
  }

  return out;
}

export async function fetchAccountTotalFollowers(
  igUserId: string,
): Promise<{ total_followers: number; media_count: number }> {
  const token = process.env.FACEBOOK_ACCESS_TOKEN!;
  const resp = await fetch(
    `${IG_API}/${igUserId}?fields=followers_count,media_count&access_token=${token}`,
  );
  if (!resp.ok) return { total_followers: 0, media_count: 0 };
  const data = await resp.json();
  return {
    total_followers: data.followers_count ?? 0,
    media_count: data.media_count ?? 0,
  };
}
