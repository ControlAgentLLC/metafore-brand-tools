---
name: deck
description: Build Metafore-branded slide decks (sales decks, pitch decks, customer presentations, board decks, all-hands decks) as HTML drafts that generate editable PPTX. Use this skill whenever a Metafore teammate asks for a deck, slides, a presentation, a pitch, a customer-facing slide deck, "Metafore-ify this deck", or wants to turn a brochure, BRD, product spec, or markdown outline into slides — even if they don't say "deck" explicitly (e.g. "make slides for X", "I need a presentation", "turn this into a pitch"). Authors in HTML at 1920×1080 (so the preview is pixel-perfect Metafore), then generates a PPTX where text is editable native shapes and complex graphics (covers, charts, glass cards) are embedded PNGs. Encodes Metafore brand invariants — two-tone hero, teal-only accent palette, three-font stack, voice rules, Pulse vocabulary — and the PPTX-specific divergences (no Plex Mono tracking, no negative letter-spacing under 22px). Do NOT trigger for brochures (use `metafore:brochure`), internal dashboards (use `metafore:dashboard`), standalone graphics (use `metafore:graphic`), or DOCX documents.
---

# Metafore Deck Builder

You are helping a Metafore teammate produce a brand-compliant slide deck. The deliverable is two files that ship together:

1. **`<deck-name>.html`** — a self-contained HTML file where each slide is a 1920×1080 frame stacked vertically. This is the design source of truth, the preview surface, and what the team iterates on.
2. **`<deck-name>.pptx`** — generated from the HTML. Editable text frames where the brand allows, embedded PNG renders where complex visuals would otherwise lose fidelity in PowerPoint.

The two stay in sync: the HTML is authoritative, the PPTX is built from it.

## Brand reference (read before producing)

Every Metafore artifact follows the same brand invariants. Before drafting, Read the shared brand pack at `../../assets/brand/metafore_brand.md` (voice rules, AI-tell blocklist, design tokens, type stack) and these deck-specific calibrations in the same folder:
- `feedback_deck_pattern_variety.md` — no pattern more than 2× per deck
- `feedback_capability_grid_eyebrows.md` — single `--teal` for P-06/P-07/P-08 eyebrows
- `feedback_redesign_preserve_content.md` and `feedback_redesign_audit_step.md` — content-preservation rules for redesigns
- `feedback_oversized_pngs.md` — keep verification PNGs under ~2000px

These supersede anything older you may have seen.

## The two invariants that bookend every deck

1. **Open with a Type 1 cover.** The first slide is always one of the three blog-hero formats from `metafore:graphic`: **1A** (split white / teal-light with data card), **1B** (full teal with glass UI card), or **1C** (split white / solid teal with color-accent term). The Metafore SVG wordmark sits in the **top-left** at `var(--logo-offset)` (~56px) — light variant on white panels, dark variant on `--teal-dark` panels.
2. **Close with a closing slide.** Either a CTA + Metafore wordmark, or a footer-style "Powered by Metafore" line. Never end on a content slide.

**Cover text is minimal — title and subtitle only.** No eyebrow, no lede paragraph. The opening slide should feel spacious. Save the supporting copy for slides 2+ where it earns its place.

Everything between those two anchors is content-driven. There is no fixed template count — a discovery deck wants three slides, a board deck wants twenty.

## Optional slides — include when the deck warrants them

Three optional templates round out a corporate intro deck. Include them when the audience needs orientation; skip them when the deck is short or purely product-focused.

| Template | When to include | When to skip |
|---|---|---|
| **Agenda** (slide 2 by convention) | Decks >8 slides; new-prospect intros; multi-section pitches where the audience benefits from a roadmap | Short discovery decks, internal reviews, single-topic pitches |
| **Company** (typically slide 3) | New-prospect intros; investor decks; first-meeting material where the audience doesn't know Metafore | Existing-customer decks, product-only reviews |
| **Platform capabilities** | Decks where the audience cares about *how* the system works (CIO/CAIO, technical buyers) | CEO-only intros, outcome-focused customer decks |
| **Integration ecosystem** | Decks where the audience cares about *what it connects to* (procurement, IT, technical evaluation) | Vision/strategy decks, executive-overview material |

