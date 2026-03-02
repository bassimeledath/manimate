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

When the user invokes `/manimate`, execute these steps in order (Steps 1-7 are the core pipeline; Step 8 is an optional visual validation offered after the report):

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

# Detect agent CLI
MANIMATE_AGENT_CLI="${MANIMATE_AGENT_CLI:-}"
if [ -z "$MANIMATE_AGENT_CLI" ]; then
  if command -v claude >/dev/null 2>&1; then
    MANIMATE_AGENT_CLI="claude -p --dangerously-skip-permissions"
    MANIMATE_AGENT_ENV_UNSET="CLAUDE_CODE_ENTRYPOINT,CLAUDECODE"
  elif command -v codex >/dev/null 2>&1; then
    MANIMATE_AGENT_CLI="codex --quiet --full-auto"
    MANIMATE_AGENT_ENV_UNSET=""
  else
    echo "No supported agent CLI found. Set MANIMATE_AGENT_CLI env var."
    exit 1
  fi
fi
AGENT_BIN=$(echo "$MANIMATE_AGENT_CLI" | awk '{print $1}')
command -v "$AGENT_BIN" >/dev/null 2>&1 || { echo "Agent CLI '$AGENT_BIN' not found"; exit 1; }

# Detect timeout command
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

> **Pipeline-wide LATEX_AVAILABLE flag**: When `false`, worker prompts explicitly instruct the agent: "Do NOT use MathTex or Tex — use Text() for all text, including math expressions. Render equations as Unicode or ASCII."

---

### Step 3: Story Decomposition

Break the prompt into scenes. Each scene specifies visual elements, animations, and narrative arc.

Think about what real-world concepts in the prompt can be represented as **custom SVG icons** vs basic Manim shapes. Apply this rule of thumb: **if a human would draw a recognizable icon for the concept, specify an SVG — if it's abstract or structural, use native shapes.**

Prefer custom SVG icons for: servers, databases, users/people, documents, locks/keys, shields, clouds, devices (phones, laptops), brains/AI, gears, rockets, envelopes, globes, checkmarks, warnings, error/denied symbols.

Use basic Manim shapes only for: array cells, flowchart boxes, graphs/axes, code blocks, bullets/dots, containers, math expressions.

Each scene spec should include an `svg_assets` field listing the custom SVG icons the scene needs. This tells workers which concepts deserve custom illustrations.

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

Workers will generate the actual SVG strings inline based on these asset names — they are hints, not file references.
```

**Continuity rules:**
- `continuity_out` of scene N must match `continuity_in` of scene N+1
- Shared visual elements should use identical styling constants
- Color palette must be consistent across all scenes (defined in `shared_style`)

**Pacing rules:**
- `text_elements` lists each text block with its approximate word count — used by workers to calculate reading pauses
- `estimated_reading_pauses` is the total seconds of `self.wait()` needed for reading time (sum of `max(2, words / 3)` for each text block)
- `duration` must be >= animation time + `estimated_reading_pauses` — increase duration if needed to fit reading time
- Workers use the formula: **`self.wait(max(2, word_count / 3))`** after every text appearance

---

### Step 4: Scene Generation (Sequential)

For each scene, spawn a worker using the agent CLI. Workers run **sequentially** in V1.

**The dispatcher reads and injects relevant library file contents into each worker prompt.** Workers are independent agent subprocesses and cannot access the skill directory.

**Library injection strategy** — inject only files relevant to the scene type:

| Scene template | Always injected | Conditionally injected |
|---------------|-----------------|----------------------|
| All types | `cheatsheet.md`, `style-guide.md`, `common-errors.md` | — |
| All types (if scene has `svg_assets`) | `svg-icons.md` | — |
| `basic` | — | `animations.md` |
| `math` | — | `text-and-math.md`, `animations.md` |
| `graph` | — | `animations.md` |
| `code` | — | `text-and-math.md` |

**For each scene N:**

1. Build the worker prompt:

```bash
SKILL_DIR="$(dirname "$(readlink -f "$0")" 2>/dev/null || cd "$(dirname "$0")" && pwd)"

# Always-injected library files
CHEATSHEET="$(cat "$SKILL_DIR/library/cheatsheet.md")"
STYLE_GUIDE="$(cat "$SKILL_DIR/library/style-guide.md")"
COMMON_ERRORS="$(cat "$SKILL_DIR/library/common-errors.md")"

