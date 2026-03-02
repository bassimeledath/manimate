# Manimate Style Guide — Creative Chaos

> Every manimate video should feel *alive* — bouncy, colorful, and unmistakably playful.
> This is not generic Manim output. This is Creative Chaos: playful rainbow energy inspired by The Coding Train.

---

## Quick Reference — Dark Mode "Creative Chaos" (default)

```python
# ── Creative Chaos Dark ──────────────────────────────
BG        = "#2a2a3a"   # Canvas — soft dark purple-gray
SURFACE   = "#3a3a4a"   # Elevated containers, cards
BORDER    = "#4a4a5a"   # Subtle borders, structural lines
PRIMARY   = "#ff3366"   # Hot Pink — THE manimate color
ACCENT    = "#33ccff"   # Cyan — secondary concepts, cool complement
HIGHLIGHT = "#ffcc00"   # Yellow — emphasis, focus, "look here"
SUCCESS   = "#66ff66"   # Green — success, correct, positive
NEGATIVE  = "#ff4444"   # Red — errors, wrong, removed
TEXT_CLR  = "#ffffff"   # White text
TEXT_DIM  = "#8a8aaa"   # Muted text, labels, secondary info
# ───────────────────────────────────────────────────────
```

## Quick Reference — Light Mode "Daylight Chaos"

```python
# ── Creative Chaos Light ─────────────────────────────
BG        = "#ffffff"   # Canvas — white
SURFACE   = "#f5f5f5"   # Light gray containers
BORDER    = "#e0e0e5"   # Soft gray borders
PRIMARY   = "#cc2952"   # Deeper Pink — darkened for contrast
ACCENT    = "#0099cc"   # Deep Cyan — darkened for readability
HIGHLIGHT = "#cc9900"   # Amber — darkened yellow
SUCCESS   = "#339933"   # Deep Green
NEGATIVE  = "#cc0000"   # Crimson
TEXT_CLR  = "#2a2a3a"   # Dark text
TEXT_DIM  = "#8a8aaa"   # Muted gray
# ───────────────────────────────────────────────────────
```

---

## The Five Signatures

These are what make a video *manimate*. Every scene should incorporate at least signatures 1, 3, and 4.

### 1. The Rainbow
The Pink + Cyan + Yellow + Green palette. Bold, saturated, playful — like a Coding Train project. Not muted pastels. Not corporate blues.

**Rule**: Maximum 3 accent colors visible at any time. PRIMARY (pink) is always dominant.

### 2. The Grid
A barely-visible dot grid on the background. Adds texture and structure without competing with content. Makes the canvas feel alive.

```python
# Add at the start of construct(), before any content
dots = VGroup(*[
    Dot([x, y, 0], radius=0.02, fill_opacity=0.08, color=TEXT_CLR)
    for x in range(-7, 8) for y in range(-4, 5)
])
self.add(dots)
```

### 3. The Bounce
Elements enter by bouncing into view — never a flat FadeIn. This upward bounce creates playful energy.

```python
# Standard entrance — bouncy rise
self.play(FadeIn(element, shift=UP * 0.4), run_time=0.5)

# For groups — stagger the bounce with lag_ratio
self.play(
    AnimationGroup(*[
        FadeIn(item, shift=UP * 0.4) for item in group
    ], lag_ratio=0.15),
    run_time=0.7,
)
```

### 4. The Roundness
Every rectangle uses rounded corners. No sharp boxes. This single detail separates manimate from default Manim instantly.

```python
# ALWAYS use RoundedRectangle, never Rectangle or Square for containers
box = RoundedRectangle(
    corner_radius=0.15, width=3, height=1.5,
    fill_color=SURFACE, fill_opacity=1,
    stroke_color=BORDER, stroke_width=1.5,
)
```

**Note**: Use `Square` only for data cells (arrays, grids) where sharp alignment matters. For everything else — containers, cards, highlights — use `RoundedRectangle`.

### 5. The Pop
Key elements get a quick scale pop for emphasis. Clean and 2D — no gradients, no blur.

```python
# Pop emphasis: quick scale up then settle back
self.play(element.animate.scale(1.15), run_time=0.2)
self.play(element.animate.scale(1.0), run_time=0.3)

# Or with a colored stroke flash
flash = element.copy().set_stroke(
    color=PRIMARY, width=6, opacity=0.4
).set_fill(opacity=0)
self.play(FadeIn(flash, scale=0.95), run_time=0.2)
self.play(FadeOut(flash, scale=1.1), run_time=0.4)
self.remove(flash)
```

---

## Typography

### Fonts
| Role | Font | Usage |
|------|------|-------|
| Headings | `font="Galvji"` | Titles, scene headers, bold text |
| Body | `font="Avenir Next"` | Primary content, descriptions, labels |
| Code | `font="Monaco"` | Code snippets, technical text, monospace |

```python
# Heading
title = Text("Scene Title", font="Galvji", font_size=44, color=TEXT_CLR, weight=BOLD)

# Body text
body = Text("This explains the concept", font="Avenir Next", font_size=26, color=TEXT_CLR)

# Code/technical
code_text = Text("def hello():", font="Monaco", font_size=22, color=ACCENT)
```

### Sizes
| Role | Size | Usage |
|------|------|-------|
| Display | 44 | Scene title on title card |
| Heading | 32 | Section headers, persistent title |
| Body | 26 | Primary content text |
| Label | 20 | Annotations, descriptions, axis labels |
| Caption | 16 | Section tags, fine print |

### Weight
- **Titles**: `weight=BOLD` — always
- **Body text**: default weight (regular)
- **Labels**: default weight

### Title Treatment — The Signature
Titles get a thin PRIMARY-colored underline that grows from center. This is the manimate look.

```python
# Title with signature underline
title = Text("Scene Title", font="Galvji", font_size=44, color=TEXT_CLR, weight=BOLD)
underline = Line(
    title.get_left() + DOWN * 0.35,
    title.get_right() + DOWN * 0.35,
    color=PRIMARY, stroke_width=2.5,
)

# Bounce + underline entrance
self.play(
    FadeIn(title, shift=UP * 0.4),
    GrowFromCenter(underline),
    run_time=0.7,
)
self.wait(1.5)

# Transition title to corner — LEFT aligned, not centered
self.play(
    title.animate.scale(0.55).to_corner(UL, buff=0.5),
    FadeOut(underline, run_time=0.3),
    run_time=0.5,
)
```

### Reusable Title Card Helper

Copy this function into any scene to get the standard title card pattern — bounce in, display, move to corner. This ensures consistent underline positioning.

```python
def title_card(scene, text, wait=1.5):
    """Show title with signature underline, then move to corner.

    Args:
        scene: the Scene instance (pass `self` from construct)
        text: the title string
        wait: seconds to display before moving to corner (default 1.5)
    Returns:
        title Mobject (now in the UL corner at scale 0.55)
    """
    title = Text(text, font="Galvji", font_size=44, color=TEXT_CLR, weight=BOLD)
    underline = Line(
        title.get_left() + DOWN * 0.35,
        title.get_right() + DOWN * 0.35,
        color=PRIMARY, stroke_width=2.5,
    )
    scene.play(
        FadeIn(title, shift=UP * 0.4),
        GrowFromCenter(underline),
        run_time=0.7,
    )
    scene.wait(wait)
    scene.play(
        title.animate.scale(0.55).to_corner(UL, buff=0.5),
        FadeOut(underline, run_time=0.3),
        run_time=0.5,
    )
    return title
```

Usage in a scene:
```python
class MyScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        # ... dot grid setup ...
        title = title_card(self, "My Scene Title")
        # title is now in the UL corner — continue with main content
```

---

## Layout

### Spacing Scale
| Token | Value | Usage |
|-------|-------|-------|
| xs | 0.15 | Within tight groups (label to object) |
| sm | 0.3 | Between related items |
| md | 0.5 | Between content sections |
| lg | 0.8 | Major separations, title to content |
| xl | 1.2 | Section breaks |

### Safe Area
- Frame: ~14.2 x 8 units
- **Minimum edge margin**: 0.8 units on all sides
- **Content area**: ~12.6 x 6.4 units
- Never place content within 0.8 units of the frame edge

### Positioning
- **Title card**: centered at `ORIGIN`, then moves to `UL` corner
- **Persistent title**: top-left at `to_corner(UL, buff=0.5)`, scale 0.55
- **Main content**: centered at `ORIGIN` or `DOWN * 0.3` (slightly below center)
- **Side-by-side**: `shift(2.5 * LEFT)` and `shift(2.5 * RIGHT)` — wider than default
- **Labels**: `next_to(referent, DOWN, buff=0.3)` — below, not beside
- **Section tag**: small PRIMARY-colored text at `UL` above the title — `font_size=16, weight=BOLD`

### Layout Best Practices — Preventing Overlaps

Default to **relative positioning** for spatially-related elements:

```python
# Label below icon — not absolute coords
label.next_to(icon, DOWN, buff=0.3)

# Row of items — not individual move_to calls
VGroup(a, b, c).arrange(RIGHT, buff=0.8)

# Grid layout — not manual coordinate math
items.arrange_in_grid(rows=2, cols=3, buff=0.8)
```

**Absolute coords for anchor points only** — placing independent groups at their starting position:

```python
# Place a group at a known anchor point
left_panel.move_to(LEFT * 3)
right_panel.move_to(RIGHT * 3)

# Then connect with relative positioning
arrow = Arrow(left_panel.get_right(), right_panel.get_left(),
              color=BORDER, stroke_width=1.5, tip_length=0.15, buff=0.1)
```

**Group before position** — build `VGroup` of related elements, arrange internally, then position the group as a unit:

```python
# GOOD: group → arrange → position
node_label = Text("API", font="Avenir Next", font_size=20, color=TEXT_CLR)
node_box = RoundedRectangle(corner_radius=0.15, width=2.2, height=0.8,
                            fill_color=SURFACE, fill_opacity=1,
                            stroke_color=PRIMARY, stroke_width=1.5)
node_label.move_to(node_box)
node = VGroup(node_box, node_label)

# Position the GROUP, not individual pieces
node.move_to(LEFT * 2 + DOWN * 0.5)

# BAD: positioning pieces independently
# node_box.move_to(LEFT * 2 + DOWN * 0.5)
# node_label.move_to(LEFT * 2 + DOWN * 0.5)  # fragile, breaks on resize
```

---

## Motion

### Entrances — "Bounce"
Everything bounces in. This is non-negotiable.

```python
# Single element
self.play(FadeIn(element, shift=UP * 0.4), run_time=0.5)

# Group with cascade
self.play(
    AnimationGroup(*[
        FadeIn(item, shift=UP * 0.4) for item in group
    ], lag_ratio=0.15),
    run_time=0.7,
)

# Subtitle / secondary text (shorter bounce, faster)
self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.3)
```

### Exits — "Drop"
Elements exit by dropping downward. The inverse of the bounce.

```python
# Single element
self.play(FadeOut(element, shift=DOWN * 0.3), run_time=0.4)

# All content — scene transition
self.play(
    *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
    run_time=0.4,
)
```

### Emphasis — "Pop"
Don't use `Indicate()` — it's the generic Manim look. Use a scale pop instead.

```python
# Quick pop: scale up then back
self.play(element.animate.scale(1.15), run_time=0.2)
self.play(element.animate.scale(1.0), run_time=0.3)

# Stroke flash (for containers/boxes)
flash = element.copy().set_stroke(
    color=PRIMARY, width=6, opacity=0.4
).set_fill(opacity=0)
self.play(FadeIn(flash, scale=0.95), run_time=0.2)
self.play(FadeOut(flash, scale=1.1), run_time=0.4)
self.remove(flash)
```

