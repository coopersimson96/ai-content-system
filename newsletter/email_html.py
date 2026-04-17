#!/usr/bin/env python3
"""
Email HTML Generator - Minimal branded HTML for newsletter emails.

Generates plain-text-style HTML. Plain-text-style emails tend to get higher open
rates than heavily-designed templates for creator newsletters.

Usage:
    from email_html import render_email
    html = render_email(
        body_markdown="Hey {{first_name | there}},\n\nHere's the thing...",
        cta_text="Get the free guide",
        cta_url="https://example.com/guide",
    )

-------------------------------------------------------------------------------
CUSTOMIZE THESE TO MATCH YOUR BRAND
-------------------------------------------------------------------------------
The COLORS dict below ships with a neutral default palette.
Replace the hex values with your own brand colors to style the email frame.
Most creators change the accent color (currently dark gray) to their primary
brand color. Keep the background near-white and the body text dark for
readability across mail clients.

SIGN-OFF NAME
Search for "Your Name" in the signoff_html section further down in this file
and replace it with your name (or first-person handle) so emails sign as you.

MERGE TAG SYNTAX
The default merge tag for the recipient's first name is {{first_name | there}}
which works for Beehiiv. Other platforms use different syntax:
    Beehiiv:     {{first_name | there}}
    Mailchimp:   *|FNAME|*
    ConvertKit:  {{ subscriber.first_name }}
    Brevo:       {{ contact.FIRSTNAME }}
Update the body templates below (template_lesson, etc.) to match your platform.
-------------------------------------------------------------------------------
"""

import re


# ======================
# CUSTOMIZE TO YOUR BRAND
# ======================
COLORS = {
    "cream": "#FFFFFF",        # page background (near-white works best)
    "dark": "#1A1A1A",          # body text (dark gray or near-black)
    "teal": "#333333",          # accent for CTA links (change to your brand color)
    "copper": "#666666",        # secondary accent (optional)
    "muted": "#6B7280",         # secondary/footer text
    "border": "#E5E1DB",        # horizontal rule / separator
}


def _markdown_to_html(text):
    """Convert minimal markdown to HTML (bold, italic, links, line breaks)."""
    # Bold: **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic: *text*
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Links: [text](url)
    text = re.sub(
        r"\[(.+?)\]\((.+?)\)",
        rf'<a href="\2" style="color:{COLORS["teal"]};text-decoration:underline;">\1</a>',
        text,
    )
    # Horizontal rule: ---
    text = re.sub(
        r"^---$",
        f'<hr style="border:none;border-top:1px solid {COLORS["border"]};margin:24px 0;">',
        text,
        flags=re.MULTILINE,
    )
    return text


def _format_body(body_markdown):
    """Convert body markdown into styled HTML paragraphs."""
    paragraphs = body_markdown.strip().split("\n\n")
    html_parts = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Check for numbered list items (1. text or **1. text**)
        lines = para.split("\n")
        is_list = all(re.match(r"^\d+\.\s", line.strip()) for line in lines if line.strip())

        if is_list:
            items = []
            for line in lines:
                line = line.strip()
                if line:
                    content = re.sub(r"^\d+\.\s*", "", line)
                    content = _markdown_to_html(content)
                    items.append(f'<li style="margin-bottom:8px;">{content}</li>')
            html_parts.append(
                f'<ol style="padding-left:20px;margin:16px 0;">'
                + "".join(items)
                + "</ol>"
            )
        elif para.startswith("- ") or para.startswith("• "):
            items = []
            for line in lines:
                line = line.strip()
                if line:
                    content = re.sub(r"^[-•]\s*", "", line)
                    content = _markdown_to_html(content)
                    items.append(f'<li style="margin-bottom:8px;">{content}</li>')
            html_parts.append(
                f'<ul style="padding-left:20px;margin:16px 0;">'
                + "".join(items)
                + "</ul>"
            )
        else:
            content = _markdown_to_html(para)
            content = content.replace("\n", "<br>")
            html_parts.append(
                f'<p style="margin:0 0 16px 0;line-height:1.6;">{content}</p>'
            )

    return "\n".join(html_parts)


def render_email(body_markdown, cta_text=None, cta_url=None, ps_text=None):
    """
    Render a complete email HTML document.

    Args:
        body_markdown: Email body with minimal markdown (bold, italic, links, lists)
        cta_text: Optional CTA link text (e.g., "Get the free guide")
        cta_url: Optional CTA URL
        ps_text: Optional P.S. line (markdown supported)

    Returns:
        Complete HTML string ready for your email platform's body field.
    """
    body_html = _format_body(body_markdown)

    # CTA section (single link, not a button - higher click rates for creators)
    cta_html = ""
    if cta_text and cta_url:
        cta_html = f"""
        <p style="margin:24px 0 16px 0;line-height:1.6;">
          <a href="{cta_url}" style="color:{COLORS['teal']};font-weight:600;text-decoration:underline;font-size:16px;">&gt;&gt; {cta_text} &lt;&lt;</a>
        </p>"""

    # P.S. section
    ps_html = ""
    if ps_text:
        ps_content = _markdown_to_html(ps_text)
        ps_html = f"""
        <p style="margin:16px 0 0 0;line-height:1.6;color:{COLORS['muted']};font-style:italic;">
          P.S. {ps_content}
        </p>"""

    # Sign-off -- REPLACE "Your Name" with your own name/handle
    signoff_html = f"""
        <p style="margin:24px 0 0 0;line-height:1.6;">Your Name</p>"""

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body {{ margin:0; padding:0; background:{COLORS['cream']}; }}
    a {{ color:{COLORS['teal']}; }}
  </style>
