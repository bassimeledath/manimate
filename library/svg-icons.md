# SVG Icons Reference

Generate custom SVG icons per-concept instead of using basic shapes. This makes manimate videos look professional and distinctive — it's manimate's key visual differentiator.

## Helper Function (include in every scene that uses SVG icons)

```python
import tempfile, os

def svg_icon(svg_string, scale=1.0):
    """Write inline SVG to temp file and load as SVGMobject."""
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, "icon.svg")
    with open(path, "w") as f:
        f.write(svg_string)
    return SVGMobject(path).scale(scale)
```

## SVG Design Rules

### DO:
- `<path d="...">` for complex shapes (bezier curves, arcs)
- `<rect>`, `<circle>`, `<ellipse>`, `<line>` for simple shapes
- `fill` with hex colors from the manimate palette
- `stroke` + `stroke-width` for outlines (white `#ffffff` outlines = clean look)
- `opacity` attribute on elements
- `viewBox` for proper scaling (use `0 0 80 100` or `0 0 64 64`)
- `fill-rule="evenodd"` for cutout/donut shapes
- `rx`/`ry` for rounded rect corners
- `stroke-linecap="round"` + `stroke-linejoin="round"` for smooth line ends

### DON'T:
- NO `<linearGradient>` / `<radialGradient>` — renders as black
- NO `<filter>` / `<feGaussianBlur>` — ignored
- NO `<text>` — stripped (use Manim `Text()` for labels)
- NO `<image>` — unsupported
- NO `stroke-dasharray` — renders as solid
- NO `<clipPath>` / `<mask>` — unsupported
- NO CSS `<style>` blocks — use inline attributes

## When to Use SVG vs Native Shapes

Use SVG: server, database, cloud, user/person, lock/key, shield, document, file, rocket, checkmark, X/denied, warning, brain/AI, gear/settings, globe, phone, laptop, envelope/email, webhook, API badge
Use native: array cells (Square), flowchart boxes (RoundedRectangle), graphs (Axes+plot), code (Code), bullets (Dot), containers (SurroundingRectangle), math (MathTex)

**Rule of thumb**: If a human would draw a recognizable icon for the concept, use SVG. If it's abstract or structural, use native shapes.

## Animation Patterns

```python
# Load and display with rise entrance
icon = svg_icon(SVG_STRING, scale=0.8)
self.play(FadeIn(icon, shift=UP * 0.3), run_time=0.6)

# Move/transform
self.play(icon.animate.shift(RIGHT * 2), run_time=1)
self.play(icon.animate.scale(1.3), run_time=0.8)

# Morph between SVGs (same structure, different details)
self.play(ReplacementTransform(svg_a, svg_b), run_time=1.5)

# Data flow: move small icon between two large icons
data = svg_icon(SVG_KEY, scale=0.4).move_to(source.get_right())
self.play(FadeIn(data), run_time=0.3)
self.play(data.animate.move_to(target.get_left()), run_time=1.5, rate_func=smooth)
self.play(FadeOut(data), run_time=0.3)

# Hybrid: SVG icons + native Manim arrows
arrow = Arrow(icon_a.get_right(), icon_b.get_left(), color=BORDER, buff=0.2, tip_length=0.15)
self.play(GrowArrow(arrow), run_time=0.6)

# Color individual submobjects (each top-level SVG element = 1 submobject)
icon.submobjects[0].set_fill("#ff3366")
```

---

## Icon Catalog

All icons use the Creative Chaos palette. Adapt colors to your scene's `shared_style`:
- PRIMARY = `#ff3366` (Hot Pink) — main concepts
- ACCENT = `#33ccff` (Cyan) — secondary, cool elements
- HIGHLIGHT = `#ffcc00` (Yellow) — emphasis, focus
- SUCCESS = `#66ff66` (Green) — success, correct
- NEGATIVE = `#ff4444` (Red) — errors, denied
- SURFACE = `#3a3a4a` — dark fills
- TEXT_CLR = `#ffffff` — light details

Workers should adapt these SVGs per-scene — change colors, sizes, and details to match the concept. These are **templates**, not exact copy-paste.

### 1. User / Person
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100">
  <circle cx="40" cy="28" r="20" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <path d="M10 85 C10 60 25 50 40 50 C55 50 70 60 70 85" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <circle cx="34" cy="24" r="3" fill="#2a2a3a"/>
  <circle cx="46" cy="24" r="3" fill="#2a2a3a"/>
  <path d="M34 34 Q40 40 46 34" fill="none" stroke="#2a2a3a" stroke-width="2"/>
