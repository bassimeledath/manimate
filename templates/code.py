from manim import *

BG_COLOR = "#1e1e2e"
ACCENT = BLUE
HIGHLIGHT = YELLOW
TEXT_CLR = WHITE
TITLE_SIZE = 48
CODE_SIZE = 20

class CodeScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- Title ---
        title = Text("Code Walkthrough", font_size=TITLE_SIZE, color=TEXT_CLR)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP).scale(0.6))

        # --- Code Block ---
        code = Code(
            code="def example():\n    return 42",
            language="python",
            font_size=CODE_SIZE,
            background="window",
        )
        self.play(Create(code))
        self.wait(2)

        # --- Highlight a line ---
        highlight = SurroundingRectangle(
            code.code[1],  # second line
            color=HIGHLIGHT,
            buff=0.05,
        )
        self.play(Create(highlight))
        self.wait(1)

        # --- Cleanup ---
        self.play(*[FadeOut(mob) for mob in self.mobjects])
