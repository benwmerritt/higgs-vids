# Soul Cinema Prompting Rules

Quick rules for formatting Soul Cinema prompts. The full theory lives in the canonical research at:

- **`docs/research/higgs-field-prompting.md`** — UI vs prompt boundary, every model's quirks, full prompt structure (610 lines).
- **`docs/skills/skill-higgsfield-shot-designer.md`** — guided shot-design workflow.
- **`docs/research/generative-media-orchestration.md`** — model stack and routing.

This file is the **agent's quick-reference** during automated runs. Do not duplicate the canonical material — link out instead.

## The 6-part prompt structure (use this order)

```
Subject → Scene → Action → Camera Feel → Lighting → Style
```

Reference: `docs/research/higgs-field-prompting.md` section 1.2.

For Soul Cinema specifically (decoded from reel frame 17):

| Section | Example fragment |
|---|---|
| Subject | "aerodynamic shape with a rosy-tinted front grille, lacks visible wheels" |
| Composition | "centered and low to the ground, subject dominating the foreground" |
| Scene | "flat, sandy desert landscape, scattered desert scrub, silhouetted foothills" |
| Lighting | "painterly gradient of sunset pink, purple, blue; soft diffused dusk lighting; no harsh shadows" |
| Palette | "pastel mauve, off-white, blush, sandy beige" |
| Optical | "deep focus on the model and car" |

## What to NOT put in Soul Cinema prompts

The Higgsfield UI controls aspect ratio, duration, resolution, model, batch count, boost. **Do not restate these in the prompt** — they're handled by `03-generate-asset.py` flags. Restating them wastes prompt capacity and can create conflicts.

Reference: `docs/research/higgs-field-prompting.md` section 1.2.2.

## High-value additions specific to Soul Cinema

- **Material physics** — "silk charmeuse with liquid drape" beats "shiny dress"
- **Specific lighting** — "golden hour side-light, 3:1 contrast" beats "dramatic light"
- **Painterly atmosphere** — Soul Cinema responds well to "painterly gradient" / "diffused" / "wraps"
- **Palette explicit** — list 3–5 colours

## Length guidance

The reel's visible prompt was ~80 words. That's a good ceiling — Soul Cinema doesn't reward longer prompts proportionally. Aim for 50–80 words per shot.

## Cost (estimate)

Per the existing research at `docs/research/generative-media-orchestration.md` section 2.3.2, Soul Cinema generations sit in the mid-tier credit range. Decoded from reel frame 17, the user had "249 free gens left" remaining. Without official per-call cost: **assume ~5–8 credits per Soul Cinema 9:16 generation × 4 batches = ~20–32 credits per shot**. A 5-shot campaign = ~100–160 credits.

These numbers are estimates. The `--dry-run` flag of `03-generate-asset.py` should print the live UI's cost preview where possible.
