---
name: Redesigns require a content-preservation audit before HTML
description: Before drafting any HTML in a deck redesign, enumerate every named axis/column/list per source slide and confirm each is preserved. If anything is dropped, split slides or surface the cut.
type: feedback
originSessionId: f3b1bf3c-f294-4748-a10f-ad3aa8f6bb09
---
When redesigning a deck, run a **content-preservation audit** after the source→pattern mapping but **before** writing any HTML. The audit is not optional.

**The audit, per source slide:**

1. List every named axis, column, list, sub-section, callout, and sub-tagline on the source slide.
2. Confirm each one is preserved somewhere in the redesign outline.
3. If anything is dropped, either (a) split the source slide across multiple Metafore slides, (b) choose a different pattern that fits everything, or (c) surface the cut to the user and get explicit OK before drafting.

**You may not silently drop content because a pattern doesn't fit.** Slide count is flexible. Content preservation is not.

**Why:** On the May 2026 telecom corp redesign, I cut major content in four places without flagging: dropped the Problems + Value columns from the Offering slide, dropped the Enterprise Functions axis from the Industries slide, dropped the entire Tech/BPO sector + ~10 engagements from Case Studies, dropped the POLICY ENGINE callout from Governance. Each cut was rationalized as "pattern doesn't fit." That rationale isn't acceptable. The customer's source content is the customer's content; my job is brand application, not editorial.

**How to apply:**

Audit format — write a one-line check per source slide before drafting any HTML:

```
S04 (Offering) — source: Problems (4), Products (4), Value (9 bullets). → New 04 Problems, 05 Products, 06 Value. ✓
S16 (Industries) — source: Functions (5), Industries (9). → New 18 Functions, 19 Industries. ✓
S17 (Case Studies) — source: 6 sectors, 30 engagements. → New 20, 3x2 cluster grid with all 30. ✓
S13 (Governance) — source: 4 phases + POLICY ENGINE callout. → New 15, timeline + callout strip below. ✓
```

If any source-slide check has a missing item, fix the mapping. Don't proceed to drafting with a known gap. Splitting a source slide into 2–3 Metafore slides is the default move when the source carries multiple axes.

The 18-slide source → 16-slide redesign was wrong. The 18-slide source → 21-slide redesign (one slide per source axis) is correct.
