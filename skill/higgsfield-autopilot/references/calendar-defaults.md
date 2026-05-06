# Calendar Defaults

Per-brand-type weekly content calendars. Distilled from `docs/ask-rag/ask-ads-marketing-9q.md` Q8.

> Use these as **starting defaults** when a brand profile doesn't specify cadence/format-mix. They get overridden by anything in the brand profile or the user's stated strategy. Adjust based on engagement signals over time.

## Personal brand

One human, opinions and expertise.

| Aspect | Default |
|---|---|
| **Cadence** | 5-7 posts/week |
| **Format mix** | Reels: 2-3/week. Single-image: 2/week. Carousels: 1-2/week. Stories: daily. |
| **Topic mix** | 40% educational / 30% personal / 20% promotional / 10% entertaining |
| **Posting times** | Early morning + late evening (when audience is in scroll mode, not work mode) |

**Adjustment signals:**
- Educational posts outperforming → increase educational %, decrease personal
- Personal posts outperforming → audience values the human; increase personal storytelling
- Promotional posts underperforming → space them out further; lead with value first

## Small business with a product

| Aspect | Default |
|---|---|
| **Cadence** | 5-6 posts/week |
| **Format mix** | Reels: 2/week (product demos / customer testimonials). Single-image: 2-3/week (high-quality product shots). Carousels: 1/week (multi-product or feature). Stories: daily. |
| **Topic mix** | 50% promotional / 30% educational / 10% entertaining / 10% personal |
| **Posting times** | Mid-morning and early evening (peak shopping windows) |

**Adjustment signals:**
- Promotional → sales conversion: increase frequency on the converting types
- Educational performing well → use story polls to gauge product interest
- Customer feature posts → high engagement; build a UGC pipeline

## Service business / agency

| Aspect | Default |
|---|---|
| **Cadence** | 4-5 posts/week |
| **Format mix** | Reels: 1-2/week (client success / service highlights). Single-image: 1-2/week (team highlights / service offers). Carousels: 1/week (case studies / tips). Stories: daily (client interactions, Q&A). |
| **Topic mix** | 50% educational / 30% promotional / 10% personal / 10% entertaining |
| **Posting times** | Business hours — mid-morning and early afternoon |

**Adjustment signals:**
- Educational content drives DMs / inquiries → lean further educational
- Case study carousels save well → make them a weekly fixture

## Content creator

Entertainment-led, audience-first.

| Aspect | Default |
|---|---|
| **Cadence** | 5-7 posts/week (varies — creators often higher) |
| **Format mix** | Trend-driven; reels-heavy on TikTok and IG; format follows content type rather than fixed ratio |
| **Topic mix** | Format-led, not topic-led — varies with what's trending and what worked recently |
| **Posting times** | Test platform-specific peaks (TikTok evening, IG morning + evening) |

**Adjustment signals:**
- Trend-fit > consistency — drop topics that aren't performing fast
- Series content (recurring formats) outperforms one-offs over time

## Cross-cutting principles (apply to all brand types)

- **Stories daily, regardless of brand type** — they don't replace feed posts; they supplement
- **Test posting times within the first 4 weeks** — every audience is different
- **Re-evaluate the topic mix monthly** — engagement metrics tell you which slice deserves more
- **Don't blindly stick to a calendar** — when something is genuinely happening (launch, news, milestone), break the calendar to ride momentum

## How the agent uses this

When `/higgsfield-make` runs and the brand profile's cadence/format-mix is empty or marked `[default]`:
1. Read `brand_type` from profile
2. Apply the matching table above
3. Note in the run report: "Used calendar default for `<brand_type>` — refine in profile if your actual cadence differs."

When building a `content-week.md` pattern (future, v3.2): the agent uses this file as the structure and lets the user override per run.

## Sources

`docs/ask-rag/ask-ads-marketing-9q.md` Q8. The percentages and cadences are starting points from marketing knowledge; **engagement signals on the user's actual posts are the ground truth** for refining.
