/**
 * Notion mirror for the Content Analytics DB.
 *
 * Source of truth is Supabase. Notion writes are best-effort: if a write fails,
 * we log and move on so a Notion outage doesn't block the data pipeline.
 *
 * Caption truncation handles the UTF-16 emoji length gotcha: Notion enforces a
 * 2000-char limit counted in UTF-16 code units. Emoji-heavy captions can blow
 * past it. We truncate to a small visual length using grapheme segmentation.
 */
import { Client } from "@notionhq/client";
import type { IgPerMediaMetrics } from "./instagram-analytics";

const ANALYTICS_DATASOURCE = process.env.NOTION_ANALYTICS_DATASOURCE!;
const SCRIPT_DATASOURCE = process.env.NOTION_SCRIPT_DATASOURCE!;

let cachedClient: Client | null = null;
function notion(): Client {
  if (!cachedClient) {
    cachedClient = new Client({ auth: process.env.NOTION_TOKEN });
  }
  return cachedClient;
}

export interface AnalyticsPageInput {
  igMediaId: string;
  igUrl: string;
  caption: string | null;
  postedAt: string; // ISO-8601
  mediaType: string;
  mediaProductType: string;
  metrics: IgPerMediaMetrics;
  snapshotCount: number;
  firstSeenAt: string;
  lastSyncedAt: string;
  deletedAt: string | null;
  notionScriptId: string | null;
  // Performance assessment (optional; only set when an assessment runs)
  performanceTier?: "Outlier" | "Average" | "Underperformer" | "Untested" | null;
  performanceNotes?: string | null;
  tierAssessedAt?: string | null;
  notesAssessedAt?: string | null;
  notesModel?: string | null;
}

/**
 * Truncate a string to ~maxGraphemes visible characters. Uses Intl.Segmenter
 * when available (Node 18+) - this counts user-perceived characters (graphemes)
 * not UTF-16 code units, so emoji and combining marks count as 1 each.
 *
 * Notion's 2000-char title limit is in UTF-16 code units. By staying well
 * under that with grapheme-counted truncation, we stay safe even when emoji
 * each take 2 UTF-16 units.
 */
export function truncateCaption(s: string | null, maxGraphemes = 80): string {
  if (!s) return "";
  try {
    const seg = new Intl.Segmenter(undefined, { granularity: "grapheme" });
    const parts = Array.from(seg.segment(s));
    if (parts.length <= maxGraphemes) return s;
    return parts.slice(0, maxGraphemes).map((p) => p.segment).join("") + "…";
  } catch {
    // Fallback: simple substring on UTF-16 (overcounts emoji but safe)
    return s.length > maxGraphemes ? s.slice(0, maxGraphemes) + "…" : s;
  }
}

/**
 * Find an existing Notion analytics page by its IG Media ID.
 * Returns the page id or null.
 */
export async function findAnalyticsPageByMediaId(
  igMediaId: string,
): Promise<string | null> {
  try {
    const resp = await notion().dataSources.query({
      data_source_id: ANALYTICS_DATASOURCE,
      filter: {
        property: "IG Media ID",
        rich_text: { equals: igMediaId },
      },
      page_size: 1,
    });
    const first = resp.results[0] as { id?: string } | undefined;
    return first?.id ?? null;
  } catch (err) {
    console.error(
      `[notion-analytics] findAnalyticsPageByMediaId(${igMediaId}) failed:`,
      err,
    );
    return null;
  }
}

/**
 * Find a Script Library page whose Instagram Post URL matches the given URL.
 * Used to populate the notion_script_id link on first-time analytics rows.
 *
 * Optional: if you don't keep a separate Script Library DB, you can stub this
 * to always return null. The pipeline will still write analytics rows fine.
 */
export async function findScriptByInstagramUrl(
  igUrl: string,
): Promise<string | null> {
  if (!SCRIPT_DATASOURCE) return null;
  try {
    const resp = await notion().dataSources.query({
      data_source_id: SCRIPT_DATASOURCE,
      filter: {
        property: "Instagram Post URL",
        url: { equals: igUrl },
      },
      page_size: 1,
    });
    const first = resp.results[0] as { id?: string } | undefined;
    return first?.id ?? null;
  } catch (err) {
    console.error(
      `[notion-analytics] findScriptByInstagramUrl(${igUrl}) failed:`,
      err,
    );
    return null;
  }
}

