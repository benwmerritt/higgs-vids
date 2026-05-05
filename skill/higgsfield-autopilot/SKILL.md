---
name: higgsfield-autopilot
description: Drive Higgsfield (Soul Cinema model) end-to-end via the Playwright MCP server to turn a one-line creative brief into a finished editorial video. Use this skill when the user wants to generate a Higgsfield campaign autonomously, automate Soul Cinema, batch-generate Higgsfield assets, or build editorial reels with AI. Requires a one-time browser login (handled by launching real Chrome via scripts/launch-browser.sh and signing in by hand). Afterward the agent uses Playwright MCP tools (browser_navigate, browser_snapshot, browser_click, browser_type, browser_evaluate) to drive the live browser session — no per-step Python scripts.
---

# Higgsfield Autopilot

Turn a single-line creative brief into a finished 9:16 editorial video by driving Higgsfield's Soul Cinema model through the Playwright MCP server.

## When to use this skill

Trigger when the user says any of:
- "make me a Higgsfield campaign about …"
- "generate a Soul Cinema reel for …"
- "automate Higgsfield"
- "run the autopilot on this brief"
- Or hands you a brief markdown file in `briefs/`.

If the user only wants prompt advice (no automation), defer to `docs/skills/skill-higgsfield-shot-designer.md` instead.

## Architecture (read this first)

```
You (the agent)
   │
   │   tool calls (browser_navigate, browser_snapshot, browser_click, ...)
   ▼
Playwright MCP server  ──attach via CDP──▶  Real Chrome (already logged in)
                                                │
                                                ▼
                                          higgsfield.ai/canvas
```

There is **no Python orchestration layer between you and the browser**. You read the page via `browser_snapshot()`, decide what to click, call `browser_click()`. When Higgsfield changes their UI, re-snapshot and adapt — there are no selector files to patch.

The only Python in this skill is `scripts/assemble-video.py` (ffmpeg wrapper), which the agent shells out to once at the end.

## Prerequisites

The user must have done these once per machine. Check at the start of every run:

