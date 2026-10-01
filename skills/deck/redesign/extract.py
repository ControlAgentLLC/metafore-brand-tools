#!/usr/bin/env python3
"""extract.py — turn an existing deck into a text-first slide manifest + contact sheet.

Usage:
    python3 extract.py SOURCE.pptx [--out DIR] [--verbose]
    python3 extract.py SOURCE.pdf  [--out DIR] [--verbose]
    python3 extract.py OUTLINE.md  [--out DIR] [--verbose]

    --out DIR    output folder (default: <source dir>/manifest/)
    --verbose    also print a compact one-line-per-slide table

Outputs (in DIR):
    slide-manifest.json   one entry per source slide (always written)
    thumbnails/NN.png     per-slide render, NN = original_index (0-based), fits 1200x1200
    contact-sheet.png     6-per-row overview grid, <=1600px wide and tall
                          (decks too long for one sheet spill into contact-sheet-2.png, ...)

Dependencies (all optional except the one needed for the source type):
    PPTX text      python-pptx                      (required for .pptx)
    PDF text       pdfplumber, else PyMuPDF          (one required for .pdf)
    PDF render     PyMuPDF, else pdf2image+poppler   (+ Pillow)
    PPTX render    LibreOffice (soffice) -> PDF -> PDF render
Missing renderers only skip thumbnails/contact sheet. A missing text package exits 2.

stdout is deliberately short: one summary line plus a few warnings.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

THUMB_MAX = 1200          # thumbnails fit inside THUMB_MAX x THUMB_MAX
SHEET_MAX = 1600          # contact sheet never wider or taller than this
SHEET_COLS = 6

# --------------------------------------------------------------------------- #
# Text heuristics
# --------------------------------------------------------------------------- #

_MONTHS = (r"JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|SEPT|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|"
           r"APRIL|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER")
CHROME_PATTERNS = [
    re.compile(r"^METAFORE\s*[·•\.]\s*CONFIDENTIAL\s*$", re.I),
    re.compile(r"^(strictly\s+)?confidential(\s*(&|and)\s*proprietary)?\.?\s*$", re.I),
    re.compile(r"^(proprietary\s*(&|and)\s*confidential|internal use only|all rights reserved)\.?\s*$", re.I),
    # "Acme Corp · Confidential", "Acme | Confidential & Proprietary"
    re.compile(r"^.{0,40}\s[·•|\-–—]\s*(strictly\s+)?confidential\b.{0,30}$", re.I),
    re.compile(r"^©.*$"),
    re.compile(r"^\(c\)\s*\d{4}.*$", re.I),
    re.compile(r"^copyright\s+(©\s*)?\d{4}.*$", re.I),
    re.compile(r"^\d{1,3}$"),                                     # page numbers
    re.compile(r"^(page|slide)\s*\d{1,3}(\s*(of|/)\s*\d{1,3})?$", re.I),
    re.compile(r"^\d{1,3}\s*(of|/)\s*\d{1,3}$", re.I),
    re.compile(rf"^({_MONTHS})\.?\s+\d{{4}}$", re.I),
    re.compile(rf"^({_MONTHS})\.?\s+\d{{1,2}},?\s+\d{{4}}$", re.I),
]
SECTION_STAMP_RE = re.compile(r"^[A-Z][A-Z0-9 &\-:/]{2,40}$")
BULLET_RE = re.compile(r"^\s*(?:[•\-·\*▪◦‣–—►✓]|\d{1,2}[.)])\s+")


def is_chrome(text: str) -> bool:
    t = text.strip()
    return bool(t) and any(p.match(t) for p in CHROME_PATTERNS)


def is_section_stamp(text: str) -> bool:
    t = text.strip()
    return bool(SECTION_STAMP_RE.match(t)) and len(t.split()) <= 5


def strip_chrome_lines(text: str) -> str:
    return "\n".join(ln.strip() for ln in text.splitlines() if ln.strip() and not is_chrome(ln))


def strip_bullet(text: str) -> str:
    return BULLET_RE.sub("", text, count=1).strip()


def infer_role(idx, title, bullets, body, total, section_stamp, chars, n_images):
    t = (title or "").lower().strip()
    stamp = (section_stamp or "").lower().strip()
    n = len(bullets)
    if idx == 0:
        return "cover"
    if idx == total - 1:
        if any(k in t for k in ("thank", "q&a", "questions", "closing", "next steps")):
            return "closing"
        if chars < 40:
            return "closing"
    if "thank you" in t and chars < 60:
        return "closing"
    if any(k in t for k in ("agenda", "what we'll cover", "table of contents")) or stamp in ("agenda", "contents"):
        return "agenda"
    if any(k in t for k in ("about us", "the team", "who we are", "leadership", "our company")) or stamp == "company overview":
        return "company"
    if any(k in t for k in ("the problem", "challenge", "today", "the issue", "pain")):
        return "statement"
    if any(k in t for k in ("by the numbers", "results", "impact", "metrics", "outcomes")) or stamp == "kpi":
        return "kpi"
    if any(k in t for k in ("roadmap", "timeline", "schedule", "phases", "crawl, walk", "milestones")) or stamp == "governance":
        return "timeline"
    if any(k in t for k in ("partners", "customers", "integrations", "ecosystem", "case studies", "in action")) or stamp in ("case studies", "customers"):
        return "integrations"
    if 3 <= n <= 4 and len(body) < 400:
        return "capability-4"
    if 5 <= n <= 8:
        return "capability-8"
    if 9 <= n <= 14:
        return "module-grid"
    return "statement"


def needs_visual(text_chars, n_images, n_charts, n_diagrams=0):
    return (n_charts > 0 or n_diagrams > 0 or n_images >= 2
            or (n_images >= 1 and text_chars < 150) or text_chars < 40)


def table_chars(tables):
    return sum(len(c) for tb in tables for row in tb for c in row)


def make_entry(i, title, stamp, body, bullets, tables, n_images, n_charts, layout, total,
               notes="", n_diagrams=0, needs_visual_override=None, hidden=False):
    if not title and body:  # single prose box whose first line is the heading
        first, _, rest = body.strip().partition("\n")
        if rest.strip() and 4 <= len(first) <= 120 and not BULLET_RE.match(first):
            title, body = first.strip(), rest.strip()
    if title:  # some decks repeat the headline inside the body
        bullets = [b for b in bullets if b.strip() != title.strip()]
    chars = len(title) + len(body) + sum(len(b) for b in bullets) + table_chars(tables)
    entry = {
        "original_index": i,
        "title": title,
        "section_stamp": stamp,
        "body": body,
        "bullets": bullets,
        "tables": tables,
        "images": n_images,
        "charts": n_charts,
        "diagrams": n_diagrams,
        "layout_hint": layout,
        "role": infer_role(i, title, bullets, body, total, stamp, chars, n_images),
        "needs_visual": (needs_visual(chars, n_images, n_charts, n_diagrams)
                         if needs_visual_override is None else needs_visual_override),
        "notes": notes,
    }
    if hidden:
        entry["hidden"] = True
    return entry


# --------------------------------------------------------------------------- #
# PPTX
# --------------------------------------------------------------------------- #

_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
_DGM = "{http://schemas.openxmlformats.org/drawingml/2006/diagram}"
_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
# PP_PLACEHOLDER values
PH_TITLE, PH_BODY, PH_CENTER_TITLE, PH_SUBTITLE, PH_OBJECT = 1, 2, 3, 4, 7
PH_SLIDE_NUMBER, PH_FOOTER, PH_DATE = 13, 15, 16
CHROME_PH = {PH_SLIDE_NUMBER, PH_FOOTER, PH_DATE}
LIST_PH = {PH_BODY, PH_OBJECT}


def _ph_type(shape):
    try:
        if shape.is_placeholder:
            return int(shape.placeholder_format.type)
    except Exception:
        pass
    return None


def _ph_idx(shape):
    try:
        if shape.is_placeholder:
            return shape.placeholder_format.idx
    except Exception:
        pass
    return None


def iter_shapes(shapes):
    """Flatten group shapes, depth-first."""
    for sh in shapes:
        if getattr(sh, "shape_type", None) == 6:  # MSO_SHAPE_TYPE.GROUP
            yield from iter_shapes(sh.shapes)
        else:
            yield sh


def reading_order(shapes, slide_h):
    bucket = max(1, int(slide_h / 40)) if slide_h else 1

    def key(sh):
        top = sh.top if sh.top is not None else 0
        left = sh.left if sh.left is not None else 0
        return (top // bucket, left)
    return sorted(shapes, key=key)


def max_font_pt(shape) -> float:
    if not shape.has_text_frame:
        return 0.0
    best = 0.0
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            if run.font.size is not None:
                best = max(best, run.font.size.pt)
    return best


def frame_text(shape) -> str:
    return strip_chrome_lines(shape.text_frame.text)


def get_title(slide, shapes):
    """(title, shape). Title placeholder -> shape named 'Title' -> largest-font single frame."""
    for ph in shapes:
        if _ph_idx(ph) == 0 or _ph_type(ph) in (PH_TITLE, PH_CENTER_TITLE):
            if ph.has_text_frame:
                txt = frame_text(ph).replace("\n", " ").strip()
                if txt and not is_section_stamp(txt):
                    return txt, ph
    for sh in shapes:
        if sh.has_text_frame and "title" in (sh.name or "").lower() and _ph_type(sh) not in (PH_SUBTITLE,):
            txt = frame_text(sh).replace("\n", " ").strip()
            if txt and not is_section_stamp(txt):
                return txt, sh
    candidates = []
    for sh in shapes:
        if not sh.has_text_frame or _ph_type(sh) in LIST_PH | {PH_SUBTITLE}:
            continue
        txt = frame_text(sh)
        if not txt or is_section_stamp(txt) or "\n" in txt:
            continue
        if not (4 <= len(txt) <= 120):
            continue
        candidates.append((max_font_pt(sh), -(sh.top or 0), sh, txt))
    if candidates:
        candidates.sort(key=lambda c: (c[0], c[1]), reverse=True)
        return candidates[0][3], candidates[0][2]
    return "", None


def frame_items(shape):
    """Split a text frame into list items. Returns (items, is_list).

    Body/object placeholders and frames written with bullet glyphs are lists: one item
    per top-level paragraph, sub-level paragraphs folded into their parent as
    "parent\\n– child". Other frames (tile text boxes) are one item each.
    """
    paras = []
    for p in shape.text_frame.paragraphs:
        txt = "".join(r.text for r in p.runs).strip() or p.text.strip()
        if txt and not is_chrome(txt):
            paras.append((p.level or 0, txt))
    if not paras:
        return [], False
    glyphs = sum(1 for _, t in paras if BULLET_RE.match(t))
    is_list = (_ph_type(shape) in LIST_PH and len(paras) >= 2) or (len(paras) >= 2 and glyphs >= len(paras) - 1)
    if not is_list:
        return ["\n".join(t for _, t in paras)], False
    items = []
    base = min(lvl for lvl, _ in paras)
    for lvl, t in paras:
        t = strip_bullet(t)
        if lvl > base and items:
            items[-1] += "\n– " + t
        else:
            items.append(t)
    return items, True


def smartart_text(slide, shape):
    """Return node texts of a SmartArt graphic frame, or None if not SmartArt."""
    el = shape._element
    gd = el.find(f".//{_A}graphicData")
    if gd is None or "diagram" not in (gd.get("uri") or ""):
        return None
    rel = el.find(f".//{_DGM}relIds")
    texts = []
    if rel is not None:
        try:
            from lxml import etree
            part = slide.part.related_part(rel.get(f"{_R}dm"))
            root = etree.fromstring(part.blob)
            for pt in root.iter(f"{_DGM}pt"):
                if pt.get("type") not in (None, "node"):
                    continue
                t = "".join(x.text or "" for x in pt.iter(f"{_A}t")).strip()
                if t and not is_chrome(t):
                    texts.append(t)
        except Exception:
            pass
    return texts


def extract_pptx(src: Path):
    try:
        from pptx import Presentation
    except ImportError:
        die_pip("python-pptx")
    prs = Presentation(str(src))
    slide_h = prs.slide_height or 0
    total = len(prs.slides)
    out = []
    for i, slide in enumerate(prs.slides):
        shapes = [sh for sh in iter_shapes(slide.shapes) if _ph_type(sh) not in CHROME_PH]
        shapes = reading_order(shapes, slide_h)
        title, title_shape = get_title(slide, shapes)
        stamp, stamp_shape = "", None
        for sh in shapes:
            if sh is not title_shape and sh.has_text_frame:
                txt = frame_text(sh)
                if is_section_stamp(txt):
                    stamp, stamp_shape = txt, sh
                    break
        if not title and stamp:      # e.g. an all-caps "THANK YOU" slide
            title, title_shape, stamp = stamp, stamp_shape, ""
        collected, long_texts, tables = [], [], []   # collected: (text, from_list) in reading order
        n_images = n_charts = n_diagrams = 0
        stamp_used = False
        for sh in shapes:
            if sh is title_shape:
                continue
            if getattr(sh, "shape_type", None) == 13 or (_ph_type(sh) is not None and hasattr(sh, "image")):
                n_images += 1  # picture or filled picture placeholder
            if getattr(sh, "has_chart", False):
                n_charts += 1
                continue
            if getattr(sh, "has_table", False):
                rows = [[strip_chrome_lines(c.text).replace("\n", " ") for c in r.cells] for r in sh.table.rows]
                rows = [r for r in rows if any(c for c in r)]
                if rows:
                    tables.append(rows)
                continue
            sa = smartart_text(slide, sh) if sh.__class__.__name__ == "GraphicFrame" else None
            if sa is not None:
                n_diagrams += 1
                collected.extend((t, True) for t in sa)
                continue
            if not sh.has_text_frame:
                continue
            txt = frame_text(sh)
            if not txt or is_chrome(txt):
                continue
            if not stamp_used and stamp and txt == stamp:
                stamp_used = True
                continue
            its, is_list = frame_items(sh)
            for t in its:
                if is_list or len(t) <= 200:
                    collected.append((t, is_list))
                else:
                    long_texts.append(t)
        # >=3 short tiles, or any real list -> bullets; otherwise it is prose body.
        if len(collected) >= 3 or any(is_list for _, is_list in collected):
            bullets, body_parts = [t for t, _ in collected], long_texts
        else:
            bullets, body_parts = [], [t for t, _ in collected] + long_texts
        notes = ""
        try:
            if slide.has_notes_slide:
                notes = (slide.notes_slide.notes_text_frame.text or "").strip()
        except Exception:
            pass
        hidden = slide._element.get("show") in ("0", "false")
        out.append(make_entry(i, title, stamp, "\n\n".join(body_parts), bullets, tables,
                              n_images, n_charts, slide.slide_layout.name, total,
                              notes=notes, n_diagrams=n_diagrams, hidden=hidden))
    return out


# --------------------------------------------------------------------------- #
# PDF
# --------------------------------------------------------------------------- #

def _import_pymupdf():
    os.environ.setdefault("PYMUPDF_SUGGEST_LAYOUT_ANALYZER", "0")  # keep stdout quiet
    try:
        import pymupdf as fitz  # PyMuPDF >= 1.24
        return fitz
    except ImportError:
        pass
    try:
        import fitz  # older PyMuPDF
        if hasattr(fitz, "open"):
            return fitz
    except ImportError:
        pass
    return None


def _inside(bbox, boxes):
    x0, y0, x1, y1 = bbox
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return any(b[0] <= cx <= b[2] and b[1] <= cy <= b[3] for b in boxes)


def _pdf_pages_pdfplumber(src):
    import pdfplumber
    with pdfplumber.open(str(src)) as pdf:
        for page in pdf.pages:
            tables, boxes = [], []
            try:
                for tb in page.find_tables():
                    rows = [[(c or "").replace("\n", " ").strip() for c in r] for r in tb.extract()]
                    rows = [r for r in rows if any(r)]
                    if len(rows) >= 2:
                        tables.append(rows)
                        boxes.append(tb.bbox)
            except Exception:
                pass
            words = page.extract_words(extra_attrs=["size"], use_text_flow=True) or []
            lines = []
            for w in sorted(words, key=lambda w: (round(w["top"]), w["x0"])):
                if lines and abs(lines[-1]["top"] - w["top"]) <= 3:
                    ln = lines[-1]
                    ln["text"] += " " + w["text"]
                    ln["size"] = max(ln["size"], w["size"])
                    ln["bbox"] = (min(ln["bbox"][0], w["x0"]), ln["bbox"][1], max(ln["bbox"][2], w["x1"]), max(ln["bbox"][3], w["bottom"]))
                else:
                    lines.append({"text": w["text"], "size": w["size"], "top": w["top"],
                                  "bbox": (w["x0"], w["top"], w["x1"], w["bottom"])})
            lines = [ln for ln in lines if not _inside(ln["bbox"], boxes)]
            yield lines, tables, len(page.images or [])


def _pdf_pages_pymupdf(src, fitz):
    doc = fitz.open(str(src))
    try:
        for page in doc:
            tables, boxes = [], []
            try:
                for tb in page.find_tables().tables:
                    rows = [[(c or "").replace("\n", " ").strip() for c in r] for r in tb.extract()]
                    rows = [r for r in rows if any(r)]
                    if len(rows) >= 2:
                        tables.append(rows)
                        boxes.append(tuple(tb.bbox))
            except Exception:
                pass
            lines = []
            for block in page.get_text("dict").get("blocks", []):
                for line in block.get("lines", []):
                    spans = [s for s in line.get("spans", []) if s.get("text", "").strip()]
                    if not spans:
                        continue
                    text = " ".join(s["text"].strip() for s in spans)
                    lines.append({"text": text, "size": max(s["size"] for s in spans),
                                  "top": line["bbox"][1], "bbox": tuple(line["bbox"])})
            lines.sort(key=lambda ln: (round(ln["top"] / 3), ln["bbox"][0]))
            lines = [ln for ln in lines if not _inside(ln["bbox"], boxes)]
            try:
                n_img = len(page.get_images(full=True))
            except Exception:
                n_img = 0
            yield lines, tables, n_img
    finally:
        doc.close()


def extract_pdf(src: Path):
    try:
        import pdfplumber  # noqa: F401
        pages = _pdf_pages_pdfplumber(src)
    except ImportError:
        fitz = _import_pymupdf()
        if fitz is None:
            die_pip("pdfplumber", alt="pymupdf")
        pages = _pdf_pages_pymupdf(src, fitz)
    pages = list(pages)
    total = len(pages)
    out = []
    for i, (lines, tables, n_images) in enumerate(pages):
        lines = [ln for ln in lines if ln["text"].strip() and not is_chrome(ln["text"])]
        # glue lone bullet glyphs to the following line
        merged = []
        for ln in lines:
            if merged and re.fullmatch(r"[•\-·\*▪◦‣–►]", merged[-1]["text"].strip()):
                merged[-1] = dict(ln, text=merged[-1]["text"].strip() + " " + ln["text"])
            else:
                merged.append(ln)
        lines = merged
        # title: largest font among short, non-stamp lines (consecutive same-size lines joined)
        title, title_idx = "", set()
        cands = [(k, ln) for k, ln in enumerate(lines)
                 if not is_section_stamp(ln["text"]) and len(ln["text"]) < 120 and not BULLET_RE.match(ln["text"])]
        if cands:
            sizes = {round(ln["size"], 1) for _, ln in cands}
            if len(sizes) > 1:
                best = max(ln["size"] for _, ln in cands)
                k0 = next(k for k, ln in cands if abs(ln["size"] - best) < 0.6)
            else:
                k0 = cands[0][0]
            title_idx = {k0}
            parts = [lines[k0]["text"]]
            k = k0 + 1
            while (k < len(lines) and abs(lines[k]["size"] - lines[k0]["size"]) < 0.6 and len(parts) < 3
                   and not is_section_stamp(lines[k]["text"]) and len(" ".join(parts)) < 100
                   and len(sizes) > 1):
                parts.append(lines[k]["text"])
                title_idx.add(k)
                k += 1
            title = " ".join(parts).strip()
        stamp = next((ln["text"].strip() for k, ln in enumerate(lines)
                      if k not in title_idx and is_section_stamp(ln["text"])), "")
        if not title and stamp:
            title, stamp = stamp, ""
        rest = [ln["text"].strip() for k, ln in enumerate(lines) if k not in title_idx]
        if stamp in rest:
            rest.remove(stamp)
        if title in rest:
            rest.remove(title)
        bullets = [strip_bullet(ln) for ln in rest if BULLET_RE.match(ln)]
        body = "\n".join(ln for ln in rest if not BULLET_RE.match(ln))
        out.append(make_entry(i, title, stamp, body, bullets, tables, n_images, 0, "pdf-page", total))
    return out


# --------------------------------------------------------------------------- #
# Markdown
# --------------------------------------------------------------------------- #

def _md_split(text):
    """Return list of slide chunks. Supports 'Slide N:' markers, '---' separators, or headings."""
    parts = re.split(r"^\s*(?:#+\s*)?[Ss]lide\s*\d+\s*[:\.\-–—]?[ \t]*", text, flags=re.MULTILINE)
    if len(parts) > 1:
        return parts[1:]
    body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)  # YAML front matter
    chunks = re.split(r"^\s*---+\s*$", body, flags=re.MULTILINE)
    chunks = [c for c in chunks if c.strip()]
    if len(chunks) > 1:
        return chunks
    for level in (1, 2, 3):
        heads = re.findall(rf"^#{{{level}}}\s+\S", body, flags=re.MULTILINE)
        if len(heads) >= 2:
            pieces = re.split(rf"^(?=#{{{level}}}\s+\S)", body, flags=re.MULTILINE)
            return [p for p in pieces if p.strip()]
    return [body] if body.strip() else []


def extract_md(src: Path):
    chunks = _md_split(src.read_text(encoding="utf-8"))
    total = len(chunks)
    out = []
    for i, content in enumerate(chunks):
        raw = [ln.rstrip() for ln in content.splitlines() if ln.strip()]
        title, stamp, bullets, body, tables, n_images = "", "", [], [], [], 0
        table = []
        for ln in raw:
            s = ln.strip()
            if s.startswith("|"):
                if re.fullmatch(r"\|?[\s:\-|]+\|?", s):
                    continue  # separator row
                table.append([c.strip() for c in s.strip("|").split("|")])
                continue
            if table:
                tables.append(table)
                table = []
            n_images += len(re.findall(r"!\[[^\]]*\]\([^)]*\)", s))
            s_clean = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s).strip()
            if not s_clean or is_chrome(s_clean):
                continue
            if not title:
                title = re.sub(r"^#+\s*", "", s_clean)
                continue
            if re.match(r"^#+\s", s_clean):
                h = re.sub(r"^#+\s*", "", s_clean)
                if not stamp and is_section_stamp(h):
                    stamp = h
                else:
                    body.append(h)
                continue
            indent = len(ln) - len(ln.lstrip())
            if BULLET_RE.match(s_clean):
                if indent >= 2 and bullets:
                    bullets[-1] += "\n– " + strip_bullet(s_clean)
                else:
                    bullets.append(strip_bullet(s_clean))
            else:
                body.append(s_clean)
        if table:
            tables.append(table)
        out.append(make_entry(i, title, stamp, "\n".join(body), bullets, tables, n_images, 0,
                              "markdown", total, needs_visual_override=False))
    return out


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

def find_soffice():
    for name in ("soffice", "libreoffice"):
        p = shutil.which(name)
        if p:
            return p
    for p in ("/Applications/LibreOffice.app/Contents/MacOS/soffice",
              "/usr/lib/libreoffice/program/soffice", "/opt/libreoffice/program/soffice"):
        if os.path.exists(p):
            return p
    return None


def pptx_to_pdf(src: Path, tmpdir: str):
    soffice = find_soffice()
    if not soffice:
        return None, "LibreOffice not found (macOS: brew install --cask libreoffice; Linux: apt install libreoffice)"
    profile = Path(tmpdir, "lo-profile").as_uri()
    try:
        r = subprocess.run([soffice, f"-env:UserInstallation={profile}", "--headless",
                            "--convert-to", "pdf", "--outdir", tmpdir, str(src)],
                           capture_output=True, timeout=300)
    except subprocess.TimeoutExpired:
        return None, "LibreOffice timed out converting to PDF"
    pdfs = list(Path(tmpdir).glob("*.pdf"))
    if r.returncode != 0 or not pdfs:
        return None, "LibreOffice PDF conversion failed"
    return pdfs[0], None


def fit(img, max_w, max_h):
    from PIL import Image
    s = min(max_w / img.width, max_h / img.height, 1.0)
    if s < 1.0:
        img = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)
    return img


def render_pdf_pages(pdf_path: Path):
    """Yield PIL images, one per page, each fitting THUMB_MAX. Returns (iterator, error)."""
    try:
        from PIL import Image
    except ImportError:
        return None, "Pillow not installed (pip install pillow)"
    fitz = _import_pymupdf()
    if fitz is not None:
        def gen():
            doc = fitz.open(str(pdf_path))
            try:
                for page in doc:
                    w, h = page.rect.width, page.rect.height
                    zoom = min(THUMB_MAX / w, THUMB_MAX / h, 3.0)
                    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
                    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                    yield fit(img, THUMB_MAX, THUMB_MAX)
            finally:
                doc.close()
        return gen(), None
    try:
        from pdf2image import convert_from_path, pdfinfo_from_path
    except ImportError:
        return None, "no PDF renderer (pip install pymupdf)"

    def gen2():
        n = pdfinfo_from_path(str(pdf_path))["Pages"]
        for p in range(1, n + 1):
            img = convert_from_path(str(pdf_path), dpi=100, first_page=p, last_page=p,
                                    size=(THUMB_MAX, None))[0]
            yield fit(img.convert("RGB"), THUMB_MAX, THUMB_MAX)
    try:
        pdfinfo_from_path(str(pdf_path))
    except Exception:
        return None, "pdf2image needs poppler (brew install poppler) — or pip install pymupdf"
    return gen2(), None


def render_thumbnails(src: Path, thumb_dir: Path, slides):
    """Write thumbnails/NN.png keyed by original_index. Returns ([(index, path)], error)."""
    with tempfile.TemporaryDirectory() as td:
        pdf_path = src
        if src.suffix.lower() == ".pptx":
            pdf_path, err = pptx_to_pdf(src, td)
            if err:
                return [], err
        pages, err = render_pdf_pages(pdf_path)
        if err:
            return [], err
        thumb_dir.mkdir(parents=True, exist_ok=True)
        try:
            imgs = list(pages)
        except Exception as e:  # renderer blew up mid-way
            return [], f"render failed: {e}"
        indices = [s["original_index"] for s in slides]
        if len(imgs) != len(indices):
            visible = [s["original_index"] for s in slides if not s.get("hidden")]
            if len(imgs) == len(visible):
                indices = visible
            else:
                return [], f"rendered {len(imgs)} pages for {len(slides)} slides — cannot align thumbnails"
        width = max(2, len(str(max(indices) if indices else 0)))
        paths = []
        for idx, img in zip(indices, imgs):
            p = thumb_dir / f"{idx:0{width}d}.png"
            img.save(p, optimize=True)
            paths.append((idx, p))
        return paths, None


def build_contact_sheets(thumbs, out_dir: Path):
    """6-per-row grids, each <= SHEET_MAX x SHEET_MAX. Returns [(path, (w, h))]."""
    from PIL import Image, ImageDraw, ImageFont
    if not thumbs:
        return []
    cell_w = SHEET_MAX // SHEET_COLS
    first = Image.open(thumbs[0][1])
    cell_h = max(1, int(round(first.height * cell_w / first.width)))
    cell_h = min(cell_h, SHEET_MAX)
    rows_per_sheet = max(1, SHEET_MAX // cell_h)
    per_sheet = rows_per_sheet * SHEET_COLS
    try:
        font = ImageFont.load_default(size=16)
    except TypeError:
        font = ImageFont.load_default()
    width = max(2, len(str(max(i for i, _ in thumbs))))  # same zero-padding as thumbnail names
    results = []
    for s, start in enumerate(range(0, len(thumbs), per_sheet)):
        chunk = thumbs[start:start + per_sheet]
        rows = (len(chunk) + SHEET_COLS - 1) // SHEET_COLS
        sheet = Image.new("RGB", (cell_w * SHEET_COLS, rows * cell_h), "white")
        draw = ImageDraw.Draw(sheet)
        for k, (idx, p) in enumerate(chunk):
            img = fit(Image.open(p).convert("RGB"), cell_w - 2, cell_h - 2)
            x, y = (k % SHEET_COLS) * cell_w, (k // SHEET_COLS) * cell_h
            sheet.paste(img, (x + (cell_w - img.width) // 2, y + (cell_h - img.height) // 2))
            label = f"{idx:0{width}d}"
            tb = draw.textbbox((0, 0), label, font=font)
            draw.rectangle((x + 3, y + 3, x + 9 + tb[2] - tb[0], y + 7 + tb[3] - tb[1]), fill="black")
            draw.text((x + 6 - tb[0], y + 5 - tb[1]), label, fill="white", font=font)
        name = "contact-sheet.png" if s == 0 else f"contact-sheet-{s + 1}.png"
        path = out_dir / name
        sheet.save(path, optimize=True)
        results.append((path, sheet.size))
    return results


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def die_pip(pkg, alt=None):
    hint = f"pip install {pkg}" + (f"  (or: pip install {alt})" if alt else "")
    print(f"error: missing python package '{pkg}' — {hint}")
    sys.exit(2)


def _rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(p)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Extract a slide manifest + contact sheet from a deck.")
    ap.add_argument("source", help=".pptx, .pdf, or .md/.txt outline")
    ap.add_argument("--out", help="output dir (default: <source dir>/manifest/)")
    ap.add_argument("--verbose", "-v", action="store_true", help="print a per-slide table")
    args = ap.parse_args(argv)

    src = Path(args.source).expanduser()
    if not src.is_file():
        print(f"error: source not found: {src}")
        return 1
    ext = src.suffix.lower()
    if ext not in {".pptx", ".pdf", ".md", ".markdown", ".txt"}:
        print(f"error: unsupported extension '{ext}' (use .pptx, .pdf, or .md)")
        return 1
    out = Path(args.out).expanduser() if args.out else src.parent / "manifest"
    out.mkdir(parents=True, exist_ok=True)

    if ext == ".pptx":
        slides = extract_pptx(src)
    elif ext == ".pdf":
        slides = extract_pdf(src)
    else:
        slides = extract_md(src)

    # clear stale renders from a previous run
    thumb_dir = out / "thumbnails"
    if thumb_dir.is_dir():
        for f in thumb_dir.glob("*.png"):
            f.unlink()
    for f in out.glob("contact-sheet*.png"):
        f.unlink()

    warnings, sheets = [], []
    if ext in {".pptx", ".pdf"} and slides:
        thumbs, err = render_thumbnails(src, thumb_dir, slides)
        if err:
            warnings.append(f"thumbnails/contact sheet skipped: {err}")
        else:
            sheets = build_contact_sheets(thumbs, out)

    manifest = {"source": str(src), "n_slides": len(slides), "slides": slides}
    mpath = out / "slide-manifest.json"
    mpath.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    n_vis = sum(1 for s in slides if s["needs_visual"])
    line = f"extracted {len(slides)} slides → {_rel(mpath)} ({n_vis} need_visual)"
    if sheets:
        line += " · " + ", ".join(f"{p.name} {w}×{h}" for p, (w, h) in sheets)
    print(line)
    if not slides:
        warnings.append("no slides found — for markdown, use 'Slide N:' markers, '---' separators, or one heading per slide")
    sparse = sum(1 for s in slides if len(s["title"]) + len(s["body"]) + sum(map(len, s["bullets"])) + table_chars(s["tables"]) < 40)
    if slides and ext != ".md" and sparse / len(slides) > 0.4:
        warnings.append(f"image-heavy: {sparse}/{len(slides)} slides have <40 chars of text — extraction lost most content")
    no_title = [s["original_index"] for s in slides if not s["title"]]
    if no_title:
        warnings.append(f"no title detected on slides {', '.join(map(str, no_title[:12]))}{' …' if len(no_title) > 12 else ''}")
    for w in warnings[:4]:
        print("warning: " + w)

    if args.verbose:
        for s in slides:
            flag = "V" if s["needs_visual"] else " "
            extra = f" t{len(s['tables'])}" if s["tables"] else ""
            print(f"{s['original_index']:>3} {flag} {s['role']:<13} b{len(s['bullets']):<2}{extra} {s['title'][:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
