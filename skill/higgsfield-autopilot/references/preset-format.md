# Preset Format

A preset = `brand × pattern × platform × style tweaks` saved as a runnable shortcut. Built on top of an existing brand profile.

> Brand profiles capture *who you are*. Presets capture *how you typically use a specific content type for a specific outcome*. Together they let you say "/higgsfield-make --preset ben-carousels 'topic'" and get post-ready output without re-explaining anything.

## File location

```
presets/
├── ben-carousels.md           ← Ben's IG carousel preset
├── ben-week.md                 ← Ben's content-week preset
├── acme-launch.md              ← Acme's launch campaign preset
└── (etc.)
```

`presets/` is gitignored by default (because brand profiles are; presets reference them). User can override.

## preset.md template

```markdown
---
name: ben-carousels
brand: ben                   # references brands/ben/profile.md
pattern: carousel-post       # which existing pattern to wrap
platforms: [instagram, linkedin]
created: 2026-05-06
last_used: 2026-05-06
---

# Preset: Ben's IG Carousels

## Default arguments

slide_count: 6              # default; can be overridden per-run
aspect: 4:5                 # IG carousel native (portrait)
caption_length: medium      # short | medium | long — see brand voice for what these mean
caption_shape: list-format  # see brand profile § Voice § Caption shape
soul_id_use: optional       # required | optional | never (per shot, not per preset)
hashtag_families: [core, topic-design, local]

## Pattern-specific tweaks (override brand profile)

### Voice override (only if different from brand default)

[Empty if same as brand. Otherwise: "carousels are educational/list-format-heavy.
Less narrative than feed posts; lots of 1-line takeaways."]

### Visual override

[Empty if same. Otherwise: "carousel slides have wider negative space than feed posts
because they're swiped through, not glanced at."]

## Posting context

When this preset is typically used:
- [Tuesdays / Thursdays — when audience is in deep-focus mode]
- [Topic types: educational, listicle, opinion drops]

## Past runs (audit log)

| Date | Topic | Result | Notes |
|---|---|---|---|
| 2026-05-06 | "5 ways AI helps small studios" | runs/2026-05-06-1430/ | First run; carousel hit, caption needed manual edit on slide 4 |

The agent appends a row here after every successful run with this preset.

## Refinement notes (from past runs)

[Agent / user notes on what to do differently next time. Examples:]
- Slide 1 hook works best when it's a question, not a statement
- Avoid generic "tap to learn more" CTAs — Ben's audience finds them cringe
- Color palette: keep slides 1-2 high-contrast, slides 3-N can be calmer
```

## How the agent uses a preset

When `/higgsfield-make --preset ben-carousels "topic"` is invoked:

1. Read `presets/ben-carousels.md`
2. Read `brands/ben/profile.md` (referenced via `brand: ben`)
3. Refresh source-fetches if stale
4. Apply preset defaults (`slide_count`, `aspect`, etc.) unless CLI args override
5. Apply preset overrides (voice / visual tweaks) on top of brand profile
6. Run pattern (`../patterns/carousel-post.md`) with the merged context
7. After successful run, append to "Past runs" table
8. If user provides feedback, update "Refinement notes"

The result: each run with the same preset is consistent with the last run, and gets sharper over time as the refinement notes accumulate.

## Difference vs brand profile

| Brand profile | Preset |
|---|---|
| One per brand | Many per brand (one per content type / outcome) |
| Captures who you are | Captures how you typically execute a specific content type |
| Long-lived (refreshed quarterly) | Short-lived (evolves with each run via refinement notes) |
| Required for any content gen | Optional (you can run patterns without one) |
| Authored by interview | Authored by interview *or* extracted from a successful one-off run |

## Creating a preset from a successful one-off run

After a `/higgsfield-make` run that produced great output, the user can say "save this as a preset". The agent then:
1. Reads the run's brief, shotlist, output
2. Asks 3-4 questions to confirm preset values (slide count, voice tweaks, etc.)
3. Writes the preset file

So presets can come from interview OR from "I liked this, save it" — both flows produce the same artefact.

## Don't bake too much into a preset

A preset is a starting point. Each new topic still goes through the agent's normal generation flow — the preset just removes the re-explaining of stuff that's already known.

Things the preset SHOULDN'T encode:
- Specific topics (those vary per post)
- Specific captions (those vary per topic)
- Specific people-in-shot (use Soul ID + per-run choice)

The preset is the "frame" — the topic fills the frame.
