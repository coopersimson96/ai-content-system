#!/usr/bin/env python3
"""
Generate a 7-email welcome series from a template.

This ships with a worked example: "Jane, a freelance designer" who sells a
$297 Brand Starter Pack. Every email demonstrates the shape and tone of a
good welcome series email. Replace the bodies with your own content before
uploading to your platform.

Cadence: Day 0, 1, 3, 5, 7, 10, 14 (2 weeks total)

Usage:
    python3 welcome_series.py
    # Generates drafts/welcome/welcome-{N}-{slug}.html for all 7 emails
"""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from email_html import render_email

OUTPUT_DIR = Path(__file__).parent / "drafts" / "welcome"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================================
# CUSTOMIZE THIS: Replace with your main offer URL
# ==========================================================================
# Example: your community, course, product, or main CTA link.
# Used only in Day 6 and Day 14 emails (the pitch emails).
MAIN_OFFER_URL = "https://your-site.com/offer"

# Example creator profile baked into the bodies below.
# Replace the body text in EMAILS to match your own voice, offer, and audience.
# The structure (hook, framework, tutorial, system-reveal, social proof, pitch)
# is what makes a welcome series work. Change the content, keep the structure.

EMAILS = [
    # ======================================================================
    # Day 0: Welcome
    # Set expectations, deliver first value, prime the reader to open future emails
    # ======================================================================
    {
        "number": 1,
        "day": 0,
        "subject": "welcome in",
        "preview": "here's what you can expect",
        "slug": "welcome",
        "body": """Hey {{first_name | there}},

Welcome. You just joined a group of small-business owners and side-hustlers who are done feeling like their brand looks amateur.

I'm Jane. Every week I share one tactic for building a brand that looks professional without hiring an agency.

Here's what to expect:

**1 email per week.** Short, useful, no fluff. Each one gives you a specific tool, workflow, or design decision you can apply the same day.

**Free resources.** Every email links to a visual guide so you never get stuck trying to figure out how to implement what I'm sharing.

**Real examples.** Everything I share is something I've personally used with clients or in my own business.

---

To get you started, here's my most popular free resource. It helps you audit your current brand in 10 minutes and pinpoint the exact things holding it back:""",
        "cta_text": "Get the Brand Audit checklist (free)",
        "cta_url": "https://your-site.com/brand-audit",
        "ps": "Reply to this email and tell me what you're working on. I read every reply - it helps me write emails that actually help you.",
    },

    # ======================================================================
    # Day 1: Big idea / framework (flip a common belief)
    # ======================================================================
    {
        "number": 2,
        "day": 1,
        "subject": "the mistake everyone makes",
        "preview": "it's not your logo",
        "slug": "mistake",
        "body": """Hey {{first_name | there}},

Most people think branding is about getting the perfect logo.

They spend weeks in Canva. They hire designers. They redo it every 6 months.

But the logo is actually the lowest-leverage part of a brand.

There are 4 layers to a brand. Most people only focus on layer 1:

**Layer 1: Logo and visual assets.** The things people think of first. They're table stakes, not a differentiator.

**Layer 2: Consistency.** Using the same fonts, colors, and voice everywhere. This is where 80% of the "looks professional" feeling comes from.

**Layer 3: Positioning.** What you stand for, who you're for, what you refuse to do. This is how your audience describes you to others.

**Layer 4: Trust signals.** Testimonials, results, visible process. This is what turns strangers into buyers.

Most small businesses are stuck on layer 1 while layer 2 costs nothing to fix.

---

I made a free template pack that gets you to layer 2 in an afternoon:""",
        "cta_text": "Get the Brand Consistency templates (free)",
        "cta_url": "https://your-site.com/consistency-templates",
        "ps": "If your brand feels 'off' but you can't explain why, you're probably missing layer 2. The templates fix it without redesign.",
    },

    # ======================================================================
    # Day 3: Tutorial (a specific "how I do X")
    # ======================================================================
    {
        "number": 3,
        "day": 3,
        "subject": "stop using canva like that",
        "preview": "there's a better starting point",
        "slug": "canva-tactics",
        "body": """Hey {{first_name | there}},

Most small business owners use Canva one way: scroll the templates, pick one that "looks good," change the colors.

Three months later they have 40 graphics that don't look like they came from the same business.

There's a better way. I call it the Brand Kit approach.

Here's the 3-step fix:

**Step 1: Build your Brand Kit first**
Open Canva Pro and go to Brand Hub. Upload your 2-3 fonts, your 4-color palette, and your logo (even if it's imperfect). Five minutes.

**Step 2: Start every graphic from a blank canvas, not a template**
Templates pull random fonts and colors in. Blank canvases force you to apply your Brand Kit. The output looks owned instead of borrowed.

**Step 3: Save templates from YOUR graphics**
Once you've made 5-10 graphics you like, save those as templates. Now you have a library that's actually yours.

Your graphics will start looking like they're from the same business without a redesign.

---

I put the full Canva Brand Kit walkthrough (with screenshots) in a free guide:""",
        "cta_text": "Get the Canva Brand Kit guide (free)",
        "cta_url": "https://your-site.com/canva-brand-kit",
        "ps": "If you already have Canva Pro this takes about 20 minutes to set up and saves you hours every month.",
    },

    # ======================================================================
    # Day 5: Second tactic (another concrete "do this today")
    # ======================================================================
    {
        "number": 4,
        "day": 5,
        "subject": "one thing saved my weekends",
        "preview": "systems instead of files",
        "slug": "systems-not-files",
        "body": """Hey {{first_name | there}},

Six months ago I was spending every Sunday creating social graphics for the week ahead.

Four to six hours. Every week. For graphics I'd post once and never use again.

I tried blocks, I tried automation tools, I tried batching. Nothing stuck.

The thing that actually worked: **building 5 reusable graphic systems instead of creating one-off graphics.**

Here's what changed:

**Before:** Every Sunday I made 7-10 graphics from scratch. Different layouts, different sizes, different feels.

**After:** I have 5 templates (quote card, product photo, testimonial, announcement, weekly tip). I fill in the content for the week in 30 minutes total.

The graphics look more cohesive because they're from the same system. And I have my Sundays back.

This works because content volume matters less than content consistency. Showing up with 5 on-brand posts beats posting 10 messy ones.

---

I built out the 5 template system (Canva + Figma versions) and put it in a free pack:""",
        "cta_text": "Get the 5 Template system (free)",
        "cta_url": "https://your-site.com/template-system",
        "ps": "This works for any brand, any niche. The templates are structural - you plug in your colors, fonts, and content.",
    },

    # ======================================================================
    # Day 7: System reveal (pivot from tips to bigger system)
    # ======================================================================
    {
        "number": 5,
        "day": 7,
        "subject": "what i actually built",
        "preview": "the whole system, not just tips",
        "slug": "system-reveal",
        "body": """Hey {{first_name | there}},

Over the last few emails I've been sharing individual tactics. Brand Kit setup, Canva approach, template systems.

But these aren't random tricks. They're pieces of a bigger system.

I built a full Brand Starter Pack that takes any small business from "this doesn't look professional" to "this looks like a real brand" in a weekend.

Here's what that looks like in practice:

**You start Friday night.** Define your voice and positioning using the 12-question brand strategy worksheet.

**Saturday morning.** Pick your font pairing and color palette from the curated options.

**Saturday afternoon.** Build your Brand Kit in Canva using the setup checklist.

**Sunday.** Create your 5 reusable templates from the pattern library.

**Monday.** Post your first on-brand graphic. The difference is visible immediately.

This is the difference between improving your brand piece-by-piece over a year and having a complete, professional brand by next Monday.

---

I've been putting this system in front of small businesses for the last 6 months. The feedback has been better than anything I've put out before. More on that next email.""",
        "cta_text": None,
        "cta_url": None,
        "ps": "Next email I'll show you what other people are doing with this. Some of the transformations have genuinely surprised me.",
    },

    # ======================================================================
    # Day 10: Social proof (3 short case studies)
    # ======================================================================
    {
        "number": 6,
        "day": 10,
        "subject": "what people are building",
        "preview": "none of them were designers",
        "slug": "social-proof",
        "body": """Hey {{first_name | there}},

I want to show you what's possible when you actually sit down and do the brand work.

**Here's what I've seen:**

A bakery owner built out her full brand system in one weekend. Two weeks later her Instagram following jumped because every post suddenly looked like it was from the same business.

A coach who'd been "about to hire a designer" for 6 months finished her brand starter pack in 4 hours. She now uses the same templates for all her content instead of buying new graphics every month.

A clothing resale shop went from a logo on a white background to a full brand with product templates, story templates, and a clear voice. Her weekly sales doubled within the first month - mostly because her Instagram finally looked trustworthy.

**None of these people are designers.** They all started exactly where you are.

The difference? They stopped tweaking logos and did the actual brand work.

---

I built the Brand Starter Pack to give small-business owners the exact templates, worksheets, and walkthrough they need to build a full brand in one weekend. If you want to see what's inside:""",
        "cta_text": "See the Brand Starter Pack",
        "cta_url": MAIN_OFFER_URL,
        "ps": "Even if you're not ready to buy yet, keep opening these emails. Every one gives you something you can apply right away.",
    },

    # ======================================================================
    # Day 14: The offer (the one pitch email)
    # ======================================================================
    {
        "number": 7,
        "day": 14,
        "subject": "the full system is here",
        "preview": "for when you're ready to stop guessing",
        "slug": "offer-pitch",
        "body": """Hey {{first_name | there}},

Over the last two weeks I've shared the four layers of brand, the Canva Brand Kit setup, the 5-template system, and the full weekend build.

If you've been following along, you already know more about building a real brand than most people who've been "working on their brand" for years.

But here's what I've noticed: the people who get the best results aren't just reading the emails. They're doing the work alongside the templates, worksheets, and walkthroughs.

That's why I built the Brand Starter Pack.

**What's inside:**

- **The 12-question brand strategy worksheet.** Get clear on voice, audience, and positioning in one sitting.
- **The curated font + color pairings library.** No more endless scrolling. Pick from 40 battle-tested combinations.
- **The Canva Brand Kit setup checklist.** Screenshot-by-screenshot walkthrough.
- **The 5 reusable graphic templates.** Quote card, product, testimonial, announcement, tip. Canva and Figma versions.
- **The Voice Guide template.** One page that tells you exactly how to write for your brand.
- **Full weekend build schedule.** Friday night to Monday morning, hour by hour.

Right now the Brand Starter Pack is **$297**. One-time payment, lifetime access.

This isn't for everyone. It's for small-business owners who want a real brand by next week, not next year.

---

If that sounds like you:""",
        "cta_text": "Get the Brand Starter Pack ($297)",
        "cta_url": MAIN_OFFER_URL,
        "ps": "Whether you buy or not, you'll keep getting my weekly emails. But if you want the full system to stop piecing your brand together slowly, this is where it lives.",
    },
]


