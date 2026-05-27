# metafore-doc

A Claude Code skill that generates Metafore-branded Word documents (`.docx`) — white papers, technical specifications, proposals, SOWs, POVs, and memos.

## What's in here

```
metafore-doc/
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

## Install (for a teammate)

1. **Copy this whole folder** to `~/.claude/skills/metafore-doc/` on the recipient's machine.
2. **Install python-docx** once:
   ```
   pip install python-docx
   ```
3. **Restart Claude Code** if it was already open, so it picks up the new skill.

That's it. Next time the teammate asks Claude for a Word doc, white paper, proposal, SOW, etc., the skill auto-loads.

## Try it without Claude

```
cd ~/.claude/skills/metafore-doc/assets
python3 example.py
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
)
```

See `SKILL.md` for the full rule set and `references/styles-reference.html` for the visual catalog of every element.

## Updating the visual reference

If you change a style value in `build_doc.py`, also update the matching entry in `references/styles-reference.html` so the reference stays in sync. Element IDs (A1, A2, B1, B2, C1–C9) are stable — only the values inside the spec tables change.
