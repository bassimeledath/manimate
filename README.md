# /animate

A coding-agent skill that generates diagram and animation videos from natural language prompts using Manim.

```
/animate "explain how binary search works"
```

Outputs: `.animate/output/animation.mp4` + `.animate/output/animation.gif`

## Installation

### Via npx skills (recommended)
```bash
npx skills add bassimeledath/manim-video-maker
```

### Via npm
```bash
npx @bassimeledath/animate
```

### Manual
```bash
# Claude Code
git clone https://github.com/bassimeledath/manim-video-maker ~/.claude/skills/animate

# Codex
git clone https://github.com/bassimeledath/manim-video-maker ~/.codex/skills/animate

# Other agents
git clone https://github.com/bassimeledath/manim-video-maker ~/.agents/skills/animate
```

## Dependencies

- **Python 3.8+** — Manim runtime
- **ManimCE** — `pip install manim`
- **ffmpeg** — video stitching and GIF conversion
- **LaTeX** (optional) — for MathTex/Tex. Falls back to Text() if unavailable
- A supported AI coding agent CLI (`claude`, `codex`, or set `ANIMATE_AGENT_CLI`)

## Agent Configuration

Animate auto-detects your agent CLI. Override with:

```bash
export ANIMATE_AGENT_CLI="codex --quiet --full-auto"
export ANIMATE_AGENT_ENV_UNSET="MY_AGENT_PARENT_SESSION"
```

## How It Works

The skill uses Manim (Community Edition) as a real animation rendering engine. The agent writes Python Scene classes, Manim renders them to video.

1. **Parameter inference** — parses your prompt to determine scene count, quality, style
2. **Preflight checks** — verifies python3, manim, ffmpeg, LaTeX availability
3. **Story decomposition** — breaks the prompt into scenes with visual specs and continuity notes
4. **Scene generation** — agent writes Python files with Manim Scene classes
5. **Render + error recovery** — `manim render` produces MP4; failures are auto-corrected (max 3 retries)
6. **Stitch + convert** — ffmpeg concatenates scenes and converts to GIF
7. **Report** — output paths and sizes

## Examples

```
# Simple (1 scene)
/animate "show the Pythagorean theorem"

# Medium (2-3 scenes)
/animate "explain how binary search works"

# Complex (3-4 scenes)
/animate "visualize bubble sort step by step with comparisons and swaps"
```

## Output

Files are written to `.animate/output/` in the current working directory:

| File | Format | Typical Size |
|------|--------|-------------|
| `animation.mp4` | H.264 MP4 | 0.5-3MB |
| `animation.gif` | Animated GIF | 1-5MB |

Last-frame PNGs for each scene are saved to `.animate/lastframes/`.

## Architecture

```
/animate "explain binary search"
    |
    |- Step 1: Infer parameters (scenes, quality, style)
    |- Step 2: Preflight (python3, manim, ffmpeg, latex?, timeout?)
    |- Step 3: Decompose into scenes -> story.json
    |- Step 4: Generate scenes sequentially (agent writes Python)
    |          Each scene validated: file exists + defines Scene class + valid syntax
    |- Step 5: Render each scene (manim render --renderer=cairo)
    |          Error recovery: parse error -> fix worker -> retry (max 3)
    |- Step 6: Stitch + convert (ffmpeg concat -> MP4 + GIF)
    '- Step 7: Report output paths
```

## Component Library

Reference docs injected into worker prompts:

- **cheatsheet.md** — Manim API quick reference (Mobjects, animations, positioning, colors)
- **style-guide.md** — color palette, font sizes, spacing, timing conventions
- **animations.md** — animation patterns with code examples
- **text-and-math.md** — Text, MathTex, Code block patterns
- **common-errors.md** — known pitfalls and fixes

Templates for different scene types: basic, math, graph, code.

Working examples: binary search, quadratic formula, bubble sort.
