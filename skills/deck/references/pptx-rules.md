# PPTX Brand Rules

These rules apply when generating the `.pptx` from the HTML. They diverge from the HTML-side rules in a few specific places — the generator must enforce these, not the author.

## Canvas

- **Widescreen 16:9.** PPTX dimensions: `13.333" × 7.5"` (`12192000 × 6858000` EMU).
- **Coordinate conversion.** `1 px = 9525 EMU`. A 1920×1080 HTML canvas maps exactly to the 13.333" × 7.5" PPT canvas at 9525 EMU/px.
- **One slide per `<section class="slide">`** in the HTML, in document order.
- **No slide master inheritance.** Each slide gets its content placed at absolute EMU coordinates. Don't rely on PowerPoint slide layouts.

## Fonts

- **Primary fonts**: `Geist` for headers, `Inter` for body, `IBM Plex Mono` for mono. These are declared on every text frame.
- **Fallback chain**: If the client machine doesn't have Geist or Inter, PowerPoint falls back through the system stack. Don't embed fonts in the PPTX — file size grows fast and licensing gets murky.
- **No design-intent font name** (Brut Grotesque, GT America) appears in the PPTX. The fallback to Geist/Inter is the deck's actual font.

## Plex Mono — divergent rules in PPTX

These are PPTX-only. The HTML uses tracked Plex Mono for eyebrows; the PPTX does not.

- **No letter-spacing.** Set character spacing to `0` on every Plex Mono text frame. Even if the HTML eyebrow uses `letter-spacing: 0.16em`, the PPT text frame uses `0`.
- **No bold.** Plex Mono weight in PPTX is always `400`, regardless of HTML weight.
- **Uppercase stays uppercase.** The HTML `text-transform: uppercase` is converted at generation time — write the actual uppercase string into the PPT text frame, don't rely on a "CAPS" formatting attribute.

The rationale: tracked Plex Mono renders cleanly in CSS where the browser hints the kerning. In PPT, the same tracking value spreads the letters into a thin uneven line. Removing tracking and bold is the only way to keep the eyebrow legible in PPT at the same point size as the HTML.

## Negative letter-spacing — clamp under 22px

