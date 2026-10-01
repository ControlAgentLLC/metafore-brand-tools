"""Metafore Doc builder — library for generating Metafore-branded .docx files.

Import this from a thin per-doc script (see `example.py` in the same dir).
Every helper takes the `doc` as its first argument so the same library can
be used to build multiple docs in one session.

Conventions encoded here (must match `references/styles-reference.html`):
  - US Letter, 0.75" margins, 7.0" content width
  - Optional cover (logo top-left, doc-type stack top-right, 46pt H1, subtitle,
    lead, bottom metadata strip)
  - Optional auto-populated TOC (driven by outline levels 0 and 1)
  - No running header on content pages; subtle one-line footer
  - Section eyebrow (Plex Mono teal) → 26pt H2 → body
  - Solid-bullet lists with optional bold leads
  - Callouts as left-bordered teal-light blocks (no label)
  - Data tables with teal-light header rows and a trailing spacer
  - Two-tone H1 (ink base + logo-dark accent run)
  - Legibility floor (brand pack §2): body 11pt / 17pt leading (12pt for
    executive memos via create_doc(body_pt=12)); nothing readable under 11pt;
    Plex Mono labels 9pt
  - Visual helpers so every two facing pages carry a visual: add_icon,
    add_icon_row, add_figure, add_kpi_band, add_pull_quote

Fonts: Geist / Inter / IBM Plex Mono. Word falls back to Arial / Calibri /
Consolas if the brand fonts aren't installed.
"""

import datetime
import os

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ====================================================================
# CONSTANTS — colors, fonts, asset paths
# ====================================================================

INK = RGBColor(0x11, 0x11, 0x11)
INK_2 = RGBColor(0x40, 0x40, 0x40)
INK_3 = RGBColor(0x66, 0x66, 0x66)
INK_4 = RGBColor(0x99, 0x99, 0x99)
TEAL = RGBColor(0x00, 0x6B, 0x6F)
TEAL_DARK = RGBColor(0x00, 0x4D, 0x50)
LOGO_DARK = RGBColor(0x03, 0x56, 0x57)
TEAL_LIGHT_HEX = 'E8F4F5'
LINE_HEX = 'ECECEC'
LINE_STRONG_HEX = 'D8D8D8'
TEAL_DARK_HEX = '004D50'

HEADER_FONT = 'Geist';            HEADER_FALLBACK = 'Arial'
BODY_FONT = 'Inter';              BODY_FALLBACK = 'Calibri'
MONO_FONT = 'IBM Plex Mono';      MONO_FALLBACK = 'Consolas'

CONTENT_WIDTH_IN = 7.0

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
# Logos live in the shared plugin assets folder, three levels up from this script
# (skills/doc/assets/build_doc.py -> plugin root -> assets/graphics/logos/)
PLUGIN_ROOT = os.path.abspath(os.path.join(ASSETS_DIR, '..', '..', '..'))
LOGOS_DIR = os.path.join(PLUGIN_ROOT, 'assets', 'graphics', 'logos')
LOGO_PNG = os.path.join(LOGOS_DIR, 'metafore-logo.png')
ICON_PNG = os.path.join(LOGOS_DIR, 'metafore-icon.png')
LINE_ICONS_DIR = os.path.join(PLUGIN_ROOT, 'assets', 'graphics', 'line-icons')

LABEL_PT = 9          # Plex Mono labels / eyebrows (decorative-label exception)
FOOTER_PT = 8         # running footer chrome


def _body_pt(doc):
    return getattr(doc, '_mf_config', {}).get('body_pt', 11)


def _lead(pt):
    """Leading that keeps the 11/17 ratio (11 → 17, 12 → 18.5)."""
    return round(pt * 17 / 11 * 2) / 2


# ====================================================================
# LOW-LEVEL HELPERS (you usually don't call these directly)
# ====================================================================

def _set_font(run, family, fallback=None, size_pt=None, color=None, bold=False,
              italic=False, all_caps=False, tracking=None):
    run.font.name = family
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts'); rPr.insert(0, rFonts)
    rFonts.set(qn('w:ascii'), family); rFonts.set(qn('w:hAnsi'), family); rFonts.set(qn('w:cs'), family)
    if fallback:
        rFonts.set(qn('w:eastAsia'), fallback)
    if size_pt is not None:
        run.font.size = Pt(size_pt)
    if color is not None:
        run.font.color.rgb = color
    if bold:
        run.font.bold = True
    if italic:
        run.font.italic = True
    if all_caps:
        run.font.all_caps = True
    if tracking is not None:
        sp = OxmlElement('w:spacing'); sp.set(qn('w:val'), str(tracking)); rPr.append(sp)


