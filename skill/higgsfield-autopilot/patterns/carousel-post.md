# Pattern: Carousel Post

Take a topic + brand profile + (optional) source assets → produce a 5-10 slide IG/LinkedIn carousel that's post-ready. **Calibration-first** (one slide before the batch), **review-and-retry** (read every output before shipping), **per-slide folder structure** (no HTML, no stitched previews), **dated run dirs** (no writes to repo root).

> **Read `references/agent-tooling-rules.md` BEFORE running this pattern.** Image review uses the Read tool (Claude has vision). No Playwright MCP, no browser, no other skills.

## When to use

- Brief asks for an Instagram or LinkedIn carousel
- Output target: 5-10 connected slides (1080×1350 IG-native, or 1:1 if specified)
- Topic is educational / list / story / opinion-drop format
- Brand profile exists at `brands/<name>/profile.md` (use `/higgsfield-brand-create` first if not)

If the user wants a single-image post → `quick-social.md`. If video reel → `product-reel.md`.

## Inputs

- **Brand** (required) — name of an existing brand profile (`brands/<name>/profile.md`)
- **Topic** (required) — one sentence describing the carousel concept
- **Optional source asset(s)** — local file path(s) to anchor the carousel (a product photo, hero image, etc.)
- **Slide count** (optional) — defaults to 6; range 5-10
- **Aspect** (optional) — defaults to 4:5 (IG carousel native portrait); 1:1 for square
- **Platform** (optional) — defaults to instagram

## Cost envelope (rack-rate; ~99% absorbed on paid plans)

| Slide count | Stills (`soul_cinematic`) | Rack-rate total | Likely actual on Starter+ |
|---|---|---|---|
| 5 | 5 × 12 | ~60 credits | ~0.6 credits |
| 6 (default) | 6 × 12 | ~72 credits | ~0.7 credits |
| 8 | 8 × 12 | ~96 credits | ~1.0 credits |
| 10 | 10 × 12 | ~120 credits | ~1.2 credits |

**Caption + hashtags = free** (text). **Calibration adds ~12 rack credits / 0.12 actual** for the trial slide.

## Run directory naming (mandatory)

```
runs/<YYYY-MM-DD>-<brand>-carousel-<seq>/
```

- Date prefix mandatory (`2026-05-06`)
- Brand name lowercase
- `carousel` is the pattern type
- `<seq>` increments per same-day same-brand run (`-1`, `-2`, `-3`...)
- Examples: `runs/2026-05-06-ben-carousel-1/`, `runs/2026-05-06-ben-carousel-2/`

**Never write any output to the repo root.** Every artefact (prompts, JSON, downloaded images, review notes, captions) goes inside the run dir.

## The recipe

### Step 0 — Pre-flight + observability + tooling guardrails

Use the canonical run-init snippet from `references/output-management.md` § commands.log. For carousel-post the required models are:

```bash
PATTERN=carousel
REQUIRED_MODELS=("soul_cinematic")   # image-only pattern
MODEL_FILTER="--image"
```

This initialises:
- `<run-dir>/commands.log` (audit trail of every higgs invocation)
- `<run-dir>/models-available.txt` (snapshot of `higgs --json model list --image`)
- `START`, `PREFLIGHT`, `MODELS`, `CHECK soul_cinematic` lines in commands.log

If `soul_cinematic` is missing → stop, surface to user. If new image models appear → mention informationally.

Per `references/cost-discipline.md` + `references/agent-tooling-rules.md`:

**Hard rules for this run (re-read these every invocation):**
- ❌ Don't open a browser to view images. Use the Read tool — it has vision.
- ❌ Don't invoke Playwright MCP. We deleted that whole layer.
- ❌ Don't load other skills (frontend-design, etc.). Stay inside this bundle.
- ❌ Don't generate HTML index files. Output is PNGs the user posts.
- ❌ Don't generate one big stitched scrolling preview image. Each slide is its own file.
- ❌ Don't write anything to the repo root.
- ✅ Every `higgs` invocation in this run appends a line to `<run-dir>/commands.log` (GEN / DL / RETRY / FAIL / END).

