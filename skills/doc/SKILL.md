---
name: doc
description: Build Metafore-branded Word documents (.docx) — white papers, technical specifications, proposals, statements of work, POVs, discovery briefs, executive memos. Use this skill whenever a Metafore teammate asks for a Word doc, .docx, white paper, technical spec, proposal, SOW, POV, brief, memo, or wants to "Metafore-ify this doc as Word", convert markdown / a brochure / a deck outline into a branded Word document, or produce a long-form leave-behind that the recipient will open in Word / Pages / Google Docs and edit with track changes. Generates editable .docx via `python-docx` with an optional two-tone cover page, optional auto-populated TOC, brand-aligned typography (Geist / Inter / IBM Plex Mono), the teal-only accent palette, Pulse vocabulary, and the Metafore AI-tell blocklist. Do NOT trigger for HTML brochures (use `metafore:brochure`), slide decks (use `metafore:deck`), internal dashboards (use `metafore:dashboard`), or standalone graphics (use `metafore:graphic`).
---

# Metafore Doc Builder

You are helping a Metafore teammate produce a brand-compliant Word document. The deliverable is a single `.docx` file generated via `python-docx` that opens cleanly in Word, Pages, and Google Docs, prints to PDF, and survives track changes.

## Brand reference (read before producing)

Every Metafore artifact follows the same brand invariants. Before drafting, Read the shared brand pack at `../../assets/brand/metafore_brand.md` (voice rules, AI-tell blocklist, design tokens, type stack) and skim any relevant `../../assets/brand/feedback_*.md` files. These supersede anything older you may have seen.

## The two invariants

1. **Open with either a cover page OR a section-01 eyebrow.** A cover (logo top-left, doc-type stack top-right, two-tone 46pt H1, subtitle, lead, bottom metadata strip) is the right open for white papers, formal proposals, and long technical specs. For shorter memos and briefs, skip the cover — the doc opens with `01 · <Section eyebrow>` directly at the top margin. There is no third option; every Metafore doc opens with one of these two.
2. **Close with the subtle footer on every page.** Light-gray Plex Mono `Metafore · <doc title> · 2026` on the left, a raw page number on the right, no hairline. Proposals and SOWs additionally close the body with a signature block before the footer.

Everything between those bookends is content-driven.

## Doc types

The same patterns build every supported doc type — the difference is **what you include**:

| Doc type | Cover | TOC | Signature | Doc-type label |
|---|---|---|---|---|
| White paper | yes | usually | no | `White Paper` |
| Technical specification | yes | yes (always) | no | `Technical Specification` |
| Proposal / SOW | yes | yes if >8 pages | **yes** | `Proposal` |
| POV / point of view | yes (short cover) | no | no | `Point of View` |
| Brief / memo | no | no | no | `Brief` |
| Executive memo | no | no | no | `Memo` |

## Optional pages

Two config flags on `create_doc()`:

- `include_cover` — adds the cover page (logo + big H1 + subtitle + lead + metadata strip)
- `include_toc` — adds a Table of Contents page with a Word TOC field that Word auto-populates from outline levels

Both default to True. Both can be turned off independently. The doc-type matrix above is the default mapping; deviate when the brief calls for it.

## Page setup (non-negotiable)

- US Letter (8.5 × 11)
- 0.75" margins all sides
- Header distance: 0.4"
- Footer distance: 0.4"
- Content area: 7.0" wide × 9.5" tall
- All paragraphs left-aligned, no centered body

## Design tokens

Single accent family — the teal stack only. Status colors only as state indicators (a danger badge, a success cell), never decoration.

| Token | Hex | Used for |
|---|---|---|
| `ink` | `#111111` | Body, H1 base, H2, subhead |
| `ink-2` | `#404040` | Takeaway body, table layer column |
| `ink-3` | `#666666` | Cover doc-type label, fine annotation |
| `ink-4` | `#999999` | Footer text — deliberately faint |
| `teal` | `#006B6F` | Section eyebrows, cover/TOC meta labels |
| `teal-dark` | `#004D50` | Cover date, callout left border, table header text, sig label |
| `teal-light` | `#E8F4F5` | Callout fill, data-table header fill |
| `logo-dark` | `#035657` | H1 accent run |
| `line` | `#ECECEC` | Section dividers, header/footer hairlines, table row dividers |
| `line-strong` | `#D8D8D8` | Data-table header bottom border |

## Typography — three families, three roles

| Role | Stack |
|---|---|
| Headers (H1 cover, H2 sections, subheads, TOC title) | **Geist** → Arial |
| Body (paragraphs, bullets, lead, callout, takeaway) | **Inter** → Calibri |
| Mono (eyebrows, footer, table headers, table IDs, signatures) | **IBM Plex Mono** → Consolas |

Cover H1 is 46pt, weight 400, two-tone (ink base + last word in `logo-dark`). H2 section titles are 26pt single-tone ink. Body is 10pt with 15pt line spacing. Eyebrows are tracked +28 to +32 (twentieths-of-pt). **Plex Mono is never bold and never italic.**

