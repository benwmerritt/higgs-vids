# Model Selection Guide

Decision tree for picking the right Higgsfield model. The agent consults this whenever a pattern needs to choose between options. **Default to the cheapest model that meets the job; escalate only when needed.**

> Costs below are *typical* per-generation estimates. Always run `higgs generate cost <model> --prompt "..."` for the real number before spending. Costs change with prompt length, resolution, and Higgsfield's pricing updates.

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

**Default: `cinematic_studio_3_0`** — ~2,500 credits per 5s @ 9:16. Takes `medias` array of source images. Cinematic quality.

**Cheaper alternatives** (price, then check):
- `kling3_0` — `--start-image`, `--mode std|pro`, `--duration 5` — generally cheapest premium video
- `seedance_2_0` — `--mode std|pro`, `--genre noir|...` — stylized
- `wan2_7` — Alibaba, often cheap
- `minimax_hailuo` — known low-cost option
- `kling2_6` — older Kling, cheaper than 3.0

**Premium / high-fidelity:**
- `veo3_1` — Google Veo, native audio support, ~30s max
- `veo3_1_lite` — cheaper Veo
- `sora_2` (if available in your account)

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

## Cost ladder (rough — verify with `generate cost`)

| Tier | Models | Use for |
|---|---|---|
| **Cheap stills** (~10-15 credits) | soul_cinematic, image_auto, flux_2 flex | Iteration, drafts, preview |
| **Mid stills** (~20-50 credits) | nano_banana_2, gpt_image_2 high, seedream_v4_5 | Final stills, brand work |
| **Cheap video** (~200-1000 credits) | kling2_6, minimax_hailuo, seedance_2_0 std | Drafts, social content |
| **Mid video** (~1000-2500 credits) | kling3_0 pro, cinematic_studio_3_0, wan2_7 | Production reels |
| **Premium video** (~2500-7000 credits) | veo3_1, veo3_1_lite, sora_2 | Hero campaigns, long-form |

A 5-shot 9:16 reel at the **mid** tier (still + 5s video per shot) typically costs **~12,500 credits** — plan accordingly.

## When the right answer is "ask the user"

- They want hyperrealism but their budget is 50 credits → tell them the floor, don't silently downgrade
- They want a 30-second video but the cheapest model maxes at 10s → flag, propose multi-shot strategy
- Their brief mentions a celebrity / public figure / branded character → don't generate, push back on the brief
- They specify a model that's broken (soul_cast) or unavailable in their plan → swap to nearest equivalent and tell them
