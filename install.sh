#!/usr/bin/env bash
# install.sh — install higgs-vids skill + slash commands globally.
#
# Symlinks (not copies) the skill and commands into ~/.claude/, so:
#   • Slash commands (/higgsfield-init, /higgsfield-make, etc.) work in ANY
#     Claude Code session, not just when CWD is this repo.
#   • The skill is discoverable globally.
#   • Edits to files in this repo propagate IMMEDIATELY to the global install
#     (same files via symlink — no re-running install needed).
#
# Idempotent: safe to run multiple times. Skips existing symlinks.
# Refuses to overwrite real files at the target locations.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
SKILLS_DIR="$CLAUDE_DIR/skills"
COMMANDS_DIR="$CLAUDE_DIR/commands"

GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
NC='\033[0m'

echo "Installing higgs-vids globally"
echo "  Source: $REPO_DIR"
echo "  Target: $CLAUDE_DIR"
echo

mkdir -p "$SKILLS_DIR" "$COMMANDS_DIR"

# ─── Skill bundle ─────────────────────────────────────────
SKILL_SRC="$REPO_DIR/skill/higgsfield-autopilot"
SKILL_LINK="$SKILLS_DIR/higgsfield-autopilot"

if [ -L "$SKILL_LINK" ]; then
  CURRENT_TARGET="$(readlink "$SKILL_LINK")"
  if [ "$CURRENT_TARGET" = "$SKILL_SRC" ]; then
    echo -e "  ${GREEN}✓${NC} skill already linked: $SKILL_LINK"
  else
    echo -e "  ${YELLOW}!${NC} skill symlink points elsewhere: $CURRENT_TARGET"
    echo "    Re-pointing to $SKILL_SRC"
    rm "$SKILL_LINK"
    ln -s "$SKILL_SRC" "$SKILL_LINK"
    echo -e "  ${GREEN}✓${NC} re-linked: $SKILL_LINK"
  fi
elif [ -e "$SKILL_LINK" ]; then
  echo -e "  ${RED}✗${NC} $SKILL_LINK exists and is not a symlink. Remove or rename it manually."
  exit 1
else
  ln -s "$SKILL_SRC" "$SKILL_LINK"
  echo -e "  ${GREEN}✓${NC} linked skill: $SKILL_LINK -> $SKILL_SRC"
fi

# ─── Slash commands ───────────────────────────────────────
LINKED_COMMANDS=()
SKIPPED_COMMANDS=()
shopt -s nullglob
for cmd in "$REPO_DIR"/.claude/commands/*.md; do
  name="$(basename "$cmd")"
  link="$COMMANDS_DIR/$name"

  if [ -L "$link" ]; then
    CURRENT_TARGET="$(readlink "$link")"
    if [ "$CURRENT_TARGET" = "$cmd" ]; then
      LINKED_COMMANDS+=("$name (already linked)")
    else
      rm "$link"
      ln -s "$cmd" "$link"
      LINKED_COMMANDS+=("$name (re-linked from $CURRENT_TARGET)")
    fi
  elif [ -e "$link" ]; then
    SKIPPED_COMMANDS+=("$name (real file at target — skipped)")
  else
    ln -s "$cmd" "$link"
    LINKED_COMMANDS+=("$name (new link)")
  fi
done
shopt -u nullglob

echo
echo "  Slash commands:"
for c in "${LINKED_COMMANDS[@]}"; do echo -e "    ${GREEN}✓${NC} $c"; done
if [ ${#SKIPPED_COMMANDS[@]} -gt 0 ]; then
  for c in "${SKIPPED_COMMANDS[@]}"; do echo -e "    ${YELLOW}!${NC} $c"; done
  echo
  echo -e "  ${YELLOW}!${NC} Skipped commands had real files (not symlinks) at the target."
  echo "    Resolve manually if you want them linked."
fi

# ─── Done ─────────────────────────────────────────────────
echo
echo -e "${GREEN}✓${NC} Done. ${#LINKED_COMMANDS[@]} commands + 1 skill linked."
echo
echo "Restart Claude Code to pick up new commands. Updates to files in"
echo "  $REPO_DIR"
echo "propagate automatically — no need to re-run this script."
echo
echo "To uninstall: bash $REPO_DIR/uninstall.sh"
