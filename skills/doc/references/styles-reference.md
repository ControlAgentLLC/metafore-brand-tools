# Metafore Doc — Styles Reference

> **Out of date — sizes.** This catalog predates the October 2026 legibility floors (body 11pt / 17pt leading, nothing readable under 11pt, Plex Mono labels 9pt, footer 8pt) and was already drifting from the code before that. **`assets/build_doc.py` is authoritative** for every size and spacing value; use this file for element names (A1–C9) and structure only.


Source of truth for every element in `metafore-doc-adnoc-test.docx` and the eventual `metafore-doc` skill. Mark this up with edits and we'll apply them.

---

## Page setup

| Property | Value |
|---|---|
| Size | US Letter (8.5 × 11) |
| Margins | **0.75"** all sides |
| Header distance from top edge | 0.35" |
| Footer distance from bottom edge | 0.35" |
| Content area | 7.0" wide × 9.5" tall |

---

## Colors

| Token | Hex | Used for |
|---|---|---|
| `ink` | `#111111` | Body, H1 base, H2 |
| `ink-2` | `#404040` | Layer lead, table layer column, takeaway body |
| `ink-3` | `#666666` | Header meta text, footer, fine annotation |
| `teal` | `#006B6F` | Section eyebrows |
| `teal-dark` | `#004D50` | Doc-type label, Layer eyebrows, callout label, data-table header text, signature labels |
| `teal-light` | `#E8F4F5` | Callout fill, data-table header fill |
| `logo-dark` | `#035657` | H1 accent run, closing line accent |
| `line` | `#ECECEC` | Header / footer hairlines, table row dividers |
| `line-strong` | `#D8D8D8` | Data-table header bottom border |

---

## Fonts

| Role | Stack (first → fallback) |
|---|---|
| Header | **Geist** → Arial |
| Body | **Inter** → Calibri |
| Mono | **IBM Plex Mono** → Consolas |

Tracking is given in twentieths of a point (Word's native unit). Convert to display units: `32 = +1.6pt`, `28 = +1.4pt`.

---

## Elements

### 1. Running header
2-col borderless table, vertical-center on both cells, full content width.

| Sub-element | Property | Value |
|---|---|---|
| Left cell (text) | Width | 6.0" |
| Right cell (icon) | Width | 1.0" |
| Doc-type run | Font / size | IBM Plex Mono / **7pt** |
| Doc-type run | Color | `teal-dark` |
| Doc-type run | Style | uppercase, tracked +32 |
| Meta run | Font / size | IBM Plex Mono / **7pt** |
| Meta run | Color | `ink-3` |
| Meta run | Style | uppercase, tracked +32 |
| Icon | Source | Metafore icon (two double-curves) |
| Icon | Size | **0.42" wide**, auto height (~0.35") |
| Icon | Alignment | Right-aligned in its cell |
| Hairline | Color / weight | `line` / 0.5pt |

### 2. Footer
Single paragraph with a right-tab at the content edge.

| Sub-element | Property | Value |
|---|---|---|
| Font / size | | IBM Plex Mono / **6.5pt** |
| Color | | `ink-3` |
| Style | | uppercase, tracked +28 |
| Left content | | `© 2026 Metafore · Confidential` |
| Right content | | `Page X of Y` (live PAGE / NUMPAGES fields) |
| Hairline above | Color / weight | `line` / 0.5pt |
| Tab stop | Position / type | 7.0" / right |

### 3. H1 — Title (page 1 only)
Two-tone hero: base ink + last word(s) in `logo-dark`.

| Property | Value |
|---|---|
| Font / size | Geist / **26pt** |
| Weight | 400 |
| Color (base run) | `ink` |
| Color (accent run) | `logo-dark` |
| Letter tracking | -0.5pt |
| Line spacing | 32pt (exact) |
| Space before | 14pt |
| Space after | 24pt |

### 4. Section eyebrow
Sits above every H2. Format: `NN · Section title` (e.g. `01 · Executive summary`).

| Property | Value |
|---|---|
| Font / size | IBM Plex Mono / **7.5pt** |
| Color | `teal` |
| Style | uppercase, tracked +28 |
| Space before | 24pt |
| Space after | 6pt |
| Line spacing | 10pt (exact) |

### 5. H2 — Section header

