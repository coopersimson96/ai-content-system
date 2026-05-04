/**
 * Smoke-test the instagram-analytics module against the live Graph API.
 * Run from the repo root:
 *   node --env-file=.env.local --experimental-strip-types --no-warnings scripts/smoke-test.ts
 */
import {
  fetchInstagramAccount,
  fetchMediaList,
  fetchPerMediaMetrics,
  fetchAccountDailyRange,
  fetchAccountTotalFollowers,
} from "../src/lib/instagram-analytics.ts";

async function main() {
  const account = await fetchInstagramAccount();
  console.log("[1] account =", account);
  if (!account) {
    console.error("FAILED: no IG account. Check FACEBOOK_ACCESS_TOKEN + FACEBOOK_PAGE_ID.");
    process.exit(1);
  }

  const totals = await fetchAccountTotalFollowers(account.id);
  console.log("[2] account totals =", totals);

  const list = await fetchMediaList(account.id, 5);
  console.log("[3] media list (5 most recent):");
  for (const m of list.items) {
    console.log("   ", m.posted_at.slice(0, 10), m.media_type, m.media_product_type, m.id, m.ig_url);
  }

  if (list.items.length === 0) {
    console.error("FAILED: no media returned.");
    process.exit(1);
  }

  // Per-media metrics for the first item (just-posted, will be sparse)
  const first = list.items[0];
  const r1 = await fetchPerMediaMetrics(first.id, first.media_product_type);
  console.log("[4a] just-posted reel:", first.id, first.media_product_type);
  console.log("     gone =", r1.mediaGone, "metrics =", r1.metrics);

  // Per-media metrics for an older reel (5th item, presumably mature)
  if (list.items.length >= 5) {
    const older = list.items[4];
    const r2 = await fetchPerMediaMetrics(older.id, older.media_product_type);
    console.log("[4b] older reel posted at", older.posted_at);
    console.log("     gone =", r2.mediaGone, "metrics =", r2.metrics);
  }

  // Account daily range - last 7 days
  const today = new Date().toISOString().slice(0, 10);
  const sevenDaysAgo = new Date(Date.now() - 7 * 86400_000).toISOString().slice(0, 10);
  console.log("[5] account daily range:", sevenDaysAgo, "→", today);
  const days = await fetchAccountDailyRange(account.id, sevenDaysAgo, today);
  for (const d of days) {
    console.log(
      "   ",
      d.date,
      "follows_gained=" + d.followers_gained,
      "reach=" + d.daily_reach,
      "profile_views=" + d.daily_profile_views,
      "views=" + d.daily_views,
    );
  }

  console.log("\nSMOKE TEST PASSED");
}

main().catch((e) => {
  console.error("SMOKE TEST FAILED:", e);
  process.exit(1);
});
