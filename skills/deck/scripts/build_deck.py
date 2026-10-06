#!/usr/bin/env python3
"""build_deck.py — Metafore deck from a compact YAML content file.

Usage:
    python3 build_deck.py deck.yaml                 # → deck.html (self-contained preview)
    python3 build_deck.py deck.yaml --check --pptx  # …then check.py, then build_pptx.py
    python3 build_deck.py deck.yaml --src           # also write deck.src.html (debugging / hand edits)

The YAML holds content only; each pattern's template supplies the HTML, classes, chrome,
footers, tiers and data attributes. Schema: references/deck-yaml.md. Inline markup in any
text field: *accent words*, `code`, [ADD: …] placeholders; raw HTML is passed through.

Exit: 0 ok · 1 build/check error · 2 usage / missing dependency.
"""
import argparse
import html as _html
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parents[2]
sys.path.insert(0, str(PLUGIN / "scripts"))

# pattern → (P-id, css class, default tier)
PATTERNS = {
    "cover-1a": ("P-01", "p-cover-1a", "hybrid"), "cover-1b": ("P-01", "p-cover-1b", "hybrid"),
    "cover-1c": ("P-01", "p-cover-1c", "hybrid"), "divider": ("P-02", "p-divider", "semantic"),
    "agenda": ("P-03", "p-agenda", "semantic"), "company": ("P-04", "p-company", "semantic"),
    "track": ("P-04", "p-track", "semantic"), "statement": ("P-05", "p-statement", "hybrid"),
    "quiz": ("P-05", "p-statement", "hybrid"), "grid4": ("P-06", "p-grid4", "hybrid"),
    "grid8": ("P-07", "p-grid8", "hybrid"), "modules": ("P-08", "p-modules", "hybrid"),
    "kpi": ("P-09", "p-kpi", "hybrid"), "integrations": ("P-10", "p-integrations", "hybrid"),
    "timeline": ("P-11", "p-timeline", "hybrid"), "radial": ("P-12", "p-radial", "hybrid"),
    "closing": ("P-13", "p-closing", "semantic"), "compare": ("P-14", "p-compare", "semantic"),
    "quote": ("P-15", "p-quote", "hybrid"), "arch": ("P-16", "p-arch", "hybrid"),
    "hero-card": ("P-17", "p-hero-card", "hybrid"), "scenario": ("P-18", "p-scenario", "hybrid"),
    "team": ("P-19", "p-team-photos", "semantic"), "table": ("P-20", "p-table", "hybrid"),
    "anchor": ("P-21", "p-anchor", "hybrid"), "industries": ("P-22", "p-industries", "semantic"),
    "vertical": ("P-22", "p-vertical", "hybrid"), "raw": (None, "", "hybrid"),
}


class DeckError(Exception):
    pass


# --------------------------------------------------------------------------- inline markup
RE_ACCENT = re.compile(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])")
RE_CODE = re.compile(r"`([^`\n]+)`")
RE_PH = re.compile(r"\[(?:ADD\b|\+ ?add\b)[^\]\n]*\]")


def t(s):
    """Text field → HTML: *accent*, `code`, [ADD: …] placeholders; raw HTML passes through."""
    if s is None:
        return ""
    s = str(s)
    s = RE_CODE.sub(lambda m: f"<code>{_html.escape(m.group(1), quote=False)}</code>", s)
    s = RE_ACCENT.sub(r'<span class="accent">\1</span>', s)
    s = RE_PH.sub(lambda m: f'<span class="ph">{m.group(0)}</span>', s)
    return s


def a(s):
    return _html.escape(str(s or ""), quote=True)


def lst(v):
    return v if isinstance(v, list) else ([] if v is None else [v])


def lines(title):
    """A title given as a list renders one block line per item (cover / display style)."""
    if isinstance(title, list):
        return "".join(f'<span class="line">{t(x)}</span>' for x in title)
    return t(title)


def p(cls, v, tag="p"):
    return f'<{tag} class="{cls}">{t(v)}</{tag}>' if v not in (None, "") else ""


