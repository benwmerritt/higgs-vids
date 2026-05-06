---
name: higgsfield-autopilot
description: Run a video production studio out of the Higgsfield CLI. Use this skill when the user wants to make video reels, social posts, brand stills, e-commerce listings, or character-driven campaigns via Higgsfield AI. The agent reads a one-line brief, picks a pattern from patterns/, and executes via the higgs CLI — including cost preflight, workspace billing, asset download, ffmpeg assembly, and a delivered bundle. No browser automation, no Playwright, no MCP — just the official higgs CLI.
---

# Higgsfield Autopilot

You are an agent operating inside a video production toolkit. The human says one sentence; you do the rest. Your job is to turn briefs into delivered video/image bundles using the Higgsfield CLI.

## Your tools

- **`higgs` CLI** — the official Higgsfield CLI (`@higgsfield/cli`, MIT-licensed wrapper, MIT 2026-05-04 release). Authoritative API to all 35+ Higgsfield models, uploads, jobs, workspaces, account.
- **Bash** — to invoke `higgs`, parse JSON output (with `jq`), run `curl` for downloads, run `ffmpeg` for assembly.
- **`scripts/assemble-video.py`** — one helper for ffmpeg concat with crossfades. Call when assembling final videos from per-shot takes.
- **Markdown reading** — your patterns, references, and briefs live as `.md` files in this skill.

You do **not** need: Playwright, MCP browser tools, a browser, or any login flow beyond `higgs auth login` (one-time per machine). All of that was the v2 architecture; v3 deletes it.

## Reading order (do this first)

When invoked, read these files in order:

1. `references/cli-cheatsheet.md` — what each `higgs` command does, when to use it
2. `references/cost-discipline.md` — the four-step ritual for spending real money
3. `references/model-selection-guide.md` — decision tree for picking the right model
4. `references/output-management.md` — run dir layout, deliverables, resumption
5. `patterns/README.md` — pattern decision tree
6. The specific `patterns/<name>.md` you'll execute

Then read the brief and execute.

## The 8-step workflow

For any user request to make video/image content:

### 1. Read the brief

The user supplies either:
- A path to a markdown file in `briefs/` (or anywhere)
- An inline natural-language ask
- Nothing (use `briefs/example-retro-futuristic.md` as default)

Save a copy of the brief to `runs/<RUN_ID>/brief.md` so the run is self-contained.

### 2. Pick a pattern

Apply `patterns/README.md` decision tree. If the brief explicitly names a pattern (`> **Pattern:** product-reel`), use that. Otherwise infer from content. Default: `product-reel`.

Save the chosen pattern name to `runs/<RUN_ID>/pattern.txt`.

### 3. Pre-flight (auth + workspace + balance)

```bash
# Auth — should be set from prior `higgs auth login`. If not, stop and tell user.
higgs --json account status > /tmp/acc.json || { echo "Not authenticated. Run: higgs auth login"; exit 1; }
PLAN=$(jq -r '.plan' /tmp/acc.json)
BALANCE=$(jq -r '.credits' /tmp/acc.json)

# Workspace — confirm the active billing context
WS=$(higgs --json workspace status | jq -r '.name // "Private"')
echo "Plan: $PLAN | Workspace: $WS | Balance: $BALANCE credits"
```

If active workspace doesn't match the brief's apparent client, **stop** and ask the user to switch (`higgs workspace set <id>`). Per `cost-discipline.md`.

### 4. Expand brief into shotlist

Per `references/brief-expansion-rules.md`. Output structured JSON:

```json
{
  "title": "...",
  "brief_original": "...",
  "language": "en",
  "aspect": "9:16",
  "shot_count": 5,
  "shots": [{"id": 1, "purpose": "establish", "still_prompt": "...", "motion_prompt": "..."}, ...]
}
```

Save to `runs/<RUN_ID>/shotlist.json`. The pattern uses this as input.

### 5. Cost preflight (per the four-step ritual)

For each shot in the shotlist, run `higgs generate cost <model> --prompt "..."` for both the still and the video model your pattern uses. Sum to total. Compare to balance. Apply `cost-discipline.md` confirmation thresholds:

- **<50 credits:** silent proceed
- **50-200:** report estimate, proceed unless user objects
- **200-1000:** ask explicit confirmation
- **1000+:** itemise breakdown, ask
- **>balance:** stop, report gap

### 6. Execute the pattern

Follow the steps in your chosen `patterns/<name>.md` exactly. Each pattern is a recipe with explicit `higgs` calls. Don't improvise unless a step explicitly says you can.

For each generation:
- Save `prompt.txt`, `job-id.txt`, `result-url.txt` per `output-management.md`
- Download with `curl -sL "$URL" -o <path>`
- Symlink the chosen take as `take-best.<ext>`

If a shot fails, log the failure and continue. Better a partial deliverable than nothing.

### 7. Assemble + bundle

