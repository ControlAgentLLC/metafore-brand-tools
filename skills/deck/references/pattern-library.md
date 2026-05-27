# Slide Pattern Library

This is the canonical catalog of slide types for a Metafore deck. Every slide you build should map to one of these patterns. Pick the pattern that fits the content, don't bend a pattern to fit a wrong slide.

Read this file before drafting the HTML. The detailed HTML/CSS recipes live in `slide-templates.md`; this file is the index, the rationale, and the rules.

---

## How to use this library

1. **Outline the deck before writing any HTML.** Every slide gets exactly one pattern from this catalog. Write the outline as a list — `Cover (P-01) → Agenda (P-04) → Problem (P-05) → ...`
2. **Pick the right pattern for the content, not the prettiest one.** If the content is two parallel facts, that's the comparison pattern. If it's a dense capability inventory, that's the capability grid. Don't force a hero pattern onto reference content.
3. **Keep the chrome consistent.** Section label top-left, icon top-right, footer bottom — same on every slide except the cover and the closing.
4. **Pull text out of pictures.** If something in the design is text the customer would ever want to edit, it belongs in a text frame, not baked into a PNG. The default tier is `hybrid`; reserve `image` for slides that are *purely* graphic.

---

## Universal invariants (apply to every pattern)

These rules are non-negotiable. They apply across every pattern in this catalog.

### Canvas
- 1920×1080 (16:9). Maps to 13.333"×7.5" widescreen PPTX.
- `--slide-pad-y: 96px`, `--slide-pad-x: 120px` for the content well.
- `--chrome-offset: 36px` for the corner-aligned chrome (section label, icon-tr, footer, logo-tl on cover). Chrome sits tighter than content.

### Palette — teal stack + grayscale only
Approved fills:
- `#004D50` `--teal-dark` · KPI bands, hero dark surfaces, deep emphasis
- `#006B6F` `--teal` · primary brand · section labels · default chart series
- `#00989E` `--teal-accent` · secondary accents · mid-stop · dark-surface highlights
- `#035657` `--logo-dark` · two-tone hero accent · product-name color
- `#67A4A4` `--logo-light` · secondary chart series · subtle accents
- `#E8F4F5` `--teal-light` · tinted callouts · row fills
- Grayscale: `#FFFFFF`, `#F8FAFA`, `#FAFBFB`, `#F4F4F4`, `#ECECEC`, `#999999`, `#666666`, `#404040`, `#1A1A1A`, `#0A0A0A`

Forbidden:
- `#00C4CC` (was `--teal-bright`) — retired, too cyan
- Status colors (success/warn/danger) as decoration — only allowed as actual state indicators
- Any non-teal hue (indigo, sky, mint, violet, coral, etc.)
- Gradients on cards, drop shadows on cards, accent line under titles

### Typography — three fonts, three roles
- **Headers / hero / KPI numbers:** Geist (web fallback for Brut Grotesque), weight 400. **Never bold.** Negative letter-spacing only above ~22px.
- **Body:** Inter (fallback for GT America), weight 400. No tracking adjustments.
- **Eyebrows / labels / mono data:** IBM Plex Mono, weight 400–600, all-caps, `0.16em–0.22em` tracking. **In PPTX, Plex Mono never carries letter-spacing and is never bold.**

### Two-tone hero
The signature Metafore type moment. First chunk renders in ink (`#1A1A1A`) or white on dark, last chunk wraps `<span class="accent">` in `#035657` (or `.accent-light` `#00989E` on dark surfaces). Same font, same size — only color changes. Never italic, never underlined, never bold.

### Header → body vertical rhythm
Headline and body need breathing room. Tighter than this and the slide reads cramped; this is a recurring tuning issue, so codify it.

| Headline size | `margin-bottom` (h1/h2 → body) | Used in |
|---|---|---|
| 48–56px h2 (scenario / table headers) | **36–40px** | in-action scenarios, delivers table |
| 56–60px h2 (content-grid header) | **48–56px** | capability grids, modules, deployment, platform |
| 64–72px h2 (statement/company) | **52–56px** | problem, suite intro, integrate, company |
| 68–84px h1 (split-hero like Why) | **48–56px** | why-style hero on dark |
| 100–110px h1 (closing) | **60–68px** | closing CTA |
| 120px h1 (cover) | **56px** | cover only — the cover gets less relative space because the rest of the slide handles the breathing |

Floor: **never less than 36px**. For most patterns the floor is 48px, but P-18 scenario slides and P-20 tables run tighter (36–40px) because they trade headline breathing room for content density. If a content slide has multiple stacked text blocks (eyebrow + h2 + lede + body), the eyebrow → h2 gap can be tighter (~16–24px), but the h2 → body gap follows the table above.

### Header line-height — tight, not loose
Geist (and Inter as fallback) at hero sizes wants tight leading. Loose line-height makes multi-line headlines feel like separate sentences instead of one stacked phrase.

| Headline size | `line-height` |
|---|---|
| 84px+ h1 (cover, why, outcome) | **0.98–1.0** |
| 60–72px h1/h2 | **1.0** |
| 48–58px h2 | **1.0–1.04** |
| < 48px h2 / sub-heads | **1.04–1.12** |

When a Geist headline at 60–84px wraps to two lines and feels airy, drop `line-height` by 0.02–0.04. The "feels airy" check is the right test — Geist at these sizes can absorb very tight leading without descender collisions because there are very few descenders in title-case copy.

### Slide titles never end in a period (except the closing)
Headlines, h2s, h1s, hero text — none of them end in a full stop. They're titles, not sentences. The accent term (the last word wrapped in `<span class="accent">`) is the natural emphasis, and a period after it weakens the punch.

```html
<!-- Right -->
<h2>Think, act, and <span class="accent">build</span></h2>
<!-- Wrong -->
<h2>Think, act, and <span class="accent">build.</span></h2>
```

This applies even when the headline contains internal punctuation. "Every function has its own dashboard. The enterprise still doesn't see itself" — keep the mid-sentence period, drop the trailing one. Agenda sub-descriptions and body copy are sentences and *do* end in periods; the rule is only for titles.

**Exception: the closing slide.** The very last slide of the deck (P-13 Closing / CTA) **does** end in a period. The closing headline is the deck's final beat — the period is a deliberate full stop that signals "we're done" and gives the headline conversational weight rather than poster punch.

```html
<!-- Closing slide — period required -->
<h1>Let's map your <span class="accent">transformation.</span></h1>
```

This is the only place in the deck where a title ends in a period. Every other slide — cover, content, dividers, statements — follows the no-period rule.

### Every slide carries a visual element
**No pure-text slides.** Every slide gets a visual presence — an illustration, a UI card, a knowledge graph, a numbered grid, a brandmark, *something* — even if the slide's job is to land a single sentence. Pure text on white reads as a draft, not a deck.

This is the rule that turned three slides in the MetaWorks deck (problem, suite intro, closing) from text-only into properly composed slides. If you find yourself building a slide that's only a headline + body paragraph, you haven't finished the slide.

### Brand vocabulary — "Pulse", never "Dashboard"
Metafore's term for what other vendors call a dashboard is **Pulse**. Never use "dashboard" in deck copy, even when describing the competitive landscape — recast as "view", "report", "Pulse", or restructure the sentence. Capitalize "Pulse" when it refers to the Metafore product surface.

### Solid white card vs glasscard
Glassmorphism (`backdrop-filter: blur(18px)` + `rgba(255,255,255,0.08)` fill) is reserved for the **cover slide (P-01) only**. Every product/UI card on every other slide — content hero (P-17), statement-with-card (P-05), capability grid (P-06/P-07) — is a **solid white card** with a 1px `--line` border and no drop shadow. Keeping glass exclusive to the cover preserves its visual punch.

### Locked vs editable (the tier decision)
- `data-pptx="semantic"` — pure text composition; everything is an editable text frame.
- `data-pptx="hybrid"` — text composed over a graphic/illustration; text frames editable, graphics baked.
- `data-pptx="image"` — entire slide is a picture; nothing editable. **Reserve for slides that are 100% visual** (a single rendered diagram, no copy). Default away from this.

Anything a teammate would reasonably want to edit (titles, body, KPI numbers, labels, eyebrows, table values, pill names) must be a text frame. Only true graphics (illustrations, icons, knowledge graphs, charts as composition rather than data) get baked.

---

# The pattern catalog

Each pattern: **when to use it**, **default tier**, **structure**, **type spec**, **locked vs editable**, **common mistakes**.

---

## P-01 · Cover

**When:** Slide 1, always. Sets the deck's two-tone hero.

**Tier:** `hybrid` (so the headline + subtitle are editable, the supporting visual is locked).

**Variants:**
- **1A · bare** — wordmark top-left, headline + subtitle centered-left, white canvas. Use for short internal decks.
- **1B · split with glasscard** — left text on light, right side carries a floating glassmorphism Pulse card on solid `--teal-dark`. Use for sales/customer decks where you want to show product context.
- **1C · split with conversational demo** — left text, right side carries a conversational agent card on solid `--teal-dark`. Use when the deck is about a specific vertical / use case.

**Structure (1B/1C):** Two-column 1fr/1fr split. Left column: `logo-tl` top-left + `textwell` centered. Right column: solid `--teal-dark` carrying one glass card.

**Type:**
- Headline: Geist 120px (1A bare) / 96px (1B/1C split), line-height 1.04, letter-spacing `-2.4px`. Two-tone — first words ink, last word `.bracket` in `--logo-dark`.
- Subtitle: Inter 28px, `--ink-3`, max-width ~640px.

**Locked vs editable:**
- Editable: headline (with run-split for the accent word), subtitle.
- Locked: wordmark, glass card or conversational card composition.

**Cover-specific chrome:** wordmark top-left (155×36), **no** section label, **no** icon-tr. Footer can be omitted on cover — pick one rule and apply it deck-wide.

**Common mistakes:**
- Using `display:flex; gap:` for multi-line headlines — descenders break row consistency. Use `display:block` with shared line-height.
- Putting the wordmark anywhere but top-left.
- Centering body copy under the headline.

See `cover-recipes.md` for the full 1A/1B/1C HTML.

---

## P-02 · Section divider

**When:** Mark a phase change in the deck narrative (e.g. between "the problem" and "the solution"). Use sparingly — one or two per deck.

**Tier:** `semantic`.

**Structure:** Full-bleed `--teal-dark` surface. Eyebrow Plex Mono top-left (with `.section-label.on-dark`), giant phrase or single word centered, optionally a one-line subtitle below.

**Type:**
- Eyebrow: Plex Mono 18px, `rgba(255,255,255,0.7)`, `0.18em` tracking.
- Headline: Geist 144px, white, two-tone with `.accent-light` in `#00989E` for the trailing word.
- Subtitle (optional): Inter 22px, `rgba(255,255,255,0.7)`.

**Locked vs editable:** Everything editable. No graphic.

**Common mistakes:** Putting body copy on a section divider. If it has more than one line of subtitle, it isn't a divider — it's a statement slide.

---

## P-03 · Agenda

**When:** Slide 2 of decks longer than ~8 slides. Skip in short decks.

**Tier:** `semantic`.

**Structure:** Two-column grid of 6–10 numbered items. Each item: small mono number + bold title in Title Case + one-line sub-description (`.a-sub`) below. h2 header above the grid is optional.

**Reading order — column-major (vertical first).** Column 1 fills top-to-bottom, then column 2 fills top-to-bottom. Item 01 sits top-left, item N/2 sits bottom-left, item N/2+1 sits top-right. This matches how people read a 2-column TOC — eye moves down each column, not back-and-forth across rows. CSS:

```css
.agenda .items {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: repeat(<items-per-column>, auto);
  grid-auto-flow: column;          /* column-major fill */
  gap: 28px 80px;
}
```

`grid-auto-flow: column` is the key — without it, the default `row` flow fills horizontally row-by-row, and item 02 ends up top-right instead of second-down on the left.

Set `grid-template-rows: repeat(N, auto)` where N = items per column (`Math.ceil(total / 2)` for an odd total). For 8 items use `repeat(4, auto)`; for 10 use `repeat(5, auto)`; for 6 use `repeat(3, auto)`.

**Type:**
- h2 header (if used): Geist 40–56px, two-tone.
- Item number (`.a-num`): Plex Mono 18px, `--ink-4`.
- Item title (`.a-text`): Geist 30px, weight 400, `--ink`.
- Item sub (`.a-sub`): Inter 15px, `--ink-3`.

