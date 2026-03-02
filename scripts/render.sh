#!/bin/bash
# Render pipeline: discover scene MP4s -> re-encode + concat -> convert to GIF
# Usage: ./render.sh [options]
#
# Options:
#   --scenes-dir DIR     Directory containing scene_*.py files
#   --media-dir DIR      Manim's media output directory
#   --output-dir DIR     Directory for final output files
#   --format FORMAT      Output format: gif, mp4, both (default: both)
#   --story-file FILE    Path to story.json

set -e

# Defaults
SCENES_DIR=".manimate/scenes"
MEDIA_DIR=".manimate/media"
OUTPUT_DIR=".manimate/output"
FORMAT="mp4"
STORY_FILE=".manimate/story.json"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --scenes-dir)  SCENES_DIR="$2"; shift 2 ;;
    --media-dir)   MEDIA_DIR="$2"; shift 2 ;;
    --output-dir)  OUTPUT_DIR="$2"; shift 2 ;;
    --format)      FORMAT="$2"; shift 2 ;;
    --story-file)  STORY_FILE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Validate
if [ ! -f "$STORY_FILE" ]; then
  echo "Error: story file not found: $STORY_FILE"
  exit 1
fi

command -v ffmpeg >/dev/null 2>&1 || { echo "Error: ffmpeg not found"; exit 1; }

mkdir -p "$OUTPUT_DIR"

# Read scene count
TOTAL_SCENES=$(python3 -c "import json; print(len(json.load(open('$STORY_FILE'))['scenes']))")

if [ "$TOTAL_SCENES" -eq 0 ]; then
  echo "Error: no scenes in story.json"
  exit 1
fi

echo "Stitching $TOTAL_SCENES scene(s)..."

# Discover rendered scene MP4s
SCENE_VIDEOS=()
for N in $(seq 1 $TOTAL_SCENES); do
  SCENE_FILE="scene_$(printf "%02d" $N)"
  SCENE_CLASS=$(python3 -c "
import json
story = json.load(open('$STORY_FILE'))
print(story['scenes'][$((N-1))]['scene_class'])
  ")

  # Try expected path first, then search
  EXPECTED="$MEDIA_DIR/videos/$SCENE_FILE/720p30/${SCENE_CLASS}.mp4"
  if [ -f "$EXPECTED" ]; then
    VIDEO="$EXPECTED"
  else
    VIDEO=$(find "$MEDIA_DIR/videos" -name "${SCENE_CLASS}.mp4" 2>/dev/null | head -1)
  fi

  if [ -z "$VIDEO" ] || [ ! -f "$VIDEO" ]; then
    echo "Error: could not find rendered video for scene $N ($SCENE_CLASS)"
    exit 1
  fi
  SCENE_VIDEOS+=("$VIDEO")
  echo "  Scene $N: $VIDEO"
done

# Single scene — just copy
if [ ${#SCENE_VIDEOS[@]} -eq 1 ]; then
  cp "${SCENE_VIDEOS[0]}" "$OUTPUT_DIR/animation.mp4"
  echo "  Single scene — copied directly"
else
  # Create concat filelist
  FILELIST=$(mktemp)
  for v in "${SCENE_VIDEOS[@]}"; do
    echo "file '$(cd "$(dirname "$v")" && pwd)/$(basename "$v")'" >> "$FILELIST"
  done

  # Re-encode and concatenate (handles codec parameter mismatches)
  FFMPEG_LOG=$(mktemp)
  if ffmpeg -y -f concat -safe 0 -i "$FILELIST" \
    -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p \
    -movflags +faststart \
    "$OUTPUT_DIR/animation.mp4" 2>"$FFMPEG_LOG"; then
    echo "  MP4 stitched"
  else
    echo "  MP4 stitching failed. ffmpeg output:"
    cat "$FFMPEG_LOG"
    rm -f "$FFMPEG_LOG" "$FILELIST"
    exit 1
  fi
  rm -f "$FFMPEG_LOG" "$FILELIST"
fi

MP4_SIZE=$(du -h "$OUTPUT_DIR/animation.mp4" | cut -f1)
echo "  MP4: $OUTPUT_DIR/animation.mp4 ($MP4_SIZE)"

# Convert to GIF if requested
if [[ "$FORMAT" == "gif" || "$FORMAT" == "both" ]]; then
  echo "Converting to GIF..."
  FFMPEG_LOG=$(mktemp)
  if ffmpeg -y -i "$OUTPUT_DIR/animation.mp4" \
    -filter_complex "[0:v]fps=12,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=196:stats_mode=diff[p];[b][p]paletteuse=dither=floyd_steinberg" \
    -loop 0 "$OUTPUT_DIR/animation.gif" 2>"$FFMPEG_LOG"; then
    GIF_SIZE=$(du -h "$OUTPUT_DIR/animation.gif" | cut -f1)
    echo "  GIF: $OUTPUT_DIR/animation.gif ($GIF_SIZE)"
  else
    echo "  GIF conversion failed. ffmpeg output:"
    cat "$FFMPEG_LOG"
    rm -f "$FFMPEG_LOG"
    exit 1
  fi
  rm -f "$FFMPEG_LOG"
fi

echo ""
echo "Animation complete!"
echo "   Scenes: $TOTAL_SCENES"
[[ "$FORMAT" != "gif" ]] && echo "   MP4: $OUTPUT_DIR/animation.mp4"
[[ "$FORMAT" == "gif" || "$FORMAT" == "both" ]] && echo "   GIF: $OUTPUT_DIR/animation.gif"
