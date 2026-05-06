<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# You are conducting deep research on Higgsfield AI's pricing structure, subscription mechanics, and CLI behavior. This is for an engineering project that needs to make accurate cost predictions before submitting AI generation jobs on behalf of paid clients.

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

### Section 6 — API \& CLI operational specifics

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
    - Issue \#1 (subscription-aware pricing in CLI)
    - Issue \#2 (MCP server for Canvas workflows)
    - Issue \#3 (Windows install bug)
    - Issue \#4 (`soul_cast --prompt` object ignored)
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

Higgsfield’s current public documentation is still quite thin and partially inconsistent with third‑party write‑ups, so your agent will not be able to get perfectly precise, plan‑aware costs purely from official sources as of 2026‑05‑06. The most important engineering implications are: (1) the CLI’s `generate cost` endpoint reports rack‑rate credits and is **not yet subscription‑aware**, so it cannot tell you which generations will actually be “unlimited” for a given plan; (2) subscription credits are fixed per billing cycle with **no rollover** and separate top‑up packs that appear to expire after ~90 days; (3) Soul ID training is gated to paid plans and requires a non‑trivial photo set but has **no documented per‑training fee**; and (4) Marketing Studio and Seedance‑based video are among the heaviest credit consumers, while selected image and legacy video models can be effectively “absorbed” on Plus/Ultra‑style plans, though the precise absorption rules are only partially documented and sometimes only observable via the web UI rather than the CLI.[^1][^2][^3][^4][^5]

***

## Section 1 — Plan tier structure (current as of May 2026)

### 1.1 What we can say with high confidence

Higgsfield’s own pricing narrative currently centers on **three annual subscription tiers** — Starter, Plus, Ultra — each with fixed monthly credits and some “unlimited” model entitlements. However, this official explainer was published on 2026‑04‑20, so its exact numbers should be treated as **[STALE — verify]** as of May 2026. The public `/pricing` landing page at `higgsfield.ai/pricing` currently only shows marketing copy and footer copyright, not a detailed feature/credit table, which forces us to rely on the April explainer plus third‑party write‑ups for numerical details.[^6][^2][^1]

Third‑party May‑2026 reviews (notably a Scribe guide from 2026‑05‑05) describe a **five‑tier structure** — Free, Basic, Pro, Ultimate, Creator — with monthly and annual pricing and credit allocations that do **not** line up perfectly with Higgsfield’s own Starter/Plus/Ultra article, suggesting either a recent renaming or plan‑matrix experiments by region. Because Higgsfield’s own UI is not directly inspectable here and official docs are lagging, the safest stance for your agent is: **treat exact tier names and credit counts as volatile**, and read the current plan/credits in real time via `higgsfield account status` for the authenticated user, rather than hard‑coding any of the tables below.[^7][^1]

### 1.2 Consolidated tier comparison table (best‑effort, with stale flags)

The table below merges the **official April 2026 article** and **early‑May third‑party summaries**; any figure sourced from ≤2026‑04 is annotated “[STALE — verify]” per your requirement.

> **Important:** Use this table for qualitative behavior (e.g., “Ultra has one unlimited video model”) rather than exact numbers; always confirm actual plan, credits, and concurrency via `higgsfield account status` and in‑app UI at runtime.[^8][^7][^6][^1]


| Dimension | Free | Starter (official article) | Plus (official article) | Ultra (official article) | “Basic” (Scribe) | “Pro” (Scribe) | “Ultimate” (Scribe) | “Creator / Business / Enterprise” |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Tier name (UI) | “Free” in most reviews.[^7][^6][^9] | Starter.[^1] | Plus.[^1] | Ultra.[^1] | Basic (3rd‑party).[^7] | Pro (3rd‑party).[^7] | Ultimate (3rd‑party).[^7] | Creator / Business / Enterprise (3rd‑party, custom).[^7][^6][^10][^11] |
| Monthly price (annual billing) | 0 USD (all sources agree).[^7][^6][^9] | 15 USD/mo [STALE — verify].[^1] | 39 USD/mo [STALE — verify].[^1] | 99 USD/mo [STALE — verify].[^1] | 9 USD/mo [STALE — verify].[^7] | 17.40 USD/mo (annual) [2026‑05‑05].[^7] | 24.50 USD/mo (annual) [2026‑05‑05].[^7] | 49.80–125 USD/mo (annual), or 119–149 USD/mo monthly for Creator; Business per‑seat; Enterprise custom [STALE — verify].[^7][^10][^6][^11] |
| Credits/month (subscription) | 5–10/day or ~10/mo in older guides [STALE — verify].[^7][^6][^9] | 200 credits/month [STALE — verify].[^1] | 1,000 credits/month [STALE — verify].[^1] | 3,000 base (scalable to 9,000) [STALE — verify].[^1] | 150 credits/mo [STALE — verify].[^7][^9] | 600 credits/mo [2026‑05‑05 Scribe, but not in official doc].[^7] | 1,200 credits/mo [2026‑05‑05 Scribe].[^7] | 6,000 credits/mo (Creator) or 1,500/seat (Business) [STALE — verify].[^7][^6] |
| Monthly credit refresh / rollover | Credits allocated at cycle start; unused credits do **not** carry over; unused balance forfeited when subscription ends.[^1][^5][^9] | Same as Free; credits reset each month; no rollover.[^1][^5][^9] | Same.[^1][^5][^9] | Same.[^1][^5][^9] | Same per third‑party guides (no rollover) [STALE — verify].[^5][^9] | Same.[^5][^9] | Same.[^5][^9] | Same; Business uses pooled credits per seat [STALE — verify].[^6] |
| “Unlimited” / absorbed image models | None documented; free tier generally limited to a handful of models.[^7][^6][^9] | None called out in official article; Starter appears to be pure credit‑based.[^1] | 365‑day **unlimited image access** to Seedream 5.0 Lite, Flux.2 Pro, GPT Image, Seedream 4.5, Nano Banana (and possibly Nano Banana 2 2K) [STALE — verify].[^1][^6] | Same as Plus, plus **4K unlimited for Seedream 4.5** and 2K unlimited for Nano Banana Pro, with higher free Soul/V2 \& Cinema quotas [STALE — verify].[^6][^1] | Third‑party guides mention “unlimited Seedream 4.0 and Nano Banana” on Basic [STALE — verify].[^7] | Extended unlimited for more image models [STALE — verify].[^7][^6] | 365‑day unlimited Nano Banana Pro and higher‑res unlimited for Seedream and Soul [STALE — verify].[^7][^6] | Ultra‑plus unlimiteds plus team‑level access; specifics vary by contract (Enterprise).[^7][^6] |
| “Unlimited” / absorbed video models | None.[^7][^6] | None.[^1] | No explicit unlimited video, but higher concurrency for Seedance/Kling etc. [STALE — verify].[^1] | **One 365‑day unlimited video model selectable** from Nano Banana 2, Wan 2.6, Seedance 1.5 Pro, or Kling 2.6 [STALE — verify].[^1] | No unlimited video.[^7][^6] | No unlimited video.[^7][^6] | Some guides claim “unlimited Kling 3.0 access” on Ultra/upper tiers, but this is 3rd‑party and older [STALE — verify].[^6] | Enterprise deals can negotiate bespoke unlimited pools; not publicly documented.[^7] |
| Soul Character (Soul ID) training | Not allowed; higgsfield‑soul‑id SKILL explicitly says “requires paid plan (Basic+).” | Allowed (as entry paid tier) per SKILL text (“Basic+”) — exact plan label mapping Free/Starter/Basic is ambiguous.[^3] | Allowed.[^3] | Allowed.[^3] | Scribe: Basic at 9 USD includes Soul ID character training access [2026‑05‑04].[^3] | Same.[^3] | Same, with higher free Soul uses.[^6][^3] | Business/Creator plans explicitly market “shareable Soul IDs” in workspace [STALE — verify].[^6] |
| Custom avatar creation (Marketing Studio) | Avatars exist in UI; no official restriction statement; likely limited or watermarked.[^12] | No hard doc; Marketing Studio intro simply says “choose from 40+ avatars or create your own in seconds.”[^12] | Same.[^12] | Same.[^12] | Third‑party articles treat custom avatar creation as part of Pro+; not confirmed in docs [STALE — verify].[^6][^13] | Same. | Same. | Enterprise likely gets custom casting pipelines; not documented. |
| Workspace / team seats | Single‑user only.[^6][^11] | Single user.[^1][^6] | Single user.[^1][^6] | Single user or small team; no explicit seats.[^1][^6] | Single.[^7][^6] | Single.[^7] | Single or small team; concurrency increased.[^7] | Business: minimum 2 seats with pooled credits; Enterprise: custom seats and SSO [STALE — verify].[^6][^1] |
| API / CLI / MCP access | CLI and MCP server appear to work as long as account has any plan and credits; no official gating of API/CLI to higher tiers.[^14] | Same; pricing page and CLI docs say CLI uses “same credit system as platform.”[^14] | Same.[^14] | Same.[^14] | Third‑party guides sometimes say API available only from Pro+; **not** confirmed in any official doc [STALE — verify].[^15][^13] | Same. | Same. | Enterprise plans can include dedicated APIs and SLAs.[^7] |
| Rate limits (concurrent jobs) | Not clearly documented; likely 1–2 concurrent jobs.[^6][^1][^9] | Up to **2 video and 4 image generations in parallel** [STALE — verify].[^1] | Up to **6 video and 8 image generations in parallel** [STALE — verify].[^1] | Up to **8 video and 8 image generations in parallel** [STALE — verify].[^1] | Various reviews quote similar numbers; all pre‑May and inconsistent [STALE — verify].[^7][^6][^9] | Higher concurrency, but not formally specified.[^7] | Higher again.[^7][^16] | Business: up to 16 video and 16 image jobs in parallel team‑wide [STALE — verify].[^6] |
| Output resolution caps (by plan) | Often capped to 720p for video on free [STALE — verify].[^17][^9] | No explicit cap per tier; resolution is **per‑model** in MODELS.md (1K/2K/4K images, 480p–1080p video), not gated by plan in docs. | Same; some older guides say 4K unlocked only higher tiers [STALE — verify].[^6][^17] | Same; Ultra adds some unlimited 4K usage on Seedream.[^6] | 4K only partly available on higher plans per older comparisons [STALE — verify].[^6][^17] | Same. | Same. | Enterprise can negotiate 4K / longer durations, but no public matrix. |
| Output duration caps (by plan) | Not per plan; durations are per‑model: typically 4–12 seconds for Seedance/Kling/Wan and 4–8 seconds for Veo; see MODELS.md. | Same. | Same. | Same. | Third‑party “Higgsfield 2.0” guides mention 8s vs 16s clip caps across Free/Creator/Studio; these refer to an older “Higgsfield 2.0” video product and should be treated as **[STALE — verify]**.[^17] | Same. | Same. | Enterprise can get longer durations via custom contracts; not documented. |
| Watermarks / attribution | Reviews consistently report **watermarks on free output**, removed on paid tiers; no explicit statement in current docs [STALE — verify].[^7][^6][^16][^13] | No watermark (per reviews).[^7][^13] | No watermark.[^7][^13] | No watermark.[^7][^13] | No watermark.[^6][^13] | No watermark. | No watermark. | No watermark. |
| Commercial use rights | Terms of Use state that Higgsfield does not claim ownership of inputs or outputs and does **not restrict commercial use** of outputs, subject to ToS and legal compliance.[^18][^19] | Same; no separate “commercial license” gating by plan.[^18][^19] | Same.[^18][^19] | Same.[^18][^19] | Third‑party blogs sometimes say “commercial rights unlock at Basic/Pro”; that conflicts with ToS and should be treated as **[STALE — verify]**.[^20][^13] | Same. | Same. | Enterprise adds additional contractual assurances/SLA but not different IP ownership.[^18][^19] |

**Key engineering takeaway for Section 1:** rather than baking any of these numeric tables into your agent, you should (a) read the active plan and remaining credits via `higgsfield account status --json`, (b) assume **no rollover**, (c) treat unlimited entitlements as **plan‑ and model‑specific exceptions** that you cannot infer from the CLI today, and (d) expect that Higgsfield may rename or reshuffle tiers again — so your integration should always rely on *capability checks* (models available, credit balance, CLI errors) instead of tier‑name checks.[^5][^9][^1]

***

## Section 2 — Per‑model pricing: rack rate vs subscriber‑absorbed

### 2.1 General constraints

Higgsfield does **not** publish a full per‑model credit cost table anywhere in current official docs; pricing is described qualitatively (“cost depends on model, duration, resolution”) with a few examples in older FAQ content. The CLI supports `higgsfield generate cost <model> ... --json`, which returns a `credits` integer representing **rack‑rate base model cost**, but as of CLI v0.1.26–0.1.28 this output is **not subscription‑aware** and does not reflect whether the user’s plan would actually treat the request as “unlimited.”[^9][^5]

The only hard numbers we have for specific models that are clearly dated May 2026 are from **GitHub issue \#1** filed on 2026‑05‑04 against the official CLI, where a user shows example responses for three image models on a Plus plan:

```json
{ "credits": 100 }   // seedream_v5_lite --prompt test --json
{ "credits": 100 }   // seedream_v4_5  --prompt test --json
{ "credits": 150 }   // nano_banana_flash --prompt test --json
```

These values can safely be treated as up‑to‑date **rack rates** for those models at default parameters as of CLI 0.1.26, but they do **not** tell you the effective cost after subscription entitlements.

Third‑party blogs provide ballpark per‑model costs (e.g. Kling 3.0 ~6 credits; “premium” models 40–70 credits; Kling 2.5 Turbo 10s 1080p ~12 credits), but almost all such posts are from 2025 or early 2026 and contradict each other, so they should be treated strictly as **[STALE — verify]** heuristics.[^21][^22][^23]

### 2.2 Image models table (limited reliable data)

Given these constraints, the table below only marks rack‑rate values where we have direct 2026‑05 evidence (CLI issue) and otherwise leaves them “unknown — primary source did not disclose.” Subscriber‑absorbed behavior is inferred from the April pricing explainer and older reviews, so all such absorption rows are annotated [STALE — verify].


| Model | Rack‑rate per generation (credits) | Free plan actual cost | Starter / “Basic” cost | Plus / “Pro” cost | Ultra / Ultimate / Creator cost | Surcharges / notes |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `soul_cinematic` (Soul Cinema) | Unknown — CLI examples not published; official docs silent. | Likely full rack‑rate credits; no unlimited.[^6][^9] | Same; no doc of absorption.[^6][^1] | Some older guides mention “Soul Cinema free gens” on Plus but do not give a per‑call credit cost [STALE — verify].[^6] | Ultra/Creator may include **free quotas** of Soul V2 \& Cinema (e.g. 5k–10k free gens/year), after which rack‑rate applies [STALE — verify].[^6] | 4K resolutions and higher quality likely burn more credits, but no official multipliers published; expect credit use to scale with resolution.[^5][^9] |
| `nano_banana` (Nano Banana) | Unknown; older docs say “cheap, basic image” but no numeric.[^5] | Full credits; no unlimited.[^7][^9] | Some guides say Nano Banana is “unlimited” on Basic [STALE — verify].[^7] | **365‑day unlimited Nano Banana** on Plus/Ultra according to pricing explainers [STALE — verify].[^6][^1] | Same but at higher resolutions and additional perks.[^6] | Using `--resolution 2k/4k` likely increases cost even if base 1K is absorbed.[^5] |
| `nano_banana_2` (Nano Banana Pro) | Unknown; premium variant; no official rack rate. | Full credits. | Full credits, though some recent marketing mentions “99% absorbed” on certain promos — not documented.[^7][^6] | Some blogs mention “2K unlimited for Nano Banana 2” on Plus [STALE — verify].[^6] | Ultra: “2K unlimited for Nano Banana Pro” [STALE — verify].[^6] | 4K resolution almost certainly surcharged even on plans with some unlimited access.[^6][^5] |
| `nano_banana_2` vs `nano_banana_flash` | `nano_banana_flash` appears as “Nano Banana 2”; CLI issue shows 150 credits rack rate at default params. | Same pattern as above. | Same pattern. | “Unlimited Nano Banana 2” likely maps to `nano_banana_flash` at 1K.[^1] | Same. | Treat 150 credits as **upper bound**; effective cost may be discounted under some promos. |
| `gpt_image_2` | Unknown; not in any cost snippets. | Full rack‑rate credits; no “unlimited GPT” mentioned.[^1] | Same. | Plus/Ultra: 365‑day unlimited GPT Image in some older pricing tables [STALE — verify].[^6][^1] | Same. | Cost likely increases with `--quality` and `--resolution` (1K → 2K → 4K) per older FAQ; no exact factors given.[^5] |
| `flux_2` (Pro / Flex / Max) | Unknown; older docs gave example “Flux Kontext Max = 1.5 credits” but pre‑2025 [STALE — verify].[^5] | Full credits. | Full credits. | 365‑day unrestricted Flux.2 Pro at 1K on Plus and above [STALE — verify].[^6][^1] | Same plus higher‑res unlimited.[^6] | Model variant `--model pro/flex/max` likely changes credits; no published matrix.[^5] |
| `seedream_v4_5` | **100 credits** per generation at default settings from CLI example (Plus plan; plan‑agnostic). | 100 credits (no unlimited).[^7] | Same. | Likely absorbed on Plus/Ultra as part of Seedream unlimited pack [STALE — verify].[^6][^1] | Same plus 4K unlimited Seedream 4.5 on Ultra [STALE — verify].[^6] | `--quality high` may increase cost vs `basic`; no numbers given. |
| `text2image_soul_v2` | Unknown; not explicitly priced. | Full credits; some free Soul gens via promos [STALE — verify].[^6][^9] | Full credits plus occasional free Soul quotas. | Plus/Ultra: 3k–10k free Soul V2/Cinema generations per year [STALE — verify].[^6][^1] | Same with higher quotas.[^6] | Soul ID training itself may or may not consume credits; **no official statement**. |
| `marketing_studio_image` | Unknown. | Full credits; no unlimited.[^12] | Full credits. | Same; not part of image‑unlimited packs described in older docs.[^6] | Same. | Higher resolutions (2K, 4K) permitted; likely surcharged but not documented.[^12] |
| `cinematic_studio_2_5` | Unknown; premium cinematic stills; no pricing doc. | Full credits. | Full credits. | Full credits. | Full credits. | Higher `--resolution` tiers (2K/4K) presumably costlier. |

For other image models in the MODELS.md list — `seedream_v5_lite`, `z_image`, `openai_hazel`, `grok_image`, `kling_omni_image`, `image_auto`, etc. — there is **no up‑to‑date public per‑model pricing**, and absorption status is only partially hinted at via older pricing charts (e.g., “Seedream 5.0 Lite unlimited on Plus”) that should be treated as **[STALE — verify]**.[^6][^1]

### 2.3 Video models table (highly underspecified)

For video, the gap is even larger. No official source lists exact credit cost per second or per model for the Higgsfield‑hosted Seedance/Kling/Wan/Veo integrations in 2026‑05; we only have:

- Old 2025 Reddit \& blog posts giving example costs for Kling 2.5, Seedance Pro, etc. [STALE — verify].[^22][^23]
- Third‑party Veo pricing commentary on other platforms (Freepik, Vertex), **not** specific to Higgsfield.[^24][^25]
- The April 2026 official article saying Ultra lets you pick one of Nano Banana 2 / Wan 2.6 / Seedance 1.5 Pro / Kling 2.6 as a **365‑day unlimited** video model.[^1]

Given this, any numeric values you may have empirically measured (e.g., “Kling 3.0 costs ~6 credits”) are **not confirmable** from primary sources and must be treated as **integration‑specific heuristics** that you calibrate in your own logging layer.[^23][^21][^22]

Below is a qualitative table:


| Model | Rack‑rate credits (official) | Free | Starter / Basic | Plus / Pro | Ultra / Ultimate / Creator | Notes on absorption \& surcharges |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `seedance_2_0` | Unknown; no published pricing. | Full credits; heavily constrained by daily free credits.[^6][^9] | Full credits. | Full credits. | Full credits; **not** listed as Ultra’s unlimited video model (only Seedance 1.5 Pro is).[^1] | Surcharges likely for 1080p vs 720p, longer `--duration`, and higher‑end `--mode`/`--genre`, but no official matrix.[^5] |
| `seedance1_5` (Pro) | Unknown. | Full credits. | Full credits. | Full credits by default. | Ultra: can be chosen as the 365‑day unlimited video model [STALE — verify].[^1] | 480p/720p/1080p options; 1080p presumably costs more credits. |
| `kling3_0` | No official numbers; third‑party reviews quote ~6 credits for a “standard” 1080p clip [STALE — verify].[^21][^22] | Full credits. | Full credits. | Full credits. | Ultra/Creator: some blogs claim “unlimited Kling 3.0 on annual Ultra,” but this is not in official docs [STALE — verify].[^6][^16] | `--mode pro` vs `std` likely changes cost; durations integer seconds; longer clips more credits. |
| `kling2_6` | Unknown; older posts show per‑clip examples but stale.[^23][^22] | Full credits. | Full credits. | Full credits by default. | Ultra: may be selectable as one unlimited video model [STALE — verify].[^1] | Supports 5s/10s durations; 10s likely roughly double cost of 5s. |
| `cinematic_studio_3_0` | Unknown; described as “cinema‑grade highest fidelity” in SKILL docs, so expect high credit burn. | Full credits. | Full credits. | Full credits. | Full credits. | Accepts multiple media inputs; cost likely scales with duration and resolution. |
| `cinematic_studio_video` / `_v2` | Unknown. | Full credits. | Full credits. | Full credits. | Full credits. | `_v2` adds `--mode` and `--genre`; pro modes probably cost more; 5 or 10 second durations for v1, integer seconds for v2. |
| `marketing_studio_video` | Unknown. | Full credits; no evidence of absorption.[^12] | Full credits. | Full credits. | Full credits. | Resolutions 480p / 720p only; `--generate_audio true` may add cost but is not documented; modes (ugc, tv_spot, etc.) all use the same underlying Seedance engine.[^12] |
| `veo3`, `veo3_1`, `veo3_1_lite` | No Higgsfield‑specific rack rates; other platforms charge very high credits per 8s Veo clip [STALE — verify].[^24][^25] | Likely disabled or extremely expensive for Free tier.[^7][^6] | Available on paid tiers, consuming large numbers of credits per clip (tens to hundreds) per older 3rd‑party reviews [STALE — verify].[^21][^22] | Same. | Same; no suggestion Veo is ever “unlimited” in official docs. | `--quality ultra` and higher durations (6–8s) likely multiply credit cost. |
| `minimax_hailuo` | Unknown. | Full credits. | Full credits. | Full credits. | Full credits. | Resolutions 512/768/1080; durations 6 or 10; cost likely increases with resolution and length. |
| `wan2_7`, `wan2_6` | Unknown. | Full credits. | Full credits. | Full credits. | Ultra may offer unlimited Wan 2.6 as one selectable video model [STALE — verify].[^1] | 720p vs 1080p options; credit cost scales accordingly. |
| `grok_video` | Unknown. | Full credits. | Full credits. | Full credits. | Full credits. | Basic 16:9/9:16/1:1; standard Seedance‑like cost patterns likely. |

Because this matrix is so underspecified, for **Section 2 your agent should default to an empirical strategy**:

- Run `higgsfield generate cost <model> ... --json` for the exact parameters you intend to use, log the `credits` value, and treat it as **rack‑rate upper bound** for that invocation.
- Where your plan has known unlimited entitlements (e.g., Seedream 5 Lite, Nano Banana, Seedance 1.5 Pro on Ultra), you should still assume rack‑rate cost until you can confirm via transaction logs that these calls deduct zero credits; currently, the CLI does **not** expose effective cost or plan‑aware fields.
- For any model with no verified documentation, mark it as **“unknown — empirical test required”** and do not attempt to guess credit usage from older blogs.

***

## Section 3 — Quota mechanics and overage behavior

### 3.1 Behavior when monthly credits are exhausted

Official Higgsfield docs and the April 2026 “pricing and plans” explainer say that credits are **pre‑paid allocations tied to your active subscription** and must be used within the current billing term; they explicitly state that unused credits have no cash value and are forfeited on cancellation, but they do not describe in detail what happens if you hit exactly zero within a cycle.[^8][^1]

Multiple 2026 YouTube tutorials and blog guides show a UI where, after credits reach zero, the user is prompted either to **buy credit packs (“Top up credits”)** or **upgrade to a higher plan**, and attempts to generate content simply fail until you do so. These sources consistently state that extra credit packs are valid for **90 days** and that there is no automatic overage billing, only explicit pack purchases or upgrades [STALE — verify].[^4][^26][^27]

Putting this together:

- The most consistent behavior is effectively a **hard stop** when your subscription credit pool reaches zero, plus the option to **top up** with credit packs that themselves expire after ~90 days.[^27][^4][^9]
- There is **no evidence** of an automatic “pay‑as‑you‑go overage” mechanism at rack‑rate (e.g., auto‑billing per extra clip without explicit purchase), and no documentation of dropping you to a “slower queue” tier when out of credits. Unknown — primary docs do not state this explicitly.[^1][^8]


### 3.2 Rack‑rate vs plan‑aware calculation

The CLI’s `higgsfield generate cost` currently returns a simple JSON object with a `credits` field that is **the same regardless of your subscription tier**, according to GitHub issue \#1 filed against CLI v0.1.26 on 2026‑05‑04. That issue specifically complains that models marked “UNLIMITED” in the web UI for a Plus plan — Seedream 5 Lite, Seedream 4.5, Nano Banana 2 — still show nonzero `credits` in CLI cost output (100/150), and asks for the CLI to return both `base_credits` and `effective_credits` along with entitlement metadata such as `billing_mode` and `is_unlimited`.

As of that issue, there is no evidence that the CLI or API exposes plan‑aware cost in any form; all suggestions about `base_credits` vs `effective_credits` and `--require-unlimited` flags are purely proposed features, not implemented. So your agent should:

- Treat `higgsfield generate cost` as returning a **plan‑agnostic, rack‑rate upper bound**, not actual billed cost.
- Avoid assuming that a response with `credits: 0` will ever appear (it does not today) or that `cost` output reflects unlimited entitlements.


### 3.3 Credit rollover and expiry

Official pricing and plan docs state clearly:

- Credits are allocated at the start of each billing cycle and **refresh when the cycle renews**.[^8]
- Credits are **tied to your active subscription timeframe** and have **no cash value**; unused credits are forfeited when you cancel your account or cease using the service.[^1]
- Unused credits **do not roll over** to subsequent months; this is also reiterated in older FAQ pages at `higgsfield.ai/pricing?via=...` and in third‑party pricing breakdowns [STALE — verify].[^5][^9]

Separate **purchased credit packs** (top‑ups) appear in multiple tutorials with explicit text like “extra credits are valid for 90 days,” though this 90‑day window is only documented in 3rd‑party content and YouTube transcripts, not in Higgsfield’s own written docs [STALE — verify].[^4][^27]

For your cost‑prediction logic, you should:

- Assume **no rollover** of subscription credits beyond the current billing cycle.[^5][^1]
- Assume that **top‑up packs expire** within ~90 days unless you can confirm otherwise when they ship updated terms; do not plan long‑term usage around pack balances.[^27][^4]


### 3.4 Top‑up mechanism

Several 2026 video tutorials show the “Buy credits” or “Top up credits” UI: users click a “Top up credits” button, choose from preset packs (e.g., 80, 170, 380, 840, 5,000 credits), and are shown that these packs are valid for 90 days. These tutorials explicitly mention that buying packs is an alternative to upgrading a subscription and that packs “sit on top of” your plan credits and are consumed first or interleaved.[^28][^4][^27]

Official docs confirm that purchased credits are pre‑paid amounts and must be used within the active subscription lifecycle, but do not repeat the 90‑day detail. So the existence of **top‑up packs** is reliable; exact denominations and expiries must be treated as **[STALE — verify]** until confirmed in your own UI.[^8][^1]

### 3.5 Workspace billing behavior

For team‑style plans, the ImagineArt‑hosted “pricing in 2026” article and other reviews describe a **Business** plan with a minimum of 2 seats and 1,500 credits per seat pooled into a shared workspace (e.g., 3,000 credits minimum, growing with more seats). Those articles say that credits are shared at the workspace level and that parallel generation limits scale across the team (e.g., up to 16 video and 16 image jobs).[^6][^1]

However, **no primary source** documents what happens when a workspace pool is exhausted — whether jobs fall back to a user’s personal balance or simply fail. There is likewise no mention in official docs of per‑user vs per‑workspace balances; everything is described at the account level. So for now the answer is: **unknown — primary source did not disclose; treat workspace exhaustion as a hard stop** and do not assume fallback to a personal pool.[^1][^8]

### 3.6 Refund policy for failed generations

The April 2026 pricing article and Terms of Use describe a strict refund policy:

- **No refunds** for amounts due, except a one‑time refund request within 7 days of **initial purchase** if *no credits have been used at all*, subject to up to a 6% service fee and only where permitted by law.[^1]
- Refunds do **not** apply to subscription renewals or in‑cycle usage; they cover only the initial purchase.[^1]

This means there is no general mechanism for “refunds” for individual failed generations. Instead, the platform appears to simply **not debit credits for failed jobs**, as illustrated by GitHub issue \#4, where two failed Soul Cast jobs were reported as “free of credit charge.”

So your agent should:

- Assume that **failed jobs (status = failed) generally do not deduct credits**, but should not expect any refund API.
- Still treat all side‑effects as non‑atomic for safety — if a job fails after partially running, you may not see a simple “no charge” guarantee until Higgsfield clarifies this.

***

## Section 4 — Soul ID specifics

### 4.1 Plan minimum and training cost

The official **higgsfield‑soul‑id SKILL** explicitly states that “Soul training requires a paid plan (Basic+). If `higgsfield account status` shows free plan, tell the user before submitting.” That is the only clear, up‑to‑date statement about plan gating; unfortunately, it uses “Basic” terminology while the April 2026 pricing article uses “Starter,” so the exact mapping is ambiguous.

Third‑party Soul ID guides published on 2026‑05‑04 state that the “Basic Plan starts at 9 USD per month and provides 150 credits with access to Soul ID character training,” aligning with the SKILL’s “Basic+” requirement. Taken together, you can safely assume that **any entry paid tier or above** (Starter/Basic, Plus/Pro, Ultra/Ultimate, Creator/Business) is eligible to train Soul IDs.[^3]

None of the current official docs clearly state whether Soul ID training itself consumes credits; the SKILL file does not mention credit costs, and the Scribe Soul ID tutorial focuses on workflow, not billing. GitHub issue \#4 notes that failed Soul Cast jobs were free of credit charge but says nothing about training jobs. So:[^3]

- **Training cost** as credits: **unknown — primary sources did not disclose**. Your agent should assume training might cost a modest one‑time credit fee (similar to other platforms’ 20–40 credit character training) but must detect actual behavior empirically in billing logs.


### 4.2 Training time and photo requirements

The Soul 2.0 product page and Soul ID FAQ state that you need **a minimum of 20 photos** to train a Soul ID, and that training “takes about 3 minutes.” The Scribe Soul ID guide repeats this minimum and says “training typically completes in about 3–5 minutes.”[^29][^3]

By contrast, the higgsfield‑soul‑id SKILL asks for **5–20 face photos**, calling out “5–20 face photos, varied angles and lighting” as sufficient input. This looks more like an **engineering minimum** (the bare minimum before the backend rejects your job) vs. a **recommended minimum of 20** for robust identity; your agent should follow the stricter guideline:

- Require **≥20 well‑lit, diverse photos** where possible and warn users if they provide fewer than 10–12 images.[^29][^3]
- Expect training jobs to take **3–5 minutes**, and use `higgsfield soul-id wait <id>` with a generous timeout (SKILL defaults to 30m).


### 4.3 Storage limits per plan

No official source specifies how many Soul IDs a user may hold per plan; neither the SKILL nor the Soul marketing pages nor the pricing article include any numeric limits. Business‑tier descriptions mention “shareable Soul IDs” but not total count limits.[^29][^6][^1]

Thus:

- **Number of Soul IDs per user or workspace:** **unknown — primary source did not disclose**. You should expect soft limits enforced via UI/CS rather than a public quota.


### 4.4 Variant differences (`--soul-2` vs `--soul-cinematic`)

The Soul ID SKILL describes two training variants:

- `--soul-2` — for **image generation** (default).
- `--soul-cinematic` — for **cinematic / video work**.

The CLI README and MODELS catalog show Soul‑related models:

- `text2image_soul_v2` — Soul V2 image generator taking `--soul-id`.
- `soul_cinematic` — Soul Cinematic still‑image model with cinematic look.
- `soul_cast` — a separate video‑style model with an object‑typed `prompt` parameter used for Soul‑driven video roles.

Best‑practice mapping from SKILL and docs:

- Train with **`--soul-2`** when the primary target is still images via `text2image_soul_v2` or `soul_cinematic`.
- Train with **`--soul-cinematic`** if you know the main use will be cinematic videos (e.g., via Canvas or Cinematic Studio pipelines), though there is no published list of models that explicitly require this variant.


