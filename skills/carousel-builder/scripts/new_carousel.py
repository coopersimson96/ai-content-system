#!/usr/bin/env python3
"""
Scaffold a new carousel folder.

Usage:
    python3 new_carousel.py "Claude Council prompts"
    python3 new_carousel.py "Email teardown - some brand" --skin field-manual --slides 6
    python3 new_carousel.py "Prompt stack" --root ~/work/carousels

Creates:
    <root>/YYYY-MM-DD-slug/
        01-strategy.md ... 08-consistency-check.md (stubs from templates/)
        images/
        images/final/

Default root is ~/carousels/. Override with --root.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

DEFAULT_ROOT = Path.home() / "carousels"
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

ARTIFACTS = [
    ("01-strategy.md", "intake.md"),
    ("02-slide-copy.md", "slide-copy.md"),
    ("03-graphic-plan.md", None),
    ("04-asset-list.md", None),
    ("05-visual-brief.md", "visual-brief.md"),
    ("06-anchor-options.md", None),
    ("07-slide-prompts.md", None),
    ("08-consistency-check.md", "consistency-check.md"),
]


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:60] or "carousel"


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new carousel folder.")
    parser.add_argument("title", help="Working title for the carousel.")
    parser.add_argument(
        "--skin",
        default="field-manual",
        help="Style skin name (default: field-manual). Build your own per references/build-your-own-skin.md.",
    )
    parser.add_argument(
        "--slides",
        type=int,
        default=8,
        help="Slide count (default: 8).",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"Override root dir (default: {DEFAULT_ROOT}).",
    )
    args = parser.parse_args()

    today = date.today().isoformat()
    slug = slugify(args.title)
    folder = args.root / f"{today}-{slug}"

    if folder.exists():
        print(f"error: {folder} already exists", file=sys.stderr)
        return 1

    folder.mkdir(parents=True)
    (folder / "images").mkdir()
    (folder / "images" / "final").mkdir()

    for filename, template_name in ARTIFACTS:
        target = folder / filename
        if template_name and (TEMPLATES_DIR / template_name).exists():
            shutil.copyfile(TEMPLATES_DIR / template_name, target)
        else:
            target.write_text(f"# {filename.removesuffix('.md').replace('-', ' ').title()}\n\n_to fill_\n")

    meta_lines = [
        f"title: {args.title}",
        f"slug: {slug}",
        f"date: {today}",
        f"skin: {args.skin}",
        f"slides: {args.slides}",
    ]
    (folder / "_meta.txt").write_text("\n".join(meta_lines) + "\n")

    print(folder)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
