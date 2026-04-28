#!/usr/bin/env python3
"""
Crop a 1080x1440 (3:4) kie.ai output down to 1080x1350 (4:5) for Instagram.

Default behavior trims equally from top and bottom (45px each side).
Pass --top-bias or --bottom-bias to shift the crop.

Usage:
    python3 crop_to_4x5.py images/anchor-v1.png
    python3 crop_to_4x5.py images/slide-2.png --out images/final/slide-2.png
    python3 crop_to_4x5.py images/anchor-v1.png --top-bias 0   # keep all of top, trim 90px from bottom
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("error: Pillow not installed. Run: python3 -m pip install Pillow", file=sys.stderr)
    raise SystemExit(2)

TARGET_W = 1080
TARGET_H = 1350


def crop(path: Path, out: Path, top_bias: int | None, bottom_bias: int | None) -> None:
    img = Image.open(path)
    w, h = img.size
    if w != TARGET_W:
        new_h = round(h * TARGET_W / w)
        img = img.resize((TARGET_W, new_h), Image.LANCZOS)
        w, h = img.size
    excess = h - TARGET_H
    if excess < 0:
        canvas = Image.new("RGB", (TARGET_W, TARGET_H), color=img.getpixel((0, 0)))
        canvas.paste(img, (0, 0))
        canvas.save(out)
        return
    if top_bias is not None:
        top = max(0, min(excess, top_bias))
    elif bottom_bias is not None:
        top = max(0, excess - max(0, min(excess, bottom_bias)))
    else:
        top = excess // 2
    bottom = top + TARGET_H
    cropped = img.crop((0, top, TARGET_W, bottom))
    cropped.save(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Crop a 3:4 image to 4:5 (1080x1350) for Instagram.")
    parser.add_argument("path", type=Path, help="Input image path.")
    parser.add_argument("--out", type=Path, help="Output path (default: alongside input as <stem>-4x5.png, or images/final/<name> if input is in images/).")
    parser.add_argument("--top-bias", type=int, help="Pixels to trim from the top (rest from bottom).")
    parser.add_argument("--bottom-bias", type=int, help="Pixels to trim from the bottom (rest from top).")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"error: {args.path} not found", file=sys.stderr)
        return 1

    if args.out:
        out = args.out
    elif args.path.parent.name == "images":
        out = args.path.parent / "final" / args.path.name
        out.parent.mkdir(exist_ok=True)
    else:
        out = args.path.with_name(f"{args.path.stem}-4x5{args.path.suffix}")

    crop(args.path, out, args.top_bias, args.bottom_bias)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
