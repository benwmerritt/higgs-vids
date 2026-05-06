# Stage 3 — Full Reel Smoke Test

> **Invoke:** `/higgsfield-test 3` or *"Read `skill/higgsfield-autopilot/test/stage-3.md` and execute it."*

**Cost: ~1,000 credits (cheap tier) to ~12,500 credits (mid tier).** Don't run until stage 1 + 2 have passed in the same session AND you have the credits.

**Purpose:** End-to-end smoke — execute the full `product-reel.md` pattern on `example-retro-futuristic.md` and produce `runs/<date>/deliverables/reel-final.mp4`. This is the production path; if it works, the toolkit ships.

## Pre-conditions

```bash
BAL=$(higgs --json account status | jq -r '.credits')
[ "$BAL" -lt 1000 ] && { echo "Need ≥1000 credits for cheap tier, have $BAL."; exit 1; }
which ffmpeg >/dev/null || { echo "ffmpeg required for assembly. Install: brew install ffmpeg"; exit 1; }
```

Stage 1 + 2 reports exist for recent runs. (Not strictly enforceable; just don't blow money on a setup that hasn't been validated.)

## Steps

### 1. Read instructions

SKILL.md, all references, `patterns/product-reel.md`, `briefs/example-retro-futuristic.md`.

### 2. Pre-flight

Verify auth + workspace. If active workspace isn't what the user wants charged, stop.

### 3. Expand brief into shotlist (5 shots, 9:16)

Save to `runs/<RUN_ID>/shotlist.json`.

### 4. Cost preflight (sum across all shots)

For mid tier (default):
```bash
TOTAL=0
for shot in shotlist.shots; do
  STILL=$(higgs --json generate cost soul_cinematic --prompt "$STILL_PROMPT" | jq -r '.cost')
  VIDEO=$(higgs --json generate cost cinematic_studio_3_0 --prompt "$MOTION_PROMPT" | jq -r '.cost')
  TOTAL=$((TOTAL + STILL + VIDEO))
done
echo "Mid-tier total: $TOTAL"
```

Cost-discipline thresholds apply: this is almost certainly >1000 credits, so itemise the breakdown and ask explicit confirmation.

### 5. If estimate exceeds balance — propose cheap tier

Recompute with `kling2_6` instead of `cinematic_studio_3_0` for video. Tell the user:
> "Mid-tier estimate $X exceeds balance $BAL. Cheap-tier alternative: $Y credits using kling2_6 instead of cinematic_studio_3_0. Proceed with cheap tier?"

Only continue with explicit confirmation.

### 6. Execute pattern (steps 4-7 of product-reel.md)

Per shot:
- Generate still (`soul_cinematic --prompt ... --aspect_ratio 9:16 --wait`)
- Save URL, download to `shot-NN/still.png`
- Animate (`<video_model> --image $STILL_JOB_ID --prompt ... --duration 5 --wait`)
- Save URL, download to `shot-NN/take-1.mp4`
- Symlink `take-best.mp4 → take-1.mp4`

If a shot fails: log it, continue with the next. Don't kill the run.

Hard cap: 60 minutes total wall-clock.

### 7. Assemble + bundle

```bash
python skill/higgsfield-autopilot/scripts/assemble-video.py \
    --run-dir runs/$RUN_ID \
    --crossfade-ms 250 \
    --force

mkdir -p runs/$RUN_ID/deliverables
cp runs/$RUN_ID/final.mp4 runs/$RUN_ID/deliverables/reel-final.mp4
ffmpeg -y -i runs/$RUN_ID/deliverables/reel-final.mp4 -vframes 1 runs/$RUN_ID/deliverables/poster.png
```

Write `runs/$RUN_ID/deliverables/README.md` with: brief title, pattern, total spend, runtime, models used, any failed shots.

### 8. Verify the final

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \
  runs/$RUN_ID/deliverables/reel-final.mp4
```

Should be ~25s for 5 × 5s shots. If wildly different, something's off.

### 9. Write the stage report

`runs/<RUN_ID>/stage-3-report.md`:

1. **Generation summary** — table per shot: prompt summary, time, success/fail, video model used, take chosen
2. **Total credit spend** — actual delta from `account status` before/after
3. **Final video** — path, duration, dimensions, file size
4. **Failures + recoveries** — what needed retry and how
5. **Tool call count** — rough breakdown of `higgs` invocations + bash subprocess calls
6. **Recommended changes** — concrete diffs to SKILL.md, patterns, references
7. **Open questions** — what we couldn't validate (audio, longer videos, Soul ID, etc.)

Then: `Stage-3 report: <path>. Final video: <path>.`

## Constraints

- **Confirm total cost before starting** if estimate exceeds 1000 credits (almost certain).
- **60-minute wall-clock cap.** If past, stop and report whatever state we reached.
- **A failed shot doesn't kill the run** — better a 4-shot final than no final.
- **Don't commit. Don't edit `skill/` files** (you can edit your run dir freely). Don't install anything.

Begin.