def _set_paragraph_spacing(p, before_pt=None, after_pt=None, line_pt=None):
    pf = p.paragraph_format
    if before_pt is not None: pf.space_before = Pt(before_pt)
    if after_pt is not None: pf.space_after = Pt(after_pt)
    if line_pt is not None: pf.line_spacing = Pt(line_pt)


def _add_paragraph_border(p, side='bottom', sz=4, color='ECECEC', space=4):
    pPr = p._element.get_or_add_pPr()
    pBdr = pPr.find(qn('w:pBdr'))
    if pBdr is None: pBdr = OxmlElement('w:pBdr'); pPr.append(pBdr)
    b = OxmlElement(f'w:{side}')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), str(sz))
    b.set(qn('w:space'), str(space)); b.set(qn('w:color'), color)
    pBdr.append(b)


def _set_outline_level(p, level):
    pPr = p._element.get_or_add_pPr()
    for el in pPr.findall(qn('w:outlineLvl')): pPr.remove(el)
    lvl = OxmlElement('w:outlineLvl'); lvl.set(qn('w:val'), str(level))
    pPr.append(lvl)


def _set_cell_shading(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def _set_cell_borders(cell, sides_props):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None: tcBorders = OxmlElement('w:tcBorders'); tcPr.append(tcBorders)
    for side in ('top', 'left', 'bottom', 'right'):
        existing = tcBorders.find(qn(f'w:{side}'))
        if existing is not None: tcBorders.remove(existing)
        if side in sides_props:
            props = sides_props[side]
            b = OxmlElement(f'w:{side}')
            b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), str(props.get('sz', 4)))
            b.set(qn('w:space'), '0'); b.set(qn('w:color'), props.get('color', 'ECECEC'))
            tcBorders.append(b)
        else:
            b = OxmlElement(f'w:{side}'); b.set(qn('w:val'), 'nil'); tcBorders.append(b)


def _set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for side, v in (('top', top), ('bottom', bottom), ('left', left), ('right', right)):
        m = OxmlElement(f'w:{side}'); m.set(qn('w:w'), str(v)); m.set(qn('w:type'), 'dxa')
        tcMar.append(m)
    tcPr.append(tcMar)


def _set_cell_valign(cell, val='center'):
    tcPr = cell._tc.get_or_add_tcPr()
    for el in tcPr.findall(qn('w:vAlign')): tcPr.remove(el)
    va = OxmlElement('w:vAlign'); va.set(qn('w:val'), val); tcPr.append(va)


def _build_fixed_table(parent, rows, cols, col_widths_in):
    """Borderless fixed-layout table with explicit tblGrid + tcW so widths stick."""
    total_in = sum(col_widths_in)
    try:   # header/footer parts take a width; the document body doesn't
        tbl = parent.add_table(rows=rows, cols=cols, width=Inches(total_in))
    except TypeError:
        tbl = parent.add_table(rows=rows, cols=cols)
    tbl.autofit = False
    tblPr = tbl._element.find(qn('w:tblPr'))
    for el in tblPr.findall(qn('w:tblLayout')): tblPr.remove(el)
    tblLayout = OxmlElement('w:tblLayout'); tblLayout.set(qn('w:type'), 'fixed'); tblPr.append(tblLayout)
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is None: tblW = OxmlElement('w:tblW'); tblPr.append(tblW)
    tblW.set(qn('w:w'), str(int(total_in * 1440))); tblW.set(qn('w:type'), 'dxa')
    existing_grid = tbl._element.find(qn('w:tblGrid'))
    if existing_grid is not None: tbl._element.remove(existing_grid)
    grid = OxmlElement('w:tblGrid')
    for w_in in col_widths_in:
        gc = OxmlElement('w:gridCol'); gc.set(qn('w:w'), str(int(w_in * 1440))); grid.append(gc)
    tbl._element.insert(tbl._element.index(tblPr) + 1, grid)
    for r in tbl.rows:
        for ci, w_in in enumerate(col_widths_in):
            cell = r.cells[ci]
            tcPr = cell._tc.get_or_add_tcPr()
            for el in tcPr.findall(qn('w:tcW')): tcPr.remove(el)
            tcW = OxmlElement('w:tcW'); tcW.set(qn('w:w'), str(int(w_in * 1440))); tcW.set(qn('w:type'), 'dxa')
            tcPr.append(tcW)
            _set_cell_borders(cell, {}); _set_cell_margins(cell, top=0, bottom=0, left=0, right=0)
    return tbl


