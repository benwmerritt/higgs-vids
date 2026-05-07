# Empirical Tests Backlog

The agent runs these to fill in pricing/behavior unknowns when there's slack credits in a paid plan. Each test is **budgeted, scoped, and produces a structured finding** that updates this toolkit's other reference docs.

> **Source:** Section 9 of the Perplexity deep research from 2026-05-06 (`docs/research/higgsfield-pricing-deep-research.md`). Ranked by cost-to-information ratio.
>
> **When to run:** When a `/higgsfield-make` run completes well under-budget and there's >50 credits of slack, OR when the user explicitly asks for one.

## Test 1 — Plan-aware cost validation [HIGHEST PRIORITY]

**Question:** For each model, what's the actual subscriber-absorbed cost on the user's current plan?

**Why it matters:** Issue #1 means `generate cost` is plan-blind. Without this measurement, every cost discussion is fiction.

**Cost:** ~12-50 credits per data point (one image generation per model). Total: ~200 credits to cover the 8 most-used models.

**Procedure:**
1. Read live balance: `BAL_BEFORE=$(higgs --json account status | jq -r '.credits')`
2. For each model in this priority order: `soul_cinematic`, `nano_banana_2`, `gpt_image_2`, `seedream_v4_5`, `flux_2`, `seedance1_5` (video!), `kling3_0` (video!), `cinematic_studio_3_0` (video!):
   - Get rack rate: `RACK=$(higgs --json generate cost <model> --prompt "test calibration shot" | jq -r '.cost')`
   - Submit one generation: `higgs --json generate create <model> --prompt "test calibration shot, simple subject" --aspect_ratio 1:1 --wait`
   - Read balance again: `BAL_AFTER=$(higgs --json account status | jq -r '.credits')`
   - Compute `actual = BAL_BEFORE - BAL_AFTER`
   - Compute `absorption_ratio = 1 - (actual / RACK)`
   - Update `BAL_BEFORE = BAL_AFTER` for next iteration
3. Save findings to `findings/<date>-plan-cost-calibration.md` with table: model, rack rate, actual, ratio.
4. Update `references/cost-discipline.md` with the per-model absorption table for the user's plan.

**Acceptance:** Calibration table written. Three or more models measured. `cost-discipline.md` references it.

**Stop conditions:**
- Balance below 100 credits → stop
- Any single model's actual cost exceeds 50 credits → flag and stop (something's wrong)

---

## Test 2 — Unlimited video model verification

**Question:** Per the April 2026 article, Ultra subscribers can pick **one** of `seedance1_5`, `wan2_6`, `kling2_6`, `nano_banana_2` as 365-day unlimited video. Does that hold? Are there hidden caps (per-day, per-hour, per-resolution)?

**Why it matters:** If Ultra genuinely uncaps a video model, the cost picture changes radically. Ultra at $99/mo could be cheaper than per-clip pricing on Veo direct.

