#!/usr/bin/env python3
"""build_html.py — resolve Metafore placeholders into a self-contained HTML file.

Usage:
    python3 build_html.py page.src.html            # writes page.html
    python3 build_html.py page.src.html --out x.html
    python3 build_html.py --list                   # list tokens kinds, logos, icons

Placeholders (in the source HTML):
    <!-- @fonts -->                      Google Fonts links (Geist, Inter, IBM Plex Mono 400/500/600)
    /* @tokens:KIND */                   contents of skills/KIND/assets/tokens.css (put inside <style>)
    /* @css:KIND/NAME */                 contents of skills/KIND/assets/NAME.css (@tokens:KIND = @css:KIND/tokens)
    <section class="slide p-…" data-label="Setup">   (or data-chrome="auto")
                                         auto deck chrome for that slide: section label, the
                                         light/dark corner icon (cover wordmark / closing
                                         brandmark), and the footer — chosen from the pattern
                                         class. data-chrome="none" opts a slide out.
    <!-- @footer --> / <!-- @footer on-dark -->
                                         (inside a <section class="slide">) deck footer with
                                         "(c) YEAR METAFORE ..." and page number NN / TT
    <!-- @logo:NAME attr="v" ... -->     inline assets/graphics/logos/NAME.svg; attrs merge onto <svg>
    @icon:Name                           (inside an attribute value) data URI of
                                         assets/graphics/line-icons/Name.png
    @asset:rel/path.ext                  (inside an attribute value / url()) data URI of assets/rel/path.ext

The source file is never modified. Running twice gives the same output.
Exit codes: 0 ok, 1 unresolved/unknown placeholder, 2 usage error.
"""
import argparse
import base64
import difflib
import mimetypes
import re
import datetime
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGO_DIR = ROOT / "assets" / "graphics" / "logos"
ICON_DIR = ROOT / "assets" / "graphics" / "line-icons"
ASSET_DIR = ROOT / "assets"

FONTS_HTML = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600'
    '&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">'
)

MIME = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}

RE_FONTS = re.compile(r"<!--\s*@fonts\s*-->")
RE_TOKENS = re.compile(r"/\*\s*@tokens:([\w-]+)\s*\*/")
RE_CSS = re.compile(r"/\*\s*@css:([\w-]+)/([\w.-]+?)(?:\.css)?\s*\*/")
RE_FOOTER = re.compile(r"<!--\s*@footer(\s+on-dark)?\s*-->")
RE_SLIDE = re.compile(r"<section\b[^>]*\bclass\s*=\s*[\"'][^\"']*\bslide\b[^\"']*[\"']", re.I)
# Attributes are captured as one run of text up to "-->" and parsed by RE_ATTR afterwards.
# Each character matches exactly one way (no nested quantifiers), so a malformed
# placeholder can't trigger catastrophic backtracking (CodeQL py/redos).
RE_LOGO = re.compile(r"<!--\s*@logo:([\w-]+)((?:[^>-]|-(?!->))*)-->")
RE_ICON = re.compile(r"@icon:([A-Za-z0-9_-]+)")
RE_ASSET = re.compile(r"@asset:([A-Za-z0-9_./ -]+?\.(?:svg|png|jpe?g|webp|gif))", re.I)
# Quoted attribute values may contain ">"; the three branches are disjoint, so matching stays linear.
RE_SECTION_OPEN = re.compile(r"<section\b(?:[^>\"']|\"[^\"]*\"|'[^']*')*>", re.I)
# Patterns whose slide surface is --teal-dark (chrome switches to the on-dark variants)
DARK_PATTERNS = {"p-cover-1b", "p-divider", "p-kpi", "dark"}
RE_ATTR = re.compile(r"([\w:-]+)(?:\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+))?")
KNOWN_CSS_AT = {"media", "page", "font", "import", "keyframes", "supports", "container", "layer",
                "charset", "namespace", "property", "counter", "scope", "starting", "apply", "tailwind"}


class BuildError(Exception):
    pass


def tokens_kinds():
    return sorted(p.parent.parent.name for p in (ROOT / "skills").glob("*/assets/tokens.css"))


def css_files():
    return sorted(f"{p.parent.parent.name}/{p.stem}" for p in (ROOT / "skills").glob("*/assets/*.css"))


def logo_names():
    return sorted(p.stem for p in LOGO_DIR.glob("*.svg"))


def icon_names():
    return sorted(p.stem for p in ICON_DIR.glob("*.png"))


