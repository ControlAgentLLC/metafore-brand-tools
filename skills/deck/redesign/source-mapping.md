# Source mapping — extracted role → Metafore pattern

Translates each `slide-manifest.json` entry into a pattern ID from `../references/pattern-library.md`. Use this only after the extractor has produced a manifest.

The `role` field on each manifest entry is the lookup key. When `role` is ambiguous or the contact sheet contradicts it, override using the heuristics in the second table.

---

## Primary mapping table

| Source role          | Metafore pattern              | Default tier | Notes                                                                |
|----------------------|-------------------------------|--------------|----------------------------------------------------------------------|
| `cover`              | P-01 cover                    | hybrid       | Default to 1B (vision-forward). 1A only if source has a product UI render to feature. 1C for image-anchored covers. |
| `agenda`             | P-03 agenda                   | semantic     | Cap at **6 items**. See collapsing rules below.                      |
| `company`            | P-04 company                  | semantic     | Drop org-chart photos. Keep one-line positioning + 3–4 proof points. |
| `statement`          | P-05 statement                | semantic     | Dense source text → single Metafore sentence + Pulse-card art.       |
| `capability-4`       | P-06 capability grid (4-up)   | image        | One icon per cell, 1-line label + 1-line body.                       |
| `capability-8`       | P-07 capability grid (8-up)   | image        | Same as P-06 but denser. Trim labels to ≤3 words.                    |
| `module-grid`        | P-08 module grid              | image        | For 9–14 items. >14 → split into two slides.                         |
| `kpi`                | P-09 KPI band                 | image        | 3 metrics max. If source has 5+, pick the 3 with the highest delta.  |
| `integrations`       | P-10 integration pills        | image        | Logo wall → teal pill row. Drop logos we can't redraw cleanly.       |
| `timeline`           | P-11 timeline                 | image        | Cap at 5 milestones. Collapse sub-phases.                            |
| `closing`            | P-13 closing                  | semantic     | One CTA. Never two.                                                   |

Patterns P-02, P-12, P-14, P-15, P-16 are not in the default mapping — promote into them deliberately if the source's structure warrants it (e.g., source has a quote slide → P-12).

---

## Override heuristics (when `role` looks wrong)

Read the contact sheet, then apply these in order:

1. **Single big number / percentage on the slide** → force `kpi` (P-09), regardless of inferred role.
2. **All-image slide, minimal text** → if it's chrome/branding, drop the slide. If it's a product UI screenshot, keep as P-02 product spotlight.
3. **Quote with attribution** → P-12 pull quote (override whatever was inferred).
4. **Two-column compare ("before / after", "old / new", "us / them")** → P-14 comparison.
5. **Diagram with arrows / flow** → if the diagram is load-bearing, keep as embedded image in P-02. If it's decorative, drop and replace with P-05 statement.
6. **>14 bullets** → split across two slides of the same pattern, not one cramped slide.

---

## Content preservation — the default rule

**Preserve source content 1:1 unless you can articulate a non-aesthetic reason to cut.** The customer's deck is the customer's content; the redesign's job is brand application, not editorial. If the source has 5 use cases, 6 solutions, 9 industries — keep all of them. Find a pattern that fits the count; do not trim the count to fit the pattern.

This rule **inverts** the older "default to collapse" guidance. Aggressive trimming caused real misses on the May 2026 telecom corp deck (cut Leadership, Solutions, and Functional Architecture overview slides — each existed in the source for a reason).

**Default behavior:** Source slides become redesigned slides 1:1. Source items within a slide stay 1:1.

**Only cut when:**
- The source slide is genuinely empty (blank chrome page, "thank you" placeholder with no content, dead section break with no payload).
- The customer explicitly asks you to compress.

**Do NOT cut for:**
- "Overlaps with another slide" — different angles are not duplicates.
- "Three things to say is one too many" — pick a 3-up pattern, don't drop the third.
- "Pattern X fits 4 items" — pick a different pattern.

---

## Adjusting pattern to source count, not the reverse

When the source slide has N items, find a pattern that accommodates N:

| Source N | Preferred pattern |
|---|---|
| 2 | P-14 two-column comparison |
| 3 | P-06 capability-4 with one empty slot, OR 3-column bullet list, OR a 2-column statement with sub-points |
| 4 | P-06 capability-4 |
| 5 | P-07 capability-8 with 5 of 8 filled (3-2 layout), OR P-08 with 5 of 12 |
| 6 | P-07 capability-8 with 6 of 8 (3-3 or 4-2), OR P-08 module grid (3x2 within 12-slot frame), OR 2-column bullet list |
| 7 | P-08 module grid (3-2-2 or 4-3), OR custom 7-up cycle |
| 8 | P-07 capability-8 (canonical fit) |
| 9 | P-08 module grid (3x3 of 12 slots) |
| 12 | P-08 module grid (canonical fit) |
| 14+ | Split across two slides only if the items are genuinely independent. Otherwise the slide is overloaded and the source is asking too much. |

