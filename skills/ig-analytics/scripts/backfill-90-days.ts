/**
 * One-shot backfill: pulls the last 90 days of IG media + insights into
 * Supabase + Notion. Writes a single `cadence='backfill'` snapshot per post.
 *
 * Run from repo root:
 *   node --env-file=.env.local --experimental-strip-types --no-warnings \
 *     scripts/backfill-90-days.ts
 *
 * Idempotent: rerunning will upsert media and insert another backfill snapshot.
 * If you want a clean re-run, delete from ig_media_snapshots where cadence='backfill'.
 *
 * Throttle: 1 call/sec on insights to stay well under Meta's ~200/hr limit.
 */
import { getSupabaseAdmin } from "../src/lib/supabase.ts";
import {
  fetchInstagramAccount,
  fetchMediaList,
  fetchPerMediaMetrics,
  fetchAccountDailyRange,
  fetchAccountTotalFollowers,
  type IgMediaListItem,
} from "../src/lib/instagram-analytics.ts";
import {
  findAnalyticsPageByMediaId,
  findScriptByInstagramUrl,
  stampScriptWithMediaId,
  upsertAnalyticsPage,
} from "../src/lib/notion-analytics.ts";

const NINETY_DAYS_MS = 90 * 24 * 60 * 60 * 1000;
const THROTTLE_MS = 1000;

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function main() {
  const supabase = getSupabaseAdmin();
  if (!supabase) throw new Error("Supabase admin client unavailable - check SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY");

  const account = await fetchInstagramAccount();
  if (!account) throw new Error("IG account not found");
  console.log(`[backfill] account = @${account.username} (${account.id})`);

  // 1. Paginate media until we hit a post older than 90 days
  const cutoffMs = Date.now() - NINETY_DAYS_MS;
  const cutoffIso = new Date(cutoffMs).toISOString();
  console.log(`[backfill] cutoff = ${cutoffIso}`);

  const allMedia: IgMediaListItem[] = [];
  let nextCursor: string | undefined;

  do {
    const page = await fetchMediaList(account.id, 50, nextCursor);
    let stop = false;
    for (const item of page.items) {
      if (new Date(item.posted_at).getTime() < cutoffMs) {
        stop = true;
        break;
      }
      allMedia.push(item);
    }
    if (stop || !page.nextCursor) break;
    nextCursor = page.nextCursor;
  } while (true);

  console.log(`[backfill] collected ${allMedia.length} posts within 90 days`);

  // 2. Upsert all into ig_media
  for (const item of allMedia) {
    const { error } = await supabase.from("ig_media").upsert(
      {
        id: item.id,
        ig_url: item.ig_url,
        posted_at: item.posted_at,
        media_type: item.media_type,
        media_product_type: item.media_product_type,
        caption: item.caption,
        thumbnail_url: item.thumbnail_url,
      },
      { onConflict: "id" },
    );
    if (error) console.error(`[backfill] upsert ${item.id}:`, error.message);
  }
  console.log(`[backfill] upserted ${allMedia.length} ig_media rows`);

  // 3. For each post: insights + snapshot + Notion mirror
  let processed = 0;
  let failed = 0;
  let gone = 0;
  let notionFailed = 0;

  for (const item of allMedia) {
    processed++;
    const { metrics, mediaGone } = await fetchPerMediaMetrics(
      item.id,
      item.media_product_type,
    );

    if (mediaGone) {
      await supabase
        .from("ig_media")
        .update({ deleted_at: new Date().toISOString() })
        .eq("id", item.id);
      gone++;
      console.log(`  [${processed}/${allMedia.length}] ${item.id} GONE`);
      await sleep(THROTTLE_MS);
      continue;
    }

    const syncedAt = new Date().toISOString();

    const { error: snapErr } = await supabase.from("ig_media_snapshots").insert({
      media_id: item.id,
      cadence: "backfill",
      reach: metrics.reach,
      views: metrics.views,
      likes: metrics.likes,
      comments: metrics.comments,
      shares: metrics.shares,
      saves: metrics.saves,
      total_interactions: metrics.total_interactions,
      avg_watch_time_ms: metrics.avg_watch_time_ms,
      total_play_time_ms: metrics.total_play_time_ms,
      reels_skip_rate: metrics.reels_skip_rate,
      reposts: metrics.reposts,
    });

    if (snapErr) {
      console.error(`  [${processed}/${allMedia.length}] ${item.id} snapshot fail:`, snapErr.message);
      failed++;
      await sleep(THROTTLE_MS);
      continue;
    }

    await supabase
      .from("ig_media")
      .update({ last_synced_at: syncedAt })
      .eq("id", item.id);

    // Resolve Notion linkages
    let notionScriptId: string | null = null;
    if (item.ig_url) {
      notionScriptId = await findScriptByInstagramUrl(item.ig_url);
      if (notionScriptId) {
        await stampScriptWithMediaId(notionScriptId, item.id);
        await supabase
          .from("ig_media")
          .update({ notion_script_id: notionScriptId })
          .eq("id", item.id);
      }
    }

    const existingPageId = await findAnalyticsPageByMediaId(item.id);

    const upsertedPageId = await upsertAnalyticsPage(
      {
        igMediaId: item.id,
        igUrl: item.ig_url,
        caption: item.caption,
        postedAt: item.posted_at,
        mediaType: item.media_type,
        mediaProductType: item.media_product_type,
        metrics,
        snapshotCount: 1,
        firstSeenAt: syncedAt,
        lastSyncedAt: syncedAt,
        deletedAt: null,
        notionScriptId,
      },
      existingPageId,
    );

    if (upsertedPageId) {
      await supabase
        .from("ig_media")
        .update({ notion_analytics_page_id: upsertedPageId })
        .eq("id", item.id);
    } else {
      notionFailed++;
    }

    console.log(
      `  [${processed}/${allMedia.length}] ${item.id} reach=${metrics.reach ?? "·"} views=${metrics.views ?? "·"} interactions=${metrics.total_interactions ?? "·"}${notionScriptId ? " [linked-to-script]" : ""}`,
    );

    await sleep(THROTTLE_MS);
  }

  // 4. Backfill account_daily for last 90 days
  const today = new Date().toISOString().slice(0, 10);
  const ninetyAgo = new Date(Date.now() - NINETY_DAYS_MS).toISOString().slice(0, 10);
  console.log(`[backfill] account_daily ${ninetyAgo} → ${today} (one call per day)`);

  const days = await fetchAccountDailyRange(account.id, ninetyAgo, today);
  console.log(`[backfill] fetched ${days.length} day-rows`);

  for (const d of days) {
    const { error } = await supabase.from("ig_account_daily").upsert(
      {
        date: d.date,
        followers_gained: d.followers_gained,
        daily_reach: d.daily_reach,
        daily_profile_views: d.daily_profile_views,
        daily_accounts_engaged: d.daily_accounts_engaged,
        daily_total_interactions: d.daily_total_interactions,
        daily_views: d.daily_views,
        daily_website_clicks: d.daily_website_clicks,
        updated_at: new Date().toISOString(),
      },
      { onConflict: "date" },
    );
    if (error) console.error(`  ${d.date} fail:`, error.message);
  }

  // 5. Account total snapshot
  const totals = await fetchAccountTotalFollowers(account.id);
  await supabase.from("ig_account_snapshots").insert({
    total_followers: totals.total_followers,
    media_count: totals.media_count,
  });
  await supabase
    .from("ig_account_daily")
    .update({ total_followers: totals.total_followers })
    .eq("date", today);

  console.log("");
  console.log("=== BACKFILL COMPLETE ===");
  console.log(`media processed:      ${processed}`);
  console.log(`media gone (deleted): ${gone}`);
  console.log(`snapshot failures:    ${failed}`);
  console.log(`notion failures:      ${notionFailed}`);
  console.log(`account days written: ${days.length}`);
  console.log(`current followers:    ${totals.total_followers}`);
}

main().catch((e) => {
  console.error("BACKFILL FAILED:", e);
  process.exit(1);
});
