#!/usr/bin/env bash
# uninstall.sh — remove higgs-vids global symlinks.
#
# The source repo and its files are NOT touched — this only removes the
# symlinks under ~/.claude/. To fully reinstall later, just run install.sh
# again.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

GREEN='\033[32m'
YELLOW='\033[33m'
NC='\033[0m'

echo "Removing higgs-vids global symlinks"
echo "  (source repo at $REPO_DIR is untouched)"
echo

REMOVED=0

# Skill
SKILL_LINK="$CLAUDE_DIR/skills/higgsfield-autopilot"
if [ -L "$SKILL_LINK" ]; then
  TARGET="$(readlink "$SKILL_LINK")"
  if [ "$TARGET" = "$REPO_DIR/skill/higgsfield-autopilot" ]; then
    rm "$SKILL_LINK"
    echo -e "  ${GREEN}✓${NC} removed $SKILL_LINK"
    REMOVED=$((REMOVED+1))
  else
    echo -e "  ${YELLOW}!${NC} skill symlink points elsewhere ($TARGET) — leaving intact"
  fi
fi

# Slash commands
shopt -s nullglob
for cmd in "$REPO_DIR"/.claude/commands/*.md; do
  name="$(basename "$cmd")"
  link="$CLAUDE_DIR/commands/$name"
  if [ -L "$link" ]; then
    TARGET="$(readlink "$link")"
    if [ "$TARGET" = "$cmd" ]; then
      rm "$link"
      echo -e "  ${GREEN}✓${NC} removed $link"
      REMOVED=$((REMOVED+1))
    fi
  fi
done
shopt -u nullglob

echo
echo -e "${GREEN}✓${NC} Done. $REMOVED symlinks removed."
echo "  (To reinstall: bash $REPO_DIR/install.sh)"