</svg>
```

### 2. Server / Rack
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100">
  <rect x="5" y="5" width="70" height="25" rx="5" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <rect x="5" y="38" width="70" height="25" rx="5" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <rect x="5" y="71" width="70" height="25" rx="5" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <circle cx="18" cy="17" r="4" fill="#33ccff"/>
  <circle cx="18" cy="50" r="4" fill="#33ccff"/>
  <circle cx="18" cy="83" r="4" fill="#ffcc00"/>
</svg>
```

### 3. Database
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100">
  <ellipse cx="40" cy="20" rx="35" ry="15" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <rect x="5" y="20" width="70" height="60" fill="#ff3366"/>
  <line x1="5" y1="20" x2="5" y2="80" stroke="#ffffff" stroke-width="2"/>
  <line x1="75" y1="20" x2="75" y2="80" stroke="#ffffff" stroke-width="2"/>
  <ellipse cx="40" cy="50" rx="35" ry="10" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.4"/>
  <ellipse cx="40" cy="80" rx="35" ry="15" fill="#cc2952" stroke="#ffffff" stroke-width="2"/>
</svg>
```

### 4. Cloud
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80">
  <path d="M30 60 C10 60 0 50 0 40 C0 28 12 20 24 22 C26 12 36 5 48 5 C62 5 74 14 76 26 C90 24 105 34 105 48 C105 58 96 65 84 65 L30 65Z" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
</svg>
```

### 5. Lock (Locked)
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 80">
  <path d="M15 35 L15 25 C15 12 23 5 30 5 C37 5 45 12 45 25 L45 35" fill="none" stroke="#ffcc00" stroke-width="4"/>
  <rect x="8" y="35" width="44" height="35" rx="5" fill="#ffcc00" stroke="#ffffff" stroke-width="2"/>
  <circle cx="30" cy="50" r="5" fill="#2a2a3a"/>
</svg>
```

### 6. Unlock (morph target for Lock — use ReplacementTransform)
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 80">
  <path d="M15 35 L15 25 C15 12 23 5 30 5 C37 5 45 12 45 25 L45 15" fill="none" stroke="#33ccff" stroke-width="4"/>
  <rect x="8" y="35" width="44" height="35" rx="5" fill="#33ccff" stroke="#ffffff" stroke-width="2"/>
  <circle cx="30" cy="50" r="5" fill="#2a2a3a"/>
</svg>
```

### 7. Key / API Key
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60">
  <circle cx="25" cy="30" r="18" fill="#ffcc00" stroke="#ffffff" stroke-width="2"/>
  <circle cx="25" cy="30" r="8" fill="#2a2a3a"/>
  <rect x="40" y="26" width="50" height="8" rx="2" fill="#ffcc00" stroke="#ffffff" stroke-width="1.5"/>
  <rect x="72" y="26" width="8" height="16" rx="2" fill="#ffcc00" stroke="#ffffff" stroke-width="1.5"/>
  <rect x="82" y="26" width="8" height="12" rx="2" fill="#ffcc00" stroke="#ffffff" stroke-width="1.5"/>
</svg>
```

### 8. Shield / Security
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100">
  <path d="M40 5 L75 20 L75 55 C75 75 55 90 40 95 C25 90 5 75 5 55 L5 20Z" fill="#33ccff" stroke="#ffffff" stroke-width="2"/>
  <path d="M30 50 L38 58 L55 38" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### 9. Document / File
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100">
  <path d="M10 5 L55 5 L70 20 L70 95 L10 95Z" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <path d="M55 5 L55 20 L70 20" fill="none" stroke="#ffffff" stroke-width="2"/>
  <rect x="20" y="30" width="40" height="3" rx="1" fill="#ffffff" opacity="0.7"/>
  <rect x="20" y="38" width="35" height="3" rx="1" fill="#ffffff" opacity="0.5"/>
  <rect x="20" y="46" width="40" height="3" rx="1" fill="#ffffff" opacity="0.5"/>
  <rect x="20" y="54" width="28" height="3" rx="1" fill="#ffffff" opacity="0.4"/>
</svg>
```

### 10. Checkmark / Success
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="28" fill="#33ccff" stroke="#ffffff" stroke-width="2"/>
  <path d="M20 32 L28 40 L44 24" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### 11. Error / Denied
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="28" fill="#ff4444" stroke="#ffffff" stroke-width="2"/>
  <path d="M22 22 L42 42" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
  <path d="M42 22 L22 42" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
</svg>
```

### 12. Warning Triangle
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <path d="M32 6 L60 56 L4 56Z" fill="#ffcc00" stroke="#ffffff" stroke-width="2" stroke-linejoin="round"/>
  <rect x="30" y="24" width="4" height="18" rx="2" fill="#2a2a3a"/>
  <circle cx="32" cy="48" r="2.5" fill="#2a2a3a"/>
</svg>
```

### 13. Gear / Settings
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <path d="M28 4 L36 4 L38 12 L44 14 L50 8 L56 14 L50 20 L52 26 L60 28 L60 36 L52 38 L50 44 L56 50 L50 56 L44 50 L38 52 L36 60 L28 60 L26 52 L20 50 L14 56 L8 50 L14 44 L12 38 L4 36 L4 28 L12 26 L14 20 L8 14 L14 8 L20 14 L26 12Z" fill="#ff3366" stroke="#ffffff" stroke-width="1.5"/>
  <circle cx="32" cy="32" r="10" fill="#2a2a3a" stroke="#ffffff" stroke-width="1.5"/>
</svg>
```

### 14. Envelope / Email
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 70">
  <rect x="3" y="5" width="94" height="60" rx="5" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <path d="M3 10 L50 40 L97 10" fill="none" stroke="#ffffff" stroke-width="2"/>
</svg>
```

### 15. Globe / Web
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="28" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <ellipse cx="32" cy="32" rx="12" ry="28" fill="none" stroke="#ffffff" stroke-width="1.5"/>
  <line x1="4" y1="32" x2="60" y2="32" stroke="#ffffff" stroke-width="1.5"/>
  <path d="M8 20 Q32 16 56 20" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.6"/>
  <path d="M8 44 Q32 48 56 44" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.6"/>
</svg>
```

### 16. Mobile Phone
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 90">
  <rect x="5" y="3" width="40" height="84" rx="8" fill="#3a3a4a" stroke="#ffffff" stroke-width="2"/>
  <rect x="9" y="14" width="32" height="56" rx="2" fill="#ff3366" opacity="0.5"/>
  <circle cx="25" cy="78" r="4" fill="none" stroke="#ffffff" stroke-width="1.5"/>
</svg>
```

### 17. Laptop
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 70">
  <rect x="15" y="5" width="70" height="45" rx="4" fill="#3a3a4a" stroke="#ffffff" stroke-width="2"/>
  <rect x="20" y="10" width="60" height="35" fill="#ff3366" opacity="0.4"/>
  <path d="M5 55 L15 50 L85 50 L95 55 L95 60 Q95 65 90 65 L10 65 Q5 65 5 60Z" fill="#4a4a5a" stroke="#ffffff" stroke-width="1.5"/>
</svg>
```

### 18. Brain / AI
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80">
  <path d="M40 10 C25 10 15 22 15 35 C15 42 18 48 22 52 C20 56 18 62 20 68 C22 72 28 74 34 72 C36 76 40 78 44 76 C48 78 54 76 58 72 C62 74 68 72 68 66 C70 62 68 56 64 52 C68 48 70 42 70 35 C70 22 60 10 40 10Z" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <path d="M40 18 L40 65" stroke="#ffffff" stroke-width="1.5" opacity="0.5"/>
  <path d="M28 30 Q40 35 52 30" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.5"/>
  <path d="M25 45 Q40 50 55 45" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.5"/>
</svg>
```

### 19. Rocket / Launch
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <path d="M32 4 C28 12 20 24 20 40 L32 48 L44 40 C44 24 36 12 32 4Z" fill="#ffffff" stroke="#ffffff" stroke-width="1.5"/>
  <circle cx="32" cy="28" r="5" fill="#ff3366"/>
  <path d="M20 40 L16 48 L24 44Z" fill="#ffcc00"/>
  <path d="M44 40 L48 48 L40 44Z" fill="#ffcc00"/>
  <path d="M28 48 L32 56 L36 48Z" fill="#ff4444"/>
</svg>
```

### 20. Token / Badge
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 40">
  <rect x="2" y="2" width="96" height="36" rx="18" fill="#3a3a4a" stroke="#ff3366" stroke-width="2"/>
  <circle cx="20" cy="20" r="10" fill="#ff3366"/>
  <rect x="36" y="14" width="20" height="4" rx="2" fill="#ffffff" opacity="0.6"/>
  <rect x="36" y="22" width="30" height="4" rx="2" fill="#ffffff" opacity="0.4"/>
</svg>
```