## The element catalog

The canonical visual reference is `references/styles-reference.html`. Open it in a browser to see every element rendered live alongside its spec table. Each element has an ID (A1, A2, B1, B2, C1–C9) — when the teammate marks up changes, they'll reference these.

**Optional pages**
- **A1 Cover page** — composite. Header, eyebrow, two-tone H1, subtitle, lead, footer metadata strip.
- **A2 TOC page** — title, hairline, TOC field. Auto-populates from outline levels 0 and 1.

**Persistent chrome**
- **B1 Inner-page header** — empty by design.
- **B2 Inner-page footer** — subtle one-line, no hairline.

**Body elements**
- **C1 Section eyebrow** — `NN · Section title`. Outline level 0.
- **C2 H2** — section's headline phrase. 26pt Geist, single-tone ink.
- **C3 Subhead** — numbered sub-heading `N · Topic`. Outline level 1.
- **C4 Body** — Inter 10pt, line 15pt. Inline bold for proper nouns.
- **C5 Takeaway** — body in `ink-2`. Used after tables/callouts as a finishing beat.
- **C6 Bullet** — solid `•`, hanging indent, tight spacing. Optional bold lead.
- **C7 Callout** — `teal-light` fill + 3pt `teal-dark` left border. **No label.**
- **C8 Data table** — teal-light header, hairline rows, 14pt trailing spacer.
- **C9 Signature block** — proposals only.

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

**Confidentiality.** Never name Kloudspot, mimik, or Airlinq as partners. Use generic vertical framing.

## AI-tell blocklist — zero tolerance

Marketing copy that follows these patterns reads as machine-written. Avoid them in every doc.

- **No "X isn't Y. It's Z." negation pivots.** Most-flagged pattern. Includes softer variants ("aren't waiting…", "The gap isn't X — it's Y"). Rewrite as a positive assertion.
- **No "X, not Y" inline contrasts.** Same family. State the thing directly.
- **No "[Subject] doesn't need X — it needs Y" pivots.** Same family.
- **No staccato fragment sentences.** Two-word sentences strung together are an AI tic. Join with commas, em dashes, or conjunctions.
- **No triplet structural lists used as a recurring device.** Three items are fine when there genuinely are three; don't default to triplets as rhetoric.
- **No department roll calls.** "Customer service runs X. Network ops has Y. Billing has Z."
- **No comfort words.** Compounding, fundamentally different, impactful, collectively unintelligent, leverage, synergy, disrupt, seamless (overuse), end-to-end, solutions (when vague).
- **No neat parallel opposition.** "Scaling costs without scaling returns."

Long-form docs amplify these tells because the reader has time to notice. Catch them on the editing pass.

## Doc-specific writing rules

- **Avoid "Executive Summary" as a section title.** Use `01 · Summary`, `01 · What matters`, or `01 · Point of View` — the eyebrow already does the structural-label job; "Executive Summary" reads as boilerplate.
- **Avoid a first-page table of contents on docs under 8 pages.** TOC on a 3-page memo is theatre.
- **Headlines in sentence case, not title case.**
- **Use inline bold (weight 500) for proper nouns and key terms** — `**Comshare Commander**`, `**TA'ZIZ**`, `**Enterprise General Intelligence**`. Not for emphasis-on-emphasis.

## What never appears

- Gradients on backgrounds, borders, or text
- Drop shadows on tables, callouts, or anywhere else
- Italic anywhere (especially in headers)
- Bold H1 (size carries weight, not weight)
- Centered text (left-align everything)
- A second accent color outside the teal stack
- "Dashboard" (always "Pulse")
- "Executive Summary" as a section title
- Bullet glyph `•` is **fine** in this skill (Word-default tell rule is suspended here — we ship docs that look like docs)
- Word's default Cambria/Calibri blue headings (we set Heading 1 / Heading 2 / TOC 1 / TOC 2 styles ourselves)
- The `•` symbol in headers, eyebrows, or footers (reserved for bullets)
- Track-change markup left in the deliverable (clean version only)

## Generator script — how to build a doc

The library lives at `assets/build_doc.py`. A working example that exercises every pattern is at `assets/example.py`. To build a new doc:

1. **Copy** `assets/example.py` to your working directory and rename it.
2. **Edit** the `create_doc(...)` call at the top — set `include_cover`, `include_toc`, `doc_type_label`, `publish_date`, `title_short`, and the 3-col metadata strip.
3. **Edit** the body content — calls to `add_section_eyebrow`, `add_h2`, `add_subhead`, `add_body`, `add_bullet`, `add_callout`, `add_data_table`, etc. Use `add_takeaway` for the lighter body line after a table or callout.
4. **Update** the `OUTPUT` path.
5. **Run** with `python3 your-script.py`. Open the `.docx` in Word — Word will ask to update fields the first time (say yes for the TOC).

The library imports python-docx. Install it once with `pip install python-docx`. No other dependencies are required at runtime; the icon and logo PNGs ship in this skill's `assets/` directory.

