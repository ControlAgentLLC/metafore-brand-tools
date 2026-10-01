#!/usr/bin/env python3
"""Build an editable Metafore .pptx from a 1920x1080 HTML deck.

Usage:
    python3 build_pptx.py path/to/deck.html [--out deck.pptx] [--build-dir _build]
                          [--no-cache] [--scale 2]

Each slide is a ``<section class="slide" data-pptx="image|semantic|hybrid"
data-slide-id="...">`` at 1920x1080. Tiers:

* image    - one full-bleed screenshot.
* hybrid   - full-bleed screenshot with the editable text made transparent
             (backgrounds, borders, pills stay baked), native text frames on top.
* semantic - no screenshot: native rectangles for every visible box with a fill
             or border, element screenshots for <img>/<svg>/locked containers,
             native text frames on top.

Text frames are chosen automatically (any rendered element with a direct
non-whitespace text child and no selected ancestor, outside <svg> and
[data-pptx-lock]) unless the slide uses explicit [data-pptx-text] markers.
Runs and paragraphs come from computed styles, so no class-to-color map is
needed. Brand PPTX rules are applied on write (no Plex Mono tracking or bold,
no negative tracking under 22px, no italic, no shadows, Geist never bold).

Renders and a cache manifest go in ``<html dir>/_build/`` (``--build-dir`` is
resolved relative to the HTML's folder). Unchanged slides reuse their PNGs.
stdout is a short per-slide summary plus warnings, then the output path.
Exit codes: 0 ok, 1 input error, 2 missing dependencies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

INSTALL_HINT = "pip install python-pptx playwright pillow && python3 -m playwright install chromium"

try:
    from PIL import Image
    from playwright.sync_api import Error as PWError
    from playwright.sync_api import TimeoutError as PWTimeout
    from playwright.sync_api import sync_playwright
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
    from pptx.oxml.ns import qn
    from pptx.util import Emu, Pt
except ImportError:
    print(INSTALL_HINT)
    sys.exit(2)

VERSION = "1"  # bump to invalidate every cached render
CANVAS_W, CANVAS_H = 1920, 1080
SLIDE_W_EMU, SLIDE_H_EMU = 12192000, 6858000
EMU_PER_PX = SLIDE_W_EMU / CANVAS_W            # 6350 (NOT 9525 - that is a 1280px canvas)
PT_PER_PX = (SLIDE_W_EMU / 12700) / CANVAS_W   # 0.5
MIN_LINE_EMU = 9525                            # 1px CSS border -> 0.75pt hairline
BRAND_FLOOR_PX = 22
FONTS_TIMEOUT_MS = 10000
TIERS = ("image", "hybrid", "semantic")

ALIGN = {
    "left": PP_ALIGN.LEFT, "start": PP_ALIGN.LEFT, "-webkit-left": PP_ALIGN.LEFT,
    "center": PP_ALIGN.CENTER, "-webkit-center": PP_ALIGN.CENTER,
    "right": PP_ALIGN.RIGHT, "end": PP_ALIGN.RIGHT, "-webkit-right": PP_ALIGN.RIGHT,
    "justify": PP_ALIGN.JUSTIFY,
}
DASH = {"dashed": MSO_LINE_DASH_STYLE.DASH, "dotted": MSO_LINE_DASH_STYLE.ROUND_DOT}

# Injected once: stable rendering + the isolation rules used for element screenshots.
BASE_CSS = """
html { scrollbar-width: none !important; }
::-webkit-scrollbar { display: none !important; }
*, *::before, *::after { transition: none !important; caret-color: transparent !important; }
html.__pptx-iso, html.__pptx-iso body { background: transparent !important; }
html.__pptx-iso * { visibility: hidden !important; }
html.__pptx-iso .__pptx-full, html.__pptx-iso .__pptx-full * { visibility: visible !important; }
html.__pptx-iso .__pptx-box { visibility: visible !important; color: transparent !important;
  -webkit-text-fill-color: transparent !important; text-shadow: none !important; }