Default to including all four for a full corporate intro deck. Pare back for shorter formats.

## Vertical-anchor slides — fitting a vertical solution into the suite

Vertical solutions (an airline IROP orchestrator, a bank customer-service agent) don't map cleanly onto the 12-block "digital C-suite" story. Use a **vertical-anchor slide** to bridge: it names the vertical solution, declares which MetaWorks module it *anchors into* via an `ANCHORS INTO → MetaWorks <Module>` badge, and shows three surface tiles for how the solution spans modules (primary surface + adjacent surfaces). It derives from the "in action" layout (header + scenario + three trace tiles + source chips), minus the UI card. One per vertical, placed right after the "in action" example slides. Full spec in `references/pattern-library.md` (vertical-anchor pattern).

## Chrome alignment — corner offset, not content padding

All slide chrome — section label, icon, footer copyright, page number — aligns to the corner at `var(--chrome-offset)` (36px from each edge). The content well lives inside the wider `var(--slide-pad-x)` (120px) padding.

This separation matters: the chrome reads as a quiet frame around the slide, the content well sits inside it with room to breathe. Don't put chrome elements at content padding — they look indented.

## The four chrome elements — every content slide

Every slide after the cover carries the same four corner-aligned elements:

| Position | Element | Notes |
|---|---|---|
| **Top-left** | Section-label eyebrow (`THE PROBLEM`, `THE SUITE`, `ARCHITECTURE`) | Plex Mono uppercase tracked, 18px, `var(--teal)` |
| **Top-right** | Icon-only mark (`icon-light.svg` or `icon-dark.svg`) | 72×60 |
| **Bottom-left** | `© <YEAR> METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL` | Plex Mono uppercase tracked, 13px |
| **Bottom-right** | Page number `03 / 12` | Plex Mono uppercase tracked, 13px |

**The year is always the current year** — at time of writing, 2026. Decks built next year use 2027. Do not hard-code 2025.

On `--teal-dark` slides, color is `rgba(255,255,255,0.55)` for the footer and `rgba(255,255,255,0.7)` for the section label. On light slides, `var(--ink-3)` for footer and `var(--teal)` for the section label.

The cover is the exception: it uses the full wordmark top-left (not the section label), and the eyebrow lives inside the content well, not at corner chrome. It keeps the footer.

## The three slide tiers — the central design decision

Every slide is tagged with `data-pptx="image" | "semantic" | "hybrid"`. This tag drives how the PPTX generator handles the slide.

| Tier | When to use | PPTX output | Editable in PowerPoint? |
|---|---|---|---|
| **`semantic`** | Pure-text compositions — section dividers, closing CTA, agenda. No illustration or chart in the layout. | Native PPT text frames + shapes, parsed from the HTML structure | Yes — every text node |
| **`hybrid`** | The default for almost every slide. Text composed over an illustration / diagram / chart that's part of the background. Capability grids, KPI bands, modules, integrations, timelines, statements with right-side art. | Editable text frames overlaid on a background PNG of the locked composition | Yes for all text — illustrations locked |
| **`image`** | Reserve for slides that are 100% visual — a single rendered diagram, a pull-quote graphic, a screen capture with no body text. Rare. | Full-bleed PNG screenshot of the HTML frame | No — picture |

**Default to `hybrid`.** If a teammate would ever want to edit a word on the slide (a KPI number, a card title, a label), that word must be a text frame — not baked into the image. `image` is the exception, not the rule.

When in doubt: ask "could the customer want to edit this label?" If yes → `hybrid`. If the whole slide is a single composition → `image`. If there's no illustration at all → `semantic`.

