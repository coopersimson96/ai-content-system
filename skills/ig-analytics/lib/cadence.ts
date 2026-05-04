/**
 * Pure cadence decision: given a post's published time and last-synced time,
 * decide whether to take a new snapshot, and what cadence label to tag it with.
 *
 * Rules (all UTC):
 * - 'hourly' if posted within the last 48h AND last sync was >55min ago
 *   (55min instead of 60 to avoid drift when cron fires slightly early)
 * - 'daily' if posted >48h ago AND last sync was >23h ago
 * - 'skip' otherwise
 *
 * Backfill is a separate flow (writes cadence='backfill' explicitly).
 */
export type Cadence = "hourly" | "daily" | "skip";

export interface CadenceInputs {
  postedAt: Date;
  lastSyncedAt: Date | null; // null means never synced
  now: Date;
}

const FIFTY_FIVE_MINUTES_MS = 55 * 60 * 1000;
const TWENTY_THREE_HOURS_MS = 23 * 60 * 60 * 1000;
const FORTY_EIGHT_HOURS_MS = 48 * 60 * 60 * 1000;

export function decideCadence(inputs: CadenceInputs): Cadence {
  const { postedAt, lastSyncedAt, now } = inputs;

  const ageMs = now.getTime() - postedAt.getTime();
  const sinceLastSyncMs = lastSyncedAt
    ? now.getTime() - lastSyncedAt.getTime()
    : Infinity;

  // Inside the 48h hot window: snapshot hourly
  if (ageMs <= FORTY_EIGHT_HOURS_MS) {
    return sinceLastSyncMs >= FIFTY_FIVE_MINUTES_MS ? "hourly" : "skip";
  }

  // Outside 48h: daily snapshot
  return sinceLastSyncMs >= TWENTY_THREE_HOURS_MS ? "daily" : "skip";
}
