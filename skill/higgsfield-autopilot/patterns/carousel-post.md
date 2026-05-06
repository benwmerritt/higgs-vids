# Pattern: Carousel Post

Take a topic + brand profile + (optional) source assets → produce a 5-10 slide IG/LinkedIn carousel that's post-ready. Each slide visually consistent, copy hooks brand-specific, caption + hashtags drafted.

## When to use

- Brief asks for an Instagram or LinkedIn carousel
- Output target: 5-10 connected slides (1080×1350 IG-native, or 1:1 if specified)
- Topic is educational / list / story / opinion-drop format
- Brand profile exists at `brands/<name>/profile.md` (use `/higgsfield-brand-create` first if not)

If the user wants a single-image post, use `quick-social.md`. If they want a video reel, use `product-reel.md`.

## Inputs

- **Brand** (required) — name of an existing brand profile (`brands/<name>/profile.md`)
- **Topic** (required) — one sentence describing the carousel concept
- **Optional source asset(s)** — local file path(s) to anchor the carousel (a product photo, a hero image, etc.)
- **Slide count** (optional) — defaults to 6; range 5-10
- **Aspect** (optional) — defaults to 4:5 (IG carousel native portrait); 1:1 for square
- **Platform** (optional) — defaults to instagram; influences caption and hashtag style

## Cost envelope (rack-rate; subscriber absorption typically ~99% on paid tiers)

| Slide count | Stills (soul_cinematic) | Rack-rate total | Likely actual on Starter+ |
|---|---|---|---|
| 5 | 5 × 12 | ~60 credits | **~0.6 credits** |
| 6 (default) | 6 × 12 | ~72 credits | **~0.7 credits** |
| 8 | 8 × 12 | ~96 credits | **~1 credit** |
| 10 | 10 × 12 | ~120 credits | **~1.2 credits** |

**Caption + hashtags = free** (text generation, no Higgsfield API calls).

## The recipe

### Step 0 — Pre-flight

Per `references/cost-discipline.md`:
- `higgs --json account status` — confirm auth + balance
- `higgs --json workspace status` — confirm correct billing context

Per the foundational rules: read the brand profile first; do not generate without one.

```bash
BRAND="$1"
TOPIC="$2"
PROFILE_PATH="brands/$BRAND/profile.md"

if [ ! -f "$PROFILE_PATH" ]; then
  echo "No brand profile at $PROFILE_PATH. Run /higgsfield-brand-create first."
  exit 1
fi
```

### Step 1 — Load brand context

Read **all of these in full** (they're the agent's working memory for this run):

1. `brands/<name>/profile.md` — voice, visual DNA, audience, spike, constraints, hashtag families
2. `brands/<name>/source-fetches/*.md` — recent voice samples (most-recent files only)
3. `references/interview-craft.md` § AI-tells — what to actively avoid
4. `references/hook-craft.md` — slide 1 hook options
5. `references/caption-craft.md` — caption shape + AI-tells in copy
6. `references/hashtag-strategy.md` — pick from brand's hashtag families

If `brand_type` is set, read the brand-type-specific notes in `references/calendar-defaults.md` (carousel topic mix and frequency vary by brand type).

### Step 2 — Plan the carousel

Per Ask Ads Marketing MCP advice (Q3), structure:

| Slide | Job |
|---|---|
| **Slide 1 — Hook** | Stop the scroll. Bold statement / question / contrarian take / specific number. Per `references/hook-craft.md`. |
| **Slides 2-N (middle)** | Beat-by-beat narrative arc — problem / elaboration / story / educational beats / examples. Build value. |
| **Slide before last (often N-1)** | Social proof / testimonial / reinforcing example (if applicable) |
| **Final slide — CTA** | Action-oriented, urgent if relevant, visually distinct. Or: deliberately no CTA if brand prefers (per profile). |

For 6 slides default: 1 hook + 4 middle + 1 CTA. For 8 slides: 1 hook + 6 middle + 1 CTA. The middle slides should each carry a single beat — don't cram multiple ideas per slide.

**Output of this step:** a `shotlist.json` with one entry per slide:

```json
{
  "carousel_topic": "...",
  "brand": "...",
  "slide_count": 6,
  "aspect": "4:5",
  "platform": "instagram",
  "slides": [
    {
      "id": 1,
      "purpose": "hook",
      "copy_draft": "...",
      "image_prompt": "..."
    },
    {
      "id": 2,
      "purpose": "problem_setup",
      "copy_draft": "...",
      "image_prompt": "..."
    },
    ...
  ]
}
```

Save to `runs/<RUN_ID>/shotlist.json`.

### Step 3 — Draft 2-3 hook options for slide 1

Per `references/hook-craft.md`, generate **3 hook variants** for slide 1 in different patterns (conversational / specific-number / contrarian / etc.) and ask the user to pick:

```
Hook options for slide 1:

A) [conversational]
B) [specific-time / number]
C) [contrarian]

I'd pick [X] because [reason — refer to brand profile].
```

Wait for user pick. Update `shotlist.json` slide 1 with the chosen hook.

### Step 4 — Cost preflight

```bash
TOTAL_RACK=0
for slide in shotlist.slides:
  RACK=$(higgs --json generate cost soul_cinematic --prompt "<slide.image_prompt>" --aspect_ratio "$ASPECT" | jq -r '.cost')
  TOTAL_RACK=$((TOTAL_RACK + RACK))

echo "Rack-rate estimate: $TOTAL_RACK credits"
echo "On a paid plan with image absorption, actual is likely ~1% of this."
```

Apply `references/cost-discipline.md` thresholds. For typical 6-slide carousel (~72 credits rack), this is a silent-proceed on any tier with reasonable balance.

### Step 5 — Generate slide images

For each slide, per `references/cost-discipline.md` capability-check ritual:

```bash
mkdir -p runs/$RUN_ID/slide-$ID
echo "$IMAGE_PROMPT" > runs/$RUN_ID/slide-$ID/prompt.txt

# Build image prompt with brand visual DNA woven in
FULL_PROMPT="$IMAGE_PROMPT, $BRAND_PALETTE, $BRAND_PHOTO_AESTHETIC"

ARGS=(soul_cinematic --prompt "$FULL_PROMPT" --aspect_ratio "$ASPECT" --wait --wait-timeout 5m)

# If brand has a Soul ID and the slide features a person → use --soul-id
[ -n "$SOUL_ID" ] && [ "$SLIDE_HAS_PERSON" = "yes" ] && ARGS+=(--soul-id "$SOUL_ID")

# If user provided source assets and this slide should reference them → --medias
[ -n "$REF_UPLOAD_ID" ] && ARGS+=(--medias "$REF_UPLOAD_ID")

RESULT=$(higgs --json generate create "${ARGS[@]}")
JOB_ID=$(echo "$RESULT" | jq -r '.id')
URL=$(echo "$RESULT" | jq -r '.result_url')

echo "$JOB_ID" > runs/$RUN_ID/slide-$ID/job-id.txt
echo "$URL" > runs/$RUN_ID/slide-$ID/url.txt
curl -sL "$URL" -o runs/$RUN_ID/slide-$ID/image.png
```

Generate sequentially (5-10 stills, no need for parallel — each takes ~30s).

### Step 6 — Visual cohesion check

After all slides generated:
- Look at all slide images side-by-side (vision capability if available, otherwise note in report)
- Check: do they share a visual language (palette, lighting, composition feel)?
- If one slide is wildly off-style → re-roll just that slide with a tighter prompt that references the others

The MCP advice (Q3) explicitly flagged "Lack of cohesion" as a common reason carousels flop. This step is non-negotiable.

### Step 7 — Slide copy overlays (optional, defer to user)

Patterns with on-image text need either:
- The agent generates the copy as text-overlay ready (font, size, position guidance per slide) — user adds in Canva / Figma / etc.
- OR the agent uses `gpt_image_2 --quality high` for slides that need text rendered (better text rendering than soul_cinematic)

Default: agent generates the copy text per slide and saves to `runs/$RUN_ID/slide-$ID/copy.txt` for the user to overlay manually. Tell the user: "I generated the slide visuals + the copy text. To add text overlays, drop into Canva or similar."

If user explicitly wants text rendered onto the image: regenerate that slide via `gpt_image_2 --quality high` with text overlay instructions in the prompt.

### Step 8 — Caption + hashtags

Per `references/caption-craft.md`:
- Pick caption structure based on carousel format (story → hook→beat→payoff; list → list format; opinion → reply-bait or single-sentence)
- Apply brand voice from profile (lexicon, sentence patterns, banned words)
- Run AI-tells scan — refuse to ship copy that uses any
- Length per platform — IG 50-200 words for engagement, longer for storytelling

Per `references/hashtag-strategy.md`:
- Platform = IG → 5-10 hashtags (1-2 broad + 5+ niche + 1 branded)
- Platform = LinkedIn → 3-5 hashtags (industry-specific, professional)
- Pull from `brand_profile.md § hashtag_families`

Save to `runs/$RUN_ID/caption.md`:

```markdown
# Caption

[the polished caption — ready to paste]

# Hashtags (8 total)

#bensmadethis · #brandidentitydesign · #aussiedesign · #typographylove · #studiomelbourne · #design · #branding · #smallbusiness

# Why this caption (agent note for user)

- Used [specific brand-voice element] from profile
- Avoided AI-tells: [list]
- CTA: [included / skipped, with reason]
```

### Step 9 — Bundle deliverables

```bash
mkdir -p runs/$RUN_ID/deliverables
for i in $(seq -f "%02g" 1 $SLIDE_COUNT); do
  cp runs/$RUN_ID/slide-$i/image.png runs/$RUN_ID/deliverables/slide-$i.png
done
cp runs/$RUN_ID/caption.md runs/$RUN_ID/deliverables/

cat > runs/$RUN_ID/deliverables/README.md <<EOF
# Carousel — $TOPIC

Brand: $BRAND
Platform: $PLATFORM
Slides: $SLIDE_COUNT
Aspect: $ASPECT
Total cost: $ACTUAL_SPEND credits

## Files
$(ls runs/$RUN_ID/deliverables/slide-*.png | xargs -I {} basename {})

## Posting

1. Upload slides 01..$SLIDE_COUNT to IG/LinkedIn in order
2. Copy caption + hashtags from caption.md
3. Optional text overlays — add in Canva/Figma using slide copy from runs/$RUN_ID/slide-XX/copy.txt
4. Schedule via your tool of choice
EOF
```

### Step 10 — Cost ledger + report

Update `runs/$RUN_ID/cost-log.json` and `runs/cost-summary.json` per `references/output-management.md`.

Tell the user:
- Path to `runs/$RUN_ID/deliverables/`
- Total spend (delta from `account status`)
- Caption draft included; review before posting
- Any visual cohesion issues flagged in step 6

### Step 11 — Update preset (if user asked for one)

If this run was via `/higgsfield-make --preset <name>`, append to the preset's "Past runs" table per `references/preset-format.md`. Surface any refinement notes the agent learned (slide that worked best, caption style that landed).

## Outputs

```
runs/<RUN_ID>/
├── brief.md                       ← copy of input topic
├── shotlist.json                  ← carousel plan (slide-by-slide)
├── pattern.txt                    ← "carousel-post"
├── cost-log.json
├── caption.md                     ← caption + hashtags + agent note
├── slide-01/
│   ├── prompt.txt
│   ├── job-id.txt
│   ├── url.txt
│   ├── copy.txt                   ← on-slide text (if pattern uses overlays)
│   └── image.png
├── slide-02..NN/                  ← same structure
└── deliverables/
    ├── slide-01.png ... slide-NN.png
    ├── caption.md
    └── README.md
```

## Common variations

- **Educational list carousel** — list format, 1 hook + 5-7 list-item slides + 1 CTA. Caption matches (list format with line breaks).
- **Story carousel** — hook + 4-6 narrative beats + 1 lesson/payoff. Caption is hook→beat→payoff prose.
- **Opinion drop** — hook (contrarian take) + 3-4 supporting argument slides + 1 reply-bait slide. Caption is short with reply-bait question.
- **Product showcase** — hook + product hero + 3-4 feature/benefit slides + 1 social-proof + 1 CTA. Use `--medias` with the product photo.
- **Behind-the-scenes** — hook + 5-6 candid moments + 1 invitation. Tone shifts to casual. Caption short.

## Failure handling

| Symptom | Action |
|---|---|
| Brand profile missing | Tell user to run `/higgsfield-brand-create <name>` first |
| Brand profile has `confidence.spike: low` or `gap` | Refuse to generate — tell user to refresh the profile (the carousel will be generic without a real spike) |
| Visual cohesion check fails (one slide off-style) | Re-roll that slide referencing the others as visual context |
| Caption fails AI-tells scan | Rewrite. If 3 attempts still fail, tell the user — the brand voice may be too underspecified |
| Soul ID expected but not trained | Generate without it; warn user that face consistency across human-featuring slides will be weak |
| User asks for >10 slides | Push back — IG caps at 10, longer carousels lose viewers. Suggest splitting into a series. |

## Why carousels matter (per MCP Q3)

> "By focusing on a strong hook, a well-structured narrative, optimal slide count, effective copy patterns, and cohesive visual design, you can create Instagram carousels that not only stop the scroll but also drive conversions through saves, shares, and follows."

The agent's job is to produce all 5 of those (hook + structure + slide count + copy + visual cohesion) on every run. Skipping any of them is a flop.

## Sources

- `docs/ask-rag/ask-ads-marketing-9q.md` Q3 (carousel structure), Q4 (hooks), Q5 (captions), Q6 (hashtags)
- `references/hook-craft.md`, `references/caption-craft.md`, `references/hashtag-strategy.md`
- `references/cost-discipline.md`, `references/output-management.md`
