# Motion Philosophy — The 11 Laws

The motion-graphics aesthetic baseline for any composition built with this skill. Re-read sections 0 and 4 at the start of any creative session - they're the discipline.

These laws are deconstructed from a reference 30-second motion-graphics spot. Apply them whenever you're building a fresh composition, picking transitions, designing kinetic typography, or composing a logo reveal.

---

## 0 · The 11 Laws (memorize)

1. **One idea per beat. Cut fast.** Average scene length is ~1.5 seconds. Each visual lands ONE word or concept and moves on. If a scene says two things, split it.
2. **Black is the canvas.** ~90% of every frame is black or near-black. Negative space is the design. Color earns its place by carrying a message.
3. **Light is the brand, not color.** Chrome gradients on type, soft halos, vignettes, light beams. The piece is *lit*, not *colored*. Light reads as premium.
4. **Camera never sleeps.** Even on "still" frames, the grid recedes, particles drift, the vignette breathes. Static = death.
5. **Motion blur is a feature.** Every transition uses a streak or blur trail to convey energy AND to mask the cut. Hard cuts feel cheap; whip-streaks feel expensive.
6. **Object metaphors carry meaning.** A red card = old or broken. A teal coin = new or working. The same coin returns three times across the piece. Visual continuity = brand.
7. **Palette is symbolic, not decorative.** Each color owns one concept. Don't drop a color in just because it looks nice - assign it a meaning.
8. **Type is a character.** Words SCALE 8x, MORPH, COMPRESS, GLOW. Typography drives ~60% of the storytelling. A text-only beat can be the strongest beat.
9. **Hold the hero shot.** Logo reveal = ~2s of stillness. Outro card = 5+ seconds. Speed earns space for stillness to land. Kinetic chaos to calm = catharsis.
10. **One unifying texture across everything.** A faint perspective grid plus crosshair markers at intersections. Even when invisible, the grid is the spine of the whole piece.
11. **Timelines must fill their slots.** Hyperframes hides a sub-composition the moment `timeline.duration()` is shorter than `data-duration` - black frame flash. Every GSAP timeline ends with `tl.to({}, { duration: SLOT_DURATION }, 0)` as a no-op duration anchor. Non-negotiable.

---

## Pacing discipline

- **Default scene length:** 1.0-2.0 seconds. If a scene is longer, it had better be a hero moment or the outro.
- **Reveal cadence:** new visual element every 0.3-0.6s within a scene. No dead air >1s mid-piece.
- **Word-reveal stagger:** 0.3-0.4s per word for narrative reads, 0.5-0.6s for dramatic single-word emphasis.
- **Whip transition duration:** 0.3-0.4s. Faster feels glitchy; slower loses energy.
- **Hold durations:**
  - Logo crystallization: 1.5-2s
  - Final CTA card: 4-6s (the longest single shot in the piece)
  - Section headlines: 1-1.5s of read time after fully revealed
- **The breathing rule:** every ~7-8s of kinetic density, give the viewer a 1s "rest" beat.

---

## Easings by purpose

| Purpose | Ease | Typical duration |
|---|---|---|
| Word reveal (slide-in) | `expo.out` | 0.20-0.33s |
| Generic element enter | `power2.out` | 0.2-0.5s |
| Generic element exit | `power2.in` | 0.2-0.33s |
| Beat-to-beat whip EXIT | `expo.in` / `power2.in` | 0.2-0.33s |
| Beat-to-beat whip ENTRY | `expo.out` / `power2.out` | 0.5-1.0s |
| Camera pan between stops | `power2.inOut` | 1.2-2.3s |
| Linear hold (after entry) | `"none"` | 0.4-0.65s |
| Bouncy card settle | `back.out(1.2)` to `back.out(1.5)` | 0.3-0.5s |
| Click compress | `power4.in` | 0.07s (70ms) |
| Click release (overshoot) | `back.out(3)` | 0.30s |
| UI overshoot (settle) | `elastic.out(1, 0.3)` to `elastic.out(1, 0.4)` | 0.20s |
| Continuous rotation | `"none"` | full beat |
| Breathe / drift | `sine.inOut` yoyo | 2-4s, `repeat: -1` |

