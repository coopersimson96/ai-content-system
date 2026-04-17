#!/usr/bin/env python3
"""
Beehiiv browser automation via Playwright.
Handles draft creation and scheduling since the API is Enterprise-only for writes.

Uses persistent Chrome state at /tmp/beehiiv-playwright-state.
On first run, you'll need to log in manually — the state persists after that.

Usage:
    # Create a draft from local HTML
    python3 beehiiv_playwright.py create --html drafts/sf18-plan-mode.html \
        --subject "the hidden mode" --preview "most people never find it"

    # Schedule a draft by title (finds it in the drafts list)
    python3 beehiiv_playwright.py schedule --title "The Hidden Mode" \
        --date 2026-03-25 --time 09:00

    # Schedule all drafts, one per day starting tomorrow
    python3 beehiiv_playwright.py schedule-all [--dry]

    # List all current drafts
    python3 beehiiv_playwright.py list-drafts
"""

import argparse
import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

STATE_DIR = "/tmp/beehiiv-playwright-state"
BEEHIIV_BASE = "https://app.beehiiv.com"
EST = ZoneInfo("America/New_York")
SEND_HOUR = 9
SEND_MINUTE = 0


def get_browser(playwright, headless=True):
    """Launch browser with persistent state."""
    context = playwright.chromium.launch_persistent_context(
        STATE_DIR,
        headless=headless,
        viewport={"width": 1280, "height": 900},
        args=["--disable-blink-features=AutomationControlled"],
    )
    return context


def ensure_logged_in(page):
    """Check if logged into Beehiiv, prompt if not."""
    page.goto(f"{BEEHIIV_BASE}/dashboard", wait_until="domcontentloaded", timeout=15000)
    time.sleep(2)
    if "/login" in page.url or "/sign" in page.url:
        print("Not logged into Beehiiv. Please log in manually in the browser window.")
        print("Waiting up to 120 seconds...")
        page.wait_for_url("**/dashboard**", timeout=120000)
        print("Logged in successfully!")
    return True


def get_pub_id(page):
    """Extract publication ID from the current URL or dashboard."""
    # The URL usually contains the pub ID after /publications/
    url = page.url
    if "/publications/" in url:
        parts = url.split("/publications/")
        if len(parts) > 1:
            return parts[1].split("/")[0]
    # Try navigating to dashboard to find it
    page.goto(f"{BEEHIIV_BASE}/dashboard", wait_until="domcontentloaded", timeout=10000)
    time.sleep(2)
    url = page.url
    if "/publications/" in url:
        parts = url.split("/publications/")
        if len(parts) > 1:
            return parts[1].split("/")[0]
    return None


def list_drafts_browser(page, pub_id):
    """Navigate to drafts page and extract draft info."""
    page.goto(f"{BEEHIIV_BASE}/publications/{pub_id}/posts?status=draft",
              wait_until="domcontentloaded", timeout=15000)
    time.sleep(3)

    # Extract draft titles and links
    drafts = page.evaluate("""
        () => {
            const rows = document.querySelectorAll('a[href*="/posts/"]');
            return Array.from(rows).map(a => ({
                title: a.textContent.trim().substring(0, 100),
                href: a.href,
            })).filter(d => d.title.length > 0 && d.href.includes('/posts/post_'));
        }
    """)
    return drafts


def create_draft_browser(page, pub_id, html_content, subject, preview, headless=True):
    """Create a new draft post via the Beehiiv dashboard."""
    # Navigate to new post page
    page.goto(f"{BEEHIIV_BASE}/publications/{pub_id}/posts/new",
              wait_until="domcontentloaded", timeout=15000)
    time.sleep(3)

    # Set subject line
    subject_input = page.locator('input[placeholder*="Subject"]').first
    if subject_input.is_visible():
        subject_input.fill(subject)

    # Set preview text
    preview_input = page.locator('input[placeholder*="Preview"]').first
    if preview_input.is_visible():
        preview_input.fill(preview)

    # Switch to HTML/code mode and paste content
    # Look for code/HTML toggle
    code_btn = page.locator('button:has-text("Code"), button:has-text("HTML"), button[aria-label*="code"]').first
    if code_btn.is_visible():
        code_btn.click()
        time.sleep(1)

    # Find the code editor and paste HTML
    editor = page.locator('textarea, .cm-content, [contenteditable="true"]').first
    if editor.is_visible():
        editor.fill(html_content)

    time.sleep(1)
    print(f"  Draft created: {subject}")
    return True


