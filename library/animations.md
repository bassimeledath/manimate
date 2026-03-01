# Animation Patterns

## Progressive Disclosure
Show elements one at a time, building complexity:
    items = VGroup(item1, item2, item3).arrange(DOWN, buff=0.5)
    for item in items:
        self.play(FadeIn(item, shift=UP * 0.3))
        self.wait(0.5)

## Transform Chain
Morph through a sequence of states:
    eq1 = MathTex(r"x^2 + 2x + 1")
    eq2 = MathTex(r"(x + 1)^2")
    self.play(Write(eq1))
    self.wait()
    self.play(TransformMatchingTex(eq1, eq2))

## Highlight and Annotate
Draw attention to a specific part:
    box = SurroundingRectangle(target, color=YELLOW, buff=0.1)
    label = Text("key insight", font_size=24).next_to(box, DOWN)
    self.play(Create(box), Write(label))

## Slide Transition
Clear the current scene, bring in the next:
    self.play(*[FadeOut(mob) for mob in self.mobjects])
    self.wait(0.3)
    # Now build the next section

## Array/List Visualization
    boxes = VGroup(*[
        Square(side_length=0.8).set_fill(BLUE, opacity=0.3)
        for _ in range(8)
    ]).arrange(RIGHT, buff=0.1)
    numbers = VGroup(*[
        Text(str(n), font_size=24).move_to(boxes[i])
        for i, n in enumerate([2, 5, 8, 12, 16, 23, 38, 56])
    ])
    array = VGroup(boxes, numbers)
    self.play(Create(array))

## Pointer/Arrow Indicator
    arrow = Arrow(start=UP, end=DOWN, color=YELLOW).next_to(boxes[3], UP)
    label = Text("mid", font_size=20).next_to(arrow, UP)
    self.play(Create(arrow), Write(label))
    # Move pointer:
    self.play(arrow.animate.next_to(boxes[5], UP),
              label.animate.next_to(boxes[5], UP).shift(UP * 0.5))

## Graph Plotting
    axes = Axes(x_range=[0, 10, 1], y_range=[0, 100, 10],
                axis_config={"include_numbers": True})
    graph = axes.plot(lambda x: x**2, color=BLUE)
    label = axes.get_graph_label(graph, label="x^2")
    self.play(Create(axes), run_time=1.5)
    self.play(Create(graph), Write(label), run_time=2)

## AnimationGroup (simultaneous)
    self.play(AnimationGroup(
        Create(circle),
        Write(label),
        FadeIn(arrow),
        lag_ratio=0.3  # stagger by 30%
    ))

## Succession (sequential in one play call)
    self.play(Succession(
        Write(step1),
        Write(step2),
        Write(step3),
        lag_ratio=1.0  # each waits for previous to finish
    ))
