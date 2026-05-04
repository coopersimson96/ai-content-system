/**
 * Re-fetch and upsert ig_account_daily for the last 90 days. Use after
 * patching fetchAccountDailyRange (e.g., to fix a 30-day series window bug).
 */
import { getSupabaseAdmin } from "../src/lib/supabase.ts";
import {
  fetchInstagramAccount,
  fetchAccountDailyRange,
} from "../src/lib/instagram-analytics.ts";

async function main() {
  const supabase = getSupabaseAdmin()!;
  const account = (await fetchInstagramAccount())!;

  const today = new Date().toISOString().slice(0, 10);
  const ninetyAgo = new Date(Date.now() - 90 * 86400_000)
    .toISOString()
    .slice(0, 10);

  console.log(`[refresh] fetching ${ninetyAgo} → ${today}`);
  const days = await fetchAccountDailyRange(account.id, ninetyAgo, today);
  console.log(`[refresh] got ${days.length} day-rows`);

  let withSeries = 0;
  for (const d of days) {
    if (d.followers_gained !== null) withSeries++;
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
    if (error) console.error(`  ${d.date} err:`, error.message);
  }

  console.log("");
  console.log("=== REFRESH COMPLETE ===");
  console.log(`days written:                ${days.length}`);
  console.log(`days with follower series:   ${withSeries}`);
}

main().catch((e) => {
  console.error("REFRESH FAILED:", e);
  process.exit(1);
});
