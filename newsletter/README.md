# Newsletter Pipeline

Takes short-form video scripts and turns them into creator-style newsletter emails. Pushes drafts to your email platform, schedules sends, and handles a 7-email welcome series for new subscribers.

**Primary platform: Beehiiv.** Works with Mailchimp, ConvertKit/Kit, Brevo, and others with minor rewiring.

## What's in this folder

| File | Purpose |
|---|---|
| `email_html.py` | Renders the final email HTML. 6 templates (lesson, tool, essay, tips, insight, comparison). |
| `beehiiv_api.py` | Wrapper around the Beehiiv REST API. Loads credentials from `.env`. |
| `beehiiv_playwright.py` | Browser-automation fallback for the Beehiiv actions that aren't exposed via the public API. |
| `push_newsletter.py` | Creates drafts in Beehiiv and schedules sends. Combines Playwright + internal dashboard API. |
| `auto_schedule.py` | Finds the next open send slot and schedules one or all drafts. |
| `welcome_series.py` | Generates the 7 HTML files for a 2-week welcome funnel. Includes a worked example (freelance designer selling a brand starter pack) you can replace. |
| `import_leads.py` | Bulk-imports subscribers from a CSV and sets custom fields. |
| `.env.example` | Template for your credentials. Copy to `.env` and fill in. |

## Quick start

1. **Install dependencies:**
   ```bash
   pip3 install python-dotenv playwright
   python3 -m playwright install chromium
   ```

2. **Create your `.env`:**
   ```bash
   cp .env.example .env
   # then edit .env and paste your real Beehiiv credentials
   ```

3. **Verify the connection:**
   ```bash
   python3 beehiiv_api.py
   # expect: {"success": true, "message": "Beehiiv API connection OK"}
   ```

4. **Customize your brand in `email_html.py`:**
   - Update the `COLORS` dict at the top to match your brand
   - Replace `"Your Name"` in the `signoff_html` section with your name

5. **Customize your welcome series in `welcome_series.py`:**
   - Replace the example creator (Jane, freelance designer) bodies with your own
   - Update `MAIN_OFFER_URL` at the top to your actual offer page
   - Run `python3 welcome_series.py` to generate the HTML files

6. **Generate your first newsletter:**
   Run the `/newsletter` skill in Claude Code on any script you have in your script library. It uses these files to produce the HTML and JSON drafts.

7. **Push drafts to Beehiiv:**
   ```bash
   python3 push_newsletter.py --dry        # preview
   python3 push_newsletter.py --limit 1    # push one for testing
   python3 push_newsletter.py              # push all
   ```

## Using a platform other than Beehiiv

The HTML generation (`email_html.py`), template structure, welcome series, and pattern-matching logic are all platform-agnostic. What you swap out:

- Replace `beehiiv_api.py` with your platform's equivalent (same method signatures)
- Update `push_newsletter.py` imports to use your new wrapper
- Adjust the merge tag syntax in `email_html.py` (search for `{{first_name | there}}`)

Minimum interface for any platform wrapper:

```python
class YourPlatformClient:
    def create_draft(self, title, subject, preview, html_body): ...
    def schedule_post(self, post_id, send_at_utc): ...
    def list_posts(self, status="draft", limit=10): ...
    def subscribe(self, email, first_name=None, custom_fields=None): ...
    def test_connection(self): ...
```

Ask Claude: "Read `beehiiv_api.py` and create the equivalent module for {your platform}. Match the method signatures exactly."

## Why Playwright for Beehiiv specifically

Beehiiv's public API restricts `POST /posts` (create a post) to Enterprise plans. On the free plan this returns 403. `push_newsletter.py` works around that by creating the blank post through the UI (which the free plan allows) and setting metadata via the internal dashboard API (same JWT the browser uses).

If you use ConvertKit, Mailchimp, Brevo, or most other platforms, their public APIs support post creation without an Enterprise tier. You can drop Playwright entirely and use direct API calls.

## Safety

- Never commit `.env` to git. The included `.gitignore` already excludes it.
- Lead CSVs may contain PII. Keep them local or in private storage.
- The Playwright state at `/tmp/beehiiv-playwright-state/` holds your session cookies. Treat it like a password.