/**
 * Stamp the matching Script Library row with the IG Media ID, so future
 * joins can use that as a hard key. Best-effort.
 */
export async function stampScriptWithMediaId(
  scriptPageId: string,
  igMediaId: string,
): Promise<void> {
  try {
    await notion().pages.update({
      page_id: scriptPageId,
      properties: {
        "IG Media ID": {
          rich_text: [{ type: "text", text: { content: igMediaId } }],
        },
      },
    });
  } catch (err) {
    console.error(
      `[notion-analytics] stampScriptWithMediaId(${scriptPageId}) failed:`,
      err,
    );
  }
}

function buildProperties(input: AnalyticsPageInput) {
  const m = input.metrics;
  const captionExcerpt = truncateCaption(input.caption);

  const props: Record<string, unknown> = {
    "Caption Excerpt": {
      title: [
        {
          type: "text",
          text: { content: captionExcerpt || `[${input.igMediaId}]` },
        },
      ],
    },
    "IG Media ID": {
      rich_text: [{ type: "text", text: { content: input.igMediaId } }],
    },
    "IG URL": { url: input.igUrl || null },
    "Posted At": { date: { start: input.postedAt } },
    "Media Type": { select: { name: input.mediaType } },
    "Media Product Type": { select: { name: input.mediaProductType } },
    "Latest Reach": { number: m.reach },
    "Latest Views": { number: m.views },
    "Latest Likes": { number: m.likes },
    "Latest Comments": { number: m.comments },
    "Latest Shares": { number: m.shares },
    "Latest Saves": { number: m.saves },
    "Latest Total Interactions": { number: m.total_interactions },
    "Avg Watch Time (s)": {
      number: m.avg_watch_time_ms != null ? m.avg_watch_time_ms / 1000 : null,
    },
    "Total Watch Time (s)": {
      number: m.total_play_time_ms != null ? m.total_play_time_ms / 1000 : null,
    },
    "Skip Rate": { number: m.reels_skip_rate },
    "Snapshot Count": { number: input.snapshotCount },
    "First Seen At": { date: { start: input.firstSeenAt } },
    "Last Synced At": { date: { start: input.lastSyncedAt } },
    "Deleted At": input.deletedAt ? { date: { start: input.deletedAt } } : { date: null },
  };

  // Only write assessment fields when explicitly provided. Otherwise leave
  // existing Notion values untouched (so manual edits aren't clobbered by
  // the cron sync - only the assessment script writes these).
  if (input.performanceTier !== undefined) {
    props["Performance Tier"] = input.performanceTier
      ? { select: { name: input.performanceTier } }
      : { select: null };
  }
  if (input.performanceNotes !== undefined) {
    props["Performance Notes"] = {
      rich_text: input.performanceNotes
        ? [{ type: "text", text: { content: input.performanceNotes } }]
        : [],
    };
  }
  if (input.tierAssessedAt !== undefined) {
    props["Tier Assessed At"] = input.tierAssessedAt
      ? { date: { start: input.tierAssessedAt } }
      : { date: null };
  }
  if (input.notesAssessedAt !== undefined) {
    props["Notes Assessed At"] = input.notesAssessedAt
      ? { date: { start: input.notesAssessedAt } }
      : { date: null };
  }
  if (input.notesModel !== undefined) {
    props["Notes Model"] = {
      rich_text: input.notesModel
        ? [{ type: "text", text: { content: input.notesModel } }]
        : [],
    };
  }

  return props;
}

/**
 * Upsert: create or update the Notion analytics page. Returns the page id
 * (or null on failure - failure is logged but never thrown).
 */
export async function upsertAnalyticsPage(
  input: AnalyticsPageInput,
  existingPageId: string | null,
): Promise<string | null> {
  try {
    if (existingPageId) {
      await notion().pages.update({
        page_id: existingPageId,
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        properties: buildProperties(input) as any,
      });
      return existingPageId;
    }

    const created = await notion().pages.create({
      parent: { data_source_id: ANALYTICS_DATASOURCE },
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      properties: buildProperties(input) as any,
    });
    return (created as { id: string }).id;
  } catch (err) {
    console.error(
      `[notion-analytics] upsertAnalyticsPage(${input.igMediaId}) failed:`,
      err,
    );
    return null;
  }
}
