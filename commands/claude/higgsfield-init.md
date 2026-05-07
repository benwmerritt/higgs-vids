---
description: First-run setup for the Higgsfield video toolkit. Verifies CLI install, runs auth login if needed, lists workspaces, helps select active workspace, reports balance. Idempotent — safe to run any time to confirm setup.
---

You are bootstrapping the Higgsfield video toolkit for this user. Walk them through the minimum setup so subsequent `/higgsfield-make` calls work cleanly.

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

### 3. Check auth state

```bash
higgs --json account status 2>&1
```

If this fails (no auth), tell the user:
> Sign in to Higgsfield:
> ```
> higgs auth login
> ```
> A browser will open for device-code auth. Sign in, then re-run `/higgsfield-init`.

Do NOT run `higgs auth login` for them — it's interactive and needs their browser.

### 4. Report account state

If auth works, parse the JSON and report:
- Email
- Plan
- Credit balance

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

### 7. Final report

Tell the user:
- ✓ Setup is complete
- Their balance
- Their active workspace
- Suggest next: `/higgsfield-make briefs/example-product-reel.md` (or any brief in `skill/higgsfield-autopilot/briefs/`) to do a first run

## Don't

- Don't skip any check, even if you're confident things are set up. The point of `/higgsfield-init` is to prove the chain works end-to-end.
- Don't print `higgs auth token` output. It's a credential.
- Don't auto-install dependencies. Tell the user what to install; let them decide.