def bullets(v, small=False):
    if not v:
        return ""
    # one <span> per item keeps mixed content (bold lead + text) in the bullet's text column
    return f'<ul class="bullets{" small" if small else ""}">' + "".join(f"<li><span>{t(x)}</span></li>" for x in v) + "</ul>"


def icon(name, cls="lineicon", style=None):
    st = f' style="{a(style)}"' if style else ""
    return f'<img class="{cls}" src="@icon:{a(name)}" alt=""{st}>' if name else ""


def stats(v):
    if not v:
        return ""
    return '<div class="stats">' + "".join(
        f'<div class="stat"><div class="n">{t(n)}</div><div class="label l">{t(l)}</div></div>' for n, l in v) + "</div>"


def pills(v):
    return '<div class="pills">' + "".join(f'<span class="pill">{t(x)}</span>' for x in lst(v)) + "</div>"


def code_block(v):
    return f'<pre class="code">{_html.escape(str(v).rstrip(), quote=False)}</pre>' if v else ""


def head_block(s, dense=True):
    out = p("eyebrow", s.get("eyebrow"), "div") + f"<h2>{t(s.get('title'))}</h2>"
    out += p("body", s.get("body")) + p("lede", s.get("lede"))
    return f'<div class="head">{out}</div>' if dense else out


# --------------------------------------------------------------------------- mini cards & art
def card(c, kind="ui-card"):
    """Locked product mock-up. kind: ui-card (solid) | glasscard (cover only)."""
    if not c:
        return ""
    if isinstance(c, str):
        return f'<div class="{kind} mini" data-pptx-lock data-decorative>{c}</div>'
    parts = []
    if c.get("eyebrow") or c.get("meta"):
        parts.append(f'<div class="mini-head"><span class="mini-eyebrow">{t(c.get("eyebrow"))}</span>'
                     f'<span class="mini-meta">{t(c.get("meta"))}</span></div>')
    if c.get("title"):
        parts.append(f'<div class="mini-title">{t(c["title"])}</div>')
    if c.get("kpis"):
        parts.append('<div class="mini-kpis">' + "".join(
            f'<div><div class="n">{t(n)}</div><div class="l">{t(l)}</div></div>' for n, l in c["kpis"]) + "</div>")
    for r in c.get("rows", []):
        k, v = r[0], r[1]
        val = f'<span class="badge {a(r[2])}">{t(v)}</span>' if len(r) > 2 else f'<span class="v">{t(v)}</span>'
        parts.append(f'<div class="mini-row"><span class="k">{t(k)}</span>{val}</div>')
    for k, pct, v in c.get("bars", []):
        parts.append(f'<div class="mini-bar"><span class="k">{t(k)}</span><span class="track">'
                     f'<span class="fill" style="width:{float(pct):g}%;display:block"></span></span>'
                     f'<span class="v">{t(v)}</span></div>')
    if c.get("trace"):
        parts.append('<div class="mini-trace">' + "".join(
            f'<div class="ph"><b>{t(ph)}</b><span>{t(x)}</span></div>' for ph, x in c["trace"]) + "</div>")
    if c.get("tree"):
        cells = []
        for row in c["tree"]:
            d, f = (row + [""])[:2] if isinstance(row, list) else ("", row)
            muted = isinstance(row, list) and len(row) > 2 and row[2]
            cells.append(f'<span class="d">{t(d)}</span><span class="{"muted" if muted else "f"}">{t(f)}</span>')
        parts.append(f'<div class="tree">{"".join(cells)}</div>')
    if c.get("changes"):
        items = "".join(f'<div class="item"><b>{t(m)}</b><span>{t(x)}</span></div>' for m, x in c["changes"])
        btns = "".join(f'<span class="btn{" pri" if i == 0 else ""}">{t(b)}</span>' for i, b in enumerate(c.get("buttons", [])))
        parts.append(items + (f'<div class="btns">{btns}</div>' if btns else ""))
    if c.get("cta"):
        parts.append(f'<div class="mini-cta">{t(c["cta"])}</div>')
    if c.get("html"):
        parts.append(c["html"])
    extra = f' {c["class"]}' if c.get("class") else ""
    if c.get("changes"):
        extra += " changelist"
    style = f' style="{a(c["style"])}"' if c.get("style") else ""
    return f'<div class="{kind} mini{extra}" data-pptx-lock data-decorative{style}>{"".join(parts)}</div>'


