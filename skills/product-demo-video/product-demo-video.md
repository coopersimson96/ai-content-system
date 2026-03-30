# Product Demo Video Generator

Generate polished, animated product demo videos using Remotion. Produces both portrait (1080x1920) and landscape (1920x1080) versions with background music and transition sounds.

**Triggers on:** "demo video", "product video", "app demo", "showcase video", "promo video", "/demo-video"

---

## Input

Collect from the user (ask if not provided):

| Field | Required | Description |
|-------|----------|-------------|
| `productName` | Yes | Product/app name |
| `tagline` | Yes | One-line tagline |
| `colors` | Yes | Primary color hex, accent color hex, background color hex |
| `features` | Yes | 3-5 key features, each with: title, subtitle, emoji icon |
| `screens` | Yes | 3 app screens to showcase. Either: screenshots (file paths), URLs to capture, or descriptions to render as styled components |
| `hook` | No | Opening hook text. Default: "Stop [old way]. Start [new way]." |
| `cta` | No | CTA button text. Default: "Get Started for Free" |
| `url` | No | Product URL for closing slide |
| `industries` | No | Target industries for closing pills |
| `duration` | No | Target length in seconds. Default: 20 |
| `musicStyle` | No | "upbeat" (default), "ambient", "cinematic", or path to custom .mp3 |

---

## Architecture

### Project Location
Use the existing Remotion studio at `~/Desktop/AI Projects/remotion-studio/`.
Create composition files in `src/compositions/{ProductName}Demo/`.
Store assets in `public/{product-name}/`.

### Scene Structure (7 scenes)
Every video follows this proven structure. Timing is proportional to total duration:

| Scene | % of Duration | Content | Background |
|-------|--------------|---------|------------|
| 1. Hook | 14% | Problem statement with strikethrough, replacement text pops in | Bright accent color |
| 2. Brand Reveal | 13% | Logo icon + product name + tagline, color wipe transition | White |
| 3. Feature Hero | 24% | Phone mockup LEFT, headline + 3 feature cards RIGHT | Light tint of primary |
| 4. Screen 2 | 18% | Text LEFT + phone mockup RIGHT (mirrored from scene 3) | Primary dark |
| 5. Screen 3 | 16% | Phone mockup LEFT + text RIGHT (mirrored from scene 4) | Light/white |
| 6. Social Proof | 14% | Avatars + team/trust element, no phone | Bright accent |
| 7. CTA | 16% | Logo + tagline + CTA button + industry pills | Primary dark |

Scenes overlap by ~0.3s for smooth crossfades.

### Visual Rules (learned from iteration)

**DO:**
- Use `Plus Jakarta Sans` (headlines, 800 weight) and `DM Sans` (body, 400-600 weight) via `@remotion/google-fonts`
- Headlines: minimum 68px in scenes, 80px+ for hero moments
- Body text: minimum 24px, never below 18px
- Phone mockups: 380x780px portrait with 50px border-radius, 6px dark border, Dynamic Island notch
- Feature cards: minimum 440px wide, 60px icon squares, 26px title, 18px subtitle
- Split layouts: `display: flex, alignItems: center, gap: 24, padding: 0 28px`
- Color wipe transitions between scenes using `clipPath: inset()` animation
- Spring animations: `{ damping: 12, stiffness: 100, mass: 0.4 }` for snappy, `{ damping: 16, stiffness: 50, mass: 1.2 }` for dramatic
- Phone floats with subtle `Math.sin(frame / (1.5 * fps)) * 4` translateY
- Phone tilts with 3D perspective: `perspective(1200px) rotateY(5deg)`
- Stagger elements: each item delays 0.15-0.25s after the previous
- Fill the frame - minimal dead space, tight margins

**DON'T:**
- Use text smaller than 18px anywhere
- Leave large empty gaps above/below phone mockups
- Use dark/moody backgrounds exclusively - alternate bright and dark
- Put more than 2 lines of body text per scene
- Use generic sans-serif fonts (Inter, Arial, etc.)
- Make transitions slower than 0.5s
- Put small pills/badges at the bottom of the frame - integrate them into the layout

### Animated Phone Screens

Phone screens MUST be animated, not static. Each screen should include:

**Recording/Input screens:**
- Live waveform/audio bars that pulse
- Counter/timer counting up
- Text appearing word by word (transcript effect)
- Status cards sliding in from bottom

**Data/Results screens:**
- Table rows sliding in with staggered cascade (each row 0.12s after last)
- Tab switching animation mid-scene
- Total/counter numbers counting up from 0
- Gentle scroll movement (translateY over time)

**Comparison/Analytics screens:**
- Stats counting up from 0 to final values
- Alert/change cards cascading in one by one
- Scroll to reveal more content

### Audio

- Background music: Use Mixkit CDN track or user-provided MP3, volume 0.8
- Whoosh transitions: Generate with ffmpeg, volume 0.1, on each scene change
- Whoosh command: `ffmpeg -y -f lavfi -i "anoisesrc=d=0.5:c=white:a=1.0" -filter_complex "highpass=f=1000,lowpass=f=6000,afade=t=in:d=0.05,afade=t=out:st=0.15:d=0.35,volume=3.0" -ar 44100 -b:a 128k whoosh.mp3`

---

## Execution Flow

### Step 1: Gather Input
If the user provides a product URL or codebase path, analyze it to extract:
- Product name and tagline from landing page/README
- Color palette from CSS/design tokens
- Feature list from marketing copy or component structure
- Screenshots by running the app or capturing from Stitch/design files

