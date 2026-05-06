# Model Selection Guide

Decision tree for picking the right Higgsfield model. The agent consults this whenever a pattern needs to choose between options. **Default to the cheapest model that meets the job; escalate only when needed.**

> **Costs below are rack-rate estimates** — what `higgs generate cost` returns. On paid plans, models often **absorb 90-99%** of rack rate (see `references/cost-discipline.md`). The CLI is plan-blind (upstream issue #1, see `references/known-issues.md`), so absorption status can only be measured empirically. Run `higgs generate cost` for the planning bound, then use the `account status` delta after the spend to learn the real number.

## Plan-aware absorption (per April 2026 official article — `[STALE — verify]`)

Higgsfield's pricing article describes "365-day unlimited" entitlements at higher tiers:

- **Plus and above:** unlimited image access to Seedream 5.0 Lite, Flux.2 Pro, GPT Image, Seedream 4.5, Nano Banana — at base resolution
- **Ultra and above:** above + 4K Seedream 4.5 + 2K Nano Banana Pro + higher Soul/Cinema quotas + **one** 365-day unlimited video model from `seedance1_5`, `wan2_6`, `kling2_6`, `nano_banana_2`

These claims are from a 2026-04-20 article and may have shifted; tier names have already drifted (Starter/Plus/Ultra vs Basic/Pro/Ultimate). **Don't make decisions on the literal tier name.** Use capability checks per `references/cost-discipline.md`.

## Image models

### "Generate a still I'll later animate"

**Default: `soul_cinematic`** — ~12 credits @ 9:16. Cinematic look, supports `medias` for ref images.

Alternatives:
- `nano_banana_2` (Nano Banana Pro) — strong text rendering, photorealistic; check cost
- `flux_2 --model pro` — sharp; `--model flex` is faster/cheaper, `--model max` is most capable
- `seedream_v4_5` — varied creative outputs

### "Generate a brand-styled product image"

**Default: `higgs product-photoshoot create --mode product_shot|lifestyle_scene`** — Higgsfield writes the enhanced prompt for you, optionally `--enhance-only` for a free preview. Routes to a real model under the hood.

Modes (from CLI help): `product_shot`, `lifestyle_scene` (more may exist — try `--mode <other>` to discover).

### "Generate Amazon/Etsy/marketplace listing imagery"

**Default: `higgs marketplace-cards create --scope product-images`** — template-driven, returns `nano_banana_2` jobs. Other scopes likely exist (try `--scope secondary-images` etc.).

### "Generate with a specific recurring character"

**Default: `text2image_soul_v2 --soul-id <id>`** — uses a trained or preset Soul ID for face-faithful generation.

Train your own: `higgs soul-id create --name X --soul-2 --image x5`.
List presets: `higgs marketing-studio avatars list` — 9 presets ship in every account.

### "Edit / variation of an existing image"

**Default: `flux_kontext --image <upload-id>`** — for prompt-driven edits.

Or `imagegen_2_0 / gpt_image_2 --image <id> --quality high` for sharp redos.

## Video models

> **Critical:** `soul_cast` is broken (upstream issue #4). Don't use it.

### "Animate a still image into a 5-second clip" (the canonical reel shot)

**Default: `cinematic_studio_3_0`** — ~2,500 credits per 5s @ 9:16 *rack rate*. Takes `medias` array of source images. Cinematic quality. **Actual cost depends on plan absorption** — measure first.

**Cheaper alternatives** (rack-rate prices, then check actual absorption on user's plan):
- `kling3_0` — `--start-image`, `--mode std|pro`, `--duration 5` — generally cheapest premium video
- `seedance_2_0` — `--image|--start-image|--end-image`, `--mode std|pro`, `--genre noir|...` — stylized; SOTA all-purpose per official skill
- `wan2_7` — Alibaba, often cheap
- `minimax_hailuo` — `--image` (multi-image input), `--resolution 512|768|1080`, `--duration 6|10` — known low-cost option, strong physics
- `kling2_6` — `--image` ONLY (no `--start-image`!), `--duration 5|10`, `--sound true|false` — older Kling, cheaper than 3.0; **listed as one of Ultra's "pick-one-unlimited" video models** per April article

> **Per-model image-flag differences (2026-05-07):** the `--start-image` / `--image` / `--medias` flags are NOT universal. Always run `higgs --json model get <name>` to see the schema before building a command. See `references/cli-cheatsheet.md` § Media flags for the verified table.

**Ultra "pick-one-unlimited" candidates** (per April 2026 official article — `[STALE — verify]`):
- `seedance1_5` (Pro)
- `wan2_6`
- `kling2_6`
- `nano_banana_2` (video — if available)

If the user has Ultra-tier and an unlimited video model selected, prefer that one (verify via empirical run — see `references/empirical-tests.md` Test 2).

**Premium / high-fidelity:**
- `veo3_1` — Google Veo, native audio support, ~30s max — **likely never absorbed**, charges full rack rate even on Ultra
- `veo3_1_lite` — cheaper Veo, fast batch
- `sora_2` (if available in your account)

**AVOID — `soul_cast`** is broken (issue #4, still open as of 2026-05-06). It ignores `--prompt` object schema and submits empty character_params. Use `cinematic_studio_3_0 --image <still-job-id>` or `kling3_0 --start-image <still-job-id>` instead. See `references/known-issues.md`.

### "Generate a multi-shot scene with one prompt"

**Default: `cinematic_studio_video_v2`** — newer multi-shot CS variant. Or `cinematic_studio_3_0` with longer prompt.

### "Marketing-style ad video"

**Default: `marketing_studio_video`** — pairs with the marketing-studio products/avatars registry.

## Decision rules (priority order)

1. **Did the user specify a model?** → use it. Don't override creative direction.
2. **Is there a Higgsfield workflow command for this job?** (`product-photoshoot`, `marketplace-cards`, `marketing-studio`) → use it. The backend prompt enhancement is generally better than what we'd write.
3. **What's the budget?** → consult `cost-discipline.md`. If budget is tight, prefer Kling/Seedance/Hailuo over Veo/Cinematic Studio.
4. **What's the deliverable's importance?** → final hero shot for paid client = premium model; daily social = cheap model.
5. **Is character consistency required across shots?** → use `--soul-id` with a trained or preset avatar. Otherwise prompts alone won't keep faces stable across generations.

## Rack-rate ladder (verify against actual via `account status` delta)

These are **rack rates** — what `higgs generate cost` returns. Subscriber absorption can drop them by 90-99% on paid plans, but you can't know until you measure.

| Tier | Models | Use for |
|---|---|---|
| **Cheap stills** (~10-15 credits rack) | soul_cinematic, image_auto, flux_2 flex | Iteration, drafts, preview |
| **Mid stills** (~20-50 credits rack) | nano_banana_2, gpt_image_2 high, seedream_v4_5 | Final stills, brand work |
| **Cheap video** (~200-1000 credits rack) | kling2_6, minimax_hailuo, seedance_2_0 std | Drafts, social content |
| **Mid video** (~1000-2500 credits rack) | kling3_0 pro, cinematic_studio_3_0, wan2_7 | Production reels |
| **Premium video** (~2500-7000 credits rack) | veo3_1, veo3_1_lite, sora_2 | Hero campaigns, long-form |

**Empirical measurement (Starter plan, 2026-05-06):**
- `soul_cinematic` rack 12 → actual ~0.12 credits (99% absorbed)
- `nano_banana` rack 100 → actual ~1 credit (99% absorbed)

That's just two data points. Image absorption is real and high on the cheapest paid tier. **Video absorption is unmeasured** — likely lower for premium models (Veo, Cinematic Studio 3.0); possibly high for "pick-one-unlimited" candidates on Ultra.

A 5-shot 9:16 reel at the mid rack-rate tier (still + 5s video per shot) is **~12,500 credits rack**. On Starter, it could be anywhere from ~125 actual (if video absorbs at 99%) to ~12,500 actual (if video doesn't absorb). **Run `references/empirical-tests.md` Test 1 once to learn the user's actual ratio**, then plan accordingly.

## When the right answer is "ask the user"

- They want hyperrealism but their budget is 50 credits → tell them the floor, don't silently downgrade
- They want a 30-second video but the cheapest model maxes at 10s → flag, propose multi-shot strategy
- Their brief mentions a celebrity / public figure / branded character → don't generate, push back on the brief
- They specify a model that's broken (soul_cast) or unavailable in their plan → swap to nearest equivalent and tell them
