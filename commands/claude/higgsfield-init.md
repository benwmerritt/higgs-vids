---
description: First-run setup and conversational onboarding for the Higgsfield video toolkit. Verifies CLI install, asks if the user has an account and signs them in if so, classifies plan tier, and ends with a four-way menu (brand setup / free moodboard demo / shape a specific idea / just explore). Idempotent — safe to run any time.
---

You are bootstrapping the Higgsfield video toolkit for this user. The first session's job is **NOT** to generate content — it's to figure out what the user wants to do, sign them in if they want that, and steer them to the right next step.

**Read `skill/higgsfield-autopilot/references/onboarding-flow.md` before responding.** That's the canonical decision tree. The steps below are the order you walk through; the *posture* and *wording* live in `onboarding-flow.md`.

## Steps

### 1. Verify the `higgs` CLI is installed AND check version

```bash
which higgs && higgs version
```

If not found, tell the user:
> Install the Higgsfield CLI:
> ```
> npm install -g @higgsfield/cli
> ```
> Then re-run `/higgsfield-init`.

Do NOT install it for them — that's a system change they should make explicitly.

**Version check:** This skill was last validated against `@higgsfield/cli@0.1.28` (released 2026-05-04). The CLI shipped 11 versions in 5 days during early May 2026, so flags and behavior may shift between minor versions. If `higgs version` reports something newer than 0.1.28:
- Note it in chat: "Note: running CLI vN.N.N (skill validated against 0.1.28). I'll watch for flag changes."
- Don't fail — just be alert. If a CLI command errors with "unknown flag" or similar, run `higgs <command> --help` to discover the current syntax.

If running an older version (≤0.1.18), warn the user that pre-launch versions had bugs and recommend updating.

### 2. Verify ffmpeg

```bash
which ffmpeg && ffmpeg -version | head -n1
```

If missing, tell them: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux). Don't install it for them.

### 3. Auth state — branch on what the user has

```bash
higgs --json account status 2>&1
```

**If this succeeds**, skip to step 4 (signed in already, just report state).

**If it fails** (no auth or expired session), ask the user — *don't assume*:

> "Looks like you're not signed in to Higgsfield yet. A few options:
> 1. **You've got an account already.** Say the word and I'll run `higgs auth login` for you. A browser will open, you sign in, we're good to go.
> 2. **You haven't made one yet.** Sign up at https://higgsfield.ai/signup. Once you've got an account, come back and I'll sign you in.
> 3. **Not ready to commit to an account yet.** Totally fine. Brand setup, moodboard ideation, and asset prep all work without a Higgsfield account. We can keep going."

**Branch on their answer:**

- **"Yes, sign me in"** → Run `higgs auth login` for them. Use Bash with `timeout: 600000` (10 min) — the CLI auto-opens the browser and the command blocks until they complete the device-code flow. Tell them what's happening before running:
  > "Running `higgs auth login` now. A browser will open — sign in there. The command returns automatically once auth completes."
  
  After it returns, re-run `higgs --json account status` to confirm. Continue to step 4.

- **"Not yet, I'll sign up"** → Don't block. Tell them: "Brand setup is free regardless. Want to start there now and re-run `/higgsfield-init` once you're signed up?" If they want to start without an account, skip to step 7 with the (a)/(b)/(c)/(d) menu noting that branches (a) and (d) are free; (b) and (c) need an account when they actually generate.

- **"No account yet, don't want one"** → Same as above. Stay conversational. The toolkit's brand and ideation work delivers real value without burning credits.

If browser doesn't auto-open in their environment (headless / SSH / WSL without browser bridge), use the fallback in `onboarding-flow.md` § 2: run in background, stream output, surface the device code line to the user, then wait.

**Never print `higgs auth token` output.** It's a credential.

### 4. Report account state + classify plan tier

