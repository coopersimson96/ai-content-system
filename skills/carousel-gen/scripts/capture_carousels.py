"""Capture Instagram carousel screenshots using Playwright.

Usage:
  python3 capture_carousels.py URL1 URL2 URL3
  python3 capture_carousels.py https://www.instagram.com/p/ABC123/

Saves screenshots to the references/ directory as style-ref-N.png.
Use these as visual style references when generating carousels.
"""
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "references"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


def dismiss_popups(page):
    """Try to dismiss login modals and cookie banners."""
    selectors = [
        'text="Not Now"',
        'text="Not now"',
        'text="Decline optional cookies"',
        'text="Allow essential and optional cookies"',
        'text="Accept"',
        'text="Accept All"',
        'text="Close"',
        '[aria-label="Close"]',
        '[aria-label="Dismiss"]',
    ]
    for sel in selectors:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=1000):
                el.click()
                time.sleep(0.5)
        except Exception:
            pass


def capture_post(page, url, filename):
    """Navigate to an Instagram post and screenshot the carousel image area."""
    print(f"Navigating to {url} ...")
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    dismiss_popups(page)
    time.sleep(1)
    dismiss_popups(page)

    selectors_to_try = ["article", 'div[role="presentation"]', "main"]

    for sel in selectors_to_try:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=3000):
                el.scroll_into_view_if_needed()
                time.sleep(0.5)
                path = str(OUTPUT_DIR / filename)
                el.screenshot(path=path)
                print(f"  Saved {path} (selector: {sel})")
                return True
        except Exception as e:
            print(f"  Selector '{sel}' failed: {e}")

    path = str(OUTPUT_DIR / filename)
    page.screenshot(path=path)
    print(f"  Saved {path} (full viewport fallback)")
    return True


def main():
    urls = sys.argv[1:]
    if not urls:
        print("Usage: python3 capture_carousels.py URL1 [URL2] [URL3]")
        print("Example: python3 capture_carousels.py https://www.instagram.com/p/ABC123/")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            viewport={"width": 1080, "height": 1350},
            user_agent=USER_AGENT,
            locale="en-US",
        )
        page = context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
        """)

        for i, url in enumerate(urls):
            try:
                capture_post(page, url, f"style-ref-{i+1}.png")
            except Exception as e:
                print(f"ERROR capturing {url}: {e}")

        browser.close()
        print("Done!")


if __name__ == "__main__":
    main()
