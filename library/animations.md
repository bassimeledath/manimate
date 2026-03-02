# Animation Patterns

## Reading-Time Pacing (apply to ALL text)
Every text element must stay on screen long enough to read.
Formula: `self.wait(max(2, len("text content".split()) / 3))`

    # After writing any text, pause for reading:
    title = Text("The Problem", font_size=48)
    self.play(Write(title))
    self.wait(2)  # max(2, 2/3) = 2 (minimum floor)

    explanation = Text("We need to find the target in a sorted array", font_size=32)
    self.play(Write(explanation))
    self.wait(3.3)  # max(2, 10/3) = 3.3

    detail = Text("Binary search eliminates half the remaining elements each step", font_size=28)
    self.play(FadeIn(detail))
    self.wait(3.3)  # max(2, 10/3) = 3.3

## Progressive Disclosure
Show elements one at a time, building complexity:
    items = VGroup(item1, item2, item3).arrange(DOWN, buff=0.5)
    for item in items:
        self.play(FadeIn(item, shift=UP * 0.3))
        # Pause for reading — calculate from text content
        self.wait(max(2, len(item.text.split()) / 3))

## Transform Chain
Morph through a sequence of states:
    eq1 = MathTex(r"x^2 + 2x + 1")
    eq2 = MathTex(r"(x + 1)^2")
    self.play(Write(eq1))
    self.wait(2)  # pause to read the equation
    self.play(TransformMatchingTex(eq1, eq2))
    self.wait(2)  # pause to read the transformed result

## Highlight and Annotate
Draw attention to a specific part:
    box = SurroundingRectangle(target, color=YELLOW, buff=0.1)
    label = Text("key insight", font_size=24).next_to(box, DOWN)
    self.play(Create(box), Write(label))
    self.wait(3)  # annotations/insights: minimum 3 seconds

## Slide Transition
Clear the current scene, bring in the next:
    self.play(*[FadeOut(mob) for mob in self.mobjects])
    self.wait(1.5)  # transition pause between conceptual sections
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

## SVG Icon Animations

### Staggered Icon Entrance
Build a system diagram by revealing icons one at a time:
    icons = [svg_icon(SVG_USER, 0.8), svg_icon(SVG_SERVER, 0.8), svg_icon(SVG_DB, 0.8)]
    positions = [LEFT * 4, ORIGIN, RIGHT * 4]
    for icon, pos in zip(icons, positions):
        icon.move_to(pos)
        self.play(FadeIn(icon, shift=UP * 0.3), run_time=0.5)

### SVG Morphing (State Change)
Morph between two SVGs with matching structure to show state transitions:
    lock = svg_icon(SVG_LOCK, scale=1.5)
    unlock = svg_icon(SVG_UNLOCK, scale=1.5)
    unlock.move_to(lock)
    self.play(FadeIn(lock, shift=UP * 0.3), run_time=0.6)
    self.wait(1)
    self.play(ReplacementTransform(lock, unlock), run_time=1.2)
    # TIP: keep same viewBox + element count for smooth morphs

### Data Flow Between SVG Icons
Animate a small object traveling from one icon to another:
    source = svg_icon(SVG_USER, 0.8).move_to(LEFT * 4)
    target = svg_icon(SVG_SERVER, 0.8).move_to(RIGHT * 4)
    arrow = Arrow(source.get_right(), target.get_left(), color=BORDER, buff=0.3)

    # Traveling object
    token = svg_icon(SVG_KEY, 0.4).move_to(source.get_right() + RIGHT * 0.3)
    self.play(FadeIn(token), run_time=0.3)
    self.play(token.animate.move_to(target.get_left() + LEFT * 0.3),
              run_time=1.5, rate_func=smooth)
    self.play(FadeOut(token), run_time=0.3)

### Icon-to-Icon Transition (Replace Concept)
Replace one concept icon with another to show progression:
    old_icon = svg_icon(SVG_WARNING, 0.8)
    new_icon = svg_icon(SVG_CHECK, 0.8).move_to(old_icon)
    self.play(FadeIn(old_icon, shift=UP * 0.3), run_time=0.6)
    self.wait(1)
    self.play(FadeOut(old_icon, scale=0.5), FadeIn(new_icon, scale=1.5), run_time=0.8)

### Hybrid Layout: SVG + Native Shapes
Mix SVG icons with Manim shapes for architecture diagrams:
    # SVG icons for real-world concepts
    user = svg_icon(SVG_USER, 0.7).move_to(LEFT * 4)
    server = svg_icon(SVG_SERVER, 0.7).move_to(RIGHT * 4)

    # Native shapes for abstract elements
    api_box = RoundedRectangle(corner_radius=0.15, width=2, height=0.8,
                               fill_color=SURFACE, fill_opacity=1,
                               stroke_color=PRIMARY, stroke_width=1.5)
    api_label = Text("API", font_size=20, color=TEXT_CLR).move_to(api_box)
    api_group = VGroup(api_box, api_label).move_to(ORIGIN)

    # Arrows connecting everything
    arr1 = Arrow(user.get_right(), api_group.get_left(), color=BORDER, buff=0.2, tip_length=0.15)
    arr2 = Arrow(api_group.get_right(), server.get_left(), color=BORDER, buff=0.2, tip_length=0.15)

### Coloring SVG Submobjects
Each top-level SVG element becomes a separate Manim submobject:
    icon = svg_icon(SVG_SERVER, 0.8)
    # Color individual rack units differently
    icon.submobjects[0].set_fill("#ff3366")  # first rect = pink
    icon.submobjects[1].set_fill("#ffcc00")  # second rect = yellow
    # Animate color change on a submobject
    self.play(icon.submobjects[2].animate.set_fill("#33ccff"), run_time=0.5)
