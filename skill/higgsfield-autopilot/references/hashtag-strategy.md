# Hashtag Strategy

How the agent picks hashtags per platform, per post. Distilled from `docs/ask-rag/ask-ads-marketing-9q.md` Q6.

## Per-platform recommendations (2026)

| Platform | Count per post | Mix |
|---|---|---|
| **Instagram** | 5-10 | broad + niche + branded |
| **TikTok** | 3-5 | trending + niche |
| **LinkedIn** | 3-5 | industry-specific, professional |
| **Twitter / X** | 1-2 | niche only |

## The three hashtag types

### Broad (high volume, low specificity)

Big-tent hashtags with millions of posts. They give discovery surface area but you're competing with everyone.
- Examples: `#design`, `#smallbusiness`, `#fitness`
- Use **1-3 per post on IG**; 0-1 on TikTok / LinkedIn

### Niche (medium volume, high specificity)

The sweet spot — narrow enough to stand out, broad enough to have an audience.
- Examples: `#brandidentitydesign`, `#smallaussiebusinesses`, `#kettlebelltraining`
- Use **3-5 per post** across all platforms — these do most of the discovery work

### Branded (low volume, owned)

Your own hashtag(s). Build a small community around them.
- Examples: `#showandgo`, `#bensmadethis`
- Use **1 per post** consistently. Encourage user-generated content under it.

## Per-brand-type defaults

Read `brand_type` from the brand profile, apply these starting points (refine over time):

| Brand type | Hashtag tilt |
|---|---|
| **personal_brand** | More niche-personality + 1 branded + 1-2 broad. e.g. expertise area + city/region + branded handle |
| **small_business** | More niche-product + 1 branded + 1-2 broad-category. e.g. product type + use case + branded |
| **service_agency** | More industry-niche + LinkedIn-professional. Broader hashtags hurt on LinkedIn — keep tight. |
| **creator** | Trending-aware. TikTok especially — refresh weekly based on what's surfacing |

## Hashtag families (in the brand profile)

A brand's profile.md should define **hashtag families** the agent picks from based on post topic:

```yaml
hashtag_families:
  core: [#brandhandle, #signature]              # always include 1-2 of these
  topic_design: [#design, #branding, #typography]
  topic_business: [#smallbusiness, #entrepreneur]
  topic_local: [#melbourne, #aussiedesign]
  topic_seasonal: [#spring2026, #christmasplanning]   # rotate per season
```

The agent picks 1-2 from `core`, then picks the rest from whichever topic family matches the post.

## Refresh cadence

Hashtags decay. The MCP advice + observed practice:

- **Branded:** never refresh (consistency is the point)
- **Niche:** refresh quarterly — check what's trending in your space
- **Broad:** refresh whenever a post tagged with one underperforms vs. peers
- **Trending (TikTok):** refresh weekly — check the For You page for what's surfacing

When the agent runs `/higgsfield-make` for a brand, if the brand's `hashtag_families` haven't been touched in >90 days, it should suggest a refresh.

## Don't

- **Don't repeat the same hashtag set every post** — IG and Instagram down-rank "spam" patterns. Vary.
- **Don't use broad hashtags only** — you'll be drowned out
- **Don't use 30 hashtags on IG** — 2026 best practice is 5-10. The "max it out" advice is from 2018-2021.
- **Don't use hashtags as captions** — `#hustle #grindset #entrepreneur` reads as stock content
- **Don't use trending hashtags that don't match the post** — algos punish irrelevant tagging
- **Don't tag competitor brands or named people** without permission — risk of being flagged

## When the agent has no idea what hashtags to use

Cold-start fallback (when the brand profile has no `hashtag_families` defined yet):

1. Read the brand profile's `who` and `audience` sections
2. Generate 3 broad + 5 niche based on those
3. Suggest a branded hashtag derived from the brand name
4. Tell the user: "I drafted these — review and add the ones you want to lock in as your families. I'll save them to the profile."

Don't ship hashtags without the user signing off on the family set the first time.

## Output shape

When the agent generates hashtags for a post, return:

```
Hashtags (8 total — 1 branded, 5 niche, 2 broad):

#bensmadethis · #brandidentitydesign · #aussiedesign · #typographylove · #studiomelbourne · #smallstudio · #design · #branding
```

Use `·` separator for readability when listed. Use spaces when they go in an actual post.

## Sources

`docs/ask-rag/ask-ads-marketing-9q.md` Q6. Recent best practice as of mid-2026 — refresh this doc if platform algorithms shift.