</head>
<body style="margin:0;padding:0;background:{COLORS['cream']};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:16px;color:{COLORS['dark']};line-height:1.6;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{COLORS['cream']};">
    <tr>
      <td align="center" style="padding:24px 16px;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:580px;">
          <!-- Body -->
          <tr>
            <td style="padding:0;">
              {body_html}
              {cta_html}
              {signoff_html}
              {ps_html}
            </td>
          </tr>

          <!-- Accent line (swap this color to your brand) -->
          <tr>
            <td style="padding:32px 0 16px 0;">
              <hr style="border:none;border-top:2px solid {COLORS['teal']};margin:0;">
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:0;font-size:13px;color:{COLORS['muted']};line-height:1.5;">
              <p style="margin:0 0 8px 0;">Reply to this email. I read every one.</p>
              <p style="margin:0;">
                <a href="{{{{unsubscribe_url}}}}" style="color:{COLORS['muted']};text-decoration:underline;">Unsubscribe</a>
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


# --- Template Functions ---
# Each returns (body, cta_text, cta_url) - optional ps_text handled in render_email
# Modeled after proven creator newsletter styles (Welsh, Koe, Clear, Bloom).

def template_lesson(title, hook, steps, resource_url=None, resource_name=None):
    """Weekly Lesson template (Justin Welsh model)."""
    steps_md = "\n\n".join(
        f"**Step {i+1}: {s['title']}**\n{s['desc']}"
        for i, s in enumerate(steps)
    )

    body = f"""Hey {{{{first_name | there}}}},

{hook}

Here's the {len(steps)}-step framework:

{steps_md}"""

    cta_text = None
    cta_url = None
    if resource_url:
        body += f"\n\n---\n\nI broke this down with visuals in my latest post:"
        cta_text = resource_name or "See the full breakdown"
        cta_url = resource_url

    return body, cta_text, cta_url


def template_tool(tool_name, outcome, time_saved, steps, resource_url=None):
    """Tool Breakdown template."""
    steps_md = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))

    body = f"""Hey {{{{first_name | there}}}},

I found something this week that I can't stop using.

**{tool_name}** does {outcome}.

Here's how I set it up:

{steps_md}"""

    cta_text = "Full walkthrough" if resource_url else None
    return body, cta_text, resource_url


def template_essay(topic, problem, insight, action_steps, resource_url=None, resource_name=None):
    """Problem-Solution Essay template (Dan Koe model)."""
    steps_md = "\n".join(f"{i+1}. {s}" for i, s in enumerate(action_steps))

    body = f"""Hey {{{{first_name | there}}}},

{problem}

The insight that changed everything:

{insight}

Here's how to apply this:

{steps_md}"""

    cta_text = resource_name or "Get the free guide" if resource_url else None
    return body, cta_text, resource_url


def template_tips(topic, tips):
    """Numbered Tips template (James Clear inspired)."""
    tips_md = "\n\n".join(
        f"**{i+1}. {t['title']}**\n{t['desc']}"
        for i, t in enumerate(tips)
    )

    body = f"""{len(tips)} things I learned about {topic} this week:

{tips_md}"""

    return body, None, None


def template_insight(stat, reframe, implications, resource_url=None, resource_name=None):
    """Insight + Resource template (Sahil Bloom model)."""
    implications_md = "\n".join(f"- {imp}" for imp in implications)

    body = f"""Hey {{{{first_name | there}}}},

{stat}

But here's what's actually happening:

{reframe}

What this means for you:

{implications_md}"""

    cta_text = resource_name or "Get the free resource" if resource_url else None
    return body, cta_text, resource_url


def template_comparison(option_a, option_b, verdict, items_a, items_b, resource_url=None):
    """Comparison Breakdown template."""
    a_md = "\n".join(f"- {item}" for item in items_a)
    b_md = "\n".join(f"- {item}" for item in items_b)

    body = f"""Hey {{{{first_name | there}}}},

I see people argue about this every week. Let me break it down.

**{option_a}:**
{a_md}

**{option_b}:**
{b_md}

The real answer: {verdict}"""

    cta_text = "Full breakdown" if resource_url else None
    return body, cta_text, resource_url


if __name__ == "__main__":
    # Quick test - generate a sample email
    body, cta_text, cta_url = template_lesson(
        title="Plan Mode",
        hook="Most people use AI like a chatbot. Type a question, get an answer, repeat.\n\nBut there's a better way.",
        steps=[
            {"title": "Open Plan Mode", "desc": "Shift from 'do mode' to 'think mode.' The AI explores before writing."},
            {"title": "Let It Map Everything", "desc": "It reads your files and drafts a step-by-step implementation plan."},
            {"title": "Approve and Execute", "desc": "Review the plan, make adjustments, then let it build with full context."},
        ],
        resource_url="https://example.com/your-guide",
        resource_name="Get the Plan Mode guide (free)",
    )

    html = render_email(
        body_markdown=body,
        cta_text=cta_text,
        cta_url=cta_url,
        ps_text="Reply and tell me what you'd build. I read every reply.",
    )

    from pathlib import Path
    test_path = Path(__file__).parent / "test_email.html"
    test_path.write_text(html)
    print(f"Test email written to: {test_path}")
    print(f"HTML length: {len(html)} chars")
