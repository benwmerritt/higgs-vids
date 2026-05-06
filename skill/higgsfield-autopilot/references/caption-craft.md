# Caption Craft

How the agent writes captions that read like a human wrote them, not an LLM. Distilled from `docs/ask-rag/ask-ads-marketing-9q.md` Q5.

> **Why captions matter:** the image stops the scroll, the caption decides whether they save / share / follow. A great image with a templated caption underperforms a good image with a great caption.

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

## Length per platform

These are guidelines from MCP advice, adapt per brand:

| Platform | Sweet-spot length | Notes |
|---|---|---|
| **Instagram** | 50-200 words for engagement; up to 500 for storytelling posts | First 125 chars show in feed before "more" — make those count |
| **TikTok** | Short. 1-3 sentences in caption (the video is the content) | Caption supports the video, doesn't replace it |
| **LinkedIn** | 100-300 words; longer storytelling 500-1500 words OK | Line breaks every 1-2 sentences. Big white space helps readability. |
| **Twitter / X** | Under 280 chars (forced); strong threads 7-12 tweets | First tweet is the hook; don't waste it on filler |

## Voice transfer from brand profile

Every caption draft should pass these checks:

1. **Lexicon match** — does it use the words the brand actually uses (per `brand_profile.md` § Voice § Words / patterns to use)?
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
