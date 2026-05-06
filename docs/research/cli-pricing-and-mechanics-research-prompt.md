---
created: 2026-05-06
modified: 2026-05-06
type: research-prompt
target-tools:
  - perplexity-pro-deep-research
  - chatgpt-deep-research
  - gemini-deep-research
  - claude-research-mode
purpose: Comprehensive research on Higgsfield AI's pricing, subscription mechanics, CLI behavior, and quota/limit specifics — the things we can only learn empirically by burning credits otherwise.
---

# Deep Research Prompt: Higgsfield AI — Pricing, Subscription Mechanics, and CLI Operational Specifics

> **How to use this file:** Copy the entire "PROMPT" section below and paste into Perplexity Pro Deep Research, ChatGPT Deep Research, Gemini Deep Research, or Claude's research mode. Save the response back to `docs/research/cli-pricing-and-mechanics-research-results-<date>.md`.

## Why this prompt exists

We're building an agentic video-production toolkit (`higgs-vids`) on top of Higgsfield AI's official CLI (`@higgsfield/cli`, released 2026-05-04). The toolkit's `cost-discipline` layer was designed against rack-rate pricing — but **empirical testing on a Starter subscription on 2026-05-06 revealed that `higgs generate cost` overestimates actual billed cost by ~100×** for image models on a paid plan (160 credits estimated → 1.6 credits actually billed for a 6-image campaign).

We can't build reliable cost discipline without understanding the real subscription mechanics. We don't want to learn each model's actual subscriber-absorbed price by burning credits one model at a time. This prompt asks deep-research to gather authoritative answers in one pass.

## Existing context (don't research these — already known)

From our existing research (`docs/research/generative-media-orchestration.md`, dated 2026-04-07, pre-CLI):
- General industry pricing: Sora ~$0.05-0.10/sec, Veo ~$0.20-0.50/sec, Kling ~$0.03-0.08/sec, Higgsfield "$40/month Creator tier with estimated 500-1000 credits"
- Higgsfield's positioning as a model aggregator
- Cinema Studio, Soul, Canvas product surface

From CLI inspection (2026-05-06):
- 35+ models exposed via `higgs model list`
- 9 preset avatars in every account
- `higgs auth login` (device-code), `higgs generate cost` (rack-rate preflight), `higgs account status` (balance + plan name), `higgs account transactions` (actual billed deltas)
- `higgs workspace` for multi-context billing
- Soul ID training via `higgs soul-id create --soul-2` requires ≥5 photos

From our test run (2026-05-06, Starter plan):
- 6× soul_cinematic image generations: 160 credit preflight → **1.6 credits actually billed** (~99% absorbed)
- 1× nano_banana hero image: 100 credit preflight → ~1 credit actually billed (same ratio)
- Balance went 208 → 206.4 (full ledger in `findings/2026-05-06-starter-plan-empirical-findings.md`)

What the official CLI's open issues confirm:
- Issue #1: "Subscription-aware pricing missing in CLI" — the team acknowledges `generate cost` doesn't reflect plan absorption
- Issue #4: `soul_cast --prompt object` ignored, generates random output
- Issue #3: Windows install fails (tar `--force-local` missing)

---

## PROMPT (copy from here down)

You are conducting deep research on Higgsfield AI's pricing structure, subscription mechanics, and CLI behavior. This is for an engineering project that needs to make accurate cost predictions before submitting AI generation jobs on behalf of paid clients.

**Recency requirement:** Today's date is 2026-05-06. Higgsfield's official CLI (`@higgsfield/cli`) launched 2026-05-04. Their official agent skills package launched 2026-05-06. **Prioritize sources dated May 2026 forward.** Sources older than April 2026 may be obsolete and should be flagged as such.

**Authoritative sources to prioritize, in order:**
1. **higgsfield.ai/pricing** — the live pricing page
2. **github.com/higgsfield-ai/cli** — repo, README, MODELS.md, issues, releases, recent commits
3. **github.com/higgsfield-ai/skills** — official agent skills (the SKILL.md frontmatter contains operational hints)
4. **higgsfield.ai's official docs** — anywhere they publish API docs, FAQs, billing terms
5. **higgsfield.ai blog / changelog** — for plan tier changes and recent product updates
6. **The Higgsfield team's accounts on X/Twitter** — Alex Mashrabov (CEO), Yerzat Dulat (CTO), maintainers Kuanysh, Zhakhanger
7. **ProductHunt launch threads, Discord, Reddit /r/aivideo** — community-reported real-world costs
8. **Comparison reviews from May 2026 onward** — sites like aitools.inc, futurepedia, Tools For Humans

If primary sources don't have the answer, **say so explicitly** rather than inferring from older data.

### Section 1 — Plan tier structure (current as of May 2026)

For each plan tier currently offered:

