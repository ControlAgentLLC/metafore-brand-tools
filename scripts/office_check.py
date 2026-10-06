#!/usr/bin/env python3
"""office_check.py — see a .pptx/.docx exactly as PowerPoint / Word render it (macOS).

Usage:
    python3 office_check.py deck.pptx [--sheet deck.office-sheet.png]
    python3 office_check.py doc.docx

Opens the file in Microsoft PowerPoint or Word, exports the app's own PDF render next to it
(<name>.office-export.pdf), and writes one contact sheet (≤1600px wide) of every page so a
single image shows the result. Read the sheet; don't open the PDF pages one by one.

A file you already had open is left open; a file this script opened is closed without saving.
If Office shows a "Grant access" prompt for a new folder, click Grant and run again.

Needs: macOS with Microsoft PowerPoint / Word, `pip install pymupdf pillow`.
Exit: 0 ok · 1 export failed · 2 usage / missing dependency.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

APPS = {".pptx": "Microsoft PowerPoint", ".ppt": "Microsoft PowerPoint",
        ".docx": "Microsoft Word", ".doc": "Microsoft Word"}


def osa(script, timeout=240):
    r = subprocess.run(["osascript", "-"], input=script, text=True, capture_output=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip())
    return r.stdout.strip()


def esc(p):
    return str(p).replace("\\", "\\\\").replace('"', '\\"')


def export(src: Path, pdf: Path) -> bool:
    """Export src to pdf with the owning Office app. Returns True if we opened (and closed) it."""
    app = APPS[src.suffix.lower()]
    word = app.endswith("Word")
    coll, item = ("documents", "document") if word else ("presentations", "presentation")
    was_open = osa(f'tell application "{app}" to return (exists {item} "{esc(src.name)}") as string', 60) == "true"
    if not was_open:
        # Launch Services open counts as a user open, which avoids most sandbox prompts
        subprocess.run(["open", "-a", app, str(src)], check=True)
        for _ in range(40):
            time.sleep(1)
            try:
                if osa(f'tell application "{app}" to return (exists {item} "{esc(src.name)}") as string', 30) == "true":
                    break
            except RuntimeError:
                pass
        else:
            raise RuntimeError(f"{app} did not open {src.name} — it may be waiting on a dialog "
                               "(folder access or repair). Answer it in the app, then run again.")
    if pdf.exists():
        pdf.unlink()
    if word:
        save = f'save as {item} "{esc(src.name)}" file name "{esc(pdf)}" file format format PDF'
    else:
        save = f'save {item} "{esc(src.name)}" in POSIX file "{esc(pdf)}" as save as PDF'
    osa(f'tell application "{app}"\n with timeout of 300 seconds\n  {save}\n end timeout\nend tell', 330)
    if not was_open:
        try:
            osa(f'tell application "{app}" to close {item} "{esc(src.name)}" saving no', 60)
        except RuntimeError:
            pass
    return not was_open


def sheet(pdf: Path, out: Path, deck: bool):
    import pymupdf
    from PIL import Image, ImageDraw
    doc = pymupdf.open(str(pdf))
    cols = 4 if deck else 3
    gap, lab = 8, 18
    tw = (1600 - gap * (cols + 1)) // cols
    thumbs = []
    for page in doc:
        r = page.rect
        zoom = tw / r.width
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
        thumbs.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    th = max(t.height for t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    per_sheet_rows = max(1, (2000 - gap) // (th + lab + gap))
    outs = []
    for si in range(0, rows, per_sheet_rows):
        chunk = thumbs[si * cols:(si + per_sheet_rows) * cols]
        nrows = (len(chunk) + cols - 1) // cols
        img = Image.new("RGB", (cols * (tw + gap) + gap, nrows * (th + lab + gap) + gap), (236, 236, 236))
        d = ImageDraw.Draw(img)
        for k, t in enumerate(chunk):
            x = gap + (k % cols) * (tw + gap)
            y = gap + (k // cols) * (th + lab + gap)
            d.text((x + 2, y + 2), f"{'slide' if deck else 'page'} {si * cols + k + 1:02d}", fill=(26, 26, 26))
            img.paste(t, (x, y + lab))
        path = out if si == 0 else out.with_name(f"{out.stem}-{si // per_sheet_rows + 1}{out.suffix}")
        img.save(path)
        outs.append((path, img.size))
    return len(doc), outs


def main():
    ap = argparse.ArgumentParser(description="Export a .pptx/.docx through PowerPoint/Word and make one contact sheet.")
    ap.add_argument("file")
    ap.add_argument("--sheet", help="contact sheet path (default: <name>.office-sheet.png)")
    a = ap.parse_args()
    src = Path(a.file).expanduser().resolve()
    if sys.platform != "darwin":
        print("error: office_check.py drives PowerPoint/Word via AppleScript and needs macOS")
        return 2
    if src.suffix.lower() not in APPS or not src.exists():
        print(f"error: need an existing .pptx or .docx (got {src})")
        return 2
    try:
        import pymupdf  # noqa: F401
        import PIL  # noqa: F401
    except ImportError:
        print("missing dependency: pip install pymupdf pillow")
        return 2
    pdf = src.with_name(src.stem + ".office-export.pdf")
    out = Path(a.sheet) if a.sheet else src.with_name(src.stem + ".office-sheet.png")
    try:
        opened = export(src, pdf)
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        msg = str(e)
        if "-1712" in msg or "timed out" in msg.lower() or isinstance(e, subprocess.TimeoutExpired):
            msg = ("the Office app stopped responding — it is probably showing a dialog (Grant access for a new "
                   "folder, or a repair prompt). Answer it, then run again.")
        print(f"error: {msg}")
        return 1
    if not pdf.exists():
        print("error: export produced no PDF (check the Office app for a dialog)")
        return 1
    n, outs = sheet(pdf, out, src.suffix.lower().startswith(".ppt"))
    app = APPS[src.suffix.lower()].split()[-1]
    print(f"{app} export {pdf.name}: {n} {'slides' if app == 'PowerPoint' else 'pages'}"
          f"{'' if opened else ' (file was already open; left open)'}")
    for p, (w, h) in outs:
        print(f"sheet {p} {w}x{h}  <- Read this once")
    return 0


if __name__ == "__main__":
    sys.exit(main())
