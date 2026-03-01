from manim import *

BG_COLOR = "#1e1e2e"
ACCENT = BLUE
HIGHLIGHT = YELLOW
TEXT_CLR = WHITE
TITLE_SIZE = 48
LABEL_SIZE = 24

class GraphScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- Title ---
        title = Text("Graph Title", font_size=TITLE_SIZE, color=TEXT_CLR)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP).scale(0.6))

        # --- Axes ---
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 10],
            axis_config={"include_numbers": True, "color": TEXT_CLR},
        )
        self.play(Create(axes), run_time=1.5)

        # --- Plot ---
        graph = axes.plot(lambda x: x**2, color=ACCENT)
        label = axes.get_graph_label(graph, label="f(x)", color=ACCENT)
        self.play(Create(graph), Write(label), run_time=2)
        self.wait(2)

        # --- Cleanup ---
        self.play(*[FadeOut(mob) for mob in self.mobjects])
