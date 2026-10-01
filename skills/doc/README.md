# metafore-doc

A Claude Code skill that generates Metafore-branded Word documents (`.docx`) — white papers, technical specifications, proposals, SOWs, POVs, and memos.

## What's in here

```
skills/doc/
├── SKILL.md                          # Instructions Claude reads to use this skill
├── assets/
│   ├── build_doc.py                  # Reusable python-docx library
│   └── example.py                    # Working example (ADNOC white paper)
└── references/
    ├── styles-reference.html         # Visual catalog — open in a browser
    └── styles-reference.md           # Same catalog as markdown
```

Logos (used by `build_doc.py` for cover embedding) live at the plugin root in `assets/graphics/logos/` and are shared across all skills:
- `metafore-logo.png` — full wordmark, for cover header
- `metafore-icon.png` — icon-only mark
- `logo-light.svg` / `logo-dark.svg` / `icon-light.svg` / `icon-dark.svg` — SVG variants for HTML-rendered surfaces

## Install

This skill ships inside the Metafore brand-tools plugin (`metafore:doc`) — see the plugin README. It needs `pip install python-docx` once.

## Try it without Claude

```
cd <plugin>/skills/doc/assets
python3 example.py
python3 ../../../scripts/check.py metafore-doc-example.docx
```

That outputs `metafore-doc-example.docx` in the same directory — open it in Word to see every pattern the skill supports.

## Customize a doc

Copy `example.py` to your working directory, edit the `create_doc(...)` call and the `add_*(...)` calls below it, run with `python3 your-script.py`.

The available helpers are:

```python
from build_doc import (
    create_doc, save_doc, page_break,
    # Cover page (optional)
    add_cover_eyebrow, add_cover_h1, add_cover_subtitle, add_cover_lead,
    # Table of contents (optional, auto-populates from outline levels)
    add_toc_page,
    # Body
    add_section_eyebrow, add_h2, add_subhead,
    add_body, add_takeaway, add_bullet,
    add_callout, add_data_table, add_signature_block,
    # Visuals (every two facing pages carry one)
    add_icon, add_icon_row, add_figure, add_kpi_band, add_pull_quote,
)
```

See `SKILL.md` for the full rule set and `references/styles-reference.html` for the visual catalog of every element.

## Updating the visual reference

If you change a style value in `build_doc.py`, also update the matching entry in `references/styles-reference.html` so the reference stays in sync. Element IDs (A1, A2, B1, B2, C1–C9) are stable — only the values inside the spec tables change.
