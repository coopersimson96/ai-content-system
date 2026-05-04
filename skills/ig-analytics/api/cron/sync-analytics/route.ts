/**
 * Hourly analytics sync. Pulls IG insights, writes snapshots to Supabase,
 * mirrors latest values to Notion. Resumable: if it times out, the next
 * cron tick picks up where this one left off (cadence check skips
 * recently-synced posts naturally).
 *
 * Source of truth: Supabase. Notion writes are best-effort.
 */
import { NextResponse } from "next/server";
import { getSupabaseAdmin } from "@/lib/supabase";
import { decideCadence } from "@/lib/cadence";
import {
  fetchInstagramAccount,
  fetchMediaList,
  fetchPerMediaMetrics,
  fetchAccountDailyRange,
  fetchAccountTotalFollowers,
} from "@/lib/instagram-analytics";
import {
  findAnalyticsPageByMediaId,
  findScriptByInstagramUrl,
  stampScriptWithMediaId,
  upsertAnalyticsPage,
} from "@/lib/notion-analytics";

export const dynamic = "force-dynamic";
export const maxDuration = 60;

interface MediaRow {
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
}

export async function GET(request: Request) {
  // Cron secret auth - matches Vercel cron Authorization header
  const authHeader = request.headers.get("authorization");
  const cronSecret = process.env.CRON_SECRET;
  if (cronSecret && authHeader !== `Bearer ${cronSecret}`) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const supabase = getSupabaseAdmin();
  if (!supabase) {
    return NextResponse.json(
      { error: "Supabase not configured" },
      { status: 500 },
    );
  }

  const startTime = Date.now();
  const stats = {
    new_media: 0,
    hourly_snapshots: 0,
    daily_snapshots: 0,
    skipped: 0,
    media_gone: 0,
    notion_updates: 0,
    notion_failures: 0,
    errors: 0,
  };

  try {
    // 1. Get IG account
    const account = await fetchInstagramAccount();
    if (!account) {
      return NextResponse.json(
        { error: "IG account not found - check FB token" },
        { status: 500 },
      );
    }

    // 2. Discover new posts: fetch the 50 most recent media, upsert into ig_media
    const { items: recent } = await fetchMediaList(account.id, 50);
    for (const item of recent) {
      const { error: upsertErr } = await supabase.from("ig_media").upsert(
        {
          id: item.id,
          ig_url: item.ig_url,
          posted_at: item.posted_at,
          media_type: item.media_type,
          media_product_type: item.media_product_type,
          caption: item.caption,
          thumbnail_url: item.thumbnail_url,
          // first_seen_at left to DEFAULT now() on insert; not overwritten on update
        },
        { onConflict: "id", ignoreDuplicates: false },
      );
      if (upsertErr) {
        console.error(`[sync-analytics] upsert ig_media ${item.id}:`, upsertErr);
        stats.errors++;
      }
    }

    // Track which IDs are "new this cron tick" (created within last 60s)
    const { count: newCount } = await supabase
      .from("ig_media")
      .select("*", { count: "exact", head: true })
      .gte("first_seen_at", new Date(Date.now() - 60_000).toISOString());
    stats.new_media = newCount ?? 0;

    // 3. Walk the full universe of non-deleted media
    const { data: universe, error: queryErr } = await supabase
      .from("ig_media")
      .select(
        "id, ig_url, posted_at, media_type, media_product_type, caption, notion_analytics_page_id, notion_script_id, first_seen_at, last_synced_at",
      )
      .is("deleted_at", null)
      .order("posted_at", { ascending: false });

    if (queryErr) {
      console.error("[sync-analytics] universe query:", queryErr);
      return NextResponse.json({ error: "DB read failed" }, { status: 500 });
    }

    const now = new Date();

    for (const media of (universe ?? []) as MediaRow[]) {
      const cadence = decideCadence({
        postedAt: new Date(media.posted_at),
        lastSyncedAt: media.last_synced_at
          ? new Date(media.last_synced_at)
          : null,
        now,
      });

      if (cadence === "skip") {
        stats.skipped++;
        continue;
      }

      // Fetch fresh insights
      const { metrics, mediaGone } = await fetchPerMediaMetrics(
        media.id,
        media.media_product_type,
      );

      if (mediaGone) {
        await supabase
          .from("ig_media")
          .update({ deleted_at: new Date().toISOString() })
          .eq("id", media.id);
        stats.media_gone++;
        continue;
      }

      // Write snapshot
      const { error: snapErr } = await supabase.from("ig_media_snapshots").insert({
        media_id: media.id,
        cadence,
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
        console.error(
          `[sync-analytics] snapshot insert ${media.id}:`,
          snapErr,
        );
        stats.errors++;
        continue;
      }

      // Update last_synced_at AFTER successful snapshot
      const syncedAt = new Date().toISOString();
      await supabase
        .from("ig_media")
        .update({ last_synced_at: syncedAt })
        .eq("id", media.id);

      // Get fresh snapshot count for the Notion page
      const { count: snapshotCount } = await supabase
        .from("ig_media_snapshots")
        .select("*", { count: "exact", head: true })
        .eq("media_id", media.id);

      // Resolve Notion linkages
      let notionScriptId = media.notion_script_id;
      if (!notionScriptId && media.ig_url) {
        notionScriptId = await findScriptByInstagramUrl(media.ig_url);
        if (notionScriptId) {
          await stampScriptWithMediaId(notionScriptId, media.id);
          await supabase
            .from("ig_media")
            .update({ notion_script_id: notionScriptId })
            .eq("id", media.id);
        }
      }

      let notionPageId = media.notion_analytics_page_id;
      if (!notionPageId) {
        notionPageId = await findAnalyticsPageByMediaId(media.id);
      }

      const upsertedPageId = await upsertAnalyticsPage(
        {
          igMediaId: media.id,
          igUrl: media.ig_url,
          caption: media.caption,
          postedAt: media.posted_at,
          mediaType: media.media_type,
          mediaProductType: media.media_product_type,
          metrics,
          snapshotCount: snapshotCount ?? 1,
          firstSeenAt: media.first_seen_at,
          lastSyncedAt: syncedAt,
          deletedAt: null,
          notionScriptId,
        },
        notionPageId,
      );

      if (upsertedPageId) {
        if (upsertedPageId !== media.notion_analytics_page_id) {
          await supabase
            .from("ig_media")
            .update({ notion_analytics_page_id: upsertedPageId })
            .eq("id", media.id);
        }
        stats.notion_updates++;
      } else {
        stats.notion_failures++;
      }

      if (cadence === "hourly") stats.hourly_snapshots++;
      else stats.daily_snapshots++;
    }

    // 4. Refresh account-level daily for last 3 days (idempotent upsert)
    const today = new Date().toISOString().slice(0, 10);
    const threeDaysAgo = new Date(Date.now() - 3 * 86400_000)
      .toISOString()
      .slice(0, 10);
    const days = await fetchAccountDailyRange(account.id, threeDaysAgo, today);
    let accountDaysWritten = 0;
    for (const d of days) {
      const { error: dailyErr } = await supabase
        .from("ig_account_daily")
        .upsert(
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
      if (dailyErr) {
        console.error(`[sync-analytics] account_daily ${d.date}:`, dailyErr);
        stats.errors++;
      } else {
        accountDaysWritten++;
      }
    }

    // 5. Account snapshot (total followers + media count)
    const totals = await fetchAccountTotalFollowers(account.id);
    await supabase.from("ig_account_snapshots").insert({
      total_followers: totals.total_followers,
      media_count: totals.media_count,
    });

    // Backfill total_followers onto today's account_daily row
    if (days.length > 0) {
      await supabase
        .from("ig_account_daily")
        .update({ total_followers: totals.total_followers })
        .eq("date", today);
    }

    const duration = Date.now() - startTime;
    return NextResponse.json({
      success: true,
      duration_ms: duration,
      account_days_written: accountDaysWritten,
      total_followers: totals.total_followers,
      stats,
    });
  } catch (err) {
    console.error("[sync-analytics] fatal error:", err);
    return NextResponse.json(
      { success: false, error: String(err), stats },
      { status: 500 },
    );
  }
}
