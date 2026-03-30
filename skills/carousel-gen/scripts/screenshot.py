#!/usr/bin/env python3
"""Web screenshot utility for carousel asset pipeline.
Captures tool/website screenshots for use as Nano Banana reference images.
"""
import argparse
import os
import sys
from playwright.sync_api import sync_playwright


def capture_screenshot(url, output_path, selector=None, width=1200, height=800, wait_ms=3000):
    """Capture a screenshot of a URL, optionally targeting a specific CSS selector."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": width, "height": height},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            color_scheme="light",
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(wait_ms)

            # Dismiss common popups
            _dismiss_popups(page)

            if selector:
                element = page.query_selector(selector)
                if element:
                    element.screenshot(path=output_path)
                    print(f"Captured element '{selector}' -> {output_path}")
                else:
                    print(f"Selector '{selector}' not found, capturing full page")
                    page.screenshot(path=output_path)
            else:
                page.screenshot(path=output_path)
                print(f"Captured full viewport -> {output_path}")

        except Exception as e:
            print(f"Error capturing {url}: {e}", file=sys.stderr)
            return False
        finally:
            browser.close()

    return os.path.exists(output_path)


def _dismiss_popups(page):
    """Try to dismiss common cookie banners and login popups."""
    dismiss_selectors = [
        'button:has-text("Accept")',
        'button:has-text("Accept All")',
        'button:has-text("Allow")',
        'button:has-text("Got it")',
        'button:has-text("Close")',
        'button:has-text("Dismiss")',
        '[aria-label="Close"]',
        '[aria-label="Dismiss"]',
        '.cookie-banner button',
        '#cookie-consent button',
    ]
    for sel in dismiss_selectors:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=500):
                btn.click()
                page.wait_for_timeout(300)
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Capture web screenshots for carousel assets")
    parser.add_argument("url", help="URL to screenshot")
    parser.add_argument("-o", "--output", required=True, help="Output PNG path")
    parser.add_argument("-s", "--selector", help="CSS selector to capture (captures element only)")
    parser.add_argument("-w", "--width", type=int, default=1200, help="Viewport width (default: 1200)")
    parser.add_argument("-H", "--height", type=int, default=800, help="Viewport height (default: 800)")
    parser.add_argument("--wait", type=int, default=3000, help="Wait time in ms after load (default: 3000)")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    success = capture_screenshot(
        url=args.url,
        output_path=args.output,
        selector=args.selector,
        width=args.width,
        height=args.height,
        wait_ms=args.wait,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
