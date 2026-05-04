# Render Contract — The 4 Lint Walls + Fixes

Hyperframes has a strict render contract. These are the four lint errors that block first preview every time, plus the exact fixes. Reference proactively when authoring any new composition - they're cheaper to avoid than to debug.

---

## 1. Audio echo / phase delay (the sneakiest)

**Symptom:** Audio sounds delayed, reverby, or echoing. Captions feel off-sync. Sometimes manifests as a faint chorus effect rather than obvious echo.

**Cause:** Splitting `edited.mp4` into `edited-noaudio.mp4` (video) + `edited.m4a` (audio) and using both in the composition. AAC has ~25ms priming silence at the start of the audio packet, so when the audio element plays it, it's offset from the video frame's PTS=0. Result: phase mismatch heard as echo.

**Fix:**

```html
<video id="speaker-video" src="assets/edited.mp4"
       data-has-audio="true"
       data-start="0" data-duration="X" data-track-index="0"></video>
```

- Single mp4 file. Both video and audio in the same container.
- `data-has-audio="true"` so the mixer feeds the video's audio into the master.
- **NO `muted` attribute.** Lint will say muted + data-has-audio is a conflict.
- **NO sibling `<audio>` element.** That's what causes the double-decode.

When you genuinely need a sibling audio file (e.g., separate music bed), give the video its own track-index and the audio a much higher track-index, and accept that you can't combine the speaker's mp4 audio with a sibling music file via the speaker's mp4 - you'd need to mux them externally first.

---

## 2. `video_nested_in_timed_element`

**Symptom:** Lint says video will be FROZEN in renders.

**Cause:** Putting `data-start` on BOTH the wrapper div AND the nested video element.

**Fix:** Pick one. Convention: put `data-start` on the `<video>` element itself, leave the wrapper div as a non-timed visual container with no timing attributes:

```html
<!-- WRONG -->
<div class="speaker-wrapper clip" data-start="0" data-duration="47" data-track-index="0">
  <video src="assets/edited.mp4" data-start="0" data-duration="47" data-track-index="0"></video>
</div>

<!-- RIGHT -->
<div class="speaker-wrapper">
  <video id="speaker-video" src="assets/edited.mp4"
         data-has-audio="true"
         data-start="0" data-duration="47" data-track-index="0"></video>
</div>
```

---

## 3. `media_missing_id`

**Symptom:** Video or audio elements throw errors on render.

**Fix:** Every `<video>` and `<audio>` element needs an `id` attribute. The renderer needs it to discover the media. Trivial but easy to miss when copying templates.

```html
<video id="speaker-video" src="..." ...></video>
<audio id="music-bed" src="..." ...></audio>
```

---

## 4. `overlapping_clips_same_track`

**Symptom:** Lint says clips overlap on track N.

**Fix:** Different `data-track-index` per overlapping clip. Audio elements should go on a high track number (e.g., 50) to avoid clashing with visual layers. Track index does NOT affect z-order - z-order comes from CSS. Track is purely for clip-conflict detection.

A safe convention:

| Track range | Use |
|-------------|-----|
| 0 | Speaker `<video>` (the spine) |
| 1 | Karaoke caption pill |
| 2-19 | Frosted-glass overlay cards (one per beat) |
| 20-29 | Body-level captions (if not using a pill) |
| 30-49 | Background layers (grain, vignette, grid) |
| 50+ | Audio elements |

---

## Less-blocking warnings (still worth fixing)

### `gsap_exit_missing_hard_kill`

After every `tl.to(el, { opacity: 0 })` exit at a clip boundary, add `tl.set(el, { opacity: 0 }, exitEnd)` so non-linear seeking lands in the right state. Cheap fix, cleaner playback during scrubbing.

### `gsap_css_transform_conflict`

Don't set `transform: rotate(-6deg)` in CSS and then `gsap.to(..., { x, y })` - GSAP overwrites the whole transform. Use `tl.fromTo(el, { rotate: -6, x: 0, y: 30 }, { ... })` to set initial state via GSAP instead.

### `overlapping_gsap_tweens`

If you have two tweens on the same property of the same element, add `overwrite: 'auto'` to the later one or move them apart in time.

---

## The build_index.py pattern

For karaoke captions or any large embedded data, use a Python build script that templates the HTML and inlines JSON via `__PLACEHOLDER__` substitution. Keeps the HTML editable while the JSON stays compact:

```
video-projects/<your-slug>/
├── build_index.py          # generator
├── words-compact.json      # transcript data (input to generator)
└── index.html              # generated output (lint-clean)
```

Run `python3 build_index.py` after every CSS or HTML edit to regenerate. See `templates/build_index.py` for the generic version.

---

## How to apply

When starting a new composition:

1. Read this file before writing any audio or video element.
2. Use the `templates/index.html.template` as the structural starting point.
3. Lint after every iteration (`npx hyperframes lint`). Fix errors immediately, defer warnings.
4. Don't try to optimize for "no warnings" - `composition_file_too_large` and small overlap warnings are non-blocking.
