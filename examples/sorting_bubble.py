from manim import *

BG_COLOR = "#1e1e2e"
ACCENT = BLUE
HIGHLIGHT = YELLOW
SUCCESS = GREEN
COMPARE = RED
TEXT_CLR = WHITE


class BubbleSortIntro(Scene):
    """Scene 1: Show unsorted array and explain the concept."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Bubble Sort", font_size=48, color=TEXT_CLR)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP).scale(0.6))

        values = [5, 3, 8, 1, 4]
        bars = VGroup(*[
            Rectangle(width=0.8, height=v * 0.5, color=ACCENT, fill_opacity=0.6)
            for v in values
        ]).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        labels = VGroup(*[
            Text(str(v), font_size=24, color=TEXT_CLR).next_to(bars[i], DOWN, buff=0.2)
            for i, v in enumerate(values)
        ])
        chart = VGroup(bars, labels).move_to(ORIGIN)

        self.play(Create(chart))
        self.wait(1)

        desc = Text("Compare adjacent pairs, swap if needed", font_size=24, color=ACCENT)
        desc.next_to(chart, DOWN, buff=0.8)
        self.play(Write(desc))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])


class BubbleSortAnimation(Scene):
    """Scene 2: Animate one pass of bubble sort."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Bubble Sort — Pass 1", font_size=28, color=TEXT_CLR).to_edge(UP)
        self.add(title)

        values = [5, 3, 8, 1, 4]
        bar_width = 0.8
        spacing = 1.0

        bars = VGroup(*[
            Rectangle(width=bar_width, height=v * 0.5, color=ACCENT, fill_opacity=0.6)
            for v in values
        ]).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        labels = VGroup(*[
            Text(str(v), font_size=24, color=TEXT_CLR).next_to(bars[i], DOWN, buff=0.2)
            for i, v in enumerate(values)
        ])
        self.add(bars, labels)

        for i in range(len(values) - 1):
            # Highlight pair being compared
            self.play(
                bars[i].animate.set_color(COMPARE),
                bars[i + 1].animate.set_color(COMPARE),
                run_time=0.3,
            )
            self.wait(0.3)

            if values[i] > values[i + 1]:
                # Swap animation
                self.play(
                    bars[i].animate.shift(RIGHT * spacing),
                    bars[i + 1].animate.shift(LEFT * spacing),
                    labels[i].animate.shift(RIGHT * spacing),
                    labels[i + 1].animate.shift(LEFT * spacing),
                    run_time=0.5,
                )
                # Swap in data
                values[i], values[i + 1] = values[i + 1], values[i]
                bars[i], bars[i + 1] = bars[i + 1], bars[i]
                labels[i], labels[i + 1] = labels[i + 1], labels[i]

            # Reset color
            self.play(
                bars[i].animate.set_color(ACCENT),
                bars[i + 1].animate.set_color(ACCENT),
                run_time=0.2,
            )

        # Mark last element as sorted
        self.play(bars[-1].animate.set_color(SUCCESS))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
