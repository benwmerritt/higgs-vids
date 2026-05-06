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

### Territory 8 — The summary playback

End by playing back what you've heard:

> "OK — here's what I've got. You're [specific summary]. Your audience is [specific]. The thing that makes you stop being a commodity is [specific spike]. You'll never produce [specific don'ts]. I'm going to write all of this to `brands/<name>/profile.md`. Anything I got wrong or want to add?"

If they correct anything, update and play back again. Don't save until they sign off.

## Question order rules

1. **Open with story, not specs.** "Tell me about yourself" before "what's your voice".
2. **Specifics before categories.** "Who's the most recent person who got it" before "who's your audience".
3. **Mine existing material before re-asking.** If they have a URL, fetch it first; questions become "is this still true?" instead of "what's true?".
4. **Drill into vague answers.** "We're authentic" / "we care more" → keep asking until you have a specific story or opinion.
5. **Mechanical questions last.** Logos, photo paths, platform list — last 3 minutes. Substance first.

## What the agent should NEVER do

- Present the user with a multi-choice form. Even when the answer space is small (e.g. platforms), ask conversationally first; lists are fallbacks if they don't volunteer.
- Make them rank their values. Nobody knows what their values are when asked cold — they know stories, opinions, frustrations.
- Accept "we're like X but with [twist]" as a complete answer. Drill into the twist.
- Fill in the profile with assumed defaults. If a question wasn't answered, put `[gap — ask later]` in the profile rather than guessing.
- Move to generating content before the brand profile has a "spike" — at least one specific, non-substitutable thing.

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
