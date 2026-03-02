from manim import *
import numpy as np

# ── Color palette (6-digit hex ONLY) ──
BG = "#1a1a2e"
ACCENT = "#6C63FF"
GREEN = "#6BCB77"
YELLOW = "#FFD93D"
RED = "#FF6B6B"
MUTED = "#888888"
TEXT_CLR = "#e0e0e0"
NODE_FILL = "#252545"
DIM_TEXT = "#666688"
CODE_BG = "#16213e"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Scene 1: "You have an idea"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class SceneIdea(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Cursor blink effect
        cursor = Rectangle(
            width=0.12, height=0.45,
            fill_color=ACCENT, fill_opacity=1, stroke_width=0
        )
        cursor.move_to(ORIGIN)

        self.play(FadeIn(cursor), run_time=0.2)
        self.play(cursor.animate.set_opacity(0), run_time=0.3)
        self.play(cursor.animate.set_opacity(1), run_time=0.3)

        # Type out the prompt
        prompt_text = '/manimate "explain how a CPU works"'
        typed = Text(prompt_text, font_size=34, color=TEXT_CLR)
        typed.move_to(ORIGIN)

        # Fade out cursor, write text
        self.play(FadeOut(cursor), run_time=0.1)
        self.play(AddTextLetterByLetter(typed, run_time=1.8))
        self.wait(0.3)

        # Caption fades in below
        caption = Text(
            "You have an idea. You want to explain it visually.",
            font_size=22, color=MUTED
        )
        caption.next_to(typed, DOWN, buff=0.8)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)
        self.wait(0.6)

        # Prompt lifts up and shrinks
        self.play(
            typed.animate.scale(0.6).to_edge(UP, buff=0.5),
            FadeOut(caption, shift=DOWN * 0.3),
            run_time=0.5,
        )

        # Big title card
        title = Text("/manimate", font_size=56, color=ACCENT, weight=BOLD)
        subtitle = Text(
            "from idea to animation in seconds",
            font_size=22, color=MUTED
        )
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(title, scale=0.8), run_time=0.4)
        self.play(FadeIn(subtitle, shift=UP * 0.15), run_time=0.3)
        self.wait(0.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Scene 2: "manimate breaks it down"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ScenePlan(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Section title
        heading = Text("Breaking it down", font_size=36, color=ACCENT, weight=BOLD)
        heading.to_edge(UP, buff=0.5)
        self.play(FadeIn(heading, shift=DOWN * 0.2), run_time=0.3)

        # Show prompt splitting into scenes
        prompt_box = RoundedRectangle(
            corner_radius=0.12, width=7, height=0.7,
            fill_color=NODE_FILL, fill_opacity=1,
            stroke_color=ACCENT, stroke_width=1.5
        )
        prompt_label = Text(
            '"explain how a CPU works"',
            font_size=22, color=TEXT_CLR
        )
        prompt_label.move_to(prompt_box)
        prompt_group = VGroup(prompt_box, prompt_label)
        prompt_group.next_to(heading, DOWN, buff=0.6)
        self.play(FadeIn(prompt_group, shift=LEFT * 0.3), run_time=0.3)
        self.wait(0.3)

        # Arrow down
        arrow_down = Arrow(
            prompt_group.get_bottom() + DOWN * 0.1,
            prompt_group.get_bottom() + DOWN * 0.8,
            color=MUTED, stroke_width=2, tip_length=0.15,
            max_stroke_width_to_length_ratio=10,
        )
        plan_label = Text("story.json", font_size=18, color=YELLOW)
        plan_label.next_to(arrow_down, RIGHT, buff=0.2)
        self.play(GrowArrow(arrow_down), FadeIn(plan_label), run_time=0.3)

        # Scene cards fan out
        scene_data = [
            ("Scene 1", "What is a CPU?"),
            ("Scene 2", "Fetch-Decode-Execute"),
            ("Scene 3", "Putting it together"),
        ]
        cards = VGroup()
        for i, (sc_title, sc_desc) in enumerate(scene_data):
            card_rect = RoundedRectangle(
                corner_radius=0.1, width=3.2, height=1.4,
                fill_color=NODE_FILL, fill_opacity=1,
                stroke_color=ACCENT, stroke_width=1.5
            )
            sc_t = Text(sc_title, font_size=18, color=ACCENT, weight=BOLD)
            sc_d = Text(sc_desc, font_size=15, color=MUTED)
            sc_t.move_to(card_rect.get_center() + UP * 0.25)
            sc_d.move_to(card_rect.get_center() + DOWN * 0.25)
            card = VGroup(card_rect, sc_t, sc_d)
            cards.add(card)

        cards.arrange(RIGHT, buff=0.4)
        cards.next_to(arrow_down, DOWN, buff=0.5)

        for i, card in enumerate(cards):
            self.play(
                FadeIn(card, shift=UP * 0.3),
                run_time=0.3,
            )

        # Caption
        caption = Text(
            "Your prompt becomes a structured, multi-scene plan.",
            font_size=20, color=MUTED
        )
        caption.next_to(cards, DOWN, buff=0.6)
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.3)
        self.wait(0.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Scene 3: "Scenes come to life"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class SceneRender(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = Text("Scenes come to life", font_size=36, color=ACCENT, weight=BOLD)
        heading.to_edge(UP, buff=0.5)
        self.play(FadeIn(heading, shift=DOWN * 0.2), run_time=0.3)

        # Show 3 render slots side by side
        slots = VGroup()
        statuses = []
        for i in range(3):
            frame = RoundedRectangle(
                corner_radius=0.1, width=3.0, height=2.0,
                fill_color=CODE_BG, fill_opacity=1,
                stroke_color=MUTED, stroke_width=1
            )
            label = Text(f"Scene {i+1}", font_size=16, color=MUTED)
            label.next_to(frame, UP, buff=0.15)

            # Code-like lines inside
            lines = VGroup()
            for j in range(4):
                line_w = np.random.uniform(1.2, 2.2)
                line = Rectangle(
                    width=line_w, height=0.1,
                    fill_color=DIM_TEXT, fill_opacity=0.4, stroke_width=0
                )
                lines.add(line)
            lines.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            lines.move_to(frame.get_center())

            slot = VGroup(frame, label, lines)
            slots.add(slot)
            statuses.append(None)

        slots.arrange(RIGHT, buff=0.6)
        slots.next_to(heading, DOWN, buff=0.6)

        self.play(
            *[FadeIn(slot, shift=UP * 0.2) for slot in slots],
            run_time=0.4,
        )

        # Render each scene: show spinner, then checkmark
        # Scene 1: success
        s1_spinner = Text("...", font_size=24, color=YELLOW)
        s1_spinner.move_to(slots[0][0].get_center())
        self.play(FadeOut(slots[0][2]), FadeIn(s1_spinner), run_time=0.2)
        self.wait(0.3)
        s1_check = Text("OK", font_size=28, color=GREEN, weight=BOLD)
        s1_check.move_to(slots[0][0].get_center())
        self.play(
            FadeOut(s1_spinner),
            FadeIn(s1_check, scale=1.3),
            slots[0][0].animate.set_stroke(color=GREEN, width=2),
            run_time=0.3,
        )

        # Scene 2: fails then recovers
        s2_spinner = Text("...", font_size=24, color=YELLOW)
        s2_spinner.move_to(slots[1][0].get_center())
        self.play(FadeOut(slots[1][2]), FadeIn(s2_spinner), run_time=0.2)
        self.wait(0.2)

        s2_x = Text("ERR", font_size=26, color=RED, weight=BOLD)
        s2_x.move_to(slots[1][0].get_center())
        self.play(
            FadeOut(s2_spinner),
            FadeIn(s2_x, scale=1.2),
            slots[1][0].animate.set_stroke(color=RED, width=2),
            run_time=0.25,
        )
        self.wait(0.2)

        # Retry label
        retry_label = Text("retry 1/3", font_size=14, color=YELLOW)
        retry_label.next_to(slots[1][0], DOWN, buff=0.15)
        self.play(FadeIn(retry_label), run_time=0.15)
        self.wait(0.2)

        # Success after retry
        s2_check = Text("OK", font_size=28, color=GREEN, weight=BOLD)
        s2_check.move_to(slots[1][0].get_center())
        self.play(
            FadeOut(s2_x), FadeOut(retry_label),
            FadeIn(s2_check, scale=1.3),
            slots[1][0].animate.set_stroke(color=GREEN, width=2),
            run_time=0.3,
        )

        # Scene 3: success
        s3_spinner = Text("...", font_size=24, color=YELLOW)
        s3_spinner.move_to(slots[2][0].get_center())
        self.play(FadeOut(slots[2][2]), FadeIn(s3_spinner), run_time=0.2)
        self.wait(0.3)
        s3_check = Text("OK", font_size=28, color=GREEN, weight=BOLD)
        s3_check.move_to(slots[2][0].get_center())
        self.play(
            FadeOut(s3_spinner),
            FadeIn(s3_check, scale=1.3),
            slots[2][0].animate.set_stroke(color=GREEN, width=2),
            run_time=0.3,
        )

        # Caption
        caption = Text(
            "The agent writes code, Manim renders, errors auto-recover.",
            font_size=20, color=MUTED
        )
        caption.next_to(slots, DOWN, buff=0.7)
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.3)
        self.wait(0.6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Scene 4: "The final cut"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class SceneOutput(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = Text("The final cut", font_size=36, color=ACCENT, weight=BOLD)
        heading.to_edge(UP, buff=0.5)
        self.play(FadeIn(heading, shift=DOWN * 0.2), run_time=0.3)

        # Three small scene thumbnails flowing into one
        thumbs = VGroup()
        for i in range(3):
            thumb = RoundedRectangle(
                corner_radius=0.08, width=1.8, height=1.2,
                fill_color=NODE_FILL, fill_opacity=1,
                stroke_color=GREEN, stroke_width=1.5
            )
            label = Text(f"S{i+1}", font_size=18, color=GREEN)
            label.move_to(thumb)
            thumbs.add(VGroup(thumb, label))

        thumbs.arrange(RIGHT, buff=0.5)
        thumbs.move_to(UP * 0.5)

        self.play(
            *[FadeIn(t, shift=DOWN * 0.2) for t in thumbs],
            run_time=0.3,
        )
        self.wait(0.3)

        # Stitch arrow
        stitch_label = Text("ffmpeg concat", font_size=16, color=MUTED)
        stitch_arrow = Arrow(
            thumbs.get_bottom() + DOWN * 0.2,
            thumbs.get_bottom() + DOWN * 1.1,
            color=MUTED, stroke_width=2, tip_length=0.15,
            max_stroke_width_to_length_ratio=10,
        )
        stitch_label.next_to(stitch_arrow, RIGHT, buff=0.2)
        self.play(GrowArrow(stitch_arrow), FadeIn(stitch_label), run_time=0.3)

        # Final output: big MP4 box
        output_rect = RoundedRectangle(
            corner_radius=0.15, width=4.0, height=1.4,
            fill_color="#1a3a1a", fill_opacity=1,
            stroke_color=GREEN, stroke_width=2.5
        )
        output_rect.next_to(stitch_arrow, DOWN, buff=0.3)

        mp4_label = Text("animation.mp4", font_size=26, color=GREEN, weight=BOLD)
        mp4_label.move_to(output_rect)
        output_group = VGroup(output_rect, mp4_label)

        self.play(FadeIn(output_group, scale=0.9), run_time=0.4)

        # Flash
        self.play(
            Flash(output_rect.get_center(), color=GREEN, line_length=0.4, num_lines=16),
            run_time=0.5,
        )

        # Final tagline
        tagline = Text(
            "/manimate — natural language to animation",
            font_size=22, color=ACCENT, weight=BOLD
        )
        tagline.next_to(output_group, DOWN, buff=0.6)
        self.play(FadeIn(tagline, shift=UP * 0.15), run_time=0.4)
        self.wait(1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
