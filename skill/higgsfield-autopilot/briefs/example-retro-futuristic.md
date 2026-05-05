# Brief: Retro-Futuristic Editorial Campaign

> **The actual brief from Timothée Oranger's reel** (DXfKnWhDPlW, frame 15) — kept verbatim as a starter so the autopilot has a known-good input.

```
va me faire une campagne éditorial retro futuristique
```

(English: *"make me a retro-futuristic editorial campaign"*)

## Expected output (rough target)

- **Aspect:** 9:16
- **Duration:** ~20–25s total
- **Shots:** 5 (`establish → subject_intro → object_detail → motion → closer`)
- **Vibe:** desert dusk, pastel sunset palette, capsule car as hero object, model in flowing silk, painterly editorial fashion photography
- **Style anchors:** Bella-Hadid-era Vogue editorial, 60s/70s concept-car aesthetic, soft diffused dusk light

The decoded reference shot list is in `references/brief-expansion-rules.md` (the worked example).

## How to use this brief

```bash
claude "Use the higgsfield-autopilot skill to execute briefs/example-retro-futuristic.md"
```

The agent will:
1. Read this file
2. Expand to a JSON shot list (per `references/brief-expansion-rules.md`)
3. Generate the assets via Soul Cinema 9:16 4/4 batches
4. Pick best take per shot
5. Assemble `runs/<date>/final.mp4`
