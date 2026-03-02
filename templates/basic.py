import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *


# ── SVG Assets (generated in Step 6, loaded here by asset_manifest ID) ──
# icon = load_asset("your_asset_id", scale=0.8)  # ID from story.json asset_manifest
# For rare one-off SVGs (under 5 lines), use svg_icon() instead:
# icon = svg_icon('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">...</svg>', scale=0.8)


class BasicScene(Scene):
    def construct(self):
        setup_scene(self)

        # 1. Title card — bounce in, display, move to corner
        title = title_card(self, "Scene Title")

        # 2. Main content — replace with your asset_manifest ID
        icon = load_asset("your_asset_id", scale=0.8)
        label = Text("Server", font="Avenir Next", font_size=20, color=TEXT_CLR)
        label.next_to(icon, DOWN, buff=0.3)
        content = VGroup(icon, label)
        content.move_to(ORIGIN)

        self.play(FadeIn(icon, shift=UP * 0.4), run_time=0.5)
        self.play(FadeIn(label, shift=UP * 0.2), run_time=0.3)
        self.wait(2)

        # 3. Exit (drop out)
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.3) for mob in self.mobjects],
            run_time=0.4,
        )
