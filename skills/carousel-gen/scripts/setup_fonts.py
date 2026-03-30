#!/usr/bin/env python3
"""One-time font downloader for carousel text overlay.
Downloads Playfair Display, Plus Jakarta Sans, and JetBrains Mono from Google Fonts.
"""
import os
import urllib.request
import zipfile
import shutil
import sys

FONTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")

FONT_URLS = {
    "PlayfairDisplay": "https://fonts.google.com/download?family=Playfair+Display",
    "PlusJakartaSans": "https://fonts.google.com/download?family=Plus+Jakarta+Sans",
    "JetBrainsMono": "https://fonts.google.com/download?family=JetBrains+Mono",
}

# Which specific files we want from each download
WANTED_FILES = {
    "PlayfairDisplay": ["PlayfairDisplay-Bold.ttf", "PlayfairDisplay-Black.ttf", "PlayfairDisplay-Regular.ttf"],
    "PlusJakartaSans": ["PlusJakartaSans-Regular.ttf", "PlusJakartaSans-Medium.ttf", "PlusJakartaSans-Bold.ttf", "PlusJakartaSans-SemiBold.ttf"],
    "JetBrainsMono": ["JetBrainsMono-Regular.ttf"],
}


def download_font_family(name, url):
    zip_path = os.path.join(FONTS_DIR, f"{name}.zip")
    extract_dir = os.path.join(FONTS_DIR, f"_{name}_temp")

    print(f"Downloading {name}...")
    try:
        urllib.request.urlretrieve(url, zip_path)
    except Exception as e:
        print(f"  Failed to download {name}: {e}")
        return False

    print(f"  Extracting...")
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)
    except Exception as e:
        print(f"  Failed to extract {name}: {e}")
        os.remove(zip_path)
        return False

    # Find and copy wanted TTF files
    wanted = WANTED_FILES.get(name, [])
    found = 0
    for root, dirs, files in os.walk(extract_dir):
        for f in files:
            if f in wanted or (not wanted and f.endswith(".ttf")):
                src = os.path.join(root, f)
                dst = os.path.join(FONTS_DIR, f)
                shutil.copy2(src, dst)
                print(f"  Saved: {f}")
                found += 1

    # Also grab any static TTF variants if the wanted files weren't found at top level
    if found == 0:
        for root, dirs, files in os.walk(extract_dir):
            for f in files:
                if f.endswith(".ttf") and "static" in root.lower():
                    # Check if basename matches any wanted pattern
                    for w in wanted:
                        base = w.replace(".ttf", "").replace("-", "")
                        if base.lower() in f.lower().replace("-", ""):
                            src = os.path.join(root, f)
                            dst = os.path.join(FONTS_DIR, f)
                            shutil.copy2(src, dst)
                            print(f"  Saved (static): {f}")
                            found += 1

    # Cleanup
    os.remove(zip_path)
    shutil.rmtree(extract_dir)

    if found == 0:
        print(f"  Warning: No matching TTF files found for {name}")
        return False

    return True


def main():
    os.makedirs(FONTS_DIR, exist_ok=True)

    # Check if fonts already exist
    existing = [f for f in os.listdir(FONTS_DIR) if f.endswith(".ttf")]
    if existing:
        print(f"Fonts already downloaded ({len(existing)} files):")
        for f in sorted(existing):
            print(f"  {f}")
        if "--force" not in sys.argv:
            print("Use --force to re-download.")
            return

    success = 0
    for name, url in FONT_URLS.items():
        if download_font_family(name, url):
            success += 1

    print(f"\nDone. {success}/{len(FONT_URLS)} font families downloaded.")

    # List final fonts
    final = [f for f in os.listdir(FONTS_DIR) if f.endswith(".ttf")]
    print(f"Font files in {FONTS_DIR}:")
    for f in sorted(final):
        print(f"  {f}")


if __name__ == "__main__":
    main()
