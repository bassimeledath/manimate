from manim import *

BG_COLOR = "#1e1e2e"
ACCENT = BLUE
HIGHLIGHT = YELLOW
SUCCESS = GREEN
ELIMINATED = RED_D
TEXT_CLR = WHITE


class BinarySearchIntro(Scene):
    """Scene 1: Show the problem — a sorted array, we need to find a target."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Binary Search", font_size=48, color=TEXT_CLR)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP).scale(0.6))

        # Sorted array
        values = [2, 5, 8, 12, 16, 23, 38, 56]
        boxes = VGroup(*[
            Square(side_length=0.8, color=ACCENT, fill_opacity=0.2)
            for _ in values
        ]).arrange(RIGHT, buff=0.1)
        nums = VGroup(*[
            Text(str(v), font_size=24, color=TEXT_CLR).move_to(boxes[i])
            for i, v in enumerate(values)
        ])
        array = VGroup(boxes, nums)
        self.play(Create(array))
        self.wait(1)

        # Target
        target_label = Text("Find: 23", font_size=32, color=HIGHLIGHT)
        target_label.next_to(array, DOWN, buff=0.8)
        self.play(Write(target_label))

        # Highlight target in array
        self.play(boxes[5].animate.set_fill(HIGHLIGHT, opacity=0.4))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])


class BinarySearchAlgorithm(Scene):
    """Scene 2: Demonstrate the algorithm step by step."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Binary Search", font_size=28, color=TEXT_CLR).to_edge(UP)
        self.add(title)

        values = [2, 5, 8, 12, 16, 23, 38, 56]
        boxes = VGroup(*[
            Square(side_length=0.8, color=ACCENT, fill_opacity=0.2)
            for _ in values
        ]).arrange(RIGHT, buff=0.1)
        nums = VGroup(*[
            Text(str(v), font_size=24, color=TEXT_CLR).move_to(boxes[i])
            for i, v in enumerate(values)
        ])
        self.add(boxes, nums)

        target = 23
        lo, hi = 0, len(values) - 1

        lo_arrow = Arrow(UP * 0.5, ORIGIN, color=ACCENT).next_to(boxes[lo], DOWN)
        hi_arrow = Arrow(UP * 0.5, ORIGIN, color=ACCENT).next_to(boxes[hi], DOWN)
        lo_label = Text("lo", font_size=20, color=ACCENT).next_to(lo_arrow, DOWN, buff=0.1)
        hi_label = Text("hi", font_size=20, color=ACCENT).next_to(hi_arrow, DOWN, buff=0.1)

        self.play(Create(lo_arrow), Create(hi_arrow), Write(lo_label), Write(hi_label))
        self.wait(0.5)

        while lo <= hi:
            mid = (lo + hi) // 2
            mid_arrow = Arrow(UP * 0.5, ORIGIN, color=HIGHLIGHT).next_to(boxes[mid], UP)
            mid_label = Text("mid", font_size=20, color=HIGHLIGHT).next_to(mid_arrow, UP, buff=0.1)
            self.play(Create(mid_arrow), Write(mid_label))
            self.wait(0.5)

            if values[mid] == target:
                self.play(boxes[mid].animate.set_fill(SUCCESS, opacity=0.5))
                found = Text("Found!", font_size=32, color=SUCCESS).next_to(boxes[mid], UP, buff=1.2)
                self.play(Write(found))
                self.wait(1)
                break
            elif values[mid] < target:
                for i in range(lo, mid + 1):
                    self.play(boxes[i].animate.set_fill(ELIMINATED, opacity=0.3), run_time=0.2)
                lo = mid + 1
                self.play(
                    lo_arrow.animate.next_to(boxes[lo], DOWN),
                    lo_label.animate.next_to(boxes[lo], DOWN, buff=0.6),
                )
            else:
                for i in range(mid, hi + 1):
                    self.play(boxes[i].animate.set_fill(ELIMINATED, opacity=0.3), run_time=0.2)
                hi = mid - 1
                self.play(
                    hi_arrow.animate.next_to(boxes[hi], DOWN),
                    hi_label.animate.next_to(boxes[hi], DOWN, buff=0.6),
                )

            self.play(FadeOut(mid_arrow), FadeOut(mid_label))

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class BinarySearchComplexity(Scene):
    """Scene 3: Show O(log n) complexity compared to O(n)."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Why is it fast?", font_size=48, color=TEXT_CLR)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP).scale(0.6))

        axes = Axes(
            x_range=[1, 20, 2],
            y_range=[0, 20, 2],
            axis_config={"include_numbers": True, "color": TEXT_CLR},
            x_length=8,
            y_length=5,
        )
        x_label = axes.get_x_axis_label("n", color=TEXT_CLR)
        y_label = axes.get_y_axis_label("steps", color=TEXT_CLR)
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)

        import math
        linear = axes.plot(lambda x: x, color=ELIMINATED, x_range=[1, 20])
        log_graph = axes.plot(lambda x: math.log2(x) * 2, color=SUCCESS, x_range=[1, 20])

        lin_label = Text("O(n) linear", font_size=20, color=ELIMINATED)
        lin_label.next_to(linear.get_end(), RIGHT)
        log_label = Text("O(log n) binary", font_size=20, color=SUCCESS)
        log_label.next_to(log_graph.get_end(), RIGHT)

        self.play(Create(linear), Write(lin_label), run_time=2)
        self.play(Create(log_graph), Write(log_label), run_time=2)
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
