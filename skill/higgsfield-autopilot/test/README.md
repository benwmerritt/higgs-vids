# Test Harness

Three-stage verification of the toolkit. Same files for any agent.

| Stage | Cost | Purpose | Hard stop |
|---|---|---|---|
| **1** | **0 credits** | Auth + workspace + brief expansion + cost preflight via `higgs generate cost` | No `generate create` calls |
| **2** | **~12 credits** | One real Soul Cinematic still — submit, wait, download, log | One image only, no video |
| **3** | **~1000–12,500 credits** | Full 5-shot reel via `product-reel` pattern + ffmpeg assembly | Produces `runs/<date>/deliverables/reel-final.mp4` |

**Run them in order.** Don't skip to stage 3 if stage 1 hasn't passed — you'll burn money on a broken setup.

## How to run

### Claude Code

```
/higgsfield-test 1
/higgsfield-test 2
/higgsfield-test 3
```

### Other agents (Gemini CLI / Codex / OpenCode / etc.)

In a fresh agent session inside this repo:

> Read `skill/higgsfield-autopilot/test/stage-1.md` and execute it.

(Substitute `stage-2.md` or `stage-3.md`.)

## Pre-conditions

```bash
which higgs                            # CLI installed
higgs account status                    # auth works
which ffmpeg                            # assembly works (only needed for stage 3)
higgs --json account status | jq .credits  # balance for stages 2 + 3
```

`/higgsfield-init` walks through these. Run that first if anything's missing.

## Output per stage

Each stage writes a markdown report into the run dir:

```
runs/2026-05-06-1430/
├── shotlist.json              ← all stages
├── stage-1-report.md          ← stage 1
├── stage-2-report.md          ← stage 2 (also: shot-01/still.png)
└── stage-3-report.md          ← stage 3 (also: shot-{01..05}/, deliverables/reel-final.mp4)
```

Reports are written for **you, the human** — what the agent saw, what worked, what surprised it, recommended changes to SKILL.md or patterns or references.

## Cross-agent consistency

Same test files, same expected behaviour across Claude Code, Gemini, Codex, OpenCode. After stage 1 in two agents, compare reports — divergence in "surprises" or "recommended changes" tells you which pieces of SKILL.md still leak agent-specific assumptions.

## Failure-mode quick table

| Symptom | Stage | Likely cause |
|---|---|---|
| "higgs not found" | any | CLI not installed → `npm install -g @higgsfield/cli` |
| "Not authenticated" | any | Run `/higgsfield-init`; it can run `higgs auth login` after consent |
| "Insufficient balance" | 2, 3 | Top up at higgsfield.ai or wait for plan reset |
| `generate cost` returns null | 1 | Model name wrong → `higgs model list` |
| Generation times out (>5 min for stage 2, >15 min per shot for stage 3) | 2, 3 | Higgsfield queue saturation. Don't restart — check `higgs generate get <id>` later |
| Asset URL returns 403/404 | 2, 3 | Signed URL expired → re-fetch with `higgs generate get <id>` |
| ffmpeg fails on concat | 3 | Codec mismatch — `../scripts/assemble-video.py` auto-falls-back to re-encode |
| Wrong workspace charged | 2, 3 | `higgs workspace status` should always be checked at start |

## Don't

- **Run stages 2 / 3 before passing stage 1.** Money down a hole.
- **Run stages in parallel.** They share an account; jobs interleave confusingly.
- **Edit `skill/` files from inside a stage.** Recommendations go in the report — apply them after reviewing.
