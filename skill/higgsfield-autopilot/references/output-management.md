# Output Management

How the agent organises its outputs so they're navigable, deliverable, and resumable.

> **Hard rules** (per `references/agent-tooling-rules.md`):
> - Every run artefact lives in the run dir. **NEVER write to the repo root.**
> - Output is **images + caption markdown**. **No HTML, no stitched previews, no scrollable mockups.**
> - The user posts to Instagram from their phone — they need PNGs and a caption to copy.

## Run directory naming (mandatory format)

```
runs/<YYYY-MM-DD>-<brand>-<pattern>-<seq>/
```

- **Date prefix mandatory** — sorts chronologically, instantly readable
- **Brand name** in lowercase (or `none` if no brand profile is in play)
- **Pattern type** lowercase (`carousel`, `reel`, `shoot`, etc.)
- **`<seq>`** auto-increments per same-day same-brand-pattern run

Examples:

```
runs/2026-05-06-ben-carousel-1/        ← Ben's first carousel run today
runs/2026-05-06-ben-carousel-2/        ← Ben's second carousel run today
runs/2026-05-07-ben-reel-1/            ← Ben's first reel tomorrow
runs/2026-05-07-acme-shoot-1/          ← Acme client shoot
runs/2026-05-08-none-carousel-1/       ← No brand, one-off exploration
```

Computing `<seq>`: list `runs/` for the same date+brand+pattern prefix, take max(seq)+1, default 1.

## Run directory layout

```
runs/2026-05-06-1430/
├── brief.md                       ← copy of the input brief (so it's self-contained)
├── shotlist.json                  ← agent-generated structured plan
├── cost-log.json                  ← per-run cost ledger (see cost-discipline.md)
├── commands.log                   ← every higgs CLI invocation (timestamp + cmd + model + exit) — audit trail
├── models-available.txt           ← higgs model list output captured at run start (snapshot of CLI truth)
├── pattern.txt                    ← the pattern name used (e.g. "product-reel")
├── shot-01/
│   ├── prompt.txt                 ← exact prompt sent to Higgsfield
│   ├── job-id.txt                 ← Higgsfield job UUID (so we can re-fetch)
│   ├── result-url.txt             ← signed URL Higgsfield returned
│   ├── take-1.mp4                 ← downloaded asset (or .png for stills)
│   ├── take-2.mp4 ..              ← additional variants if --count > 1
│   └── take-best.mp4 → take-N.mp4 ← symlink to the chosen take
├── shot-02/
│   └── …
├── deliverables/
│   ├── reel-final.mp4             ← assembled output (ffmpeg concat of take-best per shot)
│   ├── poster.png                 ← optional: first-frame export
│   └── README.md                  ← human-readable handoff (what's in the bundle, total cost, runtime)
└── notes.md                       ← agent's own observations, surprises, recommendations
```

## Naming conventions (lock these in)

- **Run ID:** `YYYY-MM-DD-HHMM` — sortable, human-readable, no spaces. Use UTC if running in CI; local time is fine for interactive use.
- **Shot directories:** `shot-NN` zero-padded to 2 digits (`shot-01`, not `shot-1`).
- **Takes:** `take-1.mp4` … `take-N.mp4`. The "best" pick is **always a symlink** to the chosen take (`ln -sf take-3.mp4 take-best.mp4`).
- **Stills vs videos:** extension reflects type. Don't put .png inside a folder named `video-shot-01`.
- **Job IDs / URLs:** plain text files, one per line, no JSON wrapping (cheap to grep).

## commands.log — the per-run audit trail

Every pattern run keeps a single flat file `commands.log` capturing every `higgs` CLI invocation made during the run. Plain text (not JSON) so `grep` / `cat` work without tools. One event per line.

### Format

```
[2026-05-07T14:23:01Z] START     pattern=moodboard brand=ben run=runs/2026-05-07-ben-moodboard-1
[2026-05-07T14:23:03Z] PREFLIGHT higgs account status → exit=0 balance=248.9 plan=Starter
[2026-05-07T14:23:04Z] MODELS    higgs model list --image → exit=0 (saved: models-available.txt, count=12)
[2026-05-07T14:23:05Z] CHECK     soul_cinematic ✓ present
[2026-05-07T14:23:15Z] GEN       shot=01 model=soul_cinematic aspect=16:9 job=abc123 → exit=0
[2026-05-07T14:24:05Z] DL        shot=01 url=https://cdn.higgsfield.ai/... → exit=0 size=2.1MB
[2026-05-07T14:26:30Z] GEN       shot=02 model=soul_cinematic aspect=4:5  job=def456 → exit=0
[2026-05-07T14:31:12Z] COMPOSE   compose-moodboard.py → exit=0 output=deliverables/moodboard.png
[2026-05-07T15:01:44Z] END       shots=9 actual_spend=1.1 failures=0
```

