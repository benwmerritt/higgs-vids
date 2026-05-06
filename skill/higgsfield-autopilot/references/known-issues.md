# Known Issues — Higgsfield CLI & Platform

Tracks upstream bugs and limitations the agent should route around. Updated when we learn new things from research, empirical tests, or upstream fixes.

> **Last reviewed:** 2026-05-06 (after Perplexity deep-research integration)
> **CLI version reviewed against:** `@higgsfield/cli@0.1.28`

## Active issues (avoid / work around)

### Issue #1 — `generate cost` is plan-blind

**Upstream:** [`higgsfield-ai/cli` issue #1](https://github.com/higgsfield-ai/cli/issues/1) — opened 2026-05-04, still **open**.

**What it does:** `higgs generate cost <model> --prompt "..."` returns the **rack-rate base credits** regardless of the user's plan. A model marked `UNLIMITED` in the web UI for a Plus subscription still shows nonzero credits via CLI cost. There is no `effective_credits`, `is_unlimited`, or `billing_mode` field anywhere in CLI output.

**Our empirical confirmation:** On a Starter subscription, a 6-shot still campaign that preflighted at 160 credits actually billed 1.6 credits — **~99% absorption, 100× discrepancy**. See `findings/2026-05-06-starter-plan-empirical-findings.md`.

**Workaround the agent must use:**
1. Use `higgs --json generate cost ...` for *planning bounds only* — it's a rack-rate upper bound.
2. Treat `higgs --json account status | jq .credits` before/after a job as **ground truth** for actual spend.
3. Log both numbers (preflight estimate + actual delta) per `references/cost-discipline.md`.
4. Don't refuse to run a job just because preflight is high — it may absorb to near-zero on the user's plan.

**When to revisit:** When upstream merges plan-aware fields. Re-run plan-aware cost validation experiment from `references/empirical-tests.md`.

---

### Issue #2 — Canvas workflows not exposed via CLI/MCP/REST

**Upstream:** [`higgsfield-ai/cli` issue #2](https://github.com/higgsfield-ai/cli/issues/2) — opened 2026-05-04, **open**.

**What's missing:** Higgsfield's **Canvas** node-graph workflow surface (multi-step pipelines composed in the web UI) is not accessible programmatically. CLI / MCP / REST only expose single-model calls.

**Implication for us:** Any user with an existing Canvas workflow can't trigger it from the agent. Our toolkit must continue composing pipelines as bash sequences of single-model calls (which is what our patterns already do).

**When to revisit:** When upstream ships `higgsfield canvas pull/push/run` or equivalent. Could replace some of our patterns with thinner Canvas-runner wrappers.

---

### Issue #3 — Windows `npm install -g @higgsfield/cli` fails

**Upstream:** [`higgsfield-ai/cli` issue #3](https://github.com/higgsfield-ai/cli/issues/3) — opened 2026-05-04, **open**.

**What's broken:** On Windows, `npm install` runs the postinstall script which calls `tar -xzf` without `--force-local`, causing it to misinterpret `C:\...` paths as remote specs.

**Workaround:**
- Use **WSL** (Windows Subsystem for Linux) or **Git Bash**, install via npm there.
- Or `npm install -g @higgsfield/cli --ignore-scripts` then manually extract the binary from the package (advanced).

**Implication for our toolkit:** We document this in `INSTALL.md`. The agent should detect Windows + native cmd/powershell and warn the user upfront if `which higgs` returns "not found" on a Windows host.

---

### Issue #4 — `soul_cast` ignores `--prompt` object schema

**Upstream:** [`higgsfield-ai/cli` issue #4](https://github.com/higgsfield-ai/cli/issues/4) — opened 2026-05-04, **open**.

**What's broken:** `soul_cast` declares `prompt` as `object` type in its schema. The CLI treats `--prompt` as string only, doesn't accept `@file.json`, silently submits empty `character_params`. Result: jobs run with random AI-generated character descriptions, or fail outright.

**Workaround:** **Don't use `soul_cast` at all** for now. For Soul-driven video, use:
- `cinematic_studio_3_0` with `--image <still-job-id>` (where the still was generated with `text2image_soul_v2 --soul-id`)
- Or `kling3_0` with `--start-image <still-job-id>` (cheaper alternative)

Both pipe a Soul-faithful still into a video model that takes images as start frames.

Failed `soul_cast` jobs do **not** appear to deduct credits (per upstream reporter), so accidental use isn't a billing risk — just produces garbage.

**When to revisit:** When upstream supports object-typed params or adds `--prompt-file`.

---

## Documentation gaps (research couldn't answer; needs empirical testing)

These aren't bugs — they're things upstream simply hasn't documented. The agent should treat them as unknowns and log behavior when encountered.

| Gap | Where it bites |
|---|---|
| Per-model rack rate for video models | `model-selection-guide.md` defaults are best-guess; calibrate per `references/empirical-tests.md` Test 2 |
| Soul ID training credit cost (free? modest fee? plan-tier-dependent?) | `patterns/character-campaign.md` warns user "may consume credits" — measure on first run |
| Top-up pack expiry (third-party says ~90 days, no official confirmation) | `references/cost-discipline.md` warns user; verify when first pack purchased |
| Asset URL retention (signed URLs eventually expire, exact duration unknown) | The agent already downloads outputs immediately; not a current blocker |
| Cross-workspace Soul ID sharing | Out of scope until business workspaces are in play |
| Marketing Studio audio surcharge (`--generate_audio true`) | Measure when first marketing video runs |
| Batch generation discount (we assume linear; unverified) | `gpt_image_2 --batch_size N` — measure during empirical test |
| Per-minute / per-day API rate limits | Only concurrency is documented per plan tier; trust `--wait` and exponential backoff |
| Webhook support | None exists — polling is the only path |
| Refund mechanism for failed jobs | No formal API; failed jobs *appear* to not deduct credits but no guarantee |

## Resolved / no longer relevant

(Empty — nothing has been fixed upstream since the issues were filed 2026-05-04. Update as upstream ships fixes.)

## How the agent uses this file

When something behaves unexpectedly:

1. Check this file first. Is the behavior a known issue?
2. If yes → apply the documented workaround. Don't try to fix Higgsfield.
3. If no → log the surprise to the run report's "Surprises" section. Future research / empirical test may codify it as a new entry here.

This file is **descriptive** of upstream state, not prescriptive — it's the agent's reference for "is this a Higgsfield bug or am I doing something wrong?"