def specimen(sp):
    """Deliberately off-brand mini slide for training. sp: {html, class, ignore}."""
    if not sp:
        return ""
    if isinstance(sp, str):
        sp = {"html": sp}
    ign = sp.get("ignore", "font,italic,gradient,shadow,absolute,voice,type-floor,orphan,contrast,para-length")
    style = f' style="{a(sp["style"])}"' if sp.get("style") else ""
    tag = sp.get("tag", "specimen · do not copy")
    return (f'<div class="specimen {a(sp.get("class", ""))}" data-pptx-lock data-decorative '
            f'data-check-ignore="{a(ign)}"{style}>{sp.get("html", "")}'
            f'<span class="tag">{t(tag)}</span></div>')


def art(v):
    """Right-hand art: {icon}|{card}|{svg}|{html}|{dead: [[label, n]]}|{specimen}|{hub}."""
    if not v:
        return ""
    if isinstance(v, str):
        return v
    if "icon" in v:
        return icon(v["icon"], "lineicon " + v.get("size", "lg"))
    if "card" in v:
        return card(v["card"])
    if "specimen" in v:
        return specimen(v["specimen"])
    if "dead" in v:
        cells = "".join(f'<div class="dead"><span class="mini-eyebrow">{t(l)}</span><span class="n">{t(n)}</span>'
                        f'<span class="foot">—</span></div>' for l, n in v["dead"])
        return f'<div class="dead-grid" data-pptx-lock data-decorative>{cells}</div>'
    if "hub" in v:
        return hub_svg(v["hub"])
    return v.get("svg") or v.get("html") or ""


def hub_svg(h):
    """One source box feeding N labelled outputs (e.g. brand pack → five skills)."""
    items = lst(h.get("items"))
    sub = lst(h.get("sub"))
    n = max(1, len(items))
    H = max(420, 130 * n)
    cy = H / 2
    ys = [65 + i * (H - 130) / max(1, n - 1) for i in range(n)] if n > 1 else [cy]
    box_h = 96 + 32 * len(sub)
    out = [f'<svg viewBox="0 0 800 {H:g}" fill="none" aria-label="{a(h.get("label", "diagram"))}">',
           f'<rect x="20" y="{cy - box_h / 2:g}" width="270" height="{box_h:g}" rx="14" fill="#E8F4F5" stroke="#006B6F" stroke-width="2"/>',
           f'<text x="44" y="{cy - box_h / 2 + 46:g}" fill="#006B6F">{a(h.get("center", ""))}</text>',
           f'<line x1="44" y1="{cy - box_h / 2 + 64:g}" x2="266" y2="{cy - box_h / 2 + 64:g}" stroke="#006B6F" stroke-opacity="0.4"/>']
    for i, s_ in enumerate(sub):
        out.append(f'<text x="44" y="{cy - box_h / 2 + 100 + 32 * i:g}" fill="#404040" '
                   f'style="text-transform:none;letter-spacing:0">{a(s_)}</text>')
    out.append(f'<g stroke="#006B6F" stroke-width="2"><line x1="290" y1="{cy:g}" x2="400" y2="{cy:g}"/>'
               f'<line x1="400" y1="{ys[0]:g}" x2="400" y2="{ys[-1]:g}"/>' +
               "".join(f'<line x1="400" y1="{y:g}" x2="460" y2="{y:g}"/>' for y in ys) + "</g>")
    out.append(f'<circle cx="400" cy="{cy:g}" r="7" fill="#006B6F"/>')
    for y, it in zip(ys, items):
        out.append(f'<rect x="460" y="{y - 34:g}" width="320" height="68" rx="10" fill="#FFFFFF" stroke="#ECECEC" stroke-width="2"/>'
                   f'<text x="484" y="{y + 8:g}" fill="#006B6F">{a(it)}</text>')
    out.append("</svg>")
    return "".join(out)


