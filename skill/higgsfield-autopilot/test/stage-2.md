# Stage 2 — Single-Shot Real Generation

> **How to invoke this:**
> - **Claude Code:** `/higgsfield-test 2`
> - **Any other agent:** tell it: *"Read `skill/higgsfield-autopilot/test/stage-2.md` and execute it."*

**Cost: ~20–32 credits** (one Soul Cinema 9:16 batch of 4 generations). Do NOT run this stage unless you've already passed stage 1, and do NOT run it if you don't have credits to spare.

**Purpose:** Verify the full generation flow for a single shot — submit, poll, download takes, save to disk. Exercises every part of the production pipeline except multi-shot orchestration and final ffmpeg assembly.

**Pre-condition:** Stage 1 has passed in this same browser session in the last hour. The model picker is known to work; we're not re-validating that.

---

## Setup that should already be true

Same as stage 1: Chrome on :9222, signed in, MCP tools visible.

Additionally: `runs/<YYYY-MM-DD-HHMM>/shotlist.json` exists from a recent stage-1 run, OR you'll generate a fresh one.

## What to do

### 1. Read the skill instructions

`skill/higgsfield-autopilot/SKILL.md` and `skill/higgsfield-autopilot/references/playwright-mcp-playbook.md`. Skim if recently read.

### 2. Acquire a shotlist

Either reuse the most recent `runs/*/shotlist.json` (sort by mtime) or create a fresh one for `briefs/example-retro-futuristic.md` per `brief-expansion-rules.md`. Save under `runs/<YYYY-MM-DD-HHMM>/shotlist.json`.

### 3. Verify session

Same as stage-1 step 4. If logged out, stop.

### 4. Confirm Soul Cinema is selected

If you did stage 1 in this same browser session within the last hour, the model is probably already set. Re-snapshot to confirm. If not Soul Cinema, switch (stage-1 step 5).

### 5. Submit shot 1 — live cost confirmation

- Fill prompt 1 from the shotlist via `browser_type`.
- Set aspect 9:16, batch 4.
- Read the cost preview via `browser_evaluate` (same JS as stage 1).
- **Tell the user the cost** and **wait for explicit confirmation** before clicking Generate. Example phrasing:
  > "About to spend ~24 credits on shot 1. Confirm to proceed?"
- Only proceed after the user says yes.

### 6. Click Generate, poll for completion

- `browser_click` the Generate button.
- Wait 30 seconds (`browser_wait_for(time=30)`).
- Loop, max 20 iterations:
  - `browser_evaluate("() => /generating|pending|queued/i.test(document.body.innerText)")` — true if still generating
  - If false → break out; generations are done
  - If true → wait another 30s
- If 20 iterations pass without completion, screenshot, stop, ask the user.

### 7. Extract asset URLs

After completion, `browser_evaluate`:

```js
() => Array.from(document.querySelectorAll('video, img'))
        .map(e => e.currentSrc || e.src)
        .filter(u => u && u.startsWith('http'))
```

Filter for the 4 newest URLs (highest in the History grid, or compare against a baseline you snapshotted before submission).

If results are `blob:` URLs only, wait 5s and retry. If still blob, fall back to `browser_network_requests()` and grep responses for `*.mp4` from `cdn.higgsfield.ai` or similar.

### 8. Download the takes

For each of the 4 URLs:

```bash
mkdir -p runs/<date>/shot-01
curl -sL "$URL" -o runs/<date>/shot-01/take-K.mp4
```

Verify each file is non-zero bytes (`stat -f %z` on macOS or `wc -c`).

### 9. Write the report

`runs/<date>/stage-2-report.md` with these sections:

1. **Submission** — prompt sent, aspect, batch, boost setting, click outcome
2. **Polling** — total wait time, number of polls, any in-progress / failed states observed
3. **Asset extraction** — what `browser_evaluate` returned, how many URLs were valid HTTPS, fallback used (if any)
4. **Download** — file paths, sizes in bytes, durations (use `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <file>`)
5. **Total credit spend** — read the live credit balance before vs after if possible (a single `browser_evaluate` of the credit display)
6. **Surprises + recommended SKILL.md changes** — same format as stage-1

Then in chat: `Stage-2 report: <path>`.

## Constraints

- **One shot only.** Do not generate shots 2–5.
- **Wait for explicit user confirmation** before clicking Generate.
- **Hard cap: 30 minutes total wall-clock.** If you're past 30 min, stop and report whatever state you got to.
- **Do not commit. Do not edit skill/. Do not install anything.**

Begin.