### Transforms
Keep transforms **snappy**. Creative Chaos moves fast.

```python
# Equation morphs
self.play(TransformMatchingTex(eq1, eq2), run_time=0.6)

# Shape transforms
self.play(ReplacementTransform(old, new), run_time=0.5)
```

### Scene Transitions
Between major sections within a scene, use a clean drop-and-bounce:

```python
# Transition between sections
self.play(
    *[FadeOut(mob, shift=DOWN * 0.3) for mob in content_group],
    run_time=0.4,
)
self.wait(0.3)
# New content enters with bounce (standard entrance)
```

### Timing Guide
| Action | Duration | Notes |
|--------|----------|-------|
| Title entrance (bounce + underline) | 0.7s | Display for 1.5s before moving |
| Element entrance (bounce) | 0.5s | |
| Secondary entrance | 0.3s | Subtitles, labels |
| Group cascade | 0.7s total | lag_ratio=0.15 |
| Transform / morph | 0.5-0.6s | Snappier than default |
| Pop emphasis | 0.2s up + 0.3s settle | |
| Exit (drop) | 0.4s | Slightly faster than entrance |
| **Text reading pause** | **max(2, word_count / 3)s** | **ALWAYS pause after text appears** |
| Pause after key concept | 1.5-2.0s | Let it breathe |
| Key insights/annotations | 3.0s minimum | Must be fully readable |
| Pause between steps | 0.8-1.0s | Keep momentum |
| Transition between sections | 1.5s wait | Before new content enters |

**CRITICAL**: NEVER use `self.wait(0.5)` or `self.wait(1)` after text with more than 3 words. Always compute: `self.wait(max(2, word_count / 3))`. Viewers need time to read.

---

## Color Usage Rules

### Semantic Meaning
| Token | Dark Value | Light Value | When to Use |
|-------|-----------|-------------|-------------|
| PRIMARY | `#ff3366` | `#cc2952` | Main concepts, active elements, links, the dominant accent |
| ACCENT | `#33ccff` | `#0099cc` | Secondary concepts, complementary info, cool contrast |
| HIGHLIGHT | `#ffcc00` | `#cc9900` | THE most important element on screen, focus, emphasis, "look here" |
| SUCCESS | `#66ff66` | `#339933` | Correct answers, completed items, positive states |
| NEGATIVE | `#ff4444` | `#cc0000` | Errors, wrong answers, eliminated items, deletions |
| SURFACE | `#3a3a4a` | `#f5f5f5` | Container backgrounds, card fills |
| BORDER | `#4a4a5a` | `#e0e0e5` | Container strokes, structural arrows, dividing lines |
| TEXT_CLR | `#ffffff` | `#2a2a3a` | All readable text |
| TEXT_DIM | `#8a8aaa` | `#8a8aaa` | Annotations, axis labels, secondary text |

### Rules
1. **Max 3 accents at once**. If PRIMARY + ACCENT + HIGHLIGHT are all on screen, don't add SUCCESS or NEGATIVE. Remove or dim something first.
2. **PRIMARY is dominant**. It should be the most-used accent color in any scene.
3. **HIGHLIGHT is singular**. Only one element at a time should be highlighted. Move it as focus shifts.
4. **Text is never raw `WHITE` or `BLACK`**. Always use TEXT_CLR or TEXT_DIM.
5. **Containers use SURFACE fill + BORDER stroke**. Stroke width 1.5, fill_opacity 1 (dark) or 0.95 (light).
6. **Structural elements use BORDER color**. Arrows connecting nodes, divider lines, axis lines — all BORDER.
7. **MathTex defaults to TEXT_CLR**. Color individual parts with set_color() for emphasis.
8. **Body text is always TEXT_CLR**. TEXT_DIM is ONLY for font_size 16 or smaller (captions, axis labels, annotations). Any text font_size >= 20 must use TEXT_CLR. When in doubt, use TEXT_CLR.

---

## Container & Node Patterns

### Standard Container (card)
```python
card = RoundedRectangle(
    corner_radius=0.15, width=4, height=2,
    fill_color=SURFACE, fill_opacity=1,
    stroke_color=BORDER, stroke_width=1.5,
)
```

### Node in a Diagram
```python
def make_node(label, color=None, w=2.5, h=0.8):
    """Create a labeled rounded rectangle node. Box auto-sizes to fit text."""
    if color is None:
        color = PRIMARY
    text = Text(label, font="Avenir Next", font_size=22, color=TEXT_CLR)
    box_w = max(w, text.width + 0.6)
    box_h = max(h, text.height + 0.4)
    box = RoundedRectangle(
        corner_radius=0.15, width=box_w, height=box_h,
        fill_color=SURFACE, fill_opacity=1,
        stroke_color=color, stroke_width=1.5,
    )
    text.move_to(box)
    return VGroup(box, text)
```

### Data Cell (array element)
```python
# Sharp-cornered squares for data grids — the ONE exception to roundness
cell = Square(
    side_length=0.8,
    fill_color=SURFACE, fill_opacity=0.6,
    stroke_color=BORDER, stroke_width=1.5,
)
value = Text("42", font="Monaco", font_size=24, color=TEXT_CLR)
value.move_to(cell)
```

### Connecting Arrows
```python
arrow = Arrow(
    start.get_right(), end.get_left(),
    color=BORDER, stroke_width=1.5,
    tip_length=0.15, buff=0.1,
)
```

### Equation Card
```python
# Wrap equations in a surface card for depth
card = RoundedRectangle(
    corner_radius=0.15, width=8, height=2.5,
    fill_color=SURFACE, fill_opacity=0.8,
    stroke_color=BORDER, stroke_width=1,
)
eq = MathTex(r"e^{i\pi} + 1 = 0", font_size=48)
eq.set_color(TEXT_CLR)
eq.move_to(card)
```

### Highlighting an Active Element
```python
# Brighten the stroke to PRIMARY and pop
self.play(box.animate.set_stroke(color=PRIMARY, width=2.5), run_time=0.3)
self.play(box.animate.scale(1.05), run_time=0.2)
self.play(box.animate.scale(1.0), run_time=0.3)
```

### Progress Bar
```python
def progress_bar(width=8, height=0.4, fill_color=None):
    """Create a progress bar. Returns VGroup(track, fill) with fill at 0%.
    Animate with: self.play(set_progress(bar, 0.75), run_time=1.0)"""
    if fill_color is None:
        fill_color = PRIMARY
    pad = height * 0.12
    track = RoundedRectangle(
        corner_radius=height / 2, width=width, height=height,
        fill_color=SURFACE, fill_opacity=1,
        stroke_color=BORDER, stroke_width=1.5,
    )
    fill = RoundedRectangle(
        corner_radius=max(0.05, (height - 2 * pad) / 2),
        width=pad, height=height - 2 * pad,
        fill_color=fill_color, fill_opacity=1, stroke_width=0,
    )
    fill.align_to(track, LEFT).shift(RIGHT * pad)
    return VGroup(track, fill)


def set_progress(bar, pct):
    """Return .animate for bar fill to reach pct (0.0-1.0). Fill stays inside track."""
    track, fill = bar[0], bar[1]
    pad = track.height * 0.12
    target_w = max(pad, (track.width - 2 * pad) * max(0.0, min(1.0, pct)))
    return fill.animate.stretch_to_fit_width(target_w).align_to(
        track, LEFT
    ).shift(RIGHT * pad)
```

Usage: `self.play(set_progress(bar, 0.75), run_time=1.0)` — fill always stays inside the track because `set_progress()` re-aligns after every stretch.