def _set_right_tab(p, position_inches):
    """Clear inherited Header/Footer-style tabs; install a single right tab."""
    pPr = p._element.get_or_add_pPr()
    existing = pPr.find(qn('w:tabs'))
    if existing is not None: pPr.remove(existing)
    tabs = OxmlElement('w:tabs')
    for pos in (4680, 9360):
        c = OxmlElement('w:tab'); c.set(qn('w:val'), 'clear'); c.set(qn('w:pos'), str(pos))
        tabs.append(c)
    mine = OxmlElement('w:tab'); mine.set(qn('w:val'), 'right')
    mine.set(qn('w:pos'), str(int(position_inches * 1440)))
    tabs.append(mine)
    pPr.append(tabs)


def _add_field(paragraph, field_code):
    r = paragraph.add_run()
    fc1 = OxmlElement('w:fldChar'); fc1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = ' ' + field_code + ' '
    fc2 = OxmlElement('w:fldChar'); fc2.set(qn('w:fldCharType'), 'end')
    r._r.append(fc1); r._r.append(it); r._r.append(fc2)
    return r


def _configure_toc_styles(doc):
    from docx.enum.style import WD_STYLE_TYPE
    styles = doc.styles
    for level in (1, 2):
        name = f'TOC {level}'
        try:
            s = styles[name]
        except KeyError:
            s = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
            s.base_style = styles['Normal']
        s.font.name = BODY_FONT
        s.font.size = Pt(12 if level == 1 else 11)
        s.font.color.rgb = INK if level == 1 else INK_2
        s.font.bold = False
        s.paragraph_format.left_indent = Inches(0 if level == 1 else 0.32)
        s.paragraph_format.space_before = Pt(10 if level == 1 else 4)
        s.paragraph_format.space_after = Pt(2)
        s.paragraph_format.line_spacing = Pt(18 if level == 1 else 16)


def _enable_field_update_on_open(doc):
    settings = doc.settings.element
    existing = settings.find(qn('w:updateFields'))
    if existing is not None:
        existing.set(qn('w:val'), 'true')
    else:
        up = OxmlElement('w:updateFields'); up.set(qn('w:val'), 'true'); settings.append(up)


# ====================================================================
# DOCUMENT CREATION
# ====================================================================

def create_doc(
    *,
    include_cover: bool = True,
    include_toc: bool = True,
    doc_type_label: str = 'White Paper',
    publish_date: str = 'May 2026',
    title_short: str = 'Metafore document',
    meta_labels=None,
    meta_values=None,
    body_pt: float = 11,
):
    """Create a Metafore-styled Document with cover/TOC chrome configured.

    The returned `doc` has its page setup, headers, and footers ready.
    Add body content with the `add_*` helpers below, then call `save_doc(doc, path)`.

    Args:
        include_cover: include a cover page (logo, big H1, subtitle, metadata strip)
        include_toc:   include an auto-populated Table of Contents page
        doc_type_label: top-right cover label ('White Paper', 'Technical Specification',
                        'Proposal', 'Point of View', 'Brief')
        publish_date:  top-right cover date ('May 2026')
        title_short:   short title used in subtle content-page footer
        meta_labels:   3 column labels for cover bottom strip
                       defaults to ['Prepared for', 'Version', 'Reading time']
        meta_values:   3 values for cover bottom strip
                       defaults to ['Client', 'v1.0', '— minutes']
        body_pt:       body size — 11 (default) or 12 for executive memos.
                       Never below 11 (brand floor for print).
    """
    if body_pt < 11:
        raise ValueError('body_pt below the 11pt print floor')
    meta_labels = meta_labels or ['Prepared for', 'Version', 'Reading time']
    meta_values = meta_values or ['Client', 'v1.0', '— minutes']

    doc = Document()
    section = doc.sections[0]
    section.page_height = Inches(11)
    section.page_width = Inches(8.5)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    section.header_distance = Inches(0.4)
    section.footer_distance = Inches(0.4)
    section.different_first_page_header_footer = include_cover

    if include_toc:
        _configure_toc_styles(doc)
        _enable_field_update_on_open(doc)

    # ---- COVER chrome (only when include_cover=True) ----
    if include_cover:
        _build_cover_header(section, doc_type_label, publish_date)
        _build_cover_footer(section, meta_labels, meta_values)

    # ---- DEFAULT footer (content + TOC pages) ----
    _build_content_footer(section, title_short)

    # ---- BODY: cover content if requested ----
    # (Cover body content is added via add_cover_* helpers in the caller's script.
    # We auto-insert the page break after the cover via add_page_break_if_cover().)

    # Store config on the doc so helpers can check it.
    doc._mf_config = {
        'include_cover': include_cover,
        'include_toc': include_toc,
        'body_pt': body_pt,
    }
    return doc


def save_doc(doc, output_path):
    """Save the document. Output path should end in .docx."""
    doc.save(output_path)
    return output_path


# ----- chrome builders --------------------------------------------------

def _build_cover_header(section, doc_type_label, publish_date):
    first_header = section.first_page_header
    default_first_p = first_header.paragraphs[0]._element

    htbl = _build_fixed_table(first_header, rows=1, cols=2, col_widths_in=[3.5, 3.5])
    for c in htbl.rows[0].cells:
        _set_cell_valign(c, 'top')

    # Left: full Metafore wordmark
    left_p = htbl.rows[0].cells[0].paragraphs[0]
    _set_paragraph_spacing(left_p, before_pt=0, after_pt=0)
    left_p.add_run().add_picture(LOGO_PNG, width=Inches(1.5))

    # Right: stacked doc-type / date
    right_cell = htbl.rows[0].cells[1]
    rp1 = right_cell.paragraphs[0]
    rp1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _set_paragraph_spacing(rp1, before_pt=0, after_pt=0, line_pt=12)
    r1 = rp1.add_run(doc_type_label)
    _set_font(r1, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=INK_3, all_caps=True, tracking=32)
    rp2 = right_cell.add_paragraph()
    rp2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _set_paragraph_spacing(rp2, before_pt=0, after_pt=0, line_pt=12)
    r2 = rp2.add_run(publish_date)
    _set_font(r2, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=TEAL_DARK, all_caps=True, tracking=32)

    default_first_p.getparent().remove(default_first_p)


def _build_cover_footer(section, meta_labels, meta_values):
    first_footer = section.first_page_footer
    ff_default = first_footer.paragraphs[0]
    _add_paragraph_border(ff_default, side='top', sz=4, color=LINE_HEX)
    _set_paragraph_spacing(ff_default, before_pt=0, after_pt=12, line_pt=2)

    mt = _build_fixed_table(first_footer, rows=2, cols=3, col_widths_in=[2.4, 2.4, 2.2])
    for ci, label in enumerate(meta_labels):
        cell = mt.rows[0].cells[ci]
        p = cell.paragraphs[0]
        _set_paragraph_spacing(p, before_pt=0, after_pt=6, line_pt=10)
        r = p.add_run(label)
        _set_font(r, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=TEAL, all_caps=True, tracking=28)
    for ci, val in enumerate(meta_values):
        cell = mt.rows[1].cells[ci]
        p = cell.paragraphs[0]
        _set_paragraph_spacing(p, before_pt=0, after_pt=0, line_pt=14)
        r = p.add_run(val)
        _set_font(r, BODY_FONT, BODY_FALLBACK, size_pt=11, color=INK)


def _build_content_footer(section, title_short):
    cf = section.footer.paragraphs[0]
    cf.text = ''
    _set_right_tab(cf, CONTENT_WIDTH_IN)
    _set_paragraph_spacing(cf, before_pt=24, after_pt=0, line_pt=11)
    fr1 = cf.add_run(f'Metafore · {title_short} · {datetime.date.today().year}')
    _set_font(fr1, MONO_FONT, MONO_FALLBACK, size_pt=FOOTER_PT, color=INK_4, tracking=20)
    cf.add_run().add_tab()
    page_run = _add_field(cf, 'PAGE')
    _set_font(page_run, MONO_FONT, MONO_FALLBACK, size_pt=FOOTER_PT, color=INK_4, tracking=20)


# ====================================================================
# BODY HELPERS — call these in order to compose the doc
# ====================================================================

def page_break(doc):
    """Insert a hard page break. Use to end the cover and to end the TOC."""
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


# ---- Cover-page body (only when include_cover=True) -------------------

def add_cover_eyebrow(doc, text):
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=180, after_pt=18, line_pt=13)
    r = p.add_run(text)
    _set_font(r, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=TEAL, all_caps=True, tracking=32)


def add_cover_h1(doc, text_before, accent_text):
    """Two-tone H1. First part in ink, accent_text in logo-dark."""
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=0, after_pt=18, line_pt=56)
    for txt, color in ((text_before, INK), (accent_text, LOGO_DARK)):
        r = p.add_run(txt)
        _set_font(r, HEADER_FONT, HEADER_FALLBACK, size_pt=46, color=color)
        b = OxmlElement('w:b'); b.set(qn('w:val'), 'false'); r._element.get_or_add_rPr().append(b)


def add_cover_subtitle(doc, text):
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=0, after_pt=32, line_pt=26)
    r = p.add_run(text)
    _set_font(r, HEADER_FONT, HEADER_FALLBACK, size_pt=18, color=INK, bold=True)


def add_cover_lead(doc, text):
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=0, after_pt=14, line_pt=19)
    r = p.add_run(text)
    _set_font(r, BODY_FONT, BODY_FALLBACK, size_pt=12, color=INK)


# ---- TOC page (only when include_toc=True) ----------------------------

def add_toc_page(doc, title='Contents', max_level=2):
    """Add a TOC page with a 'Contents' title, hairline, and the TOC field."""
    # title
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=0, after_pt=8, line_pt=34)
    r = p.add_run(title)
    _set_font(r, HEADER_FONT, HEADER_FALLBACK, size_pt=26, color=INK)
    b = OxmlElement('w:b'); b.set(qn('w:val'), 'false'); r._element.get_or_add_rPr().append(b)
    # hairline
    rp = doc.add_paragraph()
    _add_paragraph_border(rp, side='top', sz=4, color=LINE_HEX, space=1)
    _set_paragraph_spacing(rp, before_pt=2, after_pt=10, line_pt=2)
    # TOC field
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=12, after_pt=0, line_pt=18)
    r = p.add_run()
    fc1 = OxmlElement('w:fldChar'); fc1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve')
    it.text = f' TOC \\o "1-{max_level}" \\h \\z \\u '
    fc2 = OxmlElement('w:fldChar'); fc2.set(qn('w:fldCharType'), 'separate')
    placeholder = OxmlElement('w:r')
    pt = OxmlElement('w:t'); pt.text = "Right-click and choose 'Update Field' to populate."
    placeholder.append(pt)
    fc3 = OxmlElement('w:fldChar'); fc3.set(qn('w:fldCharType'), 'end')
    r._r.append(fc1); r._r.append(it); r._r.append(fc2); r._r.append(placeholder); r._r.append(fc3)


# ---- Body content ----------------------------------------------------

def add_section_eyebrow(doc, text, with_top_rule=True):
    """Section eyebrow. Outline level 0 → appears in TOC as level 1."""
    if with_top_rule:
        rp = doc.add_paragraph()
        _add_paragraph_border(rp, side='top', sz=4, color=LINE_HEX, space=1)
        _set_paragraph_spacing(rp, before_pt=24, after_pt=24, line_pt=2)
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=0, after_pt=10, line_pt=13)
    _set_outline_level(p, 0)
    r = p.add_run(text)
    _set_font(r, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=TEAL, all_caps=True, tracking=28)


def add_h2(doc, text):
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=0, after_pt=14, line_pt=34)
    r = p.add_run(text)
    _set_font(r, HEADER_FONT, HEADER_FALLBACK, size_pt=26, color=INK)
    b = OxmlElement('w:b'); b.set(qn('w:val'), 'false'); r._element.get_or_add_rPr().append(b)


def add_subhead(doc, number, text):
    """Numbered sub-heading 'N · Topic'. Outline level 1 → TOC level 2."""
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=14, after_pt=8, line_pt=19)
    _set_outline_level(p, 1)
    r = p.add_run(f'{number} · {text}')
    _set_font(r, HEADER_FONT, HEADER_FALLBACK, size_pt=14, color=INK, bold=True)