## Authoring the HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Deck name — Metafore</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    /* Paste assets/tokens.css verbatim here */
  </style>
</head>
<body>

  <!-- Slide 1: cover, hybrid tier -->
  <section class="slide" data-pptx="hybrid" data-slide-id="cover">
    <!-- Cover content per references/cover-recipes.md (1A | 1B | 1C) -->
  </section>

  <!-- Slide 2: section divider, semantic tier -->
  <section class="slide" data-pptx="semantic" data-slide-id="01-intro">
    <!-- ... -->
  </section>

  <!-- ...more slides... -->

  <!-- Final slide: closing, semantic tier -->
  <section class="slide" data-pptx="semantic" data-slide-id="closing">
    <!-- ... -->
  </section>

</body>
</html>
```

**Editable-text markers.** On hybrid slides, mark every text node that must become a native PPT text frame with `data-pptx-text="<role>"`. Roles map 1:1 to PPT shapes:

```html
<div class="eyebrow" data-pptx-text="eyebrow">DEFINITION · METAFORE FOR TELECOM</div>
<h1 data-pptx-text="headline">
  Cognitive agents for <span class="accent" data-pptx-accent>every subscriber</span>
</h1>
<p data-pptx-text="lede">Mira is the personal AI twin deployed in carrier IMS…</p>
```

The generator reads these elements' computed bounding boxes to position the equivalent PPT text frames.

## Design tokens

Live in `assets/tokens.css`. Inline verbatim into every deck's `<style>` block. Same teal stack, same three-font stack, same status colors as the rest of the Metafore system. The deck-specific additions are slide-canvas variables:

```css
--slide-w: 1920px;          --slide-h: 1080px;
--slide-pad-y: 96px;        --slide-pad-x: 120px;
--logo-offset: 56px;
```

**Single accent family.** Teal stack only. No mint, no accent blue, no warm tone. Status colors are for state, not decoration.

**White-first canvas.** Default `#FFFFFF`. Saturated teal (`#004D50` / `#006B6F`) is a deliberate accent block — a KPI band, an outcome commitment, the hero's second word, a section divider background.

## Logo — two marks, different placement on cover vs. content

Four canonical SVGs in `assets/`:

- **`logo-light.svg`** — full wordmark, light-bg variant. Use on light surfaces.
- **`logo-dark.svg`** — full wordmark, dark-bg variant (white@50% curves + full-white marks/wordmark). Use on `--teal-dark` surfaces.
- **`icon-light.svg`** — icon-only mark (just the two double-curves, no wordmark), light-bg variant. Native viewBox 43×36.
- **`icon-dark.svg`** — icon-only mark, dark-bg variant. Native viewBox 43×36.

**Placement rule** — deck convention:

| Slide type | Mark | Position | Size |
|---|---|---|---|
| **Cover (1A / 1B / 1C)** | Full wordmark | **Top-left**, `var(--chrome-offset)` (~56px) from both edges | `width="155" height="36"` |
| **Every other slide** (content, divider, closing) | **Icon-only** | **Top-right**, `var(--chrome-offset)` from both edges | `width="72" height="60"` |

The cover uses the full wordmark to anchor the brand at the opening. Every subsequent slide uses the icon-only mark — quieter, recurring, doesn't fight with the content. The closing slide uses the icon too (mirrors content-slide convention rather than the cover).

**Never** substitute CSS pseudo-element constructions of two quarter-circles. **Never** put the dark variant on a light surface or the light variant on a dark surface — the choice is determined by what's behind the mark, not by aesthetic preference.

In the PPTX, every SVG is converted to PNG at 2x and placed as a native picture shape:
- Cover wordmark → 310×72 PNG at top-left.
- Content-slide icon → 96×80 PNG at top-right.

## Typography — three fonts, three roles

| Role | Font | Notes |
|---|---|---|
| Headers, hero, slide titles | `var(--header)` (Geist → Inter fallback) | **Weight 400 only.** Never bold. Never italic. Size carries weight. Sentence case, not title case. |
| Body, lede, bullet text | `var(--body)` (Inter) | Weight 400–500. |
| Eyebrows, KPI labels, page numbers, footer line, all-caps tracked labels | `var(--mono)` (IBM Plex Mono) | **Always uppercase, always tracked +1.0 to +1.6px in HTML.** Keep eyebrow casing consistent across the deck — all caps everywhere. Exception only for a deliberate special-case slide. **In PPTX: no letter-spacing, no bold.** |

**Size for the back of the room.** Decks are presented in conference rooms at 6–25 ft — increasingly in person and abroad. Size for the back row, not the laptop. Floors: **body ≥ 28px, secondary text / labels / eyebrows ≥ 22px, nothing essential below 20px.** Cover hero typically 112–128px. Section-divider hero around 72–88px. Content-slide title around 48–64px. Body 28–32px on slides. When a larger size makes a line wrap or overflow, fix the layout (shorter copy, wider well) — don't shrink below the floor.

**Negative letter-spacing on headers only above ~22px.** Below that, tracking stays at 0. The PPTX generator enforces this.

## PPTX-specific brand rules

These divergences from the HTML-side rules are non-negotiable. The generator applies them automatically when writing the .pptx.

- **No letter-spacing on Plex Mono in PPTX.** Strip it. (The HTML eyebrow uses 0.16em tracking; the PPT text frame uses 0.)
- **No bold on Plex Mono in PPTX.** Plex Mono in PPT is always weight 400, regardless of what the HTML says.
- **No negative letter-spacing under 22px (~16pt).** Clamp to 0.
- **No drop shadows on any shape.** Even if PPT defaults to a shadow on a new text box, remove it.
- **Two-tone hero requires run-splitting.** A headline with `<span class="accent">` becomes a single text frame with two runs: ink (`#1A1A1A` or `#0A0A0A`) and `--logo-dark` (`#035657`). Never two separate text frames.

Full rule list in `references/pptx-rules.md`.

## What never appears

- Gradients on text, backgrounds, or borders
- Drop shadows on slide elements
- Italic anywhere (especially headers)
- Bold hero text
- Underlines or accent-bar decorations under titles
- Centered body copy (left-align everything except certain quote/KPI band layouts)
- A second accent color outside the teal stack
- The retired teal accents `#00989E` ("teal-accent") and `#00C4CC` ("teal-bright") — both are low-contrast. Accents/strokes/labels use `--teal #006B6F` on light surfaces, `#88DCE0` on dark; two-tone hero uses `--logo-dark #035657` on light, `#88DCE0` on dark.
- Light teal or grey as **essential** text — `#00989E`, light greys, `--teal-light` are for decoration or deliberately-muted/inert elements only (e.g. the "dead dashboard" cards on the problem slide), never for accent text, labels, or KPI numbers the audience must read across a room.
- "Dashboard" — always "Pulse"
- **Trailing periods on slide titles** — h1/h2/hero never ends in `.` *except on the closing slide* (P-13), where the final headline takes a period as a deliberate full stop. Every other slide drops it. See pattern-library.md → universal invariants for the full rule.
- Slide numbers in serif or with periods (use Plex Mono `01 / 12` format in the bottom-right footer)
- Slide numbers top-right (they live in the footer, bottom-right, since the logo occupies the top-right corner)
- Background curve/wave motifs on dark slides (no, the surface stays solid `--teal-dark`)
- Page-turn animations, fly-ins, builds — none. Decks are static.

## Illustrations — library before generation

For company / team / "proven track record" slides that want minimal abstract line-art illustrations, **pull from the LineIcons library before drawing your own SVG**. The library has 29 approved icons (`Process`, `Collaborate`, `Connect`, `Axis`, `Transform`, `Integration`, `Venn`, etc.) bundled with this plugin at `../../assets/graphics/line-icons/`. Full concept index at `../graphic/references/line-icons-library.md`.

