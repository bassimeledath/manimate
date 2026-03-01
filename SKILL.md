---
name: animate
description: Generate diagram and animation videos from natural language descriptions using Manim. Outputs MP4 and GIF.
---

# /animate — Manim Animation Video Maker

Generate diagram and animation videos from natural language descriptions using Manim. Outputs MP4 and GIF files.

## Usage

```
/animate "explain how binary search works"
/animate "show the Pythagorean theorem proof"
/animate "visualize bubble sort step by step"
```

## Pipeline

When the user invokes `/animate`, execute these steps in order:

---

### Step 1: Parameter Inference

Parse the user's prompt and infer rendering parameters:

| Parameter | Range | Default | How to infer |
|-----------|-------|---------|--------------|
| `scenes` | 1-6 | 2 | Count distinct concepts/steps/phases in the prompt |
| `quality` | l/m/h | m | Default medium; use high for math-heavy or final delivery |
| `format` | gif/mp4/both | both | Default both unless user specifies |
| `style` | educational/minimal/cinematic | educational | Infer from the tone/subject |
| `duration_per_scene` | 5-15s | 8 | Longer for complex concepts, shorter for simple transitions |

Write to `.animate/params.json`:

```json
{
  "prompt": "explain how binary search works",
  "scenes": 3,
  "quality": "m",
  "format": "both",
  "style": "educational",
  "duration_per_scene": 8
}
```

Write `.animate/manim.cfg`:

```ini
[CLI]
quality = medium_quality
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
ANIMATE_AGENT_CLI="${ANIMATE_AGENT_CLI:-}"
if [ -z "$ANIMATE_AGENT_CLI" ]; then
  if command -v claude >/dev/null 2>&1; then
    ANIMATE_AGENT_CLI="claude -p --dangerously-skip-permissions"
    ANIMATE_AGENT_ENV_UNSET="CLAUDE_CODE_ENTRYPOINT,CLAUDECODE"
  elif command -v codex >/dev/null 2>&1; then
    ANIMATE_AGENT_CLI="codex --quiet --full-auto"
    ANIMATE_AGENT_ENV_UNSET=""
  else
    echo "No supported agent CLI found. Set ANIMATE_AGENT_CLI env var."
    exit 1
  fi
fi
AGENT_BIN=$(echo "$ANIMATE_AGENT_CLI" | awk '{print $1}')
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
rm -rf .animate
mkdir -p .animate/scenes .animate/lastframes .animate/output
```

> **Pipeline-wide LATEX_AVAILABLE flag**: When `false`, worker prompts explicitly instruct the agent: "Do NOT use MathTex or Tex — use Text() for all text, including math expressions. Render equations as Unicode or ASCII."

---

### Step 3: Story Decomposition

Break the prompt into scenes. Each scene specifies visual elements, animations, and narrative arc.

Write `.animate/story.json`:

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
      "scene_class": "TheProblem",
      "duration": 8,
      "template": "basic",
      "continuity_in": null,
      "continuity_out": "Array remains visible, target highlighted"
    }
  ],
  "shared_style": {
    "background_color": "#1e1e2e",
    "accent_color": "BLUE",
    "highlight_color": "YELLOW",
    "text_color": "WHITE",
    "font_size_title": 48,
    "font_size_body": 32
  },
  "latex_available": true
}
```

**Continuity rules:**
- `continuity_out` of scene N must match `continuity_in` of scene N+1
- Shared visual elements should use identical styling constants
- Color palette must be consistent across all scenes (defined in `shared_style`)

---

### Step 4: Scene Generation (Sequential)

For each scene, spawn a worker using the agent CLI. Workers run **sequentially** in V1.

**The dispatcher reads and injects relevant library file contents into each worker prompt.** Workers are independent agent subprocesses and cannot access the skill directory.

**Library injection strategy** — inject only files relevant to the scene type:

| Scene template | Always injected | Conditionally injected |
|---------------|-----------------|----------------------|
| All types | `cheatsheet.md`, `style-guide.md`, `common-errors.md` | — |
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

# Read scene metadata
SCENE_TEMPLATE_NAME=$(python3 -c "
import json
story = json.load(open('.animate/story.json'))
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
story = json.load(open('.animate/story.json'))
scene = story['scenes'][$((N-1))]
scene['shared_style'] = story['shared_style']
scene['latex_available'] = story.get('latex_available', False)
print(json.dumps(scene, indent=2))
")

SCENE_CLASS=$(python3 -c "
import json
story = json.load(open('.animate/story.json'))
print(story['scenes'][$((N-1))]['scene_class'])
")

DURATION=$(python3 -c "
import json
story = json.load(open('.animate/story.json'))
print(story['scenes'][$((N-1))].get('duration', 8))
")

# LaTeX instruction
LATEX_RULE=""
if [ "$LATEX_AVAILABLE" = "false" ]; then
  LATEX_RULE="11. LaTeX is NOT available. Do NOT use MathTex or Tex. Use Text() for all text including math. Render equations as Unicode."
else
  LATEX_RULE="11. If LaTeX is needed, use MathTex (not Tex) for math expressions"
fi

cat > /tmp/animate-scene-$(printf "%02d" $N)-prompt.txt << PROMPT_EOF
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

## Output

Write ONLY the Python file to: .animate/scenes/scene_$(printf "%02d" $N).py
No explanation, no markdown — just the Python file.
PROMPT_EOF
```