### 4.5 Photo quality guidelines and failure modes

The Soul ID SKILL and external guides give consistent quality advice:[^3][^29]

- Use **high‑quality, well‑lit photos** with consistent lighting; avoid heavy shadows, sunglasses, hats covering the face, or cropped faces.[^3][^29]
- Include varied angles (frontal, ¾, profile) and expressions; include at least one full‑body shot for better body proportion modeling.[^29][^3]
- Training failures are attributed to low quality, insufficient diversity, or too few unique faces; SKILL references `references/photo-guide.md` and says “Training failed — check photos quality (5+ unique faces, well‑lit)” as a prototypical error.

So your agent should:

- Validate local photo metadata (resolution, count) before submitting Soul training;
- Treat server‑side `Training failed` as a signal to prompt the user for more varied, higher‑quality images.


### 4.6 Reuse, sharing, deletion

The SKILL shows how to list and fetch Soul IDs:

```bash
higgsfield soul-id list
higgsfield soul-id get <id>
```

but says nothing about cross‑workspace sharing or deletion semantics. Business‑tier descriptions on older articles mention “shareable elements and Soul IDs” within a team workspace, implying that Soul IDs can be reused by multiple users in the same workspace, but this is **[STALE — verify]** and not officially documented.[^6]

There is no mention anywhere of a `higgsfield soul-id delete` command or whether deleting a Soul ID would refund any credits used to train it; given the refund policy, it is safe to assume **no credit refund on deletion**.[^18][^1]

Thus:

- **Cross‑user reuse:** Probably allowed within a shared Business/Enterprise workspace, but **unknown** for cross‑workspace or cross‑account use — no primary documentation.[^6]
- **Deletion:** Unknown at CLI level; no docs on deletion or quota recovery.
- **Quota recovery on deletion:** Almost certainly **no**; official docs treat training costs (if any) as consumption, not refundable.[^18][^1]


### 4.7 Compatible models

From the CLI README, MODELS catalog, and Soul SKILL:

- `text2image_soul_v2` — accepts `--soul-id` for Soul‑based still images.
- `soul_cinematic` — can use Soul identity for cinematic stills; SKILL suggests using Soul 2 for image; Cinematic Studio 3.0 for video.
- `soul_cast` — separate Soul‑driven video persona model; does **not** take `--soul-id` directly but uses structured `prompt` object with `character_params` including Soul reference IDs.
- Marketing Studio avatars are powered by Soul 2.0 but are **not documented** as directly consuming `--soul-id`; they are created via `higgsfield marketing-studio avatars create` (custom) or preset avatars.[^12]

So the **confirmed** models that directly consume `--soul-id` are:

- `text2image_soul_v2`
- `soul_cinematic` (as implied by SKILL and naming)

Other models such as Cinematic Studio and Soul Cast integrate Soul identity via higher‑level parameters or Canvas workflows, but there is no explicit CLI flag list beyond what is in MODELS.md.

***

## Section 5 — Marketing Studio specifics

### 5.1 Avatar types and presets

The **Marketing Studio intro page** describes:

- An “Avatar library” with **40+ ready‑to‑use avatars** that you can choose from.[^12]
- The ability to “generate your own [avatar] from a text prompt via Soul 2.0” and “pin, rename, and reuse across campaigns.”[^12]

The higgsfield‑generate SKILL explains that:

- An **avatar** is a presenter face; you can use a curated **preset** (via `higgsfield marketing-studio avatars list`) or create a **custom avatar** via `higgsfield marketing-studio avatars create --name ... --image <upload_id>`.

Official docs do **not** list the actual preset names (Jayden, Stefan, etc.), so your list of nine named avatars comes from the live product UI, not documentation; we cannot verify it here. There is also no statement that presets expand over time, though the marketing copy says “40+ avatars” and “new formats are added regularly,” so it is safe to expect avatar sets to grow.[^12]

Nothing indicates that preset avatars are restricted by plan; everything suggests they are available to any user with Marketing Studio access.[^12]

### 5.2 Custom avatar creation and relation to Soul ID

Custom avatar creation is **distinct** from Soul ID training in current docs:

- Soul ID is trained via `higgsfield soul-id create` and produces a reusable Soul identity (`--soul-id`) for generic Soul image models.
- Marketing Studio avatars are created either by **describing a look** (text prompt to Soul 2.0) or by converting uploaded photos into an avatar, via `higgsfield marketing-studio avatars create`.[^12]

The SKILL does **not** mention any plan restriction on avatar creation or per‑avatar credit cost; nor does the Marketing Studio marketing page. Third‑party reviews sometimes imply that custom avatars are a Pro‑tier feature, but these are unverified [STALE — verify].[^13][^6][^12]

So, from a documentation standpoint:

- Custom avatar creation is **available wherever Marketing Studio is available**;
- It uses Soul 2.0 under the hood but is **not bound to Soul ID quotas**;
- The cost per avatar creation (credits or free) is **unknown — primary source did not disclose**.


### 5.3 Product registry and URL coverage

According to the SKILL and marketing‑studio page:[^12]

- A **product** is a brand item with title + reference images; it can be created either by **importing a URL** or by **uploading images**.
- `higgsfield marketing-studio products fetch --url <url> --wait` fetches product data and images for a given URL.
- SKILL mentions **“Webproduct — App Store / web page version. Auto‑routes when fetching App Store URLs.”**
- The marketing page says “Works for physical products and digital apps. Paste any product link… Paste an app link and watch a creator demo your interface on camera.”[^12]

No documentation enumerates supported domains (e.g., Shopify, Amazon, etc.), but the above strongly implies:

- **Any standard e‑commerce or product page URL** is attempted;
- **App Store URLs** are specially recognized and turned into “webproduct” entries;
- Unsupported sites likely fail with a product‑fetch error, but exact failure code/API is not documented.

So URL coverage beyond “any product URL and App Store URLs” is **not formally specified**.

### 5.4 Click‑to‑Ad URL flow and cost

The SKILL gives a “click‑to‑ad” shortcut:

```bash
higgsfield marketing-studio products fetch --url https://shop.example.com/sneakers --wait
higgsfield generate create marketing_studio_video \
  --url https://shop.example.com/sneakers \
  --mode ugc \
  --duration 15 \
  --aspect_ratio 9:16 \
  --wait
```

and notes that “Backend **dedupes by URL**, so repeated runs reuse the existing entity instead of re‑fetching.” It does **not** say that deduplication affects pricing; the dedupe appears to be a **metadata optimization**, not a billing optimization.

There is no documentation comparing the cost of this one‑shot URL‑driven workflow versus a manual multi‑step workflow (manual product creation + manual avatar selection + generate). The safest assumption is:

- Click‑to‑Ad **does not discount** credit usage; it merely orchestrates the same steps;
- Repeated runs against the same URL reuse the product entity but **still incur full video generation credits** every time.


### 5.5 Mode list and updates

The SKILL’s Marketing Studio section lists the canonical modes (slugs):

- `ugc`
- `tutorial`
- `ugc_unboxing`
- `hyper_motion`
- `product_review`
- `tv_spot`
- `wild_card`
- `ugc_virtual_try_on`
- `virtual_try_on`

The marketing page lists similar modes but groups them conceptually (UGC, Professional, Narrative) rather than exposing the internal slugs. There is **no public indication** that new modes were added after the SKILL’s 0.3.0 version (commit from early May), and no additional slugs appear in MODELS.md.[^12]

So as of 2026‑05‑06, the **authoritative mode list** is the SKILL list above; any extra UI labels should be mapped back to these canonical slugs.

### 5.6 Audio generation and resolution caps

MODELS.md and the SKILL describe `marketing_studio_video` parameters:

- `--resolution` options: `480p`, `720p`, default `720p`.
- `--generate_audio` boolean, default `false`; SKILL notes that `--generate-audio true` is **supported** for Marketing Studio (and warns to use `--audio` for Seedance 2.0 instead).

So for now:

- Marketing Studio supports **480p and 720p only**, with no documented date for 1080p or 4K support.
- Enabling `--generate_audio true` produces audio (voiceover, music) in one pass; **no documentation** confirms a separate credit surcharge beyond normal resolution/duration‑based cost — answer: **unknown — primary source did not disclose**.

The Marketing Studio marketing page notes that Seedance 2.0 “generates motion, audio, and speech in a single pass,” but again, this is about capability, not cost.[^12]

***

## Section 6 — API \& CLI operational specifics

### 6.1 Rate limits by tier