- **Headers ≥ 22px** in the HTML keep their negative letter-spacing. Convert directly: `-2.4px` HTML → `-240` (hundredths of a point) in the PPT character-spacing attribute. (PowerPoint's text-frame XML uses `<a:rPr spc="-240">`.)
- **Anything < 22px** clamps to `0`. The PPT rendering of small text with negative tracking collapses adjacent characters.

## Two-tone hero — run-splitting

The cover headline and most internal slide headlines have a two-tone treatment: ink color for most words, accent color for the last word(s) wrapped in `<span class="accent">` or `<span class="bracket">` or `<span class="accent-light">`.

This must become **one text frame with two runs**, not two text frames.

**XML pattern** (python-pptx-compatible):

```python
tf = shape.text_frame
p = tf.paragraphs[0]
r1 = p.add_run()
r1.text = "Cognitive agents for "
r1.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)   # --ink

r2 = p.add_run()
r2.text = "every subscriber"
r2.font.color.rgb = RGBColor(0x03, 0x56, 0x57)   # --logo-dark
```

**Color mapping by accent class:**

| HTML span class | PPT run color | Use case |
|---|---|---|
| `.accent` | `#035657` (`--logo-dark`) | On light/white panels — cover 1A, 1C, content slides |
| `.bracket` | `#035657` (`--logo-dark`) | Cover 1C's block-flow headline accent term |
| `.accent-light` | `#00C4CC` (`--teal-bright`) | On dark `--teal-dark` panels — cover 1B, section dividers |

The line-break inside `.bracket` (cover 1C) is preserved as a paragraph break or a soft return inside the run.

## Block-flow headlines (cover 1C)

Cover 1C uses three lines stacked via `display: block` with a shared `line-height: 1.12`. In the PPTX:

- One text frame
- Three paragraphs (one per `.line` span)
- Same `line-height` (PPT's `lnSpc` attribute, percent-based: `112000` = 112%)
- The middle paragraph's run carries the `.bracket` accent color, the others are ink
- Word-wrap disabled inside the text frame — each `.line` is its own paragraph

## Shapes

- **No drop shadows.** Set `<a:effectLst/>` empty on every shape. PowerPoint defaults to a faint shadow on text boxes — this must be stripped.
- **1px borders on cards.** When the HTML has `border: 1px solid var(--line)`, write `<a:ln w="9525"><a:solidFill><a:srgbClr val="ECECEC"/></a:solidFill></a:ln>` (1 px = 9525 EMU line weight).
- **No rotations.** Every shape is at 0°. Designs that rotate text are not Metafore.
- **Solid fills only.** No gradient fills, no patterned fills, no picture fills (except full-bleed background PNGs on image/hybrid tier slides).

## Image-tier and hybrid-tier backgrounds

- **Image tier**: the rendered PNG fills the whole slide (`0,0` to `13.333", 7.5"`). It is a single `pic` shape with no border, no shadow, behind any text frames.
- **Hybrid tier**: the rendered "text-hidden" PNG fills the whole slide as the bottom layer. Editable text frames sit on top, at coordinates measured from the original (text-visible) HTML's `getBoundingClientRect()`.
- **PNG render scale**: 2x source resolution (3840×2160) for retina-clean placement. The generator may downscale on insertion or let PowerPoint sample.

## Mark placement on PPTX slides

Two marks ship as four SVG files in `assets/`: full wordmark (`logo-light.svg` / `logo-dark.svg`) and icon-only (`icon-light.svg` / `icon-dark.svg`).

- Convert SVG → PNG at 2x for PPT (SVG support is unreliable across PowerPoint versions).
  - **Cover (full wordmark)**: native 155×36 → 310×72 PNG.
  - **Every other slide (icon only)**: 72×60 → 144×120 PNG.
- Placement:
  - **Cover**: wordmark top-left, offset from edges by `var(--chrome-offset)` (~56 px → ~533400 EMU).
  - **Content slides + closing**: icon top-right, offset from the right edge by the same `var(--chrome-offset)`.
- The PNG is NOT a slide-master element. It's a per-slide picture so its position can vary slide-to-slide if needed.

## Footer line on every PPTX slide

Every slide gets the same two-text-frame footer at the bottom edge:

- **Bottom-left frame**: `© <CURRENT-YEAR> METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL`
- **Bottom-right frame**: page number `NN / NN`

Both frames use IBM Plex Mono at 11pt, weight 400, no letter-spacing (PPTX brand rule strips Plex Mono tracking), uppercase, color `var(--ink-3)` (`#666666`) on light slides or `rgba(255,255,255,0.5)` on `--teal-dark` slides.

The year string is computed at generation time from the system date, not hard-coded. Re-running the generator next year produces a deck stamped with the new year automatically.

The footer EMU coordinates are constant across the deck:
- Bottom-left frame: `(x=120px, y=1024px)` in HTML → `(1143000, 9753600)` EMU
- Bottom-right frame: `(x=<right-edge - text-width>, y=1024px)` — measure the text width at PPT time via python-pptx's `Pt(11)` rendering, then anchor right.

## Speaker notes

- Speaker notes are read from an optional `<aside class="speaker-notes">…</aside>` element inside each `<section class="slide">`.
- The aside is `display: none` in the HTML — it doesn't render in the preview.
- Each slide's notes paragraph becomes the notes-master text frame in the corresponding PPT slide.

```html
<section class="slide" data-pptx="semantic" data-slide-id="04-what">
  <!-- ...slide content... -->
  <aside class="speaker-notes">
    Spend 60 seconds on this slide. Land the "sense, reason, and act" frame
    before moving to the Pulse capability grid.
  </aside>
</section>
```

## What never appears in the PPTX

- Animations (entrance, exit, emphasis, motion paths)
- Slide transitions (other than instant cut)
- Builds (no sequential appearance)
- Auto-advance timing
- Hyperlinks on decorative text (only on the CTA email/URL on the closing slide)
- Comments, revision marks, or tracked changes
- Hidden slides
- Background music
- `#00C4CC` (the retired "teal-bright" cyan). Use `--teal-accent #00989E` instead for any dark-surface accent or stroke color.
- Coral / amber / red as decoration. Status colors are state-only — never use them for visual emphasis.

Decks are static documents. The presenter advances them manually.

## SVG authoring gotchas (inline SVG inside `.slide`)

Every illustration the deck builds inline as SVG — Pulse mini-cards, knowledge graphs, function-silo networks, four-graph tile schematics — runs into the same handful of cross-renderer / build-pipeline issues. Don't relearn them.

### Pill buttons need explicit `rx` = half-height
**`rx="999"` on an SVG `<rect>` does NOT auto-clamp the way `border-radius: 999px` does in CSS.** It draws a literal 999-unit radius, which on a wide button (e.g. `width="432"`) collapses into a near-ellipse shape, not a pill. Always use `rx="<half-the-height>"` explicitly:

```svg
<!-- Wrong: renders as a flattened ellipse -->
<rect x="84" y="540" width="432" height="40" rx="999" fill="#004D50"/>

<!-- Right: clean pill -->
<rect x="84" y="540" width="432" height="40" rx="20" ry="20" fill="#004D50"/>
```

This bit slide 4 in this deck — the button looked like a stretched oval until the rx was fixed.

### Recognized accent classes (build-script-aware)
The PPTX builder's `ACCENT_COLORS` map only recognizes these class names when splitting a text frame into colored runs. Any other class will render in the parent's color regardless of CSS.

| Class | Render color | Use |
|---|---|---|
| `.accent` | `--logo-dark` `#035657` | two-tone hero on light surfaces |
| `.bracket` | `--logo-dark` `#035657` | cover headline second word |
| `.accent-light` | `--teal-accent` `#00989E` | two-tone hero on `--teal-dark` surfaces |
| `.t` | `--logo-dark` `#035657` | product-name accent (`<span class="m">MetaWorks</span> <span class="t">Focus</span>` on the 12-up module grid) |

If you introduce a new accent class, add it to `ACCENT_COLORS` in `build_pptx.py` — or use one of the four above.

### Whitespace between sibling color spans
A two-tone hero like `What we'll cover.` is authored as two siblings:

```html
<h2>What we'll <span class="accent">cover.</span></h2>
```

The space character between `'ll` and `<span>` is **literal** — without it the build renders `What we'llcover.`. The same applies to multi-line composition with line-spans:

```html
<h1>
  A shared nervous system for the
  <span class="accent-light">enterprise.</span>
</h1>
```

The newline + indent before `<span>` collapses to a single space in the run output. The build script preserves *interior* whitespace inside a paragraph; it cannot invent whitespace that isn't in the source.

### Special characters — UTF-8 throughout
Multiplication signs (`×`), minus signs (`−`, U+2212), em dashes (`—`), and the like need UTF-8 handling end-to-end. The build script parses HTML via `lxml.html.HTMLParser(encoding="utf-8")` for this reason — without the explicit encoding, lxml defaults to Latin-1 and produces double-encoded glyphs (`4×` → `4Ã—`). When authoring inline SVG `<text>`, paste the actual unicode character, not an HTML entity.

### Locked vs editable inside an illustration card
When a slide carries a UI card (Pulse view, conversational demo, etc.), the **entire card** is locked into the background PNG — its eyebrow, title, KPI rows, recommendation copy, and CTA are *not* editable text frames in the PPTX. The text frames that survive are only the slide's headline / body / chrome. If a customer needs the card content editable, swap it for an `<img>` they can replace, or move the data into the slide's left-column text — don't try to make every card field a text frame, the position math gets fragile.

## Accessibility hooks (write when present)

- Every text frame gets a paragraph with proper font + color, so screen readers handle reading order.
- Every image gets `<a:descr>` alt text from the HTML's `<img alt="…">` or `data-alt="…"`. For cover slides, write a one-sentence description of the visual ("Solid dark teal hero with glass card showing a workflow.").
- Reading order in the PPT shape tree should match the visual top-to-bottom, left-to-right order of the HTML elements.
