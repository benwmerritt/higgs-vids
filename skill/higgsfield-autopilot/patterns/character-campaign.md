# Pattern: Character Campaign

A multi-shot campaign featuring a recurring person, brand mascot, or named talent — face-faithful across every shot. Built around Soul ID training + reuse.

## When to use

- Brief features a recurring character (model, presenter, brand mascot, named talent)
- Visual identity must stay consistent across multiple shots / multiple campaigns
- Output: a series of stills/videos, all featuring the same person/character
- The user has 5+ photos of the person (or wants to use a preset avatar)

## Inputs

The user provides one of:

1. **5+ photos of a real person** → train a Soul ID
2. **A preset avatar name** from `higgs marketing-studio avatars list` (40+ ship in every account, see `references/cli-cheatsheet.md`)
3. **An existing trained Soul ID** (UUID from prior `higgs soul-id create`)

Plus the campaign brief (multi-shot concept).

## Cost envelope (rack-rate; subscriber absorption applies)

| Phase | Rack-rate cost |
|---|---|
| Soul ID training (one-time) | **Unknown** — could be free, could be ~50-200 credits. Measure on first run; see `references/empirical-tests.md` Test 3. |
| Per-shot generation (still) | Same as `product-reel.md` — uses `text2image_soul_v2` instead of `soul_cinematic` |
| Per-shot animation (video) | Same as `product-reel.md` — `cinematic_studio_3_0` or alternatives |
| 5-shot reel total | ~12,500 credits rack at mid-tier (likely heavily absorbed on paid plans) |

## Pre-conditions

- **Plan minimum:** any paid tier — Soul ID training requires "Basic+" per upstream skill (works on Starter/Basic/Plus/Pro/Ultra etc.). Free plan **cannot** train Soul IDs. Check via `higgs --json account status` before training.
- **Photo quality:** Soul 2.0 product page recommends **20+ well-lit, varied photos** (frontal, ¾ profile, varied lighting). The CLI's hard floor is 5 — but 5 photos produces noticeably worse identity than 20.

## Steps

### 0. Pre-flight + observability + live model check

Use the canonical run-init snippet from `references/output-management.md` § commands.log:

```bash
PATTERN=character-campaign
REQUIRED_IMAGE_MODELS=("text2image_soul_v2")              # Soul ID image generation
REQUIRED_VIDEO_MODELS=("cinematic_studio_3_0")            # downstream video (mid-tier default)
# soul-id is a separate command, not a model — its presence is verified by `higgs soul-id --help` if needed
```

This initialises `<run-dir>/commands.log` + `<run-dir>/models-available.txt` (image and video lists), writes START / PREFLIGHT / MODELS / CHECK lines.

If any required model is missing → stop. Particularly important here: `text2image_soul_v2` is the model that consumes `--soul-id` UUIDs. If it's been renamed or deprecated (Soul 3.0 is rumoured), `higgs model list --image` will surface the replacement; check the model list before training a Soul ID.

Every subsequent `higgs` invocation appends a line to `commands.log` (UPLOAD / GEN / DL / and `SOULID-TRAIN` / `SOULID-WAIT` for Soul ID phases / END).

### 1. Decide character source

Read the brief. If it mentions:
- A real person + photos provided → **train Soul ID** (this pattern, full path)
- "Use a preset model" or names a preset (Sofia, Yuna, etc.) → **skip training**, use preset avatar
- An existing `soul_id` UUID → **skip training**, reuse

### 2. (If training) Validate photo set

```bash
PHOTOS=(./talent-photos/*.{jpg,png,jpeg})
COUNT=${#PHOTOS[@]}
echo "$COUNT photos provided"

if [ "$COUNT" -lt 5 ]; then
  echo "Need ≥5 photos to train. Stopping."
  exit 1
fi
if [ "$COUNT" -lt 12 ]; then
  echo "WARN: $COUNT photos is below the recommended 20+. Identity may be weak across shots."
  # Tell user, ask whether to proceed
fi
```

Tell the user the photo count + warn if low.

### 3. (If training) Upload + train Soul ID

```bash
IMG_IDS=()
for img in "${PHOTOS[@]}"; do
  ID=$(higgs --json upload create "$img" | jq -r '.id')
  IMG_IDS+=(--image "$ID")
done

# Pick variant based on downstream use
# Brief implies images mostly → --soul-2 (default)
# Brief implies cinematic / video heavy → --soul-cinematic
SOUL_RESULT=$(higgs --json soul-id create --name "$CHARACTER_NAME" --soul-2 "${IMG_IDS[@]}")
SOUL_ID=$(echo "$SOUL_RESULT" | jq -r '.id')

# Block until training completes (~3-5 minutes)
higgs soul-id wait "$SOUL_ID"

# Read balance to learn training cost
BAL_AFTER_TRAIN=$(higgs --json account status | jq -r '.credits')
TRAINING_COST=$((BAL_BEFORE - BAL_AFTER_TRAIN))
echo "Soul ID $SOUL_ID trained. Cost: $TRAINING_COST credits."
```

