#!/usr/bin/env python3
"""
Auto-schedule Beehiiv newsletter drafts into the next available send slot.

Default rules:
- Send time: 9:00 AM EST (auto-converted to UTC)
- Send days: Every day (customize SEND_DAYS below for Tue/Thu only, etc.)
- Skip dates that already have a scheduled post

Usage:
    python3 auto_schedule.py --post-id post_xxx          # Schedule a specific draft
    python3 auto_schedule.py --post-id post_xxx --dry    # Preview without scheduling
    python3 auto_schedule.py --post-id post_xxx --date 2026-04-01  # Override date
    python3 auto_schedule.py --backfill                  # Queue all unscheduled drafts
    python3 auto_schedule.py --backfill --dry            # Preview backfill plan
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))
from beehiiv_api import BeehiivClient

EST = ZoneInfo("America/New_York")

# ==========================================================================
# CUSTOMIZE: Which days can emails go out, and what time?
# ==========================================================================
# Python weekday numbers: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
# Default is every day. Tue/Thu only would be {1, 3}.
SEND_DAYS = {0, 1, 2, 3, 4, 5, 6}
SEND_HOUR_EST = 9  # 9 AM EST is a proven high-open-rate slot for most creators


def get_send_time_utc(date):
    """Convert a date to 9:00 AM EST/EDT in UTC."""
    local_dt = datetime(date.year, date.month, date.day, SEND_HOUR_EST, 0, 0, tzinfo=EST)
    return local_dt.astimezone(timezone.utc)


def get_occupied_dates(client):
    """Fetch dates that already have scheduled or confirmed posts."""
    occupied = set()
    for status in ("scheduled", "confirmed"):
        posts = client.list_posts(status=status, limit=50)
        for post in posts:
            schedule_at = post.get("schedule_at") or post.get("publish_date")
            if schedule_at:
                try:
                    if isinstance(schedule_at, (int, float)):
                        dt = datetime.fromtimestamp(schedule_at, tz=timezone.utc)
                    else:
                        dt = datetime.fromisoformat(schedule_at.replace("Z", "+00:00"))
                    occupied.add(dt.date())
                except (ValueError, TypeError, OSError):
                    pass
    return occupied


def find_next_slot(occupied_dates, after_date=None):
    """Find the next available send day that isn't already taken."""
    if after_date is None:
        after_date = datetime.now(EST).date()

    candidate = after_date + timedelta(days=1)
    for _ in range(60):
        if candidate.weekday() in SEND_DAYS and candidate not in occupied_dates:
            return candidate
        candidate += timedelta(days=1)

    raise RuntimeError("No available send slot found in the next 60 days")


def schedule_draft(client, post_id, send_date=None, dry=False):
    """Schedule a single draft. Returns (post_title, scheduled_date_str)."""
    post = client.get_post(post_id)
    title = post.get("title", post_id)
    status = post.get("status", "unknown")

    if status not in ("draft", "archived"):
        print(f"  Skipping '{title}' - status is '{status}', not a draft")
        return None, None

    occupied = get_occupied_dates(client)

    if send_date:
        if send_date in occupied:
            print(f"  WARNING: {send_date} already has a scheduled post")
        slot_date = send_date
    else:
        slot_date = find_next_slot(occupied)

    send_utc = get_send_time_utc(slot_date)
    send_iso = send_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    send_local = send_utc.astimezone(EST).strftime("%A %b %d, %Y at %I:%M %p %Z")

    if dry:
        print(f"  [DRY RUN] Would schedule '{title}' for {send_local}")
        return title, slot_date.isoformat()

    client.schedule_post(post_id, send_iso)
    print(f"  Scheduled '{title}' for {send_local}")
    return title, slot_date.isoformat()


def backfill_drafts(client, dry=False):
    """Find all drafts and schedule them in order."""
    drafts = client.list_posts(status="draft", limit=50)
    if not drafts:
        print("No drafts found to schedule.")
        return []

    print(f"Found {len(drafts)} draft(s) to schedule:\n")

    occupied = get_occupied_dates(client)
    results = []
    last_scheduled = None

    for draft in drafts:
        post_id = draft.get("id")
        title = draft.get("title", post_id)

        after_date = last_scheduled if last_scheduled else datetime.now(EST).date()
        slot_date = find_next_slot(occupied, after_date=after_date)

        send_utc = get_send_time_utc(slot_date)
        send_iso = send_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        send_local = send_utc.astimezone(EST).strftime("%A %b %d, %Y at %I:%M %p %Z")

        if dry:
            print(f"  [DRY RUN] '{title}' -> {send_local}")
        else:
            client.schedule_post(post_id, send_iso)
            print(f"  Scheduled '{title}' -> {send_local}")

        occupied.add(slot_date)
        last_scheduled = slot_date
        results.append({
            "post_id": post_id,
            "title": title,
            "send_date": slot_date.isoformat(),
            "send_local": send_local,
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="Auto-schedule newsletter drafts")
    parser.add_argument("--post-id", help="Schedule a specific draft by post ID")
    parser.add_argument("--date", help="Override send date (YYYY-MM-DD)")
    parser.add_argument("--dry", action="store_true", help="Preview without scheduling")
    parser.add_argument("--backfill", action="store_true", help="Schedule all unscheduled drafts")
    parser.add_argument("--json", action="store_true", help="Output results as JSON (for piping)")
    args = parser.parse_args()

    if not args.post_id and not args.backfill:
        parser.error("Provide --post-id or --backfill")

    client = BeehiivClient()

    if args.backfill:
        results = backfill_drafts(client, dry=args.dry)
        if args.json:
            print(json.dumps(results, indent=2))
        return

    send_date = None
    if args.date:
        send_date = datetime.strptime(args.date, "%Y-%m-%d").date()

    title, scheduled = schedule_draft(client, args.post_id, send_date=send_date, dry=args.dry)

    if args.json and title:
        print(json.dumps({"post_id": args.post_id, "title": title, "send_date": scheduled}))


if __name__ == "__main__":
    main()
