#!/usr/bin/env python3
"""Pure HTML/CSS slide renderer. Renders carousel slides directly from config.json
using the Greg-style HTML template. No AI visual layer needed.

Usage:
  python3 render.py --config output/my-carousel/config.json
"""
import argparse
import json
import os
import sys
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATE_PATH = PROJECT_ROOT / "templates" / "greg-style.html"
FONTS_PATH = PROJECT_ROOT / "fonts"
BRAND_PATH = PROJECT_ROOT / "brand.json"


def load_brand():
    """Load brand config. Falls back to defaults if not found."""
    if BRAND_PATH.exists():
        with open(BRAND_PATH) as f:
            return json.load(f)
    return {"handle": "@your.handle", "accent_colors": {"primary": "#2D7DD2"}}


def image_to_data_uri(image_path):
    """Convert an image file to a base64 data URI."""
    path = Path(image_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = path.suffix.lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif", "svg": "image/svg+xml"}.get(ext.lstrip("."), "image/png")
    return f"data:{mime};base64,{data}"


def build_slide_html(slide, config, total_slides):
    """Build the inner HTML content for a slide based on its components."""
    parts = []
    accent = config.get("accent_color", "#2D7DD2")
    brand = load_brand()
    handle = config.get("handle", brand.get("handle", "@your.handle"))
    number = slide["number"]

    # Cover slide layout - centered, headline-dominant
    if slide.get("cover"):
        parts.append('<div class="cover-layout">')
        if slide.get("pre_header"):
            parts.append(f'<div class="cover-pre-header">{slide["pre_header"]}</div>')
        if slide.get("headline"):
            headline = slide["headline"]
            import re
            headline = re.sub(r'==(.+?)==', f'<span class="highlight">\\1</span>', headline)
            headline = re.sub(r'__(.+?)__', f'<span class="underline">\\1</span>', headline)
            headline = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', headline)
            headline = re.sub(r'\*(.+?)\*', f'<span class="serif-italic">\\1</span>', headline)
            size = slide.get("headline_size", "68px")
            parts.append(f'<div class="cover-headline" style="font-size: {size};">{headline}</div>')
        if slide.get("body"):
            parts.append(f'<div class="cover-subheadline">{slide["body"]}</div>')
        # Cover components (small, below the headline)
        for component in slide.get("components", []):
            ctype = component["type"]
            if ctype == "stats_row":
                stats_html = ""
                for stat in component.get("stats", []):
                    stats_html += f'<div class="stat-item"><div class="stat-number">{stat["number"]}</div><div class="stat-label">{stat["label"]}</div></div>'
                parts.append(f'<div class="stats-row">{stats_html}</div>')
            elif ctype == "sticky_note":
                parts.append(f'<div class="sticky-note">{component.get("text", "")}</div>')
        parts.append('</div>')

        # Footer
        parts.append('<div class="slide-footer">')
        parts.append(f'<div class="slide-counter">{number:02d} / {total_slides:02d}</div>')
        dots = ''.join(f'<div class="dot{" active" if i+1 == number else ""}"></div>' for i in range(total_slides))
        parts.append(f'<div class="progress-dots">{dots}</div>')
        parts.append(f'<div class="handle">{handle}</div>')
        parts.append('</div>')
        return "\n".join(parts)

    # Step label
    if slide.get("label"):
        parts.append(f'<div class="step-label">{slide["label"]}</div>')

    # Headline with mixed typography
    if slide.get("headline"):
        headline = slide["headline"]
        # Process markup: *text* = serif italic accent, **text** = bold, __text__ = underline, ==text== = highlight
        import re
        headline = re.sub(r'==(.+?)==', f'<span class="highlight">\\1</span>', headline)
        headline = re.sub(r'__(.+?)__', f'<span class="underline">\\1</span>', headline)
        headline = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', headline)
        headline = re.sub(r'\*(.+?)\*', f'<span class="serif-italic">\\1</span>', headline)
        size = slide.get("headline_size", "52px")
        hero_class = " headline-hero" if slide.get("hero") else ""
        parts.append(f'<div class="headline{hero_class}" style="font-size: {size};">{headline}</div>')

    # Body text
    if slide.get("body"):
        body = slide["body"]
        import re
        body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', body)
        body = re.sub(r'\*(.+?)\*', f'<span class="serif-italic">\\1</span>', body)
        parts.append(f'<div class="body-text">{body}</div>')

    # Subtext
    if slide.get("subtext"):
        parts.append(f'<div class="subtext">{slide["subtext"]}</div>')

    # Components - the building blocks
    for component in slide.get("components", []):
        ctype = component["type"]

        if ctype == "code_block":
            code_html = component.get("code", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            # Syntax coloring
            lines = code_html.split("\n")
            colored = []
            for line in lines:
                if line.strip().startswith("$"):
                    colored.append(f'<span class="prompt">$</span>{line.strip()[1:]}')
                elif line.strip().startswith("#") or line.strip().startswith("//"):
                    colored.append(f'<span class="comment">{line}</span>')
                elif "=" in line and not line.strip().startswith("$"):
                    colored.append(f'<span class="highlight-line">{line}</span>')
                else:
                    colored.append(line)
            code_content = "\n".join(colored)
            title = component.get("title", "")
            title_html = f'<div style="font-family: Inter; font-size: 14px; color: #888; margin-bottom: 8px;">{title}</div>' if title else ""
            parts.append(f'''<div class="code-block">
  <div class="dots"><span class="red"></span><span class="yellow"></span><span class="green"></span></div>
  {title_html}<pre>{code_content}</pre>
</div>''')

        elif ctype == "card":
            label = component.get("label", "")
            title = component.get("title", "")
            body = component.get("body", "")
            icon = component.get("icon", "")
            img_path = component.get("image", "")
            style = component.get("style", "")
            label_html = f'<div class="card-label">{label}</div>' if label else ""
            icon_html = f'<div class="card-icon">{icon}</div>' if icon else ""
            card_class = "card card-accent"
            if style == "dark":
                card_class = "card card-dark"
            elif style == "colored":
                card_class = "card card-colored"
            img_html = ""
            if img_path:
                full_path = Path(img_path)
                if not full_path.is_absolute():
                    full_path = PROJECT_ROOT / "output" / config["slug"] / img_path
                data_uri = image_to_data_uri(str(full_path))
                if data_uri:
                    img_html = f'<div style="border-radius: 8px; overflow: hidden; margin-top: 12px;"><img src="{data_uri}" style="width: 100%; display: block;" /></div>'
            parts.append(f'''<div class="{card_class}">
  {icon_html}{label_html}
  <div class="card-title">{title}</div>
  <div class="card-body">{body}</div>
  {img_html}
</div>''')

        elif ctype == "card_grid":
            cards_html = ""
            for card in component.get("cards", []):
                label = card.get("label", "")
                title = card.get("title", "")
                body = card.get("body", "")
                icon = card.get("icon", "")
                style = card.get("style", "")
                img_path = card.get("image", "")
                label_html = f'<div class="card-label">{label}</div>' if label else ""
                icon_html = f'<div class="card-icon">{icon}</div>' if icon else ""
                card_class = "card"
                if style == "dark":
                    card_class += " card-dark"
                elif style == "colored":
                    card_class += " card-colored"
                img_html = ""
                if img_path:
                    full_path = Path(img_path)
                    if not full_path.is_absolute():
                        full_path = PROJECT_ROOT / "output" / config["slug"] / img_path
                    data_uri = image_to_data_uri(str(full_path))
                    if data_uri:
                        img_html = f'<div style="border-radius: 6px; overflow: hidden; margin-top: 10px;"><img src="{data_uri}" style="width: 100%; display: block;" /></div>'
                cards_html += f'''<div class="{card_class}">
  {icon_html}{label_html}
  <div class="card-title">{title}</div>
  <div class="card-body">{body}</div>
  {img_html}
</div>'''
            cols_class = f' cols-{component.get("cols", 2)}' if component.get("cols") else ""
            parts.append(f'<div class="card-grid{cols_class}">{cards_html}</div>')

        elif ctype == "flow":
            steps_html = ""
            vertical = component.get("vertical", False)
            arrow_char = "&#8595;" if vertical else "&#8594;"
            for i, step in enumerate(component.get("steps", [])):
                active = " active" if step.get("active") else ""
                subtitle = f'<div style="font-size: 16px; font-weight: 400; color: #666; margin-top: 4px;">{step["subtitle"]}</div>' if step.get("subtitle") else ""
                steps_html += f'<div class="flow-step{active}">{step["text"]}{subtitle}</div>'
                if i < len(component["steps"]) - 1:
                    steps_html += f'<div class="flow-arrow">{arrow_char}</div>'
            vertical_class = " flow-vertical" if vertical else ""
            parts.append(f'<div class="flow{vertical_class}">{steps_html}</div>')

        elif ctype == "bar_chart":
            bars_html = ""
            for bar in component.get("bars", []):
                width = bar.get("width", "50%")
                bars_html += f'''<div class="bar-row">
  <div class="bar-label">{bar["label"]}</div>
  <div class="bar-track"><div class="bar-fill" style="width: {width};"><span class="bar-value">{bar.get("value", "")}</span></div></div>
</div>'''
            parts.append(f'<div class="bar-chart">{bars_html}</div>')

        elif ctype == "numbered_list":
            items_html = ""
            for item in component.get("items", []):
                if isinstance(item, str):
                    items_html += f"<li><div class='item-content'>{item}</div></li>"
                else:
                    title = item["title"]
                    desc = item.get("desc", "")
                    # Process accent highlights in titles
                    import re
                    title = re.sub(r'\*(.+?)\*', f'<span class="serif-italic">\\1</span>', title)
                    items_html += f'<li><div class="item-content"><strong>{title}</strong><span>{desc}</span></div></li>'
            parts.append(f'<ol class="numbered-list">{items_html}</ol>')

        elif ctype == "screenshot":
            img_path = component.get("path", "")
            if img_path:
                # Resolve relative to carousel output dir
                full_path = Path(img_path)
                if not full_path.is_absolute():
                    full_path = PROJECT_ROOT / "output" / config["slug"] / img_path
                data_uri = image_to_data_uri(str(full_path))
                if data_uri:
                    parts.append(f'<div class="screenshot-container"><img src="{data_uri}" /></div>')

        elif ctype == "stats_row":
            stats_html = ""
            for stat in component.get("stats", []):
                stats_html += f'''<div class="stat-item">
  <div class="stat-number">{stat["number"]}</div>
  <div class="stat-label">{stat["label"]}</div>
</div>'''
            parts.append(f'<div class="stats-row">{stats_html}</div>')

        elif ctype == "sticky_note":
            parts.append(f'<div class="sticky-note">{component.get("text", "")}</div>')

        elif ctype == "logo_row":
            logos_html = ""
            for logo in component.get("logos", []):
                img_path = logo.get("path", "")
                label = logo.get("label", "")
                full_path = Path(img_path) if Path(img_path).is_absolute() else PROJECT_ROOT / img_path
                data_uri = image_to_data_uri(str(full_path))
                if data_uri:
                    logos_html += f'<img src="{data_uri}" />'
                if label:
                    logos_html += f'<span class="logo-label">{label}</span>'
            parts.append(f'<div class="logo-row">{logos_html}</div>')

        elif ctype == "divider":
            parts.append('<hr class="divider">')

        elif ctype == "spacer":
            parts.append(f'<div class="spacer-{component.get("size", "md")}"></div>')

        elif ctype == "cta":
            keyword = component.get("keyword", "")
            subtitle = component.get("subtitle", "")
            parts.append(f'''<div class="cta-container">
  <div class="cta-headline">Comment this word below</div>
  <div class="cta-keyword-box"><div class="cta-keyword">{keyword}</div></div>
  <div class="cta-sub">{subtitle}</div>
  <div class="cta-handle">{handle}</div>
</div>''')

    # Footer
    parts.append('<div class="slide-footer">')
    parts.append(f'<div class="slide-counter">{number:02d} / {total_slides:02d}</div>')
    # Progress dots
    dots = ''.join(f'<div class="dot{" active" if i+1 == number else ""}"></div>' for i in range(total_slides))
    parts.append(f'<div class="progress-dots">{dots}</div>')
    parts.append(f'<div class="handle">{handle}</div>')
    parts.append('</div>')

    return "\n".join(parts)


def render_slide(html_content, output_path, config):
    """Render a slide's HTML to PNG using Playwright."""
    template = TEMPLATE_PATH.read_text()
    accent = config.get("accent_color", "#2D7DD2")

    # Compute accent variants
    # Light version for backgrounds
    r, g, b = int(accent[1:3], 16), int(accent[3:5], 16), int(accent[5:7], 16)
    accent_bg = f"rgba({r},{g},{b},0.12)"
    accent_light = f"rgba({r},{g},{b},0.7)"

    filled = template.replace("{{FONT_PATH}}", str(FONTS_PATH))
    filled = filled.replace("{{ACCENT_COLOR}}", accent)
    filled = filled.replace("{{ACCENT_BG}}", accent_bg)
    filled = filled.replace("{{ACCENT_LIGHT}}", accent_light)
    filled = filled.replace("{{CONTENT}}", html_content)

    temp_html = str(output_path).replace(".png", ".html")
    with open(temp_html, "w") as f:
        f.write(filled)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        page.goto(f"file://{os.path.abspath(temp_html)}", wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=str(output_path))
        browser.close()

    os.remove(temp_html)


def process_carousel(config_path):
    """Process a full carousel from config.json."""
    config_path = Path(config_path)
    with open(config_path) as f:
        config = json.load(f)

    slides_dir = config_path.parent / "slides"
    slides_dir.mkdir(exist_ok=True)

    slides = config["slides"]
    total = len(slides)

    print(f"Rendering carousel: {config.get('slug', 'unknown')} ({total} slides)")

    for slide in slides:
        n = slide["number"]
        print(f"  Slide {n}/{total} ...", end=" ")

        html_content = build_slide_html(slide, config, total)
        output_path = slides_dir / f"slide-{n:02d}.png"
        render_slide(html_content, str(output_path), config)

        print(f"done -> {output_path}")

    print(f"\nAll slides saved to {slides_dir}/")

    # Auto-open
    slide_files = sorted(slides_dir.glob("slide-*.png"))
    if slide_files:
        os.system(f"open {' '.join(str(f) for f in slide_files)}")


def main():
    parser = argparse.ArgumentParser(description="Render carousel slides from HTML templates")
    parser.add_argument("--config", required=True, help="Path to carousel config.json")
    args = parser.parse_args()
    process_carousel(args.config)


if __name__ == "__main__":
    main()
