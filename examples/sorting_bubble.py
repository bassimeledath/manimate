import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *


class BubbleSortIntro(Scene):
    """Scene 1: Show unsorted array and explain the concept."""
    def construct(self):
        setup_scene(self)

        title = title_card(self, "Bubble Sort")

        values = [5, 3, 8, 1, 4]
        bars = VGroup(*[
            RoundedRectangle(
                corner_radius=0.08, width=0.8, height=v * 0.5,
                fill_color=ACCENT, fill_opacity=0.6,
                stroke_color=BORDER, stroke_width=1.5,
            )
            for v in values
        ]).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        labels = VGroup(*[
            Text(str(v), font="Monaco", font_size=24, color=TEXT_CLR).next_to(bars[i], DOWN, buff=0.2)
            for i, v in enumerate(values)
        ])
        chart = VGroup(bars, labels).move_to(ORIGIN)

        self.play(
            AnimationGroup(*[
                FadeIn(VGroup(bars[i], labels[i]), shift=UP * 0.4)
                for i in range(len(values))
            ], lag_ratio=0.12),
            run_time=0.7,
        )
        self.wait(1)

        desc = Text(
            "Compare adjacent pairs, swap if needed",
            font="Avenir Next", font_size=26, color=TEXT_CLR,
        )
        desc.next_to(chart, DOWN, buff=0.8)
        self.play(FadeIn(desc, shift=UP * 0.3), run_time=0.4)
        self.wait(tw("Compare adjacent pairs, swap if needed"))

        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )


class BubbleSortAnimation(Scene):
    """Scene 2: Animate one pass of bubble sort."""
    def construct(self):
        setup_scene(self)

        title = title_card(self, "Bubble Sort — Pass 1")

        values = [5, 3, 8, 1, 4]
        spacing = 1.0

        bars = VGroup(*[
            RoundedRectangle(
                corner_radius=0.08, width=0.8, height=v * 0.5,
                fill_color=ACCENT, fill_opacity=0.6,
                stroke_color=BORDER, stroke_width=1.5,
            )
            for v in values
        ]).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        labels = VGroup(*[
            Text(str(v), font="Monaco", font_size=24, color=TEXT_CLR).next_to(bars[i], DOWN, buff=0.2)
            for i, v in enumerate(values)
        ])
        self.add(bars, labels)

        for i in range(len(values) - 1):
            # Highlight pair being compared
            self.play(
                bars[i].animate.set_stroke(color=PRIMARY, width=2.5),
                bars[i + 1].animate.set_stroke(color=PRIMARY, width=2.5),
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
                values[i], values[i + 1] = values[i + 1], values[i]
                bars[i], bars[i + 1] = bars[i + 1], bars[i]
                labels[i], labels[i + 1] = labels[i + 1], labels[i]

            # Reset stroke
            self.play(
                bars[i].animate.set_stroke(color=BORDER, width=1.5),
                bars[i + 1].animate.set_stroke(color=BORDER, width=1.5),
                run_time=0.2,
            )

        # Mark last element as sorted
        self.play(bars[-1].animate.set_fill(SUCCESS, opacity=0.6), run_time=0.3)
        self.wait(2)

        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )
