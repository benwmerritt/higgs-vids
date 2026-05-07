---
description: Execute a specific named pattern directly, bypassing brief expansion. Argument is the pattern name plus pattern-specific args, e.g. /higgsfield-pattern multi-platform-render --concept "..." --aspects 9:16,1:1,16:9
---

You're running a specific pattern directly. Argument: `$ARGUMENTS`

## Parse the pattern name

Take the first token from `$ARGUMENTS` — that's the pattern name.

**Valid pattern names = whatever files exist in `skill/higgsfield-autopilot/patterns/`** (excluding `README.md`). To get the live list:

```bash
ls skill/higgsfield-autopilot/patterns/*.md | xargs -n1 basename | grep -v '^README' | sed 's/\.md$//'
```

If the user's first token matches a file there, read `skill/higgsfield-autopilot/patterns/<name>.md` and execute.

If no match, run the list command above and show the user what's actually available, then stop.

**Do NOT use a hardcoded list of valid pattern names.** New patterns are added regularly — the slash command must reflect the current contents of the patterns directory, not a static list that drifts.

### Currently shipping patterns (informational — verify with `ls` before rejecting)

- `carousel-post` — IG/LinkedIn carousel, brand-aware
- `moodboard` — pre-production / pitch moodboard, brand-aware
- `product-reel` — multi-shot 9:16 reel
- `quick-social` — single still or short clip
- `multi-platform-render` — one concept × N aspects
- `brand-shoot` — product-photoshoot batch
- `ecom-listing` — marketplace listing imagery
- `character-campaign` — Soul ID-driven series

All are full as of 2026-05-07. If a new pattern was added since this list was written, the directory listing is the source of truth.

## Parse the rest of the args

Pattern-specific args follow the pattern name. Common shapes:

- `--concept "..."` — the creative ask, replaces a brief
- `--brief <path>` — alternative: read a brief file
- `--aspect 9:16` / `--aspects 9:16,1:1,16:9`
- `--budget-cap N`
- `--workspace <id>`
- pattern-specific: `--mode product_shot` (brand-shoot), `--scope product-images` (ecom-listing), `--soul-id <id>` (character-campaign)

If args are missing, ask the user before generating anything blank.

## Then follow the pattern's recipe

Same as `/higgsfield-make` but skip step 1-2 of SKILL.md (no brief expansion / pattern selection — already done). Jump to step 3 (pre-flight) and proceed.

Cost discipline still applies. Always preflight.

## Pattern completeness

All currently listed patterns are runnable. Some patterns call Higgsfield prebuilt workflow commands such as `product-photoshoot` or `marketplace-cards`; those are still part of the official `higgs` CLI path. Do not warn about stubs unless the pattern file itself explicitly says it is incomplete.
