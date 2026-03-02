---
name: manimate
description: Generate diagram and animation videos from natural language descriptions using Manim. Outputs MP4 (default) or GIF on request.
---

# /manimate — Manim Animation Video Maker

Generate diagram and animation videos from natural language descriptions using Manim. Outputs MP4 video by default; GIF available on request.

## Usage

```
/manimate "explain how binary search works"
/manimate "show the Pythagorean theorem proof"
/manimate "visualize bubble sort step by step"
```

## Pipeline

When the user invokes `/manimate`, execute these steps in order (Steps 1-8 are the core pipeline; Step 9 is an optional visual validation offered after the report):

---

### Step 1: Parameter Inference

Parse the user's prompt and infer rendering parameters:

| Parameter | Range | Default | How to infer |
|-----------|-------|---------|--------------|
| `scenes` | 1-6 | 2 | Count distinct concepts/steps/phases in the prompt |
| `quality` | l/m/h | h | Default high; use medium for quick drafts |
| `format` | gif/mp4/both | mp4 | Default mp4; use gif or both only if user explicitly requests GIF |
| `style` | educational/minimal/cinematic | educational | Infer from the tone/subject |
| `duration_per_scene` | 5-15s | 8 | Longer for complex concepts, shorter for simple transitions |

Write to `.manimate/params.json`:

```json
{
  "prompt": "explain how binary search works",
  "scenes": 3,
  "quality": "h",
  "format": "mp4",
  "style": "educational",
  "duration_per_scene": 8
}
```

Write `.manimate/manim.cfg`:

```ini
[CLI]
quality = high_quality
format = mp4
renderer = cairo
disable_caching = True

[output]
media_dir = media
video_dir = {media_dir}/videos
images_dir = {media_dir}/images
```

> **Why `renderer = cairo`**: Cairo is the safe default for headless/CI environments. It requires no GPU, no display server, and no OpenGL context.

---

### Step 2: Preflight Checks

Verify dependencies and set pipeline-wide capability flags:

```bash
# Required: Python 3.8+
python3 --version 2>/dev/null || { echo "python3 not found"; exit 1; }

# Required: ManimCE
python3 -c "import manim; print(f'manim {manim.__version__}')" 2>/dev/null || {
  echo "manim not found. Install: pip install manim"
  exit 1
}

# Required: ffmpeg
command -v ffmpeg >/dev/null 2>&1 || { echo "ffmpeg not found"; exit 1; }

# Optional: LaTeX + dvisvgm
LATEX_AVAILABLE=false
if command -v latex >/dev/null 2>&1 && command -v dvisvgm >/dev/null 2>&1; then
  LATEX_AVAILABLE=true
  echo "LaTeX + dvisvgm available — MathTex/Tex enabled"
else
  echo "LaTeX or dvisvgm not found. Falling back to Text-only mode."
  echo "  Install: brew install --cask mactex-no-gui (macOS) or apt install texlive-full (Linux)"
fi

# Detect timeout command (used for render timeouts in Step 6)
TIMEOUT_CMD=""
if command -v gtimeout >/dev/null 2>&1; then
  TIMEOUT_CMD="gtimeout"
elif command -v timeout >/dev/null 2>&1; then
  TIMEOUT_CMD="timeout"
else
  echo "Neither timeout nor gtimeout found. Render hangs won't be caught."
fi
```

Create working directory:

```bash
rm -rf .manimate
mkdir -p .manimate/scenes .manimate/lastframes .manimate/output
```

> **Pipeline-wide LATEX_AVAILABLE flag**: When `false`, scene code must NOT use MathTex or Tex — use Text() for all text, including math expressions. Render equations as Unicode or ASCII.

---

### Step 3: Story Decomposition

Break the prompt into scenes. Each scene specifies visual elements, animations, and narrative arc.

Think about what real-world concepts in the prompt can be represented as **custom SVG icons** vs basic Manim shapes. Apply this rule of thumb: **if a human would draw a recognizable icon for the concept, specify an SVG — if it's abstract or structural, use native shapes.**

Prefer custom SVG icons for: servers, databases, users/people, documents, locks/keys, shields, clouds, devices (phones, laptops), brains/AI, gears, rockets, envelopes, globes, checkmarks, warnings, error/denied symbols.

Use basic Manim shapes only for: array cells, flowchart boxes, graphs/axes, code blocks, bullets/dots, containers, math expressions.

Each scene spec should include an `svg_assets` field listing the custom SVG icons the scene needs. This tells the scene generator which concepts deserve custom illustrations.

