# Higgsfield Autopilot

Drop-in skill bundle that lets Claude Code, Codex, or OpenCode generate finished Higgsfield (Soul Cinema) campaigns from a one-line brief — driving the live browser via the **Playwright MCP server**.

No Python pipeline, no selector files. SKILL.md tells the agent which MCP tool calls to make; the agent reads the live page via `browser_snapshot()` and adapts.

## 60-second start

```bash
# 1. Clone the repo
git clone <repo-url> higgs-vids && cd higgs-vids

# 2. Prerequisites (one-time per machine)
brew install --cask google-chrome ffmpeg

# Register a Playwright MCP server that ATTACHES to our Chrome (don't reuse
# a default Playwright MCP — it'll spawn its own Chromium that Higgsfield blocks)
claude mcp add higgsfield-browser npx '@playwright/mcp@latest' -- --cdp-endpoint=http://127.0.0.1:9222

# 3. Open the long-lived browser window
bash skill/higgsfield-autopilot/scripts/launch-browser.sh --bg

# 4. Sign in to higgsfield.ai in that Chrome window (one-time; profile persists)

# 5. Tell your agent to run the autopilot
#    Claude Code (slash command):
/higgsfield-autopilot skill/higgsfield-autopilot/briefs/example-retro-futuristic.md

#    Or natural language in any of the three agents:
claude   "Run the higgsfield-autopilot on briefs/example-retro-futuristic.md"
codex    "Use the higgsfield-autopilot skill on briefs/example-retro-futuristic.md"
opencode "Run higgsfield-autopilot on briefs/example-retro-futuristic.md"
```

After ~10–20 minutes (depending on Higgsfield queue), `runs/<date>/final.mp4` exists.

## What it does

The agent:
1. Reads your brief.
2. Expands it into a 5-shot JSON shot list.
3. Drives Chrome via Playwright MCP — navigates to higgsfield.ai/canvas, switches to Soul Cinema, fills each shot's prompt, clicks Generate, polls until done.
4. Extracts asset URLs via `browser_evaluate`, downloads each take with `curl`.
5. Picks the best take per shot (vision-guided when possible).
6. Runs `assemble-video.py` (ffmpeg concat) to produce `final.mp4`.

## Repo layout

```
higgs-vids/
├── docs/                                # Existing Higgsfield research (background reading)
│   ├── research/                         # Deep dives on prompting, model stack, orchestration
│   └── skills/skill-higgsfield-shot-designer.md  # Peer skill: prompt-craft theory
├── findings/
│   └── instagram-reel-DXfKnWhDPlW-workflow.md   # Source-of-truth analysis of the reel
├── skill/higgsfield-autopilot/          # This skill bundle
│   ├── SKILL.md                          # ← Agent reads this. The protagonist.
│   ├── README.md                         # ← You are here
│   ├── briefs/example-retro-futuristic.md
│   ├── references/                       # Loaded by agent on demand
│   │   ├── playwright-mcp-playbook.md   # MCP tool calls + JS snippets
│   │   ├── workflow-architecture.md      # Topology + per-stage tool table
│   │   ├── soul-cinema-prompting.md      # Prompt rules
│   │   └── brief-expansion-rules.md      # Brief → shotlist rules
│   ├── scripts/
│   │   ├── launch-browser.sh             # Open the long-lived Chrome window
│   │   ├── 00-bootstrap.sh               # Prerequisite checker
│   │   └── assemble-video.py             # ffmpeg concat (the only Python)
│   └── auth/                             # storage_state + Chrome profile (gitignored)
└── runs/                                 # Per-run outputs (gitignored)
```

## Architecture

```
Agent  ──MCP tool calls──▶  Playwright MCP  ──CDP attach──▶  Real Chrome (your window)
                                                                    │
                                                                    ▼
                                                              higgsfield.ai/canvas
```

The Chrome window outlives the agent. You open it once with `launch-browser.sh`. Every agent run attaches via CDP on port 9222. Same window, same login, same tabs across as many `/higgsfield-autopilot` invocations as you like.

See `references/workflow-architecture.md` for the per-stage tool table.

## How it differs from the original Instagram reel

The reel that inspired this (Timothée Oranger, IG `DXfKnWhDPlW`) sells "15 agents + Playwright MCP". Frame analysis (see `findings/`) revealed the real implementation was Playwright MCP install + a numbered Python script pipeline.

This skill keeps **only** the Playwright MCP install. The numbered scripts are gone — the agent does that work directly via MCP tool calls. Result: ~7× less code, no selector maintenance, cross-agent compatible.

## Updating when Higgsfield changes their UI

You don't. The agent re-snapshots the page on every run and adapts. If a step systematically fails (e.g. a renamed button), the only file you'd ever edit is the relevant step in `SKILL.md` — and even that's usually a one-line tweak ("the model picker is now in the top-right" instead of "bottom-left").

## Testing

Three-stage harness in `test/`. Same files for any agent.

```
/higgsfield-test 1     # 0 credits — dry run, verifies auth + Soul Cinema + cost preview
/higgsfield-test 2     # ~30 credits — single real shot
/higgsfield-test 3     # ~150 credits — full 5-shot campaign
```

In Gemini / Codex / OpenCode, just say: *"Read `skill/higgsfield-autopilot/test/stage-1.md` and execute it."* Same outcome.

See `test/README.md` for full details, failure-mode table, and cross-agent comparison advice.

## Limitations

- Soul Cinema only (no Veo/Sora/Kling automation yet).
- Headed browser (visible window). The agent expects the window from `launch-browser.sh` to be running.
- No audio / no Soul ID character consistency / no LipSync.
- Cost guard is advisory; agent reports estimated credits before each run, but Higgsfield's billing is authoritative.

## License & credit

Inspired by Timothée Oranger's reel. Implementation independent — built from frame analysis only. No code or prompts taken from his (gated) "CLAUDE AUTOPILOT SYSTEM".
