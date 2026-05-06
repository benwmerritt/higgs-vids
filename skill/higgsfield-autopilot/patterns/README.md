# Patterns

Each file in this directory is a self-contained recipe the agent reads and executes. A pattern says: "given an input shaped like X, produce an output shaped like Y, using these CLI calls in this order."

Patterns are agent-facing. The agent picks one based on the brief, then follows it step by step.

## Pattern decision tree

The agent picks a pattern by reading the brief and matching against this tree (top to bottom — first match wins):

```
brief asks for an Instagram / LinkedIn carousel (multi-slide, 5-10 slides)?
  → carousel-post.md  ← brand-aware; needs a brand profile

brief mentions a product photo / hero image / lifestyle shot, no motion?
  → brand-shoot.md

brief mentions an Amazon / Etsy / marketplace listing?
  → ecom-listing.md

brief mentions a recurring character, brand mascot, or named talent across multiple shots?
  → character-campaign.md

brief asks for the same concept in multiple aspect ratios (9:16 + 1:1 + 16:9 etc.)?
  → multi-platform-render.md

brief is short / time-pressured / "for daily socials" / explicit budget cap?
  → quick-social.md

brief is a video reel / IG-ready / multi-shot narrative with motion?
  → product-reel.md  ← canonical reel default
```

If nothing matches cleanly, **default to `carousel-post.md`** if a brand profile exists (cheapest, most useful) or `product-reel.md` for video-led briefs. If the brief is genuinely outside the toolkit's scope, stop and tell the user.

## Pattern file shape

Every pattern follows the same structure (so the agent can rely on the layout):

1. **Inputs** — what the brief must provide
2. **Cost envelope** — order-of-magnitude credit cost for a typical run
3. **Steps** — numbered CLI calls with exact flags
4. **Outputs** — what lands in the deliverables/ bundle
5. **Common variations** — tweaks for related sub-cases
6. **Failure handling** — recovery procedures specific to this pattern

## Pattern status (v3.0 + research integration 2026-05-06)

| Pattern | Status | Rack-rate cost | Notes |
|---|---|---|---|
| `carousel-post.md` | ✅ Full | ~60-120 credits rack (~0.6-1.2 actual on paid) | **Brand-aware** — IG/LinkedIn carousel from a brand profile + topic; produces slides + caption + hashtags |
| `product-reel.md` | ✅ Full | ~600-12,500 credits | Multi-shot 9:16 reel, image-to-video chain |
| `quick-social.md` | ✅ Full | ~50-300 credits | Single still or short clip, low-credit fast turn |
| `multi-platform-render.md` | ✅ Full | ~36-150 credits per concept × N aspects | One concept, multiple aspects |
| `brand-shoot.md` | ✅ Full | ~50-2,000 credits per batch | Delegates to `higgsfield-product-photoshoot` official skill; supports `--enhance-only` free preview |
| `ecom-listing.md` | ✅ Full | ~150-2,000 credits | Delegates to `higgsfield-marketplace-cards` official skill; full scope/asset support |
| `character-campaign.md` | ✅ Full | varies; Soul ID training cost unknown — measure | Train Soul ID once, reuse across campaigns |

All patterns are runnable. **Subscriber-absorbed cost is typically 90-99% lower than rack rate on paid plans** (see `references/cost-discipline.md`). Use `references/empirical-tests.md` to calibrate the user's actual ratios.