Write `.manimate/story.json`:

```json
{
  "title": "How Binary Search Works",
  "scenes": [
    {
      "id": 1,
      "title": "The Problem",
      "description": "Show a sorted array of numbers. Highlight that we need to find a target value.",
      "visual_elements": ["sorted array of boxes with numbers", "target value highlighted"],
      "animations": ["Create array", "Highlight target", "Write question text"],
      "svg_assets": [],
      "scene_class": "TheProblem",
      "duration": 8,
      "template": "basic",
      "text_elements": ["title: 3 words", "description: 12 words"],
      "estimated_reading_pauses": 6.0,
      "continuity_in": null,
      "continuity_out": "Array remains visible, target highlighted"
    }
  ],
  "shared_style": {
    "background_color": "#2a2a3a",
    "primary_color": "#ff3366",
    "accent_color": "#33ccff",
    "highlight_color": "#ffcc00",
    "success_color": "#66ff66",
    "text_color": "#ffffff",
    "muted_color": "#6a6a8a",
    "font_heading": "Galvji",
    "font_body": "Avenir Next",
    "font_code": "Monaco",
    "font_size_title": 44,
    "font_size_body": 26
  },
  "latex_available": true
}
```

**Example `svg_assets` for an API authentication scene:**
```json
"svg_assets": ["user_icon", "server_icon", "lock_icon", "key_icon", "shield_icon"]
```

The scene code will generate the actual SVG strings inline based on these asset names — they are hints, not file references.
```

**Continuity rules:**
- `continuity_out` of scene N must match `continuity_in` of scene N+1
- Shared visual elements should use identical styling constants
- Color palette must be consistent across all scenes (defined in `shared_style`)

**Pacing rules:**
- `text_elements` lists each text block with its approximate word count — used to calculate reading pauses
- `estimated_reading_pauses` is the total seconds of `self.wait()` needed for reading time (sum of `max(2, words / 3)` for each text block)
- `duration` must be >= animation time + `estimated_reading_pauses` — increase duration if needed to fit reading time
- Use the formula: **`self.wait(max(2, word_count / 3))`** after every text appearance

---

### Step 4: Outline Confirmation

Before generating any scene code, present the story outline to the user for review and approval.

**Build a readable summary from `.manimate/story.json`:**

```
Scene Outline for: "{title}"

  Scene 1: {scene_title}
    {description}
    Key visuals: {visual_elements joined as comma-separated list}
    Duration: {duration}s

  Scene 2: {scene_title}
    {description}
    Key visuals: {visual_elements joined as comma-separated list}
    Duration: {duration}s

  ...

Total duration: {sum of all durations}s
Output format: MP4 (default). Would you like GIF, or both?
```

**Present this outline to the user and ask:**

```
Does this outline look good? You can:
  1. Approve and continue
  2. Request changes (add/remove/reorder scenes, adjust descriptions, change durations)
  3. Change output format (mp4 / gif / both)