### Step 1 — Load brand context

Read **all of these in full** (working memory for the run):

1. `brands/<name>/profile.md`
2. `brands/<name>/source-fetches/*.md` (most recent only)
3. `references/interview-craft.md` § AI-tells
4. `references/hook-craft.md` (slide 1 hook patterns)
5. `references/caption-craft.md` (caption shape + AI-tells, including em-dash ban)
6. `references/hashtag-strategy.md`
7. `references/agent-tooling-rules.md` (the Don'ts above)

If `confidence.spike` is `low` or `gap` in the profile → stop, tell user to refresh the brand profile. Carousels without a spike are AI slop.

### Step 2 — Pick the run dir + plan the carousel

Run dir: `runs/<YYYY-MM-DD>-<brand>-carousel-<seq>/` (calculate `<seq>` from existing dirs).

Plan slides per the structure (per MCP Q3):

| Slide | Job |
|---|---|
| Slide 1 — Hook | ≤10 words. Stop the scroll. Per `references/hook-craft.md`. |
| Slides 2..N-1 | One beat per slide. ≤15 words copy each. Build value. |
| Slide N-1 (often) | Social proof / testimonial / reinforcing example |
| Slide N — CTA | Or no CTA per brand profile. ≤10 words if present. |

**Default slide counts: 6 slides** (1 hook + 4 middle + 1 CTA).

Save planning to `<run-dir>/shotlist.json`.

### Step 3 — Hook options for slide 1 (user picks)

Per `references/hook-craft.md`, generate 3 hook variants in different patterns. Hard cap: **each option ≤10 words. No em dashes.**

```
Hook options for slide 1:

A) [conversational, ≤10 words]
B) [specific-number / time, ≤10 words]
C) [contrarian, ≤10 words]

I'd pick B because [reason from brand profile].
```

Wait for user pick. Update `shotlist.json` slide 1.

### Step 4 — CALIBRATION SHOT (slide 1 only)

**This step is mandatory.** Don't batch the whole carousel before confirming style.

```bash
mkdir -p <run-dir>/shot-01
echo "$IMAGE_PROMPT" > <run-dir>/shot-01/prompt.txt
echo "$SLIDE_COPY" > <run-dir>/shot-01/copy.txt

FULL_PROMPT="$IMAGE_PROMPT, $BRAND_PALETTE, $BRAND_PHOTO_AESTHETIC"
ARGS=(soul_cinematic --prompt "$FULL_PROMPT" --aspect_ratio "$ASPECT" --wait --wait-timeout 5m)
[ -n "$REF_UPLOAD_ID" ] && ARGS+=(--medias "$REF_UPLOAD_ID")
[ -n "$SOUL_ID" ] && [ "$SLIDE_HAS_PERSON" = "yes" ] && ARGS+=(--soul-id "$SOUL_ID")

RESULT=$(higgs --json generate create "${ARGS[@]}")
JOB_ID=$(echo "$RESULT" | jq -r '.id')
URL=$(echo "$RESULT" | jq -r '.result_url')

echo "$JOB_ID" > <run-dir>/shot-01/job-id.txt
echo "$URL" > <run-dir>/shot-01/url.txt
curl -sL "$URL" -o <run-dir>/shot-01/image.png
```

### Step 5 — REVIEW THE CALIBRATION (mandatory)

Use the **Read tool** on `<run-dir>/shot-01/image.png`. Claude has vision. Inspect against this checklist:

- ✅ Does the logo (if applicable) look intact and recognisable?
- ✅ Does the colour palette match the brand profile?
- ✅ Does the photo aesthetic match (e.g. natural light vs studio, intimate vs dramatic)?
- ✅ Does the composition support the slide's beat (room for text overlay if needed)?
- ✅ Does it look like the brand's content, or generic AI slop?
- ✅ Are there any AI tells (extra fingers, garbled logo text, distorted faces)?

Save findings to `<run-dir>/shot-01/review.md`:

```markdown
# Review — shot-01

**Logo intact:** yes / no — [details]
**Palette match:** yes / no — [details]
**Aesthetic match:** yes / no — [details]
**AI tells:** none / [list]
**Composition:** [notes]
**Verdict:** ship / retry with adjustments
```

If verdict is **retry**:
- Adjust the prompt (more specific palette / aesthetic / composition language)
- Re-generate (overwrite `image.png`, update `prompt.txt` to the new version, append to `review.md`)
- Repeat until ✅. Hard cap: 3 retries; after that, surface to user with screenshots and ask.

### Step 6 — User confirmation before batching

When calibration shot is good, show user:

```
Calibration slide ready: <run-dir>/shot-01/image.png

Review notes:
- [bullet from review.md]
- [bullet from review.md]

This is the visual style for the rest of the carousel. Proceed with slides 2-N in the same style?
[y / n / "tweak X"]
```

Wait for explicit confirmation. If user says "tweak X", incorporate the tweak into a fresh calibration retry, not into the batch.

### Step 7 — Batch generate slides 2..N

After confirmation, generate the rest with the **locked-in style** (same palette/aesthetic language carried verbatim from the approved calibration prompt):

```bash
for i in $(seq 2 $SLIDE_COUNT); do
  ID=$(printf "%02d" $i)
  mkdir -p <run-dir>/shot-$ID
  echo "$IMAGE_PROMPT" > <run-dir>/shot-$ID/prompt.txt
  echo "$SLIDE_COPY" > <run-dir>/shot-$ID/copy.txt

  FULL_PROMPT="$IMAGE_PROMPT, $LOCKED_STYLE_LANGUAGE"
  # Same locked args as step 4...

  RESULT=$(higgs --json generate create soul_cinematic --prompt "$FULL_PROMPT" --aspect_ratio "$ASPECT" --wait)
  JOB_ID=$(echo "$RESULT" | jq -r '.id')
  URL=$(echo "$RESULT" | jq -r '.result_url')

  echo "$JOB_ID" > <run-dir>/shot-$ID/job-id.txt
  echo "$URL" > <run-dir>/shot-$ID/url.txt
  curl -sL "$URL" -o <run-dir>/shot-$ID/image.png
done
```

### Step 8 — Review every batched slide (mandatory)

For each generated slide, Read the PNG and write a `review.md` per the step-5 checklist. **Don't skip this.** If any slide fails:
- Re-generate that slide once with prompt adjustments
- If second attempt also fails, log it in `review.md` and continue (don't block the whole carousel)
- Tell user about the failed slide in the final report

**No stitched scrolling preview image.** Each slide is reviewed individually.

### Step 9 — Caption + hashtags

Per `references/caption-craft.md`:

- **Em dashes are banned.** Refuse to ship copy containing one.
- IG carousel caption length: 50-200 words sweet spot
- LinkedIn: 100-300 words
- Apply brand voice from profile (lexicon, sentence patterns, banned words)
- AI-tells scan — refuse if it fails

Per `references/hashtag-strategy.md`:
- IG → 5-10 hashtags
- LinkedIn → 3-5
- Pull from `brand_profile.md § hashtag_families`

Save to `<run-dir>/caption.md`:

```markdown
# Caption

[the polished caption]

# Hashtags

#tag1 #tag2 #tag3 ...

# Why this caption (agent note)

- [brand-voice element applied]
- [AI-tell avoided]
- [CTA: included with reason / skipped with reason]
```

### Step 10 — Bundle deliverables (NO HTML, NO STITCHED PREVIEW)

```bash
mkdir -p <run-dir>/deliverables
for i in $(seq -f "%02g" 1 $SLIDE_COUNT); do
  cp <run-dir>/shot-$i/image.png <run-dir>/deliverables/slide-$i.png
done
cp <run-dir>/caption.md <run-dir>/deliverables/

cat > <run-dir>/deliverables/README.md <<EOF
# Carousel — $TOPIC

Brand: $BRAND
Run: <run-dir>
Platform: $PLATFORM
Slides: $SLIDE_COUNT
Aspect: $ASPECT
Total cost: $ACTUAL_SPEND credits

## Files
slide-01.png ... slide-$(printf "%02d" $SLIDE_COUNT).png
caption.md

## Posting

1. Upload slides 01..$SLIDE_COUNT to IG/LinkedIn in order
2. Copy caption + hashtags from caption.md
3. Optional text overlays — add in Canva/Figma using slide copy from <run-dir>/shot-XX/copy.txt
EOF
```

**No `index.html`. No combined-preview.png. No "scrollable mockup".** The user posts PNGs to Instagram from their phone — they don't need a web preview.

### Step 11 — Cost ledger + report

Update `<run-dir>/cost-log.json` and append to `runs/cost-summary.json` per `references/output-management.md`.

Tell the user:

```
✓ Carousel ready: <run-dir>/deliverables/

  Slides: <run-dir>/deliverables/slide-01.png ... slide-NN.png
  Caption: <run-dir>/deliverables/caption.md
  Total spend: X credits
  Calibration retries: N
  Failed slides (if any): [list]

Open the images directly (Finder, Preview, your phone). Don't try to open them in a browser.
```

## What this pattern explicitly does NOT do

- ❌ No HTML outputs
- ❌ No stitched scrolling preview image
- ❌ No browser opening to "view" images
- ❌ No Playwright MCP usage
- ❌ No loading the `frontend-design` skill or any other skill outside this bundle
- ❌ No fire-the-whole-batch-and-pray (calibration is mandatory)
- ❌ No silent shipping without review
- ❌ No writes to the repo root

## Outputs

```
runs/<YYYY-MM-DD>-<brand>-carousel-<seq>/
├── shotlist.json
├── pattern.txt                  ← "carousel-post"
├── cost-log.json
├── caption.md
├── shot-01/
│   ├── prompt.txt
│   ├── copy.txt                 ← on-slide text
│   ├── job-id.txt
│   ├── url.txt
│   ├── image.png
│   └── review.md                ← agent's vision-based QA
├── shot-02/
│   └── (same structure)
├── shot-NN/
└── deliverables/
    ├── slide-01.png ... slide-NN.png
    ├── caption.md
    └── README.md
```

## Failure handling

| Symptom | Action |
|---|---|
| Brand profile missing | Tell user to run `/higgsfield-brand-create <name>` first |
| `confidence.spike: low` or `gap` | Refuse — refresh profile first |
| Logo mangled in calibration | Retry with stronger logo-preservation prompt language; if still broken, ask user to provide logo as `--medias` reference image (forces it into the conditioning) |
| Slide off-style after batch | Re-roll just that slide referencing approved calibration prompt explicitly |
| Caption fails AI-tells (em dash, generic, etc.) | Rewrite. 3 attempts. If still failing, surface to user with "the brand voice may be too underspecified — refresh the profile" |
| Soul ID expected but missing | Generate without; flag face-consistency risk in final report |
| User asks for >10 slides | Push back — IG caps at 10, longer carousels lose viewers. Suggest series. |

## Sources

- `docs/ask-rag/ask-ads-marketing-9q.md` Q3 (carousel structure), Q4 (hooks), Q5 (captions), Q6 (hashtags)
- `references/agent-tooling-rules.md` (image review via Read tool, no other tooling)
- `references/hook-craft.md`, `references/caption-craft.md`, `references/hashtag-strategy.md`
- `references/cost-discipline.md`, `references/output-management.md`
- Empirical feedback from first run (2026-05-06) — calibration-first + per-slide review came from real failures