**Bootstrap step (first run in a working directory):** if `Graphics/LineIcons/` does not exist next to the deck HTML, copy the bundled icons there once so the deck HTML's `<img src="Graphics/LineIcons/<Name>.png">` references resolve when the file is opened. After that, reuse the working-directory copy.

Reference an icon in the deck HTML as a relative-path `<img>`:

```html
<div class="f-graphic" aria-hidden="true">
  <img src="../../Graphics/LineIcons/Process.png" alt="" />
</div>
```

The build pipeline (Playwright) resolves the relative path during rendering. Don't recolor library icons; don't redraw an icon the library already has. Only generate new line-art when no library icon fits the concept — and when you do, follow the visual language documented in the LineIcons library spec so it can be promoted.

## When a baked SVG schematic gets too dense, do less

Inline SVG mocks (Pulse cards, reasoning traces, dependency graphs) accumulate detail naturally — KPI sub-numbers, hop timings, sparklines, confidence bars, action panels, CTA pills. Density is good, *until* the surrounding context (header, scenario paragraph, trace tiles) already explains what the schematic is showing. Then the schematic competes with the text instead of supporting it.

The "do less" check: if the schematic *could* survive losing half its rows and still communicate the same concept, drop the rows. Specifically:

- Cap UI cards at **3 KPI rows / signal rows / deal rows / metric bars**. Beyond that, the card reads as a real product screenshot rather than a marketing schematic.
- Strip secondary instrumentation (timestamps on every row, sparklines next to KPIs, "+10 MORE · GROUPED BY SOURCE" footer text) — these belong in the product itself, not the marketing slide.
- Keep the *conceptual core* — the 3-phase REFLEX/REFLECT/RESOLVE loop, the hub-and-spoke, the central node — and let the surrounding text do the lifting.

When a schematic was just simplified, regenerate the verify PNG and double-check the slide still tells the same story. If the slide felt complete before and incomplete after, you went too far.

## Pulse UI cards — vary across slides

If a deck uses Pulse UI cards on multiple slides (P-05 problem, P-17 content hero, P-18 scenarios), each card must show a **structurally different Pulse view**. Three KPI lists in a row read as one slide repeated. Mix the card forms:

- Ranked feed (vertical signal cards with HIGH / WATCH / NORMAL badges)
- Deal/account row list (ID + name + value + delta)
- Risk metric bars (label + bar + value)
- KPI grid (3 stat cells in a row)
- Reasoning trace (3 phase nodes connected by dashed lines)
- Single-headline view (title + 2 stats + recommended action card)

Each form belongs to one slide in the deck. Don't put two ranked feeds back-to-back, even with different content.

## Cover headline = brand/product name, subtitle carries the description

P-01 cover decks open with the brand or product name as the hero, and use the subtitle to carry the descriptive phrase. Don't stack a long descriptive headline at the top — it dilutes the cover and competes with the rest of the deck for attention.

```html
<!-- Right -->
<h1><span class="line">Introducing</span><span class="line"><span class="bracket">MetaWorks</span></span></h1>
<p class="subtitle">The enterprise operating system that thinks, acts, and builds</p>

<!-- Wrong -->
<h1>The enterprise operating system that thinks, acts, and <span class="bracket">builds</span></h1>
<p class="subtitle">Every function sees the same reality.</p>
```

The cover is the product name moment. Save the descriptive sentence for slide 2 or for the subtitle.

## Voice — preferred vocabulary

These are positioning, not stylistic preference.

| Use | Not |
|---|---|
| **Pulse** (define on first use as "a live, role-scoped operating view assembled from widgets") | dashboard |
| Cognitive agents | AI bots, chatbots, virtual assistants |
| Orchestration | automation |
| Knowledge fabric, enterprise knowledge graph | data layer, data warehouse |
| Sense, reason, and act | detect, process, respond |
| Self-evolving | self-learning |
| Amplify human intelligence | replace humans |
| AI transformation partner | vendor, provider, supplier |
| Enterprise General Intelligence (EGI), Enterprise Operating Platform (EOP) | generic AI platform |

