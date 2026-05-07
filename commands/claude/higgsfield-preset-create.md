---
description: Create a reusable preset (brand × pattern × platform × style tweaks). Argument is "<brand> <pattern>" e.g. "ben carousel-post". Adaptive interview — asks pattern-specific questions on top of the existing brand profile (slide count, caption shape, platforms, voice tweaks). Saves presets/<brand>-<pattern>.md so future runs via /higgsfield-make --preset <name> apply all the brand context + preset shape automatically. Reduces re-explaining when running the same content type repeatedly.
---

You are about to create a preset. Argument: `$ARGUMENTS` — expected format: `<brand> <pattern>`.

## Read these first

1. `skill/higgsfield-autopilot/references/preset-format.md` — preset schema
2. `skill/higgsfield-autopilot/references/interview-craft.md` § Adapting on the fly — same one-question-at-a-time discipline
3. The pattern file for the pattern being preset: `skill/higgsfield-autopilot/patterns/<pattern>.md` — read fully to understand pattern-specific options

## Parse arguments

Expected: `<brand> <pattern>`. E.g. `ben carousel-post`.

If `$ARGUMENTS` doesn't include both:
- If only one token, ask which is missing (brand name or pattern name)
- If empty, ask both

Validate:
- `brands/<brand>/profile.md` must exist — if not, tell user to run `/higgsfield-brand-create <brand>` first
- `patterns/<pattern>.md` must exist — if not, list valid patterns from `patterns/README.md`

## Confirm intent

> "Building a preset for **<brand>** running **<pattern>**. This is the saved 'frame' you'll reuse for every future <pattern> run. The topic of each post still varies; the preset captures the rest. Sound right?"

On yes, continue. On no, refine until clear.

## Pattern-specific interview

The questions depend on the pattern. **Read the pattern file's "Inputs" and "Common variations" sections first** to know what's tunable.

### For `carousel-post`:

1. Default slide count? (5-10; default 6)
2. Default aspect? (4:5 IG portrait | 1:1 square)
3. Primary platform? (instagram | linkedin | both)
4. Caption shape — pick the one most often right for THIS preset's posts:
   - hook → beat → payoff (story-driven)
   - list (educational, takeaway-per-slide)
   - single-sentence (opinion drops)
   - reply-bait (community / question-led)
5. CTA preference for this preset? (always / sometimes / never — most carousels for this brand have a CTA?)
6. Typical use — when in the week / month does this preset get used? (helps with later cadence planning)
7. Voice override (only if different from brand default) — anything specific to carousels for this brand vs feed posts?

### For `quick-social`, `product-reel`, `multi-platform-render`, etc.

Read the pattern's Inputs section and ask only what's variable. Skip questions that have obvious-from-brand answers.

### For `brand-shoot`, `ecom-listing`, `character-campaign`:

Same approach — these patterns delegate to official Higgsfield skills, so the questions are mostly which mode/scope they typically use:
- `brand-shoot` — default mode? (`product_shot`, `lifestyle_scene`, etc.)
- `ecom-listing` — default scope? (`main`, `product-images`, `aplus`, `full-set`)
- `character-campaign` — which Soul ID(s) does this preset feature?

## Don't ask if it's already in the brand profile

The brand profile already has voice, palette, hashtag families, constraints. **Don't re-ask those.** A preset adds the *delta* — pattern-specific tweaks on top of the brand profile.

## Save the preset

Write `presets/<brand>-<pattern>.md` per `references/preset-format.md` schema. Include:
- Frontmatter with `name`, `brand`, `pattern`, `platforms`, `created`
- Default arguments (slide count, aspect, etc.)
- Voice/visual overrides (empty if same as brand)
- Posting context (when typically used)
- Empty "Past runs" table (gets populated by future runs)
- Empty "Refinement notes" section (gets populated as the preset is used)

## Quick alternative: extract from a successful run

If the user says "I just had a great run, save it as a preset" instead of going through the interview:
1. Read the run's `runs/<RUN_ID>/shotlist.json`, `pattern.txt`, `cost-log.json`
2. Infer pattern + arguments from the run
3. Ask 3-4 confirming questions: "Looks like you ran <pattern> for <brand> with these settings: [...]. Save as a preset called <suggested-name>?"
4. On confirm, write the preset (same schema)

This flow lets users build presets organically from "this worked" rather than only via interview.

## Final report

```
✓ Preset saved → presets/<brand>-<pattern>.md

Use it:
  /higgsfield-make --preset <brand>-<pattern> "your topic"

Refine over time — the preset's "Refinement notes" section captures lessons from each run.
```

## Don't

- Don't ask questions already answered by the brand profile
- Don't generate any content — this is preset setup only
- Don't bake a specific topic into the preset (topics vary per post; the preset is the frame)
- Don't commit anything