Save `$SOUL_ID` to `runs/<RUN_ID>/soul-id.txt` so future runs in this campaign can reuse it.

If training fails: check photo quality (see `references/known-issues.md`) and tell the user. Common failures: too few unique faces, poor lighting, sunglasses/hats covering features.

### 4. Generate stills with Soul ID

For each shot in the shotlist (per `patterns/product-reel.md` step 1-3):

```bash
RESULT=$(higgs --json generate create text2image_soul_v2 \
  --prompt "$STILL_PROMPT" \
  --soul-id "$SOUL_ID" \
  --aspect_ratio 9:16 \
  --wait --wait-timeout 5m)
```

Save job ID + result URL per shot, download per `patterns/product-reel.md` recipe.

### 5. Animate stills (per `patterns/product-reel.md` step 5)

`text2image_soul_v2` produces a still. Pipe its job ID as `--image` to a video model:

```bash
RESULT=$(higgs --json generate create cinematic_studio_3_0 \
  --image "$STILL_JOB_ID" \
  --prompt "$MOTION_PROMPT" \
  --aspect_ratio 9:16 \
  --duration 5 \
  --wait)
```

Soul identity carries through the still → video chain because the video model is conditioned on the Soul-faithful start frame.

### 6. Assemble + bundle (per `patterns/product-reel.md` steps 6-8)

ffmpeg concat → `runs/<RUN_ID>/deliverables/reel-final.mp4`.

### 7. Reuse the Soul ID across campaigns

Save `$SOUL_ID` somewhere persistent (the brief file, a project-level `soul-ids.json`, or a top-level note). Future campaigns featuring the same character skip training and reuse the ID.

```bash
higgs soul-id list                         # browse all your trained Soul IDs
higgs soul-id get <id>                     # inspect one
```

## Outputs

Same as `patterns/product-reel.md`, plus:

```
runs/<RUN_ID>/
├── soul-id.txt                    ← UUID of Soul ID used (trained or reused)
├── soul-training-cost.txt         ← (if trained) credit delta from training
├── commands.log                   ← every higgs invocation (audit trail; includes SOULID-TRAIN / SOULID-WAIT)
├── models-available-image.txt     ← snapshot of `higgs model list --image`
├── models-available-video.txt     ← snapshot of `higgs model list --video`
└── ... (rest same as product-reel.md)
```

## Common variations

- **Preset avatar instead of Soul ID** — much faster (no training), but constrained to the 40+ preset characters. Use `higgs marketing-studio avatars list` to browse, then pass via avatar params in `marketing_studio_video` (different command — see `patterns/brand-shoot.md` for marketing flow).
- **Multiple characters** — train one Soul ID per character. Combining two trained Soul IDs in a single shot is **unverified** as of 2026-05-06. Default: one Soul ID per shot.
- **Cinematic-heavy campaign** — train with `--soul-cinematic` instead of `--soul-2`. Use with `soul_cinematic` model (image) and downstream video models.
- **Long-running campaign (months)** — Soul ID persistence across sessions/months is **unverified**. Test by running a low-cost shot months later — does the Soul ID still produce face-faithful output? If degradation, retrain.

## Failure handling

| Symptom | Action |
|---|---|
| `Minimum Basic plan required` (or similar) | User on Free plan. Stop. Tell them they need to upgrade for Soul ID. |
| `Training failed` | Check photo quality. Likely too few unique faces, too similar angles, or poor lighting. Ask user for more diverse photos and retry. |
| Soul ID training appears to consume zero credits | Probably normal on the user's plan (training likely free or absorbed). Log the observation in the run report. |
| `text2image_soul_v2` ignores `--soul-id` (output doesn't look like the trained character) | Verify `$SOUL_ID` is correct via `higgs soul-id get <id>`. If correct, may be a training-quality issue — retrain with more/better photos. |
| Faces still drift across shots even with Soul ID | Soul ID is conditioning, not lock — drift can happen with very different prompts. Use consistent subject-anchor language across all shots' `still_prompt` (per `references/brief-expansion-rules.md` continuity rule). |

## Open questions (research couldn't answer; see `references/empirical-tests.md`)

- Soul ID training credit cost
- Soul ID storage limits per plan
- Cross-workspace Soul ID sharing (Test 7)
- Whether `--soul-cinematic` produces meaningfully different results from `--soul-2` for cinematic video chains
- Compatibility list — does `cinematic_studio_3_0`, `marketing_studio_video`, etc. accept `--soul-id` directly or only via piped image inputs from a Soul-faithful still?