1. **Tier name** (Free, Starter, Basic, Pro, Pro+, Enterprise — confirm actual names)
2. **Monthly USD price** (and annual if discounted)
3. **Monthly credit allocation** (raw number, distinct from "unlimited" claims)
4. **Absorption / unlimited model classes** — which specific models are "unlimited" or "absorbed" on this plan vs which still draw from the credit allocation
5. **Soul Character training eligibility** (we know Basic+ is required, but confirm exact tier and any cost)
6. **Custom avatar creation eligibility**
7. **Workspace / team seat support** — single-user or multi-seat, per-seat pricing
8. **API / CLI access** — included on all plans or gated to higher tiers?
9. **Rate limits per tier** — concurrent jobs, monthly job count caps, daily caps
10. **Output resolution caps** per tier (e.g. is 4K image gated to Pro?)
11. **Output duration caps** for video per tier (e.g. is 10s+ video gated?)
12. **Watermarks / attribution** — does the free tier watermark outputs?
13. **Commercial use rights** per tier (especially relevant for free / starter)

**Output format:** A single comparison table covering all tiers across all dimensions.

### Section 2 — Per-model pricing: rack rate vs subscriber-absorbed

For each of the following models, find:
- **Rack rate** (what `higgs generate cost` would return)
- **Subscriber-absorbed cost** by tier where confirmable (e.g. "Starter absorbs 99% of soul_cinematic" — we measured this, want to confirm and extend)
- **What surcharges apply** (resolution upgrades, audio generation, longer duration, premium quality mode)

**Image models:**
- `soul_cinematic` (Soul Cinema)
- `nano_banana` (Nano Banana)
- `nano_banana_2` (Nano Banana Pro)
- `gpt_image_2`
- `flux_2` (Pro / Flex / Max variants)
- `seedream_v4_5`
- `text2image_soul_v2`
- `marketing_studio_image`
- `cinematic_studio_2_5`

**Video models** (this is where our knowledge has the biggest gap):
- `seedance_2_0`
- `seedance1_5`
- `kling3_0`
- `kling2_6`
- `cinematic_studio_3_0`
- `cinematic_studio_video_v2`
- `marketing_studio_video`
- `veo3_1`
- `veo3_1_lite`
- `veo3`
- `minimax_hailuo`
- `wan2_7`
- `wan2_6`
- `grok_video`

**Output format:** A table per model class (image / video) with columns: model name, rack rate per generation (cite source), Free plan actual cost, Starter actual cost, Basic actual cost, Pro actual cost, surcharges that apply.

If a specific model's subscriber-absorbed cost isn't documented anywhere, note "unknown — empirical test required" and rank it by probability of being absorbed (e.g. older / cheaper models more likely fully absorbed; Veo / Sora premium models likely still credit-deducting even on Pro).

### Section 3 — Quota mechanics and overage behavior

1. When a user exhausts their monthly credit allocation:
   - Hard stop (no more generations until renewal)?
   - Auto-overage purchase (with warning)?
   - Downgrade to slower queue?
2. How is "rack rate" credit deduction calculated for users on Free vs paid tiers? (Specifically: does `generate cost` return identical numbers regardless of tier, or is it plan-aware?)
3. Credit rollover rules — do unused credits roll into the next month, or expire?
4. Is there a "topup" mechanism for paid users (buy extra credits beyond plan allocation)?
5. Workspace billing: when a workspace runs out, does it fall back to the user's personal balance? Or hard-stop?
6. Refund policy for failed generations (model returns nsfw / ip_detected / generation failure)?

### Section 4 — Soul ID specifics

1. **Plan minimum** — confirmed Basic+ from CLI error message; verify exact tier and pricing
2. **Training cost** — is it free for eligible plans, or does it consume credits?
3. **Training time** — typical wall-clock for soul-2 vs soul-cinematic
4. **Storage limits per plan** — how many Soul IDs can a user have at once?
5. **Variant differences** — `--soul-2` vs `--soul-cinematic` vs anything else; what's each best for?
6. **Photo requirements** — minimum count (5 confirmed via CLI), recommended count, quality guidelines, what causes training to fail
7. **Reuse / sharing** — can a Soul ID be shared across workspaces? Across users?
8. **Deletion** — can a Soul ID be deleted? Does deletion recover any quota?
9. **Compatible models** — which generation models accept `--soul-id` (we know `text2image_soul_v2`, `soul_cinematic` — full list?)

### Section 5 — Marketing Studio specifics

