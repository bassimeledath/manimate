# Common Errors and Fixes

## 1. Wrong import
BAD:  from manimlib import *     # This is ManimGL (3b1b's version)
GOOD: from manim import *        # This is ManimCE (Community Edition)

## 2. ShowCreation is deprecated
BAD:  self.play(ShowCreation(circle))
GOOD: self.play(Create(circle))

## 3. Multiple .animate on same object in one play()
BAD:  self.play(obj.animate.shift(RIGHT), obj.animate.set_color(RED))
GOOD: self.play(obj.animate.shift(RIGHT).set_color(RED))  # chain on one .animate

## 4. Transform doesn't replace the object
After Transform(a, b), the variable `a` still refers to the scene object.
Use ReplacementTransform(a, b) if you want `b` to be the scene object.

## 5. Forgetting to add objects to scene
Objects must be added (via self.add() or self.play(Create/FadeIn)) before animating.

## 6. LaTeX errors
If you get "LaTeX Error", check:
- Raw string prefix: r"..." not "..."
- Balanced braces: every { has a matching }
- Valid LaTeX commands (no custom macros without defining them)
Fallback: Use Text() instead of MathTex() if LaTeX keeps failing.

## 7. Overlapping text
Always check positions. Use .next_to() instead of absolute positioning.
Use VGroup().arrange() for layouts.

## 8. Animation after FadeOut
After FadeOut(obj), the object is removed. Don't animate it again without re-adding.

## 9. run_time must be positive
BAD:  self.play(Create(obj), run_time=0)
GOOD: self.play(Create(obj), run_time=0.5)

## 10. .animate chaining limitation with Succession
BAD:  Succession(circle.animate.shift(RIGHT), circle.animate.shift(UP))
GOOD: Use separate self.play() calls for sequential animations on the same object