2. Spawn the worker (with timeout):

```bash
ENV_CMD="env"
if [ -n "$ANIMATE_AGENT_ENV_UNSET" ]; then
  IFS=',' read -ra UNSET_VARS <<< "$ANIMATE_AGENT_ENV_UNSET"
  for var in "${UNSET_VARS[@]}"; do
    [ -n "$var" ] && ENV_CMD="$ENV_CMD -u $var"
  done
fi

# 120s timeout for generation worker
if [ -n "$TIMEOUT_CMD" ]; then
  $TIMEOUT_CMD 120 $ENV_CMD $ANIMATE_AGENT_CLI \
    "$(cat /tmp/animate-scene-$(printf "%02d" $N)-prompt.txt)"
else
  $ENV_CMD $ANIMATE_AGENT_CLI \
    "$(cat /tmp/animate-scene-$(printf "%02d" $N)-prompt.txt)"
fi
```

3. Validate the generated file:

```bash
FILE=".animate/scenes/scene_$(printf "%02d" $N).py"

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
QUALITY_SUBDIR="720p30"  # matches -qm

for N in $(seq 1 $TOTAL_SCENES); do
  FILE=".animate/scenes/scene_$(printf "%02d" $N).py"
  SCENE_FILE="scene_$(printf "%02d" $N)"
  SCENE_CLASS=$(python3 -c "
import json
story = json.load(open('.animate/story.json'))
print(story['scenes'][$((N-1))]['scene_class'])
  ")

  RETRY=0
  RENDER_SUCCESS=false

  while [ $RETRY -lt $MAX_RETRIES ]; do
    echo "Rendering scene $N ($SCENE_CLASS)..."

    RENDER_LOG=$(mktemp)
    RENDER_CMD="manim render scenes/${SCENE_FILE}.py $SCENE_CLASS \
        --renderer=cairo -qm --format=mp4 --disable_caching"

    if [ -n "$TIMEOUT_CMD" ]; then
      RENDER_CMD="$TIMEOUT_CMD 180 $RENDER_CMD"
    fi

    if cd .animate && eval $RENDER_CMD 2>"$RENDER_LOG"; then
      cd ..

      EXPECTED_PATH=".animate/media/videos/${SCENE_FILE}/${QUALITY_SUBDIR}/${SCENE_CLASS}.mp4"
      if [ -f "$EXPECTED_PATH" ]; then
        echo "  Scene $N rendered: $EXPECTED_PATH"
        RENDER_SUCCESS=true
      else
        FOUND_PATH=$(find .animate/media/videos -name "${SCENE_CLASS}.mp4" 2>/dev/null | head -1)
        if [ -n "$FOUND_PATH" ]; then
          echo "  Scene $N rendered: $FOUND_PATH"
          RENDER_SUCCESS=true
        fi
      fi

      rm -f "$RENDER_LOG"
      if $RENDER_SUCCESS; then
        # Capture last-frame PNG
        manim render -ql -s --renderer=cairo --disable_caching \
          ".animate/scenes/${SCENE_FILE}.py" "$SCENE_CLASS" 2>/dev/null || true
        LASTFRAME=$(find .animate/media/images -name "*.png" -newer "$FILE" 2>/dev/null | head -1)
        if [ -n "$LASTFRAME" ]; then
          cp "$LASTFRAME" ".animate/lastframes/scene_$(printf "%02d" $N).png"
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

    cat > /tmp/animate-fix-$(printf "%02d" $N)-prompt.txt << FIX_EOF
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
      $TIMEOUT_CMD 90 $ENV_CMD $ANIMATE_AGENT_CLI \
        "$(cat /tmp/animate-fix-$(printf "%02d" $N)-prompt.txt)"
    else
      $ENV_CMD $ANIMATE_AGENT_CLI \
        "$(cat /tmp/animate-fix-$(printf "%02d" $N)-prompt.txt)"
    fi
  done
done
```

---

### Step 6: Stitch & Convert

Run the render script to concatenate scene videos and convert to GIF:

```bash
bash "$SKILL_DIR/scripts/render.sh" \
  --scenes-dir .animate/scenes \
  --media-dir .animate/media \
  --output-dir .animate/output \
  --format "$FORMAT" \
  --story-file .animate/story.json
```

---

### Step 7: Report

```
Animation complete!

Prompt: "explain how binary search works"
Scenes: 3 (all rendered successfully)
Duration: 28s (8s + 12s + 8s)
Quality: 720p @ 30fps
Renderer: cairo

Output:
  MP4: .animate/output/animation.mp4 (1.2MB)
  GIF: .animate/output/animation.gif (3.4MB)
  Last-frame previews: .animate/lastframes/
```

---

## Component Library Reference

When generating scenes, the dispatcher reads these files and injects their contents into worker prompts:

| File | Purpose | Used by |
|------|---------|---------|
| `library/cheatsheet.md` | Manim API quick reference | All scene types |
| `library/style-guide.md` | Color palette, font sizes, timing | All scene types |
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
