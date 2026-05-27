# Redesigning an existing deck — optional sub-workflow

This folder is an **optional, removable** extension to `metafore-deck`. It adds one capability: take an existing slide deck (PPTX, PDF, or markdown outline) and turn it into a Metafore-branded deck using the same pattern library, brand tokens, and PPTX pipeline as a from-scratch build.

If this folder is deleted and the fenced `REDESIGN MODE` block is removed from `../SKILL.md`, the skill behaves exactly as before. See `UNINSTALL.md`.

---

## When to use this workflow

The user supplies an existing deck and wants it redesigned. Triggers:

- "Metafore-ify this deck"
- "Redesign these slides in our style"
- "Here's the customer's deck — make it ours"
- "Convert this pitch to our brand"

If the user is authoring from scratch (a BRD, brochure, outline, or talking points), **skip this folder entirely** and go straight to Step 1 of the main workflow.

---

## Sub-workflow (runs before main Step 1)

```
0a. Extract     → run the extractor recipe below → produces slide-manifest.json + contact-sheet.png
0b. Map         → assign a pattern ID to each manifest entry using source-mapping.md
0c. Rewrite     → run extracted copy through voice-rewrite.md before any HTML drafting
0d. Hand off    → use the mapped + rewritten manifest as the source of truth for main Step 1 (outline)
```

After 0d, the main workflow proceeds normally: Step 1 (outline) → Step 2 (pattern assignment, already done in 0b) → Step 3 (draft HTML) → Step 4 (build PPTX) → Step 5 (save).

---

## Context-window discipline (read this before extracting)

A 40-slide source deck rendered at full resolution will exhaust the context window in one Read. The extractor is designed around three rules — follow them.

**Rule 1 — text-first manifest is the source of truth.**
All structural redesign decisions (pattern mapping, voice rewrite, outline) work from `slide-manifest.json`, not from screenshots. Never Read individual slide PNGs to do the redesign work — the manifest already has title, body, bullets, tables, layout name, and inferred role.

**Rule 2 — one contact sheet for overview, not 40 thumbnails.**
The extractor composes a single `contact-sheet.png` (6-per-row grid, ~1600px wide total → each thumbnail ~250px). Read that **once** to sanity-check role inferences across the whole deck. Do not Read individual thumbnails from `thumbnails/` as a default action.

**Rule 3 — selective full-res inspection only.**
A manifest entry can carry `"needs_visual": true`. Only those slides (typically <20% — charts, diagrams, dense infographics) warrant Reading the corresponding `thumbnails/NN.png` at full size. Even then, thumbnails are capped at 1200px wide to stay within the image budget.

If a deck is mostly custom diagrams and the manifest is sparse for many slides, stop and tell the user: "This deck is image-heavy — extraction lost most of the content. Want me to caption each diagram with a vision pass first, or are you OK redesigning from the visible structure?"

---

## Extractor recipe — ad-hoc Python

Following the skill convention (no bundled scripts), this is run ad-hoc each time. Paste into a file (e.g., `extract_source_deck.py` next to the source deck) and run, or run via `python -c` with a heredoc.

**Dependencies** (install once per machine):
```bash
pip install python-pptx pdfplumber pdf2image pillow
# For PPTX rendering, also need LibreOffice:
#   macOS: brew install --cask libreoffice
#   Linux: apt install libreoffice
# pdf2image needs poppler:
#   macOS: brew install poppler
#   Linux: apt install poppler-utils
```

**Usage:**
```bash
python extract_source_deck.py path/to/source.pptx --out manifest/
python extract_source_deck.py path/to/source.pdf  --out manifest/
python extract_source_deck.py path/to/outline.md  --out manifest/
```

**The script:**

