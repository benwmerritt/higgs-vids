# Pattern: Quick Social

Low-credit, fast-turn social content. Single shot or 2-3 shot mini-reel. For daily posting cadence where production value < volume.

## When to use

- Brief asks for a single social post (still or short video)
- Budget is explicitly low or unspecified-but-tight
- Time pressure ("need it in the next hour")
- The user's recurring/repeatable workflow ("daily X for Y campaign")

If the brief implies a production hero piece, use `product-reel.md` instead.

## Inputs

- **Concept** — one sentence
- **Format** (optional) — `still` (default) | `short-video` (1-3 shots, 5s each)
- **Aspect** (optional) — defaults to 9:16
- **Optional product/scene image** — for ref

## Cost envelope

| Variant | Models | Total |
|---|---|---|
| Single still | soul_cinematic ×1 | ~12 credits |
| 4-variant still | soul_cinematic ×4 (or `image_auto --batch_size 4` if supported) | ~48 credits |
| 1-shot short video | soul_cinematic + kling2_6 | ~210 credits |
| 3-shot mini-reel | (soul_cinematic + kling2_6) ×3 | ~630 credits |

Always run `higgs generate cost` per `references/cost-discipline.md` to confirm.

## Steps

### 0. Pre-flight + observability + live model check

Use the canonical run-init snippet from `references/output-management.md` § commands.log. Required models depend on variant:

```bash
PATTERN=quick-social
REQUIRED_IMAGE_MODELS=("soul_cinematic")
# Only check video models if user wants the short-video variant:
[ "$VARIANT" = "short-video" ] || [ "$VARIANT" = "3-shot-mini-reel" ] && REQUIRED_VIDEO_MODELS=("kling2_6")
```

This initialises:
- `<run-dir>/commands.log` (audit trail)
- `<run-dir>/models-available.txt` (saved `higgs model list --image`; `+ models-available-video.txt` if video variant)
- `START`, `PREFLIGHT`, `MODELS`, `CHECK` lines

If any required model is missing → stop, surface to user. Every subsequent `higgs` invocation appends a line to `commands.log` (GEN / DL / END).

### 1. Determine variant

Read the brief. Default to `single still` unless brief mentions "video", "reel", "motion", or "animate". If video, default to `1-shot short video` unless brief explicitly says "multi-shot."

### 2. Build the prompt

Apply `references/soul-cinema-prompting.md` rules — Subject → Scene → Action → Camera Feel → Lighting → Style. Keep it tight (40-60 words for quick-social).

Save to `runs/<RUN_ID>/prompt.txt`.

### 3. Cost preflight + spend

```bash
COST=$(higgs --json generate cost soul_cinematic --prompt "$PROMPT" | jq -r '.cost')
# (Per cost-discipline thresholds: <50 credits = silent proceed)

mkdir -p runs/$RUN_ID
RESULT=$(higgs --json generate create soul_cinematic --prompt "$PROMPT" --aspect_ratio "$ASPECT" --wait)
JOB_ID=$(echo "$RESULT" | jq -r '.id')
URL=$(echo "$RESULT" | jq -r '.result_url')
curl -sL "$URL" -o runs/$RUN_ID/still.png
```

For variants (multi-still): loop with same prompt, save as `still-1.png` … `still-4.png`. Optionally use `--medias` with prior outputs to chain similar variations.

### 4. (If short-video variant) Animate

For each still:
```bash
RESULT=$(higgs --json generate create kling2_6 \
  --start-image runs/$RUN_ID/still.png \
  --prompt "$MOTION" \
  --aspect_ratio "$ASPECT" \
  --duration 5 \
  --wait)
URL=$(echo "$RESULT" | jq -r '.result_url')
curl -sL "$URL" -o runs/$RUN_ID/clip.mp4
```

### 5. (If 3-shot mini-reel) Repeat steps 3-4 per shot, then ffmpeg concat

Same as `product-reel.md` step 6, but with shorter shots and lighter crossfade.

### 6. Bundle + report

```bash
mkdir -p runs/$RUN_ID/deliverables
cp runs/$RUN_ID/{still.png,clip.mp4,reel-final.mp4} runs/$RUN_ID/deliverables/ 2>/dev/null
```

Write `deliverables/README.md` with the standard fields. Tell the user the path + cost.

## Outputs

```
runs/<RUN_ID>/
├── brief.md
├── prompt.txt
├── pattern.txt           ← "quick-social"
├── cost-log.json
├── commands.log                    ← every higgs invocation (audit trail)
├── models-available.txt            ← snapshot of `higgs model list --image` at run start
├── still.png             (always)
├── clip.mp4              (if video variant)
├── reel-final.mp4        (if 3-shot mini-reel)
└── deliverables/
    ├── (whichever final asset(s))
    └── README.md
```

## Common variations

- **Daily template** — user runs the same pattern with rotating prompts. Save the prompt template in `briefs/`, reference it from a cron / daily routine.
- **Caption pairing** — extend the agent's report to include a suggested IG caption based on the brief. (Out of scope for v3.0; nice-to-have.)
- **Multi-aspect single concept** — if the user wants the same concept in 9:16 + 1:1 + 16:9, switch to `multi-platform-render.md`.

## Failure handling

Same as `product-reel.md`. Quick-social runs are usually so fast that retrying the whole pattern is cheaper than diagnosing — if a single shot fails, just re-run with `--force`.
