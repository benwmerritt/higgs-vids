# Higgs Vids

A **video production toolkit** for Claude Code (and any other AI coding agent that reads markdown). Drop a brief in, get back a delivered video.

Built on the official [Higgsfield CLI](https://github.com/higgsfield-ai/cli). No browser automation, no Playwright, no MCP — just a clean CLI + agent-readable skill files.

## What it does

You talk to your AI agent (Claude Code, Codex, Gemini CLI, OpenCode). The agent reads the brief, picks a production pattern (product-reel / quick-social / multi-platform-render / brand-shoot / e-com-listing / character-campaign), runs cost preflight, executes via the `higgs` CLI, downloads assets, ffmpeg-assembles, and hands you a deliverable bundle.

## 5-minute setup

```bash
# 1. Install the Higgsfield CLI + ffmpeg
npm install -g @higgsfield/cli
brew install ffmpeg                      # or apt install ffmpeg

# 2. Sign in (opens browser for device-code)
higgs auth login

# 3. Clone this repo
git clone <this-repo-url> higgs-vids
cd higgs-vids

# 4. Open in Claude Code (Claude Desktop → Code tab → "Open" → this folder)
#    Then in the chat:
/higgsfield-init                          # verifies setup, picks workspace
/higgsfield-make briefs/example-product-reel.md
```

That's it. The agent does the rest.

## How to use it

The toolkit is **agent-driven**. You write a brief, you talk to the agent, the agent does the work. You don't run CLI commands directly (unless you want to).

## Two ways to use it

### One-off content (no setup)

A brief is a markdown file. One sentence is enough:

```markdown
# Brief: Coffee Shop Reel

Make me a 5-shot 9:16 reel for a new specialty coffee shop opening Saturday.
Warm wood and brass interior, single-origin pour-over, latte art close-ups.
Inviting, "you should come visit" vibe.
```

Drop it in `skill/higgsfield-autopilot/briefs/`, then `/higgsfield-make briefs/coffee-shop-reel.md`. Generic-but-good output, no brand context.

### Real content for a real brand (recommended for personal brands + businesses)

```bash
# One-time per brand — adaptive interview, optional channel fetch, optional Soul ID training
/higgsfield-brand-create ben

# Then run any pattern with full brand context applied
/higgsfield-make --brand ben "5 things I'd unlearn from year one of running a studio"
# → produces a 6-slide IG carousel + caption + hashtags, all in YOUR brand voice
```

The brand profile captures *who you are* — voice, audience, the specific thing that makes you non-substitutable, what you'd cringe at, your assets, your constraints. Once it's in, every future run for that brand uses it. Output stops being "AI made me content" and starts being "this is genuinely my content."

Optional: build presets for the content types you make repeatedly:
```bash
/higgsfield-preset-create ben carousel-post   # save the frame; topic varies per run
/higgsfield-make --preset ben-carousel-post "topic for this week's post"
```

The agent will:
1. Verify your setup
2. Expand the brief into a 5-shot plan
3. Run cost preflight (free) → tell you the estimated spend
4. Wait for your OK
5. Generate stills + animate them via Higgsfield
6. Download everything
7. Assemble with ffmpeg
8. Hand you `runs/<date>/deliverables/reel-final.mp4` + a cost report

## What's in the box

| Path | What |
|---|---|
| `AGENTS.md` | Agent's onboarding (read first if you're an AI) |
| `.claude/commands/` | Slash commands: `/higgsfield-init`, `/higgsfield-make`, `/higgsfield-pattern`, `/higgsfield-test`, `/higgsfield-budget` |
| `skill/higgsfield-autopilot/SKILL.md` | The agent's operating manual |
| `skill/higgsfield-autopilot/patterns/` | 6 production patterns (3 full + 3 stubs) |
| `skill/higgsfield-autopilot/briefs/` | Example briefs |
| `skill/higgsfield-autopilot/references/` | CLI cheatsheet, model selection guide, cost discipline, prompting rules |
| `skill/higgsfield-autopilot/test/` | Stage 1/2/3 verification (cost preview / single shot / full reel) |
| `docs/research/` | Background research on Higgsfield's models, prompting, orchestration |
| `findings/` | Origin story (the IG reel that inspired the project) |
| `runs/` | Per-run outputs (gitignored) |

## Patterns

| Pattern | When | Cost |
|---|---|---|
| `product-reel` | IG-ready 9:16 multi-shot reel | ~600–12,500 credits |
| `quick-social` | Single still or short clip for daily posting | ~12–600 credits |
| `multi-platform-render` | One concept, multiple aspects (9:16 + 1:1 + 16:9) | ~36–7,500 credits |
| `brand-shoot` (stub) | Product photography batches | ~30–200 credits |
| `ecom-listing` (stub) | Marketplace listing imagery | ~50–300 credits |
| `character-campaign` (stub) | Recurring talent / brand mascot | varies |

Stubs run a minimal CLI passthrough; full recipes land in v3.1.

## Cost discipline

Real money is at stake. The agent always:
1. Preflights cost (free `higgs generate cost` calls)
2. Reports the estimate
3. For >200 credits, asks explicit confirmation
4. Logs every spend to `runs/<date>/cost-log.json`

You can audit any past run: `/higgsfield-budget runs/2026-05-06-1430`. Or query workspace totals: `/higgsfield-budget Acme`.

## Multi-client / agency use

If you have multiple Higgsfield workspaces (one per client), set the active workspace before each run:

```bash
higgs workspace list                      # see options
higgs workspace set <id>                   # switch
```

The agent checks the active workspace at the start of every spending pattern. If it doesn't match what your brief implies, the agent stops and asks.

## Cross-agent compatibility

Same toolkit works in:
- **Claude Code** — slash commands native
- **Codex** — `Read AGENTS.md and execute the toolkit on briefs/X.md`
- **Gemini CLI** — same
- **OpenCode** — same

The slash commands are Claude-Code-specific UX sugar. The underlying skill is plain markdown + bash invocations of `higgs` — works anywhere.

## Test it without spending

```bash
/higgsfield-test 1                         # 0 credits — verifies cost preflight, brief expansion, model selection
```

Then when you're confident, `/higgsfield-test 2` (~12 credits, single still) and `/higgsfield-test 3` (~1k–12k credits, full reel).

## License

MIT. See `LICENSE`. Built on top of the [Higgsfield CLI](https://github.com/higgsfield-ai/cli) (also MIT). Higgsfield's underlying generation models are commercial — credits cost real money.

## Origin

This started as a reverse-engineering project of Timothée Oranger's "Claude autopilot for Higgsfield" Instagram reel (`DXfKnWhDPlW`). The reel claimed "15 agents + Playwright MCP". Frame analysis revealed it was actually a Playwright Python script pipeline. We built v1 (Python pipeline), then v2 (Playwright MCP), then deleted both when Higgsfield released their official CLI on 2026-05-04. v3 is the keeper. See `findings/instagram-reel-DXfKnWhDPlW-workflow.md` for the full story.