def closest(name, options):
    m = difflib.get_close_matches(name, options, n=3, cutoff=0.4)
    if not m:
        m = [o for o in options if name.lower() in o.lower() or o.lower() in name.lower()][:3]
    return ", ".join(m) if m else "none"


def data_uri(path):
    mime = MIME.get(path.suffix.lower()) or mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def load_svg(name, attrs_src):
    path = LOGO_DIR / f"{name}.svg"
    if not path.exists():
        raise BuildError(f"@logo:{name} unknown. available: {', '.join(logo_names())}")
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(r"<\?xml.*?\?>", "", svg, flags=re.S)
    svg = re.sub(r"<!DOCTYPE.*?>", "", svg, flags=re.S | re.I)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    m = re.search(r"<svg\b([^>]*)>", svg)
    if not m:
        raise BuildError(f"@logo:{name}: no <svg> root")
    existing = {}
    order = []
    for k, v in RE_ATTR.findall(m.group(1)):
        existing[k] = v[1:-1] if v[:1] in "\"'" else v
        order.append(k)
    for k, v in RE_ATTR.findall(attrs_src or ""):
        val = (v[1:-1] if v[:1] in "\"'" else v) if v else ""
        if k not in existing:
            order.append(k)
        existing[k] = val
    root = "<svg " + " ".join(f'{k}="{existing[k]}"' for k in order) + ">"
    return svg[:m.start()] + root + svg[m.end():]


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chrome_for(classes, label):
    """Deck chrome (as placeholders) for one slide, picked from its pattern class."""
    dark = bool(DARK_PATTERNS & classes)
    on = " on-dark" if dark else ""
    footer = f"<!-- @footer{on} -->"
    if any(c.startswith("p-cover") for c in classes):
        mark = "logo-dark" if "p-cover-1b" in classes else "logo-light"
        return f'<!-- @logo:{mark} width="155" height="36" class="logo-tl" -->{footer}'
    if "p-closing" in classes:
        return f'<!-- @logo:icon-light width="172" height="144" class="brandmark" -->{footer}'
    # P-17 puts the icon over its dark stage; dividers carry an eyebrow instead of a label
    icon = "icon-dark" if dark or "p-hero-card" in classes else "icon-light"
    parts = []
    if label and "p-divider" not in classes:
        parts.append(f'<div class="section-label{on}">{esc(label)}</div>')
    parts.append(f'<!-- @logo:{icon} width="72" height="60" class="icon-tr" -->')
    parts.append(footer)
    return "".join(parts)


def add_chrome(src, stats):
    def sec(m):
        tag = m.group(0)
        attrs = {k: (v[1:-1] if v[:1] in "\"'" else v) for k, v in RE_ATTR.findall(tag[8:-1])}
        classes = set(attrs.get("class", "").split())
        mode = attrs.get("data-chrome")
        if "slide" not in classes or mode == "none" or ("data-label" not in attrs and mode != "auto"):
            return re.sub(r'\s+data-chrome\s*=\s*(?:"none"|\'none\')', "", tag)
        stats["chrome"] += 1
        # drop data-chrome so checkers don't mistake the whole slide for chrome
        clean = re.sub(r'\s+data-chrome\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+)', "", tag)
        return clean + chrome_for(classes, attrs.get("data-label", ""))
    return RE_SECTION_OPEN.sub(sec, src)


