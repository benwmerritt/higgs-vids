# Cost Discipline

The agent is spending real money. These are the hard rules — never skip them.

## The four-step ritual (every generation, every time)

```
1. PREFLIGHT  →  higgs generate cost <model> --prompt "..."          (free)
2. SUM        →  total = sum of preflight costs across all shots
3. CONFIRM    →  if total > threshold, ASK USER before proceeding
4. SPEND      →  higgs generate create ... --wait                     (commits credits)
```

**Skip preflight = bug.** No exceptions.

## Confirmation thresholds (defaults — patterns may override)

| Estimated total | Action |
|---|---|
| < 50 credits | Proceed silently, log the estimate in the run report |
| 50–200 credits | Tell the user the estimate; proceed unless they object within the response |
| 200–1000 credits | **Pause for explicit confirmation**: "About to spend ~X credits on Y. Confirm?" |
| > 1000 credits | **Itemise the breakdown** (per shot, per model) before asking — the user needs to see what they're approving |
| > current balance | **Stop.** Tell the user the gap. Do not partially-execute. |

## Free preview paths (use them aggressively)

These don't burn credits — use them to refine before spending:

| Command | What you get |
|---|---|
| `higgs generate cost <model> --prompt "..."` | Per-call cost estimate |
| `higgs product-photoshoot create --enhance-only ...` | The AI-enhanced prompt, without generation |
| `higgs marketplace-cards create --enhance-only ...` (if supported) | Same for marketplace cards |
| `higgs model get <name>` | Param schema — verify flags before constructing a call |
| `higgs model list --image\|--video` | Browse alternatives |
| `higgs account status` | Current balance + plan |
| `higgs workspace status` | Current billing context |
| `higgs upload list --image` | Reuse a previous upload instead of re-uploading |
| `higgs generate list --size 20` | Did this prompt already run successfully? Reuse the output URL. |

## Workspace billing — the silent footgun

If the user has multiple workspaces (agency with per-client workspaces), spending without verifying active workspace charges the wrong client.

**Always run `higgs workspace status` at the start of any spending pattern.** If the active workspace doesn't match the brief's apparent client, **stop** and ask which workspace to charge.

```bash
ACTIVE=$(higgs --json workspace status | jq -r '.name')
echo "Active workspace: $ACTIVE"
# If brief says "Acme campaign" and ACTIVE is "Private" — pause.
```

## Subscription-aware pricing (caveat — upstream issue #1)

The CLI doesn't yet flag which models are included-on-plan vs. credit-deducting. A Pro subscriber may have certain models "free" within a quota that the CLI still reports as costing credits.

**Mitigation:**
- Always cross-reference `account status` (returns plan name) with the user's expectation
- If the user has a paid plan, mention this caveat in the run report ("Estimated 1,500 credits — your Pro plan may absorb some of this")
- Reconcile with `account transactions --size 50` after the run

## Logging — every run writes a cost ledger

The agent maintains a per-run JSON log at `runs/<date>/cost-log.json` with this shape (the agent writes this inline; no helper script needed):

```json
{
  "run_id": "2026-05-06-1430",
  "workspace": "Private",
  "started_at": "2026-05-06T14:30:00Z",
  "brief_path": "skill/higgsfield-autopilot/briefs/example-product-reel.md",
  "pattern": "product-reel",
  "preflight_total_estimate": 612,
  "shots": [
    {
      "shot_id": 1,
      "model": "soul_cinematic",
      "prompt": "...",
      "preflight_estimate": 12,
      "job_id": "abc-123",
      "actual_cost_inferred": 12,
      "result_url": "https://cdn.higgsfield.ai/...",
      "local_path": "runs/2026-05-06-1430/shot-01/take-1.png"
    }
  ],
  "balance_before": 8000,
  "balance_after": 7388,
  "actual_spend": 612,
  "delta_vs_estimate": 0
}
```

`balance_before` / `balance_after` come from `higgs --json account status | jq .credits` calls bracketing the run. `actual_spend = balance_before - balance_after` (this is the ground truth — `preflight_total_estimate` is just an estimate).

The agent appends a one-line summary to `runs/cost-summary.json` (a top-level rolling ledger across all runs) so `/higgsfield-budget` queries are fast.

## Hard limits (refuse to override)

The agent must refuse, not soft-warn, in these cases:

- **No active workspace selected and the user's account has multiple** → refuse, ask which to charge
- **Estimated cost exceeds balance** → refuse, report gap
- **Pattern would generate >5,000 credits in one go without explicit user OK** → refuse, itemise + ask
- **User says "go" without seeing a cost preview** → refuse, run preflight first

## When the user says "just do it"

Some users will get impatient with confirmation prompts. The right response:
- **First time per session:** confirm anyway. Set the precedent.
- **Subsequent runs in same session, similar cost range:** can skip confirmation IF user explicitly said "stop asking, just keep going" — but always log the cost estimate so they can audit later.
- **Costs jump to a new tier:** confirmation comes back, even if user said "just do it."

The cost log is the receipt. Even if the agent doesn't ask, the user can always check `runs/<date>/cost-log.json`.
