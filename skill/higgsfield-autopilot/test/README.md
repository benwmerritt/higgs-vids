# Higgsfield Autopilot — Test Harness

Three-stage verification of the autopilot skill. Same test files work in any agent (Claude Code, Gemini CLI, Codex, OpenCode) — they're plain markdown the agent reads and executes.

## Stages

| Stage | Cost | Purpose | Hard stop |
|---|---|---|---|
| **1** | **0 credits** | Auth + Soul Cinema selection + cost preview | Stops before clicking Generate |
| **2** | **~20–32 credits** | One real shot — generation, polling, download | Stops after shot 1 downloads |
| **3** | **~100–160 credits** | Full 5-shot campaign + ffmpeg assembly | Produces `runs/<date>/final.mp4` |

**Run them in order.** Don't skip to stage 3; if a foundation step is broken, stages 2 and 3 just waste credits.

## How to run

### Claude Code

```
/higgsfield-test 1     # default — dry run, no credits
/higgsfield-test 2     # single shot, ~30 credits
/higgsfield-test 3     # full campaign, ~150 credits
```

### Gemini CLI / Codex / OpenCode

In a fresh agent session inside this repo:

> Read `skill/higgsfield-autopilot/test/stage-1.md` and execute it.

(Substitute `stage-2.md` or `stage-3.md` as needed.)

## Pre-conditions

Before any stage, all of these must be true. The stage files re-check, but you can verify upfront:

```bash
# 1. Long-lived Chrome on CDP port 9222
lsof -i :9222 -sTCP:LISTEN || \
    bash skill/higgsfield-autopilot/scripts/launch-browser.sh --bg

# 2. ffmpeg available (only needed for stage 3)
which ffmpeg || brew install ffmpeg

# 3. Higgsfield logged in (sign in once in the launched Chrome window;
#    profile persists at skill/higgsfield-autopilot/auth/user-data/)

# 4. Playwright MCP server registered with --cdp-endpoint=http://127.0.0.1:9222
#    Claude Code:  claude mcp list | grep -i playwright
#    Gemini CLI:   gemini mcp list 2>&1 | grep -i higgsfield
```

The `00-bootstrap.sh` script automates checks 1, 2, and the Claude Code MCP check. Run it any time:

```bash
bash skill/higgsfield-autopilot/scripts/00-bootstrap.sh
```

## What each stage produces

Every stage writes a markdown report into the run dir:

```
runs/2026-05-05-1430/
├── shotlist.json                    ← all stages
├── stage-1-report.md                ← stage 1
├── stage-2-report.md                ← stage 2 (also: shot-01/take-{1..4}.mp4)
└── stage-3-report.md                ← stage 3 (also: shot-{01..05}/, final.mp4)
```

Reports are designed to be **read by you, the human** — they capture what the agent saw, what worked, what surprised it, and what it would change about SKILL.md or the playbook.

## Cross-agent expectations

The same test files run in any agent. After stage-1 in two different agents, compare reports:

- Same workspace nav items detected? → snapshot reading is consistent
- Same cost preview number? → MCP calls hit the same UI state
- Different "surprises"? → that's interesting — agents have different fallback strategies

If you find an agent-specific divergence, file it as a recommended change to SKILL.md (which then becomes a more agent-agnostic instruction).

## Failure modes by stage

| Symptom | Stage | Cause | Fix |
|---|---|---|---|
| "MCP browser tools not visible" | any | MCP server not registered, or registered without `--cdp-endpoint` | Re-register per the README of the parent skill |
| "Workspace nav not found, login button visible" | 1 | Chrome session expired | Sign in again in the launched Chrome window |
| "Can't find Soul Cinema model" | 1 | Higgsfield removed/renamed Soul Cinema | Update SKILL.md step 4 |
| "Cost preview returned null" | 1 | UI changed credit-cost display location | Update the JS snippet in `references/playwright-mcp-playbook.md` |
| "Generation failed" with explicit error | 2,3 | Out of credits, or content policy violation | Top up credits / rephrase prompt |
| "Polling timed out after 10 min" | 2,3 | Higgsfield queue saturation | Wait, retry shot manually, or reduce parallelism |
| "Asset URLs are blob: only" | 2,3 | Page hasn't fully hydrated | `browser_evaluate` retry after 5s, or fall back to `browser_network_requests` |
| "ffmpeg fails on concat" | 3 | Codec mismatch between takes | `assemble-video.py` auto-falls-back to re-encode; if that also fails, takes are corrupt — re-download |

## Don't

- **Don't run stage 2 or 3 without passing stage 1 first.** Money down a hole.
- **Don't run multiple stages in parallel.** They share one browser; they'll trip over each other.
- **Don't edit files in `skill/higgsfield-autopilot/` from inside a test stage.** Recommendations go in the report. Apply them after reviewing the report.
