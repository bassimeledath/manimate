# Style Guide

## Background
- Default: config.background_color = "#1e1e2e" (dark navy)
- Alternative: WHITE for academic/clean style

## Color Palette (Educational Style)
- Primary: BLUE (#58C4DD) — main concepts, default objects
- Highlight: YELLOW (#F7D96F) — focus, emphasis, current step
- Success: GREEN (#83C167) — correct, found, complete
- Error: RED (#FC6255) — wrong, eliminated, error
- Secondary: PURPLE (#9A72AC) — secondary concepts
- Text: WHITE on dark bg, BLACK on light bg

## Typography
- Title: font_size=48, centered, bold weight
- Body: font_size=32
- Labels: font_size=24
- Code: font_size=20
- Minimum readable: font_size=20

## Timing
- Simple creation (shape): run_time=0.5-1.0
- Text write: run_time=1.0-2.0
- Transform: run_time=1.0-1.5
- Pause between concepts: self.wait(1.0-2.0)
- Scene intro title: display 2s, then animate to top
- Fast-fast-SLOW-fast-fast rhythm for emphasis

## Layout
- Title at top: .to_edge(UP)
- Main content: centered (ORIGIN) or slightly below center
- Labels: next_to() their referent with buff=0.3
- Side-by-side: shift(2*LEFT) and shift(2*RIGHT)
- Leave margins: don't place objects within 0.5 units of frame edge

## Scene Pattern
1. Title card (2s) — Write title, wait, animate to top
2. Build content (main body) — progressive disclosure
3. Key insight (emphasis) — Indicate or highlight
4. Transition out — FadeOut everything
