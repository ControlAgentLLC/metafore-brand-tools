---
name: deck
description: Build Metafore-branded slide decks (sales decks, pitch decks, customer presentations, board decks, all-hands decks) as HTML drafts that generate editable PPTX. Use this skill whenever a Metafore teammate asks for a deck, slides, a presentation, a pitch, a customer-facing slide deck, "Metafore-ify this deck", or wants to turn a brochure, BRD, product spec, or markdown outline into slides — even if they don't say "deck" explicitly (e.g. "make slides for X", "I need a presentation", "turn this into a pitch"). Authors slide content in a compact YAML file rendered through 22 tested 1920×1080 patterns, lints it with a brand checker, then generates a PPTX where text is editable native shapes and complex graphics are embedded PNGs. Encodes Metafore brand invariants — two-tone hero, teal-only accent palette, three-font stack, back-of-room type floors, voice rules, Pulse vocabulary. Do NOT trigger for brochures (use `metafore:brochure`), internal dashboards (use `metafore:dashboard`), standalone graphics (use `metafore:graphic`), or DOCX documents.
---

# Metafore Deck Builder

Deliverables, side by side in `Decks/<deck-name>/`:
1. **`<deck-name>.yaml`** — what you author: slide content only, one entry per slide. This is the file you edit.
2. **`<deck-name>.html`** — the generated, self-contained preview (don't hand-edit or Read it).
3. **`<deck-name>.pptx`** — generated from the HTML. Editable text frames; locked visuals as PNG.

**Read first:** `../../assets/brand/metafore_brand.md` (voice, floors, density, visuals, tokens, content preservation, toolchain), then `references/deck-yaml.md` (the content-file schema). This file adds only deck-specific rules. Paths here are relative to this skill's directory.

## Workflow

0. **Redesigning an existing deck?** Follow `redesign/README.md` first (extract → map → audit → vocabulary pass + proposed edits), then continue at step 2.
1. **Understand the request** — purpose, audience, length (5–8 discovery, 15–25 board; push back above 25), source content, vertical (Mira only on telecom), cover variant.
2. **Outline** with one pattern per slide from the index below, as a flat list: `01 Cover (cover-1b) · 02 Agenda (agenda) · 03 Problem (statement) …`. Then:
   - **No pattern more than 2×** (3× only when structurally inevitable). A 15–20 slide deck should use 8–12 patterns. Reassign overflow to the next-best fit (4 items → modules subset, compare, or a statement with bullets; 3 layers → radial or arch).
   - If the content has N items, pick a pattern that holds N — never trim N to fit.
3. **Write `<deck-name>.yaml`** using the fields in `references/deck-yaml.md`. Only open a `references/patterns/P-XX-*.md` file when you need that pattern's finer rules or are writing a `raw` slide.
4. **Build, check, and generate in one command:**
   ```
   python3 scripts/build_deck.py Decks/<deck>/<deck>.yaml --check --pptx
   ```
   It writes the HTML, runs the checker (text report + one overview sheet in `_build/`), and builds the PPTX only when there are no errors. Fix errors with targeted edits to the YAML (never regenerate the whole file to change a slide) and re-run. Read the sheet **once** at the end for a visual pass.
5. **Optional Office check** (macOS, before sending): `python3 ../../scripts/office_check.py Decks/<deck>/<deck>.pptx` exports through PowerPoint itself and writes one overview sheet. If it reports a dialog, the user needs to click *Grant access* once for that folder.
6. **Deliver** the PPTX and point the user at the HTML preview.

**Deliberate rule-breaking** (training decks quoting banned words, "what's wrong" examples): add `ignore: voice` (or the relevant check names) to that slide, or use a `specimen`. The check counts what was waived. Overlap, overflow, retired colours and visible speaker notes can never be waived.

**Hand-written HTML** is still supported for one-off layouts: a `raw` slide inside the YAML, or a whole `<deck>.src.html` built with `../../scripts/build_html.py` (pattern files show the HTML; `data-label="…"` on a `<section class="slide …">` adds the chrome automatically). PPTX details: `references/pptx-build.md`.

## Pattern index

| ID | YAML `pattern` | Pattern | Use for | Tier |
|---|---|---|---|---|
| P-01 | `cover-1a/1b/1c` | Cover 1A / 1B / 1C | Slide 1, always | hybrid |
| P-02 | `divider` | Section divider | Phase change; 1–2 per deck | semantic |
| P-03 | `agenda` | Agenda | Slide 2 of decks > 8 slides | semantic |
| P-04 | `company / track` | Company / Track record | One "about us" slide | semantic |
| P-05 | `statement (quiz)` | Statement / Problem / Why | Land one message + supporting art | hybrid |
| P-06 | `grid4` | Capability grid 4-up | Exactly 3–4 parallel items with icons | hybrid |
| P-07 | `grid8` | Capability grid 8-up | 5–8 parallel items | hybrid |
| P-08 | `modules` | Module grid 12-up | 9–12 product items | hybrid |
| P-09 | `kpi` | KPI band | 2–4 hero metrics on teal | hybrid |
| P-10 | `integrations` | Integration ecosystem | What it connects to (pill clusters) | hybrid |
| P-11 | `timeline` | Timeline | 3–6 sequential phases | hybrid |
| P-12 | `radial` | Radial / knowledge graph | Topology, "one connected reality" | hybrid |
| P-13 | `closing` | Closing / CTA | Last slide, always | semantic |
| P-14 | `compare` | Two-column comparison | One real before/after (sparingly) | semantic |
| P-15 | `quote` | Pull quote | One per deck max | hybrid |
| P-16 | `arch` | Architecture | Platform layers | hybrid |
| P-17 | `hero-card` | Content hero + product card | "Here's what it looks like" | hybrid |
| P-18 | `scenario` | Scenario ("in action") | Cross-function story + UI card + trace | hybrid |
| P-19 | `team` | Team photos | Meet the team | semantic |
| P-20 | `table` | Wide data table | Capability → module mapping | hybrid |
| P-21 | `anchor` | Vertical anchor | Fit a vertical solution into the suite | hybrid |
| P-22 | `industries / vertical` | Industries (grouped / per-vertical) | Verticals served | semantic / hybrid |

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
- [ ] `build_deck.py --check` reports zero ERRORs; every WARN considered; waivers only on deliberate rule-breaking
- [ ] No pattern more than twice; Pulse cards structurally different from each other
- [ ] Every slide has `data-pptx`; `image` tier used at most 1–2×
- [ ] Every content slide has a `label` (auto chrome); cover, divider, closing get theirs automatically
- [ ] Agenda matches the final slide order; dividers' progress rail matches the agenda
- [ ] No typos in product names (Complexity, Multimodal, MetaWorks module names)
- [ ] `build_pptx.py` summary shows every slide with no warnings you haven't addressed
