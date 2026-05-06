# Agent Onboarding

> You're an AI agent operating inside this repo. Read this file first.

This is a **video production toolkit** built on top of the official Higgsfield CLI (`@higgsfield/cli`). The human says one sentence; you produce delivered video/image bundles.

## Your operating manual

**The single source of truth for what you do here is `skill/higgsfield-autopilot/SKILL.md`.** Read it in full at the start of any task that involves making videos or images.

## What's available to you

| Tool | Use |
|---|---|
| `higgs` CLI | All Higgsfield generation, upload, account, workspace operations. See `skill/higgsfield-autopilot/references/cli-cheatsheet.md`. |
| Bash | To invoke `higgs`, parse `--json` output with `jq`, run `curl` for downloads, run `ffmpeg`. |
| `python3` | Only for `skill/higgsfield-autopilot/scripts/assemble-video.py` (ffmpeg concat). No other Python. |
| Markdown reading | All your operational knowledge lives in `.md` files under `skill/higgsfield-autopilot/`. |

## What you must NOT do

- **Don't spawn a browser.** No Playwright, no MCP browser tools, no Chrome automation. The CLI replaced all of that.
- **Don't print `higgs auth token` output.** It's a credential.
- **Don't spend without preflight.** Always run `higgs generate cost ...` before `higgs generate create ...`. See `references/cost-discipline.md`.
- **Don't commit to git.** The user does that.
- **Don't auto-install dependencies.** Tell the user what to install; let them decide.

## Slash commands the human will type

| Command | Maps to |
|---|---|
| `/higgsfield-init` | First-run setup |
| `/higgsfield-make <brief>` | Main entry — read brief, pick pattern, execute, deliver |
| `/higgsfield-pattern <name> [args]` | Direct pattern execution |
| `/higgsfield-test <1\|2\|3>` | Stage verification |
| `/higgsfield-budget [path]` | Cost queries |

When the human invokes one of these, the matching file in `.claude/commands/` tells you exactly what to do.

## Repo map

```
.claude/commands/             ← slash commands (Claude Code projects-skill format)
skill/higgsfield-autopilot/   ← the skill bundle — your operating manual
  SKILL.md                     ← read first
  references/                  ← CLI cheatsheet, model selection, cost discipline, output management, prompting
  patterns/                    ← recipes per use case (product-reel, quick-social, multi-platform-render, +stubs)
  briefs/                      ← example inputs
  scripts/assemble-video.py    ← ffmpeg concat helper (the only script you call)
  test/                        ← stage 1/2/3 verification prompts
docs/research/                ← deep-dive research on Higgsfield (background reading)
docs/skills/                  ← peer skill: prompt design (skill-higgsfield-shot-designer.md)
findings/                     ← origin story (the IG reel that inspired v1, kept for context)
runs/                         ← per-run outputs (gitignored)
```

## Cross-agent

This toolkit is agent-agnostic. The same SKILL.md, references, patterns, and briefs work in:
- **Claude Code** (Claude Desktop's Code tab) — slash commands activate immediately
- **Codex / OpenCode / Gemini CLI** — read SKILL.md as context, invoke via natural language

There's no agent-specific code anywhere in `skill/`. The `higgs` CLI is the same binary regardless of which agent is calling it.

## When you're confused

If a brief doesn't fit any pattern, default to `patterns/product-reel.md` and adapt the shotlist. If the brief is genuinely outside scope (e.g. asks for music composition or 3D modelling), stop and tell the user.

If a `higgs` command fails in a way the CLI cheatsheet doesn't cover, run `higgs <command> --help` to check current flags. The CLI is moving fast (new release on 2026-05-04); flags may have shifted since the cheatsheet was last updated.

If the user says "just do it" without confirmation prompts, see `references/cost-discipline.md` § "When the user says 'just do it'" — the rules are there.
