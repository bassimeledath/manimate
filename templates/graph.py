import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *


class GraphScene(Scene):
    def construct(self):
        setup_scene(self)

        # 1. Title card
        title = title_card(self, "Graph Title")

        # 2. Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 10],
            axis_config={
                "color": TEXT_DIM,
                "stroke_width": 1.5,
                "include_numbers": True,
            },
            x_length=8,
            y_length=5,
        )
        self.play(Create(axes), run_time=1.0)

        # 3. Plot curve
        graph = axes.plot(lambda x: x**2, color=PRIMARY)
        label = Text("O(n\u00b2)", font="Monaco", font_size=20, color=PRIMARY)
        label.next_to(graph.get_end(), RIGHT, buff=0.2)
        self.play(Create(graph), run_time=1.5)
        self.play(FadeIn(label, shift=UP * 0.2), run_time=0.3)
        self.wait(2)

        # 4. Exit
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )
