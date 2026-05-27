# Generation Pipeline — HTML → PPTX

Step-by-step recipe for converting the authored `deck.html` into an editable `deck.pptx`. Run via Bash with python-pptx + Playwright; no bundled scripts in the skill, the recipe is run ad-hoc each time.

## Prerequisites

- Python 3.10+
- `pip install python-pptx playwright`
- `python -m playwright install chromium` (once per machine)

If anything is missing, install before running. Don't substitute headless-chrome with Selenium or wkhtmltopdf — the bounding-box measurement step requires `getBoundingClientRect()` from a real Blink runtime.

## Output layout

```
Decks/<deck-name>/
  ├── deck.html           # source of truth, authored by hand
  ├── deck.pptx           # generated
  └── _build/             # intermediate artifacts, can be deleted
      ├── slide-01.png    # full-bleed background for image/hybrid slides
      ├── slide-01.json   # bbox + text content for hybrid editable nodes
      ├── slide-02.png
      └── ...
```

## Step 1 — Render slide backgrounds via Playwright

For every `<section class="slide">`, render a PNG at 2x. For **hybrid** slides, hide editable text nodes during render so their pixels are blank (text frames will sit on top in the PPTX).

```python
# render_slides.py — run ad-hoc, paste inline
import asyncio, json, base64
from pathlib import Path
from playwright.async_api import async_playwright

DECK_DIR = Path("Decks/<deck-name>")
HTML = DECK_DIR / "deck.html"
BUILD = DECK_DIR / "_build"
BUILD.mkdir(exist_ok=True)

# Hide editable text on hybrid slides for background render.
HIDE_CSS = """
section.slide[data-pptx="hybrid"] [data-pptx-text] { visibility: hidden !important; }
section.slide[data-pptx="hybrid"] [data-pptx-image] { visibility: hidden !important; }
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,
        )
        page = await ctx.new_page()
        await page.goto(HTML.absolute().as_uri())
        await page.add_style_tag(content=HIDE_CSS)

        # Wait for fonts
        await page.evaluate("document.fonts.ready")

        slides = await page.query_selector_all("section.slide")
        for i, slide in enumerate(slides, start=1):
            await slide.scroll_into_view_if_needed()
            png = await slide.screenshot(omit_background=False)
            (BUILD / f"slide-{i:02d}.png").write_bytes(png)
            print(f"rendered slide-{i:02d}.png")

        await browser.close()

asyncio.run(main())
```

**Important**: scroll each slide into view before screenshotting. Playwright's `Locator.screenshot()` handles this, but if you grab via `page.screenshot(clip=...)` you must compute the slide's offset manually.

## Step 2 — Measure bounding boxes for editable nodes

A second Playwright pass without `HIDE_CSS` reads the on-screen rect of every `data-pptx-text` and `data-pptx-image` node. Write to JSON keyed by slide id.

```python
# measure_boxes.py — run in the same Playwright session or a second one.
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright

DECK_DIR = Path("Decks/<deck-name>")
HTML = DECK_DIR / "deck.html"
BUILD = DECK_DIR / "_build"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1,                    # rect math at 1x
        )
        page = await ctx.new_page()
        await page.goto(HTML.absolute().as_uri())
        await page.evaluate("document.fonts.ready")

        slides = await page.query_selector_all("section.slide")
        for i, slide in enumerate(slides, start=1):
            slide_id = await slide.get_attribute("data-slide-id") or f"slide-{i:02d}"
            tier = await slide.get_attribute("data-pptx") or "semantic"
            slide_box = await slide.bounding_box()

            nodes = await slide.query_selector_all("[data-pptx-text], [data-pptx-image]")
            entries = []
            for n in nodes:
                role = await n.get_attribute("data-pptx-text") or await n.get_attribute("data-pptx-image")
                box = await n.bounding_box()
                # Coordinates relative to slide origin
                rel = {
                    "x": box["x"] - slide_box["x"],
                    "y": box["y"] - slide_box["y"],
                    "w": box["width"],
                    "h": box["height"],
                }
                content = await n.inner_html() if (await n.get_attribute("data-pptx-text")) else None
                style = await page.evaluate("(el) => { const s = getComputedStyle(el); return {fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, letterSpacing: s.letterSpacing, color: s.color, textTransform: s.textTransform, lineHeight: s.lineHeight}; }", n)
                entries.append({"role": role, "rect": rel, "html": content, "style": style})

            (BUILD / f"{slide_id}.json").write_text(json.dumps({
                "tier": tier,
                "index": i,
                "entries": entries,
            }, indent=2))
            print(f"measured {slide_id} — {len(entries)} nodes")

        await browser.close()

asyncio.run(main())
```

The two passes can be combined into one Playwright session with two style-tag toggles — the split is just for clarity.

## Step 3 — Build the .pptx

```python
# build_pptx.py — run after rendering + measuring
import json, re
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

DECK_DIR = Path("Decks/<deck-name>")
BUILD = DECK_DIR / "_build"

PX_TO_EMU = 9525

# 13.333" × 7.5" widescreen
prs = Presentation()
prs.slide_width = Emu(12192000)
prs.slide_height = Emu(6858000)
BLANK = prs.slide_layouts[6]                          # truly blank layout

# Two-tone hero color map by HTML class
ACCENT_COLORS = {
    "accent": RGBColor(0x03, 0x56, 0x57),             # --logo-dark
    "bracket": RGBColor(0x03, 0x56, 0x57),
    "accent-light": RGBColor(0x00, 0xC4, 0xCC),       # --teal-bright
}
DEFAULT_INK = RGBColor(0x1A, 0x1A, 0x1A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

def parse_color(css_color: str) -> RGBColor:
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", css_color)
    if not m: return DEFAULT_INK
    return RGBColor(int(m[1]), int(m[2]), int(m[3]))

def parse_px(s: str) -> float:
    return float(s.replace("px", ""))

def add_text_frame(slide, entry, on_dark=False):
    rect = entry["rect"]
    style = entry["style"]
    html = entry["html"] or ""

    left = Emu(int(rect["x"] * PX_TO_EMU))
    top  = Emu(int(rect["y"] * PX_TO_EMU))
    w    = Emu(int(rect["w"] * PX_TO_EMU))
    h    = Emu(int(rect["h"] * PX_TO_EMU))

    box = slide.shapes.add_textbox(left, top, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0

    # Run-split: parse <span class="accent|bracket|accent-light"> nodes
    runs = re.split(r'(<span[^>]*class="(?:accent|bracket|accent-light)"[^>]*>.*?</span>)', html, flags=re.S)
    p = tf.paragraphs[0]
    # Default font from computed style
    font_family = style["fontFamily"].split(",")[0].strip().strip('"\'')
    font_size = parse_px(style["fontSize"])
    base_color = WHITE if on_dark else parse_color(style["color"])

    for chunk in runs:
        if not chunk: continue
        m = re.match(r'<span[^>]*class="(accent|bracket|accent-light)"[^>]*>(.*?)</span>', chunk, flags=re.S)
        if m:
            cls, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
            r = p.add_run(); r.text = txt
            r.font.name = font_family
            r.font.size = Pt(font_size * 0.75)         # px → pt
            r.font.color.rgb = ACCENT_COLORS[cls]
        else:
            txt = re.sub(r"<[^>]+>", "", chunk)
            if not txt.strip(): continue
            r = p.add_run(); r.text = txt
            r.font.name = font_family
            r.font.size = Pt(font_size * 0.75)
            r.font.color.rgb = base_color

    # PPTX brand rules — apply post-write
    is_mono = "Plex Mono" in font_family
    is_small = font_size < 22
    for run in p.runs:
        if is_mono:
            run.font.bold = False
            # Character spacing: strip on Plex Mono
            run.font._rPr.set("spc", "0")
        elif is_small:
            run.font._rPr.set("spc", "0")
        else:
            ls = style.get("letterSpacing", "0px")
            if ls and ls != "normal":
                px = parse_px(ls)
                # PPT spc unit: hundredths of a point
                run.font._rPr.set("spc", str(int(px * 100)))

def add_picture_fullbleed(slide, png_path):
    slide.shapes.add_picture(str(png_path), 0, 0,
                              width=prs.slide_width,
                              height=prs.slide_height)

# Iterate slides in order
json_files = sorted(BUILD.glob("*.json"), key=lambda p: json.loads(p.read_text())["index"])

for jf in json_files:
    data = json.loads(jf.read_text())
    tier = data["tier"]
    idx = data["index"]
    png = BUILD / f"slide-{idx:02d}.png"

    slide = prs.slides.add_slide(BLANK)

    if tier == "image":
        # Just the PNG, full-bleed
        add_picture_fullbleed(slide, png)

    elif tier == "hybrid":
        # PNG background (text-hidden render) + editable text frames on top
        add_picture_fullbleed(slide, png)
        # Detect dark surface — look at any role with class containing "accent-light"
        on_dark = any(
            'class="accent-light"' in (e["html"] or "")
            for e in data["entries"] if e.get("html")
        )
        for entry in data["entries"]:
            if entry["role"] == "logo-light" or entry["role"] == "logo-dark":
                # Logo PNG is baked into the background — skip
                continue
            add_text_frame(slide, entry, on_dark=on_dark)

    elif tier == "semantic":
        # All native — no background PNG.
        # Render slide-level background fill from computed body color if needed.
        bg_color_entry = next((e for e in data["entries"] if e["role"] == "bg-color"), None)
        for entry in data["entries"]:
            if entry["role"].startswith("logo-"):
                # Insert logo PNG converted from SVG
                # (svg2png conversion handled separately — produces logo-light.png / logo-dark.png)
                continue
            add_text_frame(slide, entry)

# Strip the default shadow on every shape — PowerPoint adds one to text boxes
from pptx.oxml.ns import qn
for slide in prs.slides:
    for shape in slide.shapes:
        sppr = shape._element.find(qn("p:spPr"))
        if sppr is not None:
            effect_lst = sppr.find(qn("a:effectLst"))
            if effect_lst is not None:
                sppr.remove(effect_lst)

prs.save(str(DECK_DIR / "deck.pptx"))
print("wrote deck.pptx")
```

The above is a working skeleton — adapt as needed per deck.

## Step 4 — Convert the inline SVG logos to PNG

Geist + Inter + Plex Mono fall back at runtime, but the logo SVGs don't render reliably in PowerPoint. Convert once per deck.

```bash
# Using rsvg-convert (brew install librsvg)
rsvg-convert -w 310 -h 72 \
  /Users/davidsasson/.claude/skills/metafore-deck/assets/logo-light.svg \
  -o Decks/<deck-name>/_build/logo-light.png

rsvg-convert -w 310 -h 72 \
  /Users/davidsasson/.claude/skills/metafore-deck/assets/logo-dark.svg \
  -o Decks/<deck-name>/_build/logo-dark.png
```

Or use `cairosvg` from Python if `librsvg` isn't installed:

```python
import cairosvg
cairosvg.svg2png(url="…/logo-light.svg",
                 output_width=310, output_height=72,
                 write_to="…/_build/logo-light.png")
```

The PNG is what gets placed in the slide via `add_picture`.

## Step 5 — Verify

1. Open `Decks/<deck-name>/deck.pptx` in PowerPoint or Keynote.
2. Click each cover headline — should be selectable, editable text.
3. Click an image-tier slide (KPI band, pull-quote) — should be a single locked picture.
4. Change a cover headline — accent run should stay in its color.
5. Confirm fonts: if Geist is installed, headers render in Geist; otherwise they fall back through Inter to the system sans-serif.
6. Confirm no slide has a shadow under any text box.
7. Spot-check that text-frame positions match the HTML preview within ~2px.

If any text frame is off by more than ~5px, the `getBoundingClientRect` measurement happened before fonts loaded — re-run with `await page.evaluate("document.fonts.ready")` properly awaited.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Text frames shifted up-left by ~10px | Fonts loaded after measurement, browser used fallback metrics | Await `document.fonts.ready` before measuring |
| Headline accent word renders in default color | Run-split regex didn't match the span | Check the span has `class="accent"` (no other classes mixed in) |
| Plex Mono eyebrow renders bold and stretched | Brand rules not applied | Confirm post-write step ran and `spc=0`, `bold=false` are on every Plex Mono run |
| Cover background shows the headline twice (PNG + native) | `HIDE_CSS` didn't apply during render | Verify `data-pptx-text` attributes are present on the editable nodes |
| Logo missing from PPT | SVG not converted to PNG | Run the `rsvg-convert` / `cairosvg` step |
| File opens but slide content is rasterized | Tier set to `image` when `semantic` was intended | Change `data-pptx="semantic"` in the HTML |

## What this pipeline does NOT do

- **Speaker notes formatting** — notes go in as plain text. PowerPoint's notes-master font is what renders them; don't try to style them.
- **Slide transitions / animations** — none. PowerPoint defaults to instant cut.
- **Embedded video / audio** — out of scope.
- **PowerPoint themes** — every slide uses absolute positioning on the blank layout. Don't try to retrofit a theme.
- **Live charts** — all charts are baked-in PNG. If the client needs editable numbers, regenerate from updated HTML.
