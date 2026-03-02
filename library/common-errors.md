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

## 11. Text too faint against background
```
BAD:  subtitle = Text("...", color=TEXT_DIM)  # invisible at font_size >= 20
GOOD: subtitle = Text("...", color=TEXT_CLR)  # TEXT_DIM only for font_size 16 captions
```

## 12. Text overflows container
```
BAD:  box = RoundedRectangle(width=3, ...)  # fixed width, text may not fit
      text = Text("educational", ...)
      text.move_to(box)  # text wider than box → overflow
GOOD: text = Text("educational", ...)
      box = RoundedRectangle(width=max(3, text.width + 0.6), ...)  # measure first
      text.move_to(box)
BEST: node = make_node("educational", color=HIGHLIGHT)  # auto-sizes
```

## 13. Character-by-character text animation causes flicker
```
BAD:  self.play(AddTextLetterByLetter(text))      # flickers badly in Manim CE
BAD:  for char in text: self.play(FadeIn(char))     # same issue, jarring
GOOD: self.play(Write(text), run_time=0.7)          # smooth handwriting effect
GOOD: self.play(FadeIn(text, shift=UP * 0.3))       # bounce entrance (preferred)
```
Never use `AddTextLetterByLetter`, `AddTextWordByWord`, or manual character-by-character loops. They produce visible flicker artifacts. Use `Write()` for a drawing effect or `FadeIn(shift=UP)` for the signature bounce.

## 14. Child elements escape parent container
```
BAD:  terminal = RoundedRectangle(width=8, height=4, ...)
      badge = make_node("quality: high")
      badge.next_to(terminal, DOWN, buff=0.5)  # badge is OUTSIDE the terminal
GOOD: badge.move_to(terminal.get_bottom() + UP * 0.5)  # badge stays INSIDE
```
When placing elements inside a container, use `.move_to()` with offsets from the container's edges, or use `.align_to()`. Never use `.next_to(container, ...)` for child elements — that places them OUTSIDE. Verify with: `assert container.get_left()[0] <= child.get_left()[0]`.

## 15. Missing spaces in concatenated/formatted text
```
BAD:  Text(f"{label}{value}")              # "Parametersinferred"
BAD:  Text(f">{command}")                  # ">/manimate..."
GOOD: Text(f"{label}: {value}")            # "Parameters: inferred"
GOOD: Text(f"> {command}")                 # "> /manimate ..."
```
Always double-check string literals for missing spaces, especially in f-strings and concatenations. Preview the string value mentally before passing to Text().

## 16. Font kerning issues at small sizes
Manim's Cairo renderer can produce subtle character-spacing artifacts with certain fonts, especially "Avenir Next" at font_size <= 20. If text looks oddly spaced:
```
# Option 1: Use Monaco for technical text (monospace = consistent spacing)
label = Text("access_token", font="Monaco", font_size=16, color=TEXT_DIM)

# Option 2: Use slightly larger font size
label = Text("Access granted", font="Avenir Next", font_size=22, color=TEXT_CLR)
```
For critical text that must be pixel-perfect, prefer `font="Monaco"` or increase font_size to 22+.

## 17. Progress bar fill overflows track
```
BAD:  fill = Rectangle(width=0.1, ...)
      self.play(fill.animate.stretch_to_fit_width(8))  # exceeds track
GOOD: bar = progress_bar(width=8)
      self.play(set_progress(bar, 0.75), run_time=1.0)  # always stays inside
```
