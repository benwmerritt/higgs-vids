# Agent Onboarding

> You're an AI agent operating inside this repo. Read this file first.

This is a **video production toolkit** built on top of the official Higgsfield CLI (`@higgsfield/cli`). The human says one sentence; you produce delivered video/image bundles.

## Your operating manual

**The single source of truth for what you do here is `skill/higgsfield-autopilot/SKILL.md`.** Read it in full at the start of any task that involves making videos or images.

## What's available to you

| Tool | Use |
|---|---|
| `higgs` CLI | All Higgsfield generation, upload, account, workspace operations. See `skill/higgsfield-autopilot/references/cli-cheatsheet.md`. |
| Bash | To invoke `higgs`, parse `--json` output with `jq`, run `curl` for downloads, run `ffmpeg`. |
| **Read tool** | **For inspecting generated images.** Claude has vision. Read the PNG, check logo intact, palette match, no AI tells. Mandatory in every pattern. |
| `python3` | Only for `skill/higgsfield-autopilot/scripts/assemble-video.py` (ffmpeg concat). No other Python. |
| Markdown reading | All your operational knowledge lives in `.md` files under `skill/higgsfield-autopilot/`. |
| `firecrawl_scrape` | Only during `/higgsfield-brand-create` to fetch user's existing channels (website, IG). Not during patterns. |
| Humanizer skill (if installed) | Apply as the FIRST voice pass on any generated copy, before brand voice. See README.md setup notes. |

## What you must NOT do

- **Don't spawn a browser.** No Playwright, no MCP browser tools, no Chrome automation. Use the Read tool for images. See `references/agent-tooling-rules.md`.
- **Don't load unrelated skills outside this bundle.** No `frontend-design`, no `artifacts-builder`, nothing that steers toward HTML or browser output. The only allowed external references are official Higgsfield product/listing skill docs when a pattern explicitly names them.
- **Don't generate HTML files or stitched preview images.** Output is PNGs the user posts. Each slide is its own file in its own `shot-NN/` subfolder.
- **Don't write to the repo root.** Every artefact goes in `runs/<run-dir>/`.
- **Don't ship a batch without calibration.** Generate 1, review (Read tool), confirm with user, then batch the rest.
- **Don't ship copy with em dashes.** Instant AI tell. Refuse and rewrite.
- **Don't inflate user words.** When writing brand profiles, use the user's verbatim phrasing; mark agent inferences as `[brackets]`.
- **Don't print `higgs auth token` output.** It's a credential.
- **Don't spend without preflight.** Always run `higgs generate cost ...` before `higgs generate create ...`. See `references/cost-discipline.md`.
- **Don't commit to git.** The user does that.
- **Don't auto-install dependencies.** `npm install`, `brew install`, etc. stay user-driven. (`higgs auth login` is fine to run *with explicit user consent* — it's a CLI action, not a system install — see `references/onboarding-flow.md` § 2.)
- **Don't refuse to engage with users who have no Higgsfield account yet.** Brand setup, moodboard ideation, and asset prep all deliver value without burning credits. See `references/onboarding-flow.md`.
- **Don't push first-time users straight at `/higgsfield-make`.** Cold-start handling lives in `references/onboarding-flow.md` — read it when the user lands without a brief, brand profile, or clear creative intent.

## Slash commands the human will type

| Command | Maps to |
|---|---|
| `/higgsfield-init` | First-run setup + conversational onboarding (CLI check, asks if user has an account and signs them in if so, classifies plan tier, ends with a four-way menu — brand setup / free moodboard demo / shape an idea / just explore). Reads `references/onboarding-flow.md` for the decision tree. |
| `/higgsfield-brand-create <name>` | Adaptive interview → `brands/<name>/profile.md` + assets folder |
| `/higgsfield-preset-create <brand> <pattern>` | Reusable preset on top of brand profile → `presets/<name>.md` |
| `/higgsfield-make <brief\|--brand <name> "topic"\|--preset <name> "topic">` | Main entry — brand-aware when given a brand or preset |
| `/higgsfield-pattern <name> [args]` | Direct pattern execution |
| `/higgsfield-test <1\|2\|3>` | Stage verification |
| `/higgsfield-budget [path]` | Cost queries |

