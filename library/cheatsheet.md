# Manim Cheatsheet

## Import
from manim import *  # ALWAYS use this — never manimlib

## Scene Structure
class MyScene(Scene):
    def construct(self):
        # All animation logic here
        pass

## Common Mobjects
- Text("hello", font_size=26)                                     # Pango text (no LaTeX needed)
- Text("title", font_size=44, weight=BOLD)                        # Bold title
- MathTex(r"a^2 + b^2 = c^2")                                    # LaTeX math
- Tex(r"Hello \textbf{World}")                                    # LaTeX text
- RoundedRectangle(corner_radius=0.15, width=3, height=1.5)      # Rounded container (preferred)
- Circle(), Square(), Triangle()                                   # Shapes (Square for data cells only)
- Arrow(start, end, tip_length=0.15)                              # Arrow (thin tip)
- Line(start, end)                                                 # Line
- Dot(point)                                                       # Point
- VGroup(obj1, obj2, ...)                                         # Group of objects
- NumberLine(x_range=[0, 10])                                      # Number line
- Axes(x_range=[-3,3], y_range=[-1,5])                            # Coordinate axes
- Code(code="...", language="python", background="rectangle")      # Code block

## Positioning
- obj.to_edge(UP / DOWN / LEFT / RIGHT)
- obj.to_corner(UL / UR / DL / DR)
- obj.next_to(other, RIGHT, buff=0.5)
- obj.move_to(ORIGIN)
- obj.shift(2 * RIGHT + 1 * UP)
- Constants: UP, DOWN, LEFT, RIGHT, ORIGIN, UL, UR, DL, DR

## Key Animations
- self.play(Create(obj))                              # Draw object
- self.play(Write(text))                               # Write text
- self.play(FadeIn(obj, shift=UP * 0.3))               # Rise entrance (manimate signature)
- self.play(FadeOut(obj, shift=DOWN * 0.2))            # Sink exit (manimate signature)
- self.play(GrowFromCenter(line))                      # Grow line from center
- self.play(GrowArrow(arrow))                          # Grow arrow
- self.play(Transform(a, b))                           # Morph a into b (a is modified)
- self.play(ReplacementTransform(a, b))                # Replace a with b
- self.play(TransformMatchingTex(eq1, eq2))            # Morph matching LaTeX parts
- self.play(obj.animate.shift(RIGHT))                  # Animate property change
- self.play(obj.animate.set_color(PRIMARY))            # Animate color change
- self.wait(2)                                          # Pause 2 seconds

## Animation Modifiers
- self.play(Create(obj), run_time=0.6)                               # Duration (keep snappy)
- self.play(obj.animate.shift(RIGHT), rate_func=linear)              # Easing
- self.play(AnimationGroup(a1, a2, lag_ratio=0.12))                  # Staggered cascade
- self.play(AnimationGroup(*[FadeIn(i, shift=UP*0.3) for i in group], lag_ratio=0.12))  # Rise cascade

## Quality Flags (CLI)
- -ql  →  854x480  @ 15fps
- -qm  →  1280x720 @ 30fps (default for this skill)
- -qh  →  1920x1080 @ 60fps
- -qk  →  3840x2160 @ 60fps

## Manimate Color Tokens (use these, NOT raw Manim colors)
Dark "Creative Chaos" (default):
  BG="#2a2a3a"  SURFACE="#3a3a4a"  BORDER="#4a4a5a"
  PRIMARY="#ff3366"  ACCENT="#33ccff"  HIGHLIGHT="#ffcc00"  SUCCESS="#66ff66"  NEGATIVE="#ff4444"
  TEXT_CLR="#ffffff"  TEXT_DIM="#6a6a8a"

Light "Daylight Chaos":
  BG="#ffffff"  SURFACE="#f5f5f5"  BORDER="#e0e0e5"
  PRIMARY="#cc2952"  ACCENT="#0099cc"  HIGHLIGHT="#cc9900"  SUCCESS="#339933"  NEGATIVE="#cc0000"
  TEXT_CLR="#2a2a3a"  TEXT_DIM="#6a6a8a"

## Raw Manim Colors (avoid in manimate scenes — use tokens above)
PRIMARY:   BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, TEAL, PINK
SHADES:    RED_A (lightest) → RED_E (darkest), same for all colors
NEUTRAL:   WHITE, BLACK, GREY, GREY_A → GREY_E
SPECIAL:   GOLD, MAROON, DARK_BROWN, LIGHT_BROWN

## SVG Icons (custom visuals — KEY differentiator)
For real-world concepts (servers, databases, users, locks, etc.), generate custom SVGs instead of using basic shapes. This is what makes manimate videos look professional.

### The Pipeline: string → tempfile → SVGMobject
```python
import tempfile, os

def svg_icon(svg_string, scale=1.0):
    """Write inline SVG to temp file and load as SVGMobject."""
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, "icon.svg")
    with open(path, "w") as f:
        f.write(svg_string)
    return SVGMobject(path).scale(scale)

# Define SVG as a string constant, then load it
SVG_SERVER = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100">
  <rect x="5" y="5" width="70" height="25" rx="5" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <rect x="5" y="38" width="70" height="25" rx="5" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <rect x="5" y="71" width="70" height="25" rx="5" fill="#ff3366" stroke="#ffffff" stroke-width="2"/>
  <circle cx="18" cy="17" r="4" fill="#33ccff"/>
  <circle cx="18" cy="50" r="4" fill="#33ccff"/>
  <circle cx="18" cy="83" r="4" fill="#ffcc00"/>
</svg>'''

server = svg_icon(SVG_SERVER, scale=0.8)
```

### SVG Rules
- DO: `<path>`, `<rect>`, `<circle>`, `<ellipse>`, fill w/ hex colors, `stroke`, `viewBox`
- NO: gradients, `<text>`, filters, `stroke-dasharray`, `<image>`, `<clipPath>`, CSS `<style>`
- Use manimate palette colors (PRIMARY, ACCENT, etc.) as hex values in SVG fills/strokes

### Animating SVGs
```python
# All standard animations work on SVGMobjects
self.play(FadeIn(icon, shift=UP * 0.3))              # Rise entrance
self.play(icon.animate.shift(RIGHT * 2))              # Move
self.play(icon.animate.scale(1.3))                    # Scale
self.play(Indicate(icon, color=HIGHLIGHT))             # Emphasis
self.play(ReplacementTransform(lock, unlock))          # Morph between SVGs

# Color individual submobjects (each top-level SVG element = 1 submobject)
icon.submobjects[0].set_fill(PRIMARY)                 # Recolor first element
```

### Hybrid Layouts: SVG + Native Shapes
```python
# SVG icons alongside Manim arrows and text
user = svg_icon(SVG_USER, scale=0.8).move_to(LEFT * 3)
server = svg_icon(SVG_SERVER, scale=0.8).move_to(RIGHT * 3)
arrow = Arrow(user.get_right(), server.get_left(), color=BORDER, buff=0.3)
label = Text("request", font_size=20, color=TEXT_DIM).next_to(arrow, UP, buff=0.15)
```

See `library/svg-icons.md` for the full icon catalog with 20+ ready-to-adapt templates.
