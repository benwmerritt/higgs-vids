# Pattern: Character Campaign — STUB (v3.1)

> **Status: stub.** v3.1 will fill out the full recipe.

## When to use

- Brief features a recurring character, brand mascot, or named talent across multiple shots
- Visual identity must stay consistent across the campaign
- Output: a series of stills/videos all featuring the same person/character

## Inputs

- **Character source** — one of:
  - 5+ photos of a real person (we train a Soul ID)
  - A preset avatar from `higgs marketing-studio avatars list` (9 ship free)
  - An existing trained Soul ID
- **Campaign brief** — multi-shot concept featuring the character
- **Style direction** — same prompting rules as other patterns

## Cost envelope (TBD)

- Soul ID training: ~free (one-time)
- Per shot using `--soul-id`: same as without (~12-30 credits stills, ~200-2,500 video)

## Minimal v3.0 implementation

### One-time: train Soul ID (skip if user already has one or wants a preset)

```bash
# Upload character photos
IMG_IDS=()
for img in character-photos/*.{jpg,png}; do
  ID=$(higgs --json upload create "$img" | jq -r '.id')
  IMG_IDS+=(--image "$ID")
done

# Train (need 5+ images)
SOUL_RESULT=$(higgs --json soul-id create --name "$CHARACTER_NAME" --soul-2 "${IMG_IDS[@]}")
SOUL_ID=$(echo "$SOUL_RESULT" | jq -r '.id')

# Wait for training
higgs soul-id wait "$SOUL_ID"
```

### Or pick a preset

```bash
higgs --json marketing-studio avatars list | jq '.[] | select(.name == "Sofia") | .id'
```

### Per-shot generation

Use `text2image_soul_v2 --soul-id <id>` instead of `soul_cinematic`:

```bash
higgs --json generate create text2image_soul_v2 \
  --prompt "$SHOT_PROMPT" \
  --soul-id "$SOUL_ID" \
  --aspect_ratio 9:16 \
  --wait
```

Then animate as in `product-reel.md`.

## v3.1 TODO

- Soul ID lifecycle management (rename, delete, version)
- Multi-character scenes (two trained Soul IDs in one shot — supported?)
- Wardrobe/costume consistency layer (separate from face)
- Hair/age progression for time-lapse character work
- Integration with marketing-studio avatars + products

## Open questions for the agent

If the brief mentions a character without a Soul ID and the user has no presets that fit:
1. Ask if they want to train a Soul ID (need 5+ photos)
2. Ask if a preset (Jayden/Stefan/Mei/Yuna/Adriana/Clara/Maria/Sofia/Valentina) would do
3. Otherwise warn that face consistency across shots will be limited
