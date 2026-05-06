# Pattern: Brand Shoot

Brand product photography via Higgsfield's mode-driven prompt enhancement. The product is supplied; Higgsfield writes the photographic prompt.

## When to use

- Brief asks for product photography (hero shots, lifestyle, packshot)
- Multiple variants of the same product
- Output: still images (PNG), brand-styled
- The user has a product image (or wants a CGI/conceptual style without one)

If the brief is for marketplace-listing imagery specifically, use `patterns/ecom-listing.md` instead.

## Architecture: delegate to the official skill

The official `~/.agents/skills/higgsfield-product-photoshoot/SKILL.md` handles mode selection, backend prompt enhancement, and routing to `gpt_image_2`. We provide cost discipline + run-dir layout + multi-variant orchestration.

## Inputs

- **Product image** (recommended; some modes work without)
- **Mode** — one of:
  - `product_shot` — neutral / studio / catalog background
  - `lifestyle_scene` — real-world environment
  - `closeup_product_with_person` — hands / partial face / demonstration
  - `moodboard_pin` — vertical 2:3 Pinterest aesthetic
  - `hero_banner` — wide-format website / email header
  - `social_carousel` — 3-10 connected slides
  - `ad_creative_pack` — coordinated paid-social ad pack
  - `virtual_model_tryout` — product worn/used by AI model
  - `conceptual_product` — surreal / CGI / floating / splash
  - `restyle` — transform existing image's aesthetic without changing subject
- **Brand context** (optional but recommended)
- **Product context** (optional but recommended)
- **Variant count** (1-10) — number of generations per call

## Cost envelope (rack-rate)

`gpt_image_2` rack rate is unknown but reportedly higher than `nano_banana` (no public cost figures as of 2026-05-06). Likely partial absorption on Plus+ plans (April article hints at "365-day unlimited GPT Image" on higher tiers).

| Variants | Likely rack-rate | Likely actual on absorbed plan |
|---|---|---|
| 1 | ~50-200 credits | ~0.5-2 |
| 3 | ~150-600 | ~1.5-6 |
| 10 (max) | ~500-2,000 | ~5-20 |

Measure first; see `references/empirical-tests.md` Test 1.

## The free preview path — `--enhance-only`

**Use this aggressively.** It returns the AI-enhanced prompt without generating anything (zero credits):

```bash
higgs --json product-photoshoot create \
  --mode "$MODE" \
  --prompt "$INTENT" \
  --image "$PRODUCT_IMAGE" \
  --brand_context "$BRAND" \
  --product_context "$PRODUCT" \
  --enhance-only
```

This shows the user what the backend would actually submit. They can refine intent, brand context, or product context before paying for any generations. **Run this first on every brand-shoot pattern invocation.**

## Steps

### 0. Pre-flight (per `references/cost-discipline.md`)

Auth, balance, workspace.

### 1. Pick mode

Apply the official skill's mode selection rules (in `~/.agents/skills/higgsfield-product-photoshoot/SKILL.md`):

- "Clean / studio / white / catalog" → `product_shot`
- "In use / kitchen / outdoor / cafe" → `lifestyle_scene`
- "Hands / face / beauty application" → `closeup_product_with_person`
- "Pinterest / pin / vertical" → `moodboard_pin`
- "Hero / banner / wide" → `hero_banner`
- "Carousel / multi-slide" → `social_carousel`
- "Ads / paid social / Meta / TikTok" → `ad_creative_pack`
- "Virtual try-on / model wearing" → `virtual_model_tryout`
- "Levitating / splash / CGI / surreal" → `conceptual_product`
- "Restyle existing image" → `restyle`

When two modes could apply, pick the more specific one. When the brief is ambiguous, ask the user — short labeled options, not open-ended questions.

### 2. Upload product image

```bash
PRODUCT_ID=$(higgs --json upload create "$PRODUCT_IMAGE" | jq -r '.id')
```

### 3. Free preview with `--enhance-only`

