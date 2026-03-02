import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *


class BinarySearchIntro(Scene):
    """Scene 1: Show the problem — a sorted array, we need to find a target."""
    def construct(self):
        setup_scene(self)

        title = title_card(self, "Binary Search")

        # Sorted array (Square for data cells — the one exception to roundness)
        values = [2, 5, 8, 12, 16, 23, 38, 56]
        boxes = VGroup(*[
            Square(
                side_length=0.8,
                fill_color=SURFACE, fill_opacity=0.6,
                stroke_color=BORDER, stroke_width=1.5,
            )
            for _ in values
        ]).arrange(RIGHT, buff=0.1)
        nums = VGroup(*[
            Text(str(v), font="Monaco", font_size=24, color=TEXT_CLR).move_to(boxes[i])
            for i, v in enumerate(values)
        ])
        array = VGroup(boxes, nums)
        self.play(
            AnimationGroup(*[
                FadeIn(VGroup(boxes[i], nums[i]), shift=UP * 0.4)
                for i in range(len(values))
            ], lag_ratio=0.12),
            run_time=0.7,
        )
        self.wait(1)

        # Target
        target_label = Text("Find: 23", font="Helvetica Neue", font_size=26, color=HIGHLIGHT)
        target_label.next_to(array, DOWN, buff=0.8)
        self.play(FadeIn(target_label, shift=UP * 0.3), run_time=0.4)
        self.wait(tw("Find: 23"))

        # Highlight target in array
        self.play(boxes[5].animate.set_fill(HIGHLIGHT, opacity=0.4), run_time=0.3)
        self.wait(2)

        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )


class BinarySearchAlgorithm(Scene):
    """Scene 2: Demonstrate the algorithm step by step."""
    def construct(self):
        setup_scene(self)

        title = title_card(self, "Binary Search")

        values = [2, 5, 8, 12, 16, 23, 38, 56]
        boxes = VGroup(*[
            Square(
                side_length=0.8,
                fill_color=SURFACE, fill_opacity=0.6,
                stroke_color=BORDER, stroke_width=1.5,
            )
            for _ in values
        ]).arrange(RIGHT, buff=0.1)
        nums = VGroup(*[
            Text(str(v), font="Monaco", font_size=24, color=TEXT_CLR).move_to(boxes[i])
            for i, v in enumerate(values)
        ])
        self.add(boxes, nums)

        target = 23
        lo, hi = 0, len(values) - 1

        lo_arrow = Arrow(UP * 0.5, ORIGIN, color=ACCENT, tip_length=0.15).next_to(boxes[lo], DOWN)
        hi_arrow = Arrow(UP * 0.5, ORIGIN, color=ACCENT, tip_length=0.15).next_to(boxes[hi], DOWN)
        lo_label = Text("lo", font="Monaco", font_size=16, color=ACCENT).next_to(lo_arrow, DOWN, buff=0.1)
        hi_label = Text("hi", font="Monaco", font_size=16, color=ACCENT).next_to(hi_arrow, DOWN, buff=0.1)

        self.play(
            FadeIn(lo_arrow, shift=UP * 0.3),
            FadeIn(hi_arrow, shift=UP * 0.3),
            FadeIn(lo_label, shift=UP * 0.2),
            FadeIn(hi_label, shift=UP * 0.2),
            run_time=0.5,
        )
        self.wait(0.5)

        while lo <= hi:
            mid = (lo + hi) // 2
            mid_arrow = Arrow(DOWN * 0.5, ORIGIN, color=HIGHLIGHT, tip_length=0.15).next_to(boxes[mid], UP)
            mid_label = Text("mid", font="Monaco", font_size=16, color=HIGHLIGHT).next_to(mid_arrow, UP, buff=0.1)
            self.play(FadeIn(mid_arrow, shift=UP * 0.3), FadeIn(mid_label, shift=UP * 0.2), run_time=0.4)
            self.wait(0.5)

            if values[mid] == target:
                self.play(boxes[mid].animate.set_fill(SUCCESS, opacity=0.5), run_time=0.3)
                found = Text("Found!", font="Helvetica Neue", font_size=32, color=SUCCESS, weight=BOLD)
                found.next_to(boxes[mid], UP, buff=1.2)
                self.play(FadeIn(found, shift=UP * 0.4), run_time=0.5)
                self.wait(2)
                break
            elif values[mid] < target:
                for i in range(lo, mid + 1):
                    self.play(boxes[i].animate.set_fill(NEGATIVE, opacity=0.3), run_time=0.2)
                lo = mid + 1
                self.play(
                    lo_arrow.animate.next_to(boxes[lo], DOWN),
                    lo_label.animate.next_to(boxes[lo], DOWN, buff=0.6),
                    run_time=0.4,
                )
            else:
                for i in range(mid, hi + 1):
                    self.play(boxes[i].animate.set_fill(NEGATIVE, opacity=0.3), run_time=0.2)
                hi = mid - 1
                self.play(
                    hi_arrow.animate.next_to(boxes[hi], DOWN),
                    hi_label.animate.next_to(boxes[hi], DOWN, buff=0.6),
                    run_time=0.4,
                )

            self.play(FadeOut(mid_arrow), FadeOut(mid_label), run_time=0.3)

        self.wait(2)
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )


class BinarySearchComplexity(Scene):
    """Scene 3: Show O(log n) complexity compared to O(n)."""
    def construct(self):
        setup_scene(self)

        title = title_card(self, "Why is it fast?")

        import math

        axes = Axes(
            x_range=[1, 20, 2],
            y_range=[0, 20, 2],
            axis_config={
                "include_numbers": True,
                "color": TEXT_DIM,
                "stroke_width": 1.5,
            },
            x_length=8,
            y_length=5,
        )
        x_label = axes.get_x_axis_label("n", color=TEXT_DIM)
        y_label = axes.get_y_axis_label("steps", color=TEXT_DIM)
        self.play(FadeIn(axes, shift=UP * 0.3), FadeIn(x_label), FadeIn(y_label), run_time=0.7)

        linear = axes.plot(lambda x: x, color=NEGATIVE, x_range=[1, 20])
        log_graph = axes.plot(lambda x: math.log2(x) * 2, color=SUCCESS, x_range=[1, 20])

        lin_label = Text("O(n) linear", font="Monaco", font_size=16, color=NEGATIVE)
        lin_label.next_to(linear.get_end(), RIGHT, buff=0.2)
        log_label = Text("O(log n) binary", font="Monaco", font_size=16, color=SUCCESS)
        log_label.next_to(log_graph.get_end(), RIGHT, buff=0.2)

        self.play(Create(linear), FadeIn(lin_label, shift=UP * 0.2), run_time=0.7)
        self.play(Create(log_graph), FadeIn(log_label, shift=UP * 0.2), run_time=0.7)
        self.wait(3)

        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )
