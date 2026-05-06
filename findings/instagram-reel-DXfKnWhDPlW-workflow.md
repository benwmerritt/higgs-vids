# Findings: Instagram Reel DXfKnWhDPlW — "Claude Code × Higgsfield Autopilot"

> Source-of-truth doc decoded from Timothée Oranger's IG reel pitching a Claude-Code-driven Higgsfield workflow. This is the spec the `higgsfield-autopilot` skill is built against.

## 1. Source

| Field | Value |
|---|---|
| URL | https://www.instagram.com/reel/DXfKnWhDPlW/ |
| Creator | **Timothée Oranger** (visible in terminal username `timotheeoranger@macbook-p…`, frame 3) |
| Duration | 46 seconds |
| Captured | 2026-05-05 |
| Caption hook | "Comment 'CODE' to get the full CLAUDE AUTOPILOT SYSTEM in your DMs" — gated content, prompts/agents not shown |
| Tagged | `@higgsfield.ai`, `@claudeai`, hashtags `#claudecode #higgsfield` |

**Local artefacts** (in `downloads/`):
- `instagram_reel_DXfKnWhDPlW.mp4` — original video (gitignored)
- `instagram_reel_DXfKnWhDPlW.txt` / `.srt` / `.vtt` / `.tsv` / `.json` — Whisper transcripts
- `instagram_reel_DXfKnWhDPlW.description` — IG caption
- `instagram_reel_DXfKnWhDPlW.info.json` — full IG metadata
- downloaded frame samples — sampled every 2s during the original investigation

## 2. Voiceover claims vs observed reality

The voiceover sells a clean 4-step setup. The frames show something more nuanced.

| Voiceover claim | What frames show |
|---|---|
| "Drop **this line of code** in your terminal to install the Playwright MCP" | Frame 3: terminal at `~/.../CLAUDE COD…` typing `claude mcp add -s user …`. The `-s user` scope means it's a *standing* install across all his projects, not project-local. |
| "Paste these instructions to install **15 creative agents**" | Frame 9 is a visual metaphor (15 glowing humanoid figures around a car). The actual implementation in frame 11 is **not** sub-agents — it's a numbered Python script pipeline. |
| "Cloud Code writes the script, builds the storyboard, generates every asset on Higgsfield, and assembles the final video" | Confirmed by frames 5, 7, 11, 17, 19. Includes a real Higgsfield Soul Cinema generation visible mid-flight. |
| "Cloud Code runs on **autopilot**" | Partially. Frame 11 shows "1 shell still running" / "↓ to manage" — Claude Code's background-shell feature, manually monitored. Not unattended. |

**Bottom line:** The marketed "15 agents" framing is a metaphor. The real architecture is **one Claude Code session driving numbered Python scripts that drive Playwright that drives Higgsfield**.

## 3. Decoded architecture

### Environment (frame 3)
- **Username:** `timotheeoranger@macbook-p…` (macOS)
- **CLI:** Claude Code v2 — `Claude Code v2`
- **Model:** `Opus 4.6 (1M c…)` — Opus 4.6 with 1M context window
- **Working dir:** `~/.../CLAUDE COD…` inside a `CONTENT CREATION` parent folder
- **First command typed:** `claude mcp add -s user …` — installs Playwright MCP at user scope

### The actual pipeline (frame 11)
The terminal during execution shows:

```
.../projects/editorial-capsule-car" && 02-find-soul.py 2>&1
in the background (↓ to manage)
e. Je regarde le browser naviguer et le résultat.
[…]4s · 1 shell still running
[…] cinema page via […]
[…]ts/editorial[…]/03-login.py
.../editorial-capsule-car" && 03-login.py 2>&1
in the background (↓ to manage)
[…]
.pl…
ll subsequent
t time
pathlib import Path
playwright.sync_api import sync_playwright
```

**Inferences:**
- Project dir: `editorial-capsule-car` (one project per campaign — implied)
- Numbered Python scripts: `02-find-soul.py`, `03-login.py` are explicitly visible. The numbering pattern strongly implies `01-…`, `04-…`, `05-…` exist for the other stages.
- Each script run is **`<script> 2>&1` in the background**, managed via Claude Code's down-arrow shell manager.
- Imports visible: `from pathlib import Path`, `from playwright.sync_api import sync_playwright` — **synchronous Playwright Python API**, not async, not the MCP, direct script-to-browser.
- Comments are in **French** ("Je regarde le browser naviguer et le résultat" — "I'm watching the browser navigate and the result"). The script library is bilingual / French-authored.
- "Soul Cinema page via …" — the `02-find-soul.py` script's job is to navigate to Higgsfield's Soul Cinema page.

### Inferred script roles

| Script | Job (inferred) | Evidence |
|---|---|---|
| `01-…` (login) | Open browser, sign in, persist auth | Standard pattern; required before 02 can navigate |
| `02-find-soul.py` | Navigate to Soul Cinema page, verify session | Visible in frame 11 |
| `03-login.py` | Likely *re*-login or a per-run session refresh — naming is suggestive but not definitive | Visible in frame 11 (filename ambiguous; may be a misnomer for a sub-action) |
| `04-…` (generate) | Submit prompt, wait for batch | Implied by workflow |
| `05-…` (assemble) | ffmpeg or similar to join shots | Implied by "assembles the final video" voiceover |

**Caveat:** Filename `03-login.py` is unexpected if `01` is the login. Two non-exclusive readings: (a) Oranger uses `03-login.py` as a per-job session-refresh, with the *initial* login being a manual or earlier step; (b) the numbering is non-sequential and reflects iteration history, not pipeline order. Our skill standardises on a clean monotonic numbering instead of replicating his oddity.

