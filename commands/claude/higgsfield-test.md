---
description: Run a higgsfield-autopilot test stage. Argument is "1" (default — cost preview only, 0 credits), "2" (single shot, ~12 credits), or "3" (full reel, varies by tier). Reads test/stage-N.md and executes.
---

You're running a test stage. Argument: `$ARGUMENTS`

## Stage selection

Parse `$ARGUMENTS`:
- empty / `1` / `stage-1` / `stage1` → stage 1 (cost preview, 0 credits)
- `2` / `stage-2` / `stage2` → stage 2 (single shot, ~12 credits)
- `3` / `stage-3` / `stage3` → stage 3 (full reel)
- anything else → list valid options and stop

Then read the matching file and execute as instructed:
- Stage 1 → `skill/higgsfield-autopilot/test/stage-1.md`
- Stage 2 → `skill/higgsfield-autopilot/test/stage-2.md`
- Stage 3 → `skill/higgsfield-autopilot/test/stage-3.md`

Each stage file is a self-contained prompt with its own constraints and reporting requirements.

## Pre-flight

Before any stage:
```bash
higgs --json account status > /tmp/acc.json 2>&1 || {
  echo "Not authenticated. Run /higgsfield-init first."
  exit 1
}
```

For stages 2 and 3, also check balance:
```bash
BAL=$(jq -r '.credits' /tmp/acc.json)
# stage 2 needs ~12 credits
# stage 3 needs ~600+ credits depending on tier
```

If balance is below the stage's minimum, tell the user and stop. Don't partially-execute.

## After completion

Stage files write `runs/<RUN_ID>/stage-N-report.md`. After it's written, just tell the user:
> `Stage-N report: <path>`

The user reads the report themselves. Don't summarise unless they ask.
