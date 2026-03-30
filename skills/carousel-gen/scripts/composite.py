#!/usr/bin/env python3
"""Composites visual layer (Nano Banana) + text overlay (Playwright) into final slide PNGs.

Usage:
  python3 composite.py --config output/my-carousel/config.json

The config.json should contain:
{
  "slug": "my-carousel",
  "handle": "@your.handle",
  "accent_color": "#7FB685",
  "background_tone": "cream",
  "template": "tech-editorial",
  "slides": [
    {
      "number": 1,
      "type": "cover",
      "label": "",
      "headline": "The headline text",
      "body": "",
      "subtext": "",
      "code": "",
      "checklist": [],
      "visual_prompt": "...",
      "visual_path": "visuals/visual-01.png"
    }
  ]
}
"""
import argparse
import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATE_PATH = PROJECT_ROOT / "templates" / "text-overlay.html"
FONTS_PATH = PROJECT_ROOT / "fonts"


def generate_text_html(slide, config, total_slides):
    """Generate the HTML content for a slide's text overlay."""
    slide_type = slide.get("type", "content")
    number = slide.get("number", 1)
    label = slide.get("label", "")
    headline = slide.get("headline", "")
    body = slide.get("body", "")
    subtext = slide.get("subtext", "")
    code = slide.get("code", "")
    checklist = slide.get("checklist", [])
    handle = config.get("handle", "@your.handle")
    accent = config.get("accent_color", "#7FB685")
    show_swipe = number < total_slides

    parts = []

    if slide_type == "cover":
        parts.append(f'<div class="spacer-fixed" style="height: 40px;"></div>')
        parts.append('<div class="text-bg">')
        if label:
            parts.append(f'<div class="label">{_escape(label)}</div>')
        parts.append(f'<div class="headline" style="font-size: 62px;">{_process_text(headline, accent)}</div>')
        if body:
            parts.append(f'<div class="body" style="font-size: 28px;">{_process_text(body, accent)}</div>')
        parts.append('</div>')
        parts.append('<div class="spacer"></div>')

    elif slide_type == "secondary_hook":
        parts.append(f'<div class="spacer-fixed" style="height: 120px;"></div>')
        parts.append(f'<div class="headline" style="font-size: 52px; text-align: center;">{_process_text(headline, accent)}</div>')
        if body:
            parts.append(f'<div class="body" style="font-size: 26px; text-align: center; margin: 0 auto;">{_process_text(body, accent)}</div>')
        parts.append('<div class="spacer"></div>')

    elif slide_type == "cta":
        parts.append(f'<div class="spacer-fixed" style="height: 80px;"></div>')
        parts.append('<div class="text-bg" style="text-align: center;">')
        parts.append(f'<div class="cta-headline" style="font-size: 64px;">{_process_text(headline, accent)}</div>')
        parts.append(f'<div class="cta-handle" style="font-size: 32px; margin-top: 16px;">{_escape(handle)}</div>')
        if body:
            parts.append(f'<div class="body" style="text-align: center; margin: 20px auto 0; font-size: 26px;">{_process_text(body, accent)}</div>')
        parts.append('</div>')
        parts.append('<div class="spacer"></div>')

    elif slide_type == "code":
        if label:
            parts.append(f'<div class="label">{_escape(label)}</div>')
        parts.append(f'<div class="headline" style="font-size: 44px;">{_process_text(headline, accent)}</div>')
        if code:
            parts.append(f'<div class="code-block" style="position: relative; left: 0; top: 0; width: 100%;">{_format_code(code)}</div>')
        if body:
            parts.append(f'<div class="body" style="margin-top: 16px;">{_process_text(body, accent)}</div>')

    elif slide_type == "checklist":
        if label:
            parts.append(f'<div class="label">{_escape(label)}</div>')
        parts.append(f'<div class="headline" style="font-size: 44px;">{_process_text(headline, accent)}</div>')
        parts.append(f'<div class="spacer-fixed" style="height: 24px;"></div>')
        items_html = ""
        for i, item in enumerate(checklist):
            highlighted = ' class="highlighted"' if item.get("highlight") else ""
            items_html += f'<li{highlighted}>{_process_text(item.get("text", ""), accent)}</li>'
        parts.append(f'<ul class="checklist">{items_html}</ul>')

    else:  # steps, screenshot, data, or generic content
        parts.append('<div class="text-bg">')
        if label:
            parts.append(f'<div class="label">{_escape(label)}</div>')
        parts.append(f'<div class="headline" style="font-size: 48px;">{_process_text(headline, accent)}</div>')
        if body:
            parts.append(f'<div class="body">{_process_text(body, accent)}</div>')
        if subtext:
            parts.append(f'<div class="subtext">{_escape(subtext)}</div>')
        parts.append('</div>')
        # Add spacer for slides with screenshots (visual takes up middle area)
        if slide_type == "screenshot":
            parts.append(f'<div class="spacer-fixed" style="height: 480px;"></div>')
        elif slide_type == "data":
            parts.append(f'<div class="spacer-fixed" style="height: 400px;"></div>')

    # Handle
    parts.append(f'<div class="handle">{_escape(handle)}</div>')

    # Swipe cue
    if show_swipe:
        parts.append('<div class="swipe-cue">SWIPE &gt;</div>')

    # Progress dots
    dots = ""
    for i in range(1, total_slides + 1):
        active = " active" if i == number else ""
        dots += f'<div class="dot{active}"></div>'
    parts.append(f'<div class="progress">{dots}</div>')

    return "\n  ".join(parts)


