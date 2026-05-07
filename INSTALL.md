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
4. Ask you to restart or reload Claude Code if slash commands are not visible yet.
5. Run `/higgsfield-init`. That command handles Higgsfield sign-in after your explicit consent.

## Manual Setup

<details>
<summary>Manual install commands</summary>

```bash
git clone https://github.com/benwmerritt/higgs-vids.git
cd higgs-vids
bash install.sh
```

</details>

If the installer reports missing tools, install them and re-run `bash install.sh`.

Common installs:

<details>
<summary>Dependency commands</summary>

```bash
npm install -g @higgsfield/cli
brew install jq ffmpeg
python3 -m pip install Pillow
```

Do not run `higgs auth login` manually unless you want to. `/higgsfield-init` can run it for you after asking.

</details>

On Debian, Ubuntu, or WSL:

<details>
<summary>Debian, Ubuntu, or WSL commands</summary>

```bash
sudo apt update
sudo apt install jq ffmpeg python3 python3-pip
npm install -g @higgsfield/cli
python3 -m pip install Pillow
```

Do not run `higgs auth login` manually unless you want to. `/higgsfield-init` can run it for you after asking.

</details>

## What The Installer Does

- Checks for `git`, `node`, `npm`, `higgs`, `jq`, `ffmpeg`, `python3`, and Pillow.
- Checks the installed Higgsfield CLI version and auth state.
- Symlinks `skill/higgsfield-autopilot/` into `~/.claude/skills/`.
- Symlinks `commands/claude/*.md` into `~/.claude/commands/`.
- Leaves private data out of git. Brand profiles, presets, and generated runs are ignored.

## First Verification

After setup:

```text
/higgsfield-init
```

`/higgsfield-init` is the setup and onboarding gate. It checks the CLI, asks whether you have a Higgsfield account, can run `higgs auth login` after your consent, checks workspace and balance, classifies the plan posture, and ends with the brand setup / moodboard demo / shape an idea / just explore menu.

If you want a deeper no-credit workflow check later:

```text
/higgsfield-test 1
```

Stage 1 expands a sample brief and checks model pricing without generating media.

Do not run `/higgsfield-test 2` or `/higgsfield-test 3` until Stage 1 passes and you are ready to spend Higgsfield credits. For normal content generation, `/higgsfield-init` is the setup gate.

## Windows

Native Windows installs may fail because of an upstream Higgsfield CLI issue. Use WSL or Git Bash for now.
