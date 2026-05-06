# Cost Discipline

The agent is spending real money. These are the hard rules.

> **Updated 2026-05-06** after Perplexity deep research + empirical Starter-plan testing. The previous version had rack-rate confirmation thresholds (200 / 1000 credits) that turned out to be 100× off for paid users. This version uses a **capability-check pattern** instead.

## The core insight

`higgs generate cost` is **plan-blind** (upstream issue #1, still open). It returns rack-rate base credits regardless of the user's subscription. On a paid plan, models often absorb at **>99%** — but you can't tell that from the CLI.

**Empirical example (2026-05-06, Starter plan):**
- 6-shot still campaign preflighted at **160 credits**
- Actually billed: **1.6 credits**
- Absorption: ~99%

So the agent's source of truth shifts:
- ❌ **Don't trust** `higgs generate cost` as actual spend
- ✅ **Do trust** `higgs --json account status | jq .credits` deltas before/after

`generate cost` is now an **upper bound for planning**, not an actual cost. Use it to know "this can't possibly cost more than X."

## The capability-check ritual (every spending pattern, every time)

```
1. READ live state    →  higgs --json account status (plan name + credits)
                      →  higgs --json workspace status (active billing context)
2. PLANNING BOUND     →  higgs generate cost <model> --prompt "..."  (rack rate)
3. CAPABILITY CHECK   →  Does the user's balance cover the rack-rate worst case?
                          ├─ Yes → proceed, log preflight estimate
                          └─ No  → check if model is "absorbed" on this plan
                                    → If unknown → ask user to authorize a small calibration spend
                                    → If known absorbed → proceed
                                    → If known not absorbed → stop, report gap
4. SPEND              →  higgs generate create ... --wait
5. MEASURE TRUTH      →  Re-read account status, compute actual delta
6. LOG                →  Save preflight estimate AND actual delta to runs/<date>/cost-log.json
```

**Skip preflight = bug.** Preflight is free; it gives you the rack-rate ceiling. Always run it.

**Skip post-spend balance read = bug.** That's the only way to learn the real cost on the user's plan.

## Workspace billing — non-negotiable check

Before any spending pattern:

```bash
WS=$(higgs --json workspace status | jq -r '.name // "Private"')
echo "Spending will charge: $WS"
```

If the active workspace doesn't match the brief's apparent client (brief says "Acme campaign", workspace says "Private"), **stop and ask the user to switch**:

```bash
higgs workspace list                       # see options
higgs workspace set <id>                   # switch
# Or unset to fall back to personal
higgs workspace unset
```

When a workspace pool exhausts, **assume hard stop** — there's no documented fallback to a personal balance. Run the workspace-aware check on every pattern.

## Confirmation thresholds (capability-aware, not rack-rate)

The previous "confirm at 200 credits" rule fired on every job for paid users (because rack rates inflate). Replaced with this:

| Situation | Action |
|---|---|
| Preflight rack rate ≤ current balance × 0.5 | Silent proceed. Log the estimate. |
| Preflight rack rate > current balance × 0.5 AND ≤ balance | Tell user "rack-rate estimate is X (your plan may absorb most of it). Proceed?" — wait for OK. |
| Preflight rack rate > current balance | **Stop.** Tell user "if your plan doesn't absorb this, you're short by Y credits. Calibration shot first?" |
| Single rack-rate estimate exceeds 5,000 credits regardless of balance | **Itemise breakdown** before asking — even on Ultra-tier accounts, that's a real number worth pausing on |

**Calibration shot** = run ONE cheap (`soul_cinematic` ~12 credits rack) generation, observe actual delta, infer absorption ratio, redo the whole-run estimate with that ratio. Cost: 1-12 credits. Buys you accurate planning for the rest of the run.

## Hard stop — exhausted credits

When `higgs account status` shows balance < estimated worst-case actual:

- **Don't auto-top-up** — that's a user financial decision
- **Don't auto-overage** — Higgsfield doesn't expose one anyway (no auto-billing per extra job)
- **Stop cleanly.** Report what completed. Tell user their options:
  1. Upgrade plan: visit higgsfield.ai pricing
  2. Buy a top-up pack (warns: ~90-day expiry per third-party reports — verify in UI)
  3. Wait for monthly cycle reset (no rollover; balance will be the new month's allocation, not added to remaining)

## Free preview paths (use them aggressively)

These don't burn credits:

| Command | What you get |
|---|---|
| `higgs generate cost <model> --prompt "..."` | Rack-rate planning bound (plan-blind — see issue #1) |
| `higgs --json product-photoshoot create --enhance-only ...` | The AI-enhanced prompt without generation. **Best free preview for product-photoshoot work.** |
| `higgs --json marketplace-cards create --enhance-only ...` | (If supported by current CLI version — verify with `higgs marketplace-cards create --help`) |
| `higgs model get <name>` | Param schema + accepted values |
| `higgs model list --image|--video` | Browse alternatives |
| `higgs --json account status` | Current balance + plan name (display only) |
| `higgs --json workspace status` | Active billing context |
| `higgs upload list --image` | Reuse a previous upload's UUID instead of re-uploading |
| `higgs generate list --size 20` | Did this prompt run successfully recently? Reuse the output URL. |
| `higgs --json account transactions --size 50` | **Ground truth** — actual billed history. Use after spend to reconcile. |

## Failed jobs

Per upstream issue #4 reporter: failed Soul Cast jobs were "free of credit charge". This *appears* to be the general behavior — failed jobs (status = `failed`, including content-policy / nsfw / ip_detected rejections) don't deduct credits. **But there's no formal API guarantee**, no refund mechanism, and no public statement from Higgsfield.

**Agent behavior:**
- Treat failure as zero-cost optimistically — log it, retry once if appropriate
- Read `account status` after a failure to confirm the delta is zero
- If a failure DID deduct credits, log it as a surprise — it's worth flagging upstream

## Top-up packs

Multiple third-party tutorials show the "Buy credits" UI offering preset packs (80, 170, 380, 840, 5,000 credits) with a **90-day validity** mentioned in tutorial transcripts. **This 90-day window is not in Higgsfield's official docs** — treat as `[STALE — verify when you actually buy a pack]`.

Top-ups don't roll over either. They expire on whatever the pack's stated validity is.

For your cost log: track top-ups separately from subscription credits if the user buys them, so it's clear later which pool covered which spend.

## Logging — every run writes a cost ledger

The agent maintains `runs/<RUN_ID>/cost-log.json` per `references/output-management.md`:

```json
{
  "run_id": "2026-05-06-1430",
  "plan": "Starter",                 // display only — don't make decisions on this
  "workspace": "Private",
  "started_at": "2026-05-06T14:30:00Z",
  "brief_path": "skill/higgsfield-autopilot/briefs/example-product-reel.md",
  "pattern": "product-reel",
  "preflight_total_estimate": 612,    // rack-rate, plan-blind
  "shots": [
    {
      "shot_id": 1,
      "model": "soul_cinematic",
      "prompt": "...",
      "preflight_rack_rate": 12,
      "job_id": "abc-123",
      "delta_observed": 0.12,         // actual: balance_before - balance_after for this job
      "absorption_ratio": 0.99,       // computed
      "result_url": "https://cdn.higgsfield.ai/...",
      "local_path": "runs/2026-05-06-1430/shot-01/take-1.png"
    }
  ],
  "balance_before": 208,
  "balance_after": 206.4,
  "actual_spend": 1.6,
  "preflight_estimate": 160,
  "absorption_ratio_run": 0.99,       // 1 - (actual / preflight)
  "delta_vs_estimate": -158.4         // negative = absorbed; positive = exceeded
}
```

Append a one-liner to `runs/cost-summary.json` (top-level rolling ledger) so `/higgsfield-budget` queries are fast.

## Don't bake tier names into logic

Higgsfield's tier names have shifted between Starter/Plus/Ultra (their own April 2026 article) and Free/Basic/Pro/Ultimate/Creator (third-party May 2026 reviews). They will likely shift again.

**Rule:** Use `higgs account status` for the live plan name **for display only**. Don't write code or instructions that conditionally depend on the literal string "Starter" or "Pro" — that will break.

Use **capability checks** instead:
- "Did this generation deduct ≤ 1 credit?" → it's absorbed on this plan
- "Did Soul ID training succeed?" → user has eligible plan
- "Did `generate create` return an error?" → check the error text

## Subscription-aware future

When upstream ships issue #1's fix (`base_credits` + `effective_credits` + `is_unlimited` in CLI output), this whole document gets simpler. Until then, the capability-check ritual is what protects users from both over-spending AND over-cautious refusal-to-spend.

## When the user says "just do it"

The cost-log captures the receipt either way. So the ritual is:
- **First spend per session, regardless:** confirm.
- **Subsequent spends in same session, similar magnitude, user said "stop asking":** can skip explicit confirmation, but still log the preflight estimate.
- **New tier of cost (rack rate >2× of previous in session):** confirmation comes back.
- **Out-of-balance situation:** always confirm even if user said skip.

## Hard rules (refuse to override)

The agent must refuse, not soft-warn, in these cases:

- No active workspace selected when account has multiple → ask which to charge
- Estimated rack rate > balance AND no calibration data exists yet → run calibration shot first
- Single-job rack rate > 5,000 credits → itemise + ask, even if balance covers it
- User says "go" without explicit cost preview → run preflight first

These aren't paranoia — they're scar tissue from systems that auto-spent on bad assumptions.