```bash
ENHANCED=$(higgs --json product-photoshoot create \
  --mode "$MODE" \
  --prompt "$INTENT" \
  --image "$PRODUCT_ID" \
  --brand_context "$BRAND" \
  --product_context "$PRODUCT_CONTEXT" \
  --enhance-only)

echo "$ENHANCED" | jq -r '.enhanced_prompt'
```

Show the user the enhanced prompt. Ask if they want to refine `INTENT`/`BRAND`/`PRODUCT_CONTEXT` before generating.

### 4. Cost preflight

```bash
# Marketplace-cards/photoshoot don't have a separate `cost` endpoint;
# rack rate scales with --count
echo "Estimated rack rate for $COUNT variants: high — measure first run"
```

Per `references/cost-discipline.md`, if no calibration data exists for `gpt_image_2` on this plan, **run one variant first** (`--count 1`), observe absorption, then ask user to authorize the full batch.

### 5. Generate variants

```bash
RESULT=$(higgs --json product-photoshoot create \
  --mode "$MODE" \
  --prompt "$INTENT" \
  --image "$PRODUCT_ID" \
  --brand_context "$BRAND" \
  --product_context "$PRODUCT_CONTEXT" \
  --aspect_ratio "$ASPECT" \
  --count "$VARIANTS")
```

The output is an array of jobs (one per variant). Wait + download each.

### 6. Download

For each variant:

```bash
mkdir -p runs/$RUN_ID/variants
curl -sL "$URL" -o runs/$RUN_ID/variants/variant-$N.png
```

### 7. Bundle deliverables

```bash
mkdir -p runs/$RUN_ID/deliverables
cp runs/$RUN_ID/variants/*.png runs/$RUN_ID/deliverables/

cat > runs/$RUN_ID/deliverables/README.md <<EOF
# Brand Shoot — $TITLE

Mode: $MODE
Variants: $VARIANTS
Total cost: $ACTUAL_SPEND credits
EOF
```

### 8. Cost ledger + report

Standard per `references/output-management.md`. Tell user the path.

## Outputs

```
runs/<RUN_ID>/
├── brief.md
├── pattern.txt                ← "brand-shoot"
├── cost-log.json
├── product-upload-id.txt
├── enhanced-prompt.txt        ← from --enhance-only step (great audit artifact)
├── variants/
│   ├── variant-1.png
│   ├── variant-2.png
│   └── ...
└── deliverables/
    ├── (selected PNGs)
    └── README.md
```

## Common variations

- **Multi-mode batch** — same product, multiple modes (e.g. `product_shot` + `lifestyle_scene` + `hero_banner`). Run pattern 3× with same product, different modes. Compare outputs in deliverables.
- **Brand library kickstart** — first-run for a new brand, generate 3 variants in 4 modes (12 outputs). Establishes a brand visual vocabulary the agent can reuse in future runs via `--brand_context`.
- **Restyle existing assets** — `--mode restyle` for transforming an existing image's mood/season/aesthetic without changing the subject. Use for seasonal refreshes (Christmas version of a hero shot).

## Failure handling

| Symptom | Action |
|---|---|
| `--enhance-only` flag not recognized | CLI version mismatch. Run `higgs --version` and `higgs product-photoshoot create --help` to verify current flags. |
| Backend rejects mode name | Mode list may have changed since the SKILL.md docs. Run `higgs product-photoshoot create --help` for current valid modes. |
| Generated image doesn't match brand | Refine `--brand_context` and `--product_context` strings. The backend enhancer is the only thing writing the model prompt; you can't override its style choices, only seed them. |
| All variants look identical | `--count N` produces N variants with the same seed family. To get more diversity, run multiple `--count 1` calls with slightly different `--prompt` intent. |

## Why we don't write the `gpt_image_2` prompt directly

The official skill explicitly says: "Never write the gpt_image_2 prompt yourself — backend assembles it." The mode-specific enhancement is the value-add of `product-photoshoot create`. If you bypass it (`higgs generate create gpt_image_2 --prompt "..."`), you lose the studio-photography vocabulary, lighting templates, and brand consistency that the backend has been tuned for. **Use this pattern for product work; only fall back to `generate create` for non-brand creative.**