| Requirement | Verify with | Install command |
|---|---|---|
| **Real Google Chrome** (not Playwright's bundled Chromium — Higgsfield blocks it) | `ls "/Applications/Google Chrome.app"` | `brew install --cask google-chrome` |
| **ffmpeg** | `which ffmpeg` | `brew install ffmpeg` |
| **Playwright MCP server registered with `--cdp-endpoint`** | `claude mcp list \| grep -i playwright` AND verify the registration command includes `--cdp-endpoint=http://127.0.0.1:9222` | `claude mcp add higgsfield-browser npx '@playwright/mcp@latest' -- --cdp-endpoint=http://127.0.0.1:9222` (NOTE: a Playwright MCP without `--cdp-endpoint` will spawn its own Chromium, which Higgsfield blocks. Don't reuse a default Playwright MCP — register this one separately) |
| **Higgsfield account** with credits | Visible in browser after login | Sign up at higgsfield.ai |

If any is missing, stop and tell the user what to install. Do not try to install dependencies for them.

## One-time setup (human action)

Per session, the user runs:

```bash
bash skill/higgsfield-autopilot/scripts/launch-browser.sh --bg
```

This opens a real Chrome window at higgsfield.ai/canvas, with `--remote-debugging-port=9222` enabled, against the persistent profile at `skill/higgsfield-autopilot/auth/user-data/`. The window stays open. The Playwright MCP server attaches to it via CDP — same window, same profile, same login across all your tool calls.

**First-ever run**: the user signs in to higgsfield.ai in that window. Subsequent runs reuse the saved login.

## The workflow

Execute these steps in order. Each step lists the MCP tool calls you should make. Load `references/playwright-mcp-playbook.md` once at the start of step 3 — that's your tool reference.

### Step 1 — Read the brief
Brief is either a path (e.g. `skill/higgsfield-autopilot/briefs/example-retro-futuristic.md`) or an inline string. Briefs are conversational, often one sentence, in any language. **Don't ask the user to expand it — that's your job in step 2.**

### Step 2 — Expand brief into shotlist.json
Load `references/brief-expansion-rules.md` and `references/soul-cinema-prompting.md`. Produce:

```json
{
  "title": "...",
  "brief_original": "<verbatim user brief>",
  "language": "<detected language>",
  "aspect": "9:16",
  "shot_count": 5,
  "shots": [
    {"id": 1, "purpose": "establish", "prompt": "<Soul Cinema prompt, ENGLISH>"},
    {"id": 2, "purpose": "subject_intro", "prompt": "..."},
    ...
  ]
}
```

Pick a run dir: `runs/<YYYY-MM-DD-HHMM>/` (under repo root, NOT under the skill dir). Create it. Save the shotlist as `runs/<...>/shotlist.json`.

### Step 3 — Verify session
1. `browser_navigate(url="https://higgsfield.ai/canvas")`
2. `browser_snapshot()`
3. Inspect the snapshot:
   - **Logged in**: side-nav contains "Cinema Studio", "Assets", "Marketing Studio". Top-right shows credit count, NO "Login"/"Sign up" buttons.
   - **Logged out**: "Login" / "Sign up" buttons visible.
4. If logged out → STOP. Tell the user:
   > "The browser session needs login. Open the Chrome window from `launch-browser.sh` and sign in to higgsfield.ai, then re-run."

### Step 4 — Land in the Image generator with Soul Cinema selected
The reel showed Soul Cinema is a model option inside the **Image** generator on `/canvas`. Default model is "Nano Banana Pro" — you need to switch.

1. From the snapshot at step 3, find and click the "Image" tab in the top nav. Re-snapshot if needed.
2. Look for a "Soul Cinema is here" promo card on the left of the workspace. If present, `browser_click` it — that's a single-click switch to Soul Cinema.
3. If the promo card isn't there, find the model pill at bottom-left of the prompt panel. It shows the current model (e.g. "Nano Banana Pro"). Click it. A dropdown appears. Click "Soul Cinema".
4. Verify by `browser_evaluate("() => document.body.innerText.includes('Soul Cinema')")` and by re-snapshotting — the model pill should now read "Soul Cinema".

If both methods fail after one retry, take a screenshot, share with the user, ask them to click Soul Cinema manually then resume.

### Step 5 — Cost preview (no submission)
For shot 1 only:
1. Find the prompt textbox in the snapshot (placeholder is "Describe the scene you imagine"). `browser_type(text=<shot 1 prompt>)`.
2. Set aspect ratio to 9:16: find the aspect picker (shows "3:4" or current aspect), click it, click "9:16".
3. Set batch to 4: find the "1/4" or similar counter, click up arrows or directly set to 4.
4. Read the credit-cost preview near the Generate button:
   ```js
   () => {
     const m = document.body.innerText.match(/(\d+)\s+credits?/i);
     return m ? parseInt(m[1], 10) : null;
   }
   ```
   via `browser_evaluate`.
5. Multiply by `shotlist.shot_count`. **If estimated total > 400 credits, stop and ask the user to confirm.**

### Step 6 — Generate all shots
Two strategies — pick based on shot count:

**For ≤3 shots — sequential in one tab:**
For each shot in shotlist:
1. Clear prompt (`browser_type` with empty string, or select-all + delete).
2. `browser_type` the shot's prompt.
3. `browser_click` the Generate button.
4. Wait for batch completion (see polling pattern in `references/playwright-mcp-playbook.md`).
5. Move to next shot.

**For 4+ shots — multi-tab parallel:**
1. Open N-1 additional tabs with `browser_tabs(action="new")`. In each, navigate to canvas, switch to Image+Soul Cinema (steps 3-4).
2. Submit one shot per tab.
3. Poll all tabs in round-robin via `browser_tabs(action="select", index=N)`.

### Step 7 — Download assets
For each shot's tab (or sequentially in the one-tab case):
1. `browser_evaluate` the asset-extraction snippet (see playbook):
   ```js
   () => Array.from(document.querySelectorAll('video, img'))
           .map(e => e.currentSrc || e.src)
           .filter(u => u && u.startsWith('http'))
   ```
2. Diff against pre-submit baseline → 4 new URLs are this shot's takes.
3. For each URL, shell out:
   ```bash
   mkdir -p runs/<date>/shot-NN
   curl -sL "$URL" -o runs/<date>/shot-NN/take-K.mp4
   ```

If `browser_evaluate` returns `blob:` URLs (not http), wait 5s and retry. If still blob, fall back to `browser_network_requests()` and grep for `cdn.higgsfield.ai` or similar media URLs.

### Step 8 — Pick best take per shot (optional vision step)
For each shot:
1. Use your vision capability to inspect `take-1.mp4` through `take-4.mp4` (you can read mp4 frames if your environment supports it; otherwise sample with ffmpeg first).
2. Symlink the chosen take as `take-best.mp4`:
   ```bash
   ln -sf take-2.mp4 runs/<date>/shot-NN/take-best.mp4
   ```

If vision-pick isn't feasible, default to `take-1` and tell the user to manually re-symlink any shots they want to swap.

### Step 9 — Assemble final video
```bash
python skill/higgsfield-autopilot/scripts/assemble-video.py \
    --run-dir runs/<date> \
    --crossfade-ms 250 \
    --force
```

This is the only Python the agent runs directly. ffmpeg concat with crossfades. Output: `runs/<date>/final.mp4`.

### Step 10 — Report
Tell the user:
- Path to `runs/<date>/final.mp4`
- Number of shots, total duration (`ffprobe`), aspect
- Estimated credit spend (read from cost-preview log if you saved it)
- Which takes were auto-picked vs vision-picked

## Failure handling

| Symptom | Recovery |
|---|---|
| Snapshot shows Login button | User needs to re-sign-in in the launched Chrome window. Don't proceed. |
| `browser_click` blocked by overlay | Snapshot, find dismiss button (×, Close, Skip, Maybe later), click it, retry. |
| Soul Cinema selection silently reverts | Re-snapshot after clicking; if still on the wrong model, click the model pill and select from dropdown explicitly. |
| Generation polling times out (>10 min) | Screenshot, ask user. Don't restart automatically — Higgsfield may already be processing. |
| Out of credits mid-run | Stop cleanly. Report which shots completed; user can resume after topping up. |
| `assemble-video.py` fails on codec mismatch | The script auto-falls-back to re-encode; if that also fails, the takes are corrupt — re-download. |

For anything else, load `references/playwright-mcp-playbook.md` § Failure recovery.

## Cross-agent compatibility

This skill is agent-agnostic. The same SKILL.md, references, and Playwright MCP server work in:

- **Claude Code** — Playwright MCP installed via `claude mcp add` (see Prerequisites).
- **Codex (OpenAI CLI)** — Playwright MCP via OpenAI MCP support; same `--cdp-endpoint` flag.
- **OpenCode** — Playwright MCP via `.opencode/mcp.json`.

The only platform-specific bit is the slash command in `.claude/commands/higgsfield-autopilot.md` (Claude Code only). For Codex/OpenCode, the user invokes the skill in natural language.

## What this skill does NOT do

- **Prompt design from scratch** — formats prompts per Soul Cinema rules, defers to `docs/skills/skill-higgsfield-shot-designer.md` for theory.
- **Other Higgsfield models** — Soul Cinema only. Veo/Sora/Kling would need their own snapshot-reading logic.
- **Audio generation, lip-sync, character consistency (Soul ID)** — out of scope for v2.
- **Cloud API path** — drives the web UI via MCP. The Cloud API exists but is under-documented (`docs/research/generative-media-orchestration.md` § 2.3.4); migrating would be a future v3.
- **Auto-install dependencies** — the skill checks Prerequisites and stops if anything's missing. The user installs.
