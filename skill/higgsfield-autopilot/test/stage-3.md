# Stage 3 — Full Campaign Smoke Test

> **How to invoke this:**
> - **Claude Code:** `/higgsfield-test 3`
> - **Any other agent:** tell it: *"Read `skill/higgsfield-autopilot/test/stage-3.md` and execute it."*

**Cost: ~100–160 credits** (5 shots × 4 batches × ~5–8 credits/gen). This is the real deal. Do NOT run this until both stage 1 and stage 2 have passed in this same browser session.

**Purpose:** End-to-end smoke test — execute the full SKILL.md workflow on the example brief, producing `runs/<date>/final.mp4`. This is the production path; if it works, the skill is ready for real use.

---

## Setup that should already be true

Same as stages 1 and 2: Chrome on :9222, signed in, MCP tools visible.

Plus: stages 1 and 2 have both passed recently in this browser session, AND ffmpeg is on PATH (`which ffmpeg`).

## What to do

### 1. Read the full skill

`skill/higgsfield-autopilot/SKILL.md` end-to-end. The 10 steps in the workflow are exactly what you'll execute.

### 2. Read the playbook

`skill/higgsfield-autopilot/references/playwright-mcp-playbook.md` — pay attention to the polling pattern and asset-download recipe. For 5 shots you'll do this 5 times (or in parallel via tabs — see SKILL.md step 6).

### 3. Pre-flight

- Verify session (stage-1 step 4 logic).
- Confirm Soul Cinema is selected (stage-1 step 5 logic).
- Read the shotlist's brief and produce `runs/<YYYY-MM-DD-HHMM>/shotlist.json` if not already present.
- **Sum the cost preview across all 5 shots** (per-generation × 4 × 5). **If > 200 credits, ask user to confirm the total before proceeding.** Otherwise just report the estimate and continue.

### 4. Generate all 5 shots

Choose a strategy based on agent + browser comfort:

**Sequential (safest, slowest):** for each shot in order, fill prompt → click Generate → poll → extract URLs → download → next shot.

**Parallel via tabs (faster, more complex):** open up to 5 tabs via `browser_tabs(action="new")`, submit one shot per tab, then round-robin poll. Only use if you're confident in tab management.

Either way: download each shot's 4 takes to `runs/<date>/shot-<NN>/take-{1..4}.mp4` as soon as that shot completes (don't batch downloads — risk losing them if a later shot fails).

### 5. Pick best take per shot

For each shot, inspect the 4 takes (use vision capability if available, or sample frames with `ffmpeg -i take-K.mp4 -vf "select=eq(n\,0)" -vframes 1 /tmp/preview-K.png` and look at them).

Symlink the chosen take:
```bash
ln -sf take-2.mp4 runs/<date>/shot-NN/take-best.mp4
```

If vision-pick isn't feasible, default to `take-1` for every shot and note this in the report.

### 6. Assemble the final video

```bash
python skill/higgsfield-autopilot/scripts/assemble-video.py \
    --run-dir runs/<date> \
    --crossfade-ms 250 \
    --force
```

Verify `runs/<date>/final.mp4` exists and is playable (`ffprobe` returns a non-zero duration).

### 7. Write the report

`runs/<date>/stage-3-report.md` with these sections:

1. **Generation summary** — table of all 5 shots: prompt summary, time-to-complete, success/fail, take chosen
2. **Total credit spend** — actual credits used (live balance before vs after)
3. **Final video** — path, duration, dimensions (`ffprobe`), file size
4. **Failures + recoveries** — anything that needed a retry, and how the agent recovered
5. **Tool call count** — rough breakdown by tool, plus number of bash subprocess calls
6. **Recommended changes** — concrete diffs to SKILL.md / playbook / scripts based on what you learned
7. **Open questions** — things the test couldn't resolve (e.g. audio support, Soul ID, headless mode, credit-cost-per-model accuracy)

Then in chat: `Stage-3 report: <path>. Final video: <path>.`

## Constraints

- **Confirm total cost before starting** if estimate exceeds 200 credits.
- **Hard cap: 60 minutes total wall-clock.** If past 60 min, stop and report whatever state you reached. Do not let one stuck shot block the whole run — abort that shot and continue with the others.
- **If a shot fails mid-generation, mark it failed in the report and continue.** Better a 4-shot final than no final at all.
- **Do not commit. Do not edit skill/ files** (you can edit your run-dir freely). **Do not install anything.**

Begin.
