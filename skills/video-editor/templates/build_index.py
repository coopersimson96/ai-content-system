#!/usr/bin/env python3
"""Build index.html with the karaoke words JSON embedded inline.

Usage: copy this file into your project folder, edit the HTML template
inside, then run `python3 build_index.py` to regenerate index.html.

The script reads `words-compact.json` (transcript chunks, see
`words-compact.json.example`), flattens the chunks into a single word
list, and substitutes that into the HTML at the `__WORDS_JSON__`
placeholder.

Why this pattern:
- The HTML stays editable - you don't paste hundreds of words in by hand.
- The transcript data stays compact - one JSON file, one source of truth.
- Lint-clean every time - the generated index.html has no orphan ID
  collisions, no stale data, and no formatting drift.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
chunks = json.loads((HERE / "words-compact.json").read_text())

# Flatten chunked words into a single list. Each chunk is a sub-array of
# {t: text, s: start_seconds, e: end_seconds} dicts.
WORDS = [w for chunk in chunks for w in chunk]
words_json = json.dumps(WORDS, separators=(",", ":"))

# Replace this template with your composition. Keep the __WORDS_JSON__
# placeholder where the transcript data should land.
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Your video title</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@800;900&family=JetBrains+Mono:wght@500;700&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&display=swap" rel="stylesheet" />
<style>
:root {
  /* Default brand tokens — override in your project's BRAND.md */
  --brand-tint: #ff7a1a;
  --brand-tint-glow: rgba(255, 122, 26, 0.55);
  --karaoke-bg: rgba(195, 175, 230, 0.94);
  --karaoke-text: #1f3a2c;

  --text-shadow-hard: 1.5px 1.5px 0 rgba(0,0,0,0.92), 0 4px 14px rgba(0,0,0,0.45);
  --text-shadow-hard-lg: 2px 2px 0 rgba(0,0,0,0.92), 0 6px 22px rgba(0,0,0,0.45);
  --text-shadow-hard-xl: 3px 3px 0 rgba(0,0,0,0.92), 0 8px 28px rgba(0,0,0,0.5);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #000; overflow: hidden; }

#composition-root {
  position: relative;
  width: 1080px;
  height: 1920px;
  overflow: hidden;
  background: #000;
}
.speaker-wrapper { position: absolute; inset: 0; }
.speaker-wrapper video { width: 100%; height: 100%; object-fit: cover; }

.frosted-card {
  position: absolute;
  background: rgba(255, 122, 26, 0.62);
  backdrop-filter: blur(20px) saturate(1.2);
  -webkit-backdrop-filter: blur(20px) saturate(1.2);
  border: 1.5px solid rgba(255, 255, 255, 0.32);
  border-radius: 32px;
  box-shadow:
    inset 0 1.5px 0 rgba(255, 255, 255, 0.5),
    inset 0 -1px 0 rgba(0, 0, 0, 0.12),
    0 22px 56px rgba(0, 0, 0, 0.42),
    0 0 38px rgba(255, 122, 26, 0.28);
  color: #ffffff;
  text-shadow: var(--text-shadow-hard);
  text-align: center;
  opacity: 0;
}

.karaoke-pill-wrap {
  position: absolute;
  left: 0; right: 0;
  top: 1380px;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}
.karaoke-pill {
  display: inline-block;
  padding: 14px 32px;
  border-radius: 22px;
  background: var(--karaoke-bg);
  color: var(--karaoke-text);
  font-family: 'Inter', sans-serif;
  font-weight: 900;
  font-size: 78px;
  letter-spacing: -0.015em;
  line-height: 1.0;
  box-shadow:
    0 0 0 1.5px rgba(255, 255, 255, 0.42),
    0 6px 22px rgba(195, 175, 230, 0.4),
    0 16px 44px rgba(0, 0, 0, 0.32);
  white-space: nowrap;
  opacity: 0;
}
</style>
</head>
<body>

<div id="composition-root" data-composition-id="composition-root" data-start="0" data-width="1080" data-height="1920">

  <!-- Speaker (single mp4 with embedded audio - see render-contract-gotchas.md) -->
  <div class="speaker-wrapper">
    <video id="speaker-video" src="assets/edited.mp4"
           data-has-audio="true"
           data-start="0" data-duration="REPLACE_DURATION" data-track-index="0"></video>
  </div>

  <!-- Karaoke single pill -->
  <div class="karaoke-pill-wrap clip" data-start="0" data-duration="REPLACE_DURATION" data-track-index="1">
    <span class="karaoke-pill" id="karaoke-pill">&nbsp;</span>
  </div>

  <!-- Add your beat overlays as .frosted-card elements with .clip + data-start / data-duration / data-track-index here -->

</div>

<script id="words-data" type="application/json">__WORDS_JSON__</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script>
(() => {
  const WORDS = JSON.parse(document.getElementById('words-data').textContent);
  const pillEl = document.getElementById('karaoke-pill');

  gsap.defaults({ ease: 'expo.out' });
  const tl = gsap.timeline({ paused: true });

  // ---------- Karaoke ----------
  // Caption sync offset: negative = fire captions earlier.
  // Tested as the right offset for single-mp4 + data-has-audio="true".
  const KARAOKE_LEAD = -0.03;
  WORDS.forEach((w, i) => {
    const next = WORDS[i + 1];
    const gapToNext = next ? next.s - w.e : Infinity;
    const wStart = Math.max(0, w.s + KARAOKE_LEAD);
    const wEnd = Math.max(wStart + 0.05, w.e + KARAOKE_LEAD);
    tl.call(() => { pillEl.textContent = w.t; }, null, wStart);
    tl.to(pillEl, { opacity: 1, duration: 0.06 }, wStart);
    if (gapToNext > 0.18) {
      tl.to(pillEl, { opacity: 0, duration: 0.12 }, wEnd);
    }
  });
  if (WORDS.length) {
    tl.to(pillEl, { opacity: 0, duration: 0.2 }, WORDS[WORDS.length - 1].e + 0.05 + KARAOKE_LEAD);
  }

  // ---------- Beat tweens ----------
  // Add your per-beat overlay tweens here. Pattern:
  //
  //   tl.fromTo('#beat-1',
  //     { opacity: 0, y: -28, scale: 0.94 },
  //     { opacity: 1, y: 0, scale: 1, duration: 0.45 },
  //     <beat-start-seconds>);
  //   tl.to('#beat-1', { opacity: 0, y: -16, duration: 0.3, ease: 'expo.in' },
  //     <beat-end-seconds-minus-0.3>);
  //   tl.set('#beat-1', { opacity: 0 }, <beat-end-seconds>);

  // Pad the timeline to your video's full duration (Law 11)
  tl.set({}, {}, /* REPLACE: your video duration in seconds */ 47.0);

  window.__timelines = window.__timelines || {};
  window.__timelines['composition-root'] = tl;
})();
</script>

</body>
</html>
"""

(HERE / "index.html").write_text(HTML.replace("__WORDS_JSON__", words_json))
print(f"Wrote index.html ({(HERE / 'index.html').stat().st_size:,} bytes)")
