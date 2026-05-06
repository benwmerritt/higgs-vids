# Agent Tooling Rules

Hard rules about which tools the agent uses (and doesn't) when running any pattern in this skill. Written after a real test run produced wrong outputs because the agent reached for tools outside the skill's intended boundaries.

> **Treat these as non-negotiable.** Patterns cite this file; SKILL.md cites it; AGENTS.md cites it. When something behaves unexpectedly, this is the first reference to re-read.

## Image inspection — use the Read tool

Claude has vision. The `Read` tool reads PNG / JPG files and shows them to you visually. **That's how you inspect generated images.** You don't need a browser, screenshot tool, or external viewer.

```
Read tool, file_path: runs/<run-dir>/shot-01/image.png
→ image is presented; you can describe / critique / verify
```

This is how every "review your output" step in every pattern works.

## What you must NEVER do for image work

| ❌ Forbidden | Why | Use instead |
|---|---|---|
| Invoke `mcp__playwright__*` or any Playwright MCP tool | We deleted that whole architecture in v3. The agent reaching back for it is a regression. | `Read` tool on the PNG |
| Open a browser (Chrome / Safari / etc.) to view images | Defeats the purpose of agentic generation. The user already has the file on disk. | `Read` tool |
| Generate an HTML index / scrollable mockup of slides | The user posts to Instagram from their phone. HTML is irrelevant. | Per-slide PNGs + a markdown `README.md` |
| Stitch all slides into one tall preview image | Wastes credits and produces nothing the user can post | Each slide is its own file. Review each individually. |
| ⚠ Compose multiple images into ONE designed deliverable (e.g. a moodboard) | This is NOT banned — but it's only allowed via a real composition script (Pillow / `compose-moodboard.py`). Lazy `convert -append` PNG concatenation is banned. Browser-rendered HTML mockups are banned. | If a pattern's deliverable IS a composition (moodboard, deck, branded layout), use the dedicated composer script with brand mark + typography + designed grid. |
| Take a screenshot of a webpage / browser | This is a content-generation toolkit, not a scraper | If you need a reference image, ask the user for a path or URL |

## What you must NEVER do for skill loading

| ❌ Forbidden | Why |
|---|---|
| Load `frontend-design` skill mid-pattern | It's for HTML/CSS UI work; not relevant to social content. Loading it can steer the agent toward HTML outputs (which it did in real testing). |
| Load `artifacts-builder` mid-pattern | Same reason — pulls toward web artefacts |
| Load any skill not referenced from this skill's `references/` or `patterns/` files | Each loaded skill changes your behaviour. Stay inside the bundle unless a pattern explicitly names an official Higgsfield reference skill. |

The skills you may use are documented at the top of `SKILL.md`. If a pattern needs additional reference material, it explicitly says "load `references/X.md`" or names the exact official Higgsfield reference skill. That's the only loading allowed mid-run.

## What you must NEVER write

| ❌ Forbidden output | Why |
|---|---|
| Anything in the repo root | All run artefacts live in `runs/<run-dir>/`. Repo root pollution is a bug. |
| HTML files (`.html`, `.htm`) | Output is images the user uploads to social platforms. HTML is irrelevant. |
| Combined / stitched preview images | One image with N slides stacked vertically isn't useful — the user posts individual slides. |
| Files outside the run dir for the current run | Cross-run contamination. Each run is self-contained in its dated folder. |

## When generating any post-image content

The post-generation review loop is:

1. Generate (`higgs generate create ... --wait`)
2. Download (`curl -sL $URL -o <run-dir>/shot-NN/image.png`)
3. **Read the PNG** (`Read` tool, file_path: the .png)
4. Inspect against the pattern's checklist (logo intact? palette match? AI tells?)
5. Save findings to `<run-dir>/shot-NN/review.md`
6. If verdict is "retry", adjust prompt and regenerate. If "ship", proceed to next.

Skipping step 3 is the most common failure mode. The agent generates → ships without looking → user opens the file and finds garbage. Don't do that.

## When showing output to the user

The user wants:
- A path to the run dir (`runs/<dir>/deliverables/`)
- Specific paths to the headline files (`slide-01.png`, `caption.md`)
- A short list of what's in there

The user does NOT want:
- An HTML index they have to open in a browser
- A stitched preview image they can't post
- A flowery summary that hides the actual file paths

Be specific. Path-first. Brief.

## When something goes wrong

If a pattern step fails, the response is:
1. Stop the pattern (don't push through)
2. Read the error / inspect the bad output
3. Tell the user what went wrong with a specific path or error string
4. Ask before retrying anything that costs credits

Don't hide failures. Don't auto-recover by reaching for a different tool than what the pattern specifies.

## When in doubt

If a tool is not in:
- The Bash tool (for shell + `higgs` CLI)
- The Read tool (for files including images)
- The Edit / Write tools (for files in the run dir)
- A `mcp__claude_ai_*` MCP that the user explicitly requested
- The `firecrawl_scrape` tool (only during `/higgsfield-brand-create` for fetching user's existing channels)
- An official Higgsfield reference skill explicitly named by the active pattern

…then you don't use it during a pattern run. Patterns are intentionally scoped to a small toolset. If a pattern seems to need a tool outside this list, that's a signal the pattern needs updating — surface to the user, don't reach for the tool.

## Composed-deliverable patterns (the moodboard exception)

Some patterns produce a **composed deliverable** — a single designed image that combines multiple generated images, brand mark, palette, and copy. The moodboard pattern is the canonical example. The composition IS the product, not a preview of separate assets.

For these patterns, the rule isn't "no compositing" — it's "compositing only via a designed script, never via HTML or shortcut concat":

- ✅ **Allowed:** call a dedicated Python composer script (e.g. `scripts/compose-moodboard.py` — Pillow-based, deterministic, produces PNG + PDF)
- ❌ **Banned:** generating an HTML page, taking a browser screenshot, concatenating PNGs with `convert -append`, using ffmpeg to "stitch", asking another AI image model to "lay these out"

The distinction: composition with intent (typography, brand mark placement, palette swatch design, layout system) vs. lazy concatenation (just stack the PNGs and hope). The first is a real deliverable. The second is the carousel-post failure mode.

When working on a composed-deliverable pattern, **the pattern's Step 10 (or equivalent) names the script to call**. Use that script. If the script is missing or broken, surface the error — don't reach for HTML/ffmpeg/Playwright as substitutes.

## Source

These rules are a direct response to two 2026-05 test runs:

**2026-05-06 (carousel-post):**
- Opened Playwright MCP to "screenshot" generated images (instead of using Read)
- Loaded the `frontend-design` skill mid-pattern (causing HTML-flavored outputs)
- Wrote review PNGs to the repo root instead of the run dir
- Generated HTML index + stitched preview images instead of per-slide PNGs

**2026-05-07 (moodboard):**
- Skipped composition entirely (pattern instructions said "don't compose"); user expected a finished moodboard
- When pushed to compose, generated `moodboard.html` (banned) and reached for ffmpeg (wrong tool)
- Took a screenshot of the HTML to produce `moodboard.png` (lazy stitched-preview pattern)

The moodboard test taught us: **patterns whose deliverable is a composition need an explicit composer script.** Banning all composition over-corrects; the right rule is "compose with design intent via a dedicated script, not via HTML or concat shortcuts."

All these failures stem from the agent reaching outside the skill bundle's intended toolset. This file's job is to prevent that.