# SVG icons reference — injected when scene has svg_assets
HAS_SVG_ASSETS=$(python3 -c "
import json
story = json.load(open('.manimate/story.json'))
assets = story['scenes'][$((N-1))].get('svg_assets', [])
print('yes' if assets else 'no')
")
SVG_ICONS_REF=""
if [ "$HAS_SVG_ASSETS" = "yes" ]; then
  SVG_ICONS_REF="### SVG Icons Reference
$(cat "$SKILL_DIR/library/svg-icons.md")"
fi

# Read scene metadata
SCENE_TEMPLATE_NAME=$(python3 -c "
import json
story = json.load(open('.manimate/story.json'))
scene = story['scenes'][$((N-1))]
print(scene.get('template', 'basic'))
")

# Conditionally-injected library files based on scene type
EXTRA_REFS=""
case "$SCENE_TEMPLATE_NAME" in
  basic)
    EXTRA_REFS="### Animation Patterns
$(cat "$SKILL_DIR/library/animations.md")"
    ;;
  math)
    EXTRA_REFS="### Animation Patterns
$(cat "$SKILL_DIR/library/animations.md")

### Text & Math
$(cat "$SKILL_DIR/library/text-and-math.md")"
    ;;
  graph)
    EXTRA_REFS="### Animation Patterns
$(cat "$SKILL_DIR/library/animations.md")"
    ;;
  code)
    EXTRA_REFS="### Text & Math (Code Patterns)
$(cat "$SKILL_DIR/library/text-and-math.md")"
    ;;
esac

# Read the appropriate template
TEMPLATE="$(cat "$SKILL_DIR/templates/${SCENE_TEMPLATE_NAME}.py")"

