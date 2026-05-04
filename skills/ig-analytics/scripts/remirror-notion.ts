/**
 * Notion-only re-mirror. Reads ig_media + latest snapshot from Supabase,
 * upserts a Notion analytics page per post. Use after granting the Notion
 * integration access to the new Content Analytics DB, or after schema
 * changes to the Notion DB.
 *
 * Idempotent: matches on existing IG Media ID, updates or creates.
 */
import { getSupabaseAdmin } from "../src/lib/supabase.ts";
import {
  findAnalyticsPageByMediaId,
  findScriptByInstagramUrl,
  stampScriptWithMediaId,
  upsertAnalyticsPage,
} from "../src/lib/notion-analytics.ts";

interface MediaWithLatest {
  id: string;
  ig_url: string;
  posted_at: string;
  media_type: string;
  media_product_type: string;
  caption: string | null;
  notion_analytics_page_id: string | null;
  notion_script_id: string | null;
  first_seen_at: string;
  last_synced_at: string | null;
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
}

async function main() {
  const supabase = getSupabaseAdmin()!;

  // Get all non-deleted media joined to latest snapshot
  const { data, error } = await supabase
    .from("ig_media_latest")
    .select(
      "id, ig_url, posted_at, media_type, media_product_type, caption, reach, views, likes, comments, shares, saves, total_interactions, avg_watch_time_ms, total_play_time_ms, reels_skip_rate, notion_script_id",
    )
    .order("posted_at", { ascending: false });

  if (error) throw new Error("Failed to query ig_media_latest: " + error.message);
  if (!data || data.length === 0) {
    console.log("No media found.");
    return;
  }

  console.log(`[remirror] processing ${data.length} posts`);

  const ids = data.map((d) => d.id);
  const { data: mediaMeta } = await supabase
    .from("ig_media")
    .select("id, notion_analytics_page_id, first_seen_at, last_synced_at")
    .in("id", ids);

  const metaById = new Map(
    (mediaMeta ?? []).map((m: { id: string; notion_analytics_page_id: string | null; first_seen_at: string; last_synced_at: string | null }) => [m.id, m]),
  );

  let processed = 0;
  let created = 0;
  let updated = 0;
  let failed = 0;
  let scriptLinked = 0;

  for (const row of data as MediaWithLatest[]) {
    processed++;
    const meta = metaById.get(row.id);
    const firstSeenAt = meta?.first_seen_at ?? row.posted_at;
    const lastSyncedAt = meta?.last_synced_at ?? new Date().toISOString();
    let notionPageId = meta?.notion_analytics_page_id ?? null;
    let notionScriptId = row.notion_script_id;

    // Resolve script linkage if missing
    if (!notionScriptId && row.ig_url) {
      notionScriptId = await findScriptByInstagramUrl(row.ig_url);
      if (notionScriptId) {
        await stampScriptWithMediaId(notionScriptId, row.id);
        await supabase
          .from("ig_media")
          .update({ notion_script_id: notionScriptId })
          .eq("id", row.id);
        scriptLinked++;
      }
    }

    // Look for existing Notion page if we don't have a known id
    if (!notionPageId) {
      notionPageId = await findAnalyticsPageByMediaId(row.id);
    }
    const wasNew = !notionPageId;

    const { count: snapshotCount } = await supabase
      .from("ig_media_snapshots")
      .select("*", { count: "exact", head: true })
      .eq("media_id", row.id);

    const upsertedPageId = await upsertAnalyticsPage(
      {
        igMediaId: row.id,
        igUrl: row.ig_url,
        caption: row.caption,
        postedAt: row.posted_at,
        mediaType: row.media_type,
        mediaProductType: row.media_product_type,
        metrics: {
          reach: row.reach,
          views: row.views,
          likes: row.likes,
          comments: row.comments,
          shares: row.shares,
          saves: row.saves,
          total_interactions: row.total_interactions,
          avg_watch_time_ms: row.avg_watch_time_ms,
          total_play_time_ms: row.total_play_time_ms,
          reels_skip_rate: row.reels_skip_rate,
          reposts: null,
        },
        snapshotCount: snapshotCount ?? 1,
        firstSeenAt,
        lastSyncedAt,
        deletedAt: null,
        notionScriptId,
      },
      notionPageId,
    );

    if (!upsertedPageId) {
      failed++;
      console.log(`  [${processed}/${data.length}] ${row.id} FAILED`);
      continue;
    }

    if (wasNew) {
      created++;
      await supabase
        .from("ig_media")
        .update({ notion_analytics_page_id: upsertedPageId })
        .eq("id", row.id);
    } else {
      updated++;
    }

    console.log(
      `  [${processed}/${data.length}] ${row.id} ${wasNew ? "CREATED" : "UPDATED"} reach=${row.reach ?? "·"} views=${row.views ?? "·"}${notionScriptId ? " [linked]" : ""}`,
    );
  }

  console.log("");
  console.log("=== REMIRROR COMPLETE ===");
  console.log(`processed:           ${processed}`);
  console.log(`pages created:       ${created}`);
  console.log(`pages updated:       ${updated}`);
  console.log(`failed:              ${failed}`);
  console.log(`scripts auto-linked: ${scriptLinked}`);
}

main().catch((e) => {
  console.error("REMIRROR FAILED:", e);
  process.exit(1);
});
