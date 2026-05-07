#!/usr/bin/env bash
# install.sh - install higgs-vids skill + Claude slash commands globally.
#
# Checks the local machine for required tools, then symlinks the skill and
# slash commands into ~/.claude/ so they work in any Claude Code session.
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

OK="${GREEN}ok${NC}"
WARN="${YELLOW}warn${NC}"
FAIL="${RED}missing${NC}"
MISSING=()

have() {
  command -v "$1" >/dev/null 2>&1
}

check_required_cmd() {
  local cmd="$1"
  local install_hint="$2"
  if have "$cmd"; then
    echo -e "  [$OK] $cmd: $(command -v "$cmd")"
  else
    echo -e "  [$FAIL] $cmd"
    MISSING+=("$cmd - $install_hint")
  fi
}

check_optional_cmd() {
  local cmd="$1"
  local install_hint="$2"
  if have "$cmd"; then
    echo -e "  [$OK] $cmd: $(command -v "$cmd")"
  else
    echo -e "  [$WARN] $cmd not found ($install_hint)"
  fi
}

check_pillow() {
  if have python3 && python3 -c 'import PIL' >/dev/null 2>&1; then
    local version
    version="$(python3 -c 'import PIL; print(PIL.__version__)' 2>/dev/null || true)"
    echo -e "  [$OK] Pillow: $version"
  else
    echo -e "  [$WARN] Pillow not available to python3 (needed for moodboard composition)"
    echo "         Install when needed: python3 -m pip install Pillow"
  fi
}

check_higgs_version() {
  if have higgs; then
    local version
    version="$(higgs version 2>/dev/null || true)"
    if [ -n "$version" ]; then
      echo -e "  [$OK] higgs version: $version"
      if ! echo "$version" | grep -q '0\.1\.28'; then
        echo -e "  [$WARN] Skill was validated against higgs 0.1.28; run /higgsfield-init after install."
      fi
    else
      echo -e "  [$WARN] higgs exists but version check failed; run /higgsfield-init after install."
    fi
  fi
}

check_higgs_auth() {
  if have higgs; then
    if higgs --json account status >/dev/null 2>&1; then
      echo -e "  [$OK] higgs auth: signed in"
    else
      echo -e "  [$WARN] higgs auth: not signed in or API unreachable"
      echo "         Run after install: higgs auth login"
    fi
  fi
}

echo "Installing higgs-vids globally"
echo "  Source: $REPO_DIR"
echo "  Target: $CLAUDE_DIR"
echo

echo "Preflight checks"
check_required_cmd git "install Git, then clone this repo again if needed"
check_required_cmd node "install Node.js from https://nodejs.org/ or with your package manager"
check_required_cmd npm "install Node.js/npm"
check_required_cmd higgs "npm install -g @higgsfield/cli"
check_required_cmd jq "macOS: brew install jq | Debian/Ubuntu/WSL: sudo apt install jq"
check_required_cmd ffmpeg "macOS: brew install ffmpeg | Debian/Ubuntu/WSL: sudo apt install ffmpeg"
check_required_cmd python3 "install Python 3"
check_optional_cmd claude "install Claude Code if you want slash commands available in the terminal"
check_higgs_version
check_pillow
check_higgs_auth

if [ ${#MISSING[@]} -gt 0 ]; then
  echo
  echo -e "${YELLOW}Setup is not complete yet.${NC}"
  echo "Install the missing requirements, then re-run:"
  echo "  bash install.sh"
  echo
  echo "Missing:"
  for item in "${MISSING[@]}"; do
    echo "  - $item"
  done
  echo
  echo "The skill and slash commands will still be linked now so Claude Code can"
  echo "help finish setup, but generation will not work until the missing tools exist."
  echo
fi

mkdir -p "$SKILLS_DIR" "$COMMANDS_DIR"

# Skill bundle
SKILL_SRC="$REPO_DIR/skill/higgsfield-autopilot"
SKILL_LINK="$SKILLS_DIR/higgsfield-autopilot"
COMMANDS_SRC="$REPO_DIR/commands/claude"

if [ -L "$SKILL_LINK" ]; then
  CURRENT_TARGET="$(readlink "$SKILL_LINK")"
  if [ "$CURRENT_TARGET" = "$SKILL_SRC" ]; then
    echo -e "  [$OK] skill already linked: $SKILL_LINK"
  else
    echo -e "  [$WARN] skill symlink points elsewhere: $CURRENT_TARGET"
    echo "    Re-pointing to $SKILL_SRC"
    rm "$SKILL_LINK"
    ln -s "$SKILL_SRC" "$SKILL_LINK"
    echo -e "  [$OK] re-linked: $SKILL_LINK"
  fi
elif [ -e "$SKILL_LINK" ]; then
  echo -e "  [${RED}fail${NC}] $SKILL_LINK exists and is not a symlink. Remove or rename it manually."
  exit 1
else
  ln -s "$SKILL_SRC" "$SKILL_LINK"
  echo -e "  [$OK] linked skill: $SKILL_LINK -> $SKILL_SRC"
fi

# Slash commands
LINKED_COMMANDS=()
SKIPPED_COMMANDS=()
shopt -s nullglob
for cmd in "$COMMANDS_SRC"/*.md; do
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
for c in "${LINKED_COMMANDS[@]}"; do echo -e "    [$OK] $c"; done
if [ ${#SKIPPED_COMMANDS[@]} -gt 0 ]; then
  for c in "${SKIPPED_COMMANDS[@]}"; do echo -e "    [$WARN] $c"; done
  echo
  echo -e "  [$WARN] Skipped commands had real files (not symlinks) at the target."
  echo "    Resolve manually if you want them linked."
fi

echo
echo -e "${GREEN}Done.${NC} ${#LINKED_COMMANDS[@]} commands + 1 skill linked."
echo
echo "Restart Claude Code to pick up new commands. Updates to files in"
echo "  $REPO_DIR"
echo "propagate automatically; no need to re-run this script after edits."
echo
echo "Next in Claude Code:"
echo "  /higgsfield-init"
echo
echo "To uninstall: bash $REPO_DIR/uninstall.sh"