```

**Revision loop:**

- If the user requests changes, update `.manimate/story.json` accordingly (add/remove scenes, edit descriptions, adjust durations, etc.) and re-present the outline.
- If the user changes the output format, update `.manimate/params.json` (`format` field) and `.manimate/manim.cfg` to match.
- Repeat until the user explicitly approves.

Once approved, proceed to Step 5.

---

### Step 5: Scene Generation (Inline)

Generate each scene file directly. No sub-processes — the orchestrating agent writes the code itself, ensuring the user's chosen model is used for generation.

**For each scene N (sequentially):**

1. **Read the scene spec** from `.manimate/story.json` — extract the scene entry, `shared_style`, and `latex_available` flag.

2. **Read the relevant library files** based on scene template type:

| Scene template | Always read | Conditionally read |
|---------------|------------|-------------------|
| All types | `library/cheatsheet.md`, `library/style-guide.md`, `library/common-errors.md` | — |
| `basic` | — | `library/animations.md` |
| `math` | — | `library/animations.md`, `library/text-and-math.md` |
| `graph` | — | `library/animations.md` |
| `code` | — | `library/text-and-math.md` |

3. **Read the template** from `templates/{template}.py` (e.g., `templates/basic.py`).

4. **Write the scene file** to `.manimate/scenes/scene_NN.py` following these rules:

   1. Use `from manim import *` (NOT manimlib — that is ManimGL)
   2. Define exactly ONE Scene subclass named `{scene_class}` (from story.json)
   3. All animation logic goes in the `construct(self)` method
   4. Use self.play() for animations, self.wait() for pauses
   5. Use the shared_style colors/sizes for consistency across scenes
   6. Inline all constants — do NOT import from external modules
   7. Keep the scene self-contained (no file I/O, no network)
   8. Target duration: ~{duration}s (use self.wait() to pad if needed)
   9. Use .animate syntax for simple property changes
   10. Use Transform/ReplacementTransform for morphing between objects
   11. If `latex_available` is false: do NOT use MathTex or Tex — use Text() for all text including math. Render equations as Unicode. If true: use MathTex (not Tex) for math expressions.
   12. For real-world concepts (servers, databases, users, documents, locks, etc.), generate a custom SVG icon at runtime instead of using a basic rectangle or circle. Use the svg_icon() helper and follow the SVG Icon Style Rules in the style guide. SVGs must use flat colors only — NO gradients, NO filters, NO `<text>` elements, NO stroke-dasharray. Use Manim Text() for all labels.
   13. Define SVG strings as Python string constants at the top of the scene, write them via the svg_icon() helper. Keep SVGs simple with viewBox="0 0 80 100" or similar. Use colors from the shared_style palette.

   **Text Pacing Rules (CRITICAL — text must be readable):**

   14. After EVERY Write(text) or FadeIn(text), add a reading pause: `self.wait(max(2, len("your text content".split()) / 3))` — this gives ~180 WPM reading speed with a 2-second minimum.
   15. Title cards: display for at least 2 seconds before animating to corner/top
   16. Key insight or annotation text: minimum 3 seconds on screen
   17. NEVER use bare `self.wait()` after text — always calculate from word count
   18. NEVER use `self.wait(0.5)` or `self.wait(1)` after text that has more than 3 words
   19. Between conceptual sections, use `self.wait(1.5)` as a transition pause

5. **Validate the generated file:**

```bash
FILE=".manimate/scenes/scene_$(printf "%02d" $N).py"
SCENE_CLASS="<scene_class from story.json>"

python3 -c "compile(open('$FILE').read(), '$FILE', 'exec')" 2>/dev/null || {
  echo "Syntax error in $FILE — fix before rendering"
}

python3 -c "
import ast, sys
tree = ast.parse(open('$FILE').read())
classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
if '$SCENE_CLASS' not in classes:
    print(f'$FILE does not define class $SCENE_CLASS (found: {classes})')
    sys.exit(1)
print('$FILE defines $SCENE_CLASS')
"
```

If validation fails (syntax error or wrong class name), fix the file immediately and re-validate before moving on.

---

### Step 6: Render & Error Recovery

For each scene, render with Manim. If rendering fails, read the error output, fix the scene file directly, and retry. Max 3 attempts per scene.

**Output path resolution**: Manim writes to structured subdirs. After each render, resolve the actual output path.

**For each scene N**, run the render command:

```bash
SCENE_FILE="scene_$(printf "%02d" $N)"
SCENE_CLASS="<scene_class from story.json>"

RENDER_LOG=$(mktemp)
RENDER_CMD="manim render scenes/${SCENE_FILE}.py $SCENE_CLASS \
    --renderer=cairo -qh --format=mp4 --disable_caching"

if [ -n "$TIMEOUT_CMD" ]; then
  RENDER_CMD="$TIMEOUT_CMD 180 $RENDER_CMD"
fi

cd .manimate && eval $RENDER_CMD 2>"$RENDER_LOG"
RENDER_EXIT=$?
cd ..
```

**On success**: locate the output MP4:

```bash
QUALITY_SUBDIR="1080p60"  # matches -qh
EXPECTED_PATH=".manimate/media/videos/${SCENE_FILE}/${QUALITY_SUBDIR}/${SCENE_CLASS}.mp4"
if [ ! -f "$EXPECTED_PATH" ]; then
  FOUND_PATH=$(find .manimate/media/videos -name "${SCENE_CLASS}.mp4" 2>/dev/null | head -1)
fi
```

Then capture a last-frame PNG for visual validation:

```bash
manim render -ql -s --renderer=cairo --disable_caching \
  ".manimate/scenes/${SCENE_FILE}.py" "$SCENE_CLASS" 2>/dev/null || true
LASTFRAME=$(find .manimate/media/images -name "*.png" -newer ".manimate/scenes/${SCENE_FILE}.py" 2>/dev/null | head -1)
if [ -n "$LASTFRAME" ]; then
  cp "$LASTFRAME" ".manimate/lastframes/scene_$(printf "%02d" $N).png"
