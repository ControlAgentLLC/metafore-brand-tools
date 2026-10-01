---
name: graphic
description: Create Metafore-branded HTML graphics — blog hero images, conversational demo cards, vertical feature cards, website section illustrations, OG/social preview images, pull-quote cards, concept illustrations, and line icons. Use this skill whenever someone asks for a blog graphic, hero image, card illustration, website graphic, social image, OG image, pull-quote graphic, conversational agent mockup, or any Metafore-branded visual asset rendered from HTML to PNG. Covers all verticals (travel, banking, telecom, supply chain, health, HR, public sector, etc.).
---

# Metafore Graphic Builder

You are helping a Metafore teammate produce brand-compliant HTML graphics. These are self-contained HTML files rendered at a fixed pixel size, then screenshotted to PNG for use in blogs, websites, social media, and marketing materials.

## Brand reference (read before producing)

Read `../../assets/brand/metafore_brand.md` first — voice, AI tells, legibility floors, density, tokens, and the build/check toolchain. This file adds only graphic-specific rules. Paths are relative to this skill's directory.

**Marketing's 2026 surface rules apply to graphics without exception:** solid fills, no shadows, one accent family (teal stack), white-first. Cards separate from their background with a 1px border, not elevation. The only texture is the brand dot pattern (one per surface).

## When this triggers

Any request along the lines of:
- "Make a blog hero graphic for [topic]"
- "Create card illustrations for [vertical]"
- "I need graphics for the [vertical] website page"
- "Make a conversational demo card for [use case]"
- "I need an OG image / social preview for [content]"
- "Make a pull-quote graphic from [quote]"
- "Create website graphics", "feature cards", "section illustrations"
- "Make a hero image", "blog graphic", "featured image"
- Any mention of Metafore-branded visual assets for digital use

Do not trigger for Figma brochures (use `metafore:brochure`), dashboards (use `metafore:dashboard`), slide decks (use `metafore:deck`), or Word/PDF documents (use `metafore:doc`).

---

## Brand-critical rules

These are non-negotiable design constraints. They apply to **every** graphic type below — when in doubt, follow these first.

### Backgrounds

- **No diagonal stripes.** `repeating-linear-gradient` stripe overlays are removed from the system. Texture comes from dots only.
- **Never combine two dot patterns on the same surface.** Pick ONE:
  - a **full dot grid** (small evenly-spaced dots, ~6–8px) OR
  - a **duotone-fade dot pattern** (dots fading from one corner via radial mask).
  Never both stacked.
- **Full-screen dark surfaces are SOLID.** Hero-sized dark-teal panels — Type 1B background (1422×800), Type 1C right panel, Type 2 conversational background — render as solid `--teal-dark` with **no** dot decoration. Dot patterns are reserved for lighter or smaller surfaces (Type 1A's teal-light right panel, Type 3 small data cards, Type 4 capability tiles, Type 6 horizontal features).

### Palette

- **Teal stack only for branded fills.** Forbidden: indigo, emerald, sky, slate, mint, violet, periwinkle, and any other non-teal gradient. Tile and panel fills draw from `--teal-dark` (#004D50), `--teal` (#006B6F), `--logo-dark` (#035657), `--teal-light` (#E8F4F5), or `--bg-solid` (#F8FAFA). Status colors (coral / amber / success) appear only as semantic state indicators, never as decoration.

### Type floor

- Nothing essential below **15px**; Plex Mono labels, pills and eyebrows **13px**; card body **16px**; lede **18px**. Graphics are usually shown scaled down, so these are minimums at the authored size. When a card overflows, cut rows or words — don't shrink type.
- Paragraphs ≤ 3 lines; three or more parallel facts become bullets or rows.

### Logo

- **Always use the real Metafore SVG wordmark.** Never substitute CSS pseudo-element constructions (two-quarter-circle marks built with `border-top-left-radius:100%`).
- Insert with `<!-- @logo:logo-light width="155" height="36" -->` on white / `--bg-solid` surfaces (Type 7 OG, Type 8 pull-quote) and `<!-- @logo:logo-dark … -->` over `--teal-dark` (Type 1B, 1C glass-card header). Never the retired `#00C4CC` variant. Sizes and don'ts: `references/logo-svgs.md`.

### Arrows

- **Arrowhead apex lies at the end of the line.** Standard CSS construction on the line span:

  ```css
  .ln{height:2px;background:var(--teal);position:relative}
  .ln::after{
    content:"";position:absolute;
    left:100%;top:-3px;
    border:4px solid transparent;
    border-left-color:var(--teal);
  }
  ```

  The arrowhead's base touches the line's end (`left:100%`); the apex points just past. **Never** leave the arrowhead floating before the line terminates.

### Bracketed-term accent

- **No bracket-box / corner-bracket treatment for headline text.** Highlighted terms render as plain headline text in `--logo-dark` — no monospace font, no tinted background, no four-corner L-brackets. (The older bracket-frame pattern in this skill is retired. Don't reintroduce it.)

### Headline layout (multi-line stacks)

- When a hero headline stacks across multiple lines (Type 1C "What is / [term] / subtitle"), use **natural block flow**: each line is `display:block` and a single shared `line-height` (~1.12) carries the row spacing.
- **Do NOT use** `display:flex; flex-direction:column; gap:...` for headline stacks. The gap adds spacing on top of line-height, and lines whose words have descenders (g, p, y) appear visually taller — breaks row consistency.

### Voice / agent naming

- **"Mira" is the personal-agent product for telco subscribers only.** Use the "Mira · personal agent" identification only in telecom conversational cards. For airlines, banking, supply chain, health, HR, public sector, etc., use generic "Metafore" / "Metafore · cognitive agent" naming inside conversational UI.
- Brand vocabulary and the AI-tell list from the brand pack apply to every word in a graphic.

---

## Graphic Types

There are nine graphic families in the Metafore system. Each has its own visual language, dimensions, and construction rules.

---

### 1. Blog Hero Graphics

Three sub-formats. All ~1422 × 800px.

---

#### 1A. Split White / Halftone Data Card

The primary blog hero format.

**Layout:** Two-column CSS grid (`1fr 1fr`).
- **Left panel** — white background. Vertically centered content: IBM Plex Mono eyebrow label (teal, uppercase, tracked), large Geist headline (weight 400, 56–60px, one word in `<span class="accent">` renders in `#035657`), Inter lede paragraph (18px, ink-2, max-width 460px).
- **Right panel** — `#E8F4F5` teal-light background with a **single full dot grid** (`radial-gradient` circles, 6px grid, `rgba(0,107,111,0.32)`). **Only this one pattern** — no duotone-fade overlay on top, no diagonal stripes. Contains a single white floating card.

**The right-panel card** is the creative element — it carries the data that reinforces the blog's thesis. Vary the card type across blogs:

- **Before / after timeline** — two stacked timeline blocks. "Without orchestration" shows a segmented bar with interleaved coral-hatched gap segments (handoff waste), system labels below. "With orchestration" shows a continuous teal bar. Big time stat per row. Footer strip shows the delta in teal. *Use when the blog compares a fragmented vs orchestrated cycle time.*
- **KPI grid + horizontal bar chart** — top row of 2–3 KPI cells (Plex Mono numbers, tiny delta labels), below it a labeled horizontal bar chart (by hub, by region, by segment) with teal-stack fills, plus an amber/coral bar or two for at-risk values. *Use when the headline rests on a comparative metric.*
- **Phase bars** — numbered steps (01–04), each with a phase label, a time/status stat (mono, color-coded), and a horizontal bar. *Use for multi-step processes where each step has a cost.*
- **Sparkline / area chart + KPI strip** — full-width SVG line/area chart (teal stroke, teal-light fill) with a KPI strip above and a footer label. *Use for trend stories or "before they call" narratives.*
- **Process flow** — sequential steps with timing data and an active-step highlight.

The card should feel like a real UI component. Use realistic system names, plausible metrics, and specific data points (flight numbers, loan amounts, SKU IDs).

**Exact CSS recipes:** See `references/blog-hero-recipes.md`.

**File location:** `Blogs/BLOG GRAPHICS/blog-{slug}-hero.html`

---

#### 1B. Full Teal + Floating UI Card

A single-surface blog hero on solid dark teal.

**Layout:** Single panel. **SOLID** `--teal-dark` (`#004D50`) background. **No dot pattern, no halftone, no diagonal lines, no overlays of any kind — the surface is solid.**

- **Metafore wordmark** — top-left, ~40px from edges. **Use the dark-bg logo SVG variant** (`fill="white" fill-opacity="0.5"` for the two curves, `fill="white"` for the three marks and the wordmark). See `references/logo-svgs.md`.
- **Headline** — large white text (Geist/Inter, 48–56px, weight 400–500), left-aligned, in the left half of the frame.
- **Subtitle box** (optional) — a secondary line of text inside a bracket-bordered container. Thin `--teal-on-dark` (`#88DCE0`) L-shaped corner brackets at each corner; Plex Mono uppercase content inside, white at ~90% opacity. (This corner-bracket *box* is distinct from the retired headline bracket treatment in 1C — it's a small UI badge, not headline framing.)
- **Floating UI card** — positioned right of center. Glassmorphism: `backdrop-filter: blur(18px)`, `background: rgba(255,255,255,0.08)`, `border: 1px solid rgba(255,255,255,0.14)`, `border-radius: 16px`. Inside: a realistic product UI mockup — workflow stepper with Sense / Reason / Act steps, a 2-up KPI strip, dashboard fragment, etc. The glass card is the only visual interest — the dark surface stays clean.

**File location:** `Blogs/BLOG GRAPHICS/` as PNG (HTML source alongside)

---

#### 1C. Split White / Teal with Color-Accent Term

A split-panel variant. Left side highlights a key definitional term; right side carries a glass UI on solid dark teal.

**Layout:** Two-column split, white left / **solid `--teal-dark`** right.

- **Left panel (white):**
  - Eyebrow (IBM Plex Mono, teal, uppercase, tracked) — e.g. "Definition · Metafore for Telecom"
  - Headline stack using **block-level lines** — `display:block` per line, single shared `line-height: 1.12`. Do **not** use `display:flex; flex-direction:column; gap`.
  - The accent term is wrapped in `<span class="bracket">…</span>` and renders in `--logo-dark` — same Geist font and size as the rest of the headline. **No corner brackets. No monospace. No tinted background.** The `.bracket` class is just a color wrapper.
  - A subtitle paragraph below (Inter, 20px, `--ink-3`)
  - A short lede paragraph (Inter, 18px, `--ink-2`)
- **Right panel (solid `--teal-dark`):**
  - No dot pattern. Solid surface.
  - Contains a glassmorphism product UI card (same construction as 1B's glass card) showing a workflow or dashboard. The glass card's header uses the dark-bg Metafore SVG logo variant.

**Why retired:** older versions of this skill used a bracket-frame box around the key term (four L-shaped corner brackets, gray background, IBM Plex Mono font). That treatment is fully retired — use plain headline text with `--logo-dark` color accent only.

**File location:** `Blogs/BLOG GRAPHICS/` as PNG or HTML

---

### 2. Conversational Demo Cards

Hero graphics depicting a Metafore cognitive agent in action — a realistic conversation between the agent and a user. Used on vertical website pages.

**Dimensions:** Typically ~640 × 800 (portrait) or ~640 × 380 (landscape).

**Visual signature:**

- **Background:** SOLID `--teal-dark` (`#004D50`). **No photography, no glass-on-photo composite, no dot pattern.** The dark teal surface is a deliberate brand accent block.
- **Header strip (above the card):** Plex Mono uppercase, white at ~85% opacity. Left side names the agent ("Mira · personal agent" for telecom OR "Metafore · cognitive agent" for any other vertical). Right side shows the session timestamp.
- **Card:** A solid WHITE card sits centered on the dark teal background. Rounded corners (~18–20px), no glass blur — this is a plain white surface, not glassmorphism.

**Conversational UI anatomy (top to bottom inside the card):**

1. **Status bar** — `--teal-light` fill, Plex Mono uppercase label in `--teal-dark`. Status dot (coral / amber / teal) on the left, scenario summary text on the right.
2. **Agent message block** — starts with a 36px Metafore icon (dark teal circle + white chevron SVG) inline with a bold first-person statement. E.g. "I've already rebooked you on EK030 at 21:15…" / "I've raised the ticket and credited your bill…"
3. **Detail content** — key-value rows in a soft tray (`--bg-solid` background, light border). Each row is a Plex Mono uppercase label + value pair.
4. **Callout** (optional) — `--teal-light` background with a small "i" indicator and a one-line tip.
5. **Action buttons** —
   - **Primary CTA:** Full-width, `--teal-dark` background, white text, 999px radius.
   - **Secondary CTAs:** Two side-by-side outline buttons, `--bg-solid`/white background with subtle border.

**Agent naming inside the header / status:**
- Telecom verticals: "Mira · personal agent"
- All other verticals: "Metafore · cognitive agent"

**The Metafore icon inside conv cards** is a dark teal circle (`--teal-dark`) containing a white chevron SVG — distinct from the wordmark logo. Don't substitute the wordmark here, and don't render it as a CSS quarter-circle construction.

**Voice:** First-person, proactive, specific. Always names concrete data and concrete next actions. Never generic.

**File location:** `Graphics/{Vertical}/` as PNGs

---

### 3. Small Data/Feature Cards

Compact graphics used as feature tiles on website vertical pages.

**Dimensions:** ~640 × 380px (landscape, ~5:3)

**Visual signature:**

- **Background:** A solid `--bg-solid` (`#F8FAFA`) or `--teal-light` base PLUS one duotone-fade dot pattern.
- **No diagonal stripes.** **No full-dot grid stacked under the duotone fade.** Just a solid base + one fade.
- **White floating card:** Centered, clean data display. Title, a few data rows or a route block, and a status pill. 1px `--line` border, no shadow.

**Content types:**
- Tracking cards — bag/order ID + route block + status pill
- Service activation — order ID + step progress + ETA
- Profile / account cards — patient or subscriber records
- Compact charts — sparkline + stat

When showing a route arrow, use the **standard arrow construction** (arrowhead apex at the line's end — see Brand-critical rules → Arrows).

**File location:** `Graphics/{Vertical}/` as PNGs

---

### 4. Vertical Card Illustration Grid

Sets of 4–7 cards in a responsive grid. Used for capability sections on vertical web pages.

**Dimensions:** Each illustration is 4:3 aspect ratio inside a 4-up responsive grid (max-width 1600px).

**Layout per card:**

- **Illustration block** — rounded rectangle (14px radius). **Fill from the teal stack only** — `--teal-dark`, `--teal`, `--logo-dark`, `--teal-light`, or `--bg-solid`. Forbidden: indigo, emerald, sky, slate, mint, violet, periwinkle.
- **One duotone-fade dot texture** per card. Vary the mask corner-origin across the row (TL / TR / BL / BR) so the set reads as visual variety without leaving the brand. Use white dots on dark fills (`bg-dark` / `bg-teal` / `bg-acc`); use teal dots on light fills (`bg-light` / `bg-solid`).
- **Floating white UI card** inside — depicts a realistic micro-UI. **Vary the UI form across tiles** — never four identical KV-row cards in a row. Mix at least three of:
  - KV rows (key/value pairs with status colors)
  - Bar chart (Mon–Sun, teal-stack bars)
  - Donut chart (conic-gradient, 50–90% fill)
  - Sparkline / area chart (SVG path with teal stroke + tinted fill)
  - Horizontal bar chart (hub or system labels with teal-stack bars)
  - Status timeline (dots connected by lines, current step amber-pulsed)
  - Process flow stepper (Sense / Reason / Act / Close)
- **Below the illustration** — card title (18px, Inter 600) and card body (16px, 2 lines max)

**Palette and texture recipes:** See `references/card-palettes.md`.

**File location:** `Supply Chain/mockups/card-illustrations.html` or `Graphics/{Vertical}/card-illustrations.html`

---

### 5. Concept Illustrations

Larger editorial illustrations for platform-level concepts. More artistic; varies more in style.

**Dimensions:** Varies — typically ~800 × 600 (landscape) or ~640 × 640 (square)

**Sub-styles:**

**A. Dark isometric / knowledge graph** — dark background (`#0F1416`) with a **single** dot grid, isometric shapes (diamonds, layers) in white-to-gray gradient, connected by thin `--teal-on-dark` (`#88DCE0`) lines. Step labels in small glass cards. Used for the knowledge fabric and similar architectural concepts.

**B. Network topology** — dark background with central hub node + satellite nodes connected by thin `--teal-on-dark` (`#88DCE0`) lines (some dashed for inferred relationships). Used for telecom / data fabric / connectivity concepts.

**C. Teal abstract** — teal-tinted background with one dot pattern. Large Metafore icon centered in a glass circle. Used for brand-level concepts.

**D. Security / trust** — dark background with hexagonal glass containers holding icons (lock, shield + checkmark, Metafore mark). Teal stack only, like every other type (the old blue-purple trust tint is retired — one accent family).

**File location:** `Graphics/General Illustrations/`

---

### 6. Horizontal Feature Cards

Feature graphics used across the website for cross-vertical capability sections.

**Dimensions:** ~640 × 380px (landscape)

**Visual signature:**

- **Background:** Solid `--bg-solid` or `--teal-light` base + **one** duotone-fade dot pattern. No stripes. No double-stacked dot grids.
- **Content:** Floating white card(s) showing the capability. Can include: notification cards with status pills, chat interfaces with the Metafore icon responding, data cards with inline charts (bar, donut, sparkline), patient/subscriber profiles, third-party integration cards.

**Notification card construction:** Plain white card, rounded corners, 1px `--line` border, no shadow. **No colored left border** (no red stripe, no coral stripe, no teal stripe). Priority is communicated via a status pill **inline with the title**, never via a border.

**File location:** `Graphics/Horizontals/`

---

### 7. OG / Social Preview Images

**Dimensions:** 1200 × 630px (standard OG) or 1080 × 1080px (square social)

**Layout:** White background, **solid** 8px `--teal-dark` bar on the left edge (not a gradient).

Three zones:
- **Top** — real Metafore SVG wordmark (light-bg variant — see `references/logo-svgs.md`) on the left, IBM Plex Mono uppercase meta label on the right ("Whitepaper · 2026", "Field report · 2026", etc.)
- **Middle** — eyebrow + large headline in Geist/Inter (64px). Accent word/phrase in `--logo-dark` via `<span class="accent">`.
- **Bottom** — footer line with URL or tagline

**Logo:** Real Metafore SVG only. Never the CSS pseudo-element construction.

**File location:** Alongside the content it serves, e.g. `Whitepapers/og-image-{slug}.html`

---

### 8. Pull-Quote Cards

**Dimensions:** 1080 × 1080px (Instagram/LinkedIn square)

**Layout:** White background, **solid** 8px `--teal-dark` bar on the left edge.

- **Top** — eyebrow + section label (left), page/section number in IBM Plex Mono (right)
- **Middle** — large quote text in Geist 72px (line-height ~1.18), accent on the key phrase in `--logo-dark`. Open-quote glyph in `--teal` (`#006B6F`) as ornament on light; `--teal-on-dark` on dark.
- **Bottom** — attribution line (Geist who + Inter role) + Metafore wordmark SVG (light-bg variant)

**File location:** `Whitepapers/pullquotes/pullquote-{nn}.html`

---

### 9. Line Icons

Minimal geometric line-art on white backgrounds. Used as spot illustrations throughout the site.

**Library-first approach.** A **library of 29 approved icons** ships with the plugin. Before generating a new icon, pick from the concept index in `references/line-icons-library.md` and reference it as `src="@icon:Name"` rather than redrawing.

**When to generate a new icon:**
1. **The user explicitly asks for a new icon** (e.g. "design a new icon for X", "make a fresh icon", "generate a custom icon", "don't reuse — draw a new one"). Honor the request directly.
2. **No library icon fits the concept.** Scan the index first, and only generate when nothing in the library represents the idea.

In both cases, new icons must match the library's visual language exactly so they can be added to the approved set after review.

**Dimensions:** Library masters are ~1400×900px PNGs with the icon centered in significant whitespace. When rendering new icons inline (e.g. an icon row in HTML), the SVG renders inside ~80–120px per icon with the same proportional whitespace.

**Visual language (extracted from the approved set):**

- **Pure greyscale on white.** No teal, no color of any kind. Icons live in the brand's neutral zone — color accents come from the rest of the page, not from the icons themselves.
- **Three-tier value hierarchy:**
  - **Focal (`#0A0A0A` / black)** — exactly ONE element per icon carries the eye. The "thing being emphasized" — a node, a square, a circle, an intersection wedge. Outline stroke or solid fill.
  - **Secondary (`#666666` / mid-grey)** — the next layer of meaning. Adjacent shapes, secondary nodes.
  - **Background (`#CCCCCC` / light grey)** — supporting shapes, faded earlier states, tertiary context.
- **Fine outline strokes.** Default `stroke-width: 1` to `1.5` (depending on icon size). Never thicker than 2.
- **Fills only on tiny nodes.** Small filled solids — black squares (~4–6px), black circles (~4–8px) — mark connection points where strokes meet shapes. Use solid black for the focal node, mid-grey for secondary nodes, light grey hollow circles for tertiary nodes.
- **Generous whitespace.** The icon occupies the middle 50–70% of the frame. Never edge-to-edge.
- **Geometric primitives only.** Circles, squares, isometric diamonds (rotated parallelograms), ellipses, lines, curves, simple arrows. No skeuomorphic detail.
- **Arrowheads obey the arrow rule.** When an icon includes a directional arrow, the arrowhead apex sits at the end of the line — never floating before it.

**Compositional patterns from the library** (use these as starting points when generating new icons):

| Pattern | Library examples | When to use |
|---|---|---|
| Concentric scaling (light → dark) | `Amplify`, `Ellipses`, `NestedSquares`, `Scale`, `Scale2`, `Fan` | Growth, amplification, layered states |
| Trio with one accent | `Cycle`, `Orbit`, `Stack`, `Squares2`, `Icon2`, `Connect` | Process steps, sequenced states, layered planes |
| Connected nodes / graph | `Nodes`, `Nodes2`, `Connected`, `Connect`, `Integration` | Networks, relationships, dependencies |
| Overlap / intersection | `Collaborate`, `Venn`, `Squares`, `Ensemble` | Shared state, intersection, collaboration |
| Frame + focal subject | `Detection`, `Icon3`, `Process` | Detection, focus, scope, scan |
| Cycle / flow | `Cycle`, `Icon1`, `ThroughLine`, `Transform` | Loops, processes, transformations |
| Axis / coordinate | `Axis`, `Measure`, `Scale2` | Measurement, dimensions, range |
| Cross-flow / bi-directional | `CrossSell` | Exchange, sync, mutual relationship |

**SVG construction for new icons** (when a library icon doesn't exist):

```css
.icons .ic svg{
  width:80px;height:80px;fill:none;
  stroke-linecap:round;stroke-linejoin:round;
}
.icons .ic svg .bg{stroke:#CCCCCC;stroke-width:1.2}   /* light-grey tertiary layer */
.icons .ic svg .mid{stroke:#666666;stroke-width:1.2}  /* mid-grey secondary layer */
.icons .ic svg .fg{stroke:#0A0A0A;stroke-width:1.5}   /* black focal element */
.icons .ic svg .node-bg{fill:#CCCCCC;stroke:none}
.icons .ic svg .node-mid{fill:#666666;stroke:none}
.icons .ic svg .node-fg{fill:#0A0A0A;stroke:none}     /* the one filled focal node */
```

Exactly **one** `.fg` element per icon. Build the rest of the composition out of `.bg` and `.mid`.

**File location:** new SVGs awaiting approval go in `generated/` next to the output file.

---

## Tokens, fonts, logos, icons

`assets/tokens.css` holds the palette, font stacks, label/caption/card/lede sizes and base resets — include it with `/* @tokens:graphic */`, fonts with `<!-- @fonts -->`, logos with `@logo:`, icons with `@icon:`. Full token reference: `references/design-tokens.md`. Background textures: `references/background-patterns.md` (dots only; one pattern per surface; full-screen dark panels solid). Headlines: Geist 400, 56–72px, tracking −0.025em, line-height 1.04–1.18.

## Workflow

### 1. Understand the request

Determine which graphic type is needed. If unclear, ask. Collect:
- **Graphic type** — which of the 9 types above
- **Topic/vertical** — what vertical or subject (vertical drives agent naming for Type 2 — Mira only on telecom)
- **Content** — headline text, data to show, use case to depict
- **Card variant** (for Type 1A) — timeline, KPI+bar chart, phase bars, sparkline, or process flow

For **conversational cards**, also determine:
- Vertical → drives agent naming
- What use case / scenario the agent is helping with
- What data the agent surfaces
- What action buttons make sense

For **card illustration sets**, also collect:
- How many cards (typically 4–7)
- Card titles and descriptions
- Which UI form each tile should show — vary the UI types across the set

### 2. Draft the content

Apply Metafore voice rules (cognitive agents, orchestration, knowledge fabric). For conversational cards: first-person, specific, action-oriented. For blog hero headlines: accent the key word in `<span class="accent">` rendered in `--logo-dark`.

### 3. Build the HTML

Author `<slug>.src.html`: explicit `width`/`height` on the outer frame, CSS grid/flex layout, placeholders for tokens, fonts, logo and icons. Follow the brand-critical rules above.

### 4. Assemble, check, render

```
python3 ../../scripts/build_html.py <slug>.src.html
python3 ../../scripts/check.py <slug>.html --kind graphic
python3 ../../scripts/render.py <slug>.html --out <slug>.png --scale 2
```
Fix every ERROR in the src file and rebuild. `render.py` writes the 2× PNG for delivery plus `<slug>.preview.png` (≤1600px) — **Read only the preview**, once. Save to the location for the graphic type.

## Quality Checklist

Before delivering, verify:

**Brand-critical rules**
- [ ] No diagonal stripe overlays anywhere
- [ ] No surface combines a full dot grid AND a duotone-fade dot pattern
- [ ] Full-screen dark hero panels (1B, 1C right, conv bg) are SOLID `--teal-dark` — no dot decoration
- [ ] Tile fills (Type 4) draw ONLY from the teal stack — no rainbow gradients
- [ ] No colored border-left on notification cards (Type 6)
- [ ] No bracket-box / corner-bracket treatment around accent terms in headlines (Type 1C)
- [ ] Type 1C h1 uses block flow with consistent line-height — never flex-column-with-gap

**Logo**
- [ ] Real Metafore SVG wordmark, not CSS pseudo-elements
- [ ] Dark-bg surfaces use the white-opacity logo variant
- [ ] Light-bg surfaces use the logoLight/logoDark logo variant
- [ ] OG/pull-quote left bar is SOLID `--teal-dark` (not a gradient)

**Agent naming / voice**
- [ ] "Mira" used only in telecom conversational cards; other verticals use "Metafore · cognitive agent"
- [ ] First-person agent voice; no chatbot/automation/synergy/seamless/end-to-end/leverage language

**Type 9 line icons**
- [ ] Checked the library index first; reused an existing icon (`@icon:Name`) if a concept matches
- [ ] Only generated a new icon if (a) the user explicitly asked for a new one or (b) no library icon fits
- [ ] Pure greyscale only — no teal, no color
- [ ] Three-tier value hierarchy: one black focal element, mid-grey secondary, light-grey tertiary
- [ ] Fine outline strokes (≤ 1.5px); no strokes thicker than 2
- [ ] Filled nodes (small squares / circles) used only at connection points
- [ ] Generous whitespace — icon occupies the middle 50–70% of the frame

**Arrows**
- [ ] Any arrow has its apex AT the end of the line (CSS triangle on `::after` with `left:100%; top:-3px`)

**Construction**
- [ ] `check.py --kind graphic` reports zero ERRORs (labels ≥ 13px, everything else ≥ 15px, card body 16px, lede 18px)
- [ ] Correct dimensions for the graphic type
- [ ] Geist + Inter + IBM Plex Mono loaded from Google Fonts
- [ ] Teal accent word in headlines uses `--logo-dark` (#035657)
- [ ] Status colors are semantic only (coral=fail, amber=warn, success=pass, teal=good)
- [ ] Card data is realistic and specific (real-sounding system names, plausible metrics, named IDs)
- [ ] File is fully self-contained (no external images or scripts)