```python
#!/usr/bin/env python3
"""extract_source_deck.py — convert an existing deck into a slide manifest + contact sheet.

Outputs (in --out, defaults to ./manifest/):
    slide-manifest.json   one entry per source slide (always)
    thumbnails/NN.png     downscaled per-slide renders (PPTX/PDF only)
    contact-sheet.png     6-per-row grid overview (PPTX/PDF only)
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys, tempfile
from pathlib import Path

THUMB_WIDTH = 1200
SHEET_WIDTH = 1600
SHEET_COLS  = 6

CHROME_PATTERNS = [
    re.compile(r"^METAFORE\s*[·•\.]\s*CONFIDENTIAL\s*$", re.I),
    re.compile(r"^CONFIDENTIAL\s*$", re.I),
    re.compile(r"^©.*$"),
    re.compile(r"^\d{1,2}$"),  # page numbers "01" .. "99"
    re.compile(r"^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|JANUARY|FEBRUARY|MARCH|APRIL|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s+\d{4}$", re.I),
]
SECTION_STAMP_RE = re.compile(r"^[A-Z][A-Z0-9 &\-:/]{2,40}$")


def is_chrome(text: str) -> bool:
    t = text.strip()
    return any(p.match(t) for p in CHROME_PATTERNS)


def is_section_stamp(text: str) -> bool:
    t = text.strip()
    if not SECTION_STAMP_RE.match(t):
        return False
    return len(t.split()) <= 5


def strip_chrome_lines(text: str) -> str:
    return "\n".join(ln for ln in text.splitlines() if not is_chrome(ln) and ln.strip())


def max_font_pt(shape) -> float:
    """Largest run font size on the shape (pt). 0 if none specified."""
    if not shape.has_text_frame:
        return 0.0
    best = 0.0
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            if run.font.size is not None:
                pt = run.font.size.pt
                if pt > best:
                    best = pt
    return best


def get_title(slide):
    """Return (title_text, title_shape_or_None). Tries placeholder → 'Title'-named shape → largest-font candidate."""
    # 1. Title placeholder (idx 0)
    try:
        for ph in slide.placeholders:
            if ph.placeholder_format.idx == 0:
                txt = ph.text_frame.text.strip()
                if txt and not is_chrome(txt) and not is_section_stamp(txt):
                    return txt, ph
    except Exception:
        pass
    # 2. Shape literally named "Title"
    for shape in slide.shapes:
        if shape.has_text_frame and "title" in shape.name.lower():
            txt = shape.text_frame.text.strip()
            if txt and not is_chrome(txt) and not is_section_stamp(txt):
                return txt, shape
    # 3. Largest-font short frame that isn't chrome/section-stamp
    candidates = []
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        txt = shape.text_frame.text.strip()
        if not txt or is_chrome(txt) or is_section_stamp(txt):
            continue
        if len(txt) > 120 or len(txt) < 10:
            continue
        size = max_font_pt(shape)
        candidates.append((size, -len(txt), shape, txt))
    if candidates:
        candidates.sort(key=lambda c: (c[0], c[1]), reverse=True)
        return candidates[0][3], candidates[0][2]
    return "", None


def get_section_stamp(slide) -> str:
    """Return the first ALL-CAPS short label found (e.g., 'ARCHITECTURE')."""
    for shape in slide.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text.strip()
            if is_section_stamp(txt) and not is_chrome(txt):
                return txt
    return ""


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


def needs_visual(text_chars, n_images, n_charts):
    return n_charts > 0 or n_images >= 2 or text_chars < 40


def extract_pptx(src):
    from pptx import Presentation
    prs = Presentation(src)
    total = len(prs.slides)
    out = []
    for i, slide in enumerate(prs.slides):
        title, title_shape = get_title(slide)
        section_stamp = get_section_stamp(slide)
        remaining = []
        n_images = n_charts = 0
        for shape in slide.shapes:
            if shape is title_shape:
                continue
            if getattr(shape, "shape_type", None) == 13:
                n_images += 1
            if getattr(shape, "has_chart", False):
                n_charts += 1
            if not shape.has_text_frame:
                continue
            raw = shape.text_frame.text.strip()
            if not raw or is_chrome(raw):
                continue
            if raw == section_stamp:
                continue
            cleaned = strip_chrome_lines(raw)
            if cleaned:
                remaining.append(cleaned)
        # Classify remaining text frames: tile-grid bullets vs body prose
        short_texts = [t for t in remaining if len(t) <= 200]
        long_texts  = [t for t in remaining if len(t) > 200]
        if len(short_texts) >= 3:
            bullets = short_texts
            body_parts = long_texts
        else:
            bullets = []
            body_parts = remaining
        # Dedupe: drop bullets that exactly match the title (some decks repeat the headline)
        if title:
            bullets = [b for b in bullets if b.strip() != title.strip()]
        body = "\n\n".join(body_parts)
        chars = len(title) + len(body) + sum(len(b) for b in bullets)
        out.append({
            "original_index": i,
            "title": title,
            "section_stamp": section_stamp,
            "body": body,
            "bullets": bullets,
            "images": n_images,
            "charts": n_charts,
            "layout_hint": slide.slide_layout.name,
            "role": infer_role(i, title, bullets, body, total, section_stamp, chars, n_images),
            "needs_visual": needs_visual(chars, n_images, n_charts),
        })
    return out


def extract_pdf(src):
    import pdfplumber
    out = []
    with pdfplumber.open(src) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            text = (page.extract_text() or "").strip()
            cleaned = strip_chrome_lines(text)
            lines = [ln.strip() for ln in cleaned.splitlines() if ln.strip()]
            title = ""
            if lines:
                for ln in lines:
                    if not is_section_stamp(ln) and len(ln) < 100:
                        title = ln
                        break
            section_stamp = next((ln for ln in lines if is_section_stamp(ln)), "")
            rest = [ln for ln in lines if ln != title and ln != section_stamp]
            bullets = [re.sub(r"^[•\-·\*]\s*", "", ln) for ln in rest if re.match(r"^[•\-·\*]\s", ln)]
            body = "\n".join(ln for ln in rest if not re.match(r"^[•\-·\*]\s", ln))
            n_images = len(page.images or [])
            chars = len(text)
            out.append({
                "original_index": i,
                "title": title,
                "section_stamp": section_stamp,
                "body": body,
                "bullets": bullets,
                "images": n_images,
                "charts": 0,
                "layout_hint": "pdf-page",
                "role": infer_role(i, title, bullets, body, total, section_stamp, chars, n_images),
                "needs_visual": needs_visual(chars, n_images, 0),
            })
    return out


def extract_md(src):
    text = src.read_text(encoding="utf-8")
    blocks = re.split(r"^\s*(?:#+\s*)?[Ss]lide\s*(\d+)\s*[:\.\-]?\s*", text, flags=re.MULTILINE)
    pairs = list(zip(blocks[1::2], blocks[2::2]))
    total = len(pairs)
    out = []
    for i, (_num, content) in enumerate(pairs):
        lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
        title = lines[0] if lines else ""
        bullets = [re.sub(r"^[•\-·\*]\s*", "", ln) for ln in lines[1:] if re.match(r"^[•\-·\*]\s", ln)]
        body = "\n".join(ln for ln in lines[1:] if not re.match(r"^[•\-·\*]\s", ln))
        chars = len(title) + len(body) + sum(len(b) for b in bullets)
        out.append({
            "original_index": i,
            "title": title,
            "section_stamp": "",
            "body": body,
            "bullets": bullets,
            "images": 0,
            "charts": 0,
            "layout_hint": "markdown",
            "role": infer_role(i, title, bullets, body, total, "", chars, 0),
            "needs_visual": False,
        })
    return out


def render_thumbnails(src, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        from pdf2image import convert_from_path
    except ImportError:
        print("pdf2image not installed — skipping thumbnails", file=sys.stderr)
        return []
    pdf_path = src
    if src.suffix.lower() in {".pptx", ".ppt"}:
        td = tempfile.mkdtemp()
        r = subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", td, str(src)],
            capture_output=True,
        )
        if r.returncode != 0:
            print("LibreOffice convert failed — skipping thumbnails", file=sys.stderr)
            return []
        pdf_path = next(Path(td).glob("*.pdf"))
    try:
        images = convert_from_path(str(pdf_path), dpi=80)
    except Exception as e:
        print(f"pdf2image failed: {e}", file=sys.stderr)
        return []
    paths = []
    for i, img in enumerate(images):
        if img.width > THUMB_WIDTH:
            ratio = THUMB_WIDTH / img.width
            img = img.resize((THUMB_WIDTH, int(img.height * ratio)))
        p = out_dir / f"{i:02d}.png"
        img.save(p, optimize=True)
        paths.append(p)
    return paths


def build_contact_sheet(thumb_paths, out):
    if not thumb_paths:
        return
    from PIL import Image, ImageDraw
    cell_w = SHEET_WIDTH // SHEET_COLS
    sample = Image.open(thumb_paths[0])
    cell_h = int(sample.height * (cell_w / sample.width))
    rows = (len(thumb_paths) + SHEET_COLS - 1) // SHEET_COLS
    sheet = Image.new("RGB", (SHEET_WIDTH, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for i, p in enumerate(thumb_paths):
        img = Image.open(p).resize((cell_w, cell_h))
        x, y = (i % SHEET_COLS) * cell_w, (i // SHEET_COLS) * cell_h
        sheet.paste(img, (x, y))
        draw.text((x + 6, y + 4), str(i + 1), fill="black")
    sheet.save(out, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", default="manifest")
    args = ap.parse_args()
    src = Path(args.source)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()
    if ext == ".pptx":
        slides = extract_pptx(src)
    elif ext == ".pdf":
        slides = extract_pdf(src)
    elif ext in {".md", ".txt"}:
        slides = extract_md(src)
    else:
        sys.exit(f"unsupported extension: {ext}")
    if ext in {".pptx", ".pdf"}:
        thumbs = render_thumbnails(src, out / "thumbnails")
        build_contact_sheet(thumbs, out / "contact-sheet.png")
    manifest = {"source": str(src), "n_slides": len(slides), "slides": slides}
    (out / "slide-manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"wrote {out}/slide-manifest.json  ({len(slides)} slides)")


if __name__ == "__main__":
    main()
```

