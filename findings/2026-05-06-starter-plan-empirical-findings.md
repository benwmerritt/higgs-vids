# Empirical Findings — Higgsfield Starter Plan, 2026-05-06

> Captures what we measured during the first paid test run of `higgs-vids`, so a future deep-research output can be reconciled against actual observed numbers rather than inferred ones.

## Account state

- **Plan:** Starter (lowest paid tier offered at the time of testing)
- **Email:** [redacted]
- **Workspace:** Private (default)
- **Balance at start:** 208 credits
- **Balance at end:** 206.4 credits
- **Net delta:** -1.6 credits across 6 image generations

## What we ran

A 6-shot still-image campaign per `patterns/product-reel.md` (image-only, no video step), brief `briefs/example-retro-futuristic.md`. Run dir: `runs/2026-05-06-1428/`.

| Shot | Model | Aspect | Resolution | Preflight (credits) | Actually billed (credits) | Absorption |
|---|---|---|---|---|---|---|
| 1 — establish | `soul_cinematic` | 9:16 | 1152×2048 | 12 | 0.12 | 99% |
| 2 — subject_intro | `soul_cinematic` | 9:16 | 1152×2048 | 12 | 0.12 | 99% |
| 3 — object_detail | `soul_cinematic` | 9:16 | 1152×2048 | 12 | 0.12 | 99% |
| 4 — motion | `soul_cinematic` | 9:16 | 1152×2048 | 12 | 0.12 | 99% |
| 5 — closer | `soul_cinematic` | 9:16 | 1152×2048 | 12 | 0.12 | 99% |
| Hero (control) | `nano_banana` | 9:16 | 1152×2048 | 100 | ~1.0 | 99% |
| **Total** | | | | **160** | **1.6** | **99%** |

## What this proves

1. **`higgs generate cost` returns rack rate, not subscriber-absorbed rate.** Even though our paid Starter plan absorbs 99% of the actual cost, the preflight estimator is plan-blind. (Confirms upstream issue #1.)
2. **Absorption ratio is consistent across at least two image models** (`soul_cinematic` and `nano_banana`). Both showed ~99% absorption. This suggests it's a tier-wide policy, not per-model, at least for image generation.
3. **`account transactions` is the only ground truth** for actual spend on a paid plan. Preflight is fiction.
4. **Our cost-discipline thresholds (200/1000 credits) are essentially never triggered** for Starter-plan users on image work. They were calibrated for free-tier rack rates.

## What this DOESN'T prove (open questions for deep research)

1. **Video models — completely unknown.** No video generations were run in this test. The cheapest video model (`seedance1_5`) lists 480 rack-rate credits per generation. If absorption holds at 99%, that's ~4.8 actual credits per video. If video isn't subject to the same absorption, it's ~480 actual. The two scenarios differ by 100×. We can only learn this by running ONE video shot.
2. **Higher-tier absorption** — does Pro absorb more than Starter? Is there a tier where rack rate = actual rate?
3. **Premium model absorption** — `nano_banana_2` (Pro), `gpt_image_2 --quality high`, `flux_2 --model max` — do these still absorb at 99% or do they break the pattern?
4. **Generation count caps** — can we run 1000 image generations per month on Starter, or is there a hard cap somewhere?
5. **Audio surcharge** — `--generate-audio true` on `marketing_studio_video` and Veo — surcharge structure unknown.
6. **Resolution surcharge** — `--resolution 4k` on image models — does this break absorption?

## Quality observations (separate from pricing)

Things to feed into pattern improvements (continuity, etc.) — not pricing-related but worth recording:

- **Shot 2 continuity miss:** the established "retro-futuristic capsule car" became a "vintage wagon" in shot 2. Brief expansion paraphrased the vehicle description instead of carrying it verbatim.
- **Shot 5 framing diverged:** brief specified "reclining on hood", model produced a tighter subject crop. Likely under-specified composition or model under-followed.
- **Face drift across subject shots:** no Soul ID was trained, so the model in shots 2 and 5 is a different person each time. Predictable and documented in `patterns/product-reel.md` failure handling.
- **Nano Banana hero comparison was useful:** the agent improvised running the same prompt through `nano_banana` as a control. Result: the Nano Banana frame was the strongest single image in the set (lush wildflower foreground, better composition). Worth promoting to a `hero-comparison` pattern that runs the same shot through 2-3 image models for picking.

## Implications for the toolkit

Things to update in `skill/higgsfield-autopilot/` once deep research returns:

1. `references/cost-discipline.md` — replace rack-rate thresholds with tier-aware calculation. Add calibration step: first paid run computes the absorption ratio and persists it.
2. `references/model-selection-guide.md` — add a "subscriber-effective cost" overlay column.
3. `patterns/product-reel.md` — add a continuity self-check step before submission. Subject + key-object descriptions must be **verbatim identical** across shots, not paraphrased.
4. `references/brief-expansion-rules.md` — codify the verbatim-continuity rule (currently says "reuse" which the agent interpreted as "paraphrase loosely").
5. New pattern `hero-comparison.md` (or fold into `quick-social.md`) — same prompt through 2-3 image models, contact sheet, user picks best.

## Cost of this learning

**1.6 credits.** ~$cents on a $20-ish/month Starter plan. 100× cheaper than predicted. The toolkit's run-level cost ledger captured the actual spend correctly — that part of the design works.

The bigger learning, in dollar-equivalent terms: knowing that we spent ~1.6 credits on 6 high-quality 9:16 stills means we can do production-scale image work at a tiny fraction of what the rack-rate-based budget guards assumed. The toolkit's confirmation thresholds are now actively in the way of normal use, not protecting against waste.
