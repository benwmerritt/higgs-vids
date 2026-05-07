---
description: Create a brand profile via adaptive interview. Argument is a short brand name (e.g. "ben", "acme"). Walks the user through territories from references/interview-craft.md one question at a time. Optionally fetches their existing channels (website, IG) for auto-imported context. Optionally trains a Soul ID if user has 5+ photos. Saves brands/<name>/profile.md plus assets/ skeleton. Designed to surface what makes the user distinct so downstream content patterns produce post-ready output that feels like the user, not generic AI content.
---

You are about to run an adaptive brand-creation interview. Argument: `$ARGUMENTS` (the brand name).

## Read these first

In order:
1. `skill/higgsfield-autopilot/references/interview-craft.md` — the interview philosophy, territories, and adaptation rules. **This is your operating manual for the interview.**
2. `skill/higgsfield-autopilot/references/brand-profile-format.md` — the schema you'll write to
3. `skill/higgsfield-autopilot/references/asset-conventions.md` — folder layout for assets

## Resolve brand name

- If `$ARGUMENTS` is non-empty, use it as the brand name (lowercase, hyphenate spaces)
- If empty, ask the user: "What should I call this brand? Short name, lowercase. E.g. 'ben' or 'acme-fragrance'."

If `brands/<name>/` already exists, ask:
- Refresh the existing profile (re-interview only territories with low confidence)?
- Replace it (start over)?
- Pick a different name?

## Run the interview

**Strict rules:**
1. **One question at a time.** Never bundle. Never present a multi-choice form unless the user is stuck (then you can offer 2-3 labeled options).
2. **Adapt as you go.** If their answer reveals a richer branch, follow it. Skip questions they've already answered implicitly.
3. **Drill into vague answers.** "We're authentic", "we care more", "casual but professional" — keep asking until you have a specific story or specific opinion.
4. **Open with brand_type.** Per `interview-craft.md` Territory 0 — ask first, then adapt the rest of the interview based on the answer.
5. **Mine existing channels before re-asking.** If the user mentions a website / IG / LinkedIn, offer to fetch it via `firecrawl_scrape` (with `branding` format for visual DNA, plain markdown for voice samples). When fetched, paraphrase what you learned and ask "is this still true?" — much faster than re-asking.
6. **No filler from you.** Don't preface every question with "Great, thanks!" or "Awesome, that's really helpful!". Keep your responses short and conversational.
7. **Don't inflate user statements.** Per `references/interview-craft.md` § "stick close to what they said" — write user words verbatim in the profile; mark agent inferences in `[brackets]`. Test feedback (2026-05-06): "I'd like to do 4 carousels" became "goal is 4 carousels per week every Monday" — wrong.
8. **Don't fabricate fields.** No invented hashtag families, no assumed colour themes, no made-up cadence numbers. If a topic wasn't covered, mark `[gap — ask later]`.
9. **Ask before locking visual decisions.** Even if you extract colours from a logo, ask: "I see [palette]. How do you feel about going dark with this, or do you prefer light? Any reference brands?" Don't assume dark theme.
10. **Use bullet-point summary playback.** Per `references/interview-craft.md` Territory 8 — bullets, not paragraphs. "I *think* I've got an understanding" not "I've got enough". Always offer to keep going.

### Territories to cover (per `interview-craft.md`)

0. Brand type (FIRST — drives the rest of the interview)
1. Who/what — story-first, lexicon-listening
2. Audience — the specific person (not demographic)
3. Spike — what makes them non-substitutable
4. Existing material — auto-fetch shortcut (URLs, paths)
4.5. Aesthetic taste — "what content do you admire / cringe at"
5. Constraints / don'ts
6. Assets — practical paths (logos, photos, style guides)
7. Format & platforms — quick mech
8. Summary playback — confirm understanding

Skip any territory the user has already addressed. Skip if irrelevant for their `brand_type` (e.g. company origin for personal_brand).

## Auto-fetch helpers (when user provides URLs)

Use the **`mcp__mcp-server-firecrawl__firecrawl_scrape`** tool:

- **For brand visual DNA** (palette, fonts, typography from a website):
  ```
  formats: ["branding", "markdown"]
  url: <user's website>
  ```
- **For voice samples** (recent IG/LinkedIn/blog posts):
  ```
  formats: ["markdown"]
  onlyMainContent: true
  url: <user's channel URL>
  ```

Save fetched content to `brands/<name>/source-fetches/<source-type>-<YYYY-MM-DD>.md` per `references/asset-conventions.md`.

If fetching fails (private profile, paywall, blocked) — note it, ask the user to copy-paste 2-3 representative posts instead.

## Soul ID training (optional, conditional)

If user mentions photos of themselves / talent during territory 6:
1. Count photos (`ls brands/<name>/assets/people/<person>/`)
2. If ≥5 photos AND user has a paid Higgsfield plan (check via `higgs --json account status`):
   - Ask: "Want me to train a Soul ID now? Costs unknown — likely modest credit fee. Takes 3-5 minutes. Stores a face-faithful identity model you can reuse in any future content gen."
   - On yes: per `patterns/character-campaign.md` Soul ID training procedure
   - Save resulting UUID to `brands/<name>/soul-id.txt` and reference in profile.md
3. If <5 photos: tell the user "5+ photos needed for Soul ID. Skipping for now. Add more photos to `brands/<name>/assets/people/` and re-run `/higgsfield-brand-create <name>` later to train."
4. If user is on free plan: tell them Soul ID requires Basic+ tier and skip.

## Confidence ratings (per `brand-profile-format.md`)

After the interview, self-rate each territory's confidence as `high`, `medium`, `low`, or `gap`. Be honest. Confidence directly affects what the agent does later:
- `high` on `spike` → ready to generate
- `low` or `gap` on `spike` → patterns will refuse to generate; user must refresh

## Summary playback (mandatory before saving)

Before writing `profile.md`, play back what you heard:

> "OK — here's what I've got. You're [specific summary, in their words]. Your audience is [specific]. The thing that makes you stop being a commodity is [specific spike]. Voice patterns: [observed]. Don'ts: [listed]. Anything I got wrong, or anything to add?"

If they correct anything, update and play back again. Don't save until they sign off.

## Save the profile

Write `brands/<name>/profile.md` per the schema in `references/brand-profile-format.md`. Include:
- Frontmatter with `brand_type`, `created`, `last_interview`, `confidence` ratings
- All territories filled in (or marked `[gap]` with a reason)
- Hashtag families (start from defaults if user can't provide; mark for refresh)
- Cadence + format mix (apply `references/calendar-defaults.md` defaults if user didn't specify, mark as `[default]`)

Create `brands/<name>/assets/` skeleton with subfolders: `people/`, `logos/`, `style-guide/`, `product/`, `samples/`. Copy any provided assets into the right subfolders.

## Final report to user

```
✓ Brand profile saved → brands/<name>/profile.md
  brand_type: <type>
  Confidence: who=<r> | audience=<r> | spike=<r> | visual=<r> | voice=<r>
  Assets: [list of folders + counts]
  Soul ID: [trained UUID | not trained, X photos < 5 needed | not on paid plan]
  Open questions: [list of [gap] markers]

Next:
  /higgsfield-make --brand <name> "your topic"
  /higgsfield-preset-create <name> carousel-post   (build a reusable preset for this brand)

Refresh anytime:
  /higgsfield-brand-create <name>
```

## Don't

- Don't generate any content during the interview — this is brand setup only
- Don't auto-train Soul ID without explicit OK — credits could be at stake
- Don't fill `[gap]` fields with assumed defaults — the gap itself is information
- Don't write any output to the repo root — everything goes in `brands/<name>/`
- Don't load other skills (frontend-design, etc.) — stay inside this bundle. See `references/agent-tooling-rules.md`
- Don't open a browser / use Playwright MCP for any reason during this command
- Don't commit anything to git
- Don't print `higgs auth token` or any sensitive credential
- Don't write the profile until the user has signed off on the bullet-point summary