### Event types

- `START` — first line of every run; pattern + brand + run dir
- `PREFLIGHT` — auth/balance/workspace checks
- `MODELS` — captured `higgs model list` (the snapshot lives in `models-available.txt`)
- `CHECK` — per-model availability verification (✓ present / ✗ NOT FOUND)
- `GEN` — every `higgs generate create` (record model name + job ID + exit)
- `DL` — every download (curl / asset fetch)
- `UPLOAD` — every `higgs upload create`
- `COMPOSE` — composer scripts (compose-moodboard.py, assemble-video.py)
- `RETRY` — second attempt after failure
- `FAIL` — terminal failure for a shot
- `END` — last line; final shot count + actual spend

### Why text not JSON

Ben's primary use: "what model was used for shot 3?" → `grep "shot=03" commands.log` gives the answer. JSON would need `jq` and parser knowledge. Plain text wins for an audit file you cat.

### Canonical run-init snippet (every pattern's Step 0)

Patterns reference this — it's the standard preamble before any spending:

```bash
# 1. Compute run dir
RUN_DIR="runs/$(date +%Y-%m-%d)-${BRAND:-none}-${PATTERN}-${SEQ}"
mkdir -p "$RUN_DIR"

# 2. Initialise commands.log
TS() { date -u +%Y-%m-%dT%H:%M:%SZ; }
echo "[$(TS)] START     pattern=$PATTERN brand=${BRAND:-none} run=$RUN_DIR" > "$RUN_DIR/commands.log"

# 3. Preflight (auth + balance + workspace)
ACC=$(higgs --json account status)
BAL_BEFORE=$(echo "$ACC" | jq -r '.credits')
PLAN=$(echo "$ACC" | jq -r '.plan // "unknown"')
echo "[$(TS)] PREFLIGHT higgs account status → exit=0 balance=$BAL_BEFORE plan=$PLAN" >> "$RUN_DIR/commands.log"

WS=$(higgs --json workspace status | jq -r '.name // "Private"')
echo "[$(TS)] PREFLIGHT higgs workspace status → exit=0 workspace=$WS" >> "$RUN_DIR/commands.log"

# 4. Live model check — CLI is the source of truth
# Pick --image or --video based on pattern's media type. Patterns that need both run twice.
higgs --json model list --image > "$RUN_DIR/models-available.txt"
MODEL_COUNT=$(jq 'length' "$RUN_DIR/models-available.txt")
echo "[$(TS)] MODELS    higgs model list --image → exit=0 (saved: models-available.txt, count=$MODEL_COUNT)" >> "$RUN_DIR/commands.log"

# 5. Verify required models are present (replace REQUIRED_MODELS with the pattern's list)
REQUIRED_MODELS=("soul_cinematic")
for MODEL in "${REQUIRED_MODELS[@]}"; do
  if jq -e --arg m "$MODEL" '.[] | select(.name == $m)' "$RUN_DIR/models-available.txt" > /dev/null; then
    echo "[$(TS)] CHECK     $MODEL ✓ present" >> "$RUN_DIR/commands.log"
  else
    echo "[$(TS)] CHECK     $MODEL ✗ NOT FOUND — stopping" >> "$RUN_DIR/commands.log"
    echo "ERROR: model '$MODEL' missing from higgs model list. See $RUN_DIR/models-available.txt." >&2
    exit 1
  fi
done
```

### Logging GEN events

Every `higgs generate create` call should log before+after. Inline pattern (do NOT use a wrapper script — `RESULT=$(...)` capture must stay clean):

```bash
RESULT=$(higgs --json generate create soul_cinematic --prompt "$P" --aspect_ratio 16:9 --wait)
EXIT=$?
JOB_ID=$(echo "$RESULT" | jq -r '.id // "N/A"')
echo "[$(TS)] GEN       shot=$ID model=soul_cinematic aspect=16:9 job=$JOB_ID → exit=$EXIT" >> "$RUN_DIR/commands.log"
```

### END line

Close the run before reporting to the user:

```bash
BAL_AFTER=$(higgs --json account status | jq -r '.credits')
ACTUAL=$(echo "$BAL_BEFORE - $BAL_AFTER" | bc)
echo "[$(TS)] END       shots=$SHOT_COUNT actual_spend=$ACTUAL failures=$FAIL_COUNT" >> "$RUN_DIR/commands.log"
```

### Reading the log later

```bash
# What model did I use for each shot?
grep "GEN" runs/2026-05-07-ben-moodboard-1/commands.log

# What was the total spend (from the END line)?
grep "END" runs/2026-05-07-ben-moodboard-1/commands.log

# Did any shot retry?
grep -E "RETRY|FAIL" runs/2026-05-07-ben-moodboard-1/commands.log
```

## Resumption

Because every step writes a file, the agent can resume an interrupted run. Pre-flight check at the start of every step:

| Step | Skip if exists |
|---|---|
| Brief read | `brief.md` exists in run dir |
| Shotlist generation | `shotlist.json` exists |
| Per-shot generation | `shot-NN/result-url.txt` exists AND result-url is reachable |
| Asset download | `shot-NN/take-1.<ext>` exists with non-zero bytes |
| Best-take pick | `shot-NN/take-best.<ext>` symlink exists |
| Final assembly | `deliverables/reel-final.mp4` exists |

Add `--force` semantics if the user explicitly wants to re-do a step.

## The deliverables/ bundle

This is what the user (or their client) receives. **Treat it as the only thing the user might look at.** Everything else is debug context.

Required (vary by pattern):
- The deliverable assets — PNGs for image patterns, MP4 for video patterns
- A `README.md` with:
  - Brief title + one-line summary
  - Pattern used
  - Total cost (read from cost-log.json)
  - Asset count + dimensions
  - Models used per shot
  - Date + workspace
  - Any caveats ("Shot 3 needed regeneration", "Calibration shot retried twice", etc.)
  - **Plain-language posting instructions** — "upload slides 01-06 in order", "open the file with Preview", etc.

**What MUST NOT be in `deliverables/`:**
- ❌ HTML files (`.html`, `.htm`)
- ❌ Stitched / scrollable preview images (one tall PNG with all slides stacked)
- ❌ Combined "mockup" screenshots
- ❌ Files outside the patterns the user asked for

The user opens these files in Preview / Finder / their phone. They don't open them in a browser. Don't generate web artefacts.

## Cross-run summary

`runs/cost-summary.json` is a rolling ledger across all runs in the repo:

```json
[
  {"run_id": "2026-05-04-0930", "pattern": "quick-social", "spend": 24, "deliverables": 1, "workspace": "Private"},
  {"run_id": "2026-05-06-1430", "pattern": "product-reel", "spend": 612, "deliverables": 5, "workspace": "Acme"}
]
```

The agent appends to this file at the end of each run. `/higgsfield-budget` reads it.

## What to gitignore

The `.gitignore` at the repo root excludes `runs/` and `skill/**/runs/`. **Don't commit run outputs** — they can be hundreds of MB per run, and the cost-log contains workspace-level financial info.

If the user wants to share a deliverable, they share the file directly (Slack, Drive, etc.) — not by committing it.

## When the user asks "where's my video?" / "where's my carousel?"

The answer should always be a single concrete path:

> "`runs/2026-05-06-ben-carousel-1/deliverables/`. 6 slides + caption. Total spend: 0.7 credits. Open the PNGs with Preview or your phone."

Never "check the runs folder" or "in your output directory somewhere." Be specific. Path-first.

## Anti-patterns (real failures from 2026-05-06 test run)

These are documented as failure modes so future runs avoid them:

| ❌ Failure | What happened | Fix |
|---|---|---|
| Review PNGs in repo root | Agent wrote `review-slide-1.png` etc. to `./` instead of run dir | Every artefact goes in `runs/<run-dir>/` |
| Run dir named `ben-carousel-1` (no date) | Hard to chronologically sort runs | `<YYYY-MM-DD>-<brand>-<pattern>-<seq>` is mandatory |
| `index.html` output | Agent generated a web page mockup | No HTML — output is images |
| Stitched preview screenshot | Agent made one tall PNG with all slides stacked | No stitched previews — each slide is its own file |
| "Open the index.html to review" | Agent told user to open in browser | "Open the PNGs with Preview / your phone" |
| Loaded `frontend-design` skill mid-run | Pulled in HTML-flavoured behaviour | Don't load unrelated skills outside this bundle (`references/agent-tooling-rules.md`) |