There is **no explicit numeric rate‑limit table** for the REST API or CLI in official docs as of early May 2026. The April pricing article and several older reviews give only **parallel job counts** (concurrency), which we already summarized in Section 1: Starter ~2 video / 4 image, Plus ~6 video / 8 image, Ultra ~8 video / 8 image, Business up to 16 video / 16 image [STALE — verify].[^14][^6][^1]

Nothing describes per‑minute, per‑hour, or per‑day hard caps, nor separate limits for API vs UI vs CLI. Older platform‑wide pricing pages mention general API rate‑limit language but with no numbers. Therefore:[^9][^5]

- **Concurrent jobs:** approximate, plan‑dependent, as summarized earlier (but subject to change without notice).[^6][^1]
- **Per‑minute submission caps:** **unknown — primary sources did not disclose**.
- **Per‑day or per‑hour caps:** **unknown**; likely enforced internally but not documented.

For a robust agent, you should implement exponential backoff on any 429s and be prepared for undocumented throttling, but you cannot plan by fixed “X requests per minute” rules.

### 6.2 Queue priority

Multiple non‑official guides say that higher tiers (“Pro,” “Ultra,” “Creator/Business”) receive a **priority queue** or “priority rendering,” while lower tiers may experience slower job start times under heavy load. None of this appears in the official pricing or CLI docs, which do not mention queue priority per tier.[^7][^14][^13][^6][^1]

So:

- It is **very likely** that Higgsfield internally prioritizes higher‑tier accounts (standard SaaS pattern), but this is not formally documented and cannot be relied on programmatically.
- Your cost‑prediction and scheduling logic should **not assume** any specific speed differential; treat queue times as stochastic and account‑independent unless you measure otherwise.


### 6.3 Batch generation (`gpt_image_2 --batch_size N`)

MODELS.md shows that `gpt_image_2` supports a `--batch_size` parameter (default 1) but provides no pricing commentary. Older generic credit pages say that “every action — video generation, images, effects, upscaling — consumes credits,” with cost depending on model and output count.[^9][^5]

There is no evidence of a bulk discount for batch generation in any official doc, and no CLI examples show `generate cost` returning different values for `batch_size > 1`. So the only safe assumption is:

- Batch generation **multiplies cost by N** (i.e., N independent images at rack‑rate) until proven otherwise; there is **no documented batch discount**.

Your agent should therefore treat `batch_size` as a linear multiplier on the per‑image rack rate and compute **effective rack‑rate cost = credits * batch_size**.

### 6.4 API token and REST vs CLI/MCP parity

The CLI README and the dedicated CLI site say:

- You authenticate via `higgsfield auth login`, which opens a browser and obtains OAuth tokens; no API key is needed.[^14]
- “Higgsfield tools use the same credit system as the Higgsfield platform. Each generation costs credits based on the model and resolution.”[^14]

Separate API documentation (found as a PDF on Scribd, dated 2026‑02‑08) describes a REST `POST /v1/generate` endpoint with parameters for text‑to‑video, image‑to‑video, and Soul mode, but does not include pricing fields or rate‑limit numbers. The SKILL docs for the MCP server (`higgsfield-mcp`) also emphasize that MCP and CLI hit the same backend.[^30][^31][^14]

So:

- For pricing and quota purposes, the **REST API is effectively a 1:1 mirror** of the CLI/MCP behavior — no separate billing model.[^31][^14]
- Some features (Canvas workflows, complex multi‑model graphs) are **not exposed** via CLI or REST yet (see Section 7 on Canvas issue).


### 6.5 Webhooks, retention, workspace transfer

There is **no mention** of webhooks in the current public CLI or API docs: no `callback_url`/`webhook_url` parameter in MODELS.md or SKILL files, and the PDF doesn’t show any such field. Instead, the pattern is polling (`generate wait`, `generate get`) or `--wait` to block until completion.[^31]

Similarly, no doc states how long job result URLs remain valid or how long media is stored; the platform marketing emphasizes “export / download” but no retention numbers. Third‑party posts occasionally mention 30‑day retention, but these are older and not authoritative [STALE — verify].[^19][^9][^29][^12]

There is no documentation of cross‑workspace transfer for jobs, uploads, or Soul IDs; Canvas‑related issues explicitly say Canvas cannot be accessed via CLI/MCP/REST (yet), so any such transfer would be UI‑only.

Thus:

- **Webhook support:** currently **unknown / likely absent** in public API; everything uses polling.
- **Output retention / URL expiry:** **unknown**; your agent should download and persist outputs promptly and not rely on long‑term URL validity.
- **Workspace transfer:** **unknown**; no CLI or API support documented.

***

## Section 7 — Recent changes and known issues

### 7.1 CLI release cadence

The GitHub releases list for `higgsfield-ai/cli` shows:

- v0.1.9 released 2026‑04‑30, followed by **nine more releases** (0.1.10–0.1.18) through 2026‑05‑02.
- v0.1.19–v0.1.28 all released between 2026‑05‑02 and 2026‑05‑04, with **at least eight distinct tags in a single day** on 2026‑05‑04 (0.1.21–0.1.28).

This confirms the CLI has an extremely rapid early‑launch cadence: **double‑digit releases in ~5 days**, which strongly implies that syntax, flags, and behavior (including cost estimation) are still in flux. Your integration must **not** rely on behavior remaining stable across even minor versions; pinning to a known good tag and/or checking `higgsfield version` is essential.

### 7.2 Open issues \#1–\#4 in `higgsfield-ai/cli`

From the GitHub issues we inspected (all opened 2026‑05‑04/05 and still **open**):

1. **Issue \#1 — “Expose subscription‑aware unlimited model eligibility and effective costs in CLI.”**
    - Problem: `generate cost` shows only base model credit costs (e.g., 100/150 credits) for models that the web UI marks as `UNLIMITED` under a Plus subscription.
    - Requested features: subscription‑aware entitlement metadata in `model list --json`, `base_credits` vs `effective_credits` in `generate cost`, preflight warnings in `generate create`, and flags like `--require-unlimited`.
    - Status: still open; no fix merged as of last update (created/updated 2026‑05‑04).
2. **Issue \#2 — “Feature request: API / CLI / MCP access to Canvas workflows.”**
    - Problem: **Canvas**, Higgsfield’s node‑graph workflow surface, is currently **not accessible** via CLI, MCP, or Cloud API; all programmatic interfaces only expose single‑model calls.
    - Requested features: Canvas execution endpoint (`POST /v1/canvas/{id}/run`), JSON export/import, MCP tools (`canvas_list`, `canvas_run`, etc.), and CLI parity (`higgsfield canvas pull/push/run`).
    - Status: open; last update 2026‑05‑05; would be a major future unlock for agentic workflows.
3. **Issue \#3 — “Windows install fails: tar invocation missing --force-local.”**
    - Problem: `npm install -g @higgsfield/cli` fails on Windows because `tar -xzf` misinterprets `C:\...` paths as remote spec; fix is to pass `--force-local` to tar.
    - Suggested one‑line patch to install script; workaround using `--ignore-scripts` and manual extraction is provided.
    - Status: open, as of 2026‑05‑05.
4. **Issue \#4 — “generate create soul_cast ignores --prompt (object).”**
    - Problem: `soul_cast` model declares `prompt` as `object` in schema, but CLI treats `--prompt` as string only, rejects `@file.json`, and silently drops JSON, submitting empty `character_params` and random AI‑generated description/full_name.
    - Symptom: jobs either fail immediately or run with random placeholder characters even when JSON is provided.
    - Status: open; suggests needed support for object‑typed params and `--prompt-file` or JSON parsing in CLI.

For your project, issue \#1 and \#2 are particularly important: they explicitly confirm that **subscription‑aware cost surfaces and Canvas workflows are not yet accessible via CLI/MCP**, so you must not assume their presence.

### 7.3 Roadmap signals and recent model changes

Public roadmap hints are scattered:

- The Higgsfield Skills repo and CLI README emphasize breadth: Soul 2.0, Nano Banana Pro, Flux 2, Veo 3.1, Kling 3.0, Seedance 2.0, Marketing Studio, Soul Cast, etc., implying **constant additions** to the model catalog.
- Soul 2.0 marketing and blog content highlight “Nano Banana 2 and Gemini 3.0: early signs of a major shift in AI image generation,” indicating that Nano Banana 2 is a relatively recent image‑model addition [STALE — verify].[^29]
- Social posts and Instagram reels around April 2026 mention “cheapest access to unlimited Seedance 2.0 (up to 70% off)” and workflows integrating Higgsfield with Claude Code and SKILL.md pipelines, suggesting continued investment in unlimited Seedance promo pricing, but these are marketing snippets rather than roadmaps [STALE — verify].[^32][^33]

