# Hook Craft

How the agent writes the first 1-2 seconds / first line of any post. Distilled from `docs/ask-rag/ask-ads-marketing-9q.md` Q4.

> The hook decides whether someone watches/reads the rest. Everything else in the post matters less than the first 1-3 seconds (video) or first line (text/carousel slide 1).

## Hook patterns that perform

### Conversational openers

Read like the start of a real conversation, not a polished ad.

- "No, because [specific opinion]…"
- "Okay, these are insane…"
- "Here's what nobody told me about [specific thing]"
- "I just realized why [thing] is broken"
- "Real talk: [specific take]"

**Why they work:** they feel like overhearing a friend, not being marketed to.

### Specific time + struggle

Numbers + duration + a specific problem.

- "I struggled with [thing] for 6 months before [shift]"
- "After 3 weeks of [doing X], here's what I'd change"
- "Year 1 of [thing]: 12 lessons I wish I'd known on day 1"

**Why they work:** specificity = credibility. Vague "I learned a lot" hooks die.

### Loss-aversion / curiosity triggers

Words that activate "wait what?" attention.

- "[Industry/practice]: it's a scam, and here's why"
- "Stop doing [common practice]. Here's what to do instead"
- "If you're [doing X], you're losing [specific thing]"
- "I almost lost [specific stake] because [specific mistake]"

**Why they work:** loss aversion is wired into us; "scam" / "stop" / "losing" pull eyes immediately.

### Controversial / contrarian opens

Take a position most of your space won't.

- "Hot take: [specific controversial opinion in your niche]"
- "Everyone in [industry] is wrong about [specific thing]"
- "[Common belief] is bad advice. Here's why."

**Why they work:** disagreement creates engagement (comments, debate, shares). Use carefully — must be actually true to your position, not bait.

### Visual hooks (video)

What the eye sees in the first 1-2 seconds:
- **Unexpected motion** in the first frame (a thing in motion already = attention-grabber)
- **Eye contact** if there's a person — direct camera look beats looking-elsewhere
- **Bright/contrasting color** that breaks scroll feed monotony
- **Text overlay** with the hook word visible immediately (for sound-off viewers)

### Comparison / before-after

- "What I ordered vs what I got"
- "[Cheap option] vs [expensive option] — actually different?"
- "POV: you're [specific scenario]"

**Why they work:** brain wants to compare; the format invites watching to the end.

### Insider language / specific subculture

Words that signal "I'm one of you" to a niche audience.
- For studio designers: "When the brief says 'just make it pop'"
- For founders: "The Series A vibe is wild right now"
- For [niche]: a phrase only [niche] would say

**Why they work:** in-group recognition = immediate trust + share-with-friends behavior.

## Hooks to refuse (AI tells)

| Bad hook | Why | Replace with |
|---|---|---|
| "In today's fast-paced world..." | Generic AI opener | Specific time/place: "Last Tuesday at 3pm I realized..." |
| "Are you ready to transform your business?" | Closed yes/no, salesy | Specific question: "What would you change if nobody was watching?" |
| "Let me share a thought..." | Padding, no info | Just say the thought |
| "Have you ever wondered..." | Overused, performative curiosity | Lead with the answer or the surprise |
| "The secret to [X]..." | Triggers cynicism in 2026 audiences | Specific result: "Here's what 6 months of [doing X] actually looks like" |
| "It's that time of year again..." | Filler | Specific event: "First frost hit yesterday and..." |
| "Quick thought:" / "Real quick:" | Filler, never quick | Cut and lead with the thought |
| "Check this out" / "You won't believe..." | Vague intrigue | Concrete: "I just watched [specific thing] and..." |

## Per-platform notes

### Instagram

- Hook is **slide 1 of carousel** OR **first line of caption + first half-second of video**
- Native-feeling visuals beat polished — IG users skip ads. Make it look like a friend's post.
- Mobile-first vertical (4:5 or 9:16). The hook word should be readable at thumb-scroll size.

### TikTok

- Hook is **first 1-2 seconds of video**
- Best-performing patterns:
  - "TikTok made me buy it"
  - "What I ordered vs what I got"
  - "POV: [specific situation]"
  - Direct camera + first words said matter more than visuals
- The video must *blend* with organic FYP content. Polished branded video = scroll past.

### LinkedIn

- Hook is **first 1-2 lines** before the "...see more" cut
- Industry-specific pain points work. Generic motivation does not.
- Demographics + family / specific roles outperform demographics-only
- Best openers: a specific number, a counterintuitive claim, a one-line story
- Don't open with a question (overused on LinkedIn 2024-2026)

### Twitter / X

- Hook is **first tweet of a thread** (or the whole post if standalone)
- Strong takes outperform hedged ones; specific examples outperform abstractions
- Numbers in the first tweet help: "I shipped 17 features last month. 3 mattered. Here's the pattern:"

## When the hook isn't working

If the brand's existing hooks underperform consistently:

1. Check the AI-tells table — is the brand's prior content using any?
2. Check specificity — vague hooks die. Add concrete numbers/names/places.
3. Check platform-fit — is it written for the platform's native style?
4. Check audience — is the in-group language right for THIS audience?
5. Test in pairs — write 2 hooks per post, A/B; the agent should be willing to generate alternates and ask the user to pick.

## Output shape from the agent

When generating any post, the agent produces 2-3 hook options for the user to pick from. **Each option ≤10 words. No em dashes.**

```
Hook options (pick one):

A) [conversational, ≤10 words]
B) [specific-time / number, ≤10 words]
C) [contrarian / loss-aversion, ≤10 words]

I'd pick B because [reason from brand profile].
```

The user picks; the agent finalizes the post around it. **Self-check before showing options:** did any option violate the hard rules above? If yes, regenerate that option.

## Real-world failure (2026-05-06 test run)

The agent shipped a 67-word "hook" with em dashes. That's not a hook. The hard cap and em-dash ban added above are a direct response. **A hook is one short scroll-stopping line, not a thesis statement.**

## Sources

`docs/ask-rag/ask-ads-marketing-9q.md` Q4. Cross-platform hook patterns from Meta Ads research, UGC creator advice, and LinkedIn-specific guidance.
