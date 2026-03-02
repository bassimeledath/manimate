import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *


class CodeScene(Scene):
    def construct(self):
        setup_scene(self)

        # 1. Title card
        title = title_card(self, "Code Walkthrough")

        # 2. Code Block
        code = Code(
            code="def example():\n    return 42",
            language="python",
            font_size=18,
            background="rectangle",
            background_stroke_color=BORDER,
            background_stroke_width=1,
            line_spacing=0.6,
        )
        self.play(FadeIn(code, shift=UP * 0.4), run_time=0.5)
        self.wait(2)

        # 3. Highlight a line — rounded highlight
        highlight = RoundedRectangle(
            corner_radius=0.08,
            width=code.width - 0.2,
            height=0.35,
            fill_color=PRIMARY, fill_opacity=0.12,
            stroke_width=0,
        )
        highlight.move_to(code.code[1])
        self.play(FadeIn(highlight), run_time=0.3)
        self.wait(1.5)

        # 4. Exit
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )
