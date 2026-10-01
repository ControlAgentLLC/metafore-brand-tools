#!/usr/bin/env python3
"""render.py — final PNG / PDF export for Metafore graphics and brochures.

Usage:
    python3 render.py page.html --out page.png [--selector .frame] [--scale 2] [--pdf]

PNG: screenshot of --selector (default: the outermost element with an explicit
width/height, else the full page) at device_scale_factor=--scale (default 2).
Also writes page.preview.png (<=1600px longest edge) — Read only the preview.
--pdf: also writes page.pdf (printBackground; honours @page CSS, else one tall
page at document width).
Exit: 0 ok, 1 render error, 2 usage / missing dependency.
"""
import argparse
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check import FIND_FRAME_JS, FONTS_READY_JS, need  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Export Metafore HTML to PNG/PDF.")
    ap.add_argument("file")
    ap.add_argument("--out", help="PNG path (default: <name>.png)")
    ap.add_argument("--selector")
    ap.add_argument("--scale", type=float, default=2)
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    src = Path(a.file)
    if not src.exists():
        print(f"error: {src} not found")
        return 2
    need(["playwright", "PIL"])
    from playwright.sync_api import sync_playwright
    from PIL import Image

    out = Path(a.out) if a.out else src.with_suffix(".png")
    if out.suffix.lower() == ".pdf":      # `--out x.pdf` means "PDF please"; the PNG goes beside it
        a.pdf = True
        out = out.with_suffix(".png")
    preview = out.with_name(out.stem + ".preview.png")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=a.scale)
            page.goto(src.resolve().as_uri(), wait_until="domcontentloaded", timeout=30000)
            try:
                page.wait_for_load_state("load", timeout=8000)
            except Exception:
                pass
            fonts = page.evaluate(FONTS_READY_JS, 4000)
            note = "" if fonts["loaded"] else " (web fonts NOT loaded — offline?)"
            target = "full page"
            if a.selector:
                loc = page.locator(a.selector).first
                if loc.count() == 0:
                    print(f"error: selector {a.selector} matched nothing")
                    return 1
                target = a.selector
            else:
                fr = page.evaluate(FIND_FRAME_JS)
                if fr:
                    vw, vh = int(fr["x"] * 2 + fr["w"] + 0.999), int(fr["y"] * 2 + fr["h"] + 0.999)
                    page.set_viewport_size({"width": max(vw, 200), "height": max(vh, 200)})
                    page.evaluate(FONTS_READY_JS, 1500)
                    page.evaluate(FIND_FRAME_JS)
                    loc = page.locator("[data-mf-frame]").first
                    target = "frame"
                else:
                    loc = None
            png = loc.screenshot(animations="disabled") if loc else page.screenshot(full_page=True, animations="disabled")
            out.write_bytes(png)
            img = Image.open(io.BytesIO(png))
            W, H = img.size
            s = min(1.0, 1600 / max(W, H))
            pv = img.convert("RGB").resize((max(1, int(W * s)), max(1, int(H * s))), Image.LANCZOS) if s < 1 else img.convert("RGB")
            pv.save(preview, optimize=True)
            print(f"png {out} {W}x{H} ({target}, scale {a.scale:g}){note}")
            print(f"preview {preview} {pv.width}x{pv.height}  <- Read only the preview")
            if a.pdf:
                pdf = out.with_suffix(".pdf")
                dims = page.evaluate("""() => {
                  let hasPage = false;
                  for (const sh of document.styleSheets) { try { for (const r of sh.cssRules) if (r.type === CSSRule.PAGE_RULE && r.style.size) hasPage = true; } catch (e) {} }
                  return {w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight, hasPage};
                }""")
                page.emulate_media(media="print")
                if dims["hasPage"]:
                    # @page size given; if it is "auto" height, fall back to one tall page at doc height
                    page.pdf(path=str(pdf), print_background=True, prefer_css_page_size=True,
                             width=f"{dims['w']}px", height=f"{dims['h'] + 1}px")
                else:
                    page.pdf(path=str(pdf), print_background=True, width=f"{dims['w']}px", height=f"{dims['h'] + 1}px",
                             margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
                print(f"pdf {pdf} ({dims['w']}px wide, {pdf.stat().st_size // 1024} KB)")
        finally:
            browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
