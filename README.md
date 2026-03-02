# /manimate

A coding-agent skill that turns natural language prompts into animated videos using Manim.

![How manimate works](public/manimate-intro.gif)

## Install

```bash
npx skills add bassimeledath/manimate
```

<details>
<summary>Other install methods</summary>

```bash
# npm
npx @bassimeledath/manimate

# Manual (Claude Code)
git clone https://github.com/bassimeledath/manimate ~/.claude/skills/manimate

# Manual (Codex)
git clone https://github.com/bassimeledath/manimate ~/.codex/skills/manimate
```
</details>

## Usage

```
/manimate "show the Pythagorean theorem"
/manimate "explain how binary search works"
/manimate "visualize bubble sort step by step"
```

Outputs to `.manimate/output/animation.mp4` (GIF available on request).

## Dependencies

- **Python 3.8+** and **ManimCE** (`pip install manim`)
- **ffmpeg** — video stitching
- **LaTeX** (optional) — for math expressions. Falls back to Text() if unavailable
- A supported agent CLI (`claude`, `codex`, or set `MANIMATE_AGENT_CLI`)

## How It Works

Prompt → Story → Code → Render → Video.

The agent decomposes your prompt into scenes, writes Manim Python code for each, renders via Cairo, and stitches the results with ffmpeg. Failed renders auto-recover (max 3 retries). An optional visual validation step checks layout and readability.
