#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="animate"

echo "Installing animate skill..."

INSTALLED=0

# Claude Code
if [ -d "$HOME/.claude" ] || command -v claude >/dev/null 2>&1; then
  CLAUDE_DIR="$HOME/.claude/skills/$SKILL_NAME"
  mkdir -p "$(dirname "$CLAUDE_DIR")"
  ln -sfn "$SCRIPT_DIR" "$CLAUDE_DIR"
  echo "  Linked to Claude Code: $CLAUDE_DIR"
  INSTALLED=$((INSTALLED + 1))
fi

# Codex / OpenAI
if [ -d "$HOME/.codex" ] || command -v codex >/dev/null 2>&1; then
  CODEX_DIR="$HOME/.codex/skills/$SKILL_NAME"
  mkdir -p "$(dirname "$CODEX_DIR")"
  ln -sfn "$SCRIPT_DIR" "$CODEX_DIR"
  echo "  Linked to Codex: $CODEX_DIR"
  INSTALLED=$((INSTALLED + 1))
fi

# Generic agents
AGENTS_DIR="$HOME/.agents/skills/$SKILL_NAME"
mkdir -p "$(dirname "$AGENTS_DIR")"
ln -sfn "$SCRIPT_DIR" "$AGENTS_DIR"
echo "  Linked to generic agents: $AGENTS_DIR"
INSTALLED=$((INSTALLED + 1))

echo ""
echo "animate installed! ($INSTALLED agent location(s))"
echo ""
echo "Usage:  /animate \"explain how binary search works\""
echo ""
echo "Dependencies: python3, manim (pip install manim), ffmpeg"
