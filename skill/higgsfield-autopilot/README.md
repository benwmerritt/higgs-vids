# Higgsfield Autopilot Skill

The skill bundle that powers the slash commands in Claude Code (and works in other agents too).

> **Read order if you're an agent:** `SKILL.md` → `references/agent-tooling-rules.md` → `references/cost-discipline.md` → `references/cli-cheatsheet.md` → `patterns/README.md` → the specific `patterns/<name>.md` for the recipe you're running.
>
> **Read order if you're a human:** the top-level `README.md` covers the user story (commands, recipes, setup). This file just lists what's in this directory.

## Layout

```
SKILL.md                          ← agent's operating manual (foundational rules + 8-step workflow)
README.md                         ← this file

references/                       ← agent reference docs (loaded as needed)
  cli-cheatsheet.md                 every higgs CLI command + when to use it
  cost-discipline.md                preflight ritual, ledger format, capability checks
  model-selection-guide.md          which Higgsfield model for which job
  output-management.md              run dir naming, deliverables, no-HTML/no-stitched-preview
  agent-tooling-rules.md            no Playwright, no other skills, image review via Read tool
  known-issues.md                   upstream bugs + workarounds
  empirical-tests.md                ranked experiments to calibrate unknowns
  interview-craft.md                adaptive brand-create interview philosophy
  brand-profile-format.md           schema for brands/<name>/profile.md
  preset-format.md                  schema for presets/<name>.md
  asset-conventions.md              folder layout, photo requirements, caching
  hook-craft.md                     hook patterns + ≤10-word cap + AI tells
  caption-craft.md                  caption rules + hard bans (em dashes, etc.)
  hashtag-strategy.md               per-platform hashtag counts + brand families
  calendar-defaults.md              cadence/format mix per brand type
  soul-cinema-prompting.md          Subject → Scene → Action → Camera → Lighting → Style
  brief-expansion-rules.md          brief → shotlist

patterns/                         ← the recipes
  README.md                         decision tree (when to use which recipe)
  carousel-post.md                  IG/LinkedIn carousel (calibration-first)
  moodboard.md                      pitch-deck moodboard with composed PNG/PDF deliverable
  quick-social.md                   single still / short clip
  multi-platform-render.md          one concept × N aspects
  brand-shoot.md                    product photography (delegates to higgsfield-product-photoshoot)
  ecom-listing.md                   marketplace listing imagery
  character-campaign.md             Soul ID-driven series
  product-reel.md                   multi-shot 9:16 video reel

briefs/                           ← example inputs for testing/learning
scripts/
  assemble-video.py                 ffmpeg concat helper (reel patterns)
  compose-moodboard.py              Pillow image composer (moodboard pattern)
test/                             ← stage-1/2/3 verification (cost-preview / single-shot / full)
```

## Dependencies

- `higgs` CLI from `@higgsfield/cli` — the engine
- `ffmpeg` — required by `assemble-video.py` (reel patterns)
- `Pillow` (Python `pip install Pillow`) — required by `compose-moodboard.py`

The skill itself is just markdown + two small Python scripts. No Node, no virtualenv, no Playwright.

## Why no Playwright / MCP / browser automation

We deleted all of that. The Higgsfield CLI (released 2026-05-04) replaces every reason we needed it. The `references/agent-tooling-rules.md` file documents the explicit "don't reach for these tools" rules that came out of real test failures. See `../../findings/instagram-reel-DXfKnWhDPlW-workflow.md` for the full v1 → v2 → v3 history.
