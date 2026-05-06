# Pattern: Multi-Platform Render

One creative concept rendered to multiple aspect ratios for cross-platform distribution. E.g. a campaign visual that needs to ship as 9:16 (IG Reels), 1:1 (IG feed), 16:9 (YouTube/web).

## When to use

- Brief mentions multiple platforms or aspect ratios
- Brief says "make this for IG, TikTok, and YouTube" or similar
- Brand needs platform-native deliverables from one concept

## Inputs

- **Concept** — one sentence (a single creative idea)
- **Aspects** — comma-separated list of aspect ratios. Defaults to `9:16,1:1,16:9` if not specified.
- **Format** (optional) — `still` (default) or `video`
- **Optional reference image**

## Cost envelope

For one concept × 3 aspects, **stills only**:

| Tier | Per render | Total |
|---|---|---|
| Cheap | soul_cinematic ~12 | ~36 |
| Mid | nano_banana_2 ~30 | ~90 |

For one concept × 3 aspects, **video** (5s each):

| Tier | Per render | Total |
|---|---|---|
| Cheap | soul_cinematic + kling2_6 ~210 | ~630 |
| Mid | soul_cinematic + cinematic_studio_3_0 ~2,512 | ~7,536 |

## Why not just generate 16:9 and crop?

You can — for some content. But:
- 9:16 needs different composition (subject vertical-friendly, headroom)
- 1:1 needs centred subject
- 16:9 needs negative space on the sides

Higgsfield's models compose differently per aspect. Native generation per aspect typically beats crop. For brand-critical work, generate each. For drafts, crop.

The agent should ask the user once when this pattern starts: "Generate native per aspect (3× cost) or generate one then crop (1× cost, lower quality on extreme aspects)?"

## Steps

### 0. Pre-flight + observability + live model check + clarify approach

Use the canonical run-init snippet from `references/output-management.md` § commands.log:

```bash
PATTERN=multi-platform-render
REQUIRED_IMAGE_MODELS=("soul_cinematic")
# Add video models only if user picks video variant:
# REQUIRED_VIDEO_MODELS=("kling2_6")  # or cinematic_studio_3_0 for mid tier
```

This initialises `<run-dir>/commands.log` + `<run-dir>/models-available.txt` and writes START / PREFLIGHT / MODELS / CHECK lines. If any required model is missing → stop.

Per cost-discipline: confirm workspace, balance, and ask the native-vs-crop question.

Every subsequent `higgs` invocation appends a line to `commands.log` (GEN / DL / END).

### 1. Build one shared prompt

The concept is shared. The prompt should be aspect-agnostic — describe the subject + scene + style, *don't* describe composition specifics ("centred", "vertical-leading subject" etc.) since those vary by aspect.

Save to `runs/<RUN_ID>/concept.txt`.

### 2. Cost preflight (per aspect)

```bash
TOTAL=0
for aspect in $ASPECTS; do
  COST=$(higgs --json generate cost soul_cinematic --prompt "$PROMPT" | jq -r '.cost')
  TOTAL=$((TOTAL + COST))
  echo "  $aspect: $COST credits"
done
echo "Total: $TOTAL credits"
```

(Cost may vary by aspect for some models; preflight each separately to be sure.)

### 3. Generate per aspect

```bash
for aspect in $ASPECTS; do
  ASPECT_TAG=${aspect//:/x}  # "9:16" → "9x16" for filenames
  mkdir -p runs/$RUN_ID/$ASPECT_TAG

  RESULT=$(higgs --json generate create soul_cinematic \
    --prompt "$PROMPT" \
    --aspect_ratio "$aspect" \
    --wait)
  URL=$(echo "$RESULT" | jq -r '.result_url')
  curl -sL "$URL" -o runs/$RUN_ID/$ASPECT_TAG/render.png
done
```

For video variant: chain still → video per aspect (same as product-reel pattern but per aspect).

### 4. (If crop-from-one variant)

Generate the canonical 1:1 (most universal), then ffmpeg-crop:

```bash
# 1:1 → 9:16 by adding letterbox pad
ffmpeg -i canonical.png -vf "scale=1080:1080,pad=1080:1920:0:420:black" 9x16/render.png

# 1:1 → 16:9 by cropping height + adding side bars OR using a different crop strategy
ffmpeg -i canonical.png -vf "scale=1080:1080,pad=1920:1080:420:0:black" 16x9/render.png
```

(Subject-aware cropping is better than letterboxing — leave that as a v3.1 enhancement.)

### 5. Bundle deliverables

```bash
mkdir -p runs/$RUN_ID/deliverables
for aspect in $ASPECTS; do
  ASPECT_TAG=${aspect//:/x}
  cp runs/$RUN_ID/$ASPECT_TAG/render.* runs/$RUN_ID/deliverables/render-$ASPECT_TAG.${EXT}
done
```

Output naming: `render-9x16.png`, `render-1x1.png`, `render-16x9.png`. Predictable for downstream tools.

### 6. Report

Tell the user the bundle path. List each rendered aspect with file size.

## Outputs

```
runs/<RUN_ID>/
├── brief.md
├── concept.txt
├── pattern.txt           ← "multi-platform-render"
├── cost-log.json
├── commands.log                    ← every higgs invocation (audit trail)
├── models-available.txt            ← snapshot of `higgs model list --image` at run start
├── 9x16/render.png  (or .mp4)
├── 1x1/render.png
├── 16x9/render.png
└── deliverables/
    ├── render-9x16.png
    ├── render-1x1.png
    ├── render-16x9.png
    └── README.md
```

## Common variations

- **One-aspect-per-platform** — if the user names platforms instead of aspects, map: IG-Reels/TikTok → 9:16, IG-Feed → 1:1, YouTube → 16:9, Twitter/X → 16:9 or 1:1.
- **More than 3 aspects** — agent shouldn't refuse, but should warn if >5: cost compounds quickly.
- **Brand watermark** — out of scope for v3.0. ffmpeg overlay is straightforward; defer to user post-process.

## Failure handling

Per-aspect failures are independent. If 9:16 fails but 1:1 + 16:9 succeed, deliver the two and tell the user which one is missing. Don't roll back the run.