### 21. Webhook / Arrow-Flow
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 60">
  <circle cx="15" cy="30" r="12" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <path d="M30 30 L55 30" stroke="#33ccff" stroke-width="3" stroke-linecap="round"/>
  <path d="M50 22 L58 30 L50 38" fill="none" stroke="#33ccff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="68" cy="30" r="8" fill="#33ccff" stroke="#ffffff" stroke-width="1.5"/>
</svg>
```

### 22. Folder
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 70">
  <path d="M5 15 L5 60 Q5 65 10 65 L80 65 Q85 65 85 60 L85 25 Q85 20 80 20 L40 20 L35 12 Q33 10 30 10 L10 10 Q5 10 5 15Z" fill="#ffcc00" stroke="#ffffff" stroke-width="2"/>
  <rect x="5" y="25" width="80" height="40" rx="5" fill="#ffcc00" stroke="#ffffff" stroke-width="2"/>
</svg>
```

### 23. Clock / Timer
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="28" fill="#3a3a4a" stroke="#ff3366" stroke-width="2.5"/>
  <line x1="32" y1="32" x2="32" y2="16" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="32" y1="32" x2="44" y2="38" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
  <circle cx="32" cy="32" r="3" fill="#ff3366"/>
</svg>
```

### 24. Lightning / Fast
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 80">
  <path d="M30 2 L10 38 L22 38 L18 78 L42 32 L28 32Z" fill="#ffcc00" stroke="#ffffff" stroke-width="2" stroke-linejoin="round"/>
</svg>
```

---

## Complete Scene Example

```python
from manim import *
import tempfile, os

# ── Creative Chaos Dark ──
BG        = "#2a2a3a"
SURFACE   = "#3a3a4a"
BORDER    = "#4a4a5a"
PRIMARY   = "#ff3366"
ACCENT    = "#33ccff"
HIGHLIGHT = "#ffcc00"
NEGATIVE  = "#ff4444"
TEXT_CLR  = "#ffffff"
TEXT_DIM  = "#6a6a8a"

def svg_icon(svg_string, scale=1.0):
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, "icon.svg")
    with open(path, "w") as f:
        f.write(svg_string)
    return SVGMobject(path).scale(scale)

SVG_USER = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100">
  <circle cx="40" cy="28" r="20" fill="#ff3366" stroke="#fff" stroke-width="2"/>
  <path d="M10 85 C10 60 25 50 40 50 C55 50 70 60 70 85" fill="#ff3366" stroke="#fff" stroke-width="2"/>
</svg>'''

SVG_SERVER = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100">
  <rect x="5" y="5" width="70" height="25" rx="5" fill="#ff3366" stroke="#fff" stroke-width="2"/>
  <rect x="5" y="38" width="70" height="25" rx="5" fill="#ff3366" stroke="#fff" stroke-width="2"/>
  <rect x="5" y="71" width="70" height="25" rx="5" fill="#ff3366" stroke="#fff" stroke-width="2"/>
  <circle cx="18" cy="17" r="4" fill="#33ccff"/>
  <circle cx="18" cy="50" r="4" fill="#33ccff"/>
  <circle cx="18" cy="83" r="4" fill="#ffcc00"/>
</svg>'''

SVG_KEY = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60">
  <circle cx="25" cy="30" r="18" fill="#ffcc00" stroke="#fff" stroke-width="2"/>
  <circle cx="25" cy="30" r="8" fill="#2a2a3a"/>
  <rect x="40" y="26" width="50" height="8" rx="2" fill="#ffcc00" stroke="#fff" stroke-width="1.5"/>
</svg>'''


class APIAuthFlow(Scene):
    def construct(self):
        self.camera.background_color = BG

        user = svg_icon(SVG_USER, scale=0.8).move_to(LEFT * 4)
        server = svg_icon(SVG_SERVER, scale=0.8).move_to(RIGHT * 4)

        self.play(FadeIn(user, shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(server, shift=UP * 0.3), run_time=0.6)

        # Arrow between them
        arrow = Arrow(user.get_right(), server.get_left(),
                      color=BORDER, buff=0.3, tip_length=0.15)
        self.play(GrowArrow(arrow), run_time=0.6)

        # Animate a key traveling from user to server
        key = svg_icon(SVG_KEY, scale=0.4)
        key.move_to(user.get_right() + RIGHT * 0.3)
        self.play(FadeIn(key), run_time=0.3)
        self.play(key.animate.move_to(server.get_left() + LEFT * 0.3),
                  run_time=1.5, rate_func=smooth)
        self.play(FadeOut(key), run_time=0.3)
        self.wait(1)
```
