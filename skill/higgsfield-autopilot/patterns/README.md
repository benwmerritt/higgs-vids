# Patterns

Each file in this directory is a self-contained recipe the agent reads and executes. A pattern says: "given an input shaped like X, produce an output shaped like Y, using these CLI calls in this order."

Patterns are agent-facing. The agent picks one based on the brief, then follows it step by step.

## Pattern decision tree

The agent picks a pattern by reading the brief and matching against this tree (top to bottom — first match wins):

```
brief mentions a product photo / hero image / lifestyle shot, no motion?
  → brand-shoot.md  [STUB — v3.1]

brief mentions an Amazon / Etsy / marketplace listing?
  → ecom-listing.md  [STUB — v3.1]

brief mentions a recurring character, brand mascot, or named talent across multiple shots?
  → character-campaign.md  [STUB — v3.1]

brief asks for the same concept in multiple aspect ratios (9:16 + 1:1 + 16:9 etc.)?
  → multi-platform-render.md

brief is short / time-pressured / "for daily socials" / explicit budget cap?
  → quick-social.md

brief is a video reel / IG-ready / multi-shot narrative with motion?
  → product-reel.md  ← the canonical, default pattern
```

If nothing matches cleanly, **default to `product-reel.md`** and adapt the shotlist to fit. If the brief is genuinely outside the toolkit's scope, stop and tell the user.

## Pattern file shape

Every pattern follows the same structure (so the agent can rely on the layout):

1. **Inputs** — what the brief must provide
2. **Cost envelope** — order-of-magnitude credit cost for a typical run
3. **Steps** — numbered CLI calls with exact flags
4. **Outputs** — what lands in the deliverables/ bundle
5. **Common variations** — tweaks for related sub-cases
6. **Failure handling** — recovery procedures specific to this pattern

## Pattern status (v3.0)

| Pattern | Status | Cost (rough) |
|---|---|---|
| `product-reel.md` | ✅ Full | ~600-12,500 credits depending on video model |
| `quick-social.md` | ✅ Full | ~50-300 credits |
| `multi-platform-render.md` | ✅ Full | ~36-150 credits per concept × N aspects |
| `brand-shoot.md` | 🚧 Stub (v3.1) | ~30-200 credits |
| `ecom-listing.md` | 🚧 Stub (v3.1) | ~50-300 credits |
| `character-campaign.md` | 🚧 Stub (v3.1) | varies; Soul ID training is one-time ~free, then per-shot |

Stubs document the API surface and are runnable as "kick-off then ask user to refine" — they just don't have the full optimised recipe yet. The agent should warn the user when running a stub.
