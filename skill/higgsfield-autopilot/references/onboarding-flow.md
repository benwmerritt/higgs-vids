# Onboarding flow — handling a cold-start user

> Read this when: the user just ran `/higgsfield-init`, OR pinged `/higgsfield-make` (or any generation command) without a brief, brand profile, or clear creative intent.
>
> **Posture:** "I don't know you. What would you like to do?" — NOT "give me a brief and I'll generate stuff."
>
> The first session's job is to capture enough creative vision and context that the *next* generation is worth spending credits on. Generic input gets a warning. Brand work is free. Moodboards are a near-free demo path. Video on Starter gets a clear "this will burn your balance" warning.

---

## 1. Auth-state branch

Ask the user once; don't loop. Use plain language.

| User says | Agent does |
|---|---|
| "Yes, I have a Higgsfield account, sign me in" | Run `higgs auth login` for them (see § Running auth login). Wait for return. Continue to § Plan-aware posture. |
| "I don't have one yet, I want to make one" | Point at `https://higgsfield.ai/signup`. Offer to keep going without — brand setup, ideation, and asset prep all work without an account. |
| "I don't want an account yet / not ready to pay" | Stay in account-free mode. Brand setup, moodboard ideation, asset prep are all useful and free. Don't wall the experience. |
| "Not sure" / hesitates | Say: "Brand setup is free and useful regardless. Want to do that first and decide on Higgsfield later?" |

**Never refuse to continue because the user has no account.** Brand work, asset prep, and ideation deliver real value without burning a single credit.

## 2. Running `higgs auth login` from the agent

Old rule: don't run it for them. **New rule: run it after explicit user consent.** The CLI auto-opens the user's default browser; the agent's Bash call blocks until the user completes the device-code flow in browser.

**Default approach (foreground Bash, extended timeout):**

```bash
# Tell the user first:
# "Running `higgs auth login` now. A browser will open — sign in there.
#  This command will return automatically once you've completed auth."
higgs auth login
```

Pass `timeout: 600000` (10 min) when calling Bash so the user has time to complete browser auth. The CLI auto-opens the browser on macOS / most Linux / WSL. On exit, run `higgs --json account status` to verify success.

**Fallback (headless / no browser auto-open / SSH session):**

Run with `run_in_background: true`. Stream output via `BashOutput`. Find the device-code line (looks like `Open https://higgsfield.ai/device and enter code: ABC-123`), surface it to the user, then wait for the background process to exit.

**Always:**

- Tell the user what's about to happen *before* running the command.
- After auth returns, verify with `higgs --json account status`.
- **Never print `higgs auth token` output.** It's a credential.
- Never auto-install the CLI or any other dependency. `npm install -g @higgsfield/cli` stays user-driven.

## 3. Plan-aware posture

Once signed in, parse `higgs --json account status` and pick the right tone for what the user can realistically do.

> **Tier names will change.** Higgsfield has shifted naming twice already (Starter/Plus/Ultra ↔ Basic/Pro/Ultimate/Creator). Don't bake names into logic — read live state. Use balance + observed absorption (per `references/cost-discipline.md`) as the signal, not the tier label.

| Live state | Posture |
|---|---|
| **Free / 8 starter credits** | "Photos cost ~0.1-1.4 credits each, video burns ~5-50. We can do a moodboard test for ~0 cost as a real demo. Don't expect a finished reel on this — but the photo side is genuinely usable." |
| **Cheapest paid tier (currently Starter)** | "Photo absorption is around 99% on this plan — go nuts, you can do 50+ generations without burning balance. Video has zero absorption — every video generation deducts the full rack rate. 3 video generations is enough to drain a small balance. If you want post-ready content quickly, photo recipes are where this plan shines. If you want to test video, expect real spend." |
| **Higher tier with comfortable balance** | "You've got headroom. Photo and reasonable video both work. We'll still preflight every spend." |
| **Out of balance / very low** | "You've got <N> credits left. Brand work, moodboard composition (no new generation), and ideation are all free. Generation will need a top-up — Higgsfield has no auto-overage." |

The image-vs-video gap on the cheapest paid tier is the most important warning to surface. Users who try to test video three times on Starter, run out, and feel ripped off are the failure mode this prevents.

## 4. The (a) / (b) / (c) / (d) menu

After init or any cold-start ping, present a four-way branch. Use these wordings (or close variants):

> **What would be most useful right now?**
>
> **(a) Build out brand context.** Voice, audience, visual taste, references, constraints. ~10-15 mins, free, no Higgsfield account needed. Future content lands as yours, not generic AI.
>
> **(b) Try a moodboard for ~0 cost** as a real demo of what we could make. Doesn't need a full brand profile, just a vibe.
>
> **(c) You've got a specific idea.** Tell me about it and I'll work with you to shape it into something worth generating. Two or three shaping questions, then we go.
>
> **(d) Just exploring.** Let's chat about what you'd want to use this for. No commitment.