def traces(v):
    if not v:
        return ""
    return '<div class="traces" data-visual>' + "".join(
        f'<div class="trace"><div class="a-num">{t(x.get("num"))}</div><h3>{t(x.get("title"))}</h3>'
        f'<div class="a-role">{t(x.get("role"))}</div>{p("small", x.get("body"))}</div>' for x in v) + "</div>"


def sources(v):
    if not v:
        return ""
    return (f'<div class="sources"><span class="label">{t(v.get("label", "Sources"))}</span>'
            + "".join(f'<span class="pill">{t(x)}</span>' for x in lst(v.get("pills"))) + "</div>")


def scale(v):
    if not v:
        return ""
    rows = []
    for r in v:
        tag = f'<span class="tag">{t(r["tag"])}</span>' if r.get("tag") else ""
        rows.append(f'<div class="row"><div class="top"><span class="label">{t(r.get("label"))}</span>{tag}</div>'
                    f'<div class="track"><div class="fill" style="width:{float(r.get("pct", 50)):g}%"></div></div>'
                    f'{p("small", r.get("text"))}</div>')
    return f'<div class="scale">{"".join(rows)}</div>'


# --------------------------------------------------------------------------- patterns
def r_cover(s, variant):
    title = f"<h1>{lines(s.get('title'))}</h1>" + p("subtitle", s.get("subtitle"))
    if variant == "1b":
        title += p("badge-box", s.get("badge"), "div")
        return f"<div>{title}</div>" + card(s.get("card"), "glasscard")
    right = card(s.get("card"), "ui-card datacard" if variant == "1a" else "glasscard")
    return f'<div class="left">{title}</div><div class="right">{right}</div>'


def r_divider(s):
    title = s.get("title")
    sentence = s.get("sentence", len(re.sub(r"<[^>]+>|\*", "", str(title))) > 28)
    prog = ""
    if s.get("progress"):
        cur = s.get("current")
        on = ' class="on"'
        prog = '<div class="progress" data-visual>' + "".join(
            f'<span{on if (i + 1 == cur or x == cur) else ""}>{t(x)}</span>'
            for i, x in enumerate(s["progress"])) + "</div>"
    h1_cls = ' class="sentence"' if sentence else ""
    return (p("eyebrow", s.get("eyebrow"), "div") +
            f'<h1{h1_cls}>{t(title)}</h1>' + p("subtitle", s.get("subtitle")) + prog)


def r_agenda(s):
    items = s.get("items", [])
    rows = s.get("rows") or math.ceil(len(items) / 2)
    cells = "".join(f'<div class="item"><span class="a-num">{i + 1:02d}</span><div class="a-title">{t(x[0])}'
                    f'<span class="a-sub">{t(x[1] if len(x) > 1 else "")}</span></div></div>' for i, x in enumerate(items))
    return head_block(s) + f'<div class="items" data-visual style="--rows: {rows}">{cells}</div>'


def r_company(s):
    left = f"<h2>{t(s.get('title'))}</h2>" + p("body", s.get("body")) + p("signature", s.get("signature"))
    facts = "".join(f'<div class="fact">{icon(f[0])}<div><div class="f-label">{t(f[1])}</div>'
                    f'<div class="f-value">{t(f[2])}</div>{p("f-sub", f[3] if len(f) > 3 else "", "div")}</div></div>'
                    for f in s.get("facts", []))
    return f'<div>{left}</div><div class="facts">{facts}</div>'


def r_track(s):
    left = f"<h2>{t(s.get('title'))}</h2>" + p("body", s.get("body"))
    cards = "".join(f'<div class="card alt">{icon(c.get("icon"))}<h3>{t(c.get("title"))}</h3>{p("small", c.get("body"))}</div>'
                    for c in s.get("cards", []))
    return f'<div>{left}</div><div class="grid">{cards}</div>'


