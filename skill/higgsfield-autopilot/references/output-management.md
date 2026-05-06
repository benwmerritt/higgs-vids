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
