# Stage 1 — Cost Preview (No Credits)

> **Invoke:** Claude Code → `/higgsfield-test 1`. Other agents → *"Read `skill/higgsfield-autopilot/test/stage-1.md` and execute it."*

**Cost: 0 credits.** Stops at cost preview. No `higgs generate create` calls — only `higgs generate cost`. Verifies you can authenticate, query the API, expand a brief into a shotlist, and price a full run.

## Pre-conditions

- `higgs` CLI installed (`which higgs`)
- `higgs auth login` completed (`higgs account status` returns OK)
- ffmpeg installed (only matters for stage 3, but check now)

If any are missing, stop and tell the user. Don't install for them.

## Steps

### 1. Verify the toolkit

```bash
higgs version
higgs --json account status > /tmp/acc.json
PLAN=$(jq -r '.plan' /tmp/acc.json)
BAL=$(jq -r '.credits' /tmp/acc.json)
WS=$(higgs --json workspace status 2>/dev/null | jq -r '.name // "Private"')

echo "Plan: $PLAN | Workspace: $WS | Balance: $BAL credits"
```

### 2. Read the skill instructions

In order:
1. `skill/higgsfield-autopilot/SKILL.md`
2. `skill/higgsfield-autopilot/references/cli-cheatsheet.md`
3. `skill/higgsfield-autopilot/references/cost-discipline.md`
4. `skill/higgsfield-autopilot/references/model-selection-guide.md`
5. `skill/higgsfield-autopilot/references/brief-expansion-rules.md`
6. `skill/higgsfield-autopilot/patterns/product-reel.md`

### 3. Read the brief

`skill/higgsfield-autopilot/briefs/example-retro-futuristic.md`.

### 4. Expand into shotlist

Per `references/brief-expansion-rules.md`. 5 shots, 9:16, English prompts. Save to `runs/<YYYY-MM-DD-HHMM>/shotlist.json` (under repo root, NOT under skill bundle).

### 5. Cost preflight (the thing this stage actually tests)

For each shot, query both still + video model costs:

```bash
TOTAL=0
for shot in shots in shotlist; do
  STILL_COST=$(higgs --json generate cost soul_cinematic --prompt "$STILL_PROMPT" | jq -r '.cost // 0')
  VIDEO_COST=$(higgs --json generate cost cinematic_studio_3_0 --prompt "$MOTION_PROMPT" | jq -r '.cost // 0')
  echo "Shot $ID: still=$STILL_COST video=$VIDEO_COST"
  TOTAL=$((TOTAL + STILL_COST + VIDEO_COST))
done
echo "Total estimate: $TOTAL credits"
```

Confirm this is greater than the balance reported in step 1 (it almost certainly is — Cinematic Studio 3.0 is expensive). Note in the report.

Then check a cheaper alternative:

```bash
TOTAL_CHEAP=0
for shot in shots; do
  STILL=$(higgs --json generate cost soul_cinematic --prompt "$STILL_PROMPT" | jq -r '.cost')
  VIDEO=$(higgs --json generate cost kling2_6 --prompt "$MOTION_PROMPT" | jq -r '.cost' 2>/dev/null || echo "N/A")
  TOTAL_CHEAP=$((TOTAL_CHEAP + STILL + VIDEO))
done
echo "Cheap-tier estimate: $TOTAL_CHEAP credits"
```

### 6. Write the report

`runs/<RUN_ID>/stage-1-report.md` with these sections:

1. **Auth + workspace** — plan, workspace, balance
2. **Brief read** — title + first 100 chars
3. **Shotlist** — number of shots + first shot's prompt summary
4. **Mid-tier cost estimate** — shot-by-shot table + total
5. **Cheap-tier alternative** — total + which model swapped (e.g. cinematic_studio_3_0 → kling2_6)
6. **Affordable?** — TOTAL ≤ balance? if not, by how much short
7. **Surprises / recommended changes to SKILL.md or refs** — anything you noticed that didn't match expectations (renamed CLI flags, missing commands, etc.)

Then in chat: `Stage-1 report: <path>`. Done.

## Constraints

- **No `higgs generate create` calls.** Hard rule. `cost` and `model get` only.
- **No `--enhance-only` calls either** in stage 1 (those use `product-photoshoot create` which I want to keep as a stage-2+ test).
- **No commits, no edits to `skill/`** — recommendations go in the report.
- **Stop after 2 attempts** on any single CLI call. If `higgs generate cost` errors twice in a row, log it and continue with placeholder costs in the report.

Begin.
