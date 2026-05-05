---
name: higgsfield-autopilot
description: Drive Higgsfield (Soul Cinema model) end-to-end via Playwright to turn a one-line creative brief into a finished editorial video. Use this skill when the user wants to generate a Higgsfield campaign autonomously, automate Soul Cinema, batch-generate Higgsfield assets, or build editorial reels with AI. Requires a one-time headed login to save auth state; afterward runs unattended via numbered Python scripts that the agent invokes in sequence.
---

# Higgsfield Autopilot

Turn a single-line creative brief into a finished 9:16 editorial video by orchestrating Higgsfield's Soul Cinema model through Playwright.

## When to use this skill

Trigger when the user says any of:
- "make me a Higgsfield campaign about …"
- "generate a Soul Cinema reel for …"
- "automate Higgsfield"
- "run the autopilot on this brief"
- Or hands you a brief markdown file in `briefs/`.

If the user just wants prompt advice (no automation), defer to the existing `higgsfield-shot-designer` skill at `docs/skills/skill-higgsfield-shot-designer.md` instead.

## Prerequisites

- **Python 3.11+** with `pip`
- **ffmpeg** on PATH (`brew install ffmpeg` on macOS)
- A **Higgsfield account** with credits (Soul Cinema 9:16 4/4 batches consume credits — see `references/soul-cinema-prompting.md` for cost notes)

## One-time setup (human required)

Run **once** per machine:

```bash
bash skill/higgsfield-autopilot/scripts/00-bootstrap.sh
python skill/higgsfield-autopilot/scripts/01-login.py
```

`01-login.py` opens a headed Chromium. The user signs in to higgsfield.ai manually, then presses Enter in the terminal. Storage state is saved to `skill/higgsfield-autopilot/auth/storage_state.json` (gitignored). After this, the skill runs unattended until auth expires (typically weeks).

## The workflow (agent execution order)

When invoked with a brief, follow these steps **in order**. Each step is a separate background shell so the user can monitor progress.

### Step 1 — Read the brief
Brief is either a path (e.g. `briefs/example-retro-futuristic.md`) or an inline string. Briefs are conversational, often one sentence. Don't ask the user to expand the brief — that's your job in step 2.

### Step 2 — Expand brief into shot list
Load `references/brief-expansion-rules.md`. Produce a JSON shot list:

```json
{
  "title": "Retro-futuristic editorial campaign",
  "aspect": "9:16",
  "shot_count": 5,
  "shots": [
    {"id": 1, "purpose": "establish", "prompt": "<Soul Cinema prompt per references/soul-cinema-prompting.md>"},
    ...
  ]
}
```

Save to `runs/<YYYY-MM-DD-HHMM>/shotlist.json`.

### Step 3 — Verify session
Run `scripts/02-open-soul-cinema.py` once. Exits non-zero with `AUTH_EXPIRED` if storage state is stale — in that case, tell the user to re-run `scripts/01-login.py`.

### Step 4 — Generate assets
For each shot in the shot list:

```bash
python scripts/03-generate-asset.py \
  --prompt "<shot.prompt>" \
  --aspect 9:16 --batch 4 --boost on \
  --shot-id <shot.id> \
  --run-dir runs/<YYYY-MM-DD-HHMM>
```

Run multiple shots **in parallel background shells** (Higgsfield queues them server-side). Capture asset IDs to `runs/<...>/shot-<NN>/asset-ids.json`.

**Cost guard:** Before kicking off, run with `--dry-run` first to see estimated credit consumption. If > 400 credits, confirm with the user.

### Step 5 — Download assets
```bash
python scripts/04-download-assets.py --run-dir runs/<YYYY-MM-DD-HHMM>
```

Pulls the 4 batch outputs per shot into `runs/<...>/shot-<NN>/take-{1..4}.mp4`.

### Step 6 — Pick best take per shot
Use vision capability to inspect `take-1.mp4` through `take-4.mp4` for each shot. Symlink the chosen one as `take-best.mp4`. If no vision available, default to `take-1` and tell the user to manually swap.

### Step 7 — Assemble final video
```bash
python scripts/05-assemble-video.py --run-dir runs/<YYYY-MM-DD-HHMM>
```

Concatenates the `take-best.mp4` files in shot-id order with crossfades. Output: `runs/<...>/final.mp4`.

Report the path to the user with playback duration and total credit cost.

## Failure handling

| Symptom | Likely cause | Action |
|---|---|---|
| `AUTH_EXPIRED` from script 02 | storage_state stale | Tell user to re-run `01-login.py` |
| `SELECTOR_NOT_FOUND` from any script | Higgsfield UI changed | Load `references/selectors-cheatsheet.md`, identify the broken selector, propose a fix in `scripts/lib/selectors.py` |
| Generation hangs > 10 min | Higgsfield queue saturation | `lib/higgsfield.py` has exponential backoff; let it run. Don't restart. |
| `RATE_LIMIT` from Higgsfield | Too many parallel submissions | Reduce parallelism in step 4; serialise if needed |
| ffmpeg fails | Aspect mismatch between takes | Re-check shot list `aspect` field; all shots must share aspect |

## Cross-agent compatibility

This skill is designed to work in **Claude Code**, **Codex**, and **OpenCode** without modification. The skill bundle is just markdown + Python — no MCP, no agent-specific runtime.

- **Claude Code:** symlink the bundle into `~/.claude/skills/higgsfield-autopilot/`, or use as a project skill via `.claude/skills/`.
- **Codex (OpenAI CLI):** include `skill/higgsfield-autopilot/SKILL.md` in your `AGENTS.md` context, or pass it as a system prompt prefix.
- **OpenCode:** drop into `.opencode/skills/higgsfield-autopilot/`.

In all three cases the agent reads SKILL.md, follows the numbered steps, and shells out to the Python scripts. No agent-specific code paths.

## What this skill does NOT do

- **Prompt design from scratch** — it formats prompts per Soul Cinema rules, but defers to `docs/skills/skill-higgsfield-shot-designer.md` for the underlying prompt-craft theory.
- **Other Higgsfield models** — only Soul Cinema. Adding Veo/Sora/Kling would require new selectors and a model-routing layer.
- **Audio generation, lip-sync, character consistency (Soul ID)** — out of scope for v1.
- **Cloud API path** — uses Playwright against the web UI. The Cloud API exists but is under-documented; see `docs/research/generative-media-orchestration.md` section 2.3.4. Migrating to the API would be a clean swap of `lib/higgsfield.py` only.
