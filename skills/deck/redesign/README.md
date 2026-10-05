# Redesigning an existing deck — optional sub-workflow

Take an existing deck (PPTX, PDF, or markdown outline) and rebuild it in the Metafore style with the same patterns, tokens, and PPTX pipeline as a from-scratch deck. Removable — see `UNINSTALL.md`.

**Use when** the user supplies a deck and asks to "Metafore-ify", redesign, or convert it. If they're authoring from scratch (BRD, brochure, outline, talking points), skip this folder.

The governing rule (brand pack §3–4): **this is brand application, not editorial.** Keep every source slide and item; apply brand vocabulary automatically; *propose* every other wording change and wait for approval.

## Steps (before the main workflow's step 2)

```
0a. Extract   python3 extract.py path/to/source.pptx            → manifest/slide-manifest.json + contact-sheet.png
0b. Map       source-mapping.md: one pattern per manifest entry; content-preservation audit; pattern-variety tally
0c. Voice     voice-rewrite.md: vocabulary swaps applied; editorial edits listed for approval
0d. Hand off  the mapped manifest + approved wording is the source content for the main outline (SKILL.md step 2)
```

## 0a · Extract

```
python3 extract.py SOURCE.(pptx|pdf|md) [--out DIR] [-v]
```
Default output `<source dir>/manifest/`. One summary line on stdout (`extracted 18 slides → … (3 need_visual) · contact-sheet.png 1596×812`) plus any warnings; `-v` adds a one-line-per-slide table.

Dependencies: `pip install python-pptx pymupdf pillow` (pdfplumber is used for PDF text if installed). PPTX thumbnails come from LibreOffice if installed, otherwise (macOS) from Microsoft PowerPoint itself; with neither, the manifest is still written and the script says thumbnails were skipped. PowerPoint may ask once to *Grant access* to the source folder.

**Context-window discipline**
1. **The manifest is the source of truth.** Map and rewrite from `slide-manifest.json` — it has titles, body, bullets, tables, notes, and inferred roles. Don't Read slide images to do this work.
2. **Read `contact-sheet.png` once** (≤1596px wide, 6 per row) to sanity-check roles. Very long decks continue into `contact-sheet-2.png`.
3. **Zoom selectively.** Read `thumbnails/NN.png` (≤1200px) only for entries with `"needs_visual": true` — charts, diagrams, image-heavy slides. If the script warns that the deck is image-heavy, ask the user whether to caption diagrams with a vision pass first or redesign from the visible structure.

Numbering: contact-sheet labels, thumbnail file names, and `original_index` are all **0-based** (label "04" = `thumbnails/04.png`).

### Manifest fields

```json
{ "source": "…/source.pptx", "n_slides": 18,
  "slides": [ { "original_index": 0, "title": "Connected Operations for Carriers",
    "section_stamp": "CORPORATE OVERVIEW", "body": "", "bullets": [], "tables": [],
    "notes": "", "images": 1, "charts": 0, "diagrams": 0, "layout_hint": "Title Slide",
    "role": "cover", "needs_visual": false } ] }
```
- `title` — the real headline (not the section stamp). `section_stamp` — the small all-caps chrome label.
- `bullets` — one per top-level paragraph; sub-levels fold into their parent as `"Parent\n– child"`. SmartArt node text lands here too (`diagrams` counts SmartArt).
- `tables` — list of tables, each a list of rows of cell strings. `notes` — PPTX speaker notes. `hidden: true` only on hidden slides.
- `role` — `cover | agenda | company | statement | capability-4 | capability-8 | module-grid | kpi | timeline | integrations | closing`. Heuristic — expect to override 4–6 per deck.
- `needs_visual` — true for picture-led slides (one image and < 150 chars of text, or SmartArt).

Limitations: PDF hierarchies still flatten; chart contents aren't extracted (PDF `charts` is always 0); image-anchored slides extract sparse — trust `needs_visual`.

## Files

- `extract.py` — the extractor
- `source-mapping.md` — role → pattern playbook, content-preservation audit, pattern variety
- `voice-rewrite.md` — automatic vocabulary table + proposed-edits checklist
- `UNINSTALL.md` — removing this workflow