---

## Manifest schema

`slide-manifest.json`:

```json
{
  "source": "path/to/source.pptx",
  "n_slides": 18,
  "slides": [
    {
      "original_index": 0,
      "title": "Connected Operations for Carriers",
      "section_stamp": "CORPORATE OVERVIEW",
      "body": "",
      "bullets": [],
      "images": 1,
      "charts": 0,
      "layout_hint": "Title Slide",
      "role": "cover",
      "needs_visual": false
    }
  ]
}
```

Field notes:
- `title` — the real slide headline (not the section stamp). Title detection tries the title placeholder first, then any shape literally named "Title", then the largest-font frame ≥10 chars.
- `section_stamp` — the small ALL-CAPS section label printed in the chrome (e.g., "ARCHITECTURE", "OFFERING"). Captured separately so it doesn't pollute the title.
- `role` — one of: `cover | agenda | company | statement | capability-4 | capability-8 | module-grid | kpi | timeline | integrations | closing`. Drives the pattern mapping. Heuristically inferred; **expect to override 4–6 entries per deck** during the mapping pass, especially "mega-grid" source slides that flatten into 20+ bullets and default to `statement`.
- `needs_visual` — only when this is true, consider Reading `thumbnails/NN.png`.
- `layout_hint` — the source's own layout name (for PPTX). Sometimes useful, often unreliable.

