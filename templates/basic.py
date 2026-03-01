from manim import *

# ---- Style Constants (will be replaced by shared_style) ----
BG_COLOR = "#1e1e2e"
ACCENT = BLUE
HIGHLIGHT = YELLOW
TEXT_CLR = WHITE
TITLE_SIZE = 48
BODY_SIZE = 32
LABEL_SIZE = 24

class BasicScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- Title Card ---
        title = Text("Scene Title", font_size=TITLE_SIZE, color=TEXT_CLR)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP).scale(0.6))

        # --- Main Content ---
        content = Text("Main content here", font_size=BODY_SIZE, color=TEXT_CLR)
        self.play(FadeIn(content))
        self.wait(2)

        # --- Transition Out ---
        self.play(*[FadeOut(mob) for mob in self.mobjects])
