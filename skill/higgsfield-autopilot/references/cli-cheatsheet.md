# Higgsfield CLI Cheatsheet

Single source of truth for which `higgs` command does what. The agent loads this when running any pattern.

> **Heads up — open issues + operational caveats.** Full details in `references/known-issues.md`. Quick summary:
> - **soul_cast** (issue #4): ignores `--prompt` object. Use `cinematic_studio_3_0` or `kling3_0` for video instead.
> - **Windows install** (issue #3): `tar --force-local` missing. Windows users need WSL/Git Bash.
> - **Subscription pricing** (issue #1): CLI is plan-blind. `generate cost` is rack rate; actual cost only knowable via `account status` delta. See `references/cost-discipline.md`.
> - **Canvas workflows** (issue #2): not accessible via CLI/MCP/REST. Compose pipelines as bash sequences of single-model calls.
> - **Webhooks**: NOT supported. Use `--wait` (blocks) or `generate wait <id>` (poll).
> - **CLI cadence**: 11+ versions in 5 days (0.1.18 through 0.1.28 between 2026-05-02 and 2026-05-04). Pin to a known-good version OR run `higgs version` at session start to detect breaking changes.
> - **REST API**: 1:1 mirror of CLI. No separate billing model. Same primitives.

## Auth + identity

| Command | Use when |
|---|---|
| `higgs auth login` | First run on a machine; user signs in via browser device-code |
| `higgs auth logout` | Rotating tokens or switching accounts |
| `higgs auth token` | **NEVER print this in chat or logs.** It's a credential. Used only when calling the REST API directly. |
| `higgs account status` | Before any spend — read balance + plan |
| `higgs account transactions --size 50` | Reconciling actual vs. predicted spend |
| `higgs workspace list` | Check what billing contexts exist |
| `higgs workspace status` | Confirm active workspace before spending |
| `higgs workspace set <id>` | Switch to a client's workspace |
| `higgs workspace unset` | Return to personal/private context |

## Discovery

| Command | Use when |
|---|---|
| `higgs model list` | Browse all 35 models |
| `higgs model list --image` / `--video` | Filter by media type |
| `higgs --json model get <name>` | Get the model's full param schema (machine-readable) |
| `higgs model get <name>` | Same, human-readable table |

## Cost preflight (free, always run before spending)

| Command | Use when |
|---|---|
| `higgs generate cost <model> --prompt "..."` | Per-shot preflight |
| `higgs generate cost <model> --prompt "..." --image <upload-id>` | Image-to-image / image-to-video preflight |
| `higgs product-photoshoot create --enhance-only ...` | **Free** — returns the AI-enhanced prompt without generating. Best preview. |

## Upload

| Command | Use when |
|---|---|
| `higgs upload create ./photo.png` | One-time upload of a reference image; returns upload_id |
| `higgs upload list --image --size 50` | Find a previous upload's id |
| `higgs upload list --video` | Same for video |

Media flags (`--image`, `--start-image`, `--end-image`, `--video`, `--audio`) accept either an upload UUID, a previous job UUID, OR a local file path (auto-uploaded). Prefer reusing upload IDs across a run to save round-trips.

> **The flags are NOT universal across models.** Each video model accepts a different subset. Always run `higgs --json model get <name>` first to see what flags that specific model takes. Examples (verified 2026-05-07):
>
> | Model | Image input flag | Notes |
> |---|---|---|
> | `kling2_6` | `--image` only | Rejects `--start-image` with "Model accepts only --image" |
> | `minimax_hailuo` | `--image` (1+ — array under the hood) | Multi-image input supported |
> | `seedance1_5`, `seedance_2_0` | `--image` or `--start-image` or `--end-image` | More flexible — accepts multiple roles via `medias` array |
> | `kling3_0` | `--start-image` (verify with `model get`) | Newer Kling — more flexible than 2.6 |
> | `cinematic_studio_3_0` | `--medias` array (multiple ref images) | Heaviest creative coverage |
>
> **Don't assume.** Cost-discipline says preflight before spending; this rule says **schema-check before crafting the command**. Model schemas drift; the CLI is the source of truth.

## Generation

| Command | Use when |
|---|---|
| `higgs generate create <model> --prompt "..." --wait` | Submit + block until done; prints the result URL on stdout |
| `higgs generate create <model> --prompt "..."` (no `--wait`) | Submit + return job_id immediately; useful for parallel/batched submission |
| `higgs generate create <model> --prompt "..." --wait --wait-timeout 20m --wait-interval 5s` | Tune polling for slow models (video) |
| `higgs --json generate create <model> --prompt "..." --wait` | Same, but returns JSON — easier to parse for output URLs and metadata |
| `higgs generate get <job_id>` | Inspect one job |
| `higgs generate wait <job_id>` | Poll an already-submitted job |
| `higgs generate list --size 20` | Recent job history (across this account/workspace) |

## Pre-built workflow commands (Higgsfield writes the prompt for you)

| Command | Use when |
|---|---|
| `higgs product-photoshoot create --mode product_shot --prompt "intent" --image bottle.jpg --count 3` | Brand product hero/lifestyle shots, multi-variant |
| `higgs product-photoshoot create --mode lifestyle_scene ...` | Same but with environmental context |
| `higgs product-photoshoot create --enhance-only ...` | Get the enhanced prompt without spending — preview workflow |
| `higgs marketplace-cards create --scope product-images --prompt "..." --image can.png` | Amazon/Etsy/eBay-style listing imagery |

Useful flags: `--brand_context "..."`, `--product_context "..."`, `--count 1-10`.

## Soul ID (custom character refs)

| Command | Use when |
|---|---|
| `higgs soul-id create --name Alice --soul-2 --image x5` | Train a face-faithful character ref from 5+ photos |
| `higgs soul-id list` | Available trained refs |
| `higgs soul-id get <id>` | Inspect one |
| `higgs soul-id wait <id>` | Block until training completes |

Use the resulting soul_id with image models that accept `--soul-id`: `text2image_soul_v2`, `soul_cinematic`, etc.

## Marketing Studio (asset registry)

| Command | Use when |
|---|---|
| `higgs marketing-studio avatars list` | See trained + preset avatars (you have 9 presets free) |
| `higgs marketing-studio products list` | Your registered brand products |
| `higgs marketing-studio products create --title "X" --image <upload-id>` | Register a product for re-use across campaigns |
| `higgs marketing-studio products fetch --url <product-url> --wait` | Scrape a product page into your registry |
| `higgs marketing-studio webproducts list/create/fetch` | Same primitives for web products |

## Global flags (work on every command)

| Flag | Effect |
|---|---|
| `--json` | Machine-readable output. **Always use this when piping into bash/jq.** |
| `--no-color` | Strip ANSI when capturing to files |
| `-h` / `--help` | Per-command help |

## Idiomatic patterns

### Preflight + spend + log (the sacred ritual)

```bash
# 1. Preflight cost
COST=$(higgs --json generate cost soul_cinematic --prompt "$PROMPT" | jq -r '.cost')
echo "About to spend $COST credits"

# 2. Confirm balance covers it
BAL=$(higgs --json account status | jq -r '.credits')
[ "$BAL" -lt "$COST" ] && { echo "Insufficient balance ($BAL < $COST)"; exit 1; }

# 3. Spend
URL=$(higgs --json generate create soul_cinematic --prompt "$PROMPT" --aspect_ratio 9:16 --wait | jq -r '.result_url')

# 4. Download
curl -sL "$URL" -o "runs/$RUN/shot-01/take-1.png"
```

### Image-to-video chain

```bash
# 1. Generate still
STILL_JOB=$(higgs --json generate create soul_cinematic --prompt "$STILL_PROMPT" --aspect_ratio 9:16 --wait | jq -r '.id')

# 2. Use the still as input to the video model — pass the job_id, not the URL
VIDEO_URL=$(higgs --json generate create cinematic_studio_3_0 --image "$STILL_JOB" --prompt "$MOTION_PROMPT" --aspect_ratio 9:16 --duration 5 --wait | jq -r '.result_url')
```

Job IDs are valid as `--image` inputs to other models — Higgsfield resolves them server-side. No re-upload needed.

### Parallel batch (no `--wait`)

```bash
# Fire 5 image jobs without blocking
JOB_IDS=()
for prompt in "${PROMPTS[@]}"; do
  ID=$(higgs --json generate create soul_cinematic --prompt "$prompt" --aspect_ratio 9:16 | jq -r '.id')
  JOB_IDS+=("$ID")
done

# Then poll all of them
for id in "${JOB_IDS[@]}"; do
  higgs generate wait "$id"
done
```

## Anti-patterns

- **Don't** call `generate create` without a preceding `generate cost`. You'll spend without knowing.
- **Don't** skip `--json` if you're piping output into anything. The human-readable table format breaks parsers.
- **Don't** hard-code model names in patterns — let `model-selection-guide.md` route based on goal + budget.
- **Don't** use `soul_cast` until upstream issue #4 is fixed.
- **Don't** print `higgs auth token` output anywhere. Treat it like a password.
- **Don't** assume the active workspace is correct. Always `workspace status` first if billing matters.