Known extractor limitations (worth knowing before you map):
- **3-tier hierarchies** (section → tile → sub-bullet) flatten into a single bullet list. A 4-product comparison with 5 sub-points each will produce 20+ bullets and default to `statement`. Override to module-grid / capability via `source-mapping.md`.
- **Image-anchored slides** (architecture diagrams, KPI bands with the metrics rendered as images) extract as sparse text. Trust `needs_visual: true` and inspect the thumbnail.
- **Repeated headlines** are deduped — if the same text appears as a title and a bullet, the bullet is dropped.

---

## After extraction — what to do next

1. Read `contact-sheet.png` once. Skim for inferred-role mismatches (e.g., the script labelled slide 5 `statement` but it's clearly a KPI band).
2. Open `source-mapping.md`. Walk the manifest top-to-bottom and write the outline (same format as main Step 2) with pattern IDs assigned.
3. Apply `voice-rewrite.md` to titles, bullets, and body across the whole manifest **before** drafting HTML. Don't carry source copy verbatim into Step 3.
4. Hand off to main `SKILL.md` Step 3 (Draft the HTML). The rewritten + mapped manifest is your authoritative source content.

---

## Files in this folder

- `README.md` — this file
- `source-mapping.md` — source role → Metafore pattern ID playbook
- `voice-rewrite.md` — voice transformation checklist applied to extracted copy
- `UNINSTALL.md` — how to remove the redesign workflow without affecting the rest of the skill