def add_body(doc, text_or_parts, after_pt=10, color=INK):
    """Body paragraph. Pass a string OR a list of (text, is_bold) tuples for inline bold.

    Keep each paragraph to ~3 lines (45–60 words); three or more parallel facts
    belong in add_bullet() calls instead.
    """
    pt = _body_pt(doc)
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=0, after_pt=after_pt, line_pt=_lead(pt))
    parts = [(text_or_parts, False)] if isinstance(text_or_parts, str) else text_or_parts
    for text, bold in parts:
        r = p.add_run(text)
        _set_font(r, BODY_FONT, BODY_FALLBACK, size_pt=pt, color=color, bold=bold)


def add_takeaway(doc, text):
    """Lighter body, used after tables/callouts as a finishing beat."""
    add_body(doc, text, after_pt=0, color=INK_2)


def add_bullet(doc, parts):
    """One bullet item. Pass list of (text, is_bold) tuples; first usually bolded as the lead noun."""
    pt = _body_pt(doc)
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=0, after_pt=3, line_pt=_lead(pt) - 1)
    p.paragraph_format.left_indent = Inches(0.24)
    p.paragraph_format.first_line_indent = Inches(-0.24)
    rb = p.add_run('•\t'); _set_font(rb, BODY_FONT, BODY_FALLBACK, size_pt=pt, color=INK)
    for text, bold in parts:
        r = p.add_run(text)
        _set_font(r, BODY_FONT, BODY_FALLBACK, size_pt=pt, color=INK, bold=bold)


def add_callout(doc, text):
    """Sticky-block callout: teal-light fill + 3pt teal-dark left border. No label."""
    tbl = doc.add_table(rows=1, cols=1); tbl.autofit = False
    cell = tbl.rows[0].cells[0]; cell.width = Inches(CONTENT_WIDTH_IN)
    _set_cell_shading(cell, TEAL_LIGHT_HEX)
    _set_cell_borders(cell, {'left': {'sz': 24, 'color': TEAL_DARK_HEX}})
    _set_cell_margins(cell, top=240, bottom=240, left=320, right=280)
    p = cell.paragraphs[0]
    pt = _body_pt(doc) + 1
    _set_paragraph_spacing(p, before_pt=0, after_pt=0, line_pt=_lead(pt))
    r = p.add_run(text)
    _set_font(r, BODY_FONT, BODY_FALLBACK, size_pt=pt, color=INK)
    spacer = doc.add_paragraph()
    _set_paragraph_spacing(spacer, before_pt=0, after_pt=18, line_pt=4)


def add_data_table(doc, headers, rows, col_widths_in):
    """A data table with teal-light header row and 14pt trailing spacer.

    headers: list of column header strings
    rows:    list of rows; each row is a list of (text, kind) tuples where
             kind is one of: 'id' | 'layer' | 'name' | 'states' | 'parents' | None
    col_widths_in: list of column widths in inches (should sum to 7.0)
    """
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers)); tbl.autofit = False
    for i, w in enumerate(col_widths_in):
        for cell in tbl.columns[i].cells:
            cell.width = Inches(w)
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        c = hdr_cells[i]
        _set_cell_shading(c, TEAL_LIGHT_HEX)
        _set_cell_borders(c, {'bottom': {'sz': 6, 'color': LINE_STRONG_HEX}})
        _set_cell_margins(c, top=110, bottom=110, left=140, right=140)
        p = c.paragraphs[0]
        _set_paragraph_spacing(p, before_pt=0, after_pt=0, line_pt=12)
        r = p.add_run(h)
        _set_font(r, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=TEAL_DARK, all_caps=True, tracking=32)
    for ri, row_data in enumerate(rows):
        is_last = (ri == len(rows) - 1)
        for ci, (text, kind) in enumerate(row_data):
            c = tbl.rows[ri + 1].cells[ci]
            _set_cell_borders(c, {} if is_last else {'bottom': {'sz': 3, 'color': LINE_HEX}})
            _set_cell_margins(c, top=100, bottom=100, left=140, right=140)
            p = c.paragraphs[0]
            _set_paragraph_spacing(p, before_pt=0, after_pt=0, line_pt=15)
            r = p.add_run(text)
            if kind == 'id':
                _set_font(r, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT + 1, color=TEAL_DARK, tracking=8)
            elif kind == 'layer':
                _set_font(r, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=INK_2, all_caps=True, tracking=12)
            elif kind in ('states', 'parents'):
                _set_font(r, MONO_FONT, MONO_FALLBACK, size_pt=10, color=INK_2, tracking=4)
            else:
                _set_font(r, BODY_FONT, BODY_FALLBACK, size_pt=11, color=INK)
    # trailing spacer
    spacer = doc.add_paragraph()
    _set_paragraph_spacing(spacer, before_pt=0, after_pt=14, line_pt=4)