def build(src_text):
    stats = {"tokens": [], "logos": 0, "icons": 0, "assets": 0, "fonts": 0, "footers": 0, "chrome": 0}

    out = add_chrome(src_text, stats)
    # deck footers (first, on the raw source): page number = index of the enclosing section.slide
    masked = re.sub(r"<!--(?!\s*@).*?-->|/\*.*?\*/", lambda c: " " * len(c.group(0)), out, flags=re.S)
    slide_starts = [m.start() for m in RE_SLIDE.finditer(masked)]
    total = len(slide_starts)
    year = datetime.date.today().year

    def footer(m):
        idx = sum(1 for st in slide_starts if st < m.start())
        if idx == 0:
            raise BuildError("@footer must be inside a <section class=\"slide\">")
        stats["footers"] += 1
        cls = "deck-footer on-dark" if m.group(1) else "deck-footer"
        return (f'<div class="{cls}">'
                f'<span class="copy-line">\u00a9 {year} METAFORE \u00b7 ALL RIGHTS RESERVED \u00b7 CONFIDENTIAL</span>'
                f'<span class="page-num">{idx:02d} / {total:02d}</span></div>')
    out = RE_FOOTER.sub(footer, out)

    def fonts(_m):
        stats["fonts"] += 1
        return FONTS_HTML
    out = RE_FONTS.sub(fonts, out)

    def tok(m):
        kind = m.group(1)
        p = ROOT / "skills" / kind / "assets" / "tokens.css"
        if not p.exists():
            raise BuildError(f"@tokens:{kind} unknown. available: {', '.join(tokens_kinds())}")
        stats["tokens"].append(kind)
        return p.read_text(encoding="utf-8")
    out = RE_TOKENS.sub(tok, out)

    def css(m):
        kind, name = m.group(1), m.group(2)
        p = ROOT / "skills" / kind / "assets" / f"{name}.css"
        if not p.exists():
            raise BuildError(f"@css:{kind}/{name} unknown. available: {', '.join(css_files())}")
        stats["tokens"].append(f"{kind}/{name}" if name != "tokens" else kind)
        return p.read_text(encoding="utf-8")
    out = RE_CSS.sub(css, out)


    def logo(m):
        stats["logos"] += 1
        return load_svg(m.group(1), m.group(2))
    out = RE_LOGO.sub(logo, out)

    icons = icon_names()
    cache = {}

    def icon(m):
        name = m.group(1)
        p = ICON_DIR / f"{name}.png"
        if not p.exists():
            raise BuildError(f"@icon:{name} unknown. closest: {closest(name, icons)}")
        stats["icons"] += 1
        if name not in cache:
            cache[name] = data_uri(p)
        return cache[name]
    out = RE_ICON.sub(icon, out)

    def asset(m):
        rel = m.group(1).strip()
        p = (ASSET_DIR / rel).resolve()
        if ASSET_DIR.resolve() not in p.parents or not p.exists():
            allf = [str(x.relative_to(ASSET_DIR)) for x in ASSET_DIR.rglob("*") if x.suffix.lower() in MIME]
            raise BuildError(f"@asset:{rel} not found under assets/. closest: {closest(rel, allf)}")
        stats["assets"] += 1
        return data_uri(p)
    out = RE_ASSET.sub(asset, out)

    # leftover check: any @placeholder-ish token outside data URIs
    scan = re.sub(r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=]+", "", out)
    bad = []
    for m in re.finditer(r"(?<![\w.@])@([a-z][\w-]*):([\w./-]*)", scan):
        if m.group(1) in KNOWN_CSS_AT:
            continue
        bad.append(m.group(0))
    for m in re.finditer(r"<!--\s*@([\w-]+)", scan):
        bad.append("<!-- @" + m.group(1))
    for m in re.finditer(r"/\*\s*@(tokens|css)\b[^*]*\*/", scan):
        bad.append(m.group(0))
    if bad:
        uniq = sorted(set(bad))
        raise BuildError("unresolved placeholder(s): " + ", ".join(uniq[:8]) +
                         " (known: @fonts, @tokens:KIND, @css:KIND/NAME, @footer, @logo:NAME, @icon:Name, @asset:path)")
    return out, stats


def main():
    ap = argparse.ArgumentParser(description="Resolve Metafore placeholders into self-contained HTML.")
    ap.add_argument("src", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--list", action="store_true", help="list available tokens kinds, logos, icons")
    a = ap.parse_args()
    if a.list:
        print("tokens:", ", ".join(tokens_kinds()))
        print("css:", ", ".join(css_files()))
        print("logos:", ", ".join(logo_names()))
        print("icons:", ", ".join(icon_names()))
        return 0
    if not a.src:
        ap.error("src required")
    src = Path(a.src)
    if not src.exists():
        print(f"error: {src} not found")
        return 2
    if a.out:
        out = Path(a.out)
    elif ".src" in src.name:
        out = src.with_name(src.name.replace(".src", "", 1))
    else:
        print("error: input has no '.src' in its name; pass --out")
        return 2
    if out.resolve() == src.resolve():
        print("error: --out would overwrite the source")
        return 2
    try:
        html, st = build(src.read_text(encoding="utf-8"))
    except BuildError as e:
        print(f"error: {e}")
        return 1
    out.write_text(html, encoding="utf-8")
    parts = []
    if st["tokens"]:
        parts.append("css:" + "+".join(st["tokens"]))
    if st["fonts"]:
        parts.append("fonts")
    parts.append(f"{st['logos']} logos")
    parts.append(f"{st['icons']} icons")
    if st["chrome"]:
        parts.append(f"{st['chrome']} auto-chrome")
    if st["footers"]:
        parts.append(f"{st['footers']} footers")
    if st["assets"]:
        parts.append(f"{st['assets']} assets")
    parts.append(f"{out.stat().st_size // 1024} KB")
    print(f"built {out} ({', '.join(parts)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