### Step 2: Generate Theme File
Create `theme.ts` with all design tokens extracted from the product's actual design system. Document where each value came from.

### Step 3: Generate Screen Components
Create animated screen content components that match the product's actual UI. Use the product's real colors, fonts, and data patterns.

### Step 4: Generate Scene Files
Create all 7 scene files following the architecture above. Each scene is a separate `.tsx` file.

### Step 5: Generate Composition Index
Create `index.tsx` that sequences all scenes with proper timing and audio.

### Step 6: Register & Render
- Add `<Composition>` to `Root.tsx` for both portrait (1080x1920) and landscape (1920x1080)
- Type-check with `npx tsc --noEmit`
- Render portrait: `npx remotion render src/index.ts {Id} out/{name}-portrait.mp4`
- Render landscape: `npx remotion render src/index.ts {Id}Landscape out/{name}-landscape.mp4`
- Open both for review

### Step 7: Iterate
The user will likely want adjustments. Common requests and how to handle them:

| Request | Action |
|---------|--------|
| "Text too small" | Bump all font sizes 30-40% |
| "Too much dead space" | Reduce padding from 36px to 28px, tighten margins |
| "Too slow" | Compress all sequence timings by 15%, tighten spring delays |
| "Phone too small" | Increase PhoneMockup width/height and scale prop |
| "Can't read the cards" | Increase card width, icon size, font sizes |
| "Feels static" | Add more animated elements inside phone screens |
| "Needs music" | Download from Mixkit CDN or generate ambient with ffmpeg |

---

## File Template Reference

### Composition Index Pattern
```tsx
import { AbsoluteFill, Html5Audio, Sequence, staticFile, useVideoConfig } from "remotion";
// ... scene imports

export const ProductDemo: React.FC = () => {
  const { fps } = useVideoConfig();
  const transitions = [/* scene start times */];
  return (
    <AbsoluteFill style={{ backgroundColor: PRIMARY_DARK }}>
      <Html5Audio src={staticFile("product/bg-music.mp3")} volume={0.8} startFrom={0} />
      {transitions.map((t) => (
        <Sequence key={t} from={Math.round(t * fps)} durationInFrames={Math.round(0.5 * fps)}>
          <Html5Audio src={staticFile("product/whoosh.mp3")} volume={0.1} />
        </Sequence>
      ))}
      {/* Scenes with overlapping sequences */}
    </AbsoluteFill>
  );
};
```

### Color Wipe Transition Pattern
```tsx
export const ColorWipe: React.FC<{
  fromColor: string; toColor: string; direction?: "left"|"right"|"up"|"down";
  children: React.ReactNode;
}> = ({ fromColor, toColor, direction = "right", children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const wipe = interpolate(frame, [0, Math.round(0.6 * fps)], [0, 100],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const clips = {
    right: `inset(0 ${100-wipe}% 0 0)`, left: `inset(0 0 0 ${100-wipe}%)`,
    up: `inset(${100-wipe}% 0 0 0)`, down: `inset(0 0 ${100-wipe}% 0)`,
  };
  return (
    <AbsoluteFill style={{ backgroundColor: fromColor }}>
      <AbsoluteFill style={{ backgroundColor: toColor, clipPath: clips[direction] }} />
      {children}
    </AbsoluteFill>
  );
};
```

### Phone Mockup Pattern
```tsx
export const PhoneMockup: React.FC<{
  children: React.ReactNode; tiltY?: number; tiltX?: number; scale?: number;
}> = ({ children, tiltY = 0, tiltX = 0, scale = 1 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const floatY = Math.sin(frame / (1.5 * fps)) * 4;
  return (
    <div style={{
      width: 380, height: 780, borderRadius: 50, border: "6px solid #222",
      overflow: "hidden", position: "relative",
      boxShadow: "0 40px 80px rgba(0,0,0,0.25)",
      transform: `perspective(1200px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale(${scale}) translateY(${floatY}px)`,
    }}>
      {/* Dynamic Island notch */}
      <div style={{ position: "absolute", top: 10, left: "50%", transform: "translateX(-50%)",
        width: 100, height: 28, backgroundColor: "#000", borderRadius: 18, zIndex: 10 }} />
      <div style={{ width: "100%", height: "100%", overflow: "hidden" }}>{children}</div>
    </div>
  );
};
```

### Split Layout Scene Pattern (phone left, text right)
```tsx
<AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
  <div style={{ display: "flex", alignItems: "center", gap: 24, padding: "0 28px" }}>
    <div style={{ /* phone entry animation */ }}>
      <PhoneMockup tiltY={5} tiltX={-2}>
        <AnimatedScreen />
      </PhoneMockup>
    </div>
    <div style={{ flex: 1 }}>
      {/* Headline 68-72px */}
      {/* Subtitle 24-26px */}
      {/* Feature cards or alert badges */}
    </div>
  </div>
</AbsoluteFill>
```

---

## Example Usage

User: "Create a demo video for my app called FoodTracker - it helps people log meals with photos. Primary color is orange #F97316, it's a health/fitness app."

The skill would:
1. Ask for 3 key features and any screenshots
2. Generate the full 7-scene composition with orange theme
3. Create animated phone screens showing meal logging, nutrition dashboard, progress charts
4. Render both orientations with upbeat music
5. Open for review

Total time: ~5 minutes from prompt to rendered video, vs the ~2 hours of iteration we did manually.