"""

FONTS_READY_JS = f"""() => Promise.race([
  document.fonts.ready.then(() => true),
  new Promise(r => setTimeout(() => r(false), {FONTS_TIMEOUT_MS}))])"""

# All DOM analysis happens in the page. Installs window.__pptx.
PAGE_JS = r"""
() => {
if (window.__pptx) return;
const BLOCK = new Set(['block','flex','grid','list-item','table','flow-root','table-row',
  'table-caption','table-row-group','table-header-group','table-footer-group']);
const SKIP = 'svg, img, picture, video, canvas, iframe, object, script, style, noscript, template, aside.speaker-notes, [data-pptx-lock]';
const EXCL = 'svg, aside.speaker-notes, [data-pptx-lock], script, style, noscript, template';
const PICTURE_TAGS = 'svg, img, video, canvas, iframe, object, [data-pptx-image]';
const cv = document.createElement('canvas'); cv.width = cv.height = 1;
const cx = cv.getContext('2d', {willReadFrequently: true});
const colorCache = new Map();
const num = v => { const f = parseFloat(v); return Number.isFinite(f) ? f : 0; };

function color(s) {
  if (!s) return [0, 0, 0, 0];
  if (colorCache.has(s)) return colorCache.get(s);
  let out;
  const m = s.match(/^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,/]\s*([\d.]+%?))?\s*\)$/);
  if (m) {
    const a = m[4] === undefined ? 1 : (m[4].endsWith('%') ? parseFloat(m[4]) / 100 : parseFloat(m[4]));
    out = [+m[1], +m[2], +m[3], a];
  } else if (s === 'transparent') {
    out = [0, 0, 0, 0];
  } else {  // color(srgb ...), oklch(...), etc: let the canvas resolve it
    cx.clearRect(0, 0, 1, 1); cx.fillStyle = 'rgba(0,0,0,0)'; cx.fillStyle = s; cx.fillRect(0, 0, 1, 1);
    const d = cx.getImageData(0, 0, 1, 1).data; out = [d[0], d[1], d[2], d[3] / 255];
  }
  colorCache.set(s, out); return out;
}
const mix = (c, a, bd) => [0, 1, 2].map(i => Math.round(c[i] * a + bd[i] * (1 - a)));
function opacity(el, slide) {
  let o = 1;
  for (let e = el; e; e = e.parentElement) { o *= num(getComputedStyle(e).opacity); if (e === slide) break; }
  return o;
}
function backdrop(el, slide, bg) {  // nearest opaque background at or above el
  for (let e = el; e && e !== slide; e = e.parentElement) {
    const c = color(getComputedStyle(e).backgroundColor);
    if (c[3] >= 0.999) return c;
  }
  return bg;
}
function opaque(c, el, slide, bg, from) {
  const a = c[3] * opacity(el, slide);
  if (a >= 0.999) return c.slice(0, 3).map(Math.round);
  return mix(c, a, backdrop(from, slide, bg));
}
function rendered(el) {
  if (!el.getClientRects().length) return false;
  const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0;
}
const hasDirectText = el => [...el.childNodes].some(n => n.nodeType === 3 && /\S/.test(n.data));
const TEXT_TAGS = new Set(['H1','H2','H3','H4','H5','H6','P','LI','BLOCKQUOTE','FIGCAPTION','DT','DD',
  'TH','TD','CAPTION','LABEL','BUTTON']);
