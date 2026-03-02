import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *


class QuadraticSetup(Scene):
    """Scene 1: Introduce the quadratic equation."""
    def construct(self):
        setup_scene(self)

        title = title_card(self, "The Quadratic Formula")

        # Starting equation in a card
        card = RoundedRectangle(
            corner_radius=0.15, width=8, height=2,
            fill_color=SURFACE, fill_opacity=0.8,
            stroke_color=BORDER, stroke_width=1,
        )
        eq = MathTex(r"ax^2 + bx + c = 0", font_size=44)
        eq.set_color(TEXT_CLR)
        eq.move_to(card)

        self.play(FadeIn(card, shift=UP * 0.4), run_time=0.4)
        self.play(Write(eq), run_time=0.7)
        self.wait(1)

        desc = Text(
            "We want to solve for x",
            font="Helvetica Neue", font_size=26, color=TEXT_CLR,
        )
        desc.next_to(card, DOWN, buff=0.5)
        self.play(FadeIn(desc, shift=UP * 0.3), run_time=0.4)
        self.wait(tw("We want to solve for x"))

        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )


class QuadraticDerivation(Scene):
    """Scene 2: Derive the formula step by step."""
    def construct(self):
        setup_scene(self)

        title = title_card(self, "Completing the Square")

        steps = [
            r"ax^2 + bx + c = 0",
            r"x^2 + \frac{b}{a}x = -\frac{c}{a}",
            r"x^2 + \frac{b}{a}x + \frac{b^2}{4a^2} = \frac{b^2}{4a^2} - \frac{c}{a}",
            r"\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}",
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
        ]

        current = MathTex(steps[0], font_size=36)
        current.set_color(TEXT_CLR)
        self.play(Write(current), run_time=0.7)
        self.wait(1.5)

        for step in steps[1:]:
            next_eq = MathTex(step, font_size=36)
            next_eq.set_color(TEXT_CLR)
            self.play(TransformMatchingTex(current, next_eq), run_time=0.6)
            current = next_eq
            self.wait(1.5)

        # Highlight the final formula with a rounded card
        highlight = RoundedRectangle(
            corner_radius=0.15,
            width=current.width + 0.6, height=current.height + 0.4,
            fill_color=SURFACE, fill_opacity=0.5,
            stroke_color=PRIMARY, stroke_width=2,
        )
        highlight.move_to(current)
        self.play(FadeIn(highlight), run_time=0.3)

        # Pop emphasis
        self.play(highlight.animate.scale(1.05), run_time=0.2)
        self.play(highlight.animate.scale(1.0), run_time=0.3)
        self.wait(2)

        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )
