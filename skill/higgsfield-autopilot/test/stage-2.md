# Stage 2 — Single Shot Real Generation

> **Invoke:** `/higgsfield-test 2` or *"Read `skill/higgsfield-autopilot/test/stage-2.md` and execute it."*

**Cost: ~12 credits** (one Soul Cinematic still, 9:16). NO video step in stage 2 — that's stage 3. Verifies you can submit, wait, download, and log cost to JSON for one image.

**Pre-condition:** stage 1 has passed in the same session and you have ≥12 credits.

## Pre-conditions

```bash
BAL=$(higgs --json account status | jq -r '.credits')
[ "$BAL" -lt 12 ] && { echo "Need ≥12 credits, have $BAL. Top up first."; exit 1; }
```

If this fails, stop. Don't partially execute.

## Steps

### 1. Read instructions (skim if recently read)

SKILL.md + cli-cheatsheet + cost-discipline.

### 2. Acquire a shotlist

Reuse the most recent `runs/*/shotlist.json` (sort by mtime). If none exists, generate one for `briefs/example-retro-futuristic.md` per `brief-expansion-rules.md`. Save under `runs/<NEW_RUN_ID>/shotlist.json`.

### 3. Pick shot 1

Pull `shots[0].still_prompt` from the shotlist. That's the prompt for this stage.

### 4. Cost preflight + explicit confirmation

```bash
COST=$(higgs --json generate cost soul_cinematic --prompt "$STILL_PROMPT" | jq -r '.cost')
echo "About to spend $COST credits on a single Soul Cinematic still."
```

Tell the user the cost and **wait for explicit confirmation** before submitting:
> "About to spend $COST credits. Confirm to proceed?"

Only proceed after the user says yes.

### 5. Submit + wait + download

```bash
mkdir -p runs/$RUN_ID/shot-01
echo "$STILL_PROMPT" > runs/$RUN_ID/shot-01/prompt.txt

RESULT=$(higgs --json generate create soul_cinematic \
  --prompt "$STILL_PROMPT" \
  --aspect_ratio 9:16 \
  --wait --wait-timeout 5m)

JOB_ID=$(echo "$RESULT" | jq -r '.id')
URL=$(echo "$RESULT" | jq -r '.result_url // .url // .urls[0]')

echo "$JOB_ID" > runs/$RUN_ID/shot-01/job-id.txt
echo "$URL" > runs/$RUN_ID/shot-01/result-url.txt
curl -sL "$URL" -o runs/$RUN_ID/shot-01/still.png
ls -la runs/$RUN_ID/shot-01/still.png
```

### 6. Verify the file

```bash
SIZE=$(stat -f%z runs/$RUN_ID/shot-01/still.png 2>/dev/null || stat -c%s runs/$RUN_ID/shot-01/still.png)
[ "$SIZE" -lt 10000 ] && echo "WARNING: still.png is suspiciously small ($SIZE bytes)"
```

### 7. Read live balance + compute actual spend

```bash
BAL_AFTER=$(higgs --json account status | jq -r '.credits')
ACTUAL=$((BAL - BAL_AFTER))
echo "Balance: $BAL → $BAL_AFTER (delta: $ACTUAL credits)"
```

### 8. Write the report

`runs/<RUN_ID>/stage-2-report.md` with:

1. **Submission** — prompt, aspect, wait time, click outcome
2. **Result** — job ID, result URL, local file path, file size in bytes
3. **Cost** — preflight estimate vs. actual delta vs. expected (12)
4. **Discrepancies** — preflight estimate vs. actual delta — diff if any
5. **Surprises + recommended changes** — anything off-spec

Then: `Stage-2 report: <path>`.

## Constraints

- **One shot only.** No video generation. No multi-shot.
- **Wait for explicit user confirmation** before clicking submit.
- **Hard cap: 10 minutes total wall-clock.** If past, stop and report what state we got to.
- **Don't commit. Don't edit `skill/`.** Don't install anything.

Begin.