---

## Content-preservation audit — mandatory step before HTML drafting

After mapping every source slide to a pattern in your outline, **run a content audit before writing any HTML**. For each source slide, enumerate every named axis, column, list, sub-section, and callout. Confirm each one is present in the redesign. If anything is dropped, you must either:

1. Restore it by splitting the source slide across multiple Metafore slides, or
2. Restore it by choosing a different pattern that holds all of it, or
3. **Surface the cut to the user before drafting** and get an explicit OK.

You may **never** silently drop content because a pattern doesn't fit. Slide count is flexible; content preservation is not. A 21-slide redesign of an 18-slide source is correct if the source had axes that needed splitting. A 16-slide compression that hides content from the customer is wrong.

**Common source-slide shapes that require splitting in the redesign:**

| Source slide carries... | Redesign treatment |
|---|---|
| Two parallel axes (e.g., Functions × Industries) | Two separate Metafore slides, one per axis. Or a single slide with both axes if there's truly room. |
| Three sections (Problems / Products / Value) | Three slides — one per section. Or a dense 3-column slide if all three can breathe. |
| A grid + a callout / policy / framework note | Keep both: the grid + the callout as a strip below. Don't trim the callout. |
| A list of 6+ items + sub-bullets per item | Pick a pattern that holds the depth (2-col bullet list, cap-2x2, P-08 module grid). Don't trim sub-bullets to fit a 4-up. |
| A "by sector" grid with N pills total | Use the densest viable pattern (3x2 of clusters, or a 2-slide split). Don't drop pills or merge sectors to fit a 4-cluster layout. |

**Audit format:** Before drafting HTML, write a one-line check per source slide:

```
S04 (Offering) — source has: Problems (4 areas), Products (4), Value (9). → New 04 Problems, 05 Products, 06 Value. ✓
S16 (Industries) — source has: Functions (5), Industries (9). → New 18 Functions, 19 Industries. ✓
S17 (Case Studies) — source has: 6 sectors, 30 engagements. → New 20 Case Studies, 3x2 cluster grid with all 30. ✓
```

If any source slide ends with a missing item, restart the mapping for that slide. Don't proceed to drafting with a known gap.

---

## Pattern variety — no pattern more than 2×

After mapping every slide, count pattern instances. **No pattern should appear more than twice in one deck** (rare exception: 3× when structurally inevitable). If P-06 shows up four times in your outline, the deck is going to read as monotonous regardless of how good each slide is.

Force variety by reaching for the next-best pattern. The library has ~16 patterns for a reason — a 15–18 slide deck should exercise 8–12 of them, not 3.

Common reassignments when you've over-used P-06:
- "4 features with sub-points" → cap-2x2 (denser variant) or 2-column bullet list instead of cap-4
- "3 layers" → P-12 radial knowledge graph or P-16 architecture diagram instead of cap-4
- "4 stages" → P-11 timeline if sequential, P-14 comparison if paired
- "What we deliver" → P-05 statement with sub-points rather than another grid

Audit step before drafting HTML: tally the patterns, confirm the cap holds, reassign if not.

---

## Slide-count rule (revised)

The Metafore length target ("15–25 slides") is a **cap on bloat**, not a floor to hit. A faithful 18-slide redesign of an 18-slide source is correct. A compressed 16-slide redesign of an 18-slide source is wrong unless the user asked for compression.

The old guidance below applies **only** to source decks meaningfully longer than the target (30+ slides), where the source itself is bloated:

- Cut chrome slides — true blanks, "thank you" placeholders, navigational filler with no content.
- Cut "in this section" recap pages — Metafore decks don't recap themselves.

Even in those cases, ask the customer first: "Your source is 42 slides. Metafore decks land at 15–25. Want me to compress, or keep your structure 1:1?"

---

## Worked example

Source: a customer-supplied 22-slide deck. Manifest excerpt:

```
01 cover           → P-01 cover (1B)
02 agenda (7)      → P-03 agenda — merge "Setup" + "Onboarding" into "Setup"
03 about us        → P-04 company
04 the problem     → P-05 statement — rewrite, see voice-rewrite.md
05 the problem 2   → CUT (duplicate framing)
06 our solution    → P-05 statement
07 4 features      → P-06 capability grid (4-up)
08 4 more features → P-07 capability grid (8-up) — merge with 07
09 by the numbers  → P-09 KPI band (drop 2 of the 5 metrics)
10 customer logos  → P-10 integration pills (12 → 9)
11 roadmap (8)     → P-11 timeline — collapse to 5 milestones
...
21 thank you       → CUT
22 q&a             → P-13 closing
```

Result: 22 source slides → 17 Metafore slides. The deck got tighter, the brand got applied, and the customer's narrative is intact.
