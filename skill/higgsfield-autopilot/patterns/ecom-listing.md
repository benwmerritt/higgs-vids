# Pattern: E-Commerce Listing

Generate marketplace-ready product imagery (Amazon, Etsy, eBay, Shopify, etc.) — main image, secondary product images, A+ content modules. Strict format compliance.

## When to use

- Brief asks for marketplace listing imagery
- Output: hero image + secondary product images + (optional) A+ content modules
- Format compliance matters (white BG, specific aspect, ≥1000px on Amazon, etc.)

If the brief is generic brand product photography without a marketplace angle, use `patterns/brand-shoot.md` instead.

## Architecture: delegate to the official skill

The official Higgsfield skill `~/.agents/skills/higgsfield-marketplace-cards/SKILL.md` handles all the marketplace specifics — backend prompt enhancement, marketplace-compliant templates, scope/asset slugs, routing to `nano_banana_2`. **We don't reinvent that.**

Our value-add is: cost discipline (per `references/cost-discipline.md`), run-dir layout (per `references/output-management.md`), cost ledger, deliverable bundle, multi-product orchestration.

## Inputs

- **Product image** (required, or upload UUID)
- **Marketplace scope** — pick one:
  - `main` — 1 marketplace main image
  - `product-images` — main image + 5 secondary images
  - `aplus` — main image + 7 A+ modules
  - `full-set` — main image + 5 secondary + 7 A+ modules
- **Listing context** (recommended): product category, target market, brand context
- **Custom asset subset** (optional): pick from `main_image`, `infographic`, `multi_angle`, `detail_shot`, `lifestyle`, `whats_in_box`, `aplus_hero_banner`, `aplus_pain_points`, `aplus_features`, `aplus_ingredients`, `aplus_efficacy`, `aplus_how_to_use`, `aplus_endorsement`

## Cost envelope (rack-rate)

Each generated image is `nano_banana_2` rack rate (~150 credits per image). On paid plans, much of this likely absorbs (we measured ~99% absorption for `nano_banana` on Starter — `nano_banana_2` Pro variant unverified).

| Scope | Image count | Rack-rate total | Likely actual on Starter+ |
|---|---|---|---|
| `main` | 1 | ~150 | ~1.5 |
| `product-images` | 6 | ~900 | ~9 |
| `aplus` | 8 | ~1,200 | ~12 |
| `full-set` | 13 | ~1,950 | ~20 |

(Measure on first run; absorption may differ from `nano_banana` base.)

## Steps

### 0. Pre-flight (per `references/cost-discipline.md`)

Auth, balance, workspace. Read live plan name (display only).

### 1. Identify the marketplace + scope

Read the brief. If it explicitly names a marketplace (Amazon, Etsy, etc.), use that to choose scope:
- Amazon: typically `full-set` for a complete listing
- Etsy / Shopify: `product-images` is usually enough
- A+ content add-on: `aplus` only

If the user doesn't specify, ask: "Which marketplace? And do you want main image only, full product set, or A+ content?"

### 2. Upload product image (if local file)

```bash
PRODUCT_ID=$(higgs --json upload create "$PRODUCT_IMAGE" | jq -r '.id')
```

### 3. Cost preflight

```bash
# Marketplace-cards has its own cost endpoint behavior — verify with --help
# Generally: cost is approximate scope_image_count × nano_banana_2 rack rate
echo "Estimated rack rate: $((SCOPE_COUNT * 150)) credits"
```

Apply cost-discipline thresholds.

### 4. Run the marketplace-cards command

```bash
higgs --json marketplace-cards create \
  --scope "$SCOPE" \
  --prompt "$LISTING_INTENT" \
  --image "$PRODUCT_ID" \
  --category "$CATEGORY" \
  --brand_context "$BRAND" \
  --product_context "$PRODUCT_DESC"
```

Or for custom asset subsets:

```bash
higgs --json marketplace-cards create \
  --asset main_image \
  --asset infographic \
  --asset lifestyle \
  --prompt "..." \
  --image "$PRODUCT_ID"
```

Reuse a prior main image without regenerating it:

```bash
higgs --json marketplace-cards create \
  --main-job <prior_main_job_id> \
  --asset infographic --asset lifestyle \
  --prompt "..."
```

The official skill manages prompt enhancement, scope-to-asset expansion, and submission. Output is one job per asset returning result URLs.

### 5. Download all outputs

For each returned URL:

```bash
mkdir -p runs/$RUN_ID/listing
curl -sL "$URL" -o runs/$RUN_ID/listing/$ASSET_LABEL.png
```

Use `$ASSET_LABEL` (`main_image`, `infographic`, etc.) as the filename so the user / their listing tool can find the right asset by name.

### 6. Bundle deliverables

```bash
mkdir -p runs/$RUN_ID/deliverables
cp runs/$RUN_ID/listing/*.png runs/$RUN_ID/deliverables/

cat > runs/$RUN_ID/deliverables/README.md <<EOF
# Marketplace Listing — $LISTING_TITLE

Generated $SCOPE for $MARKETPLACE.

## Files
$(ls runs/$RUN_ID/deliverables/*.png | xargs -I {} basename {})

## Metadata
- Scope: $SCOPE
- Product: $PRODUCT_TITLE
- Category: $CATEGORY
- Total cost: $ACTUAL_SPEND credits (rack-rate estimate was $RACK_RATE)
EOF
```

### 7. Cost ledger + report

Standard per `references/output-management.md`. Tell user the path + spend.

## Outputs

```
runs/<RUN_ID>/
├── brief.md
├── pattern.txt           ← "ecom-listing"
├── cost-log.json
├── product-upload-id.txt
├── listing/
│   ├── main_image.png
│   ├── infographic.png       (if scope includes)
│   ├── lifestyle.png
│   └── ... (per scope)
└── deliverables/
    ├── (copied PNG files)
    └── README.md
```

## Common variations

- **Multi-product** — loop steps 2-6 per product. Each product gets its own subdirectory.
- **Reuse main image across SKUs** — generate the main image once for a flagship SKU, then use `--main-job <id>` for variants. Saves credits + ensures visual consistency.
- **Custom subsets per platform** — Amazon needs `main_image` + `multi_angle` ×4 + `aplus_hero_banner` etc.; Etsy is happy with `main_image` + `lifestyle`. Pre-build platform-specific asset lists.

## Failure handling

| Symptom | Action |
|---|---|
| `marketplace-cards create` errors with unknown scope | Verify scope name via `higgs marketplace-cards create --help` (may have changed in CLI updates). |
| Output image doesn't show product clearly | The backend prompt enhancer is doing the work; if results are off, refine `--prompt` and `--product_context`. Don't try to write `nano_banana_2` prompts directly. |
| White background bleeds into product (Amazon main-image rule violation) | This is a model artefact. Re-run; if persistent, fall back to manual masking in post. |
| Job fails | Per `references/known-issues.md`, failed jobs likely don't deduct credits. Retry once with refined prompt. |

## Marketplace-specific compliance notes

These aren't enforced by the CLI — the user is responsible. Document in the deliverable README so the user can verify before listing:

- **Amazon main image:** pure white background, product fills 80%+ of frame, no text/logos/props, ≥1000px on longest side
- **Etsy:** flexible; lifestyle / styled OK
- **Shopify:** site-specific; check the merchant's brand guidelines

The agent should mention these requirements in the deliverables/README.md as a checklist.