**NEVER** animate a raw Rectangle's width for progress — it will overflow the track. Always use `progress_bar()` + `set_progress()`.

---

## Axes & Graphs

```python
axes = Axes(
    x_range=[0, 10, 1],
    y_range=[0, 100, 10],
    axis_config={
        "color": TEXT_DIM,          # Axes in muted color, not white
        "stroke_width": 1.5,        # Thinner than default
        "include_numbers": True,
    },
    x_length=8,
    y_length=5,
)
# Labels in TEXT_DIM
x_label = axes.get_x_axis_label("n", color=TEXT_DIM)
y_label = axes.get_y_axis_label("f(n)", color=TEXT_DIM)

# Plot curves in accent colors
curve1 = axes.plot(lambda x: x**2, color=PRIMARY)
curve2 = axes.plot(lambda x: 2*x, color=ACCENT)

# Graph labels
label1 = Text("O(n²)", font="Monaco", font_size=20, color=PRIMARY)
label1.next_to(curve1.get_end(), RIGHT, buff=0.2)
```

---

## Code Blocks

```python
code = Code(
    code="def search(arr, target):\n    lo, hi = 0, len(arr) - 1\n    ...",
    language="python",
    font_size=18,
    background="rectangle",           # Use rectangle for control
    background_stroke_color=BORDER,
    background_stroke_width=1,
    line_spacing=0.6,
)

# Highlight a line — use a rounded highlight, not the default SurroundingRectangle
highlight = RoundedRectangle(
    corner_radius=0.08,
    width=code.width - 0.2,
    height=0.35,
    fill_color=PRIMARY, fill_opacity=0.12,
    stroke_width=0,
)
highlight.move_to(code.code[1])  # highlight line 2
```

---

## Scene Structure Template

Every manimate scene follows this structure:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *


class SceneName(Scene):
    def construct(self):
        setup_scene(self)                          # BG + dot grid

        title = title_card(self, "Title Here")     # bounce in → corner

        # Main content (bounces in)
        # ... build content here using bounce entrances ...

        # Exit (drop out)
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )
```

---

## Complete Examples

> All examples use `from shared import *` — never inline palette constants.
> See `templates/basic.py` for the minimal starter template.

### Example A: Title Card with Subtitle

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *


class TitleCard(Scene):
    def construct(self):
        setup_scene(self)

        title = title_card(self, "Binary Search")

        # Subtitle (font_size 24 → TEXT_CLR, not TEXT_DIM)
        subtitle = Text(
            "Finding elements in sorted data, fast.",
            font="Avenir Next", font_size=24, color=TEXT_CLR,
        )
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.3)
        self.wait(tw("Finding elements in sorted data, fast."))

        self.play(FadeOut(subtitle, shift=DOWN * 0.3), run_time=0.4)
        self.wait(1)
```

### Example B: Diagram / Flowchart

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *


class DiagramExample(Scene):
    def construct(self):
        setup_scene(self)

        title = title_card(self, "Request Lifecycle")

        # Nodes (make_node from shared.py)
        client  = make_node("Client", color=BORDER)
        gateway = make_node("API Gateway", color=PRIMARY)
        service = make_node("Service", color=ACCENT)
        db      = make_node("Database", color=HIGHLIGHT)

        nodes = VGroup(client, gateway, service, db)
        nodes.arrange(RIGHT, buff=1.0).move_to(DOWN * 0.3)

        # Arrows
        arrows = VGroup()
        pairs = [(client, gateway), (gateway, service), (service, db)]
        for a, b in pairs:
            arrows.add(Arrow(
                a.get_right(), b.get_left(),
                color=BORDER, stroke_width=1.5,
                tip_length=0.15, buff=0.1,
            ))

        # Staggered entrance
        for i, node in enumerate(nodes):
            self.play(FadeIn(node, shift=UP * 0.4), run_time=0.4)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.3)
        self.wait(1)

        # Pop the service node
        self.play(service[0].animate.set_stroke(color=ACCENT, width=2.5), run_time=0.3)
        self.play(service.animate.scale(1.1), run_time=0.2)
        self.play(service.animate.scale(1.0), run_time=0.3)

        # Caption label (font_size 16 → TEXT_DIM is fine)
        label = Text(
            "processes the request",
            font="Avenir Next", font_size=16, color=TEXT_DIM,
        )
        label.next_to(service, DOWN, buff=0.4)
        self.play(FadeIn(label, shift=UP * 0.2), run_time=0.3)
        self.wait(2)

        # Exit
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )
```

### Example C: Equation Derivation

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *


class EquationExample(Scene):
    def construct(self):
        setup_scene(self)

        # Section tag (font_size 16 → TEXT_DIM-eligible, but tags use PRIMARY)
        tag = Text(
            "DERIVATION", font="Galvji", font_size=16,
            color=PRIMARY, weight=BOLD,
        )
        tag.to_corner(UL, buff=0.5)
        self.play(FadeIn(tag), run_time=0.3)

        # Title below the tag
        title = Text(
            "Euler's Identity", font="Galvji", font_size=40,
            color=TEXT_CLR, weight=BOLD,
        )
        title.next_to(tag, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.4)
        self.wait(1)

        # Equation card
        card = RoundedRectangle(
            corner_radius=0.15, width=8, height=2.5,
            fill_color=SURFACE, fill_opacity=0.8,
            stroke_color=BORDER, stroke_width=1,
        )
        card.move_to(DOWN * 0.5)

        eq = MathTex(r"e^{i\pi} + 1 = 0", font_size=48)
        eq.set_color(TEXT_CLR)
        eq.move_to(card)

        self.play(FadeIn(card, shift=UP * 0.4), run_time=0.4)
        self.play(Write(eq), run_time=1.0)
        self.wait(1)

        # Color individual parts for emphasis
        eq_colored = MathTex(
            r"e", r"^{i\pi}", r"+", r"1", r"=", r"0",
            font_size=48,
        )
        eq_colored[0].set_color(PRIMARY)      # e
        eq_colored[1].set_color(ACCENT)       # ipi
        eq_colored[2].set_color(BORDER)       # + (structural, not TEXT_DIM)
        eq_colored[3].set_color(HIGHLIGHT)    # 1
        eq_colored[4].set_color(BORDER)       # = (structural, not TEXT_DIM)
        eq_colored[5].set_color(HIGHLIGHT)    # 0
        eq_colored.move_to(card)

        self.play(TransformMatchingTex(eq, eq_colored), run_time=0.6)
        self.wait(0.5)

        # Annotation (font_size 20 → TEXT_CLR, not TEXT_DIM)
        desc = Text(
            "Five fundamental constants in one equation.",
            font="Avenir Next", font_size=20, color=TEXT_CLR,
        )
        desc.next_to(card, DOWN, buff=0.5)
        self.play(FadeIn(desc, shift=UP * 0.2), run_time=0.3)
        self.wait(tw("Five fundamental constants in one equation."))

        # Pop emphasis on the card
        self.play(card.animate.scale(1.03), run_time=0.2)
        self.play(card.animate.scale(1.0), run_time=0.3)
        self.wait(2)

        # Exit
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )
```

---

## SVG Icon Style Rules

SVG icons are manimate's visual differentiator. When a scene represents real-world concepts, use custom SVGs instead of basic shapes.

### Color Mapping
SVG fills and strokes must use the Creative Chaos palette hex values — never raw Manim color names:

| Palette Token | Hex Value | SVG Usage |
|---------------|-----------|-----------|
| PRIMARY | `#ff3366` | Main icon fills — servers, users, documents |
| ACCENT | `#33ccff` | Secondary icons, cool elements — shields, data |
| HIGHLIGHT | `#ffcc00` | Focus icons — keys, locks, warnings |
| SUCCESS | `#66ff66` | Success icons — checkmarks, shields |
| NEGATIVE | `#ff4444` | Error/denied icons |
| SURFACE | `#3a3a4a` | Dark inner fills — screen areas, keyholes |
| BG | `#2a2a3a` | Cut-out shapes, inner details |
| `#ffffff` | White | Outlines (stroke), inner details |

### Stroke Consistency
- Outer strokes: `stroke="#ffffff" stroke-width="2"` — matches the clean manimate look
- Detail strokes: `stroke-width="1.5"` for inner lines
- Line endings: `stroke-linecap="round" stroke-linejoin="round"` for smooth joints

### ViewBox Conventions
- Tall icons (person, server, document): `viewBox="0 0 80 100"`
- Square icons (checkmark, gear, warning): `viewBox="0 0 64 64"`
- Wide icons (key, token, laptop): `viewBox="0 0 100 60"` or similar
- Always center the content within the viewBox

### Sizing
- Main concept icons: `scale=0.8` to `scale=1.0`
- Small traveling objects (tokens, keys in data flow): `scale=0.3` to `scale=0.5`
- Large hero icons (single concept on screen): `scale=1.2` to `scale=1.5`

### Flat Design Only
- NO gradients — renders as black
- NO filters / blur — ignored by Manim
- NO text in SVG — use Manim `Text()` placed next to the icon
- NO dashed strokes — renders as solid
- Use `opacity` attribute for subtle layering (e.g., `opacity="0.5"` on background elements)

---

## Anti-Patterns — Do NOT

| Instead of... | Do this |
|---|---|
| `BLUE`, `YELLOW`, `GREEN`, `RED` (Manim defaults) | Use `PRIMARY`, `ACCENT`, `HIGHLIGHT`, `SUCCESS` |
| `FadeIn(element)` (flat entrance) | `FadeIn(element, shift=UP * 0.4)` (bounce) |
| `FadeOut(element)` (flat exit) | `FadeOut(element, shift=DOWN * 0.3)` (drop) |
| `Rectangle()` for containers | `RoundedRectangle(corner_radius=0.15, ...)` |
| `stroke_width=4` (thick default) | `stroke_width=1.5` (refined) |
| `WHITE` text color | `TEXT_CLR` (#ffffff) |
| `Indicate(obj)` for emphasis | Pop pattern (scale up + settle) |
| `background_color = "#1e1e2e"` | `background_color = BG` (use the token) |
| `font_size=48` for everything | Use the size scale: 44/32/26/20/16 |
| No `font` parameter | `font="Galvji"` for headings, `font="Avenir Next"` for body |
| Sharp-cornered `SurroundingRectangle` | `RoundedRectangle` positioned with `move_to` |
| 4+ accent colors on screen | Max 3 accents. Dim or remove before adding more |
| `run_time=2` for simple transforms | `run_time=0.5-0.6` — keep it snappy |
| Content touching frame edges | 0.8-unit minimum margin on all sides |
| Center-top persistent title | Top-LEFT corner: `.to_corner(UL, buff=0.5)` |
| `self.wait(0.5)` after multi-word text | `self.wait(max(2, word_count / 3))` |
| `Rectangle()` for a "server" or "database" | Custom SVG icon via `svg_icon()` helper |
| `Circle()` for a "user" or "person" | Custom SVG person icon |
| Raw Manim colors in SVG fills (`BLUE`) | Palette hex values (`#ff3366`) |
| Gradients/filters in SVGs | Flat fills only |
| `TEXT_DIM` for body text (font_size >= 20) | `TEXT_CLR` — TEXT_DIM is only for captions (16) and axis labels |
| Hard-coded box width with text inside | `make_node()` — auto-sizes box to fit text. Or measure: `max(w, text.width + 0.6)` |
| Animating a raw Rectangle for a progress bar fill | `progress_bar()` + `set_progress()` — fill stays inside track |