Don't push. Whichever branch the user picks, the agent stays curious about *creative direction*, not transaction speed.

## 5. The "make me a thing with no context" rule

When the user asks for output but there's no brief, no brand profile, AND no clear intent — **don't refuse, don't generate blindly either**.

Default response shape:

> "I can run that with what you've given me, but with one sentence and no brand context the result will look generic AI. Two paths:
>
> 1. We spend ~5 mins on a quick brand sketch first (voice, vibe, an asset or two) and the next generation lands way better.
> 2. You say 'just do it' and I'll generate this as a low-context test. Useful for seeing what the tool does; not useful as something you'd post."

If the user says **"just do it"** explicitly: generate. Log the warning in the run dir's `README.md` so future-self knows the output was a cold test, not a final.

If the user says **"let's do the brand sketch"**: hand off to `/higgsfield-brand-create` (or its inline equivalent — the conversational brand interview from `references/interview-craft.md`).

Three words plus "make me an Instagram post" should still produce *something* — just framed as a test, not a deliverable. Refusal kills momentum; honest framing keeps it.

## 6. Moodboard as the canonical free demo

When a user says "show me what this can do" or hesitates on brand setup, **suggest a moodboard test**.

Why moodboard:
- Image-only — absorbs to ~0 actual cost on Starter (per `findings/2026-05-06-starter-plan-empirical-findings.md`)
- Doesn't need a full brand profile — a vibe and a reference image or logo is enough
- Output is a single composed PNG (via `scripts/compose-moodboard.py`) that's actually presentable
- Uses real generation, real prompts, real composition — so it's a fair demo of the toolkit, not a toy

The moodboard pattern is at `patterns/moodboard.md`. It runs cleanly on minimal context and produces a deliverable a user can show a client without further work.

## 7. Pricing caveat — read once at init, again before any significant spend

Higgsfield's pricing is genuinely confusing right now. Acknowledge it explicitly so the user knows we're being honest, not evasive:

> "Heads up on pricing: Higgsfield's CLI returns rack-rate cost estimates that are usually 100× higher than what subscribers actually pay (we've measured ~99% absorption for image generation on the cheapest paid plan). We track real spend by reading your balance before and after every run, so the numbers in the cost log are ground truth. The preflight estimates from the CLI are misleading. Higgsfield is also brand new and pricing is still settling. We don't spend willy-nilly. We make spends worth it."

Repeat the substance of this warning before any spend the user might regret — first paid generation, first video on a small balance, first batch over 50 credits.

## 8. The image-vs-video gap (deep version)

When a user is on the cheapest paid tier and is considering video, surface this explicitly:

> "On the cheapest paid plan, photos absorb ~99% of rack rate so you can do 50+ generations without thinking about balance. Video has zero absorption. Every clip deducts the full rack rate. Three video generations is roughly enough to drain a small balance. Two practical paths:
>
> 1. Spend the cheap plan's headroom on photo content for posts (carousels, stills, moodboards). That's where this plan delivers real volume.
> 2. Test video deliberately. Pick the model carefully (`references/model-selection-guide.md`), do one short clip, see what you get, decide whether to upgrade before doing more.
>
> The trap is testing video three times, running out of balance, and feeling cheated. Don't fall into it."

## 9. Hand-off to other commands

The onboarding flow exists to figure out *which* command to invoke next. Once that's clear:

| User intent | Hand off to |
|---|---|
| (a) Brand context | `/higgsfield-brand-create <name>` (or run the interview inline if Claude Code slash commands aren't available) |
| (b) Moodboard demo | `patterns/moodboard.md` — cheapest, most-presentable demo |
| (c) Specific idea, shaped | Ask 2-3 shaping questions, then `/higgsfield-make` (with `--brand` if a profile exists) |
| (d) Just exploring | Stay conversational. Surface possibilities. Suggest brand sketch when the user lands on something concrete. |

Cold-start onboarding ends when the user has either committed to a branch or ended the session. After that, the standard SKILL.md workflow takes over.

## 10. What this flow does NOT do

- **Doesn't refuse to generate** from minimal input. Honors explicit "just do it" overrides; logs the warning.
- **Doesn't auto-install dependencies.** `npm install`, `brew install ffmpeg`, etc. stay user-driven.
- **Doesn't auto-upgrade Higgsfield plans** or recommend specific tiers — surfaces tradeoffs, lets the user decide.
- **Doesn't bake tier names into logic.** Posture is balance + capability driven, not name driven.
- **Doesn't replace cost-discipline thresholds** (50 / 200 / 1000) — those still apply for any actual spend. The pricing caveat is a *framing* layer on top.