**Wording:**
- Items in Title Case ("The Company", "The Problem", "Platform & Integrations").
- "The" only where it reads naturally — don't force it onto every item.
- Sub-description is one sentence, ends with a period (body copy, not a title — so the no-trailing-period rule doesn't apply here).

**Locked vs editable:** All text editable.

**How many items.** The agenda condenses the deck's narrative arc — not every slide gets an agenda item. 22-slide decks fit in 8 agenda items; 12-slide decks fit in 6. Group consecutive content into named sections ("MetaWorks in Action" covers three In-Action slides; "The Suite" covers Suite Intro + Modules + Inside Every Module).

**Common mistakes:**
- Lists with 11+ items — the agenda reads as a book TOC, not a talk outline. Compress or split into two slides.
- Default `grid-auto-flow: row` — items zigzag (01 top-left, 02 top-right, 03 second-row-left). Looks like a bingo card. Always set `grid-auto-flow: column`.
- Using verb phrases ("Reviewing the problem") instead of noun phrases ("The Problem").
- Letting agenda items drift out of sync with the deck — when slides are added/removed/reordered, update the agenda to match. The agenda is a contract with the audience.

---

## P-04 · Company / About

**When:** Slide 3, after the agenda. One slide tops — never multiple "about us" slides.

**Tier:** `semantic`.

**Structure:** Two-column split. Left: h2 two-tone + mission paragraph + optional one-line signature. Right: 3–5 fact rows, each with a Plex Mono label and a value (e.g. HEADQUARTERS · San Francisco; FLAGSHIP PLATFORM · Metafore One).

**Type:**
- h2: Geist 72px, two-tone.
- Mission paragraph (`.mission`): Inter 22px, `--ink-2`.
- Fact label (`.f-label`): Plex Mono 12px, `--teal`, `0.16em` tracking.
- Fact value (`.f-value`): Geist 22px, with `.secondary` Inter 14px line under for the elaboration.

**Locked vs editable:** All text editable.

**Common mistakes:** Bullet list of company facts (use the label/value pairs). Burying the headline in a wall of text.

---

## P-05 · Statement / Problem / Why-style

**When:** A slide whose job is to land a single message — the problem, the insight, the strategic claim. Used for Problem and Why-MetaWorks slides.

**Tier:** `hybrid` — text editable, supporting illustration locked.

**Structure:** Two-column split (≈ 1.05fr / 0.9fr). Left: hero h2 two-tone + one body paragraph. Right: a brand-style illustration tied to the message (see *Illustration patterns* below).

**Type:**
- h2: Geist 60–64px, weight 400, letter-spacing `-1.6px`, line-height 1.06.
- Body: Inter 22px, `--ink-2`, no max-width past column.
- On `--teal-dark` background: h1 84px white + accent-light on the trailing word + optional stat pair below.

**Illustration on the right side:**
- **Problem-style** — a single brand-style Pulse UI card on white. Shows one function's view (e.g. METAFORE PULSE · FINANCE), with header + title + KPI rows + recommendation box + CTA. Subtle hints in the sub-meta (`DETECTED · FINANCE · 1 SURFACE`) and recommendation copy (`cross-function routes unavailable`) carry the fragmentation message — the headline does the rest. White card, 1px `--line` border, 14px radius, no drop shadow. See MetaWorks deck slide 4 for the canonical implementation.
- **Insight-style** — a single radial / knowledge-graph composition. See MetaWorks deck slide 11.
- **Convergence-style** — many surfaces collapsing to one center mark. See MetaWorks deck slide 6.

The illustration must follow brand graphic rules: teal stack only, no chart fragments (no donuts, gauges, multi-color bar charts), no decorative rotations, no scattered "playful" arrangements. Schematic and aligned, not whimsical.

**Why a UI card and not a chart-shaped illustration:** the Pulse card *is* the product surface — showing one of them on this slide is brand-correct ("here is a Pulse") and the headline reframes it ("...and every function has its own"). A UI card on light always sits flat on the white slide; reserve glassmorphism for the cover (P-01) only.

**Locked vs editable:** h2, body, any stat pair labels/numbers → editable. Illustration → baked.

**Common mistakes:**
- Using a chart-shaped visual (donut + bar + line + gauge composition) — that reads as a generic dashboard, not Metafore.
- Scattered/rotated cards or playful "decorative" illustration — reads as whimsical, not professional. Use aligned schematic compositions.
- Two-line h2 in a narrow column at 80px+ — wraps badly. Drop to 60–64px when the column is half-width.

---

## P-06 · Capability grid (4-up)

**When:** Showing the 4 graphs, the 4 pillars, the 4 stages. Whenever you have exactly 4 parallel items with illustrations.

**Tier:** `hybrid`. The illustrations are baked; every label and body is a text frame.

**Structure:** h2 header at top + 1×4 grid below. Each card: illustration block (140px tall, dotted divider below) + Plex Mono eyebrow + Geist headline (38px) + Inter body.

**Type:**
- h2: Geist 56px, two-tone.
- Card eyebrow (`.t-num`): Plex Mono 15px, `0.18em` tracking, **`--teal` on every tile**. Earlier versions of this spec stepped through the teal stack (`--teal`, `--teal-accent`, `--teal-dark`, `--logo-dark`) tile-by-tile — that read as inconsistency, not subtlety. Use a single color across all four tiles; let the tile content carry the rhythm.
- Card name (`.t-name`): Geist 38px, weight 400, letter-spacing `-0.9px`. Add `margin-bottom: 32px` to separate from body.
- Card body (`.t-body`): Inter 19px, line-height 1.5, `--ink-2`.

**Illustrations:** Pull from `Graphics/LineIcons/` first — the line-icon library has stylized 4-graph diagrams (Nodes, ThroughLine, Stack, Axis). Custom SVG only if no line icon fits.

**Locked vs editable:** Illustration PNG locked. Eyebrow/name/body editable.

**Common mistakes:**
- More than 4 cards in this layout — drop to P-10 (8-up) or P-11 (12-up).
- Using emoji or photos in the illustration block.

---

## P-07 · Capability grid (8-up)

**When:** Platform capabilities, integrations, feature inventory. 6–10 parallel items.

**Tier:** `hybrid`.

**Structure:** h2 header + lede subtitle + 2×4 or 4×2 grid. Each card: Plex Mono eyebrow + line-icon SVG (24×24, currentColor stroke) + title + 2-line body.

**Type:**
- h2: Geist 56px, two-tone.
- Lede (`.lede`): Inter 22px, `--ink-2`.
- Card eyebrow (`.c-num`): Plex Mono 14px, `--teal`.
- Card icon (`.c-icon`): 24×24 SVG, `stroke="currentColor"`, `stroke-width="1.6"`, no fill. Color matches the eyebrow.
- Card title (`.c-title`): Geist 24px, weight 400.
- Card body (`.c-body`): Inter 15px, `--ink-2`.

**Locked vs editable:** SVG line icons locked. All text editable.

**Common mistakes:**
- Filling the icons (use stroke only).
- Mixing icon styles within a single grid (all line icons or all PNGs, not both).

---

## P-08 · Module / product grid (12-up)

**When:** Exactly twelve parallel items with a strong product-name pattern. Use sparingly — this is the densest slide in the system.

**Tier:** `hybrid`.

**Structure:** h2 header + 4×3 grid. Each card: small mono number + product name (two-tone: brand word in ink + accent word in `--logo-dark`) + Plex Mono "FOR THE ..." line + 2-line body.

**Type:**
- h2: Geist 56px, two-tone (match other content slides — don't downgrade to h3).
- Card number (`.m-num`): Plex Mono 11px, `--ink-4`.
- Card name (`.m-name`): Geist 24px. Two spans: `<span class="m">MetaWorks</span> <span class="t">Focus</span>`. The `.t` span renders in `--logo-dark` via the build script.
- For-line (`.m-for`): Plex Mono 10px, `--teal`.
- Body (`.m-body`): Inter 14px, `--ink-2`.

**Locked vs editable:** All text editable.

**Common mistakes:**
- Letting the brand word and accent word run together (`MetaWorksFocus`) — happens if the build script drops the interior space. Verify each card renders as `Brand Accent` with the accent in teal.
- Using h3 to fit more cards on screen — keep h2 at 56px and drop the grid height instead.

---

## P-09 · KPI band

**When:** End-of-section impact slide. Four hero metrics that anchor the case.

**Tier:** `hybrid`.

**Structure:** Full-bleed `--teal-dark` surface. h2 or eyebrow not required (the numbers carry the slide). 1×4 grid of cells, each with vertical hairline left-border separator.

**Type:**
- Number (`.num`): Geist 84px, weight 400, line-height 0.95, letter-spacing `-1.6px`, white, `font-variant-numeric: tabular-nums`, **`white-space: nowrap`** so ranges like `8–12wks` and `40–60%` don't wrap.
- Suffix (`.num .suffix`): 30px Geist, `rgba(255,255,255,0.9)`, 6px left margin.
- Label (`.label`): Inter 19px, `rgba(255,255,255,0.78)`, max-width 280px.

**Locked vs editable:** All text editable. The dark surface and the vertical hairlines are CSS — they survive as background.

**Common mistakes:**
- Numbers above 90px — they wrap or overflow at quarter-width.
- Centering the labels. Left-align them under the numbers.

---

## P-10 · Integration ecosystem / pill clusters

**When:** Showing what the platform connects to — enterprise systems, LLM providers, sources of record.

**Tier:** `hybrid`.

**Structure:** Two-column split. Left: h2 two-tone + body paragraph. Right: 3–4 clusters, each with a Plex Mono cluster label and a row of pills.

**Type:**
- h2: Geist 56px, two-tone.
- Cluster label (`.cl-label`): Plex Mono 12px, `--teal`, `0.18em` tracking.
- Pill (`.pill`): Inter 14px, `--ink-2`, `999px` radius, `--card-grey` fill, no border, 12px horizontal padding.

**Locked vs editable:** Every cluster label and pill is editable — these are the things the user is most likely to want to swap (Salesforce → HubSpot, Claude → OpenAI).

**Common mistakes:**
- Filling pills with a teal accent color — keep them neutral grey so the brand stays clean.
- Logos inside pills — text only.

---

## P-11 · Timeline / horizontal stepper

**When:** Deployment plan, phased rollout, time-to-value narrative. 4–6 sequential steps.

**Tier:** `hybrid`.

**Structure:** h2 header + lede + 1×N horizontal row of steps. Each step: Plex Mono week-range + large mono number + Geist title + 2-line body. A thin teal hairline runs underneath, breaking at each step.

**Type:**
- h2: Geist 56px, two-tone.
- Lede: Inter 22px, `--ink-2`.
- Week range (`.s-week`): Plex Mono 12px, `--teal`.
- Step number (`.s-num`): Plex Mono 32px, `--ink-4`.
- Step title (`.s-title`): Geist 22px.
- Step body (`.s-body`): Inter 14px, `--ink-2`.

**Locked vs editable:** All text editable. The hairline is CSS.

**Common mistakes:**
- More than 6 steps — wraps badly. Compress or split into two slides.
- Step bodies that wrap to 3+ lines — keep them tight, this is a glance-slide.

---

## P-12 · Radial diagram / knowledge graph

**When:** Showing topology, connectivity, the "one connected reality" claim. Pairs with a Why-style left column.

**Tier:** `hybrid`.

**Structure:** Two-column split, often on `--teal-dark`. Left: h1 two-tone + body + stat pair row. Right: a single radial SVG — center node, 8 satellite nodes at compass positions, solid spokes and dashed peripheral connections, Plex Mono labels around the perimeter.

**Type:**
- h1 on dark: Geist 84px, white with `.accent-light` in `#00989E`.
- Body on dark: Inter 22px, white.
- Stat number (`.s-num`): Geist 64px, `--teal-accent`.
- Stat label (`.s-label`): Plex Mono 12px, `rgba(255,255,255,0.7)`.
- Diagram labels: Plex Mono 13px, `rgba(255,255,255,0.85)`, `0.18em` tracking.

**Locked vs editable:** h1, body, stat pair text → editable. Diagram → baked. Diagram labels are part of the SVG, intentionally not editable.

**Common mistakes:**
- Using `#00C4CC` for the spokes — that color is retired. Use `--teal-accent` `#00989E` for line work on dark surfaces.
- Filling satellites with solid teal-bright. Use outlined circles with a small filled inner dot.

---

## P-17 · Content hero with right image

**When:** "Here's what it looks like" slides. A single product surface — a Pulse view, a workflow capture, a notebook screenshot, a conversational agent moment — anchors the right side; the left explains. The content-slide adaptation of cover variants 1B/1C.

**Tier:** `hybrid` — left text editable, right product card baked into the background.

**Structure:** Two-column split, 56% / 44%. The right column is **full-bleed** solid `--teal-dark` from edge to edge (not just inside the content well — the dark surface reaches all four edges of its 44%). Left column: standard chrome (section label TL, footer copy line) over white, content well in the middle with eyebrow + h2 two-tone + body + optional meta strip. Right column: a **solid white** product card centered on the dark stage.

**Why solid white, not glass:** The cover (P-01) uses glassmorphism on its right card because the cover is the most distinctive moment in the deck. Content slides reuse the split silhouette but trade the glass for a solid white card — more legible, less precious, and visually distinct from the cover. **Don't use `backdrop-filter` on content-slide cards.**

**Type:**
- Eyebrow (`.eyebrow` in textwell): Plex Mono 14px, `--teal`, `0.2em` tracking, above the headline.
- h2: Geist 64px two-tone, line-height 1.06, letter-spacing `-1.6px`, max-width 880px.
- Body: Inter 22px, `--ink-2`, max-width 760px.
- Optional meta row: Plex Mono 12px label / Geist 32px value pairs, 56px gap between stats.
- Card title: Geist 22px weight 500.
- Card eyebrow / time / row labels / recommendation label: Plex Mono 10–11px, tracked, `--teal` or `--ink-4`.
- Card row values: Plex Mono 22px, `--logo-dark` (or `--ink-3` for muted values).
- Card CTA: 999px pill, `--teal-dark` fill, white text, Geist 14px weight 500.

**Chrome:**
- Section label top-left over the white side → use `.section-label` standard (teal on light).
- Icon top-right sits over the **dark side** → use `#icon-dark` (white variant).
- Footer spans both columns — copy line on the white side uses `--ink-3`, page number on the dark side uses `rgba(255,255,255,0.55)`.

**Locked vs editable:**
- Editable: eyebrow, h2 (with two-tone run-split), body, meta-strip values, footer.
- Locked: the entire product card on the right stage — eyebrow, time, title, all rows, recommendation, CTA. It's a visual proof, not editable copy. If a customer wants to edit the card content, swap the screenshot.

**Common mistakes:**
- Using a glasscard on a content slide. Glass is reserved for the cover. Solid white card here.
- Stretching the headline past the column. Cap at 64px and keep `max-width: 880px`.
- Filling the right stage with dot grid / halftone overlay. The dark stage is **solid**, not patterned.
- Putting the icon on the light side. The icon sits where the chrome sits (top-right corner of the slide), which on this pattern is over the dark right column — so use the white icon variant.

**Use cases:**
- "The Pulse in action" — product preview slides.
- "Mira responding live" — conversational agent demo as content (not as cover).
- "Workflow inside Operate" — one screenshot from one module, with the explanation on the left.

**Don't use for:**
- Abstract concept illustrations (use P-05 instead).
- Charts (use P-09 KPI band).
- Multiple parallel screenshots (use P-06 / P-07 grid).

---

## P-13 · Closing / CTA

**When:** Final slide, always.

**Tier:** `semantic`.

**Structure:** Centered. A brandmark above (large icon-only mark, 172×144), an h1 two-tone CTA below, a single Plex Mono contact line under that.

**Type:**
- Brandmark: 172×144 icon-only SVG, `data-pptx-image="icon-light"`.
- h1: Geist 104px, two-tone, letter-spacing `-2.6px`.
- CTA line (`.cta-line`): Plex Mono 22px, `--teal`, no tracking.

**Locked vs editable:** Brandmark locked. h1 and CTA line editable.

**Common mistakes:**
- Adding a Plex Mono tag next to the brandmark ("START WHERE IT MATTERS") — too much chrome on a slide that should be pure intent. Brandmark, headline, contact line. Stop there.
- Repeating the wordmark from the cover — the closer uses the icon-only mark, not the wordmark.

---

# Patterns to use sparingly

These exist in the system but should be reached for less often than the core patterns (P-01 to P-13, plus P-17). If you find yourself using two of these in a single deck, reconsider.

## P-14 · Two-column comparison (before/after, with/without)

**When:** A single binary comparison where both sides matter. Don't use this for "look how bad the old way is" — that's just rhetorical decoration. Use it when both states are real states the customer actually experiences.

**Structure:** Two equal columns under a single h2. Each column has its own Plex Mono eyebrow ("WITHOUT METAFORE" / "WITH METAFORE"), one or two stat numbers, a body paragraph.

**Type spec:** Match P-05 (statement) on the header; match P-09 (KPI band) on the numbers but in `--logo-dark` rather than white-on-dark.

## P-15 · Pull-quote

**When:** Customer quote, analyst quote, or a marquee internal insight that earns a whole slide. One per deck max.

**Structure:** Full-width, large Geist quote (60–72px, weight 400, no italic), attribution Plex Mono below in `--teal`. Optional small portrait or logo on the left.

**Type:** Geist 64px quote, line-height 1.18, max-width 1480px. Attribution: Plex Mono 14px, `--teal`, all-caps, `0.18em` tracking, prefixed with `—`.

## P-16 · Architecture diagram

**Placeholder pattern.** No canonical recipe yet — architecture diagrams are deck-specific. When you build one, follow the radial diagram pattern (P-12) for type rules and palette: Plex Mono labels, teal-stack fills only, no third color.

---

## P-18 · Two-on-top + three-on-bottom (scenario slide)

**When:** Narrative cross-function scenario slides — "MetaWorks in Action" stories where a single situation traces across multiple modules. Used when you want to show *both* the role-scoped UI surface *and* the cross-function module trace on the same slide. The MetaWorks deck uses three of these in a row (Executive Intelligence / Revenue & Pipeline / People & Operations).

**Tier:** `hybrid`. Header text, scenario paragraph, and trace tile text are all editable; the UI card is locked.

**Structure (explicit grid rows):**

```
┌──────────────────────────────────────────────┐
│ section-label                       icon-tr  │
│                                              │
│ ┌──────────────┐  ┌──────────────────┐       │
│ │ Headline     │  │                  │       │
│ │ Scenario     │  │   UI card        │       │
│ │ paragraph    │  │   (Pulse view)   │       │
│ └──────────────┘  └──────────────────┘       │
│                                              │
│ ┌────────┐ ┌────────┐ ┌────────┐             │
│ │ Trace 1│ │ Trace 2│ │ Trace 3│             │
│ └────────┘ └────────┘ └────────┘             │
│                                              │
│ Sources line                                 │
│ ©  ...                            NN/NN      │
└──────────────────────────────────────────────┘
```

**CSS (the key parts):**

```css
.in-action.with-card {
  padding: 100px var(--slide-pad-x) 92px;
  display: grid;
  grid-template-rows: 1fr 260px auto;   /* top flexes, traces fixed-short */
  row-gap: 64px;                        /* generous gap between sections */
}
.in-action.with-card .header-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
}
.in-action.with-card .header h2 {
  font-size: 52px; line-height: 0.98;
  letter-spacing: -1.3px;
  margin: 0 0 40px;                     /* big gap between headline and scenario */
}
.in-action.with-card .ui-card {
  height: 100%; max-height: 440px;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 22px 26px;
}
.in-action.with-card .traces {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}
```

**UI card content must vary across slides.** If you build three of these in a row, give each a structurally different Pulse view — a ranked feed, a list of deals, a stack of metric bars, a reasoning trace. Three Pulse cards in a row that all look like KPI lists read as one slide repeated three times. The trace tile structure stays identical (1/2/3 + module + role + body) because it's the spine of the narrative — only the UI card on the right changes shape per scenario.

**Trace tile sizing.** Keep bottom row tight — 260–300px is enough for `.a-num` mono eyebrow + 22px `.a-mod` title + 11px `.a-role` mono label + 4 lines of `.a-body` at 14px. Anything taller leaves the tile feeling empty.

**Common mistakes:**
- Trace tiles too tall — looks empty under the body copy. Cap at 260–300px.
- UI card and trace tiles use the same Pulse layout — repeats. Force structural variety on the UI card per scenario.
- Header margin-bottom too small — the scenario paragraph crowds the headline. Use 36–40px.
- Letting traces row `1fr` — they grow to fill remaining height and end up half-empty. Use a fixed `260px` for the trace row.

---

## P-19 · Team photos placeholder

**When:** Company/team intro slide. Pair this with P-04 (Proven Track Record) when the deck has a "Meet the team" moment.

**Tier:** `semantic`. The headline, lede, name, and role are all editable; the photo cards are placeholder containers waiting for real headshots.

**Structure:**

```
section-label (TEAM)              icon-tr

Headline + accent term
Lede / instruction line

┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│ photo  │  │ photo  │  │ photo  │  │ photo  │
│ (4:5)  │  │        │  │        │  │        │
└────────┘  └────────┘  └────────┘  └────────┘
Name        Name        Name        Name
ROLE · CO   ROLE · CO   ROLE · CO   ROLE · CO

© ...                                    NN/NN
```

**Photo placeholder construction:**

```css
.team-photos .photo {
  width: 100%;
  aspect-ratio: 4 / 5;
  background: var(--bg-solid);
  border: 1px solid var(--line);
  border-radius: 12px;
  position: relative;
}
.team-photos .photo::before {
  /* faint diagonal line to mark this as a placeholder, not a missing image */
  content: ""; position: absolute; inset: 0;
  background: linear-gradient(135deg,
    transparent 49.6%, var(--line) 49.6%,
    var(--line) 50.4%, transparent 50.4%);
}
.team-photos .photo .photo-label {
  /* "PHOTO" mono label centered over the diagonal */
  position: relative;
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--ink-4);
  background: var(--bg-solid);
  padding: 4px 10px;
}
```

The diagonal line is intentional. Empty boxes read as missing images; the diagonal slash reads as "photo goes here."

**To finalize:** drop real headshots into each `.photo` container (replace the `<span class="photo-label">PHOTO</span>` with an `<img>` or set `background-image`). The `.m-name` and `.m-role` text frames remain editable in the PPTX.

**Common mistakes:**
- Filling the placeholder with a stock-photo silhouette — looks like a real-but-bad photo. Keep the diagonal slash; it's clearly a placeholder.
- 3-up grid when you have 4 team members — leaves the row visually unbalanced. Use 4-up for 4 members; 5–6 use 3-up and a second row.

---

## P-20 · Wide data table

**When:** A capability/module mapping or a "what we deliver" matrix that's best read as rows, not cards. The MetaWorks "What MetaWorks Delivers" slide is the canonical example — Capability / Module / Description.

**Tier:** `hybrid`. Cell text is editable; the horizontal divider lines are baked.

**Structure:** A `--ink`-bordered header row, then 4–6 data rows separated by `--line` hairline borders. 2–3 columns. No vertical dividers.

**Type:**
- Header cells: Plex Mono 12px, weight 600, `0.18em` tracking, uppercase, `--ink-3`
- Capability column: Geist 22px, weight 500, `--ink`
- Module column: Plex Mono 13px, weight 600, `0.16em` tracking, uppercase, `--logo-dark`
- Body column: Inter 17px, line-height 1.55, `--ink-2`

**Headline width.** When the headline is intentionally one line, set `max-width` to the full content width (1680px) **and** add `white-space: nowrap` — `max-width` alone isn't enough; the browser will still break long lines if a word doesn't fit. With `nowrap`, the layout breaks visibly if you overflow, so you'll see the bug at build time rather than after the customer opens the PPTX.

```css
.delivers .header h2 {
  font-size: 48px;
  letter-spacing: -1.2px;
  max-width: 1680px;
  white-space: nowrap;   /* don't wrap */
}
```

If the headline wraps anyway, reduce font-size — don't widen the slide canvas.

**Common mistakes:**
- Column gap too narrow — the table reads as a wall of text. Use `gap: 40px` between columns.
- Treating the header row like a normal row — it needs the strong `--ink` border, not the `--line` hairline. The visual hierarchy is "header is the underline of the title row, hairlines separate data rows."

---

# Composing a deck — sequencing patterns

The MetaWorks deck is the reference sequence. Use it as a template; deviate intentionally, not accidentally.

```
P-01  Cover                              (always slide 1)
P-03  Agenda                             (skip in short decks)
P-04  Company                            (one slide max)
P-05  Statement / Problem
P-06  Capability grid (4-up)             — the four pillars / four graphs
P-05  Statement / Suite Intro
P-08  Module grid (12-up)                — the surfaces
P-07  Capability grid (8-up)             — the shared platform
P-10  Integration ecosystem
P-09  KPI band
P-05  Statement / Why
P-11  Deployment timeline
P-13  Closing                            (always last)
```

A 5–8 slide deck can drop the agenda, the company, the integration ecosystem, and the timeline. A 20+ slide deck adds section dividers (P-02) at narrative breaks and may use the pull-quote (P-15) once.

**Don't repeat a pattern more than 3× in a deck.** If you have four "statement" slides, three of them are probably overlap.

---

# When in doubt

- **Is this slide editable enough?** If the answer is "the title, but everything else is a picture" — promote the picture to a real layout (P-06 / P-07 / P-10) and let every label become a text frame.
- **Is the headline doing the work?** If you can remove the headline and the slide still communicates, the slide is over-illustrated. If you can remove every illustration and the slide reads fine, the slide is under-illustrated. The right balance is the headline as the spine, the illustration as the proof.
- **Does the slide look like Metafore at a glance?** Three tells: two-tone hero, Plex Mono eyebrow somewhere, single teal accent family. If a stranger could mistake the slide for a generic SaaS template, the brand isn't doing its job.