# Read scene spec + shared style + latex flag
SCENE_SPEC=$(python3 -c "
import json
story = json.load(open('.manimate/story.json'))
scene = story['scenes'][$((N-1))]
scene['shared_style'] = story['shared_style']
scene['latex_available'] = story.get('latex_available', False)
print(json.dumps(scene, indent=2))
")

SCENE_CLASS=$(python3 -c "
import json
story = json.load(open('.manimate/story.json'))
print(story['scenes'][$((N-1))]['scene_class'])
")

DURATION=$(python3 -c "
import json
story = json.load(open('.manimate/story.json'))
print(story['scenes'][$((N-1))].get('duration', 8))
")

# LaTeX instruction
LATEX_RULE=""
if [ "$LATEX_AVAILABLE" = "false" ]; then
  LATEX_RULE="11. LaTeX is NOT available. Do NOT use MathTex or Tex. Use Text() for all text including math. Render equations as Unicode."
else
  LATEX_RULE="11. If LaTeX is needed, use MathTex (not Tex) for math expressions"
fi

cat > /tmp/manimate-scene-$(printf "%02d" $N)-prompt.txt << PROMPT_EOF
You are generating a Python file for a Manim animation scene.

## Scene Specification
$SCENE_SPEC

## Template (use as starting point)
\`\`\`python
$TEMPLATE
\`\`\`

## Manim Reference

### API Cheatsheet
$CHEATSHEET

### Style Guide
$STYLE_GUIDE

$EXTRA_REFS

$SVG_ICONS_REF

### Common Errors to Avoid
$COMMON_ERRORS

## Rules

1. Use \`from manim import *\` (NOT manimlib — that is ManimGL)
2. Define exactly ONE Scene subclass named \`${SCENE_CLASS}\`
3. All animation logic goes in the \`construct(self)\` method
4. Use self.play() for animations, self.wait() for pauses
5. Use the shared_style colors/sizes for consistency across scenes
6. Inline all constants — do NOT import from external modules
7. Keep the scene self-contained (no file I/O, no network)
8. Target duration: ~${DURATION}s (use self.wait() to pad if needed)
9. Use .animate syntax for simple property changes
10. Use Transform/ReplacementTransform for morphing between objects
$LATEX_RULE
12. For real-world concepts (servers, databases, users, documents, locks, etc.), generate a custom SVG icon instead of using a basic rectangle or circle. Use the svg_icon() helper and follow SVG rules from the reference docs. SVGs must use flat colors only — NO gradients, NO filters, NO <text> elements, NO stroke-dasharray. Use Manim Text() for all labels.
13. Define SVG strings as Python string constants at the top of the scene, write them via the svg_icon() helper. Keep SVGs simple with viewBox="0 0 80 100" or similar. Use colors from the shared_style palette.

## Text Pacing Rules (CRITICAL — text must be readable)

Every text element MUST stay on screen long enough to read. Apply these rules:

14. After EVERY Write(text) or FadeIn(text), add a reading pause:
    \`\`\`python
    self.wait(max(2, len("your text content".split()) / 3))
    \`\`\`
    This gives ~180 WPM reading speed with a 2-second minimum.

15. Title cards: display for at least 2 seconds before animating to corner/top
16. Key insight or annotation text: minimum 3 seconds on screen
17. NEVER use bare \`self.wait()\` after text — always calculate from word count
18. NEVER use \`self.wait(0.5)\` or \`self.wait(1)\` after text that has more than 3 words
19. Between conceptual sections, use \`self.wait(1.5)\` as a transition pause

Examples:
- Title "The Problem" (2 words) → \`self.wait(2)\` (minimum floor)
- "We need to find the target value in this sorted array" (11 words) → \`self.wait(max(2, 11/3))\` = \`self.wait(3.7)\`
- "Binary search eliminates half the remaining elements each step by comparing the target to the middle element" (16 words) → \`self.wait(max(2, 16/3))\` = \`self.wait(5.3)\`

## Output

Write ONLY the Python file to: .manimate/scenes/scene_$(printf "%02d" $N).py
No explanation, no markdown — just the Python file.
PROMPT_EOF
```

2. Spawn the worker (with timeout):

```bash
ENV_CMD="env"
if [ -n "$MANIMATE_AGENT_ENV_UNSET" ]; then
  IFS=',' read -ra UNSET_VARS <<< "$MANIMATE_AGENT_ENV_UNSET"
  for var in "${UNSET_VARS[@]}"; do
    [ -n "$var" ] && ENV_CMD="$ENV_CMD -u $var"
  done
fi

# 120s timeout for generation worker
if [ -n "$TIMEOUT_CMD" ]; then
  $TIMEOUT_CMD 120 $ENV_CMD $MANIMATE_AGENT_CLI \
    "$(cat /tmp/manimate-scene-$(printf "%02d" $N)-prompt.txt)"
else
  $ENV_CMD $MANIMATE_AGENT_CLI \
    "$(cat /tmp/manimate-scene-$(printf "%02d" $N)-prompt.txt)"
fi
```

3. Validate the generated file:

```bash
FILE=".manimate/scenes/scene_$(printf "%02d" $N).py"

if [ ! -f "$FILE" ]; then
  echo "Missing: $FILE"
  exit 1
fi

python3 -c "compile(open('$FILE').read(), '$FILE', 'exec')" 2>/dev/null || {
  echo "Syntax error in $FILE — will attempt fix during render"
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

---

### Step 5: Render & Error Recovery

For each scene, render with Manim. If rendering fails, feed the error back to a fix worker.

**Output path resolution**: Manim writes to structured subdirs. After each render, resolve the actual output path.

```bash
MAX_RETRIES=3
QUALITY_SUBDIR="1080p60"  # matches -qh

for N in $(seq 1 $TOTAL_SCENES); do
  FILE=".manimate/scenes/scene_$(printf "%02d" $N).py"
  SCENE_FILE="scene_$(printf "%02d" $N)"
  SCENE_CLASS=$(python3 -c "
import json
story = json.load(open('.manimate/story.json'))
print(story['scenes'][$((N-1))]['scene_class'])
  ")

  RETRY=0
  RENDER_SUCCESS=false

  while [ $RETRY -lt $MAX_RETRIES ]; do
    echo "Rendering scene $N ($SCENE_CLASS)..."

    RENDER_LOG=$(mktemp)
    RENDER_CMD="manim render scenes/${SCENE_FILE}.py $SCENE_CLASS \
        --renderer=cairo -qh --format=mp4 --disable_caching"

    if [ -n "$TIMEOUT_CMD" ]; then
      RENDER_CMD="$TIMEOUT_CMD 180 $RENDER_CMD"
    fi

    if cd .manimate && eval $RENDER_CMD 2>"$RENDER_LOG"; then
      cd ..

      EXPECTED_PATH=".manimate/media/videos/${SCENE_FILE}/${QUALITY_SUBDIR}/${SCENE_CLASS}.mp4"
      if [ -f "$EXPECTED_PATH" ]; then
        echo "  Scene $N rendered: $EXPECTED_PATH"
        RENDER_SUCCESS=true
      else
        FOUND_PATH=$(find .manimate/media/videos -name "${SCENE_CLASS}.mp4" 2>/dev/null | head -1)
        if [ -n "$FOUND_PATH" ]; then
          echo "  Scene $N rendered: $FOUND_PATH"
          RENDER_SUCCESS=true
        fi
      fi

      rm -f "$RENDER_LOG"
      if $RENDER_SUCCESS; then
        # Capture last-frame PNG
        manim render -ql -s --renderer=cairo --disable_caching \
          ".manimate/scenes/${SCENE_FILE}.py" "$SCENE_CLASS" 2>/dev/null || true
        LASTFRAME=$(find .manimate/media/images -name "*.png" -newer "$FILE" 2>/dev/null | head -1)
        if [ -n "$LASTFRAME" ]; then
          cp "$LASTFRAME" ".manimate/lastframes/scene_$(printf "%02d" $N).png"
        fi
        break
      fi
    else
      RENDER_EXIT=$?
      cd ..
    fi

    RETRY=$((RETRY + 1))
    ERROR_OUTPUT="$(cat "$RENDER_LOG")"
    rm -f "$RENDER_LOG"

    if [ $RETRY -ge $MAX_RETRIES ]; then
      echo "  Scene $N failed after $MAX_RETRIES attempts"
      break
    fi

    echo "  Render failed (attempt $RETRY/$MAX_RETRIES). Fixing..."

    CURRENT_CODE="$(cat "$FILE")"

    cat > /tmp/manimate-fix-$(printf "%02d" $N)-prompt.txt << FIX_EOF
Fix this Manim scene. The render failed with the following error:

## Error Output
\`\`\`
$ERROR_OUTPUT
\`\`\`

## Current Code
\`\`\`python
$CURRENT_CODE
\`\`\`

## Common Errors Reference
$COMMON_ERRORS

## Rules
1. Use \`from manim import *\` (NOT manimlib)
2. The Scene class must be named \`$SCENE_CLASS\`
3. Fix the error while preserving the animation intent
4. If LaTeX is failing, switch to Text() as fallback
5. The file will be rendered with --renderer=cairo (no OpenGL)

Write the corrected Python file to: $FILE
FIX_EOF

    if [ -n "$TIMEOUT_CMD" ]; then
      $TIMEOUT_CMD 90 $ENV_CMD $MANIMATE_AGENT_CLI \
        "$(cat /tmp/manimate-fix-$(printf "%02d" $N)-prompt.txt)"
    else
      $ENV_CMD $MANIMATE_AGENT_CLI \
        "$(cat /tmp/manimate-fix-$(printf "%02d" $N)-prompt.txt)"
    fi
  done
done
```

---

### Step 6: Stitch & Convert

Run the render script to concatenate scene videos and convert to GIF:

```bash
bash "$SKILL_DIR/scripts/render.sh" \
  --scenes-dir .manimate/scenes \
  --media-dir .manimate/media \
  --output-dir .manimate/output \
  --format "$FORMAT" \
  --story-file .manimate/story.json
```

---

### Step 7: Report

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

### Step 8: Visual Validation (Optional)

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

If the user accepts, re-run Steps 4-5 for the failed scenes only, then re-stitch in Step 6 and re-validate.

> **Note**: This step uses only the agent's built-in image reading capability — no external dependencies required.

---

## Component Library Reference

When generating scenes, the dispatcher reads these files and injects their contents into worker prompts:

| File | Purpose | Used by |
|------|---------|---------|
| `library/cheatsheet.md` | Manim API quick reference | All scene types |
| `library/style-guide.md` | Color palette, font sizes, timing | All scene types |
| `library/svg-icons.md` | SVG icon catalog, helper function, design rules | Scenes with `svg_assets` |
| `library/animations.md` | Animation patterns with code | basic, math, graph |
| `library/text-and-math.md` | Text, MathTex, Code patterns | math, code |
| `library/common-errors.md` | Known pitfalls and fixes | All scene types |

## Key Conventions

1. **ManimCE only** — `from manim import *` (never `manimlib`). Cairo renderer for headless safety.
2. **One Scene class per file** — each scene is a separate `.py` file for isolated error recovery.
3. **Sequential generation** — workers run one at a time for V1. Simpler to debug.
4. **Shared style via story.json** — colors, font sizes, and background injected into every worker prompt for consistency.
5. **LaTeX fallback** — if LaTeX is unavailable, workers use `Text()` instead of `MathTex()`.
6. **Timeout wrappers** — 120s for generation, 180s for render, 90s for fix workers.
7. **Error recovery** — render failures are parsed and fed back to fix workers. Max 3 retries per scene.
8. **Selective library injection** — only relevant docs per scene type to keep prompts focused.
9. **Generation tier for creation, review tier for QC** — use your agent's most capable model for generation.
10. **SVG-forward visuals** — for real-world concepts (servers, users, databases, etc.), workers generate custom inline SVG icons instead of basic shapes. This is manimate's key visual differentiator.
