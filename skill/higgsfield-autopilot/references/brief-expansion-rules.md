# Brief Expansion Rules

How to turn a one-sentence brief into a JSON shot list.

## Input shape

Briefs are conversational, often a single sentence. Examples (decoded from the reel + plausible variants):

- `"va me faire une campagne éditorial retro futuristique"` (the actual reel brief)
- `"make me a moody coffee shop reel for a barista brand"`
- `"luxury watch unboxing in a brutalist concrete interior"`

Briefs may be in any language. Prompts to Soul Cinema should be in **English** regardless (Higgsfield's training data is English-dominant).

## Output shape

```json
{
  "title": "Retro-futuristic editorial fashion campaign",
  "brief_original": "va me faire une campagne éditorial retro futuristique",
  "language": "fr",
  "aspect": "9:16",
  "shot_count": 5,
  "estimated_credits": 100,
  "shots": [
    {
      "id": 1,
      "purpose": "establish",
      "duration_target_s": 4,
      "prompt": "<full Soul Cinema prompt per soul-cinema-prompting.md>"
    },
    {
      "id": 2,
      "purpose": "subject_intro",
      "duration_target_s": 4,
      "prompt": "..."
    }
  ]
}
```

Save to `runs/<YYYY-MM-DD-HHMM>/shotlist.json`.

## How to choose `shot_count`

| Total target duration | Shot count |
|---|---|
| 10–15s reel | 3–4 shots |
| 15–25s reel | 4–6 shots |
| 25–40s reel | 6–8 shots |

Default to **5 shots** for a one-line brief without duration guidance. The reel's example had 5 distinct visual setups (driving POV → exterior establish → wheel detail → model + car → motion blur action).

## Shot purpose taxonomy

Use these `purpose` values (consistent across runs makes vision-pick easier in step 6):

| Purpose | Function in the cut |
|---|---|
| `establish` | Wide environment, sets the world |
| `subject_intro` | First reveal of the protagonist |
| `subject_detail` | Tight crop on subject, expression / texture |
| `object_detail` | Tight crop on the hero product / object |
| `motion` | Kinetic shot, movement-driven |
| `interaction` | Subject + object interacting |
| `mood` | Atmospheric beat, lighting-driven |
| `closer` | Final beat, often slow / quiet |

A 5-shot reel typically goes: `establish → subject_intro → object_detail → motion → closer` (or similar). Use the brief's energy to choose.

## Continuity rules

- **Same palette across all shots** — pick 3–5 dominant colours from the brief vibe; reuse in every shot's prompt.
- **Same lighting register** — if the brief implies sunset, every shot says some variant of sunset. No mixing dawn + noon + dusk in one campaign.
- **Same subject identity language** — if shot 2 says "a woman with a low ponytail in a pale yellow halter dress", shot 4 must use the same description verbatim. Higgsfield has no character-consistency layer at this skill's level (Soul ID is out of scope).
- **Aspect always 9:16 for v1** — landscape support not yet wired into `03-generate-asset.py`.

## Worked example (from the reel)

**Brief:** `va me faire une campagne éditorial retro futuristique`

**Decoded shotlist** (reverse-engineered from final video frames):

```json
{
  "title": "Retro-futuristic editorial fashion campaign",
  "brief_original": "va me faire une campagne éditorial retro futuristique",
  "language": "fr",
  "aspect": "9:16",
  "shot_count": 5,
  "shots": [
    {
      "id": 1,
      "purpose": "establish",
      "prompt": "Aerodynamic retro-futuristic capsule car, white seamless body lacking visible wheels, parked low on a flat sandy desert plain at dusk. Wide low-angle composition. Sky in painterly gradient of sunset pink, purple, blue. Silhouetted foothills on horizon. Pastel mauve, off-white, blush, sandy beige palette. Diffused dusk lighting, no harsh shadows. Painterly editorial fashion photography style."
    },
    {
      "id": 2,
      "purpose": "subject_intro",
      "prompt": "A woman with a low ponytail in a pale yellow silk halter dress walks slowly toward camera in front of the parked retro-futuristic capsule car. Desert sunset behind her. Painterly diffused light wrapping her face. Pastel mauve, off-white, blush, sandy beige palette. Editorial fashion photography, deep focus."
    },
    {
      "id": 3,
      "purpose": "object_detail",
      "prompt": "Tight low-angle close-up of the rear of a retro-futuristic white capsule car at dusk, glowing red taillight strip illuminated, dust kicked up against pastel sunset gradient sky. Pastel mauve, off-white, blush, sandy beige palette. Soft diffused light. Editorial automotive photography style."
    },
    {
      "id": 4,
      "purpose": "motion",
      "prompt": "Tight low-angle tracking shot of a wheel of a retro-futuristic white capsule car at dusk, red glowing ring of motion blur around the wheel, dust trailing behind, desert ground rushing past. Pastel sky. Pastel mauve, off-white, blush, sandy beige palette. Kinetic editorial cinematography."
    },
    {
      "id": 5,
      "purpose": "closer",
      "prompt": "A woman with a low ponytail in a pale yellow silk halter dress reclines against the hood of a retro-futuristic white capsule car at dusk. Mountain silhouettes behind. Painterly diffused light, pastel pink and purple gradient sky. Pastel mauve, off-white, blush, sandy beige palette. Calm, intimate editorial fashion close. Deep focus."
    }
  ]
}
```

Note how every shot reuses: the car description, the palette line, the lighting register, and the editorial-photography framing. That's continuity in action.

## Edge cases

- **Brief is already a shot list.** If the user hands you a JSON or numbered list, skip expansion — go straight to step 3.
- **Brief is multiple sentences with strong creative direction.** Honour the user's vision verbatim where possible; only expand the parts they leave open.
- **Brief is hostile / out-of-scope.** Refuse: "Soul Cinema is editorial; that prompt isn't a fit for this skill."