**Defaults pattern:** don't use `gsap.defaults()` - every tween declares its ease and duration explicitly. Inheritance bugs are harder to diagnose than verbose tweens.

---

## Audio mix defaults

Every scene with audio sets `data-volume` explicitly. Don't reach for a music track by default - a 0.15 warm pad is almost always the right answer.

| Layer | `data-volume` | Role |
|------|---------------|------|
| Voiceover | `1.0` | Primary, drives timing |
| Underscore (warm ambient pad) | `0.15` | Barely there - sets mood without competing |
| SFX (clicks, twinkles, whooshes) | `0.2` | Tails allowed to bleed into next beat |

Wire as sibling `<audio>` elements in the root composition, **not** inside a `<video>` (when the video has its own embedded audio - see `render-contract-gotchas.md`). Music-free is a valid choice; pad-only is premium; full music cue is last resort.

---

## 4 · Pre-flight Checklist (before claiming any motion piece is "done")

- [ ] **Average scene length less than or equal to 2s** in mid-section (intro and outro can hold longer)
- [ ] **No dead air more than 1s** anywhere except the deliberate hold moments
- [ ] **Every transition uses motion** (whip, morph, slide, recolor - no hard fades)
- [ ] **Color palette less than or equal to 5 active hues** total in the whole piece, each with a meaning
- [ ] **Every text block uses chrome gradient + halo** - no flat white (override per archetype if needed)
- [ ] **Background grid + crosshairs present in greater than or equal to 60% of scenes** (the unifying texture)
- [ ] **Vignette layer on top of every scene** (don't ship a flat-lit composition)
- [ ] **Grain overlay on every scene** (subtle, but there)
- [ ] **One callback minimum** - a visual element that returns later
- [ ] **Outro holds for 4+ seconds** (silence after the kinetic act)
- [ ] **Visual verification done** - extracted frames, opened them, confirmed: no cropped faces, no text overflow, no scene landing on the wrong word, no broken transitions
- [ ] **Every sub-composition timeline ends with `tl.to({}, { duration: SLOT_DURATION }, 0)`** - kills black-frame flashes at beat tails (Law 11)
- [ ] **All tween end-times snap to multiples of `1/fps`** - at 30fps: 0.0333, 0.0667, 0.1, 0.1333... Steep-tail easings (`expo.in`, `power4.in`) visibly alias at sub-frame boundaries
- [ ] **Ran the timeline-duration diagnostic** - open Studio preview, run this in the devtools console, and compare every value against the `data-duration` on its host:

```js
const p = document.querySelector('hyperframes-player');
const iw = p.shadowRoot.querySelector('iframe').contentWindow;
Object.fromEntries(Object.entries(iw.__timelines).map(([k, v]) =>
  [k, +v.duration().toFixed(4)]));
```

Any gap where `timeline.duration() < data-duration` is a black-frame risk.

---

## Anti-patterns

- Centered, axis-aligned, motionless text fades. Always add scale, blur, or directional energy.
- Hard cuts between scenes. Every cut needs a transition element bridging it (streak, morph, wipe, shader). Exception: `screen-face-split` archetype uses hard cuts intentionally.
- Flat white text on flat black background. Use chrome gradient and halo glow.
- 6+ colors across the piece. You're decorating, not communicating.
- No callbacks. A visual element that appears once and never returns wastes a setup.
- Outro that ends on the last beat. Always hold the CTA for 4+ seconds.
- Scenes that try to say two things. Split into two scenes.
- Static backgrounds. Every background should have at least one slow-moving element (parallax grid, drifting particles, breathing vignette).
- `Math.random()` / `Date.now()` / unseeded PRNGs inside a render loop. Renders must be deterministic frame-to-frame. Use harmonic hashes: `80 + 220 * Math.abs(Math.sin(i*0.7 + 0.3) * Math.cos(i*1.3 + 0.7))` gives "random-looking" reproducible values.
- Forgetting to render a draft and look at it. Lint passing is not the same as design working. **VIEW THE FRAMES.**

---

## TL;DR — The philosophy in one sentence

> One idea per beat, lit not colored, kinetic not still, callbacks not novelty, hold the hero, breathe the outro - the grid is always under everything, every timeline fills its slot, every exit snaps to a frame boundary, and every cut hides inside a motion-blurred whip.