**Mira** is the personal-agent product for telecom subscribers only — never use Mira naming on banking, wealth, travel, health, or supply chain decks. Renamed from Echo on 2026-04-24.

**Metafore One** is the platform product. **MWC Barcelona March 2026 is in the past** — never pitch it as forward-looking.

## AI writing tells — zero tolerance

Same Elana-flagged blocklist as every Metafore deliverable:

- **No "isn't X. It's Y."** negation-pivot. Most-flagged pattern.
- **No "X, not Y"** inline contrasts.
- **No triplet structural lists** — three parallel items / sentences. Use 2 or 4.
- **No staccato fragment sentences** — join with commas, em dashes, conjunctions.
- **No department roll calls** — "Customer service runs X. Network ops has Y. Billing has Z."
- **No "compounding / fundamentally different / impactful / collectively unintelligent / leverage / synergy / disrupt / seamless / end-to-end / solutions"** — AI comfort words.
- **No neat parallel opposition** — "scaling costs without scaling returns".

Slides amplify these tells because text is sparse and structural. A triplet bullet list on a slide is twice as visible as the same triplet in a brochure paragraph. Use 2 or 4 bullets.

## The cover slide — picking 1A, 1B, or 1C

Three Type 1 covers, all adapted to the 1920×1080 slide canvas. Full recipes in `references/cover-recipes.md`.

| Cover | When to use | Logo variant | Editable text overlays |
|---|---|---|---|
| **1A** — split white / teal-light + data card | Decks where a hard metric or before/after data is the opening argument. Use when you can show evidence in the cover. | Light (top-left of white panel) | Eyebrow, headline, accent span, lede on the left panel |
| **1B** — full teal + floating glass card | Brand-forward decks, vision decks, product launches. Use when the hero is positioning, not data. | Dark (top-left of solid teal) | Eyebrow, headline, accent span. Glass card content stays in the rendered image. |
| **1C** — split white / solid teal with accent-term hero | Definitional decks — "What is X", "Introducing Y". Use when the cover is naming a thing. | Light (top-left of white panel) | Eyebrow, headline (with accent term span), subtitle, lede |

The cover decision usually follows from the input content. A pitch deck with a "we cut handling time 47%" thesis → 1A. A product launch deck → 1B. A platform-introduction deck → 1C.

## Generation pipeline — HTML → PPTX

Documented step by step in `references/generation-pipeline.md`. Summary:

1. **Draft** the HTML deck following the templates. Tag every slide with `data-pptx`. Tag editable text nodes on hybrid slides with `data-pptx-text` and `data-pptx-accent`.
2. **Preview** by opening the HTML in a browser — slides stack vertically, you scroll through them.
3. **Render** image and hybrid slide backgrounds via headless Chrome (Playwright). For hybrid slides, render a copy where editable text nodes are `visibility:hidden` so their layout is preserved but the pixels are blank — that's the background PNG.
4. **Measure** bounding boxes for every `data-pptx-text` node by reading `getBoundingClientRect()` in the same Playwright session. Persist as JSON keyed by slide id.
5. **Build** the .pptx with python-pptx: 13.333" × 7.5" widescreen, one slide per `<section class="slide">`, full-bleed PNG for image tier, native text frames at measured coords for semantic + hybrid tiers, run-split for two-tone hero, Plex Mono tracking stripped.
6. **Verify** by opening the .pptx and confirming text is editable where expected, fonts render (Geist/Inter fall back gracefully on machines without them), and no slide has the shadow default.

## Workflow

<!-- BEGIN REDESIGN MODE (optional, removable — see redesign/UNINSTALL.md) -->
### 0. (Optional) Redesigning an existing deck