def generate_all():
    metadata = []

    for email in EMAILS:
        html = render_email(
            body_markdown=email["body"],
            cta_text=email["cta_text"],
            cta_url=email["cta_url"],
            ps_text=email.get("ps", ""),
        )

        filename = f"welcome-{email['number']:02d}-{email['slug']}"
        html_path = OUTPUT_DIR / f"{filename}.html"
        html_path.write_text(html)
        print(f"  [{email['number']}/7] {filename}.html ({len(email['body'].split())} words)")

        metadata.append({
            "number": email["number"],
            "day": email["day"],
            "subject": email["subject"],
            "preview": email["preview"],
            "slug": email["slug"],
            "word_count": len(email["body"].split()),
            "cta_url": email["cta_url"],
            "html_file": str(html_path),
        })

    meta_path = OUTPUT_DIR / "welcome_series.json"
    meta_path.write_text(json.dumps(metadata, indent=2))
    print(f"\n  Metadata: {meta_path}")

    print(f"\nWELCOME SERIES GENERATED: 7 emails")
    print(f"  Location: {OUTPUT_DIR}/")
    for m in metadata:
        print(f"  Day {m['day']:2d} | Email {m['number']} | \"{m['subject']}\" | {m['word_count']} words")


if __name__ == "__main__":
    generate_all()
