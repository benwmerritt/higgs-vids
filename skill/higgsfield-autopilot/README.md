# Higgsfield Autopilot

Drop-in skill bundle that lets Claude Code, Codex, or OpenCode generate finished Higgsfield (Soul Cinema) campaigns from a one-line brief.

## 60-second start

```bash
# 1. Clone the parent repo
git clone <repo-url> higgs-vids && cd higgs-vids

# 2. Install deps + Playwright Chromium
bash skill/higgsfield-autopilot/scripts/00-bootstrap.sh

# 3. One-time login (headed browser opens; sign in to higgsfield.ai)
python skill/higgsfield-autopilot/scripts/01-login.py

# 4. Tell your agent to run the autopilot
#    In Claude Code, the simplest path is the slash command:
#       /higgsfield-autopilot skill/higgsfield-autopilot/briefs/example-retro-futuristic.md
#
#    Or natural language in any of the three agents:
#       Claude Code: claude "Run the higgsfield-autopilot on briefs/example-retro-futuristic.md"
#       Codex:       codex --context skill/higgsfield-autopilot/SKILL.md "Run on briefs/example-retro-futuristic.md"
#       OpenCode:    opencode "Run higgsfield-autopilot on briefs/example-retro-futuristic.md"
```

The agent expands the brief, then invokes `scripts/run-autopilot.py` once — no per-step orchestration from you.

After ~10–20 minutes (depending on Higgsfield queue), `runs/<date>/final.mp4` exists.

## What it does

| Stage | Script | Output |
|---|---|---|
| Bootstrap | `scripts/00-bootstrap.sh` | Installs Playwright + Chromium |
| Login | `scripts/01-login.py` | Saves `auth/storage_state.json` |
| Verify | `scripts/02-open-soul-cinema.py` | Confirms session is live |
| Generate | `scripts/03-generate-asset.py` | Submits one shot, returns asset IDs |
| Download | `scripts/04-download-assets.py` | Pulls all batches to `runs/<date>/shot-NN/` |
| Assemble | `scripts/05-assemble-video.py` | ffmpeg concat → `runs/<date>/final.mp4` |

## Repo layout

```
higgs-vids/
├── docs/                                # Existing Higgsfield research (reference material)
│   ├── research/                         # Deep dives on prompting, model stack, orchestration
│   └── skills/skill-higgsfield-shot-designer.md  # Prompt-craft skill (peer skill)
├── findings/
│   └── instagram-reel-DXfKnWhDPlW-workflow.md   # Source-of-truth analysis of the reel
├── skill/higgsfield-autopilot/          # This skill bundle
│   ├── SKILL.md                          # Entry point — agent reads this
│   ├── README.md                         # You are here
│   ├── briefs/example-retro-futuristic.md
│   ├── references/                       # Loaded into context only when needed
│   ├── scripts/                          # Numbered pipeline + lib/
│   └── auth/                             # storage_state.json (gitignored)
└── downloads/                            # Original reel + frames + transcripts
```

## How it differs from the reel

The Instagram reel that inspired this (Timothée Oranger, IG `DXfKnWhDPlW`) sells "15 agents + Playwright MCP." The reality decoded from frame analysis (see `findings/`) is one Claude Code session + numbered Python scripts using `playwright.sync_api` directly. This skill replicates the *real* architecture without the MCP overhead, making it portable across agents.

## Updating selectors when Higgsfield changes their UI

All DOM selectors live in `scripts/lib/selectors.py`. When a script fails with `SELECTOR_NOT_FOUND`:

1. Re-run `scripts/01-login.py` (it dumps the post-login DOM to `auth/last-login-dom.html` for inspection).
2. Open `references/selectors-cheatsheet.md` — it documents which selector goes with which UI element.
3. Patch `scripts/lib/selectors.py`. No other file should need changes.

## Limitations / known issues

- Soul Cinema only (no Veo/Sora/Kling).
- Headed browser by default (Higgsfield headless behaviour unverified — see findings open questions).
- No audio / no Soul ID / no LipSync.
- Cost guard is advisory; actual credit usage depends on Higgsfield's billing at run time.

## License & credit

Inspired by Timothée Oranger's reel. Implementation independent. No code or prompts taken from his (gated) "CLAUDE AUTOPILOT SYSTEM" — built from frame analysis only.
