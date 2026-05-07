---
description: Make videos/images from a brief using the Higgsfield CLI. Argument is a brief file path or an inline brief. Defaults to skill/higgsfield-autopilot/briefs/example-retro-futuristic.md if no argument given. Reads SKILL.md, picks a pattern, runs cost preflight, executes, delivers.
---

You're about to run the Higgsfield video toolkit on a brief. Argument: `$ARGUMENTS`

## Resolve the brief

- If `$ARGUMENTS` is a path that exists → read it as the brief
- If `$ARGUMENTS` is non-empty but not a path → treat as inline brief content
- If `$ARGUMENTS` is empty → use `skill/higgsfield-autopilot/briefs/example-retro-futuristic.md`

## Load instructions

Read in order:
1. `skill/higgsfield-autopilot/SKILL.md` — your operating manual
2. `skill/higgsfield-autopilot/references/cli-cheatsheet.md`
3. `skill/higgsfield-autopilot/references/cost-discipline.md`
4. `skill/higgsfield-autopilot/references/model-selection-guide.md`
5. `skill/higgsfield-autopilot/references/output-management.md`
6. `skill/higgsfield-autopilot/patterns/README.md` (decision tree)
7. The specific `patterns/<name>.md` you'll execute

Then follow SKILL.md's 8-step workflow.

## Pre-flight check

Before reading the brief, confirm setup:

```bash
higgs --json account status > /tmp/acc.json 2>&1 || { echo "Not authenticated. Run /higgsfield-init first."; exit 1; }
```

If auth fails or balance is suspiciously low (e.g. <50 credits and the brief obviously needs more), tell the user upfront before doing any work.

## Cost discipline (mandatory)

Per `references/cost-discipline.md`:
- ALWAYS run `higgs generate cost ...` before `higgs generate create ...`
- For estimates >200 credits, ask explicit confirmation before spending
- For estimates >1000 credits, itemise the breakdown
- For estimates >balance, stop

## Final report

When the run completes (or partially completes), report concisely:
- Path to `runs/<RUN_ID>/deliverables/<headline-file>`
- Total spend (balance_before − balance_after)
- Number of shots, total duration if video
- Any failures or surprises

Don't summarise the whole run if it succeeded — just point at the deliverable. The user reads it themselves.