def r_statement(s):
    tag = "h2"
    left = (p("eyebrow", s.get("eyebrow"), "div") + f"<{tag}>{t(s.get('title'))}</{tag}>" + p("body", s.get("body"))
            + bullets(s.get("bullets"), small=s.get("bullets_small", False)) + stats(s.get("stats"))
            + p("small", s.get("small")))
    return f'<div>{left}</div><div class="art">{art(s.get("art"))}</div>'


def r_quiz(s):
    left = f'<h2 style="margin-bottom:24px">{t(s.get("title"))}</h2>' + specimen(s.get("specimen"))
    answers = "".join(f"<li>{t(x)}</li>" for x in s.get("answers", []))
    right = f'<div class="label" style="margin-bottom:24px">{t(s.get("answers_label", "Answers"))}</div><ol class="numbered">{answers}</ol>'
    return f'<div class="art stack">{left}</div><div>{right}</div>'


def r_grid4(s):
    tiles = s.get("tiles", [])
    cells = "".join(f'<div class="tile">{icon(x.get("icon"))}<div class="t-num">{t(x.get("tag"))}</div>'
                    f'<h3>{t(x.get("title"))}</h3>{p("small", x.get("body"))}</div>' for x in tiles)
    return head_block(s) + f'<div class="tiles{" cols-3" if len(tiles) == 3 else ""}">{cells}</div>'


def r_grid8(s):
    cells = s.get("cells", [])
    cols3 = s.get("cols") == 3 or len(cells) in (3, 6, 9)
    html_cells = "".join(f'<div class="cap"><div class="c-num">{t(x.get("tag"))}</div>{icon(x.get("icon"))}'
                         + (f'<div class="skill">{t(x["mono"])}</div>' if x.get("mono") else f'<h3>{t(x.get("title"))}</h3>')
                         + f'{p("small", x.get("body"))}</div>' for x in cells)
    return head_block(s) + f'<div class="grid{" cols-3" if cols3 else ""}">{html_cells}</div>'


def r_modules(s):
    cells = "".join(f'<div class="mod"><div class="m-top"><span class="m-num">{i + 1:02d}</span>'
                    f'<span class="m-for">{t(x.get("for"))}</span></div><h3>{t(x.get("name"))}</h3>{p("small", x.get("body"))}</div>'
                    for i, x in enumerate(s.get("modules", [])))
    return head_block(s) + f'<div class="grid" data-visual>{cells}</div>'


def r_kpi(s):
    kpis = s.get("kpis", [])
    cells = "".join(f'<div class="kpi"><div class="num">{t(k[0])}<span class="suffix">{t(k[1])}</span></div>'
                    f'<p class="l">{t(k[2])}</p></div>' for k in kpis)
    return (head_block(s) + f'<div class="kpis" data-visual style="--cols: {len(kpis)}">{cells}</div>'
            + p("source", s.get("source")))


def r_integrations(s):
    left = f"<h2>{t(s.get('title'))}</h2>" + p("body", s.get("body")) + "".join(p("small", x) for x in lst(s.get("small")))
    cl = "".join(f'<div class="cluster"><div class="label">{t(c.get("label"))}</div>{pills(c.get("pills"))}</div>'
                 for c in s.get("clusters", []))
    return f'<div>{left}</div><div class="clusters" data-visual>{cl}</div>'


def r_timeline(s):
    steps = s.get("steps", [])
    cells = "".join(f'<div class="step"><div class="s-week">{t(x.get("when"))}</div>'
                    + (f'<div class="s-num">{t(x["num"])}</div>' if x.get("num") else "")
                    + f'<h3>{t(x.get("title"))}</h3>{p("small", x.get("body"))}</div>' for x in steps)
    out = head_block(s) + f'<div class="steps" data-visual style="--steps: {len(steps)}">{cells}</div>'
    return out + code_block(s.get("code")) + p("small", s.get("note"))


def r_radial(s):
    left = (f"<h2>{t(s.get('title'))}</h2>" + p("body", s.get("body"))
            + bullets(s.get("bullets"), small=True) + stats(s.get("stats")) + p("small", s.get("small")))
    diagram = hub_svg(s["hub"]) if s.get("hub") else (s.get("svg") or "")
    return f'<div>{left}</div><div class="diagram">{diagram}</div>'


def r_closing(s):
    return f"<h1>{t(s.get('title'))}</h1>" + p("cta-line", s.get("cta"))


def r_compare(s):
    cols = []
    for c in s.get("cols", []):
        body = f'<div class="label">{t(c.get("label"))}</div>'
        if c.get("icon"):
            body += icon(c["icon"], "lineicon sm", "margin-bottom:24px")
        if c.get("card"):
            body += card(c["card"])
        if c.get("specimen"):
            body += specimen(c["specimen"])
        if c.get("stat"):
            body += f'<div class="stat"><div class="n">{t(c["stat"][0])}</div><div class="label l">{t(c["stat"][1])}</div></div>'
        if c.get("bullets"):
            body += bullets(c["bullets"])
        if c.get("body"):
            body += f'<p class="body" style="margin-top:24px">{t(c["body"])}</p>'
        cols.append(f'<div class="col">{body}</div>')
    return head_block(s) + f'<div class="cols">{"".join(cols)}</div>' + p("note-line", s.get("note"))


def r_quote(s):
    return (f'<div data-visual><div class="quote-glyph">“</div><p class="quote">{t(s.get("quote"))}</p>'
            f'<div class="label attribution">— {t(s.get("attribution"))}</div></div>')


def r_arch(s):
    layers = s.get("layers", [])
    cells = "".join(f'<div class="layer"><h3>{t(x.get("title"))}</h3>{p("small", x.get("body"))}'
                    + "".join(f'<div class="chip">{t(c)}</div>' for c in lst(x.get("chips"))) + "</div>" for x in layers)
    return head_block(s) + f'<div class="layers" data-visual style="--cols: {len(layers)}">{cells}</div>'


def r_hero_card(s):
    meta = ""
    if s.get("meta"):
        meta = '<div class="meta">' + "".join(f'<div><div class="label">{t(k)}</div><div class="v">{t(v)}</div></div>'
                                             for k, v in s["meta"]) + "</div>"
    left = (p("eyebrow", s.get("eyebrow"), "div") + f"<h2>{t(s.get('title'))}</h2>" + p("body", s.get("body"))
            + bullets(s.get("bullets"), small=True) + scale(s.get("scale")) + meta)
    return f'<div class="left">{left}</div><div class="stage">{card(s.get("card"))}</div>'


def r_scenario(s):
    top = f'<div class="top"><div><h2>{t(s.get("title"))}</h2>{p("body", s.get("body"))}</div>{card(s.get("card"))}</div>'
    return top + traces(s.get("traces")) + sources(s.get("sources"))


def r_anchor(s):
    badge = (f'<div class="anchor-badge"><span class="ab-lbl">Anchors into</span><span class="ab-arrow">→</span>'
             f'<span class="ab-mod">{t(s.get("anchor"))}</span></div>')
    return f"<h2>{t(s.get('title'))}</h2>" + badge + p("body", s.get("body")) + traces(s.get("traces")) + sources(s.get("sources"))


def r_team(s):
    ppl = s.get("people", [])
    ph = ('<svg class="ph" viewBox="0 0 100 100" preserveAspectRatio="none"><line x1="0" y1="100" x2="100" y2="0"/></svg>'
          '<span class="ph-label">Photo</span>')
    def photo(x):
        return f'<img src="{a(x[2])}" alt="{a(x[0])}">' if len(x) > 2 and x[2] else ph
    cells = "".join(f'<div><div class="photo">{photo(x)}</div>'
                    f'<div class="name">{t(x[0])}</div><div class="role">{t(x[1])}</div></div>' for x in ppl)
    return head_block(s) + f'<div class="people" style="--cols: {s.get("cols", 4 if len(ppl) <= 4 else 3)}">{cells}</div>'