## 4. Higgsfield generation profile

### Model (frame 17)
- **Model:** `Soul Cinema` (visible bottom-left of generation panel)
- **Aspect ratio:** `9:16` (vertical, reels-native)
- **Mode toggle:** `On` (Boost — labelled "Boost speed" in the upgrade banner above)
- **Batch size:** `4/4` (4 generations per prompt — burning the full batch)
- **Free credits visible:** `…249 free gens left` (so this is a paid account, not free tier)
- **Action:** "Generate" button (green, bottom-right)

### Sample expanded prompt (frame 17, partially visible)
```
[…] aerodynamic shape with a rosy-tinted front grille, and it lacks visible
wheels, heightening the space-age allure. The composition is
centered and low to the ground, with the subject dominating the
foreground. The expansive backdrop features a flat, sandy desert
landscape, scattered desert scrub, and silhouetted foothills. The sky
is rendered in a painterly gradient of sunset pink, purple, and blue
hues, suffusing the scene with soft, diffused dusk lighting that casts
no harsh shadows and wraps the models' face with a gentle glow.
Dominant colors include pastel mauve, off-white, blush, and sandy
beige. The photograph exhibits deep focus on the model and car […]
```

**Prompt structure detected:**
1. Subject + form ("aerodynamic shape with a rosy-tinted front grille, lacks visible wheels")
2. Composition ("centered and low to the ground, subject dominating the foreground")
3. Environment ("flat, sandy desert landscape, scattered desert scrub, silhouetted foothills")
4. Sky / lighting ("painterly gradient of sunset pink, purple, blue; soft diffused dusk")
5. Palette ("pastel mauve, off-white, blush, sandy beige")
6. Optical ("deep focus on the model and car")

This matches the **Subject → Scene → Action → Camera Feel → Lighting → Style** structure documented in `docs/skills/skill-higgsfield-shot-designer.md`. The skill's prompt-craft rules apply directly to Soul Cinema.

### Final output evidence (frames 1, 7, 13, 17, 19, 21)
- Retro-futuristic capsule car (white, aerodynamic, no visible wheels, red glowing tail strip)
- Desert sunset settings, mountains backdrop
- Bella-Hadid-lookalike model in pale-yellow silk halter dress
- Kinetic shots: wheel close-up with red glow rings, motion blur, dust trails
- Project tab visible in frame 7: "Retro-futuristic editorial fashion campaign"

## 5. Brief format observed

Frame 15 shows the user input typed into Claude Code (or a similar text field):

> **`va me faire une campagne éditorial retro futuristique`**
> ("you'll make me a retro-futuristic editorial campaign")

Observations:
- **Conversational French** — no shot list, no JSON, no specs
- **One sentence** — under 10 words
- **Implicit aspect/duration/style** — the agent infers everything from the brief plus the project context

This is the *input* shape the autopilot has to accept.

## 6. Replication checklist

To rebuild this workflow we need:

1. **Playwright Python (sync API)** — confirmed by frame 11 import. `pip install playwright && playwright install chromium`.
2. **Persistent auth** — Higgsfield login must survive across script invocations. Standard pattern: `storage_state.json` saved by a one-time headed login, loaded by every subsequent script.
3. **Centralised selectors** — Higgsfield's UI is fast-moving. All DOM selectors in one library file so a redesign is a single-point fix.
4. **High-level page actions** — `open_soul_cinema()`, `submit_prompt(text, aspect, batch, boost)`, `wait_for_batch(n)`, `download_asset(id, dest)` — so the numbered scripts stay readable.
5. **Numbered, single-purpose scripts** — matches Oranger's pattern, lets Claude Code orchestrate via background shells.
6. **A brief-expansion step** — turns the conversational one-liner into a JSON shot list of 3–8 shots, each with a Soul-Cinema-formatted prompt.
7. **ffmpeg** — for final assembly. No fancy library; subprocess is fine.
8. **Per-shot directories** — `runs/<date>/shot-NN/` holding the 4 batch outputs + a chosen-best symlink.

## 7. Open questions (resolve during implementation)

- **Headless vs headed.** Does Higgsfield throttle or block headless Chromium? Default to **headed** for reliability; add headless flag once verified safe.
- **Selector stability.** The Higgsfield app likely uses generated CSS classes. Prefer ARIA roles, `data-testid` (if present), and visible text matchers in `lib/selectors.py`.
- **Batch-completion detection.** How does Soul Cinema signal "all 4 done"? Polling the History grid for 4 new entries? A toast? A status badge? Resolve during 03 implementation.
- **Boost toggle persistence.** Is "Boost on" a per-prompt or per-session setting? If per-session, set it once in `02-open-soul-cinema.py`; if per-prompt, set in `03-generate-asset.py`.
- **Asset download path.** Does Soul Cinema expose direct download URLs, or do we screenshot/canvas-extract from the History view? Resolve during 04 implementation.
- **Credit cost per Soul Cinema 9:16 4/4 batch.** Need to capture this for the `--dry-run` cost estimator. Surface it in `selectors-cheatsheet.md` after first real run.

## 8. What we deliberately don't replicate

- **The Playwright MCP install.** Oranger installs it (`claude mcp add -s user …`) but the *actual work* in frame 11 is done by direct `playwright.sync_api`. The MCP is dead weight for our pipeline; skipping it removes a dependency and keeps the skill cross-agent compatible (Codex/OpenCode don't have MCP equivalents in the same shape).
- **The "15 agents" framing.** It's a marketing visual. We use one Claude Code session + a clean script library — same outcome, less cognitive overhead.
- **French-only comments.** Our library is English-commented for portability. The brief itself can stay any language; we test with both English and French.