fi
```

**On failure (up to 3 retries):**

1. Read the render error output from the log file
2. Read the current scene file and `library/common-errors.md`
3. Fix the scene file directly — preserve the animation intent, fix the error, ensure the Scene class name stays `{scene_class}`
4. If LaTeX is failing, switch to Text() as fallback
5. Re-run the render command

---

### Step 7: Stitch & Convert

Run the render script to concatenate scene videos and convert to GIF:

```bash
bash "scripts/render.sh" \
  --scenes-dir .manimate/scenes \
  --media-dir .manimate/media \
  --output-dir .manimate/output \
  --format "$FORMAT" \
  --story-file .manimate/story.json
```

> `scripts/render.sh` is relative to the skill directory. `$FORMAT` comes from `.manimate/params.json`.

---

### Step 8: Report

```
Animation complete!

Prompt: "explain how binary search works"
Scenes: 3 (all rendered successfully)
Duration: 28s (8s + 12s + 8s)
Quality: 1080p @ 60fps
Renderer: cairo

Output:
  MP4: .manimate/output/animation.mp4 (1.2MB)
  GIF: .manimate/output/animation.gif (3.4MB)
  Last-frame previews: .manimate/lastframes/
```

---

### Step 9: Visual Validation (Optional)

After reporting, ask the user:

```
Would you like me to validate the animation quality before you see it? (recommended for final delivery)
```

If the user declines, skip this step entirely. If the user accepts, evaluate each scene's last-frame PNG.

**For each scene, read `.manimate/lastframes/scene_NN.png` and evaluate against this rubric:**

| Criterion | What to check | Pass condition |
|-----------|--------------|----------------|
| **Text readability** | All text visible, not cut off, readable size | No text extends beyond frame edges; font size >= 24px equivalent |
| **Color consistency** | Colors match `shared_style` from story.json | Background, accent, highlight, and text colors match the palette |
| **Layout balance** | No overlapping elements, nothing off-screen | All Mobjects within frame bounds; no unintended overlap |
| **Animation completeness** | Final frame shows expected end state | Last frame matches the scene's `description` / `continuity_out` |

**Evaluation process:**

1. Read `.manimate/story.json` to get `shared_style` and each scene's expected end state
2. For each scene, read the last-frame PNG from `.manimate/lastframes/scene_NN.png`
3. Evaluate the image against the four rubric criteria
4. Compile results

**Report format:**

```
Visual Validation Results:

  Scene 1 (TheProblem): PASS
  Scene 2 (TheSolution): FAIL
    - Text readability: title text cut off on right edge
    - Layout balance: array boxes overlap with subtitle
  Scene 3 (TheResult): PASS

Summary: 2/3 scenes passed
```

If any scenes fail, ask:

```
Scene(s) 2 failed validation. Would you like to regenerate the failed scene(s)?
```

If the user accepts, re-run Steps 5-6 for the failed scenes only, then re-stitch in Step 7 and re-validate.

> **Note**: This step uses only the agent's built-in image reading capability — no external dependencies required.

---

## Component Library Reference

Read these library files before writing each scene (see Step 5 for which files apply per scene type):

| File | Purpose | Used by |
|------|---------|---------|
| `library/cheatsheet.md` | Manim API quick reference | All scene types |
| `library/style-guide.md` | Color palette, font sizes, timing, SVG style rules | All scene types |
| `library/animations.md` | Animation patterns with code | basic, math, graph |
| `library/text-and-math.md` | Text, MathTex, Code patterns | math, code |
| `library/common-errors.md` | Known pitfalls and fixes | All scene types |

## Key Conventions

1. **ManimCE only** — `from manim import *` (never `manimlib`). Cairo renderer for headless safety.
2. **One Scene class per file** — each scene is a separate `.py` file for isolated error recovery.
3. **Inline generation** — the orchestrating agent writes scene files directly (no sub-processes), ensuring the user's chosen model is used throughout.
4. **Shared style via story.json** — colors, font sizes, and background are defined once and referenced by every scene for consistency.
5. **LaTeX fallback** — if LaTeX is unavailable, use `Text()` instead of `MathTex()`.
6. **Render timeout** — 180s timeout on render commands to catch hangs.
7. **Error recovery** — on render failure, read the error, fix the scene file, and retry. Max 3 attempts per scene.
8. **Selective library reads** — only read library docs relevant to the scene type to stay focused.
9. **SVG-forward visuals** — for real-world concepts (servers, users, databases, etc.), generate custom inline SVG icons instead of basic shapes. This is manimate's key visual differentiator.
