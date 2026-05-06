# Higgsfield Autopilot Skill

The skill bundle that turns a brief into a delivered video using the Higgsfield CLI.

> **Read order if you're an agent:** `SKILL.md` → `references/cli-cheatsheet.md` → `references/cost-discipline.md` → `patterns/README.md` → the specific `patterns/<name>.md` you'll execute.

> **Read order if you're a human:** the top-level `README.md` and `AGENTS.md` cover the user-facing story. This file is here for completeness; the operational stuff lives in `SKILL.md`.

## What's in this directory

```
SKILL.md                   ← Agent's operating manual (8-step workflow + rules)
README.md                  ← This file
references/
  cli-cheatsheet.md         ← Every higgs CLI command + when to use it
  cost-discipline.md        ← Preflight, confirmation thresholds, ledger
  model-selection-guide.md  ← Which Higgsfield model for which job
  output-management.md      ← Run dir layout, deliverables, resumption
  soul-cinema-prompting.md  ← Subject → Scene → Action → Camera → Lighting → Style
  brief-expansion-rules.md  ← Brief → shotlist
patterns/
  README.md                 ← Pattern decision tree
  product-reel.md           ← Full — IG-ready 9:16 multi-shot reel
  quick-social.md           ← Full — single shot, low credit
  multi-platform-render.md  ← Full — one concept × N aspects
  brand-shoot.md            ← Stub (v3.1) — product-photoshoot batches
  ecom-listing.md           ← Stub (v3.1) — marketplace cards
  character-campaign.md     ← Stub (v3.1) — Soul ID series
briefs/
  README.md                 ← Brief format guide
  example-{product-reel,quick-social,multi-platform,retro-futuristic}.md
scripts/
  assemble-video.py         ← ffmpeg concat helper (the only script the agent calls)
test/
  README.md                 ← Verification harness overview
  stage-1.md                ← Cost preview only (0 credits)
  stage-2.md                ← Single shot (~12 credits)
  stage-3.md                ← Full reel (~1k–12k credits)
```

## Why no install.sh, cost-log.py, deliver.sh, etc.?

The agent does these inline as a few lines of bash. Wrapping each into a script for the sake of it adds maintenance debt with no benefit.

The one exception is `assemble-video.py` — ffmpeg concat with crossfades has enough variants and gotchas (codec mismatch, filter graph syntax) that a tested wrapper script saves the agent from re-discovering the right invocation each time.

## Why no Playwright, MCP, browser automation?

We deleted all of that. The Higgsfield CLI (`@higgsfield/cli`, released 2026-05-04) replaces every reason we needed it. See `../findings/instagram-reel-DXfKnWhDPlW-workflow.md` for the full history of v1 (Python pipeline) → v2 (Playwright MCP) → v3 (CLI).