1. **Avatar types** — preset (we have 9: Jayden, Stefan, Mei, Yuna, Adriana, Clara, Maria, Sofia, Valentina) vs custom. Is the preset list expanding? Are presets free across all plans?
2. **Custom avatar creation** — is this distinct from Soul ID? What plans? What cost?
3. **Product registry** — `higgs marketing-studio products fetch --url <product-url>` scrapes web pages. What's the URL coverage (Shopify? Amazon? raw HTML? App Store?). What's the failure mode for unsupported sites?
4. **Click-to-Ad URL flow** — `higgs generate create marketing_studio_video --url <product-url> --wait` triggers a backend pipeline (fetch product → generate ad). What's the cost vs the multi-step manual approach? Is there deduplication on repeated runs against the same URL?
5. **Mode list** — confirmed from official skill: `ugc`, `tutorial`, `ugc_unboxing`, `hyper_motion`, `product_review`, `tv_spot`, `wild_card`, `ugc_virtual_try_on`, `virtual_try_on`. Any others added recently?
6. **Audio generation** — `--generate-audio true` is supported on `marketing_studio_video`. Surcharge?
7. **Resolution caps** — `marketing_studio_video` supports `480p` and `720p` — when does 1080p+ ship?

### Section 6 — API & CLI operational specifics

1. **Rate limits** by tier:
   - Concurrent in-flight jobs
   - Per-minute submission limits
   - Per-hour / per-day caps
2. **Queue priority** — do paid users get faster queue processing than free?
3. **Batch generation** — `gpt_image_2 --batch_size N` is supported. Does this multiply cost by N, or is there a batch discount?
4. **API token (`higgs auth token`) capabilities** — is the REST API a 1:1 mirror of the CLI, or are there CLI-only / API-only features?
5. **Webhook support** — can jobs notify a webhook URL on completion?
6. **Retention** — how long are job outputs (signed URLs) accessible? Are they cached server-side or do they expire?
7. **Workspace transfer** — can jobs/uploads/Soul IDs created in workspace A be moved to workspace B?

### Section 7 — Recent changes and known issues

1. **CLI release cadence** — `@higgsfield/cli` had 11 versions in days; what's the cadence and what's likely next?
2. **Open GitHub issues at higgsfield-ai/cli** — current state of:
   - Issue #1 (subscription-aware pricing in CLI)
   - Issue #2 (MCP server for Canvas workflows)
   - Issue #3 (Windows install bug)
   - Issue #4 (`soul_cast --prompt` object ignored)
3. **Roadmap signals** — what are Higgsfield publicly committing to ship next? (longer Veo durations, audio for Seedance, more Soul ID variants, etc.)
4. **Recent model additions / deprecations** — anything launched in the last week or planned?

### Section 8 — Comparative pricing (sanity check)

For the same job class — say "5-shot 25-second 9:16 vertical reel with stills + image-to-video" — what does it cost on each of:

1. Higgsfield Starter (we measured: ~1.6 credits for stills; video unknown)
2. Krea Pro
3. Magnific
4. OpenArt
5. Pika Labs
6. Runway (Standard / Pro)
7. Direct provider API (Veo via Vertex AI, Sora via OpenAI, Kling direct)

This isn't to compare value — it's to sanity-check whether Higgsfield's subscription absorption is genuinely as aggressive as we measured, or whether the rack-rate is artificially inflated to make subscriptions look better.

### Section 9 — Business / agency use cases

1. **Volume / commitment discounts** — does Higgsfield offer custom pricing for agencies producing >100 reels/month?
2. **White-label / reseller** — can an agency repackage Higgsfield as their own offering?
3. **API-only access** — is there a plan that gates out the web UI but keeps API/CLI access cheaper?
4. **Compliance / legal** — terms of service for commercial output, especially branded ad video using preset avatars (do the presets have model releases for commercial use?)
5. **Image rights** — who owns generations? Can outputs be used in paid ads, on packaging, in ToS-restricted contexts (alcohol, gambling, healthcare)?

### Output format

Your response should be one comprehensive markdown document with these sections (mirroring sections 1-9 above). For every claim, **cite the primary source inline** as `[(source)](url)`. If a source isn't datable to May 2026 or later, note its date and mark it `[STALE — verify]`.

Where data is genuinely unavailable, write "unknown — primary source did not disclose" rather than guessing. We'd rather have one accurate "unknown" than five plausible-but-wrong inferences.

Open the document with a one-paragraph summary of the most actionable findings (the 3-5 things that change how an agentic toolkit should make cost decisions). Close with a bulleted list of follow-up empirical tests we should run, ranked by cost-to-information ratio.

---

## After research returns

When the deep-research output comes back:

1. Save it as `docs/research/cli-pricing-and-mechanics-research-results-<YYYY-MM-DD>.md`
2. Reconcile against `findings/2026-05-06-starter-plan-empirical-findings.md` — does the research confirm or contradict our 99% absorption observation?
3. Update `skill/higgsfield-autopilot/references/cost-discipline.md` with:
   - Tier-aware confirmation thresholds
   - Per-model absorption table
   - Calibration recipe for first-run-on-new-plan
4. Update `skill/higgsfield-autopilot/references/model-selection-guide.md` with subscriber-cost-tier overlay (which model is genuinely cheapest *given the user's actual plan*, not just rack rate)
5. Decide whether the 3 stub patterns (`brand-shoot`, `ecom-listing`, `character-campaign`) need additional cost flags now that we know real pricing

This is the single biggest information unlock available right now. Worth getting right.