### Available helpers

```python
from build_doc import (
    create_doc, save_doc, page_break,
    # Cover
    add_cover_eyebrow, add_cover_h1, add_cover_subtitle, add_cover_lead,
    # TOC
    add_toc_page,
    # Body
    add_section_eyebrow, add_h2, add_subhead,
    add_body, add_takeaway, add_bullet,
    add_callout, add_data_table, add_signature_block,
)
```

Inline-bold pattern for body and bullets — pass a list of `(text, is_bold)` tuples instead of a plain string:

```python
add_body(doc, [
    ('The platform answers ', False),
    ('what is about to happen', True),
    (', why, and which lever moves it.', False),
])
```

## Workflow

### 1. Understand the request
Determine: doc type, audience, intended length, source content (markdown, brochure, deck outline, transcript), and whether cover/TOC are warranted.

### 2. Plan the structure
Before writing any code, outline the sections as a flat list:
```
01 · Executive summary
02 · The problem
03 · What we propose
04 · Scope and timeline
05 · Investment
06 · Next steps
```
This catches structural issues (too many sections, weak progression, missing transition) before they're baked into the doc.

### 3. Draft body content
Apply voice rules ruthlessly. Headlines in sentence case. Inline bold on proper nouns. Watch for the AI tells. Use **callouts** to lift the executive summary or key insight; use **takeaways** for finishing beats; use **subheads** for sub-section navigation.

### 4. Build the doc
Copy `example.py`, modify it, run it. Output a `.docx` next to your script.

### 5. Verify in Word
Open the file. Word prompts to update fields the first time — accept (this populates the TOC). Check:
- Cover renders correctly with logo top-left and doc-type stack top-right
- Icon and date are vertically aligned with the meta text
- H1 wraps cleanly with the accent run on a sensible word
- Section eyebrows + H2s read at the right hierarchy
- TOC entries appear with correct page numbers
- Callouts have the left border + teal-light fill, no label
- Data table column widths stick, header row has teal-light fill
- Footer shows on every page in faint gray, no hairline
- No widow/orphan headings (H2 stranded at bottom of a page is bad)

## Output

- Single `.docx` file.
- Filename pattern: `metafore-<topic>-<doc-type>.docx`. Examples: `metafore-adnoc-whitepaper.docx`, `metafore-pinewood-proposal.docx`, `metafore-q1-board-memo.docx`.
- Save to the user's current working directory unless they specify otherwise.

## Quality checklist

Before delivering, verify:

**Bookends**
- [ ] Doc opens with cover (if `include_cover`) or section 01 directly (if not)
- [ ] Subtle footer on every page; no hairline above it
- [ ] Page numbers are raw integers (`3`), not `Page 3 of 8`

**Brand-critical**
- [ ] Single accent family — teal stack only, no second hue
- [ ] No gradients, no drop shadows, no italic, no bold H1
- [ ] Cover H1 is two-tone (last word in `logo-dark`)
- [ ] H2 section titles are single-tone ink at 26pt
- [ ] Callouts have the 3pt `teal-dark` left border and no label

**Headers / hierarchy**
- [ ] Section eyebrows in format `NN · Title`, Plex Mono uppercase teal
- [ ] Sub-headings in format `N · Topic`, Geist 13pt bold
- [ ] Eyebrows carry outline level 0; subheads carry outline level 1 (so TOC populates)
- [ ] Top hairline above every section eyebrow except the first

**Body**
- [ ] Body is 10pt Inter, line spacing 15pt
- [ ] Inline bold on proper nouns and key terms
- [ ] Bullets are solid `•`, tight (2pt after, 14pt line)
- [ ] Takeaway after a table or callout is `ink-2` (lighter)

**Tables**
- [ ] Data tables have fixed layout, autofit off
- [ ] Header row has `teal-light` fill + 0.5pt `line-strong` bottom border
- [ ] Body rows have hairline `line` bottom borders, except last
- [ ] 14pt trailing spacer paragraph follows every data table

**Voice**
- [ ] "Pulse" used; "dashboard" does not appear (except as the antagonist concept being replaced)
- [ ] No Elana-flagged AI tells (no "isn't X. It's Y.", no staccato fragments, no roll-call structures, no comfort words)
- [ ] Headlines in sentence case, not title case
- [ ] No "Executive Summary" as a section title

**Fields**
- [ ] TOC field is present (if `include_toc`); Word offers to update on open
- [ ] PAGE field in footer renders correctly
- [ ] No `{TOC ...}` or `{PAGE}` literal text — fields must show their resolved values

## Anti-patterns to skip

- Don't trigger on HTML brochures, slide decks, dashboards, or graphics — each has its own skill.
- Don't recreate the structure of an existing doc unless explicitly asked. Same-shape docs are a failure mode.
- Don't add a TOC to a 3-page memo.
- Don't lift "Executive Summary" boilerplate; rewrite the section name.
- Don't use the bullet glyph for any decorative purpose — bullets only.
- Don't ship a doc with track changes still visible. Accept all, then deliver.