No official blog or changelog entry in May 2026 explicitly commits to longer Veo durations, audio for Seedance outside Marketing Studio, or additional Soul ID variants; all such expectations are extrapolations from current model capabilities and broader industry trends. So:[^29][^12]

- **Roadmap:** effectively **opaque**; there is no public, versioned roadmap your agent can rely on.
- **Model additions/deprecations in last week:** aside from the CLI’s rapid release cycle and Skills repo update, we found no primary statement of new models launched in May 2026; the catalog in MODELS.md already includes Veo 3.1, Kling 3.0, Seedance 2.0 as of early May.

***

## Section 8 — Comparative pricing (sanity check)

Because Higgsfield does not publish per‑model credit costs and competitor pricing is also evolving, it is **not possible** to compute an exact, bullet‑proof cost comparison for a specific workload — “5‑shot 25‑second 9:16 vertical reel with stills + image‑to‑video” — across Higgsfield and all competitors using only public docs as of 2026‑05‑06. Most sources provide high‑level “credits per clip” examples under simplified assumptions and older model versions.[^21][^22][^23][^5][^9][^6]

However, third‑party 2026 reviews give a qualitative sense:

- Higgsfield Starter/Plus/Ultra are generally framed as **cheaper per Veo/Kling/Seedance clip** than buying Veo or Kling direct (e.g., via Vertex AI or Freepik), where a single Veo 3.1 8‑second clip can cost hundreds to thousands of credits on those platforms [STALE — verify].[^25][^24]
- Compared with platforms like Krea, Pika, Runway, and OpenArt, Higgsfield is usually priced as **mid‑tier**: more expensive than some budget‑oriented tools but cheaper than high‑end b2b Veo/Sora pipelines for comparable quality.[^17][^34][^13]

Given the lack of precise matrixes, the **only reliable way** to answer your Section 8 question is **empirical benchmarking**:

- Construct a standard job spec (e.g., Seedance 2.0 or Kling 3.0 25‑second 9:16 reel with specified resolution and audio).
- Run that job (or as close as possible) on Higgsfield, Krea, Magnific, OpenArt, Pika Labs, Runway (Standard/Pro), and direct provider APIs (Veo on Vertex AI, Sora on OpenAI, Kling direct) and record actual billed credits or dollars per clip.
- Update your agent’s internal reference table from those experimental results rather than public marketing content.

As of today, we cannot provide robust numerical rows without risking inaccurate or obsolete data.

***

## Section 9 — Business / agency use cases

### 9.1 Volume / commitment discounts

Official docs and older pricing explainers suggest:

- **Enterprise** and high‑volume customers can contact sales for custom pricing; “Enterprise Plan — custom pricing, dedicated infrastructure, team collaboration, SLAs, and advanced admin controls” are mentioned in both official and third‑party materials.[^7][^1]
- Some articles describe **aggressive discounts** on annual Creator/Ultra plans (up to ~55–60% off vs monthly billing), plus additional percentage discounts on extra credit packs at Creator/Business tier [STALE — verify].[^7][^6]

There is no fixed, public “>100 reels/month” discount schedule; everything above Ultra/Creator is bespoke. So:

- Yes, **volume/commitment discounts exist**, but only via direct Enterprise/Business negotiation.
- There is no API exposed “agency rate card” your agent can rely on.


### 9.2 White‑label / reseller

Higgsfield’s Terms of Use explicitly forbid reselling or sublicensing the service itself:

- You may not “license, sell, rent, lease, transfer, assign, reproduce, distribute, host or otherwise **commercially exploit the Service** or any portion of the Service.”[^18]

However, the same Terms and Trust page say that Higgsfield does **not** claim ownership of your inputs or outputs and **does not restrict commercial use of outputs**, subject to legal restrictions.[^19][^18]

That implies:

- You **can** build a commercial service that uses Higgsfield to generate assets and sells finished assets or campaigns to clients (agency model).
- You **cannot** white‑label the Higgsfield UI or expose a pass‑through Higgsfield service that looks like your own infrastructure without a separate Enterprise agreement.

So a formal “reseller” role is **not granted** by default; it must be negotiated.

### 9.3 API‑only access

No plan matrix document shows an “API‑only” tier that excludes the web UI; all tiers appear to include access to the main platform plus APIs/CLI. Some 3rd‑party comparisons talk about API access only being available on higher plans, but this is not confirmed in official docs [STALE — verify].[^15][^13][^14][^1]

So as of May 2026:

- There is **no public API‑only cheaper plan** that removes UI access.
- API and CLI access seem to be included wherever you have a valid Higgsfield account and credits.


### 9.4 Compliance / legal and preset avatar rights

The Terms of Use and Trust pages emphasize:

- Users retain rights to their inputs and outputs, and Higgsfield does not claim IP ownership over generated content, but retains broad rights to use inputs/outputs to improve models and for marketing.[^19][^18]
- Users must ensure that uploaded content and likenesses are lawful and that they hold the necessary rights; this especially applies to faces and biometric data.[^18][^19]

There is **no explicit “model release” statement** for preset avatars on Marketing Studio — nothing that explicitly says “these avatars are synthetic and cleared for commercial advertising use,” though the entire feature is marketed as a tool for branded ads. In practice, the combination of “no ownership claimed over outputs” and “no restrictions on commercial use of outputs” strongly suggests preset avatars are intended for commercial use, but there is no dedicated legal clause for them.[^19][^18][^12]

For strict compliance, your agency should:

- Treat preset avatars as synthetic and commercially usable, but consult legal counsel for high‑risk verticals (alcohol, gambling, healthcare) and jurisdictions where “synthetic presenter” disclosure is required.
- Ensure any real‑person likeness used in Soul ID or custom avatars has an appropriate model release, as required by the Terms.[^18][^19]


### 9.5 Image and video rights

Per the Terms of Use Agreement and Trust page:[^19][^18]

- Higgsfield does **not** claim ownership over **inputs or outputs**; you retain ownership of your uploads and generated media.
- The service **does not restrict commercial use** of outputs; you may use them in paid ads, packaging, etc., subject to compliance with content policies and law.[^18][^19]
- Higgsfield retains a broad, perpetual license to use your inputs and outputs internally (model training, product improvement, marketing), which may matter for sensitive campaigns.[^18]

The only major restrictions are:

- You may not claim that synthetic content is “natural content” in ways that violate law.[^35][^18]
- You must not use the service to generate or distribute illegal, infringing, or harmful content, and content with other people’s faces is especially regulated.[^19][^18]

So **from a business/agency perspective**, Higgsfield is compatible with commercial ad use, including preset avatar‑led marketing videos, as long as you comply with local advertising and personality‑rights law and with Higgsfield’s content guidelines.

***

## Follow‑up empirical tests (ranked by cost‑to‑information ratio)

To make your agentic toolkit safe and accurate, you should run the following **empirical tests** under a dedicated Higgsfield account and log actual credit behavior:

1. **Plan‑aware cost validation (high impact, low cost).**
    - For each subscription tier you can access (Free, entry paid, Plus/Ultra), run `higgsfield generate cost` and `generate create` for a matrix of simple prompts across key models: Nano Banana, Nano Banana 2, Seedream 4.5/5 Lite, GPT Image 2, Seedance 2.0, Kling 3.0, Wan 2.6, Marketing Studio video.
    - Compare `generate cost` outputs with actual credit deltas from `higgsfield account status` before/after to discover which model/parameter combos are truly “absorbed” vs billed on each tier.
2. **Unlimited video model verification on Ultra (medium cost, high information).**
    - On an Ultra‑like account, select each advertised unlimited video model in turn (Seedance 1.5 Pro, Wan 2.6, Kling 2.6, Nano Banana 2 video if available).[^1]
    - Generate multiple clips at varying resolutions/durations and confirm whether credits are ever deducted, and whether there are hidden concurrency or daily caps.
3. **Soul ID training cost and failure patterns (medium cost).**
    - Train several Soul IDs with varying photo counts and qualities (5, 10, 20, 30 images; good vs poor lighting).[^29]
    - Measure whether training jobs consume credits and how sensitive failure rates are to photo count/quality, then codify stricter validation heuristics for your agent.
