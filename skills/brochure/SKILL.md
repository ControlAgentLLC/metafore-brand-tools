---
name: brochure
description: Build Metafore-branded marketing brochures, product overviews, one-pagers, and multi-section sales collateral as self-contained HTML files. Use this skill whenever a Metafore teammate asks for a brochure, product overview, sales sheet, marketing one-pager, customer-facing PDF, "Metafore-ify this doc", or wants to turn a markdown product spec/BRD/feature doc into branded marketing HTML — even if they don't say "brochure" explicitly (e.g. "make this look like Metafore", "marketing version of this", "external-facing version", "give this the Metafore treatment"). Encodes Metafore's brand invariants — two-tone hero, teal-only accent palette, three-font type stack, legibility floors, voice rules, AI-tell blocklist, "Pulse" vocabulary — and explicitly leaves layout content-determined rather than template-fixed. Do NOT trigger for internal dashboards (use `metafore:dashboard`), DOCX documents, or PPTX decks.
---

# Metafore Brochure Builder

The deliverable is one self-contained `.html` brochure (fonts from Google Fonts, everything else embedded) that opens in a browser and prints cleanly to PDF.

**Read first:** `../../assets/brand/metafore_brand.md` — voice, AI tells, legibility floors, density, visual coverage, tokens, content preservation, and the build/check toolchain. This file adds only brochure-specific rules. Paths are relative to this skill's directory.

## Content determines structure

There is **no fixed section template**. Read the input end to end, then pick a section pattern for each theme by the shape of its content. Two brochures should not look interchangeable. What stays constant is the brand surface — type, color, voice, the two-tone hero, the footer.

**Bookends (non-negotiable):**
1. **Open with a two-tone hero** — big `h1`, weight 400, first word(s) in `--ink`, final word in `<span class="accent">` (`--logo-dark`).
2. **Close with the Metafore footer** — top hairline, 28px vertical padding; left `Powered by Metafore — AI-Native Transformation Platform` (Plex Mono uppercase), right `© <year> Metafore · <document name> · Confidential`.

| Content shape | Section pattern |
|---|---|
| Parallel items at equal weight | Grid (2×2, 3-up, 4-up cards), each card with a library icon |
| Sequential progression | Process timeline / numbered steps |
| Quantified outcomes worth headlining | KPI band on `--teal-dark` (2–4 cells) |
| Head-to-head against an alternative | Comparison table |
| One big commitment or thesis | Outcome band on `--teal`, white text |
| Customer or third-party voice | Quote pull |
| One primary thing + one supporting artifact | Hero with side UI card |
| Thematic pillars previewing the doc | Pillar cards (one per theme, same `--teal` bar) |
| Operational mechanics the reader skims | Callout strip (eyebrow + body cells) |

Don't pre-commit to a section count — a short story may need three sections, a dense overview six. One-pager (~1880px) vs multi-section (~3000–3600px) is a content-volume decision. Don't add a section just because a pattern exists. Snippets for these patterns: `references/pattern-library-DRAFT.md` (a working draft — inspiration, not a catalog).

**Every section carries a visual** (library icon, diagram, UI card, KPI band, or pull quote) and **no paragraph runs past three lines** — set three or more parallel facts as bullets.

## Build

Author `metafore-<topic>-<format>.src.html` with placeholders, then assemble and check:

```html
<head><meta charset="UTF-8"><title>…</title>
<!-- @fonts -->
<style>
/* @tokens:brochure */
/* brochure-specific section CSS */
</style></head>
<body><div class="page">
  <header class="topbar"><!-- @logo:logo-light width="155" height="36" --> …</header>
  <section class="section"> … <img src="@icon:Nodes" alt=""> … </section>
  …
</div></body>
```
```
python3 ../../scripts/build_html.py metafore-<topic>.src.html
python3 ../../scripts/check.py metafore-<topic>.html --kind brochure --sheet metafore-<topic>.sheet.png
python3 ../../scripts/render.py metafore-<topic>.html --pdf      # PDF (plus PNG + preview) when one is wanted
```
Fix every ERROR with targeted edits to the `.src.html`, rebuild, re-check, then Read the sheet once. Deliver the built `.html` (and PDF if asked). Save to the user's working directory unless told otherwise.

## Brochure tokens and type

`assets/tokens.css` (inlined by `@tokens:brochure`) carries the palette, type scale, base element styles, and the print rules. Don't retype it.

| Role | Size | Notes |
|---|---|---|
| H1 | 40px, shrinks to 32px floor | Max 2 lines; beyond that, revise the copy |
| H2 | 27px, shrinks to 24px floor | |
| H3 | 21px | |
| Lede | 21px | Never shrinks |
| Body | **18px** | Never shrinks |
| Captions, card meta, footnotes | 15px | The floor — nothing essential smaller |
| Eyebrow / labels | 13px Plex Mono, uppercase | |

- Headers shrink between default and floor via `clamp()` + container queries; margins scale with each element's size so nothing collides. Body, lede, caption and eyebrow sizes are fixed.
- **Letter-spacing is 0 everywhere in brochures** (a deliberate brochure exception to tracked eyebrows elsewhere).
- Weight 400 for headers; Inter 400–500 body; Plex Mono uppercase for labels.

## Page mechanics

- Page 1440px wide, centered. Section padding `88px 96px`; usable width ~1248px. Alternate sections `#FFFFFF` / `#F8FAFA`.
- Cards: 6px radius (14px only for inline UI-card mockups), `1px solid var(--line)`, no shadows; grid gap 18–20px; pills 999px.
- Logo: `@logo:logo-light` in the topbar of every brochure, native 155×36 ratio.
- Print/PDF: the `@page` + `print-color-adjust: exact` rules ship in `tokens.css` — keep them, or teal bands print grey.
- Brochure voice note: use **Metafore** as the brand name in customer copy; "Metafore One" only when the platform-product distinction matters.

## Don't trigger for

Internal dashboards or operator UIs (`metafore:dashboard`), Word deliverables (`metafore:doc`), decks (`metafore:deck`), or non-Metafore marketing. Don't recreate an existing brochure's structure unless asked.

## Checklist (brochure-specific; brand pack §7 also applies)

- [ ] Two-tone hero opens; Metafore footer closes
- [ ] `check.py --kind brochure` reports zero ERRORs
- [ ] Body 18px, nothing essential under 15px; no header over two lines
- [ ] Every section has a visual; no paragraph over three lines
- [ ] Sections chosen by content shape — not a copy of the last brochure
- [ ] PDF export keeps the teal bands (print rules intact)
