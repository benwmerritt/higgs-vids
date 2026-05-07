# Caption Craft

How the agent writes captions that read like a human wrote them, not an LLM. Distilled from `docs/ask-rag/ask-ads-marketing-9q.md` Q5.

> **Why captions matter:** the image stops the scroll, the caption decides whether they save / share / follow. A great image with a templated caption underperforms a good image with a great caption.

## Hard bans (refuse to ship — non-negotiable)

These are immediate-fail rules. If a caption draft contains any of these, the agent rewrites — does not ship.

| ❌ Banned | What it looks like | Why |
|---|---|---|
| **Em dashes (`—`)** | "We don't just make content — we make movements." | Instant AI tell in 2026. Replace with period, comma, or colon. |
| **Carousel slide copy >15 words** | A whole paragraph crammed onto slide 4 | One short beat per slide is the carousel format |
| **Hooks >10 words** | The 67-word "hook" from the 2026-05-06 test | A hook is one scroll-stopping line, not a thesis |
| **Generic openers** | "In today's fast-paced world", "Now more than ever", "The secret to" | Templated AI fingerprint |
| **Closed yes/no questions** | "Are you ready to transform your business?" | Triggers cynicism; nobody answers |
| **Symmetric emoji clusters** | "🚀✨💪" at line ends | ChatGPT-flavoured |

The agent **scans every caption draft against this table** before showing it to the user. Rewrites until clean.

## The AI-tells (refuse to ship copy that does these)

These are the patterns that immediately mark a caption as AI-generated. The agent treats them as hard fails and rewrites until none are present:

| Tell | Examples to refuse | Replace with |
|---|---|---|
| **Overly formal language / corporate jargon** | "leverage", "utilize", "ecosystem", "elevate", "synergize", "seamless" | Plain words: "use", "system", "lift", "work together", "smooth" |
| **Generic phrases** | "in today's fast-paced world", "in the realm of", "the power of X", "now more than ever" | Cut entirely. Open with something specific. |
| **Predictable structures** | every caption opening "Have you ever...", every CTA "Tap the link in bio" | Vary deliberately. Some captions need no CTA at all. |
| **Symmetric emoji clusters** | "✨🚀💪" at line ends, emoji-decorated bullet lists | Single emoji where it actually helps tone, max 2-3 per caption |
| **Closed yes/no questions** | "Are you ready to transform your business?" | Open: "what would you change if you knew nobody was watching?" |
| **Lack of specificity** | "amazing results", "game-changing", "next-level" | Concrete numbers, names, dates, places |
| **CTAs on every post** | "Comment below!", "DM us!", "Follow for more!" on every post | ~30-40% of posts have CTAs. The rest just *are* the post. |
| **Padding / filler openers** | "Let's talk about...", "Quick thought:", "Here's the thing:" | Cut the opener, lead with the point |

## What humans do that AI typically doesn't

- **Vary length unpredictably.** One caption is 8 words. The next is 4 paragraphs. AI averages.
- **Use line breaks for rhythm**, not just structure. Single-line beats. Strategic isolation of one line for emphasis.
- **Drop articles / use sentence fragments** — fine in social copy.
- **Reference specific moments** — "yesterday at the studio", "the third time this happened this month", "Sarah from Newcastle DM'd me about this"
- **Aside in parentheses** (often the most human-feeling thing in a caption)
- **One specific detail that has nothing to do with the post** — proves a human wrote it
- **Asymmetric formatting** — a list of 3 things where one item is twice as long as the others

## Caption structure patterns (use as starting points, not templates)

### The hook → beat → payoff (good for stories)

```
[1-line hook — specific, surprising, or contrarian]

[1-3 sentences setting up the situation]

[The shift / the reveal / the lesson]

[Optional: 1-line takeaway or open question]
```

### The list (good for educational / carousel companions)

```
[Specific framing — "5 things I'd do differently if starting again"]

→ [thing 1, one line]
→ [thing 2, two lines, with one specific detail]
→ [thing 3, one line]
→ [thing 4, three lines, slightly longer because this one matters more]
→ [thing 5, one line]

[Optional close — a question, a take, or just stop]
```

(Asymmetric line lengths matter. AI evens them out. Don't.)

### The single-sentence

```
[One sentence that does the whole job.]
```

Often the strongest caption. AI rarely produces these because it wants to keep generating. Resist.

### The reply-bait (use sparingly)

A specific question that someone with relevant experience can't help but answer. Not "what do you think?" — that's bait without specificity. Better: "what's the one thing you'd unlearn from your first year doing this?"

## Length per platform AND per surface

| Surface | Hard cap | Sweet-spot |
|---|---|---|
| **Hook** (any platform — slide 1, video first line, opener) | **10 words** | 5-8 |
| **Carousel slide copy** (slides 2..N) | **15 words per slide** | 8-12 |
| **CTA slide / line** | **10 words** | 4-7 |
| **Instagram caption** | 2,200 chars (platform limit) | 50-200 words |
| **TikTok caption** | 2,200 chars | 1-3 sentences |
| **LinkedIn caption** | 3,000 chars | 100-300 words; storytelling up to 500 |
| **Twitter / X** | 280 chars | Whole post |

The agent enforces the hard caps. If brand voice or topic genuinely needs more space, it splits across slides / posts — never overshoots a single surface.

**Why this matters (2026-05-06 test):** the first run produced essay-length blocks crammed onto carousel slides. People scroll. The cap forces the actual social-media format — short beats, one idea per slide.

## Voice transfer from brand profile

Every caption draft should pass these checks:

1. **Lexicon match** — does it use the words the brand actually uses (per `brand-profile-format.md` § Voice § Words / patterns to use)?
2. **Banned words check** — does it avoid the brand's banned-word list?
3. **Sentence-pattern match** — does it match the brand's typical sentence rhythm (per profile)?
4. **AI-tells scan** — does it pass the "tells" table above?

If any check fails, rewrite. The agent doesn't ship captions that fail these.

## CTA discipline

CTAs aren't bad — *every* post having one is bad. Decision tree:

- Educational / list / informational post → CTA optional ("save this for later" works if it actually helps)
- Story post → no CTA usually; let the story land
- Promotional / launch post → CTA required, specific (not "DM us!")
- Open-ended thought → end with a question, not a CTA

## Emoji discipline by platform

- **Instagram** — emojis fine, used as occasional punctuation, not decoration
- **LinkedIn** — minimal. One per post max, often zero. Bullet-point emojis (👉🔥💡) read as cringe.
- **TikTok** — playful emojis OK in caption, lots of `:)` energy
- **Twitter / X** — sparingly; emoji at end of line gives "AI tweet" energy

## When generating a caption, output BOTH:

1. **The polished caption** — ready to copy-paste-post
2. **A one-line note** explaining why this caption (which AI-tells were avoided, which brand-voice elements were applied)

The note is for the user to learn / refine; it's not part of what they post.

## Sources

`docs/ask-rag/ask-ads-marketing-9q.md` Q5. The MCP advice agreed with first-principles caption craft; this doc adds the specific AI-tells the MCP flagged + the platform-specific length/emoji guidance.
