# Pattern: Moodboard

Take a brand + a concept (e.g. "yacht shoot for X client") → produce a curated visual moodboard the user can present to a client. Calibration-first, brand-styled, includes creative-direction copy in the brand's voice. Photo-only (cheap on any plan).

> **Read `references/agent-tooling-rules.md` BEFORE running.** Image review uses the Read tool. No Playwright MCP, no browser, no HTML output, no stitched previews.

## When to use

- User wants to **pitch a creative concept** to a client (production shoot, campaign direction, brand refresh)
- Output target: a folder of reference images + a creative-direction document, suitable for slide-deck presentation
- Photo-only — no video generation
- Brand profile exists at `brands/<name>/profile.md`

If the user wants finished IG content, use `carousel-post.md` or `quick-social.md`. A moodboard is for **pre-production / pitch** work.

## Inputs

- **Brand** (required) — name of an existing brand profile (`brands/<name>/profile.md`)
- **Concept** (required) — what the shoot/campaign is about (e.g. "yacht shoot for luxury watch brand", "rebrand moodboard for fragrance launch")
- **Client name** (optional) — appears in the creative-direction document for presentation
- **Image count** (optional) — defaults to 9; range 6-12
- **Treatment angles** (optional) — by default the agent covers a balanced mix (3 wide hero / 3 mid lifestyle / 3 close-up detail). User can override.

## Cost envelope (rack-rate; ~99% absorbed on paid plans)

| Image count | Stills (`soul_cinematic`) | Rack-rate total | Likely actual on Starter+ |
|---|---|---|---|
| 6 | 6 × 12 | ~72 credits | ~0.7 credits |
| 9 (default) | 9 × 12 | ~108 credits | ~1.1 credits |
| 12 | 12 × 12 | ~144 credits | ~1.4 credits |

**Creative-direction copy = free** (text). Calibration adds ~0.12 credits actual for the trial image.

## Run directory naming

```
runs/<YYYY-MM-DD>-<brand>-moodboard-<seq>/
```

Examples: `runs/2026-05-06-ben-moodboard-1/`, `runs/2026-05-07-acme-moodboard-3/`

## The recipe

### Step 0 — Pre-flight + tooling guardrails

```bash
higgs --json account status   # auth + balance
higgs --json workspace status # billing context
```

**Hard rules** (per `references/agent-tooling-rules.md`):
- ❌ No browser opening, no Playwright MCP, no other skills loaded mid-pattern
- ❌ No HTML output, no stitched scrollable preview image
- ❌ Never write to repo root — everything in `<run-dir>/`

### Step 1 — Load brand context

Read in full:
1. `brands/<name>/profile.md`
2. `brands/<name>/source-fetches/*.md` (recent only)
3. `references/interview-craft.md` § AI-tells (the rules apply to copy)
4. `references/caption-craft.md` § Hard bans (em dashes, etc.)
5. `references/agent-tooling-rules.md`

If `confidence.spike` is `low` or `gap`, refuse — refresh brand profile first. A moodboard without a clear brand spike is generic.

### Step 2 — Plan the moodboard structure

Based on the concept, decompose into **angles**. Default 9-image structure:

| Slot | Treatment | Purpose |
|---|---|---|
| 1 | **Hero wide** — establishing | Sets the world |
| 2 | **Hero wide** — alt angle / time of day | Shows range |
| 3 | **Mid lifestyle** — subject in scene | Human element |
| 4 | **Mid product / object detail** | Hero subject up close |
| 5 | **Mid atmospheric** — light study | Mood / feel |
| 6 | **Close-up texture / material** | Tactile beat |
| 7 | **Close-up subject moment** — face / hands / gesture | Intimacy |
| 8 | **Wide architectural / environmental** | Context layer |
| 9 | **Hero wide — alternative palette / time** | Range / flexibility for client |

Adjust slots based on the concept. For **yacht shoot** specifically:
- Hero wide: yacht in open water + golden hour
- Mid lifestyle: people on deck (Soul ID if applicable + ≥1 person photos available)
- Mid detail: helm / varnished wood / brass / ropes
- Atmospheric: light on water, sail textures, sunset reflections
- Close-up: a glass, a watch face, a hand on the wheel (subtle product context if there's a product brief)

Save plan to `<run-dir>/structure.json`.

### Step 3 — Write the creative-direction copy FIRST (in brand voice)

Before generating any images, draft a 50-100 word creative-direction statement in the brand's voice. This is the spine of the moodboard. Save to `<run-dir>/direction-draft.md`:

```markdown
# Creative Direction — <concept>

For: <client name or [placeholder]>
Brand: <brand name>
Date: <YYYY-MM-DD>

## The vision

[50-100 words in brand voice — what this shoot feels like, what it's about,
what the audience walks away with. Apply hard bans: no em dashes, no generic
openers, no AI tells. Reference brand profile § Voice.]

## Treatment angles

- **Hero wides** — [1 sentence on what these establish]
- **Lifestyle** — [1 sentence]
- **Detail** — [1 sentence]
- **Atmospheric** — [1 sentence]
```

Show the user the direction copy. Wait for OK or tweaks. Don't generate images until the direction lands. **The direction shapes the image prompts** — getting it right first saves credits.

### Step 4 — Calibration shot (1 image, locked palette)

Pick the highest-stakes image (usually hero wide #1) and generate it first:

```bash
mkdir -p <run-dir>/shot-01
echo "$IMAGE_PROMPT" > <run-dir>/shot-01/prompt.txt
echo "$SLOT_DESCRIPTION" > <run-dir>/shot-01/treatment.txt

FULL_PROMPT="$IMAGE_PROMPT, $BRAND_PALETTE, $BRAND_PHOTO_AESTHETIC"
ARGS=(soul_cinematic --prompt "$FULL_PROMPT" --aspect_ratio 16:9 --wait --wait-timeout 5m)
[ -n "$REF_UPLOAD_ID" ] && ARGS+=(--medias "$REF_UPLOAD_ID")
[ -n "$SOUL_ID" ] && [ "$SLOT_HAS_PERSON" = "yes" ] && ARGS+=(--soul-id "$SOUL_ID")

RESULT=$(higgs --json generate create "${ARGS[@]}")
JOB_ID=$(echo "$RESULT" | jq -r '.id')
URL=$(echo "$RESULT" | jq -r '.result_url')
echo "$JOB_ID" > <run-dir>/shot-01/job-id.txt
echo "$URL" > <run-dir>/shot-01/url.txt
curl -sL "$URL" -o <run-dir>/shot-01/image.png
```

**Aspect ratio default for moodboards: 16:9** (wide hero) — overrides per slot if needed (vertical for some details, square for tight crops).

### Step 5 — Review the calibration (mandatory, Read tool)

Read `<run-dir>/shot-01/image.png` with the Read tool. Inspect:

- ✅ Does the palette match the brand profile?
- ✅ Does the photo aesthetic match (intimate / dramatic / clean / textured)?
- ✅ Does the concept land — does this look like the moodboard subject?
- ✅ Composition leaves room for context if the client will overlay copy?
- ✅ AI tells: weird hands, garbled text, distorted geometry?
- ✅ Does this look like a moodboard reference, or AI slop?

Save `<run-dir>/shot-01/review.md`. If retry needed, adjust prompt, regenerate, log. Cap: 3 retries.

### Step 6 — User confirmation

Show the user:

```
Calibration image: <run-dir>/shot-01/image.png

Open with: open <run-dir>/shot-01/image.png

Direction held: [1-line summary of what worked]
Palette read: [observed colours from the image]

This is the visual direction for the rest of the moodboard. Proceed with the other 8 images in matching style?
```

Wait for explicit OK. If "tweak X", incorporate into a fresh calibration and re-confirm — don't batch with unconfirmed direction.

### Step 7 — Batch generate slots 2-N

Same locked-in style language across all remaining slots. Vary the slot's treatment / subject focus, keep palette + aesthetic identical:

```bash
for i in $(seq 2 $IMAGE_COUNT); do
  ID=$(printf "%02d" $i)
  mkdir -p <run-dir>/shot-$ID
  echo "$IMAGE_PROMPT" > <run-dir>/shot-$ID/prompt.txt
  echo "$SLOT_DESCRIPTION" > <run-dir>/shot-$ID/treatment.txt

  FULL_PROMPT="$IMAGE_PROMPT, $LOCKED_STYLE_LANGUAGE"
  # Aspect varies per slot: hero wides 16:9, vertical detail 4:5, square close-ups 1:1
  ASPECT=$(get_slot_aspect $i)

  RESULT=$(higgs --json generate create soul_cinematic --prompt "$FULL_PROMPT" --aspect_ratio "$ASPECT" --wait)
  # Save job-id, url, download to image.png
done
```

### Step 8 — Review every batched image (mandatory)

Read each PNG, write `review.md`. Failures: re-roll once with a tighter prompt. If second attempt fails, log and continue — don't block the moodboard for one bad slot.

### Step 9 — Extract the actual palette (post-hoc)

After all images generated, the agent samples the dominant colours across the set and writes them to `<run-dir>/palette.md`:

```markdown
# Palette — <concept>

Derived from the moodboard images:

- #C2A878 — warm sand
- #2D3540 — deep navy
- #F5F1E8 — bone white
- #8E6F4A — varnished wood
- #4A5C6E — overcast water

(These are observations from the generated set, not strict brand colours — use as a reference for the client conversation.)
```

Use vision via Read tool to estimate dominants from each image; aggregate the most common across the set.

### Step 10 — Assemble the presentation bundle

```bash
mkdir -p <run-dir>/deliverables
for i in $(seq -f "%02g" 1 $IMAGE_COUNT); do
  cp <run-dir>/shot-$i/image.png <run-dir>/deliverables/image-$i.png
done
cp <run-dir>/direction-draft.md <run-dir>/deliverables/creative-direction.md
cp <run-dir>/palette.md <run-dir>/deliverables/

cat > <run-dir>/deliverables/README.md <<EOF
# Moodboard — <concept>

For: <client name>
Brand: <brand>
Date: <YYYY-MM-DD>
Generated: <image count> images, $ASPECT_MIX aspects
Total cost: <actual credits>

## Files

- creative-direction.md — the vision + treatment angles (read this first)
- palette.md — colour reference observed from the set
- image-01.png ... image-NN.png — the moodboard images, ordered hero → mid → detail

## Presenting to a client

Recommended layout (for Keynote / Figma / PDF):

1. Cover: brand mark + concept name + date
2. Vision: the creative-direction copy
3. Hero spread: image-01 + image-02 (the wides, side by side)
4. Treatment grid: lifestyle (image-03) + detail (image-04, image-05) + atmospheric (image-06)
5. Close-up beats: image-07, image-08
6. Range / alternative: image-09 (the alt-palette/time hero)
7. Palette summary: from palette.md

Don't include this README in the client-facing deck — it's for your reference.
EOF
```

**No HTML, no auto-generated slide deck, no combined preview image.** Hand the user the assets; they assemble the deck in their own tool (Keynote, Figma, Canva, etc.).

### Step 11 — Cost ledger + report

Update `<run-dir>/cost-log.json` and `runs/cost-summary.json` per `references/output-management.md`.

Tell the user:

```
✓ Moodboard ready: <run-dir>/deliverables/

  Images: image-01.png ... image-NN.png
  Direction: creative-direction.md
  Palette: palette.md
  Total spend: X credits
  Calibration retries: N
  Failed slots: [list, if any]

Open the run dir to assemble your client deck:
  open <run-dir>/deliverables/

Suggested layout in deliverables/README.md.
```

## What this pattern explicitly does NOT do

- ❌ No HTML / web mockup / scrollable layout
- ❌ No auto-generated slide deck (Keynote/PDF) — the user owns the deck assembly
- ❌ No stitched preview image
- ❌ No browser opening (Read tool only)
- ❌ No video generation (image-only — keep it cheap)
- ❌ No fire-the-batch-and-pray (calibration mandatory)

## Outputs

```
runs/<YYYY-MM-DD>-<brand>-moodboard-<seq>/
├── structure.json                  ← slot plan
├── direction-draft.md              ← creative-direction copy (in brand voice)
├── pattern.txt                     ← "moodboard"
├── cost-log.json
├── palette.md                      ← observed dominant colours
├── shot-01/
│   ├── prompt.txt
│   ├── treatment.txt               ← what slot this is (hero wide / mid lifestyle / etc.)
│   ├── job-id.txt
│   ├── url.txt
│   ├── image.png
│   └── review.md
├── shot-02/ ... shot-NN/
└── deliverables/
    ├── image-01.png ... image-NN.png
    ├── creative-direction.md
    ├── palette.md
    └── README.md (presentation layout suggestion)
```

## Common variations

- **Yacht shoot** — hero wides 16:9, lifestyle 4:5, details 1:1. Default 9 images.
- **Fragrance launch moodboard** — heavy on close-up texture + atmospheric light, fewer wide establishing shots
- **Food / restaurant moodboard** — overhead flat-lays, hands on table, ambient room shots
- **Architecture / interiors** — wide → mid → detail of materials/textures/light
- **Portrait series direction** — fewer scenes, more variations on the subject (Soul ID essential)
- **Low budget pitch** — 6 images instead of 9; ~0.7 credits actual on Starter

## Failure handling

| Symptom | Action |
|---|---|
| Brand profile missing or `confidence.spike: low` | Stop. Run `/higgsfield-brand-create` first. |
| Calibration retried 3x and still off | Surface to user with screenshots; ask for direction tweak. Don't burn through more retries blindly. |
| One slot generates poorly | Re-roll once. If second fails, log and continue with N-1 images. |
| Direction copy fails AI-tells scan | Rewrite. 3 attempts. If still failing, the brand voice may be underspecified — surface to user. |
| Soul ID expected but not trained | Generate without; use brand profile's described talent style. Note in deliverables/README. |

## Sources

- `references/agent-tooling-rules.md` — image review via Read tool, no other tooling
- `references/caption-craft.md` — direction copy quality
- `references/cost-discipline.md` — preflight + ledger
- `references/output-management.md` — run dir naming, no HTML, no root writes
- `references/brand-profile-format.md` — voice + visual DNA + Soul ID lookup

Designed in response to a 2026-05-06 client moodboard request — yacht shoot pitch material; calibration-first + brand-voice direction copy + presentation-ready bundle as the differentiators from generic AI image batches.
