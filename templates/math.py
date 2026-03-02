import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *


class MathScene(Scene):
    def construct(self):
        setup_scene(self)

        # 1. Title card
        title = title_card(self, "Mathematical Concept")

        # 2. Equation in a card
        card = RoundedRectangle(
            corner_radius=0.15, width=8, height=2.5,
            fill_color=SURFACE, fill_opacity=0.8,
            stroke_color=BORDER, stroke_width=1,
        )
        card.move_to(DOWN * 0.3)

        eq1 = MathTex(r"a^2 + b^2 = c^2", font_size=48)
        eq1.set_color(TEXT_CLR)
        eq1.move_to(card)

        self.play(FadeIn(card, shift=UP * 0.4), run_time=0.4)
        self.play(Write(eq1), run_time=1.0)
        self.wait(2)

        # 3. Transform
        eq2 = MathTex(r"c = \sqrt{a^2 + b^2}", font_size=48)
        eq2.set_color(TEXT_CLR)
        eq2.move_to(card)
        self.play(TransformMatchingTex(eq1, eq2), run_time=0.6)
        self.wait(2)

        # 4. Exit
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )
