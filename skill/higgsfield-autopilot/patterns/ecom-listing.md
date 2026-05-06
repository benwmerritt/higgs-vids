# Pattern: E-Com Listing — STUB (v3.1)

> **Status: stub.** v3.1 will fill out the full recipe. For now, documents the API surface.

## When to use

- Brief asks for Amazon / Etsy / eBay / marketplace listing imagery
- Output: hero image + secondary product images + (optional) A+ content modules
- Strict format compliance matters (white BG, specific aspect, etc.)

## Inputs

- **Product image** (required)
- **Marketplace scope** — `product-images` (default) | `secondary-images` | `aplus-modules`
- **Listing context** — short string (product category, target market)

## Cost envelope (TBD)

Roughly: ~50-300 credits depending on scope and number of variants.

## Minimal v3.0 implementation

Use Higgsfield's built-in `marketplace-cards`:

```bash
higgs --json marketplace-cards create \
  --scope product-images \
  --prompt "$INTENT" \
  --image "$PRODUCT_IMAGE"
```

The backend keeps marketplace prompt templates private and routes to `nano_banana_2` under the hood.

## v3.1 TODO

- Multi-scope batch (hero + secondary + A+ in one run)
- Marketplace-specific aspect/resolution validation (e.g. Amazon main image = 1:1, ≥1000px)
- Compliance checks (no text overlays for some marketplaces, white-BG enforcement)
- Integration with marketing-studio products registry for catalog management

## Open questions for the agent

Tell the user this is a stub and ask which marketplace they're targeting (the formatting requirements vary).
