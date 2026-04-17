#!/usr/bin/env python3
"""
Beehiiv API wrapper for newsletter operations.
Loads credentials from .env - never hardcodes keys.

Usage:
    from beehiiv_api import BeehiivClient
    client = BeehiivClient()
    draft = client.create_draft(title="...", subject="...", preview="...", html_body="...")

NOTE: If you use a different email platform (Mailchimp, ConvertKit, Brevo), create
a module with the same method signatures and import it instead of this one.
The push and schedule scripts will work as long as the interface matches.
"""

import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the newsletter directory
_env_path = Path(__file__).parent / ".env"
load_dotenv(_env_path)

BASE_URL = "https://api.beehiiv.com/v2"


class BeehiivClient:
    def __init__(self):
        self.api_key = os.environ.get("BEEHIIV_API_KEY")
        self.pub_id = os.environ.get("BEEHIIV_PUBLICATION_ID")
        if not self.api_key or not self.pub_id:
            raise RuntimeError(
                f"Missing Beehiiv credentials. Ensure .env exists at {_env_path} "
                "with BEEHIIV_API_KEY and BEEHIIV_PUBLICATION_ID"
            )

    def _request(self, method, path, body=None):
        """Make an authenticated API request."""
        url = f"{BASE_URL}/publications/{self.pub_id}{path}"
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {self.api_key}")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        try:
            with urllib.request.urlopen(req) as resp:
                body = resp.read().decode()
                return json.loads(body) if body.strip() else {}
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            raise RuntimeError(
                f"Beehiiv API error {e.code} on {method} {path}: {error_body}"
            ) from e

    def create_draft(self, title, subject, preview, html_body, content_tags=None):
        """
        Create a draft post in Beehiiv.

        NOTE: Beehiiv's public API restricts POST /posts to Enterprise plans.
        On the free plan this returns 403. Use push_newsletter.py (Playwright
        + internal dashboard API) instead for draft creation.

        Returns: {"post_id": "post_xxx", "url": "..."}
        """
        body = {
            "title": title,
            "status": "draft",
            "body_content": html_body,
            "email_settings": {
                "subject_line": subject,
                "preview_text": preview,
            },
        }
        if content_tags:
            body["content_tags"] = content_tags

        resp = self._request("POST", "/posts", body)
        post_data = resp.get("data", {})
        post_id = post_data.get("id", "")
        dashboard_url = f"https://app.beehiiv.com/publications/{self.pub_id}/posts/{post_id}"
        return {
            "post_id": post_id,
            "url": dashboard_url,
            "web_url": post_data.get("web_url", ""),
        }

    def publish_post(self, post_id):
        """Attempt to publish a draft. May fail on non-Enterprise plans."""
        try:
            self._request("PUT", f"/posts/{post_id}", {"status": "confirmed"})
            return {"success": True, "message": "Post published via API"}
        except RuntimeError as e:
            dashboard_url = f"https://app.beehiiv.com/publications/{self.pub_id}/posts/{post_id}"
            return {
                "success": False,
                "message": f"API publish failed - open dashboard to send manually: {dashboard_url}",
                "url": dashboard_url,
                "error": str(e),
            }

    def schedule_post(self, post_id, send_at_utc):
        """
        Schedule an existing draft for future delivery.

        Beehiiv has no PATCH/PUT endpoint for scheduling, so this reads the
        draft content, deletes the draft, and creates a new confirmed post with
        scheduled_at.

        Args:
            post_id: The Beehiiv post ID
            send_at_utc: ISO 8601 datetime string in UTC (e.g. "2026-03-25T14:00:00Z")
        Returns: dict with new post_id, url, web_url
        """
        resp = self._request(
            "GET",
            f"/posts/{post_id}?expand[]=free_web_content&expand[]=free_email_content"
        )
        draft = resp.get("data", {})

        content = draft.get("content", {})
        email_html = (
            content.get("free", {}).get("email", "")
            or content.get("free", {}).get("web", "")
        )

        self._request("DELETE", f"/posts/{post_id}")

        body = {
            "title": draft.get("title", ""),
            "subtitle": draft.get("subtitle", ""),
            "status": "confirmed",
            "scheduled_at": send_at_utc,
            "body_content": email_html,
            "email_settings": {
                "subject_line": draft.get("subject_line", ""),
                "preview_text": draft.get("preview_text", ""),
            },
        }
        if draft.get("content_tags"):
            body["content_tags"] = draft["content_tags"]

        resp = self._request("POST", "/posts", body)
        post_data = resp.get("data", {})
        new_id = post_data.get("id", "")
        dashboard_url = f"https://app.beehiiv.com/publications/{self.pub_id}/posts/{new_id}"
        return {
            "post_id": new_id,
            "url": dashboard_url,
            "web_url": post_data.get("web_url", ""),
        }

    def create_scheduled_post(self, title, subject, preview, html_body, send_at_utc,
                               subtitle="", content_tags=None):
        """Create a post directly as scheduled (confirmed + scheduled_at)."""
        body = {
            "title": title,
            "status": "confirmed",
            "scheduled_at": send_at_utc,
            "body_content": html_body,
            "email_settings": {
                "subject_line": subject,
                "preview_text": preview,
            },
        }
        if subtitle:
            body["subtitle"] = subtitle
        if content_tags:
            body["content_tags"] = content_tags

        resp = self._request("POST", "/posts", body)
        post_data = resp.get("data", {})
        new_id = post_data.get("id", "")
        dashboard_url = f"https://app.beehiiv.com/publications/{self.pub_id}/posts/{new_id}"
        return {
            "post_id": new_id,
            "url": dashboard_url,
            "web_url": post_data.get("web_url", ""),
        }

    def delete_post(self, post_id):
        """Delete a draft or archive a confirmed post."""
        return self._request("DELETE", f"/posts/{post_id}")

    def get_post(self, post_id):
        """Get details for a specific post."""
        resp = self._request("GET", f"/posts/{post_id}")
        return resp.get("data", {})

    def list_posts(self, status="draft", limit=10):
        """List posts, optionally filtered by status."""
        resp = self._request("GET", f"/posts?status={status}&limit={limit}")
        return resp.get("data", [])

    def subscribe(self, email, first_name=None, utm_source=None, utm_campaign=None,
                  automation_ids=None, double_opt="off", reactivate=True, custom_fields=None):
        """
        Add a subscriber to the publication.

        Args:
            email: Subscriber email
            first_name: Optional first name (stored via custom field)
            utm_source: Attribution source
            utm_campaign: Attribution campaign
            automation_ids: List of automation IDs to enroll subscriber in
            double_opt: "on", "off", or "not_set"
            reactivate: Whether to reactivate previously unsubscribed addresses
            custom_fields: List of {"name": "...", "value": "..."} dicts
        """
        body = {
            "email": email,
            "reactivate_existing": reactivate,
            "double_opt_override": double_opt,
            "send_welcome_email": False,
        }
        if utm_source:
            body["utm_source"] = utm_source
        if utm_campaign:
            body["utm_campaign"] = utm_campaign
        if automation_ids:
            body["automation_ids"] = automation_ids

        fields = list(custom_fields or [])
        if first_name:
            fields.append({"name": "first_name", "value": first_name})
        if fields:
            body["custom_fields"] = fields

        resp = self._request("POST", "/subscriptions", body)
        return resp.get("data", {})

    def enroll_in_automation(self, automation_id, email):
        """Enroll an existing subscriber in an automation via the journeys endpoint."""
        return self._request("POST", f"/automations/{automation_id}/journeys", {
            "email": email,
            "double_opt_override": "off",
        })

    def update_subscriber(self, subscription_id, custom_fields=None, **kwargs):
        """Update a subscriber's custom fields or other properties."""
        body = {}
        if custom_fields:
            body["custom_fields"] = custom_fields
        body.update(kwargs)
        return self._request("PUT", f"/subscriptions/{subscription_id}", body)

    def get_subscriber(self, email):
        """Look up a subscriber by email."""
        try:
            resp = self._request("GET", f"/subscriptions/by_email/{email}")
            return resp.get("data", {})
        except RuntimeError:
            return None

    def test_connection(self):
        """Verify API key and publication ID are valid."""
        try:
            resp = self._request("GET", "/posts?limit=1")
            return {"success": True, "message": "Beehiiv API connection OK"}
        except RuntimeError as e:
            return {"success": False, "message": str(e)}


if __name__ == "__main__":
    client = BeehiivClient()
    result = client.test_connection()
    print(json.dumps(result, indent=2))
