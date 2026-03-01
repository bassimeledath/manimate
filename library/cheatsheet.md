# Manim Cheatsheet

## Import
from manim import *  # ALWAYS use this — never manimlib

## Scene Structure
class MyScene(Scene):
    def construct(self):
        # All animation logic here
        pass

## Common Mobjects
- Text("hello", font_size=32)          # Pango text (no LaTeX needed)
- MathTex(r"a^2 + b^2 = c^2")         # LaTeX math
- Tex(r"Hello \textbf{World}")         # LaTeX text
- Circle(), Square(), Triangle()        # Shapes
- Arrow(start, end)                     # Arrow
- Line(start, end)                      # Line
- Dot(point)                            # Point
- VGroup(obj1, obj2, ...)              # Group of objects
- NumberLine(x_range=[0, 10])           # Number line
- Axes(x_range=[-3,3], y_range=[-1,5]) # Coordinate axes
- Code(code="...", language="python")   # Code block

## Positioning
- obj.to_edge(UP / DOWN / LEFT / RIGHT)
- obj.to_corner(UL / UR / DL / DR)
- obj.next_to(other, RIGHT, buff=0.5)
- obj.move_to(ORIGIN)
- obj.shift(2 * RIGHT + 1 * UP)
- Constants: UP, DOWN, LEFT, RIGHT, ORIGIN, UL, UR, DL, DR

## Key Animations
- self.play(Create(obj))                # Draw object
- self.play(Write(text))                # Write text
- self.play(FadeIn(obj))                # Fade in
- self.play(FadeOut(obj))               # Fade out
- self.play(Transform(a, b))           # Morph a into b (a is modified)
- self.play(ReplacementTransform(a, b)) # Replace a with b
- self.play(Indicate(obj))              # Flash highlight
- self.play(obj.animate.shift(RIGHT))  # Animate property change
- self.play(obj.animate.set_color(RED)) # Animate color change
- self.wait(2)                          # Pause 2 seconds

## Animation Modifiers
- self.play(Create(obj), run_time=2)                    # Duration
- self.play(obj.animate.shift(RIGHT), rate_func=linear) # Easing
- self.play(AnimationGroup(a1, a2, lag_ratio=0.5))      # Staggered

## Quality Flags (CLI)
- -ql  →  854x480  @ 15fps
- -qm  →  1280x720 @ 30fps (default for this skill)
- -qh  →  1920x1080 @ 60fps
- -qk  →  3840x2160 @ 60fps

## Colors
PRIMARY:   BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, TEAL, PINK
SHADES:    RED_A (lightest) → RED_E (darkest), same for all colors
NEUTRAL:   WHITE, BLACK, GREY, GREY_A → GREY_E
SPECIAL:   GOLD, MAROON, DARK_BROWN, LIGHT_BROWN
