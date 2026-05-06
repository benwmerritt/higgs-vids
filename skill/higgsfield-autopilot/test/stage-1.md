# Stage 1 — Dry Run (No Credits)

> **How to invoke this:**
> - **Claude Code:** `/higgsfield-test 1` (or just `/higgsfield-test` — stage 1 is the default)
> - **Any other agent (Gemini, Codex, OpenCode, …):** tell it: *"Read `skill/higgsfield-autopilot/test/stage-1.md` and execute it."*

**Cost: 0 credits.** This stage stops at the cost-preview step. You will NOT click Generate. You will NOT spend any Higgsfield credits.

**Purpose:** Verify the autopilot can navigate Higgsfield, select Soul Cinema, fill a prompt, and read the live cost preview — all the steps that *would* lead to a generation, without actually generating.

---

## Setup that should already be true

Before you begin, these things should already be in place. Don't re-do them:

- Real Chrome is open at `higgsfield.ai/canvas` with `--remote-debugging-port=9222` (started via `bash skill/higgsfield-autopilot/scripts/launch-browser.sh --bg`)
- Higgsfield account is already signed in (persistent profile at `skill/higgsfield-autopilot/auth/user-data/`)
- A Playwright MCP server is registered and exposes browser-control tools (names: `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_evaluate`, `browser_wait_for`, `browser_take_screenshot`, `browser_tabs`, `browser_network_requests`)

If the MCP browser tools aren't visible to you, **stop now and report that** — there's nothing to test until they're connected.

If the Chrome window isn't running on port 9222 (`lsof -i :9222 -sTCP:LISTEN` is empty), **stop and tell the user** to run `bash skill/higgsfield-autopilot/scripts/launch-browser.sh --bg` first.

## What to do

### 1. Read the skill instructions

In order:

1. `skill/higgsfield-autopilot/SKILL.md`
2. `skill/higgsfield-autopilot/references/playwright-mcp-playbook.md`
3. `skill/higgsfield-autopilot/references/brief-expansion-rules.md`

### 2. Read the brief

`skill/higgsfield-autopilot/briefs/example-retro-futuristic.md` — the verbatim brief from the original Instagram reel.

### 3. Expand the brief into a shotlist

Per `references/brief-expansion-rules.md`, produce a shotlist JSON with **5 shots**, **9:16 aspect**, English prompts. Save it to `runs/<YYYY-MM-DD-HHMM>/shotlist.json` (create the run dir under the **repo root**, NOT under the skill bundle). Use today's date and current time.

### 4. Verify session via MCP

- `browser_navigate(url="https://higgsfield.ai/canvas")`
- `browser_snapshot()`
- Confirm in the snapshot:
  - Side-nav contains "Cinema Studio" and/or "Assets" (workspace-only items)
  - There is NO visible "Login" or "Sign up" button at the top right
- If session looks logged out → **STOP** and tell the user. Do not proceed.

### 5. Land in the Image generator with Soul Cinema selected

- Click the "Image" tab in the top nav.
- Re-snapshot.
- Find one of these (in preference order):
  - The "Soul Cinema is here" promotional card on the left → click it (single-click switch)
  - The model pill at bottom-left of the prompt panel showing the current model (e.g. "Nano Banana Pro") → click it, then click "Soul Cinema" in the dropdown
- Verify by `browser_evaluate` that the page text now references "Soul Cinema" as the active model.

If neither path works after one retry, take a `browser_take_screenshot` and stop with a clear description.

### 6. Cost preview (NO submission)

For shot 1 only:

- Find the prompt textbox (placeholder: "Describe the scene you imagine"). `browser_type` shot 1's prompt.
- Set aspect ratio to 9:16.
- Set batch size to 4.
- Read the credit cost preview near the Generate button:

```js
() => {
  const m = document.body.innerText.match(/(\d+)\s+credits?/i);
  return m ? parseInt(m[1], 10) : null;
}
```

via `browser_evaluate`.

**DO NOT click the Generate button.** This is the hard stop.

### 7. Write the report

Write `runs/<YYYY-MM-DD-HHMM>/stage-1-report.md` containing exactly these six sections:

1. **Auth check** — pass / fail, with which workspace nav items you saw
2. **Soul Cinema selection** — pass / fail, which path (promo card vs dropdown), how many clicks
3. **Cost preview** — per-generation cost, multiplied by 4 (batch) × 5 (shots) = estimated total
4. **Surprises** — anything in the actual UI that didn't match SKILL.md (renamed buttons, missing controls, extra modals, snapshot quirks)
5. **Tool call count** — rough breakdown by tool name (e.g. `browser_navigate: 1`, `browser_snapshot: 4`, `browser_click: 3`, …)
6. **Recommended changes to SKILL.md or the playbook** — concrete diffs you'd make if anything was unclear or wrong

Then in chat, just say: `Stage-1 report: <path>`. The user will read the report.

## Constraints

- **No generations. No credits spent.** Hard stop at cost preview.
- **Narrate each step briefly** so the user can intervene.
- **Stop after 2 attempts on any single step.** Don't burn time guessing — flag and screenshot.
- **Do not edit any files in `skill/higgsfield-autopilot/`** — recommendations go in the report.
- **Do not commit anything to git.**
- **Do not install anything.** If something's missing, stop and report.

Begin.
