from manim import *

BG_COLOR = "#1e1e2e"
ACCENT = BLUE
HIGHLIGHT = YELLOW
TEXT_CLR = WHITE


class QuadraticSetup(Scene):
    """Scene 1: Introduce the quadratic equation."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("The Quadratic Formula", font_size=48, color=TEXT_CLR)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP).scale(0.6))

        eq = MathTex(r"ax^2 + bx + c = 0", font_size=44)
        self.play(Write(eq))
        self.wait(1)

        desc = Text("We want to solve for x", font_size=28, color=ACCENT)
        desc.next_to(eq, DOWN, buff=0.8)
        self.play(FadeIn(desc))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])


class QuadraticDerivation(Scene):
    """Scene 2: Derive the formula step by step."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Completing the Square", font_size=28, color=TEXT_CLR).to_edge(UP)
        self.add(title)

        steps = [
            r"ax^2 + bx + c = 0",
            r"x^2 + \frac{b}{a}x = -\frac{c}{a}",
            r"x^2 + \frac{b}{a}x + \frac{b^2}{4a^2} = \frac{b^2}{4a^2} - \frac{c}{a}",
            r"\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}",
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
        ]

        current = MathTex(steps[0], font_size=36)
        self.play(Write(current))
        self.wait(1)

        for step in steps[1:]:
            next_eq = MathTex(step, font_size=36)
            self.play(TransformMatchingTex(current, next_eq))
            current = next_eq
            self.wait(1.5)

        # Highlight the final formula
        box = SurroundingRectangle(current, color=HIGHLIGHT, buff=0.2)
        self.play(Create(box))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
