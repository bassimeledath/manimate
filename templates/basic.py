from manim import *
import tempfile, os

# ── Creative Chaos Dark ──
BG        = "#2a2a3a"
SURFACE   = "#3a3a4a"
BORDER    = "#4a4a5a"
PRIMARY   = "#ff3366"
ACCENT    = "#33ccff"
HIGHLIGHT = "#ffcc00"
SUCCESS   = "#66ff66"
NEGATIVE  = "#ff4444"
TEXT_CLR  = "#ffffff"
TEXT_DIM  = "#6a6a8a"


def svg_icon(svg_string, scale=1.0):
    """Write inline SVG to temp file and load as SVGMobject."""
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, "icon.svg")
    with open(path, "w") as f:
        f.write(svg_string)
    return SVGMobject(path).scale(scale)


# ── SVG Assets (define inline, adapt colors to match shared_style) ──
# Example: a server icon using the Creative Chaos palette
SVG_EXAMPLE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100">
  <rect x="5" y="5" width="70" height="25" rx="5" fill="#ff3366" stroke="#fff" stroke-width="2"/>
  <rect x="5" y="38" width="70" height="25" rx="5" fill="#ff3366" stroke="#fff" stroke-width="2"/>
  <rect x="5" y="71" width="70" height="25" rx="5" fill="#ff3366" stroke="#fff" stroke-width="2"/>
  <circle cx="18" cy="17" r="4" fill="#33ccff"/>
  <circle cx="18" cy="50" r="4" fill="#33ccff"/>
  <circle cx="18" cy="83" r="4" fill="#ffcc00"/>
</svg>'''


class BasicScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # 1. Dot grid (signature background)
        dots = VGroup(*[
            Dot([x, y, 0], radius=0.02, fill_opacity=0.08, color=TEXT_CLR)
            for x in range(-7, 8) for y in range(-4, 5)
        ])
        self.add(dots)

        # 2. Title card with signature underline
        title = Text("Scene Title", font="Galvji", font_size=44, color=TEXT_CLR, weight=BOLD)
        underline = Line(
            title.get_left() + DOWN * 0.35,
            title.get_right() + DOWN * 0.35,
            color=PRIMARY, stroke_width=2.5,
        )
        self.play(
            FadeIn(title, shift=UP * 0.4),
            GrowFromCenter(underline),
            run_time=0.7,
        )
        self.wait(1.5)

        # 3. Transition title to corner
        self.play(
            title.animate.scale(0.55).to_corner(UL, buff=0.5),
            FadeOut(underline, run_time=0.3),
            run_time=0.5,
        )

        # 4. Main content — SVG icon example
        icon = svg_icon(SVG_EXAMPLE, scale=0.8)
        label = Text("Server", font="Avenir Next", font_size=20, color=TEXT_DIM)
        label.next_to(icon, DOWN, buff=0.3)
        self.play(FadeIn(icon, shift=UP * 0.4), run_time=0.5)
        self.play(FadeIn(label, shift=UP * 0.2), run_time=0.3)
        self.wait(2)

        # 5. Exit (drop out)
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )
