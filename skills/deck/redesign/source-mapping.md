# Source mapping — manifest role → Metafore pattern

Turn each `slide-manifest.json` entry into a pattern ID from the index in `../SKILL.md` (details in `../references/patterns/`). Three passes, in order: **map → audit → variety**. All three happen before any HTML.

## 1 · Map

| Source role | Pattern | Tier | Notes |
|---|---|---|---|
| `cover` | P-01 | hybrid | 1B default (vision); 1A when the source opens on a metric or product render; 1C when it names/defines a thing |
| `agenda` | P-03 | semantic | Keep every item (up to 10; group into named sections beyond that — ask first) |
| `company` | P-04 | semantic | Keep every fact; org-chart photos → P-19 |
| `statement` | P-05 | hybrid | Keep the paragraph; at the type floor long copy becomes bullets or a split (propose the wording) |
| `capability-4` | P-06 | hybrid | One library icon per tile |
| `capability-8` | P-07 | hybrid | |
| `module-grid` | P-08 | hybrid | 9–12 items; more → split across two slides |
| `kpi` | P-09 | hybrid | Keep every metric — 5+ metrics → two KPI slides, or P-09 + P-20 |
| `integrations` | P-10 | hybrid | Logo wall → pill clusters with every name |
| `timeline` | P-11 | hybrid | 3–6 steps per slide; more → split into two timelines, don't collapse phases |
| `closing` | P-13 | semantic | Several CTAs → ask which one leads |

**Override heuristics** (when the contact sheet contradicts `role`):
1. Single big number or percentage → P-09.
2. Product UI screenshot with little text → P-17 (keep the screenshot as the locked card). Pure branding/chrome image → true chrome, cut.
3. Quote with attribution → P-15.
4. Before/after, old/new, us/them → P-14.
5. Load-bearing diagram → P-16 (or P-05 with the diagram as the locked art). Decorative diagram → replace with a library icon; keep the slide's text.
6. Situation traced across teams → P-18; vertical solution mapped onto the suite → P-21.
7. Industries list → P-22.

**Fit the pattern to N, never N to the pattern:**

| Items | Pattern |
|---|---|
| 2 | P-14, or P-05 with two stats |
| 3 | P-06 `.cols-3`, P-11 with 3 steps, or bullets on P-05 (a factual three is fine) |
| 4 | P-06 |
| 5–8 | P-07 (fill the first row first) or P-22 grouped with `--cols` |
| 9–12 | P-08 |
| 13+ | Split across two slides of the same pattern |

## 2 · Content-preservation audit (mandatory)

For every source slide, write one line listing each named axis, column, list, callout, and sub-tagline, and where it lands:

```
S04 (Offering) — Problems (4), Products (4), Value (9) → new 04 P-06, 05 P-06, 06 P-07 ✓
S16 (Industries) — Functions (5), Industries (9) → new 18 P-07, 19 P-08 ✓
S17 (Case studies) — 6 sectors, 30 engagements → new 20 P-22 (3×2), every engagement as a pill ✓
S13 (Governance) — 4 phases + POLICY ENGINE callout → new 15 P-11 + callout strip ✓
```

Any line without ✓: split the slide, re-pattern, or **ask the user before drafting**. Never drop content silently. Slide count is flexible — an 18-slide source becoming 21 slides is correct when it had axes to split.

**Only cut** true chrome (blank dividers, "thank you" placeholders with no content, "in this section" recap pages) — or when the user explicitly asks to compress. "Overlaps with another slide" and "the pattern holds 4" are not reasons. If the source is 30+ slides, ask: "Your source is 42 slides; Metafore decks usually land at 15–25. Compress, or keep your structure 1:1?"

## 3 · Pattern variety

Tally the outline. **No pattern more than 2×** (3× only when structurally inevitable). Reassign overflow to the next-best fit:
- 4 features with sub-points → P-08 subset, or P-05 with bullets
- 3 layers / components → P-12 radial or P-16 architecture
- 4 stages → P-11 if sequential, P-14 if paired
- "What we deliver" → P-20 table or P-05 with bullets

## Worked example

```
S01 cover            → 01 P-01 1B
S02 agenda (7)       → 02 P-03, all 7 items
S03 about us         → 03 P-04
S04 the problem      → 04 P-05 (dead-end grid art); source wording kept, 2 edits proposed
S05 the problem 2    → 05 P-05 dark (a different angle — kept)
S06 our solution     → 06 P-17
S07 4 features       → 07 P-06
S08 4 more features  → 08 P-07 (all 8 features; S07 keeps its own slide)
S09 by the numbers 5 → 09 P-09 (4) + 10 P-20 (the fifth with its context) — or ask
S10 customer logos   → 11 P-10, all 12 names
S11 roadmap (8)      → 12 P-11 (1–4) + 13 P-11 (5–8)
…
S21 thank you        → cut (chrome)
S22 q&a              → P-13
```