def r_table(s):
    head = s.get("head", [])
    kinds = s.get("kinds") or (["cap", "mod"] + ["desc"] * max(0, len(head) - 2))[:len(head)]
    cols = s.get("cols") or " ".join(["1fr", "0.8fr"] + ["2fr"] * max(0, len(head) - 2))
    cells = "".join(f'<div class="th">{t(h)}</div>' for h in head)
    for row in s.get("rows", []):
        cells += "".join(f'<div class="{kinds[i] if i < len(kinds) else "desc"}">{t(c)}</div>' for i, c in enumerate(row))
    return head_block(s) + f'<div class="table" data-visual style="--table-cols: {a(cols)}">{cells}</div>'


def r_industries(s):
    cards = s.get("cards", [])
    cells = "".join(f'<div class="card alt">{icon(c.get("icon"))}'
                    + (f'<div class="label">{t(c["label"])}</div>' if c.get("label") else "")
                    + (f'<h3>{t(c["title"])}</h3>' if c.get("title") else "")
                    + (f'<p class="quote-text">{t(c["quote"])}</p>' if c.get("quote") else p("small", c.get("body")))
                    + "</div>" for c in cards)
    return head_block(s) + f'<div class="grid" style="--cols: {s.get("cols", 3)}">{cells}</div>'


def r_vertical(s):
    rows = "".join(f'<div class="row"><strong>{t(r[0])}</strong>{p("small", r[1] if len(r) > 1 else "")}</div>'
                   for r in s.get("rows", []))
    left = f"<h1>{t(s.get('title'))}</h1>" + p("lede", s.get("lede")) + (f'<div class="rows card alt">{rows}</div>' if rows else "")
    return f'<div>{left}</div><div class="media">{art(s.get("art"))}</div>'


RENDER = {
    "cover-1a": lambda s: r_cover(s, "1a"), "cover-1b": lambda s: r_cover(s, "1b"), "cover-1c": lambda s: r_cover(s, "1c"),
    "divider": r_divider, "agenda": r_agenda, "company": r_company, "track": r_track, "statement": r_statement,
    "quiz": r_quiz, "grid4": r_grid4, "grid8": r_grid8, "modules": r_modules, "kpi": r_kpi,
    "integrations": r_integrations, "timeline": r_timeline, "radial": r_radial, "closing": r_closing,
    "compare": r_compare, "quote": r_quote, "arch": r_arch, "hero-card": r_hero_card, "scenario": r_scenario,
    "team": r_team, "table": r_table, "anchor": r_anchor, "industries": r_industries, "vertical": r_vertical,
    "raw": lambda s: s.get("html", ""),
}
ALIASES = {"cover": "cover-1b", "p-01": "cover-1b", "p-02": "divider", "p-03": "agenda", "p-04": "company",
           "p-05": "statement", "p-06": "grid4", "p-07": "grid8", "p-08": "modules", "p-09": "kpi",
           "p-10": "integrations", "p-11": "timeline", "p-12": "radial", "p-13": "closing", "p-14": "compare",
           "p-15": "quote", "p-16": "arch", "p-17": "hero-card", "p-18": "scenario", "p-19": "team",
           "p-20": "table", "p-21": "anchor", "p-22": "industries", "hero": "hero-card", "pullquote": "quote"}