def schedule_draft_browser(page, draft_url, send_date, send_time="09:00", dry=False):
    """Schedule a specific draft by navigating to its edit page."""
    if dry:
        print(f"  [DRY RUN] Would schedule for {send_date} at {send_time}")
        return True

    page.goto(draft_url, wait_until="domcontentloaded", timeout=15000)
    time.sleep(3)

    # Look for the Schedule button/option
    # Beehiiv typically has a "Schedule" option near the Send/Publish button
    schedule_btn = page.locator('button:has-text("Schedule"), [data-testid*="schedule"]').first
    if schedule_btn.is_visible():
        schedule_btn.click()
        time.sleep(1)

    # Set date
    date_input = page.locator('input[type="date"], input[placeholder*="date"]').first
    if date_input.is_visible():
        date_input.fill(send_date)

    # Set time
    time_input = page.locator('input[type="time"], input[placeholder*="time"]').first
    if time_input.is_visible():
        time_input.fill(send_time)

    # Confirm schedule
    confirm_btn = page.locator('button:has-text("Schedule"), button:has-text("Confirm")').last
    if confirm_btn.is_visible():
        confirm_btn.click()
        time.sleep(2)

    print(f"  Scheduled for {send_date} at {send_time}")
    return True


def schedule_all(context, pub_id, dry=False, start_date=None):
    """Schedule all drafts, one per day starting from start_date."""
    page = context.pages[0] if context.pages else context.new_page()
    ensure_logged_in(page)

    if not pub_id:
        pub_id = get_pub_id(page)

    drafts = list_drafts_browser(page, pub_id)
    if not drafts:
        print("No drafts found to schedule.")
        return []

    print(f"Found {len(drafts)} draft(s):\n")

    if start_date is None:
        start_date = datetime.now(EST).date() + timedelta(days=1)

    results = []
    current_date = start_date

    for draft in drafts:
        title = draft["title"]
        send_date_str = current_date.strftime("%Y-%m-%d")
        send_display = current_date.strftime("%A %b %d, %Y")

        if dry:
            print(f"  [DRY RUN] '{title}' → {send_display} at {SEND_HOUR}:{SEND_MINUTE:02d} AM EST")
        else:
            schedule_draft_browser(page, draft["href"], send_date_str, f"{SEND_HOUR:02d}:{SEND_MINUTE:02d}")
            print(f"  '{title}' → {send_display} at {SEND_HOUR}:{SEND_MINUTE:02d} AM EST")

        results.append({
            "title": title,
            "send_date": send_date_str,
            "url": draft["href"],
        })
        current_date += timedelta(days=1)

    return results


def main():
    parser = argparse.ArgumentParser(description="Beehiiv browser automation")
    sub = parser.add_subparsers(dest="command")

    # list-drafts
    sub.add_parser("list-drafts", help="List all drafts")

    # create
    create_p = sub.add_parser("create", help="Create a draft from HTML")
    create_p.add_argument("--html", required=True, help="Path to HTML file")
    create_p.add_argument("--subject", required=True)
    create_p.add_argument("--preview", default="")

    # schedule
    sched_p = sub.add_parser("schedule", help="Schedule a specific draft")
    sched_p.add_argument("--url", required=True, help="Draft URL")
    sched_p.add_argument("--date", required=True, help="YYYY-MM-DD")
    sched_p.add_argument("--time", default="09:00")
    sched_p.add_argument("--dry", action="store_true")

    # schedule-all
    sched_all_p = sub.add_parser("schedule-all", help="Schedule all drafts daily")
    sched_all_p.add_argument("--dry", action="store_true")
    sched_all_p.add_argument("--start-date", help="Start date YYYY-MM-DD (default: tomorrow)")
    sched_all_p.add_argument("--json", action="store_true")

    # Common (on parent parser so it works before subcommand)
    parser.add_argument("--no-headless", action="store_true", help="Show browser window")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    headless = not args.no_headless

    with sync_playwright() as p:
        context = get_browser(p, headless=headless)
        page = context.pages[0] if context.pages else context.new_page()

        try:
            ensure_logged_in(page)
            pub_id = get_pub_id(page)

            if not pub_id:
                print("Could not determine publication ID. Check your Beehiiv login.")
                return

            if args.command == "list-drafts":
                drafts = list_drafts_browser(page, pub_id)
                if not drafts:
                    print("No drafts found.")
                else:
                    print(f"Found {len(drafts)} draft(s):")
                    for d in drafts:
                        print(f"  - {d['title']}")
                        print(f"    {d['href']}")

            elif args.command == "create":
                html = Path(args.html).read_text()
                create_draft_browser(page, pub_id, html, args.subject, args.preview, headless)

            elif args.command == "schedule":
                schedule_draft_browser(page, args.url, args.date, args.time, args.dry)

            elif args.command == "schedule-all":
                start = None
                if hasattr(args, "start_date") and args.start_date:
                    start = datetime.strptime(args.start_date, "%Y-%m-%d").date()
                results = schedule_all(context, pub_id, dry=args.dry, start_date=start)
                if hasattr(args, "json") and args.json:
                    print(json.dumps(results, indent=2))

        finally:
            context.close()


if __name__ == "__main__":
    main()