When the human invokes one of these, the matching file in `commands/claude/` tells you exactly what to do. Claude Code gets those files through symlinks created by `install.sh`; the source lives in this repo.

## Brand-flow (the personalisation layer)

If the human's request mentions a brand by name (or you see `brands/<name>/` exists in the repo), **load that brand profile first** and apply it to every step. The brand profile contains:
- Voice (how they actually write — lexicon, sentence patterns, banned words)
- Visual DNA (palette, photo aesthetic, mood)
- Audience (the specific person, not demographic)
- Spike (what makes them non-substitutable)
- Constraints (hard rules — refuse to produce these)
- Soul ID (face-faithful identity model, if trained)
- Hashtag families

Without a brand profile, generation is generic (acceptable for exploration). With one, output should feel like that brand's content. **The brand profile is not optional once it exists** — refusing to apply it would be a bug.

When the human invokes one of these, the matching file in `commands/claude/` tells you exactly what to do. Claude Code gets those files through symlinks created by `install.sh`; the source lives in this repo.

## Repo map

```
commands/claude/              ← slash command source (symlinked into ~/.claude/commands/)
brands/                       ← real brand profiles (gitignored — private assets)
  <name>/profile.md             voice, audience, spike, visual DNA, constraints
  <name>/assets/                user-provided logos, photos, style refs, samples
  <name>/source-fetches/        auto-imported context from web channels
  <name>/soul-id.txt            UUID of trained Soul ID (if any)
presets/                      ← reusable brand × pattern × platform configs (gitignored)
  <brand>-<pattern>.md
skill/higgsfield-autopilot/   ← the skill bundle — your operating manual
  SKILL.md                     ← read first
  references/                  ← CLI cheatsheet, model selection, cost discipline, brand/preset/interview/hook/caption/hashtag craft, prompting
  patterns/                    ← 8 recipes per use case (carousel-post, moodboard, product-reel, quick-social, multi-platform-render, brand-shoot, ecom-listing, character-campaign)
  briefs/                      ← example inputs
  scripts/assemble-video.py    ← ffmpeg concat helper (the only script you call)
  test/                        ← stage 1/2/3 verification prompts
docs/research/                ← deep-dive research on Higgsfield (background reading)
docs/ask-rag/                 ← MCP knowledge artefacts (Ads Marketing 9-question)
docs/skills/                  ← peer skill: prompt design (skill-higgsfield-shot-designer.md)
findings/                     ← origin story (IG reel that inspired v1) + empirical findings (Starter plan)
runs/                         ← per-run outputs (gitignored)
```

## Cross-agent

This toolkit is agent-agnostic. The same SKILL.md, references, patterns, and briefs work in:
- **Claude Code** (Claude Desktop's Code tab) — slash commands activate immediately
- **Codex / OpenCode / Gemini CLI** — read SKILL.md as context, invoke via natural language

There's no agent-specific code anywhere in `skill/`. The `higgs` CLI is the same binary regardless of which agent is calling it.

## When you're confused

If a brief doesn't fit any pattern, default to `patterns/product-reel.md` and adapt the shotlist. If the brief is genuinely outside scope (e.g. asks for music composition or 3D modelling), stop and tell the user.

If a `higgs` command fails in a way the CLI cheatsheet doesn't cover, run `higgs <command> --help` to check current flags. The CLI is moving fast (new release on 2026-05-04); flags may have shifted since the cheatsheet was last updated.

If the user says "just do it" without confirmation prompts, see `references/cost-discipline.md` § "When the user says 'just do it'" — the rules are there.
