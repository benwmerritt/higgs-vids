# Briefs

A brief is the input the agent reads to figure out what to make. They're conversational — one sentence is fine — but examples here show what works well for each pattern.

## Brief format

A brief is a markdown file. Required content:

- The creative ask in plain language. Any language the user is comfortable with.

That's it. The agent expands the brief into a structured shotlist using `references/brief-expansion-rules.md` and picks a pattern from `patterns/README.md`.

Optional structured fields the agent will use if present:

```markdown
# Brief: My Campaign

> **Pattern:** product-reel  ← optional explicit pattern selection
> **Aspect:** 9:16            ← override default
> **Budget cap:** 1000 credits ← refuses to start if estimate exceeds this
> **Workspace:** Acme         ← named workspace to charge

## Concept

[The actual creative ask, conversational]

## Reference assets (optional)

- `./products/bottle.jpg` — hero product photo
- `./brand-style/moodboard.png` — style reference

## Notes (optional)

- Anything you'd tell a director: "no people in shot", "must show the logo at the end", etc.
```

## Examples in this directory

| File | Pattern | Why |
|---|---|---|
| `example-retro-futuristic.md` | product-reel | The original brief from Timothée Oranger's Instagram reel — kept verbatim as the canonical test input |
| `example-product-reel.md` | product-reel | A clean, modern product-launch brief with explicit reference image |
| `example-quick-social.md` | quick-social | Single-still daily social post |
| `example-multi-platform.md` | multi-platform-render | One concept, three aspects |

## Tips

- **Don't pre-write the shotlist** unless you really mean to lock the agent in. Briefs work better when you say "what" not "how" — let the agent + patterns decide the shotlist structure.
- **Mention your audience** if it's distinctive — "for IG fitness audience" or "for B2B SaaS landing page" steer style choices.
- **Mention budget if it's tight** — saves you the cost-confirmation back-and-forth.
- **Drop reference images in the same folder** as the brief and link relatively, or use absolute paths.