def add_signature_block(doc, left_label, left_who, right_label, right_who):
    """Two-column signature block for proposals/SOWs.

    Each column: label (e.g. 'For Pinewood Bank'), 0.6pt sign line, name/title, date.
    """
    sig = _build_fixed_table(doc, rows=4, cols=2, col_widths_in=[3.3, 3.3])
    # row 0: labels
    for ci, label in enumerate((left_label, right_label)):
        p = sig.rows[0].cells[ci].paragraphs[0]
        _set_paragraph_spacing(p, before_pt=0, after_pt=24, line_pt=12)
        r = p.add_run(label)
        _set_font(r, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=TEAL_DARK,
                  all_caps=True, tracking=32)
    # row 1: signature lines
    for ci in range(2):
        cell = sig.rows[1].cells[ci]
        _set_cell_borders(cell, {'bottom': {'sz': 6, 'color': '111111'}})
        p = cell.paragraphs[0]
        _set_paragraph_spacing(p, before_pt=0, after_pt=6, line_pt=2)
    # row 2: name/title
    for ci, who in enumerate((left_who, right_who)):
        p = sig.rows[2].cells[ci].paragraphs[0]
        _set_paragraph_spacing(p, before_pt=0, after_pt=0, line_pt=11)
        r = p.add_run(who)
        _set_font(r, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=INK_2,
                  all_caps=True, tracking=28)
    # row 3: Date
    for ci in range(2):
        p = sig.rows[3].cells[ci].paragraphs[0]
        _set_paragraph_spacing(p, before_pt=14, after_pt=0, line_pt=11)
        r = p.add_run('Date')
        _set_font(r, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=INK_3,
                  all_caps=True, tracking=28)


# ---- Visual helpers ---------------------------------------------------
# Brand rule: every two facing pages carry at least one visual. Reach for the
# bundled LineIcons library first (names: see skills/graphic/references/
# line-icons-library.md), then KPI bands, pull quotes, and figures.

def _icon_path(name):
    path = os.path.join(LINE_ICONS_DIR, f'{name}.png')
    if not os.path.exists(path):
        import difflib
        names = sorted(f[:-4] for f in os.listdir(LINE_ICONS_DIR) if f.endswith('.png'))
        close = difflib.get_close_matches(name, names, n=3)
        raise FileNotFoundError(f"unknown line icon '{name}'" + (f" — closest: {', '.join(close)}" if close else ''))
    return path


def add_icon(doc, name, width_in=1.4):
    """A single library line icon, left-aligned, e.g. add_icon(doc, 'Nodes')."""
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=4, after_pt=10)
    p.add_run().add_picture(_icon_path(name), width=Inches(width_in))


def add_icon_row(doc, items, icon_width_in=1.1):
    """2–4 columns, each a library icon + title + one-line body.

    items: list of (icon_name, title, body) tuples.
    """
    n = len(items)
    col_w = CONTENT_WIDTH_IN / n
    tbl = _build_fixed_table(doc, rows=1, cols=n, col_widths_in=[col_w] * n)
    pt = _body_pt(doc)
    for ci, (icon, title, body) in enumerate(items):
        cell = tbl.rows[0].cells[ci]
        _set_cell_valign(cell, 'top')
        _set_cell_margins(cell, top=0, bottom=0, left=0 if ci == 0 else 120, right=120)
        p = cell.paragraphs[0]
        _set_paragraph_spacing(p, before_pt=0, after_pt=8)
        p.add_run().add_picture(_icon_path(icon), width=Inches(min(icon_width_in, col_w - 0.2)))
        tp = cell.add_paragraph()
        _set_paragraph_spacing(tp, before_pt=0, after_pt=4, line_pt=18)
        tr = tp.add_run(title)
        _set_font(tr, HEADER_FONT, HEADER_FALLBACK, size_pt=13, color=INK)
        bp = cell.add_paragraph()
        _set_paragraph_spacing(bp, before_pt=0, after_pt=0, line_pt=_lead(pt) - 1)
        br = bp.add_run(body)
        _set_font(br, BODY_FONT, BODY_FALLBACK, size_pt=pt, color=INK_2)
    spacer = doc.add_paragraph()
    _set_paragraph_spacing(spacer, before_pt=0, after_pt=16, line_pt=4)


