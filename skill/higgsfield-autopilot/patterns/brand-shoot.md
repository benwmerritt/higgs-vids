# Pattern: Brand Shoot — STUB (v3.1)

> **Status: stub.** v3.1 will fill out the full recipe. For now, this file documents the API surface and the agent should run a minimal version + ask the user to refine.

## When to use

- Brief asks for product photography (hero shots, lifestyle, packshot)
- Multiple variants of the same product
- Output target: still images (PNG), brand-styled

## Inputs

- **Product image** (required)
- **Mode** — `product_shot` (clean studio) | `lifestyle_scene` (in context). Other modes may exist.
- **Brand context** (optional) — short string about the brand
- **Product context** (optional) — short string about the product
- **Variant count** — 1-10

## Cost envelope (TBD — verify with `--enhance-only` first)

Roughly: ~30 credits per variant, mid-tier model under the hood.

## Minimal v3.0 implementation

Use Higgsfield's built-in `product-photoshoot` command — it does the heavy lifting:

```bash
# Free preview — get the enhanced prompt without spending
higgs product-photoshoot create \
  --mode product_shot \
  --prompt "$INTENT" \
  --image "$PRODUCT_IMAGE" \
  --brand_context "$BRAND" \
  --product_context "$PRODUCT" \
  --enhance-only

# Real run
higgs --json product-photoshoot create \
  --mode product_shot \
  --prompt "$INTENT" \
  --image "$PRODUCT_IMAGE" \
  --brand_context "$BRAND" \
  --product_context "$PRODUCT" \
  --count "$VARIANTS"
```

Save outputs to `runs/<RUN_ID>/variant-{1..N}.png`. Bundle as deliverables.

## v3.1 TODO

- Variant comparison + best-pick logic
- Multi-mode batch (product_shot + lifestyle_scene in one run)
- Integration with marketing-studio products registry (so repeat campaigns reuse the product record)
- Brand-style consistency checks across variants

## Open questions for the agent

If the brief is for brand-shoot work and this stub is incomplete, **tell the user up front**:
> "Running the brand-shoot pattern in v3.0 minimal mode. The full recipe lands in v3.1. Want me to proceed with --count 3 variants, or should we wait?"