function subtreeHasText(el) {
  const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  for (let t = tw.nextNode(); t; t = tw.nextNode()) if (/\S/.test(t.data) && !t.parentElement.closest(EXCL)) return true;
  return false;
}
// A text frame root: direct text, or a text-block tag / block whose children are all
// inline (so <h1><span class="line">..</span><span class="line">..</span></h1> and
// <div><span>A</span> <span class="accent">B</span></div> stay one frame). Flex/grid
// containers never qualify on their own: their children are laid out independently.
function isTextRoot(el) {
  if (hasDirectText(el)) return true;
  const cs = getComputedStyle(el);
  if (/flex|grid/.test(cs.display) || !subtreeHasText(el)) return false;
  if (TEXT_TAGS.has(el.tagName)) return true;
  if (!/^(block|list-item|table-cell|flow-root)$/.test(cs.display)) return false;
  return [...el.children].every(c => { const d = getComputedStyle(c).display;
    return c.tagName === 'BR' || d === 'none' || d.startsWith('inline') || d === 'contents'; });
}
const family = f => (f.split(',')[0] || '').trim().replace(/^["']|["']$/g, '');
function transform(t, mode) {
  if (mode === 'uppercase') return t.toUpperCase();
  if (mode === 'lowercase') return t.toLowerCase();
  if (mode === 'capitalize') return t.replace(/(^|[\s\-–—(\["'“‘])(\p{L})/gu, (m, a, b) => a + b.toUpperCase());
  return t;
}
function textColor(p, slide, bg) {
  const cs = getComputedStyle(p);
  let c = color(cs.webkitTextFillColor);
  if (c[3] === 0) c = color(cs.color);
  return opaque(c, p, slide, bg, p);
}

function buildParas(root, slide, bg) {
  const paras = []; let cur = null; const stack = [root];
  const pstyle = el => {
    const cs = getComputedStyle(el); const fs = num(cs.fontSize);
    return {align: cs.textAlign, lineHeight: cs.lineHeight === 'normal' ? fs * 1.2 : num(cs.lineHeight),
            fontSize: fs, runs: [], br: false};
  };
  const ensure = () => { if (!cur) { cur = pstyle(stack[stack.length - 1]); paras.push(cur); } return cur; };
  const hardBreak = () => { ensure().br = true; cur = null; };
  const visit = node => {
    if (node.nodeType === 3) {
      const p = node.parentElement; const cs = getComputedStyle(p);
      if (cs.visibility !== 'visible' || !node.data) return;
      const ws = cs.whiteSpace;
      const keepNL = /^(pre|pre-wrap|pre-line|break-spaces)$/.test(ws);
      const collapse = !/^(pre|pre-wrap|break-spaces)$/.test(ws);
      const base = {font: family(cs.fontFamily), size: num(cs.fontSize), weight: parseInt(cs.fontWeight, 10) || 400,
        color: textColor(p, slide, bg), ls: cs.letterSpacing === 'normal' ? 0 : num(cs.letterSpacing),
        italic: cs.fontStyle !== 'normal', transform: cs.textTransform, collapse,
        footer: !!p.closest('.deck-footer')};
      const parts = keepNL ? node.data.split('\n') : [node.data];
      parts.forEach((t, i) => { if (i > 0) hardBreak(); if (t) ensure().runs.push({...base, text: t}); });
      return;
    }
    if (node.nodeType !== 1) return;
    const el = node;
    if (el.tagName === 'BR') { hardBreak(); return; }
    if (el !== root && el.matches(SKIP)) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none') return;
    const block = el !== root && BLOCK.has(cs.display);
    if (block) { cur = null; stack.push(el); }
    for (const ch of el.childNodes) visit(ch);
    if (block) { stack.pop(); cur = null; }
  };
  visit(root);
  const out = [];
  for (const p of paras) {
    let prevSpace = true;  // drops leading whitespace of the paragraph
    for (const r of p.runs) {
      let t = r.text;
      if (r.collapse) { t = t.replace(/[ \t\n\r\f]+/g, ' '); if (prevSpace) t = t.replace(/^ /, ''); }
      r.text = t; if (t) prevSpace = r.collapse && t.endsWith(' ');
    }
    for (let i = p.runs.length - 1; i >= 0; i--) {
      const r = p.runs[i]; if (!r.collapse) break;
      r.text = r.text.replace(/ +$/, ''); if (r.text) break;
    }
    p.runs = p.runs.filter(r => r.text).map(r => { const {collapse, transform: tm, ...rest} = r;
      return {...rest, text: transform(r.text, tm)}; });
    if (p.runs.length || p.br) out.push(p);
  }
  return out;
}

function rel(r, S) { return {x: r.left - S.left, y: r.top - S.top, w: r.width, h: r.height}; }
function frameOf(el, slide, S, bg) {
  const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
  const l = num(cs.borderLeftWidth) + num(cs.paddingLeft), t = num(cs.borderTopWidth) + num(cs.paddingTop);
  const rr = num(cs.borderRightWidth) + num(cs.paddingRight), b = num(cs.borderBottomWidth) + num(cs.paddingBottom);
  const paras = buildParas(el, slide, bg);
  const maxLh = Math.max(0, ...paras.map(p => p.lineHeight));
  const h = r.height - t - b;
  return {x: r.left - S.left + l, y: r.top - S.top + t, w: r.width - l - rr, h, paras,
          single: paras.length <= 1 && h < 1.5 * maxLh,
          label: (el.tagName.toLowerCase() + (el.classList[0] ? '.' + el.classList[0] : ''))};
}
function radiusOf(v, w, h) {
  const first = (v || '0').split(' ')[0];
  return first.endsWith('%') ? num(first) / 100 * Math.min(w, h) : num(first);
}
function shapeOf(el, cs, slide, S, bg) {
  const fillC = color(cs.backgroundColor);
  const fill = fillC[3] > 0 ? opaque(fillC, el, slide, bg, el.parentElement) : null;
  const sides = ['Top', 'Right', 'Bottom', 'Left'].map(s => {
    const w = num(cs['border' + s + 'Width']), st = cs['border' + s + 'Style'], c = color(cs['border' + s + 'Color']);
    const on = w > 0 && st !== 'none' && st !== 'hidden' && c[3] > 0;
    return {on, w, style: st, c: on ? opaque(c, el, slide, bg, el.parentElement) : null};
  });
  if (!fill && !sides.some(s => s.on)) return null;
  const r = rel(el.getBoundingClientRect(), S);
  const uniform = sides.every(s => s.on && s.w === sides[0].w && s.style === sides[0].style && String(s.c) === String(sides[0].c));
  return {...r, fill, radius: radiusOf(cs.borderTopLeftRadius, r.w, r.h),
          border: uniform ? {w: sides[0].w, color: sides[0].c, style: sides[0].style} : null,
          sides: uniform ? [] : sides.filter(s => s.on).map((s, i) => ({side: ['Top','Right','Bottom','Left'][sides.indexOf(s)], w: s.w, color: s.c}))};
}

window.__pptx = {
  state: {},
  slides() { return [...document.querySelectorAll('section.slide')]; },
  styles() {
    return [...document.querySelectorAll('style')].map(s => s.textContent).join('\n') + '\n' +
      [...document.querySelectorAll('link[rel~="stylesheet"]')].map(l => l.href).join('\n');
  },
  fontsAvailable(fams) {  // canvas width probe against two generic fallbacks
    const probe = 'mmmmmmmmmmlli1WQ@#';
    const width = f => { cx.font = '72px ' + f; return cx.measureText(probe).width; };
    const out = {};
    for (const f of fams) {
      const q = '"' + f.replace(/"/g, '') + '"';
      out[f] = width(q + ', monospace') !== width('monospace') || width(q + ', serif') !== width('serif');
    }
    return out;
  },
  analyze(idx) {
    const slide = this.slides()[idx];
    const S = slide.getBoundingClientRect(); const scs = getComputedStyle(slide);
    const sc = color(scs.backgroundColor);
    const bg = sc[3] >= 0.999 ? sc.slice(0, 3).map(Math.round) : mix(sc, sc[3], [255, 255, 255]);
    const tier = slide.getAttribute('data-pptx');
    const explicit = !!slide.querySelector('[data-pptx-text]');
    const all = [...slide.querySelectorAll('*')];

    // Text elements
    const sel = []; const selSet = new Set();
    const inSel = el => { for (let a = el; a && a !== slide; a = a.parentElement) if (selSet.has(a)) return true; return false; };
    for (const el of all) {
      if (el.closest(EXCL)) continue;
      if (!rendered(el) || (el.parentElement && inSel(el.parentElement))) continue;
      if (explicit ? !el.hasAttribute('data-pptx-text') : !isTextRoot(el)) continue;
      sel.push(el); selSet.add(el);
    }
    const frames = sel.map(el => frameOf(el, slide, S, bg)).filter(f => f.paras.some(p => p.runs.length));
    this.state[idx] = {textEls: sel};

    // Semantic layer: shapes (+ box pictures for background-image), pictures
    const layer0 = [], pics = []; let n = 0, pseudo = 0, lost = 0;
    const pic = (el, mode) => {
      const u = idx + '-' + (n++); el.setAttribute('data-pptx-uid', u);
      const title = el.tagName.toLowerCase() === 'svg' ? el.querySelector(':scope > title') : null;
      const alt = el.getAttribute('alt') || el.getAttribute('aria-label') || el.getAttribute('data-alt') ||
                  (title ? title.textContent.trim() : '') || '';
      return {kind: 'pic', uid: u, mode, alt, ...rel(el.getBoundingClientRect(), S)};
    };
    if (tier === 'semantic') {
      for (const el of all) {
        if (el.closest('aside.speaker-notes, script, style, noscript, template')) continue;
        const lock = el.closest('[data-pptx-lock]');
        if (lock) { if (lock === el && rendered(el)) pics.push(pic(el, 'full')); continue; }
        const par = el.parentElement;
        if (par && par.closest('svg, [data-pptx-image]')) continue;
        if (!rendered(el)) continue;
        const cs = getComputedStyle(el);
        if (el.matches(PICTURE_TAGS)) { if (cs.visibility === 'visible') pics.push(pic(el, 'full')); continue; }
        if (cs.visibility !== 'visible') continue;
        for (const ps of ['::before', '::after']) {
          const p = getComputedStyle(el, ps);
          if (p.content && p.content !== 'none' && p.content !== 'normal' && p.display !== 'none') pseudo++;
        }
        if (cs.backgroundImage && cs.backgroundImage !== 'none') { layer0.push(pic(el, 'box')); continue; }
        const s = shapeOf(el, cs, slide, S, bg);
        if (s) layer0.push({kind: 'shape', ...s});
      }
      const tw = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
      for (let t = tw.nextNode(); t; t = tw.nextNode()) {
        const p = t.parentElement;
        if (!/\S/.test(t.data) || p.closest(EXCL + ', [data-pptx-image]') || inSel(p)) continue;
        if (rendered(p) && getComputedStyle(p).visibility === 'visible') lost++;
      }
    }
    const notes = [...slide.querySelectorAll('aside.speaker-notes')].map(a => {
      const ps = a.querySelectorAll('p, li');
      const parts = ps.length ? [...ps].map(p => p.textContent) : [a.textContent];
      return parts.map(s => s.replace(/\s+/g, ' ').trim()).filter(Boolean).join('\n');
    }).filter(Boolean).join('\n\n');
    return {id: slide.getAttribute('data-slide-id') || '', tier, explicit, w: S.width, h: S.height, bg,
            frames, layer0, pics, notes, pseudo, lost};
  },
  // Hybrid: make selected text transparent, freezing everything that would
  // otherwise follow currentColor (borders, fills, pseudo bullets, locked/svg content).
  hide(idx) {
    const st = this.state[idx]; const recs = []; const rules = []; let k = 0;
    const FREEZE = ['background-color', 'border-top-color', 'border-right-color', 'border-bottom-color',
                    'border-left-color', 'outline-color', 'box-shadow', 'column-rule-color', 'fill', 'stroke'];
    for (const root of st.textEls) {
      for (const e of [root, ...root.querySelectorAll('*')]) {
        const cs = getComputedStyle(e);
        const keep = !!(e.closest('[data-pptx-lock]') || e.closest('svg'));
        const props = {};
        for (const p of FREEZE) props[p] = cs.getPropertyValue(p);
        if (keep) { props['color'] = cs.color; props['-webkit-text-fill-color'] = cs.webkitTextFillColor; }
        else {
          Object.assign(props, {'color': 'transparent', '-webkit-text-fill-color': 'transparent',
                                'text-shadow': 'none', 'text-decoration-color': 'transparent'});
          for (const ps of ['::before', '::after', '::marker']) {
            const p = getComputedStyle(e, ps);
            if (ps !== '::marker' && (!p.content || p.content === 'none' || p.content === 'normal')) continue;
            if (ps === '::marker' && cs.display !== 'list-item') continue;
            if (!e.hasAttribute('data-pptx-ps')) e.setAttribute('data-pptx-ps', String(k++));
            const sel = '[data-pptx-ps="' + e.getAttribute('data-pptx-ps') + '"]' + ps;
            const decl = ['color', '-webkit-text-fill-color', ...(ps === '::marker' ? [] : FREEZE)]
              .map(q => q + ':' + (q === '-webkit-text-fill-color' ? p.webkitTextFillColor : p.getPropertyValue(q)) + ' !important').join(';');
            rules.push(sel + '{' + decl + '}');
          }
        }
        recs.push([e, e.getAttribute('style'), props]);
      }
    }
    for (const [e, , props] of recs) for (const [p, v] of Object.entries(props)) if (v) e.style.setProperty(p, v, 'important');
    const tag = document.createElement('style'); tag.textContent = rules.join('\n'); document.head.appendChild(tag);
    st.hidden = {recs, tag};
  },
  unhide(idx) {
    const h = this.state[idx].hidden; if (!h) return;
    for (const [e, orig] of h.recs.reverse()) { if (orig === null) e.removeAttribute('style'); else e.setAttribute('style', orig); }
    h.tag.remove(); document.querySelectorAll('[data-pptx-ps]').forEach(e => e.removeAttribute('data-pptx-ps'));
    this.state[idx].hidden = null;
  },
  isolate(uid, mode) {
    const el = document.querySelector('[data-pptx-uid="' + uid + '"]');
    el.classList.add(mode === 'box' ? '__pptx-box' : '__pptx-full');
    document.documentElement.classList.add('__pptx-iso');
  },
  unisolate() {
    document.documentElement.classList.remove('__pptx-iso');
    document.querySelectorAll('.__pptx-box, .__pptx-full').forEach(e => e.classList.remove('__pptx-box', '__pptx-full'));
  },
};
}
"""


# ----------------------------------------------------------------------------
# Render (single Playwright session)
# ----------------------------------------------------------------------------

def render(html: Path, build: Path, scale: float, use_cache: bool,
           global_warn: list[str]) -> list[dict[str, Any]]:
    """Measure every slide and produce its PNGs. Returns per-slide records."""
    cache_path = build / "cache.json"
    try:
        cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    except (OSError, ValueError):
        cache = {}
    if cache.get("version") != VERSION:
        cache = {"version": VERSION, "decks": {}}
    old = cache["decks"].get(html.name, {}) if use_cache else {}
    new: dict[str, Any] = {}
    stem = html.stem
    slides: list[dict[str, Any]] = []

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except PWError as e:
            if "Executable doesn't exist" in str(e) or "playwright install" in str(e):
                print(INSTALL_HINT)
                sys.exit(2)
            raise
        ctx = browser.new_context(viewport={"width": CANVAS_W, "height": CANVAS_H},
                                  device_scale_factor=scale)
        page = ctx.new_page()
        try:
            page.goto(html.as_uri(), wait_until="load", timeout=30000)
        except PWTimeout:
            global_warn.append("page 'load' timed out after 30s (remote assets?); continuing")
        page.add_style_tag(content=BASE_CSS)
        if not page.evaluate(FONTS_READY_JS):
            global_warn.append(f"document.fonts.ready not settled after {FONTS_TIMEOUT_MS // 1000}s; "
                               "measurements may use fallback fonts")
        page.evaluate("() => document.getAnimations().forEach(a => { try { a.finish(); } catch (e) {} })")
        page.evaluate(PAGE_JS)
        styles = page.evaluate("() => window.__pptx.styles()")
        count = page.evaluate("() => window.__pptx.slides().length")
        locators = page.locator("section.slide")

        for i in range(count):
            nn = f"{i + 1:02d}"
            outer = page.evaluate("i => window.__pptx.slides()[i].outerHTML", i)
            digest = hashlib.sha1("\0".join([VERSION, str(scale), styles, outer]).encode()).hexdigest()
            data = page.evaluate("i => window.__pptx.analyze(i)", i)
            data["index"] = i + 1
            data["id"] = data["id"] or f"slide-{nn}"
            data["warnings"] = warns = []
            tier = data["tier"]
            if tier is None:
                warns.append("no data-pptx attribute; treated as hybrid")
                tier = "hybrid"
            elif tier not in TIERS:
                warns.append(f"unknown data-pptx={tier!r}; treated as hybrid")
                tier = "hybrid"
            data["tier"] = tier
            if abs(data["w"] - CANVAS_W) > 0.5 or abs(data["h"] - CANVAS_H) > 0.5:
                warns.append(f"slide is {data['w']:g}x{data['h']:g}, expected 1920x1080")

            entry = old.get(str(i + 1))
            hit = bool(entry and entry.get("hash") == digest
                       and all((build / f).exists() for f in entry.get("files", [])))
            files: list[str] = []
            if tier in ("image", "hybrid"):
                name = f"{stem}-slide-{nn}.png"
                files.append(name)
                data["bg_png"] = str(build / name)
                if not hit:
                    if tier == "hybrid":
                        page.evaluate("i => window.__pptx.hide(i)", i)
                    try:
                        locators.nth(i).screenshot(path=str(build / name), animations="disabled")
                    finally:
                        if tier == "hybrid":
                            page.evaluate("i => window.__pptx.unhide(i)", i)
            else:
                for j, item in enumerate(data["layer0"] + data["pics"], start=1):
                    if item["kind"] != "pic":
                        continue
                    name = f"{stem}-slide-{nn}-pic-{j:02d}.png"
                    item["png"] = str(build / name)
                    if not hit:
                        page.evaluate("([u, m]) => window.__pptx.isolate(u, m)", [item["uid"], item["mode"]])
                        try:
                            page.locator(f'[data-pptx-uid="{item["uid"]}"]').screenshot(
                                path=item["png"], omit_background=True, animations="disabled", timeout=15000)
                        except PWError as e:
                            warns.append(f"could not render picture {item['uid']}: {str(e).splitlines()[0]}")
                            item["png"] = None
                        finally:
                            page.evaluate("() => window.__pptx.unisolate()")
                    if item["png"]:
                        files.append(name)
            data["cached"] = hit
            new[str(i + 1)] = {"hash": digest, "id": data["id"], "files": files}
            slides.append(data)

        fams = sorted({r["font"] for s in slides if s["tier"] != "image"
                       for f in s["frames"] for p in f["paras"] for r in p["runs"]})
        if fams:
            avail = page.evaluate("f => window.__pptx.fontsAvailable(f)", fams)
            missing = [f for f, ok in avail.items() if not ok]
            if missing:
                global_warn.append("fonts not available to Chromium (text measured with a fallback): "
                                   + ", ".join(missing))
        browser.close()

    cache["decks"][html.name] = new
    cache_path.write_text(json.dumps(cache, indent=1))
    return slides


# ----------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------

def emu(px: float) -> int:
    return int(round(px * EMU_PER_PX))


def rgb(c: list[int]) -> RGBColor:
    return RGBColor(*(max(0, min(255, int(v))) for v in c[:3]))


def clamp_box(x: float, y: float, w: float, h: float) -> tuple[float, float, float, float] | None:
    x0, y0 = max(0.0, x), max(0.0, y)
    x1, y1 = min(float(CANVAS_W), x + w), min(float(CANVAS_H), y + h)
    if x1 - x0 < 0.5 or y1 - y0 < 0.5:
        return None
    return x0, y0, x1 - x0, y1 - y0


def is_mono(font: str) -> bool:
    return "plex mono" in font.lower()


def add_shape(shapes, s: dict[str, Any]) -> int:
    """Rectangle / rounded rectangle for a CSS box. Returns shapes added."""
    added = 0
    b = s["border"]
    inset = b["w"] / 2 if b else 0.0  # PowerPoint strokes are centered on the edge
    box = clamp_box(s["x"] + inset, s["y"] + inset, s["w"] - 2 * inset, s["h"] - 2 * inset)
    if box and (s["fill"] or b):
        x, y, w, h = box
        radius = max(0.0, min(s["radius"] - inset, w / 2, h / 2))
        kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius > 0.25 else MSO_SHAPE.RECTANGLE
        shp = shapes.add_shape(kind, Emu(emu(x)), Emu(emu(y)), Emu(emu(w)), Emu(emu(h)))
        shp.name = "box"
        if kind == MSO_SHAPE.ROUNDED_RECTANGLE:
            shp.adjustments[0] = min(0.5, radius / min(w, h))
        if s["fill"]:
            shp.fill.solid()
            shp.fill.fore_color.rgb = rgb(s["fill"])
        else:
            shp.fill.background()
        if b:
            shp.line.width = Emu(max(MIN_LINE_EMU, emu(b["w"])))
            shp.line.color.rgb = rgb(b["color"])
            if b["style"] in DASH:
                shp.line.dash_style = DASH[b["style"]]
        else:
            shp.line.fill.background()
        added += 1
    for side in s["sides"]:  # non-uniform borders -> thin filled bars
        w_px = side["w"]
        x, y, w, h = s["x"], s["y"], s["w"], s["h"]
        geo = {"Top": (x, y, w, w_px), "Bottom": (x, y + h - w_px, w, w_px),
               "Left": (x, y, w_px, h), "Right": (x + w - w_px, y, w_px, h)}[side["side"]]
        box = clamp_box(*geo)
        if not box:
            continue
        bx, by, bw, bh = box
        bar = shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(emu(bx)), Emu(emu(by)),
                               Emu(max(emu(bw), MIN_LINE_EMU if bw < bh else 1)),
                               Emu(max(emu(bh), MIN_LINE_EMU if bh <= bw else 1)))
        bar.name = f"border-{side['side'].lower()}"
        bar.fill.solid()
        bar.fill.fore_color.rgb = rgb(side["color"])
        bar.line.fill.background()
        added += 1
    return added


def add_picture(shapes, item: dict[str, Any]) -> bool:
    path = item.get("png")
    if not path:
        return False
    with Image.open(path) as im:
        if im.mode in ("RGBA", "LA") and im.getchannel("A").getbbox() is None:
            return False  # nothing visible
    pic = shapes.add_picture(path, Emu(emu(item["x"])), Emu(emu(item["y"])),
                             Emu(max(1, emu(item["w"]))), Emu(max(1, emu(item["h"]))))
    pic.name = "picture"
    if item.get("alt"):
        pic._element.nvPicPr.cNvPr.set("descr", item["alt"])
    return True


def add_text_frame(shapes, f: dict[str, Any]) -> bool:
    x, y, w, h = f["x"], f["y"], f["w"], max(f["h"], 1.0)
    align = f["paras"][0]["align"] if f["paras"] else "left"
    if f["single"]:  # leave room for font-substitution width drift
        slack = w * 0.02
        x -= slack / 2 if align in ("center", "-webkit-center") else (slack if align in ("right", "end") else 0)
        w += slack
    box = clamp_box(x, y, w, h)
    if not box:
        return False
    x, y, w, h = box
    tb = shapes.add_textbox(Emu(emu(x)), Emu(emu(y)), Emu(emu(w)), Emu(emu(h)))
    first_text = next((r["text"] for p in f["paras"] for r in p["runs"]), "")
    tb.name = f"text: {first_text[:40]}"
    tf = tb.text_frame
    tf.word_wrap = not f["single"]
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for k, para in enumerate(f["paras"]):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = ALIGN.get(para["align"], PP_ALIGN.LEFT)
        p.line_spacing = Pt(para["lineHeight"] * PT_PER_PX)
        if not para["runs"]:
            p.font.size = Pt(para["fontSize"] * PT_PER_PX)
        for run in para["runs"]:
            r = p.add_run()
            r.text = run["text"]
            font = r.font
            mono = is_mono(run["font"])
            font.name = run["font"]
            font.size = Pt(run["size"] * PT_PER_PX)
            font.bold = run["weight"] >= 600 and not mono and "geist" not in run["font"].lower()
            font.italic = False
            font.color.rgb = rgb(run["color"])
            spc = 0 if mono else run["ls"] * PT_PER_PX * 100
            if run["size"] < BRAND_FLOOR_PX and spc < 0:
                spc = 0
            r._r.get_or_add_rPr().set("spc", str(int(round(spc))))
    return True


def strip_effects(prs) -> None:
    """No shadows anywhere: drop theme style refs and any effect lists."""
    for slide in prs.slides:
        for shape in slide.shapes:
            el = shape._element
            style = el.find(qn("p:style"))
            if style is not None:
                el.remove(style)
            for eff in list(el.iter(qn("a:effectLst"))):
                eff.getparent().remove(eff)


def build(slides: list[dict[str, Any]], out: Path) -> None:
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(SLIDE_W_EMU), Emu(SLIDE_H_EMU)
    blank = prs.slide_layouts[6]
    for s in slides:
        slide = prs.slides.add_slide(blank)
        shapes = slide.shapes
        s["n_frames"] = s["n_pics"] = s["n_shapes"] = 0
        if s["tier"] in ("image", "hybrid"):
            bg = shapes.add_picture(s["bg_png"], 0, 0, prs.slide_width, prs.slide_height)
            bg.name = "background"
            bg._element.nvPicPr.cNvPr.set("descr", f"Slide {s['index']:02d} background")
        else:
            slide.background.fill.solid()
            slide.background.fill.fore_color.rgb = rgb(s["bg"])
            empty = 0
            for item in s["layer0"]:
                if item["kind"] == "shape":
                    s["n_shapes"] += add_shape(shapes, item)
                elif add_picture(shapes, item):
                    s["n_pics"] += 1
                else:
                    empty += 1
            for item in s["pics"]:
                if add_picture(shapes, item):
                    s["n_pics"] += 1
                else:
                    empty += 1
            if empty:
                s["warnings"].append(f"{empty} picture(s) rendered empty or failed; skipped")
        if s["tier"] != "image":
            for f in s["frames"]:
                s["n_frames"] += add_text_frame(shapes, f)
        if s["notes"]:
            slide.notes_slide.notes_text_frame.text = s["notes"]
    strip_effects(prs)
    prs.save(str(out))


# ----------------------------------------------------------------------------
# Warnings + CLI
# ----------------------------------------------------------------------------

def collect_text_warnings(s: dict[str, Any]) -> None:
    if s["tier"] == "image":
        return
    small, italic = [], 0
    for f in s["frames"]:
        for p in f["paras"]:
            for r in p["runs"]:
                if r["size"] < BRAND_FLOOR_PX and not r["footer"]:
                    small.append(r)
                italic += bool(r["italic"])
    if small:
        smallest = min(small, key=lambda r: r["size"])
        s["warnings"].append(f"{len(small)} run(s) under {BRAND_FLOOR_PX}px (smallest {smallest['size']:g}px: "
                             f"{smallest['text'][:30]!r})")
    if italic:
        s["warnings"].append(f"{italic} italic run(s); written upright (brand: no italic)")
    if s["tier"] == "semantic":
        if s["pseudo"]:
            s["warnings"].append(f"{s['pseudo']} ::before/::after decoration(s) not exported on semantic tier")
        if s["lost"]:
            what = "outside [data-pptx-text]" if s["explicit"] else "not captured"
            s["warnings"].append(f"{s['lost']} visible text node(s) {what}; missing from the slide")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build an editable .pptx from a Metafore HTML deck.")
    ap.add_argument("html", type=Path, help="self-contained deck HTML (1920x1080 section.slide elements)")
    ap.add_argument("--out", type=Path, help="output .pptx (default: next to the HTML, same basename)")
    ap.add_argument("--build-dir", default="_build", help="render dir, relative to the HTML's folder (default _build)")
    ap.add_argument("--no-cache", action="store_true", help="re-render every slide")
    ap.add_argument("--scale", type=float, default=2, help="screenshot device scale factor (default 2)")
    args = ap.parse_args(argv)

    html = args.html.resolve()
    if not html.is_file():
        print(f"error: {html} not found")
        return 1
    out = args.out.resolve() if args.out else html.with_suffix(".pptx")
    build_dir = Path(args.build_dir)
    if not build_dir.is_absolute():
        build_dir = html.parent / build_dir
    build_dir.mkdir(parents=True, exist_ok=True)

    global_warn: list[str] = []
    slides = render(html, build_dir, args.scale, not args.no_cache, global_warn)
    if not slides:
        print('error: no <section class="slide"> elements found')
        return 1
    build(slides, out)

    for w in global_warn:
        print(f"! {w}")
    id_w = max(len(s["id"]) for s in slides)
    for s in slides:
        collect_text_warnings(s)
        extra = f" shapes={s['n_shapes']}" if s["tier"] == "semantic" else ""
        cached = "  (cached)" if s["cached"] else ""
        print(f"{s['index']:02d} {s['tier']:<8} {s['id']:<{id_w}}  frames={s['n_frames']} "
              f"pictures={s['n_pics']}{extra}{cached}")
        for w in s["warnings"]:
            print(f"   ! {w}")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