| Property | Value |
|---|---|
| Font / size | Geist / **15pt** |
| Weight | 500 (rendered as Word's regular for Geist — close to design intent) |
| Color | `ink` |
| Letter tracking | -0.1pt |
| Line spacing | 20pt (exact) |
| Space before | 0 |
| Space after | 10pt |

### 6. Layer eyebrow (sub-section)
Format: `Layer N · Topic` (e.g. `Layer 1 · Macro-economic drivers`).

| Property | Value |
|---|---|
| Font / size | IBM Plex Mono / **7.5pt** |
| Color | `teal-dark` |
| Style | uppercase, tracked +32 |
| Space before | 14pt |
| Space after | 2pt |
| Line spacing | 10pt (exact) |

### 7. Layer lead (one line under each Layer eyebrow)

| Property | Value |
|---|---|
| Font / size | Inter / **9pt** |
| Color | `ink-2` |
| Line spacing | 12pt (exact) |
| Space after | 4pt |

### 8. Body paragraph

| Property | Value |
|---|---|
| Font / size | Inter / **9.5pt** |
| Color | `ink` |
| Line spacing | 14pt (exact) |
| Space after | 10pt |

### 9. Body — takeaway (lighter sibling, e.g. after a table)

| Property | Value |
|---|---|
| Font / size | Inter / **9.5pt** |
| Color | `ink-2` |
| Line spacing | 14pt |
| Space after | 0 |

### 10. Bullet list item

| Property | Value |
|---|---|
| Font / size | Inter / **9.5pt** |
| Color | `ink` |
| Bullet glyph | `•` (10pt, ink), followed by tab |
| Left indent | 0.22" |
| First-line indent | -0.22" (hanging) |
| Space after each item | 4pt |
| Lead noun (when used) | Inter / 9.5pt / **bold** (e.g. "**Term** — description") |

### 11. Insight / Field Note callout
Single-cell table with shaded fill. Label is configurable (`Insight`, `Field Note`, `Note`, etc.) — the visual treatment is brand-locked.

| Sub-element | Property | Value |
|---|---|---|
| Cell fill | | `teal-light` |
| Cell margins | top/bottom | 9pt |
| Cell margins | left/right | 11pt |
| Label | Font / size | IBM Plex Mono / **7pt** |
| Label | Color | `teal-dark` |
| Label | Style | uppercase, tracked +32 |
| Label | Space after | 4pt |
| Body | Font / size | Inter / **9pt** |
| Body | Color | `ink` |
| Body | Line spacing | 13pt |
| Block | Space after | 12pt |

### 12. Data table

| Sub-element | Property | Value |
|---|---|---|
| Table width | | 7.0" (full content) |
| Layout | | fixed, autofit off |
| Header row fill | | `teal-light` |
| Header row text | Font / size | IBM Plex Mono / **6.5pt** |
| Header row text | Color | `teal-dark` |
| Header row text | Style | uppercase, tracked +32 |
| Header row bottom border | | 0.5pt `line-strong` |
| Header cell padding | top/bottom | 9pt |
| Header cell padding | left/right | 12pt |
| Body row bottom border | | 0.5pt `line` (except last row, no border) |
| Body cell padding | top/bottom | 7pt |
| Body cell padding | left/right | 12pt |
| Body row default text | Font / size | Inter / **8pt**, color `ink` |

### 13. Data table — column variants
Used in the 21-node topology table. Each column overrides the default body-row text style for its purpose:

| Column | Font / size | Color | Style |
|---|---|---|---|
| Node ID | IBM Plex Mono / 7.5pt | `teal-dark` | tracked +8 |
| Layer | IBM Plex Mono / 7pt | `ink-2` | uppercase, tracked +12 |
| Name | Inter / 8pt | `ink` | — |
| States | IBM Plex Mono / 7.5pt | `ink-2` | tracked +4 |
| Parents | IBM Plex Mono / 7.5pt | `ink-2` | tracked +4 |

### 14. Signature block (proposals)
Not present in this test doc but defined in the skill. 2-col borderless table with equal columns.

| Sub-element | Property | Value |
|---|---|---|
| Label | Font / size | IBM Plex Mono / **7pt** |
| Label | Color | `teal-dark` |
| Label | Style | uppercase, tracked +32 |
| Label | Space after | 24pt |
| Signature line | | 0.6pt bottom border in `ink` |
| Signature line | Space after | 6pt |
| Name / title | Font / size | IBM Plex Mono / **7pt** |
| Name / title | Color | `ink-2` |
| Name / title | Style | uppercase, tracked +28 |
| Date | Font / size | IBM Plex Mono / **6.5pt** |
| Date | Color | `ink-3` |
| Date | Space before | 14pt |

---

## How to use this doc

Mark up specific changes inline. Examples of clear requests:

- "H1 — bump to 30pt"
- "Body — go to 10pt, line spacing 15pt"
- "Section eyebrow color → `teal-dark` everywhere"
- "Layer eyebrow — also make it 8pt instead of 7.5pt"
- "Bullets — switch the glyph from `•` to `›` and make it teal"
- "Footer — add the doc name in a centered tab between the copyright and the page number"
- "Insight callout — drop the cell fill, use a 2pt left border in `teal-dark` instead"

When you've marked it up, hand me back the diff and I'll roll it into the generator script.
