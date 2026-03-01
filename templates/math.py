from manim import *

BG_COLOR = "#1e1e2e"
ACCENT = BLUE
HIGHLIGHT = YELLOW
TEXT_CLR = WHITE
TITLE_SIZE = 48
BODY_SIZE = 36

class MathScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- Title ---
        title = Text("Mathematical Concept", font_size=TITLE_SIZE, color=TEXT_CLR)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP).scale(0.6))

        # --- Equation ---
        eq1 = MathTex(r"a^2 + b^2 = c^2", font_size=BODY_SIZE)
        self.play(Write(eq1))
        self.wait(1)

        # --- Transform ---
        eq2 = MathTex(r"c = \sqrt{a^2 + b^2}", font_size=BODY_SIZE)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(2)

        # --- Cleanup ---
        self.play(*[FadeOut(mob) for mob in self.mobjects])
