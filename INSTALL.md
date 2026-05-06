# Install Higgs Vids

This repo is designed so a non-technical user can hand it to Claude Code and let the agent guide setup. A browser sign-in and a few approved installs may still be required because Higgsfield auth and system dependencies live outside this repo.

## Claude Code Setup

Paste this into Claude Code:

```text
Clone https://github.com/benwmerritt/higgs-vids, read its README.md and INSTALL.md, run bash install.sh, and walk me through any missing setup. Do not generate content yet. Once setup passes, run /higgsfield-init.
```

Claude should:

1. Clone the repo.
2. Run `bash install.sh`.
3. Tell you exactly what is missing, if anything.
4. Ask you to sign in with `higgs auth login` if Higgsfield auth is not ready.
5. Run `/higgsfield-init` after Claude Code restarts or reloads slash commands.

## Manual Setup

```bash
git clone https://github.com/benwmerritt/higgs-vids.git
cd higgs-vids
bash install.sh
```

If the installer reports missing tools, install them and re-run `bash install.sh`.

Common installs:

```bash
npm install -g @higgsfield/cli
brew install jq ffmpeg
python3 -m pip install Pillow
higgs auth login
```

On Debian, Ubuntu, or WSL:

```bash
sudo apt update
sudo apt install jq ffmpeg python3 python3-pip
npm install -g @higgsfield/cli
python3 -m pip install Pillow
higgs auth login
```

## What The Installer Does

- Checks for `git`, `node`, `npm`, `higgs`, `jq`, `ffmpeg`, `python3`, and Pillow.
- Checks the installed Higgsfield CLI version and auth state.
- Symlinks `skill/higgsfield-autopilot/` into `~/.claude/skills/`.
- Symlinks `.claude/commands/*.md` into `~/.claude/commands/`.
- Leaves private data out of git. Brand profiles, presets, and generated runs are ignored.

## First Verification

After setup:

```text
/higgsfield-init
/higgsfield-test 1
```

Stage 1 is free. It checks auth, workspace, model pricing, and the agent workflow without generating media.

Do not run `/higgsfield-test 2`, `/higgsfield-test 3`, or `/higgsfield-make` until Stage 1 passes and you are ready to spend Higgsfield credits.

## Windows

Native Windows installs may fail because of an upstream Higgsfield CLI issue. Use WSL or Git Bash for now.

