# Higgs Vids

A video production toolkit for Claude Code. Tell the agent what you want; it uses your brand profile, the Higgsfield CLI, and a set of recipes to produce post-ready content (carousels, moodboards, reels, product photos, listings) — saved to a dated folder ready to share or post.

Built on the official [Higgsfield CLI](https://github.com/higgsfield-ai/cli). MIT-licensed.

## Setup

Fastest path: paste this into Claude Code.

```text
Clone https://github.com/benwmerritt/higgs-vids, read its README.md and INSTALL.md, run bash install.sh, and walk me through any missing setup. Do not generate content yet. Once setup passes, run /higgsfield-init.
```

<details>
<summary>Manual install commands</summary>

```bash
git clone https://github.com/benwmerritt/higgs-vids.git
cd higgs-vids
bash install.sh
```

</details>

`install.sh` checks local dependencies, reports exact next steps for anything missing, and symlinks the skill and slash commands into `~/.claude/` so they work in **any** Claude Code session. To remove the symlinks (repo stays intact): `bash uninstall.sh`.

Then open Claude Code and run:

```text
/higgsfield-init
```

`/higgsfield-init` verifies the CLI, sign-in, workspace, balance, and model access. If you want a deeper no-credit workflow check later, run `/higgsfield-test 1`. See [INSTALL.md](INSTALL.md) for dependency details, Windows notes, and the full first-run flow.

Optional but recommended: install a "humanizer" skill if you have one — the toolkit applies it as a base voice layer so generated copy reads like a human wrote it before brand voice gets layered on.

## Slash commands

Type these in Claude Code. The two commands that make this stop feeling generic are brand profiles and presets.

### Setup your brand engine — no credits spent

- **`/higgsfield-init`** — first-run health check. Confirms the Higgsfield CLI is installed and signed in, picks the active workspace, reports your credit balance. Run once per machine.

**Use this when you want Higgsfield output to feel like your brand, not generic AI content.** Claude interviews you once, learns your voice, audience, taste, visual references, constraints, content goals, and reusable assets, then saves that as a brand profile. After this, content generated with your brand stops starting from a blank generic prompt and starts from your actual style.

Run: **`/higgsfield-brand-create <name>`**  
Then generate with: **`/higgsfield-make --brand <name> "topic"`**

**Use this when you repeat the same kind of content and do not want to re-explain the format every time.** Presets save the shape of repeatable work: carousel length, aspect ratio, platform, caption style, moodboard direction, product-shot mode, or whatever else makes that format yours. After this, you only change the topic.

Run: **`/higgsfield-preset-create <brand> <recipe>`**  
Then generate with: **`/higgsfield-make --preset <name> "topic"`**

- **`/higgsfield-budget [path|workspace]`** — shows what you spent. Reads cost logs across runs. No args = all-time total. With a run path = just that run. With a workspace name = filter to that workspace.

### Generate content — spends credits

- **`/higgsfield-make "topic"`** — the main entry. The agent reads your topic, picks the right recipe, generates the content. Add `--brand <name>` to apply a brand profile, or `--preset <name>` to use a saved shape.

- **`/higgsfield-pattern <name> "args"`** — run a specific recipe directly when you already know which one you want. E.g. `/higgsfield-pattern moodboard --brand ben "yacht shoot"`.

Both of these always preflight first and ask before spending if the estimate is significant.

### Verify the toolkit works

- **`/higgsfield-test <1|2|3>`** — staged verification. **Stage 1 is free** (preflights only, no generation). Stage 2 spends ~12 credits (one image). Stage 3 runs a full reel.

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

## Public Repo Hygiene

Private working data is ignored:

- `brands/` — real brand profiles, source fetches, logos, people, products
- `presets/` — reusable brand-specific content shapes
- `runs/` — generated prompts, job IDs, URLs, costs, and deliverables
- media binaries and downloaded research artifacts

Do not commit generated media, private brand assets, Higgsfield auth output, or run ledgers.

## Origin

Started as a reverse-engineering project of an Instagram reel claiming "Claude autopilot for Higgsfield" via 15 agents and Playwright MCP. Frame analysis revealed it was actually a Playwright Python pipeline. v1 reproduced that. v2 replaced it with Playwright MCP (cleaner, but Higgsfield's UA sniffer blocked our browser). v3 deleted both when Higgsfield released their official CLI on 2026-05-04 — and built a real video-business toolkit on top instead. See `findings/instagram-reel-DXfKnWhDPlW-workflow.md` for the full story.

## License

MIT. The Higgsfield CLI is also MIT. Higgsfield's underlying generation models are commercial — credits cost real money. The toolkit's job is to spend them carefully on your behalf.