If signed in, parse the JSON and report:
- Email
- Plan name (display only — don't bake into logic)
- Credit balance

Then pick the right *posture* based on balance + observed capability per `onboarding-flow.md` § 3. Tier names will change; balance and absorption are stable signals.

| Live state | What to say |
|---|---|
| Free / 8 starter credits | "Photos cost ~0.1-1.4 credits each, video burns 5-50. We can do a moodboard test for ~0 cost as a demo. Don't expect a finished reel on this — but the photo side is genuinely usable." |
| Cheapest paid (currently Starter) | "Photo absorption is around 99% on this plan — you can do 50+ generations without burning balance. **Video has zero absorption** — every clip deducts the full rack rate, so 3 video tests can drain a small balance. Photo recipes shine here. If you want to test video, expect real spend." |
| Higher tier with comfortable balance | "You've got headroom. Photo and reasonable video both work. We'll still preflight every spend." |
| Out of balance / very low | "You've got <N> credits left. Brand work, moodboard composition, and ideation are all free. Generation will need a top-up." |

### 5. List workspaces + active selection

```bash
higgs --json workspace list
higgs --json workspace status
```

If only one workspace ("Private"), say so and skip selection.

If multiple workspaces, list them and ask the user which to set as active. Then:
```bash
higgs workspace set <id>
```

(Don't pick for them — billing matters.)

### 6. Quick sanity check

```bash
higgs model list --image | head -5
higgs model list --video | head -5
```

Just to confirm the CLI can reach Higgsfield's API.

### 7. Final report — pricing caveat + the (a)/(b)/(c)/(d) menu

**Read the pricing caveat once** (per `onboarding-flow.md` § 7):

> "Heads up on pricing: Higgsfield's CLI returns rack-rate cost estimates that are usually 100× higher than what subscribers actually pay. We track real spend by reading your balance before and after every run. Those numbers are ground truth; the preflight estimates are misleading. Higgsfield is also brand new and pricing is still settling. We don't spend willy-nilly. We make spends worth it."

Then end with the four-way menu — **NOT** "go run /higgsfield-make":

> "Setup's done. What would be most useful right now?
>
> **(a) Build out brand context.** Voice, audience, visual taste, references, constraints. ~10-15 mins, free, no Higgsfield account needed. Future content lands as yours, not generic AI.
>
> **(b) Try a moodboard for ~0 cost** as a real demo of what we could make for one of your ideas. Doesn't need a full brand profile, just a vibe.
>
> **(c) You've got a specific idea.** Tell me about it and I'll work with you to shape it into something worth generating.
>
> **(d) Just exploring.** Let's chat about what you'd want to use this for. No commitment."

**Hand off based on their pick:**

| Pick | Hand off to |
|---|---|
| (a) | `/higgsfield-brand-create <name>` (or run the interview inline if slash commands aren't active) |
| (b) | `patterns/moodboard.md` — cheapest, most-presentable demo |
| (c) | Ask 2-3 shaping questions per `references/interview-craft.md`; then run `/higgsfield-make` (with `--brand <name>` if a profile exists) |
| (d) | Stay conversational. Surface possibilities. When they land on something concrete, suggest a brand sketch. |

**Don't push toward generation.** The first-session win is creative-direction capture, not credits spent.

## Don't

- Don't skip any check, even if you're confident things are set up. The point of `/higgsfield-init` is to prove the chain works end-to-end.
- Don't print `higgs auth token` output. It's a credential.
- Don't auto-install dependencies (`npm`, `brew`, `apt`). Tell the user; let them decide.
- Don't refuse to continue when the user has no Higgsfield account — brand work, moodboard ideation, and asset prep all work without one.
- Don't bake plan tier names ("Starter", "Plus", "Ultra") into decision logic — they will rename. Use balance + observed absorption.
- Don't push the user toward `/higgsfield-make` at the end. Use the (a)/(b)/(c)/(d) menu.
- Don't generate from minimal input without warning. See `onboarding-flow.md` § 5.