If the user supplied a `.pptx`, `.pdf`, or markdown outline of an existing deck and wants it redesigned in the Metafore style ("Metafore-ify this deck", "redesign these slides", "convert this pitch to our brand"), follow `redesign/README.md` **before** Step 1. That sub-workflow:

1. Extracts the source into a `slide-manifest.json` + a single `contact-sheet.png` (text-first; never Read individual slide PNGs as a default action).
2. Maps each source slide to a pattern ID via `redesign/source-mapping.md`.
3. Rewrites extracted copy through `redesign/voice-rewrite.md` before any HTML is drafted.

The mapped + rewritten manifest then becomes the source content for Step 1 (outline). Steps 3–5 (draft HTML, build PPTX, save) are unchanged.

**Skip this section entirely** if the user is authoring from scratch — outline, brochure, BRD, talking points, customer transcript. The rest of the workflow below is the authoritative path for everything else.
<!-- END REDESIGN MODE -->

### 1. Understand the request

Determine:
- **Deck purpose** — sales, pitch, vision, product launch, board, all-hands, customer story
- **Length** — short discovery deck (5–8 slides) vs. board deck (15–25 slides). Push back on >25 slides.
- **Source content** — markdown outline, brochure, BRD, talking points, customer transcript
- **Cover variant** — 1A, 1B, or 1C, driven by the opening argument
- **Vertical** — drives voice (Mira only on telecom) and example data

### 2. Outline the slide order

Before writing HTML, list the slides as a flat outline with tier tags:

```
01 Cover                       hybrid    (1B — vision-forward)
02 The problem                 semantic
03 Three forms of waste        image     (capability tile grid)
04 What Metafore does          semantic
05 Pulse for ops               image     (Pulse mockup screenshot)
06 Customer outcome — Carrier X image     (KPI band)
07 What changes when you adopt semantic
08 Closing CTA                 semantic
```

This catches structural problems (too many image slides in a row, missing transitions) before you've committed to layouts.

### 3. Draft the HTML

**Before writing any HTML, open `references/pattern-library.md` and assign a pattern (P-01 to P-16) to every slide in the outline.** That file is the canonical catalog — when to use each pattern, type/color/tier spec, locked-vs-editable rules, common mistakes. Patterns map content shape (a problem statement, a 4-up grid, a KPI band) to layout — the right pattern is determined by the content, not by which slide reads best aesthetically.

Inline the tokens. Build each `<section class="slide">`. For cover proportions/logo position/dot-grid/glass card recipes, follow `references/cover-recipes.md` exactly. For full HTML/CSS for each pattern, see `references/slide-templates.md` (the long-form companion to the pattern library).

Apply voice rules ruthlessly. A cover headline is six words; every one must earn its place.

### 4. Generate the PPTX

Follow `references/generation-pipeline.md`. The result is a `.pptx` next to the `.html` source.

### 5. Save and present

Save both files to the deck output location (typically `Decks/<deck-name>/` with `<deck-name>.html` and `<deck-name>.pptx` side by side). Open the HTML in a browser for design QA, open the PPTX in PowerPoint or Keynote for editability QA.

## Quality checklist

Before delivering, verify:

**Bookends**
- [ ] Slide 1 is a Type 1 cover (1A / 1B / 1C)
- [ ] Final slide closes the deck (CTA, closing line, or Metafore wordmark — never a content slide)

