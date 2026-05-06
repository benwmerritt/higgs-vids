# Interview Craft — surfacing distinctiveness, not filling forms

> **The whole point:** if every brand answers the same form ("voice: casual, palette: warm, audience: 25-45 women"), every output looks the same. The interview's job is to find the **specific, weird, true things** about this person/brand that templated questions never surface. The agent uses those specifics to shape generation downstream.

## Philosophy

Bad interview question:
> "What's your brand voice — casual, formal, irreverent, or poetic?"

Why it's bad: every answer fits one of the four boxes. The output reads like one of four templates. Nothing distinct about it.

Good interview question:
> "Tell me about the moment a customer/follower really *got* what you do. What did they say, and why did that one stick with you?"

Why it's good: the answer is unique. It surfaces what they care about, who they're for, the specific language that resonates. The agent can ground every output in that real detail.

**Rule:** never ask anything answerable from a multiple-choice list of fewer than 100 options. If the answer is "casual" or "warm" or "Gen-Z women", you've not learned anything that makes them distinct.

## The interview shape (adaptive — not a script)

The agent runs an interactive interview, **one question at a time**, adapting to what comes back. There's no fixed list — there's a set of *territories* to cover, in roughly this order. If the user has already answered a question implicitly in a prior answer, skip it. If the user's answer reveals a more interesting branch, follow it.

### Territory 0 — Brand type (ask FIRST, then adapt the rest)

Open with a single question that determines how the rest of the interview branches:

> "Quick first thing — which of these is closest to what you're making content for?
>   • a personal brand (one human, your opinions and expertise)
>   • a small business with a product
>   • a service business or agency (consultancy, coaching, agency work)
>   • a content creator (entertainment-led, audience-first)"

Save the answer as `brand_type` in the profile. The remaining territories adapt:
- **personal_brand:** lean into the human's personal story, opinions, lived experience. Skip "company origin" — the brand is the person.
- **small_business:** ask about product, customer journey, team. Less personal-story, more "what does this product solve for whom".
- **service_agency:** ask about case studies, methodology, decision-makers (it's b2b — different audience model than consumer).
- **creator:** ask about format affinity, audience interaction style, niche / vibe.

If the user picks "all of these" or "I don't know", default to `personal_brand` and ask brand-type-specific questions opportunistically as they come up.

### Territory 1 — Who/what (the foundation)

Open with something disarming and outcome-oriented:

- "Tell me about yourself / what you do — like you're explaining it to a friend at a dinner party, not pitching it to investors."
- (If business) "What does the company do, and what's the *non-obvious* version of why it exists? The story behind it."

Listen for:
- The specific origin / pivot moment
- Words they use repeatedly (their actual lexicon)
- What they're *against* (often more revealing than what they're for)

### Territory 2 — The audience (specific, not demographic)

Bad: "Who's your target audience?"
Good:
- "Who's the most recent person who really got it / bought / followed? What were they like?"
- "Walk me through a real conversation you had with someone who became a fan — what did they ask, what made them lean in?"
- "When someone unfollows or doesn't get it, what kind of person are they usually?"

Listen for: the *specific* person. Not "25-45 women in fashion" — "Sarah, who runs a salon in Newcastle and got my newsletter from a friend." That specificity is what we'll write to.

### Territory 3 — The hook / the magnet

What makes them stop scrolling on this person, not the next one? Adaptive questions:

- "What's the one thing you'd say if you only had 5 seconds before someone scrolled past?"
- "What do you talk about that other people in your space *don't* — or that they avoid?"
- "What's a strong opinion you have that most people in your space would disagree with?"
- "If your account vanished tomorrow, what would your followers actually miss? Not 'good content' — be specific."

Listen for: the spike. The thing that makes the brand non-substitutable. **If they can't answer "what makes you different" with a specific story or specific opinion, the agent should keep asking until they can.** Generic answers ("we care more", "we're authentic") are signals to drill deeper, not accept.

### Territory 4 — Existing material (the auto-fetch shortcut)

This is where we save 30 minutes of asking. If the user has any of these, ask for them rather than re-asking the brand questions:

- A website URL → use `firecrawl_scrape` with `branding` format to extract their actual colors, fonts, typography. **Way more accurate than them describing "warm tones".**
- Existing IG / TikTok / LinkedIn → `firecrawl_scrape` recent posts. Extract: actual writing style, hashtag families, topic mix, format mix (carousel vs single vs video ratio), engagement signals.
- Recent newsletter / blog / interview → scrape for voice samples. Get their actual words.
- A doc / PDF / Notion page they use to onboard contractors or interns → priceless. Read it and skip 80% of the rest of the interview.

When fetched, **paraphrase what you learned back to the user** ("I see you write a lot about X, with a vocabulary of Y, and your most engaged posts seem to be about Z — true?"). They'll either confirm and you skip a chunk of the interview, or they'll correct you, which itself is information.

### Territory 4.5 — Aesthetic taste via reference

Before getting practical, ask one taste-revealing question:

> "Show me content (yours, a competitor's, anyone's) that you'd be proud to make. What about it works? And on the other side — content in your space that makes you cringe. Why?"

Listen for: the *specific* visual/copy patterns they admire, the specific things that put them off. This is one of the highest-information questions in the interview — it surfaces aesthetic taste, brand personality, and AI-content tells (if they cringe at "AI-looking content", that's a constraint we record).

If they share URLs or paths to specific posts, fetch / inspect those — they're the strongest reference material we'll get.

### Territory 5 — Constraints and don'ts (often the most important)

What we *won't* do is as defining as what we will. Ask:

- "Is there anything I should never produce for you? Topics, words, kinds of imagery?"
- "Has anyone in your space made content that made you cringe? What was wrong with it?"
- (If applicable) "Any compliance/legal — alcohol, gambling, healthcare, financial advice?"
- "Faces — anyone who must NOT appear, or only-with-permission?"

Listen for: the cringe-content answer. It tells you exactly what aesthetic / approach to avoid in their voice.

### Territory 6 — Assets (the practical bit)

Now you've got the substance, ask for the practical inputs:

- "Do you have logos? Where?"
- "Photos of yourself or talent? Roughly how many — 5, 10, 20?" (5+ unlocks Soul ID training)
- "Style references / moodboards?"
- "Product photos? (if applicable)"
- "Any existing posts you'd point to and say 'more like this'? File paths or URLs both work."

### Territory 7 — Format and platforms

Quick. Mostly multi-choice OK here, since this is mechanical:
- IG / TikTok / LinkedIn / Twitter / Pinterest / YouTube — pick all that apply
- Posting cadence rough estimate
- Most-used post format (single image / carousel / reel / story / mix)

### Territory 8 — The summary playback (BULLET POINTS, not paragraphs)

End by playing back what you've heard. **Format: bullet points, one per fact.** Not paragraphs. Not "here's what I've got" walls of text.

```
I think I've got an understanding. Here's what I heard:

- Name: Ben Merritt
- Where: Adelaide
- What you do: [specific, in their words]
- Differentiator (the spike): [specific, non-substitutable thing]
- Audience: [specific person, not demographic]
- Voice: [observed sentence patterns + lexicon]
- Don'ts: [their cringe-content list]
- Assets you've shared: [what's in /assets/ + Soul ID status]

Open questions I'd still want to dig into:
- [thing 1]
- [thing 2]
- ... (don't cap — list everything you didn't fully resolve)

Does this feel right? Anything missing, or should we move on to making content?
```

**Critical phrasing:**
- ✅ "I *think* I've got an understanding" — acknowledge the agent doesn't know what enough is
- ❌ "I've got enough" — sounds final and overconfident
- ✅ "Anything missing, or should we move on?" — gives the user the door to add more
- ❌ "Saving the profile now" — doesn't give them a chance

If they say "no, there's more" → keep interviewing. If they say "looks good" → save.

**Don't cap the open-questions list.** If the conversation surfaced 7 things that need more depth later, list all 7. The list is a TODO for future sessions, not a "here's a few things" courtesy.

## Question order rules

1. **Open with story, not specs.** "Tell me about yourself" before "what's your voice".
2. **Specifics before categories.** "Who's the most recent person who got it" before "who's your audience".
3. **Mine existing material before re-asking.** If they have a URL, fetch it first; questions become "is this still true?" instead of "what's true?".
4. **Drill into vague answers.** "We're authentic" / "we care more" → keep asking until you have a specific story or opinion.
5. **Mechanical questions last.** Logos, photo paths, platform list — last 3 minutes. Substance first.

## AI-tells the agent must actively avoid in any generated output

Per Ask Ads Marketing MCP knowledge (`docs/ask-rag/ask-ads-marketing-9q.md` Q5):

The patterns that immediately mark content as AI-generated:
- **Overly formal language / jargon** — "leverage", "utilize", "ecosystem", "elevate" — flag and replace with plain words
- **Generic phrases** — "in today's fast-paced world", "in the realm of", "the power of" — refuse to use
- **Predictable formulaic structure** — every caption opening with a hook formula, every CTA being "tap the link in bio" — vary deliberately
- **Lack of spontaneity / humor** — captions that read like LinkedIn-posts-as-a-service. Add specific details, asides, line-break rhythm
- **Closed questions or no questions** — "Are you ready to transform your business?" → bin. Open questions: "what would you change if you knew nobody would judge?"
- **Symmetric emoji clusters at line ends** — gives away ChatGPT instantly
- **CTAs on every post** — sometimes the post just is the post; no CTA needed

The agent should treat these as hard constraints when generating captions, slide copy, or any user-facing text. Refuse to ship copy that fits any of these patterns.

## What the agent should NEVER do

- Present the user with a multi-choice form. Even when the answer space is small (e.g. platforms), ask conversationally first; lists are fallbacks if they don't volunteer.
- Make them rank their values. Nobody knows what their values are when asked cold — they know stories, opinions, frustrations.
- Accept "we're like X but with [twist]" as a complete answer. Drill into the twist.
- **Inflate user statements.** If they said "I'd like to do 4 carousels", DON'T write "your goal is 4 carousels per week, posted every Monday" in the profile. Stick to what they actually said. Add nothing they didn't volunteer.
- **Fabricate hashtag families, colour palettes, or any field the user didn't address.** Mark `[gap]` and ask later instead of guessing. Test feedback (2026-05-06): the agent fabricated hashtag families and an explicit posting cadence the user never mentioned. Don't do this.
- **Assume visual decisions without asking.** If the user gave a logo and you extracted colours from it, that's good context — but DON'T lock in "dark theme" or "minimalist style" or any aesthetic direction without explicit confirmation. Ask: "I extracted these colours from your logo. How do you feel about going dark with this, or do you prefer light? Any reference brands you like the visual direction of?"
- Fill in the profile with assumed defaults. If a question wasn't answered, put `[gap — ask later]` in the profile rather than guessing.
- Move to generating content before the brand profile has a "spike" — at least one specific, non-substitutable thing.

## The "stick close to what they said" rule

The user's words go in the profile. The agent's interpretations go in `[brackets]` flagged as inferences:

✅ Good profile entry:
```
What you do: "Helping small studios scale without losing the founder's voice."
[inference: positions against agency-style scaling that produces generic output]
```

❌ Bad profile entry (inflated):
```
What you do: Empowering small creative studios to achieve sustainable growth
while maintaining authentic brand identity through founder-led storytelling.
```

The first version uses Ben's exact phrasing. The second is the agent's "improvement" of it — and now the brand voice is the agent's voice, not Ben's. **Always prefer the user's actual words.**

## Adapting on the fly

If during the interview you realize:
- They're a personal brand, not a business → drop the "company origin story" question, lean into personal story
- They're b2b, not consumer → audience question becomes about decision-makers and procurement triggers
- They're a creator with a strong existing aesthetic → spend more time on the auto-fetch + less on visual questions
- They've never thought about this stuff → slow down, give examples ("for instance, [Brand X] does [Y]"), let them react

The interview is a conversation about *them*, not a checklist about brands.

## Handing off

When the brand profile is written, the agent should also note in the profile:
- **Confidence level per territory** — how sharp is voice? audience? spike? Use these to decide whether the first content run is small (test) or full (proven).
- **Open questions** — anything that came up but wasn't resolved. Surface in the next session.
- **Source materials referenced** — paths/URLs of anything fetched, so future runs can re-fetch if context drifts.

This is what distinguishes "I have a brand profile" from "I have a brand profile that produces non-generic content."