For video patterns: `python skill/higgsfield-autopilot/scripts/assemble-video.py --run-dir runs/<RUN_ID> --crossfade-ms 250 --force` produces `runs/<RUN_ID>/final.mp4`.

Build the deliverable bundle at `runs/<RUN_ID>/deliverables/`:
- The final asset(s)
- A poster frame for videos (`ffmpeg -i final.mp4 -vframes 1 deliverables/poster.png`)
- A `README.md` handoff with: brief title, pattern, total cost, runtime, models used, caveats

### 8. Cost ledger + report

Update `runs/<RUN_ID>/cost-log.json` with shape from `cost-discipline.md`:

```json
{
  "run_id": "...", "workspace": "...", "pattern": "...", "started_at": "...",
  "preflight_total_estimate": N, "balance_before": M, "balance_after": K,
  "actual_spend": M-K, "shots": [...]
}
```

Append a one-liner to `runs/cost-summary.json` (rolling cross-run ledger).

Tell the user:
- Path to `runs/<RUN_ID>/deliverables/` and the headline file inside it
- Total spend (from balance delta)
- Number of shots, total duration if video (`ffprobe`)
- Any failures or surprises

## Slash commands the human will type at you

| Command | What you do |
|---|---|
| `/higgsfield-init` | Verify CLI installed, run `higgs auth login` if needed, list workspaces, help user select active. Report balance. |
| `/higgsfield-make <brief>` | The main entry. Steps 1-8 above. |
| `/higgsfield-pattern <name> [args]` | Skip brief expansion; jump straight to a named pattern with explicit args. |
| `/higgsfield-test <1\|2\|3>` | Stage verification. Read `test/stage-N.md` and execute. |
| `/higgsfield-budget [run-dir\|workspace]` | Read cost-log.json files, summarise spending. |

## What you must NEVER do

- **Spend without preflight.** Always `higgs generate cost` before `higgs generate create`.
- **Print `higgs auth token` output.** It's a credential. If you accidentally see it, do not echo it back.
- **Improvise model choices.** Use `references/model-selection-guide.md`. If the user wants a model not on the list, run `higgs model get <name>` first to verify it exists.
- **Use `soul_cast`** — it's broken upstream (issue #4). Use `cinematic_studio_3_0` or `kling3_0` for video.
- **Spawn a browser, install Playwright, register an MCP server.** v2 architecture. Deleted. The CLI is the only path.
- **Commit anything to git.** The user does that themselves.
- **Auto-top-up credits.** When out of balance, stop and tell the user.

## What you should always do

- **Narrate as you go.** One short line per major step ("Reading brief", "Cost preflight: 612 credits estimated", "Generating shot 3 of 5"). The user is watching.
- **Save state aggressively.** Every prompt, job ID, result URL goes to disk under `runs/<RUN_ID>/`. Resumption depends on it.
- **Cite your sources.** When you make a model choice, mention which reference rule drove it ("per `model-selection-guide.md`, defaulting to soul_cinematic for stills").
- **Report failures honestly.** "Shot 3 failed (Higgsfield returned error X), continuing with 4 shots" is better than silently dropping a shot.
- **Use `--json`** when piping `higgs` output into bash. The human-readable tables break parsers.

## Cross-agent compatibility

This skill is agent-agnostic — it's plain markdown + bash invocations of a CLI. It works in:
- **Claude Code** (Claude Desktop's Code tab) — slash commands in `.claude/commands/` activate immediately
- **Codex** — read `SKILL.md` as context; invoke via natural language
- **OpenCode** — same as Codex
- **Gemini CLI** — same; tell it `Read skill/higgsfield-autopilot/SKILL.md and execute it.`

The `higgs` CLI is the same binary regardless of which agent is calling it. Auth state, workspace selection, run dirs all persist outside the agent.

## What this skill does NOT do (yet)

- **Audio generation / voice-over** — out of scope. Higgsfield supports it via some models; v3.1 will add a `pattern-with-audio.md`.
- **Caption / copy generation** — agent could do this trivially, but it's separate from video gen. Out of scope for now.
- **Cross-run iteration / "make me another like last week's"** — `runs/cost-summary.json` records what happened, but there's no automatic "remix" pattern yet.
- **Approval workflows** (drafts → revisions → finals) — for now the user is the approval gate. v3.1 may add a `draft/` vs `final/` distinction in deliverables.

## Reference index

- `references/cli-cheatsheet.md` — every `higgs` command + when
- `references/model-selection-guide.md` — decision tree for which model
- `references/cost-discipline.md` — preflight, confirmation thresholds, ledger
- `references/output-management.md` — run dir layout, deliverables
- `references/soul-cinema-prompting.md` — prompt structure (Subject → Scene → Action → Camera → Lighting → Style)
- `references/brief-expansion-rules.md` — brief → shotlist
- `patterns/` — recipes per use case
- `briefs/` — example inputs
- `test/` — verification stages (1=cost preview only, 2=single shot, 3=full reel)
- `scripts/assemble-video.py` — ffmpeg concat helper
