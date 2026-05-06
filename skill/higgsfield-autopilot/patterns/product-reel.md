# Pattern: Product Reel

Turn a brief + (optional) product photo into a 9:16 multi-shot reel. The canonical/default pattern.

## When to use

- Brief asks for an Instagram Reel / TikTok / vertical video
- Brief implies multiple shots / a narrative arc
- Brief includes a product, scene, or hero subject
- Output target: a single playable .mp4 at 9:16

If the brief is *just* "make me a single video clip" with no narrative, prefer `quick-social.md`.

## Inputs (brief must provide, or the agent infers)

- **Concept** (required) — what the reel is about. One sentence is fine.
- **Optional product image** — a path to a local file or upload UUID. Used as `--medias` reference for stills.
- **Optional duration target** — defaults to 5 shots × 5s = 25s
- **Optional aspect** — defaults to 9:16

## Cost envelope

For 5 shots at 9:16:

| Tier | Still model | Video model | Per-shot cost | Total |
|---|---|---|---|---|
| **Cheap** | soul_cinematic (~12) | kling2_6 / minimax_hailuo (~200) | ~212 | **~1,060** |
| **Mid** (default) | soul_cinematic (~12) | cinematic_studio_3_0 (~2,500) | ~2,512 | **~12,560** |
| **Premium** | nano_banana_2 (~30) | veo3_1 (~5,000) | ~5,030 | **~25,150** |

**Default:** mid tier. If user balance < ~3,000 credits, drop to cheap tier and tell them.

## Steps

### 0. Pre-flight

```bash
# Verify auth + workspace
higgs --json account status | jq '{credits, plan}'
higgs --json workspace status | jq '{name, id}'
```

If active workspace looks wrong for this brief (e.g. brief mentions client X but workspace is "Private"), **stop** and ask the user to confirm or switch via `higgs workspace set <id>`.

### 1. Read brief + expand to shotlist

Per `references/brief-expansion-rules.md`, produce a 3-8 shot list. Save to `runs/<RUN_ID>/shotlist.json`. Default 5 shots, 9:16, English prompts. Each shot has:
- `id`, `purpose` (establish/subject_intro/object_detail/motion/closer)
- `still_prompt` (Soul Cinematic prompt per `references/soul-cinema-prompting.md`)
- `motion_prompt` (camera + subject motion description for the video model — keep short, see soul-cinema-prompting Mode 2 / Mode 3 guidance)

### 2. Upload reference image (if provided)

```bash
if [ -n "$PRODUCT_IMAGE" ]; then
  REF_ID=$(higgs --json upload create "$PRODUCT_IMAGE" | jq -r '.id')
  echo "$REF_ID" > runs/$RUN_ID/reference-upload-id.txt
fi
```

### 3. Cost preflight (sum across all shots)

For each shot, compute still + video cost separately:

```bash
TOTAL=0
for shot in shots; do
  STILL_COST=$(higgs --json generate cost soul_cinematic --prompt "$STILL_PROMPT" | jq -r '.cost')
  VIDEO_COST=$(higgs --json generate cost cinematic_studio_3_0 --prompt "$MOTION_PROMPT" | jq -r '.cost')
  TOTAL=$((TOTAL + STILL_COST + VIDEO_COST))
done
```

Then per `references/cost-discipline.md`:
- Compare TOTAL against current balance
- If TOTAL > balance: stop, report gap
- If TOTAL > 1000: itemise breakdown, ask explicit confirmation
- Else: report estimate, proceed

### 4. Generate stills (per shot)

For each shot:

```bash
mkdir -p runs/$RUN_ID/shot-$NN
echo "$STILL_PROMPT" > runs/$RUN_ID/shot-$NN/still-prompt.txt

ARGS=(soul_cinematic --prompt "$STILL_PROMPT" --aspect_ratio 9:16 --wait --wait-timeout 5m)
[ -n "$REF_ID" ] && ARGS+=(--medias "$REF_ID")

RESULT=$(higgs --json generate create "${ARGS[@]}")
JOB_ID=$(echo "$RESULT" | jq -r '.id')
URL=$(echo "$RESULT" | jq -r '.result_url')

echo "$JOB_ID" > runs/$RUN_ID/shot-$NN/still-job-id.txt
echo "$URL" > runs/$RUN_ID/shot-$NN/still-url.txt
curl -sL "$URL" -o runs/$RUN_ID/shot-$NN/still.png
```

Stills can be done sequentially (cheap, fast) or in parallel via tab background (faster but more bash gymnastics — sequential is fine for 5 shots).

### 5. Animate stills (per shot)