def slide_html(s, idx):
    name = str(s.get("pattern", "")).strip().lower()
    name = ALIASES.get(name, name)
    if name not in RENDER:
        raise DeckError(f"slide {idx}: unknown pattern '{s.get('pattern')}'. "
                        f"Known: {', '.join(k for k in RENDER)}")
    pid, cls, tier = PATTERNS[name]
    classes = ["slide"] + ([cls] if cls else []) + lst(s.get("class")) + (["dark"] if s.get("dark") else [])
    attrs = [f'class="{a(" ".join(classes))}"', f'data-pptx="{a(s.get("tier", tier))}"']
    if pid or s.get("pattern_id"):
        attrs.append(f'data-pattern="{a(s.get("pattern_id", pid))}"')
    if s.get("label"):
        attrs.append(f'data-label="{a(s["label"])}"')
    else:
        attrs.append('data-chrome="auto"' if s.get("chrome", True) else 'data-chrome="none"')
    if s.get("ignore"):
        attrs.append(f'data-check-ignore="{a(s["ignore"])}"')
    style = s.get("style")
    if isinstance(style, dict):
        style = "; ".join(f"{k}: {v}" for k, v in style.items())
    if style:
        attrs.append(f'style="{a(style)}"')
    body = s["html"] if (name != "raw" and s.get("html")) else RENDER[name](s)
    body += s.get("extra", "")
    if s.get("notes"):
        body += f'<aside class="speaker-notes">{t(s["notes"])}</aside>'
    return f"<section {' '.join(attrs)}>{body}</section>"


def deck_src(d):
    slides = d.get("slides") or []
    if not slides:
        raise DeckError("no slides")
    body = "\n".join(slide_html(s, i + 1) for i, s in enumerate(slides))
    title = a(d.get("title", "Metafore deck"))
    css = d.get("css", "")
    return (f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><title>{title}</title>\n<!-- @fonts -->\n'
            f"<style>\n/* @tokens:deck */\n/* @css:deck/patterns */\n{css}\n</style></head>\n<body>\n{body}\n</body></html>\n")


def main():
    ap = argparse.ArgumentParser(description="Build a Metafore deck from a YAML content file.")
    ap.add_argument("yaml")
    ap.add_argument("--out", help="output .html (default: next to the YAML)")
    ap.add_argument("--src", action="store_true", help="also write the generated .src.html")
    ap.add_argument("--check", action="store_true", help="run check.py --kind deck with a contact sheet")
    ap.add_argument("--pptx", action="store_true", help="run build_pptx.py after a clean check")
    ap.add_argument("--force-pptx", action="store_true", help="build the PPTX even if the check has errors")
    args = ap.parse_args()
    try:
        import yaml
    except ImportError:
        print("missing dependency: pip install pyyaml")
        return 2
    import build_html
    src_path = Path(args.yaml)
    if not src_path.exists():
        print(f"error: {src_path} not found")
        return 2
    try:
        d = yaml.safe_load(src_path.read_text(encoding="utf-8")) or {}
        src = deck_src(d)
        html_out, st = build_html.build(src)
    except (DeckError, build_html.BuildError, yaml.YAMLError) as e:
        print(f"error: {e}")
        return 1
    stem = src_path.name.rsplit(".", 1)[0]
    out = Path(args.out) if args.out else src_path.with_name(stem + ".html")
    if args.src:
        out.with_name(stem + ".src.html").write_text(src, encoding="utf-8")
    out.write_text(html_out, encoding="utf-8")
    n = len(d.get("slides", []))
    print(f"built {out} ({n} slides, {st['chrome']} auto-chrome, {st['icons']} icons, {out.stat().st_size // 1024} KB)",
          flush=True)
    rc = 0
    if args.check or args.pptx:
        build_dir = out.parent if out.parent.name == "_build" else out.parent / "_build"
        build_dir.mkdir(exist_ok=True)
        r = subprocess.run([sys.executable, str(PLUGIN / "scripts" / "check.py"), str(out), "--kind", "deck",
                            "--sheet", str(build_dir / f"{stem}.sheet.png")])
        rc = r.returncode
    if args.pptx and (rc == 0 or args.force_pptx):
        r = subprocess.run([sys.executable, str(HERE / "build_pptx.py"), str(out)])
        rc = rc or r.returncode
    elif args.pptx:
        print("pptx: skipped — fix the check errors first (or pass --force-pptx)")
    return 1 if rc == 1 else rc


if __name__ == "__main__":
    sys.exit(main())