**Brand-critical**
- [ ] One accent family — teal stack only, no second hue
- [ ] No gradients, no drop shadows, no italic, no bold hero text
- [ ] Two-tone hero on cover: first word(s) `--ink`, last word `--logo-dark`, no underline
- [ ] **No trailing period on any slide title except the closing** (h1/h2/hero). Internal periods are OK. Closing headline (P-13) takes a period as a deliberate full stop.
- [ ] Header line-height is tight (0.98–1.04 for hero sizes, 1.04–1.12 for smaller h2)
- [ ] Status colors used only as state indicators, never decoration
- [ ] Retired accents absent — neither `#00C4CC` ("teal-bright") nor `#00989E` ("teal-accent") appears. Accents/strokes/labels use `--teal #006B6F` on light, `#88DCE0` on dark; two-tone hero `--logo-dark #035657` on light, `#88DCE0` on dark.
- [ ] Inline SVG art (Pulse cards, diagrams, reasoning traces) uses palette tokens for fills/strokes — grep the finished file for retired hexes (`#00989E`, `#00C4CC`) and for light greys used as essential text. A CSS-variable swap does **not** reach hardcoded hex inside inline SVG.
- [ ] Glassmorphism appears on the **cover only** (P-01). Every other product card is solid white with a 1px `--line` border.
- [ ] Pulse UI cards across multiple slides use structurally different views (ranked feed / deal rows / metric bars / reasoning trace) — no two cards in the deck use the same internal layout
- [ ] Line-art illustrations on company/team slides pulled from `Graphics/LineIcons/` library, not redrawn

**Visual on every slide**
- [ ] No slide is pure text. Every slide carries a visual element — illustration, UI card, knowledge graph, brandmark, capability grid. If a slide has only a headline and a body paragraph, it's not finished.
- [ ] Header → body vertical rhythm follows the table in `pattern-library.md` (universal invariants). Floor: 48px between h1/h2 and body. Bigger headlines need 56–68px.

**Logo**
- [ ] Real Metafore SVG, never CSS pseudo-element construction
- [ ] Light variant on light panels, dark variant on `--teal-dark` panels
- [ ] Cover: top-left, 155×36. Content slides: top-right, 110×26.

**Footer**
- [ ] Every slide carries the footer line
- [ ] Bottom-left: `© <CURRENT-YEAR> METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL`
- [ ] Bottom-right: page number `NN / NN` in Plex Mono uppercase tracked
- [ ] Year matches current year — not last year
- [ ] No typos (spell-check `Complexity`, `Multimodal`, `drift`, `Record`, etc. — these were misspelled in a prior deck)

**Voice**
- [ ] "Pulse" used; "dashboard" does not appear (except as the antagonist concept being replaced)
- [ ] "Mira" used only on telecom decks
- [ ] No Elana-flagged AI tells (no "isn't X. It's Y.", no triplets, no staccato fragments, no roll-call structures)
- [ ] No "seamless" — prior corp deck slipped "seamless continuum" through, which is on the blocklist
- [ ] Headlines in sentence case, not title case
- [ ] Short, evocative slide titles where they fit ("Pulse Check", "Connecting the dots") — suggested pattern, not a rule

**PPTX-specific**
- [ ] Plex Mono in PPTX has no letter-spacing and no bold
- [ ] Headers under 22px have no negative letter-spacing
- [ ] Two-tone hero is a single text frame with two runs, not two text frames
- [ ] Geist + Inter declared as primary fonts (system fallback expected)
- [ ] No drop shadows on any shape
- [ ] Editable text frames are positioned within ~2px of their HTML bounding box

**Construction**
- [ ] Every slide is exactly 1920×1080 in the HTML
- [ ] Every slide has a `data-pptx` tier tag
- [ ] Hybrid is the default. Count your `image` slides — if more than 1–2, you're baking text into pictures that should be editable.
- [ ] Hybrid slides have `data-pptx-text` markers on every editable node
- [ ] PNG renders are at 2x (3840×2160 source → 1920×1080 placement)
- [ ] Fonts loaded from Google Fonts in the HTML
- [ ] No external image dependencies in the HTML (everything inline or in `assets/`)
- [ ] Inline SVG pill buttons use `rx="<half-the-height>"`, **not** `rx="999"` — see `references/pptx-rules.md` SVG gotchas section. The `rx="999"` shortcut works in CSS but renders as an ellipse in SVG.
- [ ] Color spans have a literal space character before them in the source HTML (`for the <span class="accent">enterprise.</span>`). Build script preserves interior whitespace but cannot invent it.
