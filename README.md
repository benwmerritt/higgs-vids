# Higgs Vids

A video production toolkit for Claude Code. Tell the agent what you want; it uses your brand profile, the Higgsfield CLI, and a set of recipes to produce post-ready content (carousels, moodboards, reels, product photos, listings) — saved to a dated folder ready to share or post.

Built on the official [Higgsfield CLI](https://github.com/higgsfield-ai/cli). MIT-licensed.

## Setup (5 min, one-time)

```bash
# Dependencies
npm install -g @higgsfield/cli           # the Higgsfield CLI
brew install ffmpeg                      # for reel patterns (or apt install ffmpeg)
pip install Pillow                       # for moodboard composition

# Sign in (browser opens)
higgs auth login

# Clone + install
git clone <repo-url> higgs-vids
cd higgs-vids
bash install.sh                          # symlinks skill + commands into ~/.claude/

# Open Claude Code (in any folder), then:
/higgsfield-init
```

`install.sh` symlinks the skill and slash commands into `~/.claude/` so they work in **any** Claude Code session, not just inside this repo. Edits in this repo propagate immediately. To remove the symlinks (repo stays intact): `bash uninstall.sh`.

Optional but recommended: install a "humanizer" skill if you have one — the toolkit applies it as a base voice layer so generated copy reads like a human wrote it before brand voice gets layered on.

## Slash commands

Type these in Claude Code. They auto-detect a brand profile when one applies.

| Command | What it does | Spends credits? |
|---|---|---|
| `/higgsfield-init` | First-run health check: confirms CLI is installed and authed, picks active workspace, reports balance. Run once per machine. | No |
| `/higgsfield-brand-create <name>` | Adaptive interview to build a brand profile. ~30 min. Captures voice, audience, visual DNA, do's and don'ts. Optionally fetches your existing channels and trains a Soul ID. Saves to `brands/<name>/`. | No (Soul ID training is opt-in) |
| `/higgsfield-preset-create <brand> <recipe>` | Save a reusable shape for a content type, e.g. *"Ben's IG carousels are always 6 slides, 4:5, list-format"*. After this you can run that recipe by preset name. | No |
| `/higgsfield-make "topic"` | Main entry. Agent reads your topic, picks the right recipe, generates the content. Add `--brand <name>` to apply a brand profile. Add `--preset <name>` to use a saved shape. | Yes |
| `/higgsfield-pattern <name> "args"` | Run a specific recipe directly when you know which one you want. E.g. `/higgsfield-pattern moodboard --brand ben "yacht shoot"`. | Yes |
| `/higgsfield-budget [path\|workspace]` | "What did I spend?" Reads cost logs across runs. No args = all-time total. With a path = that run only. With a workspace name = filter to that workspace. | No |
| `/higgsfield-test <1\|2\|3>` | Verify the toolkit works. **Stage 1 = no credits** (preflight only), 2 = ~12 credits (one image), 3 = a full reel. | Stage-dependent |

## Recipes (patterns)

| Recipe | Use for | Typical actual cost on a paid plan |
|---|---|---|
| `carousel-post` | IG/LinkedIn carousel — 5-10 slides + caption + hashtags, all in your brand voice | ~0.6-1.2 credits |
| `moodboard` | Pre-production / pitch-deck reference for a client. Composed branded PNG + PDF. | ~0.7-1.4 credits |
| `quick-social` | Single still or short clip for daily posts | ~0.1-3 credits |
| `multi-platform-render` | One concept rendered to multiple aspect ratios (9:16 + 1:1 + 16:9) | ~0.4-2 credits |
| `brand-shoot` | Product photography batch — hero, lifestyle, virtual try-on, etc. | ~0.5-20 credits |
| `ecom-listing` | Amazon / Etsy / Shopify listing imagery (main + secondary + A+) | ~1.5-20 credits |
| `character-campaign` | Recurring talent / brand mascot using a trained Soul ID | varies |
| `product-reel` | Multi-shot 9:16 video reel — stills + image-to-video + ffmpeg assembly | ~6-125 credits |

These are estimates on a paid Higgsfield plan; rack rates run ~100× higher and the toolkit handles preflight + confirmation. See `skill/higgsfield-autopilot/references/cost-discipline.md` for how cost is actually measured (live balance deltas, not preflight estimates).

## Where things live

```
brands/<name>/                ← your brand profiles + assets (gitignored)
  profile.md                    voice, audience, visual DNA, constraints
  assets/                       logos, photos of you, style guides
  source-fetches/               cached scrapes of your existing channels
presets/                      ← saved recipe shapes (gitignored)

runs/<date>-<brand>-<recipe>/ ← every run, dated and labelled (gitignored)
  shot-NN/                      per-shot prompts, URLs, images, agent reviews
  deliverables/                 ← what you actually post / send to clients

skill/higgsfield-autopilot/   ← the toolkit — agent reads this
  SKILL.md                      operating manual
  patterns/                     recipes
  references/                   how-to docs the agent loads
  scripts/                      ffmpeg + Pillow helpers
  test/                         verification stages

docs/                         ← background research + MCP knowledge artefacts
findings/                     ← origin story + empirical findings
```

The agent always tells you the deliverable path at the end of a run. Everything important is in `runs/<date>-<brand>-<recipe>/deliverables/`.

## Cost discipline

Real money is at stake. The toolkit:

1. Always **preflights** before spending (`higgs generate cost`, free).
2. **Reports the estimate** to you.
3. **Asks before spending** if the estimate is significant.
4. **Measures actual spend** by reading your `higgs account status` balance before and after — not by trusting the preflight number.
5. **Logs every run** to `runs/<date>-<brand>-<recipe>/cost-log.json`.

Higgsfield's CLI is currently plan-blind: `generate cost` returns rack rate even if your subscription absorbs 99% of it. The toolkit handles that gap by relying on the live balance delta as ground truth.

## Cross-agent compatibility

The skill is plain markdown + bash. Slash commands are Claude Code UX sugar. The same toolkit works in:

- **Claude Code** — slash commands native
- **Codex / Gemini CLI / OpenCode** — point the agent at `AGENTS.md` and instruct via natural language

## Origin

Started as a reverse-engineering project of an Instagram reel claiming "Claude autopilot for Higgsfield" via 15 agents and Playwright MCP. Frame analysis revealed it was actually a Playwright Python pipeline. v1 reproduced that. v2 replaced it with Playwright MCP (cleaner, but Higgsfield's UA sniffer blocked our browser). v3 deleted both when Higgsfield released their official CLI on 2026-05-04 — and built a real video-business toolkit on top instead. See `findings/instagram-reel-DXfKnWhDPlW-workflow.md` for the full story.

## License

MIT. The Higgsfield CLI is also MIT. Higgsfield's underlying generation models are commercial — credits cost real money. The toolkit's job is to spend them carefully on your behalf.