def _escape(text):
    """HTML escape."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _process_text(text, accent_color):
    """Process text with accent markers: *word* becomes highlighted, **word** becomes bold."""
    import re
    # Bold: **word**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Accent highlight: *word*
    text = re.sub(r'\*(.+?)\*', f'<span class="accent">\\1</span>', text)
    return text


def _format_code(code):
    """Basic syntax coloring for terminal-style code."""
    lines = code.split("\n")
    formatted = []
    for line in lines:
        if line.strip().startswith("$"):
            formatted.append(f'<span class="prompt">$</span>{_escape(line.strip()[1:])}')
        elif line.strip().startswith("#"):
            formatted.append(f'<span class="comment">{_escape(line)}</span>')
        elif line.strip().startswith('"') or line.strip().startswith("'"):
            formatted.append(f'<span class="string">{_escape(line)}</span>')
        else:
            formatted.append(_escape(line))
    return "\n".join(formatted)


def render_text_overlay(html_content, output_path, config):
    """Render text overlay HTML to transparent PNG using Playwright."""
    template = TEMPLATE_PATH.read_text()
    accent = config.get("accent_color", "#7FB685")

    # Fill template variables
    filled = template.replace("{{FONT_PATH}}", str(FONTS_PATH))
    filled = filled.replace("{{ACCENT_COLOR}}", accent)
    filled = filled.replace("{{HEADLINE_COLOR}}", "#2C2926")
    filled = filled.replace("{{BODY_COLOR}}", "#2C2926")
    filled = filled.replace("{{LABEL_COLOR}}", "#6B6560")
    filled = filled.replace("{{HEADLINE_SIZE}}", "52px")
    filled = filled.replace("{{BODY_SIZE}}", "26px")
    filled = filled.replace("{{CODE_LEFT}}", "60px")
    filled = filled.replace("{{CODE_TOP}}", "auto")
    filled = filled.replace("{{CODE_WIDTH}}", "960px")
    filled = filled.replace("{{SPACER_HEIGHT}}", "40px")
    filled = filled.replace("{{CONTENT}}", html_content)

    # Write temp HTML file
    temp_html = output_path.replace(".png", ".html")
    with open(temp_html, "w") as f:
        f.write(filled)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        page.goto(f"file://{os.path.abspath(temp_html)}", wait_until="networkidle")
        page.wait_for_timeout(500)  # Wait for fonts
        page.screenshot(path=output_path, omit_background=True)
        browser.close()

    # Clean up temp HTML
    os.remove(temp_html)
    return output_path


def composite_layers(visual_path, text_path, output_path):
    """Composite text overlay on top of visual layer using PIL."""
    try:
        from PIL import Image
    except ImportError:
        print("Pillow not installed. Installing...")
        os.system(f"{sys.executable} -m pip install Pillow -q")
        from PIL import Image

    visual = Image.open(visual_path).convert("RGBA").resize((1080, 1350), Image.LANCZOS)
    text = Image.open(text_path).convert("RGBA")

    # Composite text on visual
    result = Image.alpha_composite(visual, text)
    result.save(output_path, "PNG")
    print(f"  Composited -> {output_path}")


def process_carousel(config_path):
    """Process a full carousel from config.json."""
    config_path = Path(config_path)
    with open(config_path) as f:
        config = json.load(f)

    carousel_dir = config_path.parent
    slides_dir = carousel_dir / "slides"
    visuals_dir = carousel_dir / "visuals"
    slides_dir.mkdir(exist_ok=True)

    slides = config["slides"]
    total = len(slides)

    print(f"Processing carousel: {config.get('slug', 'unknown')} ({total} slides)")

    for slide in slides:
        n = slide["number"]
        print(f"\n  Slide {n}/{total} ({slide.get('type', 'content')}):")

        # Generate text HTML
        text_html = generate_text_html(slide, config, total)

        # Render text overlay
        text_png = str(carousel_dir / f"text-{n:02d}.png")
        render_text_overlay(text_html, text_png, config)
        print(f"    Text overlay rendered")

        # Check for visual layer
        visual_path = carousel_dir / slide.get("visual_path", f"visuals/visual-{n:02d}.png")
        if not visual_path.exists():
            print(f"    Warning: visual layer not found at {visual_path}")
            print(f"    Saving text-only slide")
            # Just copy text overlay as the slide
            import shutil
            shutil.copy2(text_png, str(slides_dir / f"slide-{n:02d}.png"))
        else:
            # Composite
            output_path = str(slides_dir / f"slide-{n:02d}.png")
            composite_layers(str(visual_path), text_png, output_path)

        # Clean up text PNG
        if os.path.exists(text_png):
            os.remove(text_png)

    print(f"\nDone! Slides saved to {slides_dir}/")

    # Auto-open in Preview
    slide_files = sorted(slides_dir.glob("slide-*.png"))
    if slide_files:
        os.system(f"open {' '.join(str(f) for f in slide_files)}")


def main():
    parser = argparse.ArgumentParser(description="Composite carousel visual + text layers")
    parser.add_argument("--config", required=True, help="Path to carousel config.json")
    args = parser.parse_args()
    process_carousel(args.config)


if __name__ == "__main__":
    main()
