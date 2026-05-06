# Brand Profile Format

The schema for `brands/<name>/profile.md`. Designed to be read by the agent on every run for that brand, so the agent applies real brand context instead of generic defaults.

> The interview that fills this out lives in `references/interview-craft.md`. **The format is flexible, not strict** — fields can be empty, marked `[gap]`, or filled with rich qualitative text. The agent treats this as a knowledge document, not a database row.

## File location

```
brands/<name>/
├── profile.md                  ← the document below
├── assets/
│   ├── people/                  ← photos of person/talent (for Soul ID + general use)
│   ├── logos/
│   ├── style-guide/             ← moodboards, brand-ref shots
│   └── product/                 ← if applicable
├── source-fetches/              ← cached output of firecrawl_scrape from URLs (auto-imported context)
│   ├── homepage-2026-05-06.md
│   └── instagram-2026-05-06.md
└── soul-id.txt                  ← UUID(s) of trained Soul IDs, one per line
```

`brands/` is **gitignored by default** because it contains real photos and possibly private brand info. Users who want to commit a brand kit (e.g. for a public open-source project) can override per-folder.

## profile.md template

```markdown
---
name: ben
type: personal_brand        # personal_brand | business | agency_client | fictional
created: 2026-05-06
last_interview: 2026-05-06
confidence:
  who: high                  # high | medium | low | gap — agent self-rates after interview
  audience: medium
  spike: high
  visual: medium
  voice: high
  constraints: high
---

# Brand: Ben

## Who / what

[Free-form 2-4 paragraphs. The honest "tell me what you do at a dinner party" answer. Specific. Stories.
This is NOT a tagline. NOT positioning copy. The actual unvarnished version.]

### Origin / pivot

[The non-obvious story behind it, if it came up.]

### Lexicon

[Words and phrases the user actually uses repeatedly. The agent should reuse these in captions and prompts.
- Example: "we don't do 'campaigns', we do 'launches'"
- Example: avoids the word "content" — uses "posts" or "work"
]

## Audience — the specific people

[NOT a demographic. The most recent real person who got it. What they're like, what they asked, why they leaned in.
Paragraph form is fine. Multiple example people is better than one demographic statement.]

### What they're NOT

[Often more useful. "Sarah's not the kind of person who wants pricing-page energy. She wants the story."]

## The spike — what makes them non-substitutable

[The 1-3 specific things this brand has that nobody else in their space does, says, or believes.
NOT "we care more" / "we're authentic". Actual specific opinions, takes, methodologies, points of view.
If this section feels generic, the interview wasn't done — re-run.]

## Existing material (auto-fetched + provided)

### URLs the agent may re-fetch for fresh context

- [website-url] — primary site
- [instagram-handle-or-url] — recent posts
- [linkedin-url] — voice samples
- (etc.)

### Cached fetches (in `source-fetches/`)

- `source-fetches/homepage-2026-05-06.md`
- `source-fetches/instagram-2026-05-06.md`

The agent re-fetches these when context feels stale (>30 days, or when content quality drops).

### Manually provided

- [path] — file/folder paths to brand kits, style guides, screenshot collections, etc.

## Visual DNA

### Palette

[Either: hex codes / color names / phrases ("dusty terracotta and bone white, never anything saturated").
Or: extracted from `firecrawl_scrape` with `branding` format on their website, cite source.]

### Photo aesthetic

[Specific. NOT "warm and inviting". Examples: "always overhead flat-lay style for product, always natural light", "people shots are mid-distance, never close-ups", "we live in shadow and texture, not bright clean studio".]

### Mood / energy

[How content should *feel*. Examples: "calm authority", "messy and human", "polished but with one weird detail per shot", "no smiles, ever".]

### Reference images / moodboard

- `assets/style-guide/moodboard-1.png`
- `assets/style-guide/competitor-vibe.png`

## Voice

[How they actually write. Examples and rules.]

### Sentence patterns

[E.g. "short. punchy. line breaks for emphasis."
Or: "long-form, conversational, lots of asides in parentheses."]

### Words / patterns to use

[Things they say. Phrases they reuse. Examples.]

### Words / patterns to avoid

[Things that make them cringe. Banned words. Specific styles.
- "Never the word 'unlock' — overused."
- "Never start a post with 'In today's world...'."
- "No emoji clusters at line ends."
]

### Caption shape (typical)

[E.g. "hook line, beat, story-bit, payoff, soft CTA"
Or: "single sentence with line breaks, no CTA, sometimes a question"]

## Recurring talent

### People

- name: Ben
  soul_id: [UUID if trained]
  photos: assets/people/ben/
  notes: [anything specific — e.g. "always in the navy linen jacket, never with sunglasses on"]

[Repeat per person if multiple]

## Hashtag families

[Grouped by use case — agent picks the right family per post.]

- core: [#brandhandle, #handle-handle]
- topic-design: [#design, #branding, #typography]
- local: [#melbourne, #sydneydesign]
- (etc.)

## Posting cadence and platforms

- Primary platforms: [IG, LinkedIn, etc.]
- Cadence: [e.g. 3 posts/week IG, 1 post/week LinkedIn]
- Format mix: [e.g. 60% carousel, 30% single, 10% reel]

## Constraints — never do

[Hard rules. The agent refuses to produce these.]

- [topic / style / aesthetic to avoid]
- [people who must not appear]
- [legal / compliance, if applicable]

## Open questions (gaps from last interview)

[The agent fills this when the user couldn't answer something. Surface in next session.]

- [ ] How does the brand handle seasonality / timely content?
- [ ] What's the position on AI-disclosure on AI-generated posts?
```

## How the agent uses this file

**On every `/higgsfield-make` run for this brand:**

1. Read `profile.md` in full — load it as primary context
2. Read any cached `source-fetches/*.md` to refresh recent voice samples
3. Apply Voice section to caption generation
4. Apply Visual DNA + Photo aesthetic to image prompts
5. Apply Constraints as hard rules — refuse to generate against them
6. Apply Hashtag families based on post topic
7. Use Recurring talent → if a person is featured, use their `soul_id`

**On `/higgsfield-make` start:**
1. Detect active brand from CWD or explicit `--brand` flag
2. If `confidence.spike == "low"` or `"gap"`, refuse to generate — tell user to re-run brand-create
3. If profile is >90 days old or has many `[gap]` markers, suggest a refresh interview

## Refreshing a profile

Brands evolve. The agent suggests a refresh when:
- Last interview > 90 days
- More than 3 generations in a row produced output the user rejected
- The user's existing channels have new material the cached fetches don't reflect

`/higgsfield-brand-refresh <name>` re-runs the interview with the existing profile pre-loaded — only asks about territories with low confidence or stale data.

## Why this format works

- **Free-form fields** instead of strict enums = the brand profile actually captures distinctiveness
- **Confidence ratings** = the agent knows what it doesn't know, can ask before guessing
- **Cached fetches** = the agent has real voice samples, not just user descriptions of their voice
- **Constraints section** = explicit don'ts protect from cringe outputs
- **Open questions list** = profile is a living document, gets sharper over time

The whole thing is designed so a fresh agent reading just `profile.md` can write content that sounds like the brand, without re-interviewing.