4. **Marketing Studio cost curve (medium cost).**
    - Measure `marketing_studio_video` credit usage for combinations of `--resolution` (480p vs 720p), `--duration` (10 vs 15), `--generate_audio` true/false, and different modes (`ugc`, `tv_spot`, `hyper_motion`).[^12]
    - Confirm whether audio and mode choices influence credits or only duration/resolution do.
5. **Batch generation cost linearity (low cost).**
    - For `gpt_image_2`, run `generate cost` and `generate create` with `batch_size` 1, 2, 4, 8 at fixed prompt and resolution.
    - Verify whether cost scales linearly with `batch_size` or if there is any hidden discount.
6. **Retention and URL lifetime (medium‑term test).**
    - Generate a small set of images and videos and track how long their result URLs remain usable before expiring; test both subscription and credit‑pack outputs.[^19][^12]
    - Use results to decide how quickly your agent should download and archive content.
7. **Cross‑workspace Soul ID behavior (higher friction, medium information).**
    - On a Business‑style setup, create Soul IDs in one workspace and test whether they are visible/reusable across other workspaces and whether deletion is exposed via UI or CLI.[^6]
    - This will inform how you model identity assets for agency clients.
8. **Comparative per‑clip cost benchmark (highest cost, high strategic value).**
    - Run your standard “5‑shot 25‑second 9:16 reel” spec through Higgsfield, Krea, Magnific, OpenArt, Pika, Runway Standard/Pro, and direct provider APIs for Veo/Sora/Kling.[^34][^17][^24][^25]
    - Normalize costs to USD per finished clip and update your internal pricing reference so your orchestrator can choose the cheapest viable backend for a given client SLA.

These experiments will give you the missing ground truth that the current documentation cannot provide, and let you build a **plan‑aware, empirically calibrated cost layer** around Higgsfield’s evolving credit model.
<span style="display:none">[^36][^37][^38][^39][^40][^41][^42][^43][^44][^45][^46][^47][^48][^49][^50][^51][^52][^53][^54][^55][^56][^57][^58][^59][^60][^61][^62][^63][^64][^65][^66][^67][^68][^69]</span>

<div align="center">⁂</div>

[^1]: https://geo.higgsfield.ai/task/blog/higgsfield-ai-pricing-plans

[^2]: https://higgsfield.ai/pricing

[^3]: https://scribehow.com/page/Higgsfield_Soul_ID_The_Best_Tool_for_AI_Character_Consistency_in_2026__i1nfbuF-TcalH-r-LeNQgg

[^4]: https://www.youtube.com/watch?v=y_ZtBfRn2HA

[^5]: https://higgsfield.ai/pricing?via=appscribed

[^6]: https://www.imagine.art/blogs/higgsfield-ai-pricing

[^7]: https://scribehow.com/page/Higgsfield_AI_Pricing_2026_From_dollar0_to_dollar119Mo__What_Do_You_Actually_Get__5l9qI0AVTtewF1YoVWjxmA

[^8]: https://geo.higgsfield.ai/higgsfield-ai-pricing-plans-how-it-works

[^9]: https://noflufftech.org/blog/higgsfield-pricing-credits

[^10]: https://www.vo3ai.com/higgsfield-ai-pricing

[^11]: https://www.reddit.com/r/HiggsfieldAI/comments/1t0axoj/choosing_higgsfield_pricing_plan_in_2026_full/

[^12]: https://higgsfield.ai/marketing-studio-intro

[^13]: https://freerdps.com/blog/higgsfield-ai-review/

[^14]: https://higgsfield.ai/cli

[^15]: https://apostle.io/pricing/higgsfield/

[^16]: https://hackceleration.com/higgsfield-review/

[^17]: https://flowith.io/blog/higgsfield-pricing-2026-free-vs-creator-vs-studio/

[^18]: https://higgsfield.ai/terms-of-use-agreement

[^19]: https://higgsfield.ai/trust

[^20]: https://www.seaart.ai/blog/higgsfield-ai

[^21]: https://www.yangsweb.com/blog/higgsfield-ai-review-alternatives-pricing

[^22]: https://sites.google.com/view/higgsfield-ai-pricing/home

[^23]: https://www.reddit.com/r/HiggsfieldAI/comments/1pam690/new_to_higgsfield_and_ai_in_general_how_much/

[^24]: https://www.linkedin.com/posts/james-kenna007_is-googles-ai-video-model-veo-3-worth-it-activity-7333520857912238080-1P4z

[^25]: https://www.linkedin.com/posts/eugeniofierro_veo3-googledeepmind-freepikai-activity-7349452538699550722-EuX5

[^26]: https://www.youtube.com/watch?v=1FCpIZxjsRc

[^27]: https://appreviewlab.com/?p=2192

[^28]: https://www.youtube.com/watch?v=isen7GTzVHE

[^29]: https://higgsfield.ai/soul-intro

[^30]: https://libraries.io/npm/higgsfield-mcp

[^31]: https://www.scribd.com/document/992401211/Higgsfield-API-Documentation

[^32]: https://flowith.io/blog/higgsfield-pricing-free-vs-creator-vs-studio/

[^33]: https://www.instagram.com/reel/DW_4P9gAEtu/

[^34]: https://pikes.ai/blog/higgsfield-ai-review-2026-features-pricing-pros-and-best-alternatives

[^35]: https://firebasestorage.googleapis.com/v0/b/higgsfield-app.firebasestorage.app/o/Terms of Service.pdf?alt=media\&token=624518a3-9cd6-416c-aa25-d6f6df27d0a3

[^36]: https://blog.segmind.com/higgsfield-ai-features-pricing-guide/

[^37]: https://www.youtube.com/watch?v=XDrbSAJLnn0

[^38]: https://higgsfield.ai/soul

[^39]: https://github.com/higgsfield-ai/skills/blob/main/INSTALL.md

[^40]: https://github.com/higgsfield-ai/skills/blob/main/INSTALL_FOR_AGENTS.md

[^41]: https://www.youtube.com/watch?v=czT_xpp8XVI

[^42]: https://github.com/OSideMedia/higgsfield-ai-prompt-skill

[^43]: https://higgsfield.ai/skills

[^44]: https://www.linkedin.com/posts/spiritnovel_styletransformation-generativeai-aicontentcreation-activity-7437784479911321600-Q96U

[^45]: https://github.com/higgsfield-ai/skills

[^46]: https://higgsfield.ai/earn

[^47]: https://marketingagent.blog/2026/03/14/tutorial-scroll-animated-sites-with-claude-cowork/

[^48]: https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md

[^49]: https://github.com/higgsfield-ai/skills/blob/main/setup

[^50]: https://github.com/openclaw/skills/blob/main/skills/killerapp/agentskills-io/SKILL.md

[^51]: https://www.instagram.com/reel/DX2JNSeRlsC/

[^52]: https://github.com/higgsfield-ai/higgsfield/blob/main/README.md

[^53]: https://www.instagram.com/p/DXoavP8AJvc/

[^54]: https://www.youtube.com/watch?v=gDt0WOrkfjs

[^55]: https://www.youtube.com/watch?v=JZACe9GoYow

[^56]: https://libraries.io/pypi/higgsfield-cli

[^57]: https://www.reddit.com/r/HiggsfieldAI/comments/1pvu9t2/what_happened_to_my_credits/nvz3z3t/

[^58]: https://www.reddit.com/r/HiggsfieldAI/comments/1s8qmxi/got_burned_by_higgsfields_unlimited_plan/

[^59]: https://www.youtube.com/watch?v=fOTwqHviBlc

[^60]: https://sozee.ai/resources/higgsfield-pricing-plans-comparison-higgsfield/

[^61]: https://www.kapwing.com/resources/how-to-use-higgsfield-ai-video-generator/

[^62]: https://www.youtube.com/watch?v=cksEVv1tArI\&list=PLVGtMgCPBP8gYr1rWDA3GMPZscuAVOaO1

[^63]: https://higgsfield.cc/terms

[^64]: https://www.youtube.com/watch?v=mAq_q4xs_aw

[^65]: https://creators.higgsfield.ai/terms

[^66]: https://www.linkedin.com/posts/eugeniofierro_ainews-freepik-veo31-activity-7384329481697718273-yUrZ

[^67]: https://www.reddit.com/r/HiggsfieldAI/comments/1qxfbnh/hot_take_higgsfield_would_be_a_lot_more/

[^68]: https://www.youtube.com/watch?v=PPUdzB8QMEE

[^69]: https://www.facebook.com/groups/aiimagesworld/posts/854660487129980/

