---
name: deck
description: Build Metafore-branded slide decks (sales decks, pitch decks, customer presentations, board decks, all-hands decks) as HTML drafts that generate editable PPTX. Use this skill whenever a Metafore teammate asks for a deck, slides, a presentation, a pitch, a customer-facing slide deck, "Metafore-ify this deck", or wants to turn a brochure, BRD, product spec, or markdown outline into slides — even if they don't say "deck" explicitly (e.g. "make slides for X", "I need a presentation", "turn this into a pitch"). Authors slide HTML against a bundled pattern stylesheet at 1920×1080, lints it with a brand checker, then generates a PPTX where text is editable native shapes and complex graphics are embedded PNGs. Encodes Metafore brand invariants — two-tone hero, teal-only accent palette, three-font stack, back-of-room type floors, voice rules, Pulse vocabulary. Do NOT trigger for brochures (use `metafore:brochure`), internal dashboards (use `metafore:dashboard`), standalone graphics (use `metafore:graphic`), or DOCX documents.
---

# Metafore Deck Builder

Deliverables, side by side in `Decks/<deck-name>/`:
1. **`<deck-name>.src.html`** — what you author: slide HTML only, with placeholders for tokens, CSS, logos, icons, footers. This is the file you edit.
2. **`<deck-name>.html`** — the assembled, self-contained preview (built by script; don't hand-edit or Read it).
3. **`<deck-name>.pptx`** — generated from the HTML. Editable text frames; locked visuals as PNG.

**Read first:** `../../assets/brand/metafore_brand.md` (voice, floors, density, visuals, tokens, content preservation, toolchain). This file adds only deck-specific rules. Paths here are relative to this skill's directory.

## Workflow

0. **Redesigning an existing deck?** Follow `redesign/README.md` first (extract → map → audit → vocabulary pass + proposed edits), then continue at step 2.
1. **Understand the request** — purpose, audience, length (5–8 discovery, 15–25 board; push back above 25), source content, vertical (Mira only on telecom), cover variant.
2. **Outline** with one pattern per slide from the index below, as a flat list: `01 Cover (P-01 1B) · 02 Agenda (P-03) · 03 Problem (P-05) …`. Then:
   - **No pattern more than 2×** (3× only when structurally inevitable). A 15–20 slide deck should use 8–12 patterns. Reassign overflow to the next-best fit (4 items → P-08 subset, P-14, or a P-05 with bullets; 3 layers → P-12 or P-16).
   - If the content has N items, pick a pattern that holds N — never trim N to fit.
3. **Read only the pattern files you picked** (`references/patterns/P-XX-*.md`). Each has the HTML skeleton, limits, and common mistakes. The CSS already exists in `assets/patterns.css` — don't rewrite it.
4. **Author `<deck-name>.src.html`** from the skeleton below. Write slide HTML only. Per-deck CSS tweaks go in a short `<style>` after the includes.
5. **Build and check:**
   ```
   python3 ../../scripts/build_html.py Decks/<deck>/<deck>.src.html
   python3 ../../scripts/check.py Decks/<deck>/<deck>.html --kind deck --sheet Decks/<deck>/_build/sheet.png
   ```
   Fix every ERROR in the src file with targeted edits (never regenerate the whole file to change a slide), rebuild, re-check. Read `sheet.png` **once** at the end for a visual pass; `--zoom N` for a single flagged slide.
6. **Generate the PPTX:** `python3 scripts/build_pptx.py Decks/<deck>/<deck>.html` (details: `references/pptx-build.md`). It renders only image/hybrid slides, caches unchanged ones, and prints a one-line-per-slide summary — trust the summary; don't open the PNGs.
7. **Deliver** both files; point the user at the HTML preview and the PPTX.

## Source skeleton

```html
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Deck name — Metafore</title>
<!-- @fonts -->
<style>
/* @tokens:deck */
/* @css:deck/patterns */
/* per-deck tweaks (keep short) */
</style></head>
<body>
  <section class="slide p-cover-1b" data-pptx="hybrid" data-pattern="P-01"> … </section>
  …
  <section class="slide p-closing" data-pptx="semantic" data-pattern="P-13"> … </section>
</body></html>
```

**Chrome on every slide after the cover** (the closing slide uses its brandmark instead of the icon):
```html
<div class="section-label">The problem</div>                         <!-- add class on-dark on teal slides -->
<!-- @logo:icon-light width="72" height="60" class="icon-tr" -->       <!-- icon-dark on teal surfaces -->
<!-- @footer -->                                                         <!-- @footer on-dark on teal slides -->
```
`@footer` writes `© <current year> METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL` and the `NN / TT` page number — never type them by hand. The cover carries the full wordmark top-left (`@logo:logo-light` / `logo-dark`, 155×36) and the footer, but no section label or icon.

**Markup the generator reads:**
- `data-pptx="hybrid|semantic|image"` on every slide (tiers below). `data-pattern="P-xx"` lets the checker count pattern use.
- Text becomes editable frames automatically. Wrap locked product mockups (Pulse cards, glass cards, dead-end grids) in `data-pptx-lock data-decorative` — they stay baked and may use the 16px mockup floor.
- `data-visual` marks a structural visual (agenda grid, KPI band, timeline, table, progress rail) so the checker counts it.
- `<aside class="speaker-notes">…</aside>` inside a slide → PPTX notes.

## Pattern index

| ID | Pattern | Use for | Tier |
|---|---|---|---|
| P-01 | Cover 1A / 1B / 1C | Slide 1, always | hybrid |
| P-02 | Section divider | Phase change; 1–2 per deck | semantic |
| P-03 | Agenda | Slide 2 of decks > 8 slides | semantic |
| P-04 | Company / Track record | One "about us" slide | semantic |
| P-05 | Statement / Problem / Why | Land one message + supporting art | hybrid |
| P-06 | Capability grid 4-up | Exactly 3–4 parallel items with icons | hybrid |
| P-07 | Capability grid 8-up | 5–8 parallel items | hybrid |
| P-08 | Module grid 12-up | 9–12 product items | hybrid |
| P-09 | KPI band | 2–4 hero metrics on teal | hybrid |
| P-10 | Integration ecosystem | What it connects to (pill clusters) | hybrid |
| P-11 | Timeline | 3–6 sequential phases | hybrid |
| P-12 | Radial / knowledge graph | Topology, "one connected reality" | hybrid |
| P-13 | Closing / CTA | Last slide, always | semantic |
| P-14 | Two-column comparison | One real before/after (sparingly) | semantic |
| P-15 | Pull quote | One per deck max | hybrid |
| P-16 | Architecture | Platform layers | hybrid |
| P-17 | Content hero + product card | "Here's what it looks like" | hybrid |
| P-18 | Scenario ("in action") | Cross-function story + UI card + trace | hybrid |
| P-19 | Team photos | Meet the team | semantic |
| P-20 | Wide data table | Capability → module mapping | hybrid |
| P-21 | Vertical anchor | Fit a vertical solution into the suite | hybrid |
| P-22 | Industries (grouped / per-vertical) | Verticals served | semantic / hybrid |

A visual catalog of every pattern, rendered live from `assets/patterns.css`, is in `references/pattern-library.html` — for people; don't Read it (Claude works from the pattern files). Rebuild it after any CSS change with `python3 ../../scripts/build_html.py references/pattern-library.src.html`.

**Reference sequence** (MetaWorks corporate deck; deviate on purpose): P-01 → P-03 → P-04 → P-05 problem → P-06 four graphs (Meta → Knowledge → Context → Control) → P-05 suite intro → P-08 modules → P-07 platform → P-10 → P-09 → P-05 why → P-18 ×1–3 → P-21 (optional) → P-11 → P-13. Short decks drop the agenda, company, integrations, and timeline; 20+ slide decks add P-02 dividers and may use P-15 once.

## Deck-specific rules

**Tiers.** `hybrid` is the default — text over a baked illustration, every word editable. `semantic` for slides that are text plus simple shapes and icons (rebuilt natively, nothing rasterized). `image` only for slides that are 100% picture — more than 1–2 means text is being baked that should be editable.

**Type — size for the back of the room.** Body 32px; labels, eyebrows and the section label 24px; card and tile secondary text 22–24px; footer 22px; nothing essential below 22px. Content titles 56–64px, cover 112px, closing 88px. Titles fit two lines; when a line overflows, cut words or widen the well — never shrink. (Locked mockup text may drop to 16px.)

**Rhythm.** h2 → body gap ≥ 48px (36–40px only on P-18 / P-20). Header line-height 0.98–1.04 at hero sizes. Titles never end in a period — except the closing headline. Headlines in sentence case; agenda items are Title Case labels.

**Every slide carries a visual** — library icon, diagram, UI card, KPI band, pull quote, or a `data-visual` structure. A headline and a paragraph alone is an unfinished slide. Pull illustrations from the LineIcons library (`src="@icon:Name"`, index in `../graphic/references/line-icons-library.md`) before drawing SVG; one icon per tile, never repeated on a slide.

**Pulse cards vary.** If several slides show a Pulse card, each uses a different form — ranked feed, deal rows, metric bars, KPI grid, reasoning trace, single-headline + action. Cap mockups at 3 rows; strip timestamps-on-every-row, sparklines and "+10 more" footers. If a schematic could lose half its rows and say the same thing, drop them.

**Surface.** White-first; solid `--teal-dark` for dividers, KPI bands and dark stages — never patterned. Glassmorphism on the cover only; every other product card is solid white with a 1px `--line` border. No shadows, gradients, italics, bold heroes, underlines under titles, or slide animations.

**Logo.** Wordmark top-left on the cover only (light on white, dark on teal). Icon-only 72×60 top-right on every other slide, light/dark by what's behind it. Closing: large icon brandmark only.

**Inline SVG gotchas.** Pill rects need `rx` = half the height (`rx="999"` draws an ellipse). Hardcoded hex in SVG isn't reached by CSS variables — use `#006B6F` / `#88DCE0`, never `#00989E` / `#00C4CC`. Paste real Unicode (`×`, `−`, `—`), not entities, inside SVG `<text>`. Keep a literal space before a color span (`for the <span class="accent">enterprise</span>`).

**Deck voice.** Cover headline ≤ 6 words — the product or brand name, with the description in the subtitle. Statement slides ≤ 14 words of headline. One CTA on the closing. Slides amplify AI tells (the text is sparse) — apply the brand pack's list strictly to your own copy, and on customer decks flag rather than rewrite.

## Quality checklist (deck-specific; the brand pack's §7 also applies)

- [ ] Slide 1 is a P-01 cover with title + subtitle only; the last slide is P-13
- [ ] `check.py --kind deck` reports zero ERRORs; every WARN considered
- [ ] No pattern more than twice; Pulse cards structurally different from each other
- [ ] Every slide has `data-pptx`; `image` tier used at most 1–2×
- [ ] Footer via `@footer` on every slide; chrome icon/variant correct per surface
- [ ] Agenda matches the final slide order; dividers' progress rail matches the agenda
- [ ] No typos in product names (Complexity, Multimodal, MetaWorks module names)
- [ ] `build_pptx.py` summary shows every slide with no warnings you haven't addressed
