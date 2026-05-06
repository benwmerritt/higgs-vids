# Output Management

How the agent organises its outputs so they're navigable, deliverable, and resumable.

## Run directory layout

Every invocation creates `runs/<YYYY-MM-DD-HHMM>/` under the repo root. Predictable structure means the agent can resume mid-run and the user can find anything fast.

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

Required:
- The final assembled video (`reel-final.mp4`)
- A `README.md` with:
  - Brief title + one-line summary
  - Pattern used
  - Total cost (read from cost-log.json)
  - Number of shots, total duration
  - Models used per shot
  - Date + workspace
  - Any caveats (e.g. "Shot 3 had to be regenerated — note quality difference")

Optional (depending on pattern):
- Individual shot videos (some clients want these)
- Stills (poster frames)
- Multi-platform variants (if pattern is `multi-platform-render`, output 9:16, 1:1, 16:9)
- Source assets (uploaded reference photos)

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

## When the user asks "where's my video?"

The answer should always be a single concrete path:

> "`runs/2026-05-06-1430/deliverables/reel-final.mp4`. Total cost: 612 credits. See `runs/2026-05-06-1430/deliverables/README.md` for the full handoff."

Never "check the runs folder" or "in your output directory somewhere." Be specific.
