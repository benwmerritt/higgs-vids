---
description: Cost queries — what did this run cost, what did this workspace spend this month, etc. Argument is optional run-dir path or workspace name. With no argument, summarises the rolling cost-summary.json.
---

Read cost ledgers and report. Argument: `$ARGUMENTS`

## Modes

### No argument
Read `runs/cost-summary.json` (rolling cross-run ledger). Print:
- Total runs
- Total credits spent across all runs
- Breakdown by workspace
- Breakdown by pattern
- Top 5 most expensive runs (with paths)

If `runs/cost-summary.json` doesn't exist, say so and exit cleanly.

### Argument is a path to a run dir (e.g. `runs/2026-05-06-1430`)
Read `<path>/cost-log.json`. Print:
- Brief title + pattern
- Workspace + balance before/after
- Per-shot breakdown (shot id, model, prompt summary, estimated cost, actual delta)
- Total spend
- Path to deliverables/

### Argument is a workspace name (e.g. "Acme")
Filter `runs/cost-summary.json` for entries matching that workspace. Aggregate:
- Total runs for that workspace
- Total spend for that workspace
- Pattern breakdown
- Recent runs (last 10)

## Live balance

Always also report current live balance from:
```bash
higgs --json account status | jq '{plan, credits}'
```

So the user can see what they still have to spend.

## Output format

Plain text, scannable. Tables where appropriate. No JSON dumps unless the user explicitly asked for raw.

Example:
```
Workspace: Acme
Total runs: 12
Total spend: 8,420 credits
Patterns:
  product-reel: 7 runs, 7,200 credits
  quick-social: 4 runs, 800 credits
  multi-platform-render: 1 run, 420 credits

Recent runs:
  2026-05-06-1430  product-reel        612 credits  → runs/2026-05-06-1430/deliverables/
  2026-05-05-0930  quick-social         48 credits  → runs/2026-05-05-0930/deliverables/
  ...

Live balance: 1,580 credits (Plan: Pro)
```