```bash
echo "$MOTION_PROMPT" > runs/$RUN_ID/shot-$NN/motion-prompt.txt
STILL_JOB=$(cat runs/$RUN_ID/shot-$NN/still-job-id.txt)

RESULT=$(higgs --json generate create cinematic_studio_3_0 \
  --image "$STILL_JOB" \
  --prompt "$MOTION_PROMPT" \
  --aspect_ratio 9:16 \
  --duration 5 \
  --wait --wait-timeout 15m)

JOB_ID=$(echo "$RESULT" | jq -r '.id')
URL=$(echo "$RESULT" | jq -r '.result_url')

echo "$JOB_ID" > runs/$RUN_ID/shot-$NN/video-job-id.txt
echo "$URL" > runs/$RUN_ID/shot-$NN/video-url.txt
curl -sL "$URL" -o runs/$RUN_ID/shot-$NN/take-1.mp4
ln -sf take-1.mp4 runs/$RUN_ID/shot-$NN/take-best.mp4
```

Note: the still's job_id is passed as `--image` to the video model. Higgsfield resolves it server-side; no re-upload.

If a video shot fails, log the failure but continue with remaining shots. Better a 4-shot final than nothing.

### 6. Assemble

```bash
python skill/higgsfield-autopilot/scripts/assemble-video.py \
    --run-dir runs/$RUN_ID \
    --crossfade-ms 250 \
    --force
```

Produces `runs/$RUN_ID/final.mp4`.

### 7. Bundle deliverables

```bash
mkdir -p runs/$RUN_ID/deliverables
cp runs/$RUN_ID/final.mp4 runs/$RUN_ID/deliverables/reel-final.mp4
# Optional: extract poster frame
ffmpeg -y -i runs/$RUN_ID/final.mp4 -vframes 1 runs/$RUN_ID/deliverables/poster.png
```

Write `runs/$RUN_ID/deliverables/README.md` with: brief title, pattern, total spend, runtime, models used, any caveats.

### 8. Cost ledger

Update `runs/$RUN_ID/cost-log.json` (per `references/output-management.md`) and append a one-liner to `runs/cost-summary.json`.

### 9. Report

Tell the user:
- Path to `runs/$RUN_ID/deliverables/reel-final.mp4`
- Total cost (balance_before − balance_after)
- Number of shots, total duration (`ffprobe`)
- Any failed shots or surprises

## Outputs

```
runs/<RUN_ID>/
├── brief.md
├── shotlist.json
├── cost-log.json
├── pattern.txt           ← "product-reel"
├── reference-upload-id.txt   (if product image was provided)
├── shot-{01..NN}/
│   ├── still-prompt.txt
│   ├── still-job-id.txt
│   ├── still-url.txt
│   ├── still.png
│   ├── motion-prompt.txt
│   ├── video-job-id.txt
│   ├── video-url.txt
│   ├── take-1.mp4
│   └── take-best.mp4 → take-1.mp4
└── deliverables/
    ├── reel-final.mp4
    ├── poster.png
    └── README.md
```

## Common variations

- **Cheap-tier reel** — swap `cinematic_studio_3_0` → `kling2_6` or `minimax_hailuo` in step 5. Update cost preflight accordingly.
- **Premium-tier hero reel** — swap to `veo3_1` (supports native audio) and `nano_banana_2` for stills.
- **Recurring character** — train Soul ID first (`higgs soul-id create --name X --soul-2 --image x5`), then add `--soul-id <id>` to the still generation. Switches `soul_cinematic` → `text2image_soul_v2`.
- **Long-form** — chain multiple 5s shots with longer ffmpeg crossfades. Or use `cinematic_studio_3_0 --duration 10` if supported.

## Failure handling

| Symptom | Action |
|---|---|
| `higgs generate cost` errors | Check model name spelling. Run `higgs model list` to verify. |
| Still generation fails | Retry once with same prompt. If second fails, simplify prompt (drop the most flowery clause), retry. If still failing, skip the shot, log it. |
| Video generation hangs (>15min) | Don't kill — log timeout, continue with next shot. The job may still complete; you can recover via `higgs generate get <job_id>` later. |
| Out of credits mid-run | Stop. Report what completed. Don't auto-top-up — that's a user decision. |
| Asset URL returns 403/404 | Higgsfield URLs are signed and time-limited. Re-fetch via `higgs generate get <job_id>` to get a fresh URL. |
| ffmpeg concat fails on codec mismatch | `assemble-video.py` auto-falls back to re-encode. If that also fails, downloaded files are corrupt — re-download. |
