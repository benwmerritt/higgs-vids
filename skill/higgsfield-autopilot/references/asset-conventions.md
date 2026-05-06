# Asset Conventions

How users provide brand assets, where the agent puts them, and how patterns reference them.

## Folder structure inside `brands/<name>/assets/`

```
brands/<name>/assets/
├── people/                     ← photos of person/talent (for Soul ID + general use)
│   └── <person-name>/          ← one folder per person if brand has multiple
│       ├── *.jpg
│       └── *.png
├── logos/
│   ├── primary.png
│   ├── primary.svg             ← if available
│   ├── monochrome.png
│   └── (variants)
├── style-guide/                ← moodboards, vibe references, competitor screenshots
│   ├── moodboard-1.png
│   └── reference-competitor.png
├── product/                    ← if applicable
│   └── <product-name>/
│       └── *.{jpg,png}
└── samples/                    ← examples of past content (the user's own posts) for tone reference
    └── *.{jpg,png,mp4}
```

## What goes in `samples/`

This is the **tone reference** folder — past posts, screenshots of content the user liked, examples of what they want more of. The agent doesn't generate from these, but reads them as visual context for tone-matching.

E.g. if the user drops 5 screenshots of their best-performing IG carousels into `samples/`, the agent uses them as visual reference when prompting for new carousels in the same brand.

## Photo requirements (people/)

For Soul ID training, per `references/known-issues.md`:
- **Hard floor:** 5 photos
- **Recommended:** 20+ photos, varied angles + lighting + expressions
- Quality: well-lit, face clearly visible, no sunglasses/hats
- Diversity: include frontal, ¾, profile; smiling and neutral

If user has 5-10 photos: train with `--soul-2` but warn about identity weakness.
If user has 20+: full quality.

## How to provide assets

The user can:

1. **Drop into the folder directly** — fastest, just copy files into `brands/<name>/assets/<subfolder>/`
2. **Point to existing paths** — during interview, agent asks "where are your photos?"; user gives a path; agent **copies** (not symlinks) into the brand folder so it's portable
3. **URLs** — user gives a URL to a photo / logo on their site; agent downloads it during interview
4. **Skip** — empty subfolders are fine; agent works without those assets and notes the gap in `confidence`

## Caching fetched material — `source-fetches/`

Separate from `assets/` because it's auto-generated, not user-provided:

```
brands/<name>/source-fetches/
├── homepage-2026-05-06.md       ← firecrawl scrape of brand website
├── instagram-2026-05-06.md      ← scrape of recent IG posts
├── linkedin-2026-05-06.md       ← scrape of recent LinkedIn
└── branding-2026-05-06.json     ← firecrawl `branding` format output (palette, fonts)
```

Filename convention: `<source-type>-<YYYY-MM-DD>.md`. Multiple dated copies allowed — the agent uses the most recent unless explicitly told otherwise.

The agent refreshes these when:
- > 30 days old
- The user's content style appears to have shifted
- The user explicitly asks: "re-fetch my IG"

## Format conventions

| Asset type | Preferred format |
|---|---|
| Logos | PNG with transparent background. SVG if available. |
| Photos | JPG (smaller) or PNG (lossless). Min 1080px on longest side for stills, 1920px for stuff that goes into video. |
| Moodboards | PNG, single image (collage) or multi-image folder |
| Existing posts (samples) | Whatever — JPG/PNG/MP4. Used as visual reference, not regenerated. |

## Privacy & version control

`brands/` is in `.gitignore` by default. Real assets stay local.

If the user wants their brand kit committed (open source project, public design system), they can:
- Add an exception: `!brands/<name>/profile.md` (commit the profile but not the assets)
- Or full override: `!brands/<name>/` (commit everything, accept that real photos are now in git history)

The agent never commits brand assets without explicit user OK per CLAUDE.md.

## Path references in profile.md and presets

Use **relative paths** rooted at the brand folder:

```yaml
photos: assets/people/ben/      ← relative to brands/ben/
moodboard: assets/style-guide/moodboard-1.png
```

Not absolute paths — the brand folder should be portable across machines (e.g. user copies it to a different repo or shares with a collaborator).

## When the agent uploads assets to Higgsfield

For Soul ID training and `--image` references in generation, the agent uploads via `higgs upload create <path>`. To minimize repeated uploads:

- After the first upload of a given file, save the upload UUID to `brands/<name>/assets/<subfolder>/.upload-ids.json`:
  ```json
  {
    "ben-1.jpg": "uuid-1",
    "ben-2.jpg": "uuid-2"
  }
  ```
- On subsequent runs, check the cache before uploading. Reuse UUIDs.
- If the file mtime is newer than the cached upload, re-upload (file changed).

## Don't

- Don't commit `brands/` without explicit user OK
- Don't use absolute paths in profile.md — breaks portability
- Don't auto-resize photos before Soul ID training — let the upstream service do quality control
- Don't let `assets/` and `source-fetches/` mix — keep auto-fetched material separate so users can re-curate their own assets without losing fetched context
