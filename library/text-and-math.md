# Text & Math Reference

## Text (Pango-based — no LaTeX needed)
    title = Text("Hello World", font_size=48, color=TEXT_CLR)
    bold = Text("Bold", weight=BOLD, font_size=32)
    italic = Text("Italic", slant=ITALIC, font_size=32)

## MathTex (LaTeX math mode)
    eq = MathTex(r"E = mc^2", font_size=36)
    # Color specific parts:
    eq = MathTex(r"a^2", "+", r"b^2", "=", r"c^2")
    eq[0].set_color(PRIMARY)   # a^2
    eq[2].set_color(ACCENT)    # b^2

## TransformMatchingTex
    eq1 = MathTex(r"a^2 + b^2 = c^2")
    eq2 = MathTex(r"c = \sqrt{a^2 + b^2}")
    self.play(TransformMatchingTex(eq1, eq2))

## Code Blocks
    code = Code(
        code="def binary_search(arr, target):\n    lo, hi = 0, len(arr) - 1",
        language="python",
        font_size=20,
        background="window",
    )
    self.play(Create(code))

## Pitfalls
- MathTex requires LaTeX installed. If LaTeX is not available, use Text() instead.
- Use raw strings (r"...") for LaTeX to avoid escape issues.
- Double braces {{ }} in MathTex for literal braces.
- For multi-line equations, use aligned environment:
    MathTex(r"\begin{aligned} a &= b + c \\ d &= e + f \end{aligned}")