**Cost:** ~5-50 credits if the model is genuinely unlimited (we'd see ~zero deltas). Up to 500-2000 credits if it's not. **Run on Ultra-tier accounts only.**

**Procedure:**
1. Confirm plan via `higgs account status`. If not Ultra-tier (or whatever the current name maps to), skip this test.
2. Check which video model the user has selected as their unlimited pick (if the UI exposes this — may not via CLI).
3. Generate 5 short clips at varying resolutions (480p, 720p, 1080p if supported) and durations (5s, 10s).
4. Check `account transactions` after each — confirm zero or near-zero deduction.
5. Try a different "unlimited" candidate model from the list — does it also absorb? Or does the unlimited status only apply to one choice?

**Acceptance:** Findings doc records: which video model is selected as unlimited; observed absorption ratio; any concurrency or daily caps hit.

---

## Test 3 — Soul ID training cost

**Question:** Does `higgs soul-id create` consume credits, and how much?

**Why it matters:** `patterns/character-campaign.md` warns "may consume credits" — that's not good enough for client work. Need a number.

**Cost:** Unknown — that's literally what the test reveals. Worst-case estimate: 50-200 credits per training based on similar platforms.

**Procedure:**
1. Read balance.
2. Upload 5 photos: `higgs upload create photo{1..5}.jpg`. Capture upload IDs.
3. `higgs --json soul-id create --name "TestRef$(date +%s)" --soul-2 --image <id1> ... --image <id5>` → SOUL_ID
4. `higgs --json soul-id wait $SOUL_ID` → blocks ~3-5 min
5. Read balance. Compute delta.
6. Repeat with `--soul-cinematic` variant if budget allows. Compute delta.
7. Try with 10 photos and 20 photos (separate IDs) — does cost or training quality vary?

**Acceptance:** Findings doc states soul-2 training cost in credits and soul-cinematic training cost in credits. Updates `patterns/character-campaign.md` to give the user an accurate cost estimate.

**Side benefit:** You now have 1-3 trained Soul IDs reusable in future client work.

---

## Test 4 — Marketing Studio cost curve

**Question:** How does `marketing_studio_video` cost change with `--resolution`, `--duration`, `--generate_audio`, and `--mode`?

**Why it matters:** `patterns/quick-social.md` and any future ad-creation pattern need to estimate Marketing Studio cost. Currently we have no data.

**Cost:** ~2000-5000 credits for the full curve (multiple variants). Run only when needed.

**Procedure:**
1. Pick or fetch one product (`higgs marketing-studio products fetch --url <url>` or use a preset).
2. Pick one preset avatar.
3. Run a 2×2×2 matrix: `--resolution {480p,720p}` × `--duration {10,15}` × `--generate_audio {true,false}`. Eight runs.
4. Log balance delta for each.
5. Then try varying `--mode` (`ugc` vs `tv_spot` vs `hyper_motion`) — same params, different mode. Three runs. Log deltas.

**Acceptance:** A small cost matrix in findings doc covering: resolution multiplier, duration multiplier, audio surcharge, mode-dependent variation.

**Stop conditions:** Balance below 1000 credits → run a partial matrix and document what you got.

---

## Test 5 — Batch generation linearity

**Question:** Does `gpt_image_2 --batch_size N` cost N× the single-image rate, or is there a discount?

**Why it matters:** If batches are discounted, agents should batch-submit when generating multiple variants. If linear, batching is purely a UX convenience.

**Cost:** ~50-200 credits depending on plan absorption.

**Procedure:**
1. `RACK_1=$(higgs --json generate cost gpt_image_2 --prompt "x" --batch_size 1 | jq .cost)`
2. `RACK_4=$(higgs --json generate cost gpt_image_2 --prompt "x" --batch_size 4 | jq .cost)`
3. Compare: is `RACK_4` exactly `4 * RACK_1`?
4. Confirm with actual deltas: run both, compare `account status` deltas.

**Acceptance:** Linearity confirmed or discount documented in `references/cli-cheatsheet.md`.

---

## Test 6 — Output URL lifetime

**Question:** How long does a `result_url` from `generate create` remain valid?

**Why it matters:** `references/output-management.md` says "download outputs promptly" but doesn't specify "or it'll be gone in N hours/days". A real number lets us decide retention strategy.

**Cost:** ~12 credits (one generation), spread over multiple days.

**Procedure:**
1. Run one cheap generation. Save `result_url` to a file.
2. After 1 hour: `curl -I "$URL"` → 200?
3. After 24 hours: same.
4. After 7 days: same.
5. After 30 days: same.
6. Note when 200 → 403/404.

**Acceptance:** A "URLs expire after ~N hours/days" number in `references/output-management.md`.

**Note:** This is a longitudinal test, not a single-session run. The agent kicks it off and notes a follow-up date in the findings.

---

## Test 7 — Cross-workspace Soul ID behavior

**Question:** If I create a Soul ID in workspace A, can I use it in workspace B? Does deletion in A remove it from B?

**Why it matters:** Agencies running multiple client workspaces need to know whether to train one Soul ID per character or one per client.

**Cost:** Same as Test 3 (Soul ID training). Plus requires a Business or multi-workspace plan.

**Procedure:**
1. With workspace A active: train a Soul ID per Test 3.
2. Switch to workspace B: `higgs workspace set <B-id>`.
3. List Soul IDs: `higgs soul-id list` — does the workspace-A Soul ID appear?
4. Try generating with it: `higgs generate create text2image_soul_v2 --soul-id <ID> --prompt "test"`. Does it work?
5. Switch back to A. Try `higgs soul-id delete <ID>` (if such a command exists). What happens? Is the Soul ID gone from B too?

**Acceptance:** Cross-workspace Soul ID semantics documented. Updates `patterns/character-campaign.md` for agency users.

**Defer until:** User actually has multi-workspace setup. No point running on a single-workspace personal account.

---

## Test 8 — Comparative per-clip benchmark [LOWEST PRIORITY for Higgsfield-only work]

**Question:** For an identical 5-shot 25-second 9:16 reel, what does Higgsfield, Krea, Magnific, OpenArt, Pika, Runway, and direct-API (Veo via Vertex) cost?

**Why it matters:** Strategic — informs whether Higgsfield is genuinely cheaper or just absorbs aggressively at the marketing level.

**Cost:** Hundreds of dollars across multiple platforms. **Don't run unless specifically commissioned for a build-vs-buy decision.**

**Procedure:** Beyond scope of an agentic test; this is a procurement / strategic exercise. Note in findings if a client ever asks for it.

---

## How to log a completed test

Save findings to `findings/<YYYY-MM-DD>-test-N-<name>.md` with:

1. **Question** — copy from above
2. **Plan tested** — name (display only) + balance at start
3. **Procedure followed** — note any deviations
4. **Raw measurements** — every API call's input/output, balance deltas, error messages
5. **Conclusions** — what we now know
6. **Toolkit changes** — which references / patterns / SKILL.md files updated as a result
7. **Open follow-ups** — questions surfaced but not answered

The agent can self-author this file at the end of a test.

## Don't

- **Don't run a test on a plan that doesn't match the question.** (E.g. don't run Test 2 on Starter — it asks about Ultra.)
- **Don't run two tests in parallel.** They share an account; deltas get muddled.
- **Don't run any test if balance is <2× the test's worst-case cost.** Leaves no buffer for client work.
- **Don't auto-run tests without user OK** — they spend real money. Always confirm.