def add_figure(doc, image_path, caption=None, width_in=CONTENT_WIDTH_IN):
    """A diagram, chart, or screenshot (PNG/JPG) with an optional caption."""
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=6, after_pt=6)
    p.add_run().add_picture(image_path, width=Inches(width_in))
    if caption:
        cp = doc.add_paragraph()
        _set_paragraph_spacing(cp, before_pt=0, after_pt=16, line_pt=15)
        cr = cp.add_run(caption)
        _set_font(cr, BODY_FONT, BODY_FALLBACK, size_pt=11, color=INK_3)


def add_kpi_band(doc, kpis, source=None):
    """A --teal-dark band of 2–4 metrics: kpis = [(value, label), ...]. Real numbers only."""
    n = len(kpis)
    tbl = _build_fixed_table(doc, rows=1, cols=n, col_widths_in=[CONTENT_WIDTH_IN / n] * n)
    for ci, (value, label) in enumerate(kpis):
        cell = tbl.rows[0].cells[ci]
        _set_cell_shading(cell, TEAL_DARK_HEX)
        _set_cell_margins(cell, top=260, bottom=260, left=240, right=200)
        _set_cell_valign(cell, 'top')
        vp = cell.paragraphs[0]
        _set_paragraph_spacing(vp, before_pt=0, after_pt=6, line_pt=34)
        vr = vp.add_run(value)
        _set_font(vr, HEADER_FONT, HEADER_FALLBACK, size_pt=28, color=RGBColor(0xFF, 0xFF, 0xFF))
        b = OxmlElement('w:b'); b.set(qn('w:val'), 'false'); vr._element.get_or_add_rPr().append(b)
        lp = cell.add_paragraph()
        _set_paragraph_spacing(lp, before_pt=0, after_pt=0, line_pt=15)
        lr = lp.add_run(label)
        _set_font(lr, BODY_FONT, BODY_FALLBACK, size_pt=11, color=RGBColor(0xCC, 0xDB, 0xDC))
    if source:
        sp = doc.add_paragraph()
        _set_paragraph_spacing(sp, before_pt=6, after_pt=16, line_pt=12)
        sr = sp.add_run(source)
        _set_font(sr, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=INK_3, tracking=12)
    else:
        spacer = doc.add_paragraph()
        _set_paragraph_spacing(spacer, before_pt=0, after_pt=16, line_pt=4)


def add_pull_quote(doc, quote, attribution):
    """A pull quote: Geist 18pt with a teal-dark left rule and a Plex Mono attribution."""
    tbl = doc.add_table(rows=1, cols=1); tbl.autofit = False
    cell = tbl.rows[0].cells[0]; cell.width = Inches(CONTENT_WIDTH_IN)
    _set_cell_borders(cell, {'left': {'sz': 32, 'color': TEAL_DARK_HEX}})
    _set_cell_margins(cell, top=120, bottom=120, left=360, right=200)
    qp = cell.paragraphs[0]
    _set_paragraph_spacing(qp, before_pt=0, after_pt=10, line_pt=25)
    qr = qp.add_run(quote)
    _set_font(qr, HEADER_FONT, HEADER_FALLBACK, size_pt=18, color=INK)
    b = OxmlElement('w:b'); b.set(qn('w:val'), 'false'); qr._element.get_or_add_rPr().append(b)
    ap = cell.add_paragraph()
    _set_paragraph_spacing(ap, before_pt=0, after_pt=0, line_pt=13)
    ar = ap.add_run(f'— {attribution}')
    _set_font(ar, MONO_FONT, MONO_FALLBACK, size_pt=LABEL_PT, color=TEAL, all_caps=True, tracking=28)
    spacer = doc.add_paragraph()
    _set_paragraph_spacing(spacer, before_pt=0, after_pt=18, line_pt=4)
