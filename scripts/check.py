#!/usr/bin/env python3
"""check.py — programmatic Metafore brand + layout lint, with an optional contact sheet.

Usage:
    python3 check.py page.html --kind deck|brochure|graphic|dashboard [--sheet sheet.png] [--zoom N] [--json]
    python3 check.py doc.docx [--json]

Opens the HTML once in headless Chromium (deck 1920x1080, brochure 1440 wide,
graphic = outer fixed-size frame, dashboard 1440x900), runs type-floor,
paragraph-length, overflow, overlap, positioning, visual-presence, color,
voice and deck-structure checks per unit (slide / section / frame / card).

  --sheet PATH   one PNG contact sheet of all units (errors outlined red); <=1600 wide,
                 split into PATH-1.png, PATH-2.png ... if taller than 2000
  --zoom N       also write <name>.unit-NN.png for unit N (<=1600 longest edge)
  --json         machine-readable output

Exit: 0 = no errors, 1 = errors found, 2 = usage / missing dependency.
No PNG written by this script exceeds 2000px on either edge.
"""
import argparse
import json
import re
import sys
import zipfile
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIP_HINT = "pip install playwright pillow && python3 -m playwright install chromium"
MAX_LINES = 40

RETIRED = {"#00989E": (0, 152, 158), "#00C4CC": (0, 196, 204)}
RE_RETIRED_SRC = re.compile(r"#(00989E|00C4CC)\b|rgba?\(\s*0\s*,\s*(152|196)\s*,\s*(158|204)\s*[,)]", re.I)

VIEWPORTS = {"deck": (1920, 1080), "brochure": (1440, 900), "graphic": (1920, 1080), "dashboard": (1440, 900)}
UNIT_LABEL = {"deck": "slide", "brochure": "sect", "graphic": "frame", "dashboard": "card", "docx": "sect"}


def need(mods):
    try:
        for m in mods:
            __import__(m)
    except ImportError:
        print(f"missing dependency ({m}): " + ("pip install python-docx" if m == "docx" else PIP_HINT))
        sys.exit(2)


# --------------------------------------------------------------------------- shared JS
FIND_FRAME_JS = r"""
() => {
  const bad = /%|auto|vw|vh|fit|min-content|max-content/;
  const ruleSizes = new Map();
  const walk = (rs) => { for (const r of rs) {
    if (r.cssRules && !r.selectorText) { walk(r.cssRules); continue; }
    if (!r.selectorText || !(r.style.width || r.style.height)) continue;
    let els; try { els = document.querySelectorAll(r.selectorText); } catch (e) { continue; }
    for (const el of els) { const o = ruleSizes.get(el) || {}; if (r.style.width) o.w = r.style.width;
      if (r.style.height) o.h = r.style.height; ruleSizes.set(el, o); }
  } };
  for (const sh of document.styleSheets) { try { walk(sh.cssRules); } catch (e) {} }
  const explicit = (el) => {
    if (el.hasAttribute('data-frame')) return true;
    if (el instanceof SVGElement || el.tagName === 'IMG' || el.tagName === 'CANVAS') return false;
    const o = ruleSizes.get(el) || {};
    const w = el.style.width || o.w || '', h = el.style.height || o.h || '';
    if (!w || !h || bad.test(w) || bad.test(h)) return false;
    const r = el.getBoundingClientRect();
    return r.width >= 40 && r.height >= 40;
  };
  document.querySelectorAll('[data-mf-frame]').forEach(e => e.removeAttribute('data-mf-frame'));
  let queue = [...document.body.children], found = null;
  const df = document.querySelector('[data-frame]');
  if (df) found = df;
  while (!found && queue.length) {
    const next = [];
    for (const el of queue) { if (explicit(el)) { found = el; break; } next.push(...el.children); }
    queue = next;
  }
  if (!found) return null;
  found.setAttribute('data-mf-frame', '1');
  const r = found.getBoundingClientRect();
  return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height};
}
"""

FONTS_READY_JS = """
async (ms) => {
  await Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, ms))]);
  const fams = new Set(); let loaded = 0;
  document.fonts.forEach(f => { fams.add(f.family.replace(/['"]/g, '')); if (f.status === 'loaded') loaded++; });
  return {families: [...fams], loaded};
}
"""

CHECK_JS = r"""
(args) => {
  const {kind} = args;
  const CHROME = '.section-label, .deck-footer, .icon-tr, .logo-tl, .logo, [data-chrome]';
  const BRAND_FONTS = ['geist', 'inter', 'ibm plex mono'];
  const SKIP = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'TITLE', 'HEAD']);
  const BLOCK = /^(block|flex|grid|list-item|table|table-row|table-cell|flow-root|inline-block|inline-flex|inline-grid)$/;
  const F = [];
  const csCache = new Map();
  const cs = (el) => { let c = csCache.get(el); if (!c) { c = getComputedStyle(el); csCache.set(el, c); } return c; };
  const visCache = new Map();
  const visible = (el) => {
    if (!el || el.nodeType !== 1) return true;
    if (visCache.has(el)) return visCache.get(el);
    const c = cs(el);
    let v = !(c.display === 'none' || c.visibility === 'hidden' || c.visibility === 'collapse' || parseFloat(c.opacity) === 0);
    if (v && el.parentElement) v = visible(el.parentElement);
    visCache.set(el, v); return v;
  };
  const snip = (t, n = 40) => { t = (t || '').replace(/\s+/g, ' ').trim(); return t.length > n ? t.slice(0, n - 1) + '…' : t; };
  const desc = (el) => {
    if (el.id) return '#' + el.id;
    const cl = [...(el.classList || [])].filter(c => !c.startsWith('mf-')).slice(0, 2);
    return cl.length ? '.' + cl.join('.') : el.tagName.toLowerCase();
  };
  const selOf = (el, root) => {
    const d = desc(el);
    let p = el.parentElement;
    for (let i = 0; p && p !== root && i < 4; i++, p = p.parentElement) {
      if (p.classList && p.classList.length || p.id) return desc(p) + ' ' + d;
    }
    return d;
  };
  const firstFam = (ff) => (ff.split(',')[0] || '').replace(/['"]/g, '').trim().toLowerCase();
  const rgb = (s) => { const m = (s || '').match(/rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+%?))?/);
    if (!m) return null; let a = m[4] === undefined ? 1 : (m[4].endsWith('%') ? parseFloat(m[4]) / 100 : parseFloat(m[4]));
    return [Math.round(+m[1]), Math.round(+m[2]), Math.round(+m[3]), a]; };
  const RET = {'0,152,158': '#00989E', '0,196,204': '#00C4CC'};
  const retired = (s) => { const c = rgb(s); if (!c || c[3] === 0) return null; return RET[c.slice(0, 3).join(',')] || null; };

  // ---------- units
  let units = [];
  if (kind === 'deck') units = [...document.querySelectorAll('section.slide')];
  else if (kind === 'brochure') { const all = [...document.querySelectorAll('section, .section')];
    units = all.filter(e => !all.some(o => o !== e && o.contains(e))); }
  else if (kind === 'graphic') { const f = document.querySelector('[data-mf-frame]'); units = [f || document.body]; }
  else if (kind === 'dashboard') { let all = [...document.querySelectorAll('.card, [data-unit]')];
    all = all.filter(e => !all.some(o => o !== e && o.contains(e)));
    units = all.length ? all : [document.querySelector('main') || document.body]; }
  const uIndex = new Map(units.map((u, i) => [u, i]));
  const unitOf = (el) => { for (let e = el; e; e = e.parentElement) if (uIndex.has(e)) return uIndex.get(e); return -1; };
  const add = (u, lvl, chk, key, extra = '') => F.push({u, lvl, chk, key, extra});

  // ---------- text owners (elements with direct visible text)
  const owners = new Map();
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = tw.nextNode(); n; n = tw.nextNode()) {
    if (!n.nodeValue.trim()) continue;
    const el = n.parentElement; if (!el) continue;
    let skip = false; for (let e = el; e; e = e.parentElement) if (SKIP.has(e.tagName)) { skip = true; break; }
    if (skip || !visible(el)) continue;
    const rg = document.createRange(); rg.selectNodeContents(n);
    const rects = [...rg.getClientRects()].filter(r => r.width > 1 && r.height > 1);
    if (!rects.length) continue;
    let o = owners.get(el);
    if (!o) { o = {el, rects: [], text: ''}; owners.set(el, o); }
    o.rects.push(...rects); o.text += n.nodeValue;
  }
  const lineH = (el) => { const c = cs(el); const lh = parseFloat(c.lineHeight); return isNaN(lh) ? parseFloat(c.fontSize) * 1.2 : lh; };
  for (const o of owners.values()) {
    const el = o.el, c = cs(el);
    o.inSvg = el instanceof SVGElement;
    let fs = parseFloat(c.fontSize);
    if (o.inSvg && el.getScreenCTM) { const m = el.getScreenCTM(); if (m) fs *= Math.hypot(m.a, m.b); }
    o.fs = Math.round(fs * 10) / 10;
    o.u = unitOf(el);
    o.root = o.u >= 0 ? units[o.u] : document.body;
    o.chrome = !!el.closest(CHROME);
    o.footer = !!el.closest('.deck-footer');
    o.decor = o.inSvg || !!el.closest('[data-decorative]');
    const letters = o.text.replace(/[^A-Za-z]/g, '');
    o.label = firstFam(c.fontFamily).includes('mono') || c.textTransform === 'uppercase' ||
              (letters.length >= 4 && letters === letters.toUpperCase());
    o.body = !!el.closest('p, li');
    o.bodyish = o.body || [0, 1, 2].some(i => { let e = el; for (let k = 0; k < i && e; k++) e = e.parentElement;
      return e && /body|desc|lede/i.test(e.className && e.className.baseVal !== undefined ? e.className.baseVal : (e.className || '')); });
    // clamp rects vertically to the line-height so tight leading doesn't read as overlap
    const lh = lineH(el);
    o.boxes = o.rects.map(r => { const h = Math.min(r.height, o.inSvg ? r.height : lh); const t = r.top + (r.height - h) / 2;
      return {l: r.left, r: r.right, t, b: t + h}; });
  }
  const ownerList = [...owners.values()];

  // ---------- type floor
  for (const o of ownerList) {
    const fs = o.fs, s = selOf(o.el, o.root), t = `"${snip(o.text)}"`;
    const k = `${s} ${fs}px`;
    if (o.decor) { const lim = kind === 'deck' ? 16 : 12; if (fs < lim - 0.05) add(o.u, 'WARN', 'type-floor', k + ' (svg/decorative)', t); continue; }
    if (kind === 'deck') {
      if (fs < 21.95) add(o.u, 'ERROR', 'type-floor', k, t);
      else if (o.label && !o.footer && fs < 23.95) add(o.u, 'WARN', 'type-floor', k + ' label<24', t);
    } else if (kind === 'brochure' || kind === 'graphic') {
      if (o.label && fs < 12.95) add(o.u, 'ERROR', 'type-floor', k + ' label<13', t);
      else if (!o.label && fs < 14.95) add(o.u, 'ERROR', 'type-floor', k, t);
      else if (!o.label && kind === 'brochure' && o.body && fs < 17.95) add(o.u, 'WARN', 'type-floor', k + ' body<18', t);
      else if (!o.label && kind === 'graphic' && o.bodyish && fs < 15.95) add(o.u, 'WARN', 'type-floor', k + ' body<16', t);
    } else if (kind === 'dashboard') {
      if (fs < 13.95) add(o.u, 'ERROR', 'type-floor', k, t);
      else if (!o.label && !o.chrome && fs < 15.95) add(o.u, 'WARN', 'type-floor', k + ' content<16', t);
    }
  }

  // ---------- leaf blocks (block boxes with no block descendants)
  const isBlock = (el) => BLOCK.test(cs(el).display);
  const leafOf = new Map();
  const leafFor = (el) => {
    if (el instanceof SVGElement) return el;
    for (let e = el; e && e !== document.body; e = e.parentElement) {
      if (!isBlock(e)) continue;
      if (leafOf.has(e)) return leafOf.get(e) ? e : el;
      const leaf = ![...e.querySelectorAll('*')].some(d => !(d instanceof SVGElement) && isBlock(d) && visible(d) && d.textContent.trim());
      leafOf.set(e, leaf); return leaf ? e : el;
    }
    return el;
  };
  const leaves = new Set(ownerList.map(o => leafFor(o.el)));

  // ---------- paragraph length / word count
  for (const el of leaves) {
    if (el instanceof SVGElement || el.closest(CHROME)) continue;
    const u = unitOf(el), root = u >= 0 ? units[u] : document.body;
    const txt = el.textContent.replace(/\s+/g, ' ').trim();
    if (el.closest('[data-allow-long]')) continue;
    const words = txt.split(' ').filter(w => /\w/.test(w)).length;
    if (words > 60) add(u, 'WARN', 'word-count', `${selOf(el, root)} ${words} words`, `"${snip(txt)}"`);
    const cand = el.matches('p, li') || /body|lede|desc/i.test(typeof el.className === 'string' ? el.className : '');
    if (!cand || el.closest('blockquote, [class*="quote"]')) continue;
    const rg = document.createRange(); rg.selectNodeContents(el);
    const fs = parseFloat(cs(el).fontSize);
    const mids = [...rg.getClientRects()].filter(r => r.width > 1 && r.height > 1).map(r => (r.top + r.bottom) / 2).sort((a, b) => a - b);
    let lines = 0, last = -1e9;
    for (const m of mids) { if (m - last > fs * 0.5) { lines++; last = m; } }
    if (lines > 3) add(u, 'ERROR', 'para-length', `${selOf(el, root)} ${lines} lines`, `"${snip(txt)}"`);
  }

  // ---------- overflow: clipped content
  const allEls = [...document.body.querySelectorAll('*')];
  for (const el of allEls) {
    if (el instanceof SVGElement || uIndex.has(el) || SKIP.has(el.tagName) || !visible(el)) continue;
    const c = cs(el);
    if (c.overflowX === 'visible' && c.overflowY === 'visible') continue;
    if (el.clientWidth <= 1 || el.clientHeight <= 1) continue;
    if (!el.textContent.trim()) continue;
    const dy = el.scrollHeight - el.clientHeight, dx = el.scrollWidth - el.clientWidth;
    const clipY = dy > 1 && c.overflowY !== 'visible', clipX = dx > 1 && c.overflowX !== 'visible';
    if (!clipY && !clipX) continue;
    const scroll = /auto|scroll/.test(c.overflowX + c.overflowY);
    const u = unitOf(el);
    add(u, scroll && kind === 'dashboard' ? 'WARN' : 'ERROR', 'overflow',
        `${selOf(el, u >= 0 ? units[u] : document.body)} clipped ${clipY ? dy + 'px tall' : ''}${clipY && clipX ? ', ' : ''}${clipX ? dx + 'px wide' : ''}`, `"${snip(el.textContent)}"`);
  }
  // ---------- overflow: text outside its unit
  for (const o of ownerList) {
    if (o.u < 0 || o.decor) continue;
    const R = units[o.u].getBoundingClientRect();
    let d = '';
    for (const b of o.boxes) {
      if (b.r > R.right + 1) d = `right ${Math.round(b.r - R.right)}px`;
      else if (b.l < R.left - 1) d = `left ${Math.round(R.left - b.l)}px`;
      else if (b.b > R.bottom + 1) d = `bottom ${Math.round(b.b - R.bottom)}px`;
      else if (b.t < R.top - 1) d = `top ${Math.round(R.top - b.t)}px`;
      if (d) break;
    }
    if (d) add(o.u, 'ERROR', 'overflow', `${selOf(o.el, o.root)} text outside ${kind === 'deck' ? 'slide' : 'unit'} (${d})`, `"${snip(o.text)}"`);
  }
  // ---------- heading orphan
  for (const h of document.querySelectorAll('h1, h2, h3')) {
    if (!visible(h) || h.querySelector('.line')) continue;   // deliberate line-by-line headings
    const words = [];
    const w2 = document.createTreeWalker(h, NodeFilter.SHOW_TEXT);
    for (let n = w2.nextNode(); n; n = w2.nextNode()) {
      const re = /\S+/g; let m;
      while ((m = re.exec(n.nodeValue))) { const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
        const r = rg.getBoundingClientRect(); if (r.width > 0) words.push({w: m[0], y: (r.top + r.bottom) / 2}); }
    }
    if (words.length < 2) continue;
    const fs = parseFloat(cs(h).fontSize); const lines = [];
    for (const w of words) { const L = lines.find(l => Math.abs(l.y - w.y) < fs * 0.5); if (L) L.n.push(w.w); else lines.push({y: w.y, n: [w.w]}); }
    lines.sort((a, b) => a.y - b.y);
    if (lines.length >= 2 && lines[lines.length - 1].n.length === 1) {
      const u = unitOf(h); add(u, 'WARN', 'orphan', `${selOf(h, u >= 0 ? units[u] : document.body)} last line "${lines[lines.length - 1].n[0]}"`, `"${snip(h.textContent)}"`);
    }
  }
  // ---------- overlap
  const groups = new Map();
  for (const o of ownerList) { if (o.inSvg || o.decor) continue; if (!groups.has(o.u)) groups.set(o.u, []); groups.get(o.u).push(o); }
  for (const [u, list] of groups) {
    for (let i = 0; i < list.length; i++) for (let j = i + 1; j < list.length; j++) {
      const A = list[i], B = list[j];
      if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
      let best = null;
      for (const a of A.boxes) for (const b of B.boxes) {
        const w = Math.min(a.r, b.r) - Math.max(a.l, b.l), h = Math.min(a.b, b.b) - Math.max(a.t, b.t);
        if (w > 2 && h > 2 && (!best || w * h > best[0] * best[1])) best = [w, h];
      }
      if (best) add(u, 'ERROR', 'overlap', `text overlaps text: ${selOf(A.el, A.root)} × ${selOf(B.el, B.root)} (${Math.round(best[0])}×${Math.round(best[1])}px)`, `"${snip(A.text, 28)}"`);
    }
  }
  // ---------- absolute positioning
  const absSeen = new Set();
  for (const o of ownerList) {
    if (o.inSvg || o.chrome) continue;
    const stop = o.u >= 0 ? units[o.u] : document.body;
    for (let e = o.el; e && e !== stop && e !== document.body; e = e.parentElement) {
      const p = cs(e).position;
      if (p === 'absolute' || p === 'fixed') {
        if (!absSeen.has(e) && !e.closest(CHROME)) { absSeen.add(e);
          add(o.u, 'WARN', 'absolute', `${selOf(e, stop)} position:${p} on text — use flex/grid with gaps`, `"${snip(e.textContent)}"`); }
        break;
      }
    }
  }
  // ---------- visual presence
  const isVisual = (el) => {
    if (!visible(el) || el.closest(CHROME)) return false;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false;
    if (el.tagName.toLowerCase() === 'svg') { if (el.parentElement && el.parentElement.closest('svg')) return false; return r.width >= 48 || r.height >= 48; }
    if (el.hasAttribute('data-visual') || el.hasAttribute('data-pptx-lock')) return true;   // locked mockups (UI cards) are visuals
    if (['IMG', 'CANVAS', 'VIDEO', 'PICTURE'].includes(el.tagName)) return true;
    return /url\(/.test(cs(el).backgroundImage) && r.width >= 48 && r.height >= 48;
  };
  const unitVisual = units.map(u => [u, ...u.querySelectorAll('*')].some(isVisual));
  if (kind === 'deck' || kind === 'brochure') units.forEach((u, i) => { if (!unitVisual[i]) add(i, 'ERROR', 'no-visual', `no visual in this ${kind === 'deck' ? 'slide' : 'section'}`); });
  if (kind === 'dashboard' && !unitVisual.some(Boolean) && ![...document.body.querySelectorAll('*')].some(isVisual)) add(-1, 'ERROR', 'no-visual', 'no visual (chart/svg/img/canvas) on the page');

  // ---------- color / gradient / shadow / italic / font
  const SHAPES = new Set(['path', 'rect', 'circle', 'ellipse', 'polygon', 'polyline', 'line', 'text', 'tspan', 'use']);
  for (const el of allEls) {
    if (SKIP.has(el.tagName) || !visible(el)) continue;
    const c = cs(el), r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0 && el.tagName.toLowerCase() !== 'stop') continue;
    const u = unitOf(el), root = u >= 0 ? units[u] : document.body, s = () => selOf(el, root);
    const hits = [];
    if (owners.has(el)) { const x = retired(c.color); if (x) hits.push('color ' + x); }
    for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
      if (parseFloat(c['border' + side + 'Width']) > 0 && c['border' + side + 'Style'] !== 'none') { const x = retired(c['border' + side + 'Color']); if (x) { hits.push('border ' + x); break; } }
    }
    if (el instanceof SVGElement) {
      const tag = el.tagName.toLowerCase();
      if (SHAPES.has(tag)) { const f = retired(c.fill); if (f) hits.push('fill ' + f);
        if (c.stroke !== 'none' && parseFloat(c.strokeWidth) > 0) { const st = retired(c.stroke); if (st) hits.push('stroke ' + st); } }
      if (tag === 'stop') { const st = retired(c.stopColor); if (st) hits.push('stop-color ' + st); }
    }
    for (const h of hits) add(u, 'ERROR', 'color', `${s()} ${h} (retired)`);
    { const x = retired(c.backgroundColor);
      if (x) add(u, 'WARN', 'color', `${s()} background ${x} \u2014 retired teal as fill, allowed for graphic tiles only`); }
    if (el instanceof SVGElement) continue;
    const big = r.width > 2 && r.height > 2;
    if (big && /gradient\(/.test(c.backgroundImage)) add(u, 'WARN', 'gradient', `${s()} ${c.backgroundImage.match(/(repeating-)?(linear|radial|conic)-gradient/)[0]}`);
    if (big && c.boxShadow && c.boxShadow !== 'none') add(u, 'WARN', 'shadow', `${s()} box-shadow`);
    if (big && /drop-shadow/.test(c.filter)) add(u, 'WARN', 'shadow', `${s()} filter:drop-shadow`);
    if (owners.has(el) && c.textShadow && c.textShadow !== 'none') add(u, 'WARN', 'shadow', `${s()} text-shadow`);
  }
  for (const o of ownerList) {
    const c = cs(o.el), s = selOf(o.el, o.root);
    if (/italic|oblique/.test(c.fontStyle)) add(o.u, 'WARN', 'italic', `${s} font-style:${c.fontStyle}`, `"${snip(o.text)}"`);
    const fam = firstFam(c.fontFamily);
    if (!BRAND_FONTS.includes(fam)) add(o.u, 'WARN', 'font', `${s} font-family "${fam}"`, `"${snip(o.text)}"`);
  }

  // ---------- voice
  const VOICE = [['dashboard', /\bdashboards?\b/i], ['leverage', /\bleverag(e|es|ed|ing)\b/i], ['synergy', /\bsynerg(y|ies|istic)\b/i],
    ['seamless', /\bseamless(ly)?\b/i], ['end-to-end', /\bend[-\s]to[-\s]end\b/i], ['disrupt', /\bdisrupt(s|ed|ing|ive|ively|or|ors)?\b/i],
    ['compounding', /\bcompounding\b/i], ['fundamentally different', /\bfundamentally different\b/i], ['impactful', /\bimpactful\b/i],
    ['collectively unintelligent', /\bcollectively unintelligent\b/i], ['chatbot', /\bchat\s?bots?\b/i], ['ai bot', /\bai bots?\b/i],
    ['virtual assistant', /\bvirtual assistants?\b/i], ['automation', /\bautomations?\b/i]];
  const PIVOTS = [/\b(isn't|aren't|is not|are not|wasn't|weren't|doesn't|don't|not just)\b[^.?!]{0,80}[.?!;,—–-]\s*(it's|it is|they're|they are|that's|this is|it)\b/i,
    /\b(it's|it is|this is) not\b[^.?!]{0,60}[,;.—–]\s*(it's|it is|but)\b/i];
  const ctx = (t, i, len) => snip(t.slice(Math.max(0, i - 12), i + len + 24), 40);
  for (const el of leaves) {
    const t = (el.textContent || '').replace(/\s+/g, ' ').replace(/[‘’]/g, "'");
    const u = unitOf(el);
    for (const [w, re] of VOICE) { const m = t.match(re); if (m) add(u, 'WARN', 'voice', `"${w}"`, `— "${ctx(t, m.index, m[0].length)}"`); }
    for (const re of PIVOTS) { const m = t.match(re); if (m) { add(u, 'WARN', 'voice', 'negation pivot', `— "${snip(m[0], 40)}"`); break; } }
  }

  // ---------- deck structure
  const meta = {units: units.length, rects: units.map(u => { const r = u.getBoundingClientRect(); return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height}; })};
  if (kind === 'deck') {
    if (!units.length) add(-1, 'ERROR', 'structure', 'no section.slide found');
    const pat = {}; let img = 0;
    units.forEach((s, i) => {
      if (!s.hasAttribute('data-pptx')) add(i, 'ERROR', 'pptx', 'slide missing data-pptx');
      else if (s.getAttribute('data-pptx') === 'image') img++;
      const r = s.getBoundingClientRect();
      if (Math.round(r.width) !== 1920 || Math.round(r.height) !== 1080) add(i, 'ERROR', 'slide-size', `slide is ${Math.round(r.width)}×${Math.round(r.height)}, must be 1920×1080`);
      if (i < units.length - 1) for (const h of s.querySelectorAll('h1, h2')) {
        if (h.closest(CHROME) || !visible(h)) continue;
        const t = h.textContent.replace(/\s+/g, ' ').trim();
        if (/\.$/.test(t) && !/\.\.\.$|…$/.test(t)) add(i, 'WARN', 'headline', 'headline ends with "."', `"${snip(t)}"`);
      }
      for (const e of [s, ...s.querySelectorAll('[data-pattern]')]) { const p = e.getAttribute('data-pattern'); if (p) (pat[p] = pat[p] || []).push(i + 1); }
    });
    for (const [p, list] of Object.entries(pat)) if (list.length > 2) add(-1, 'WARN', 'pattern', `${p} used ${list.length}× (slides ${list.join(', ')}) — max 2`);
    if (img > 2) add(-1, 'WARN', 'pptx', `${img} data-pptx="image" slides (max 2)`);
  }
  return {findings: F, meta};
}
"""


# --------------------------------------------------------------------------- helpers
def load_page(pw, html, kind, scale=1):
    w, h = VIEWPORTS.get(kind, (1440, 900))
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
    page.goto(Path(html).resolve().as_uri(), wait_until="domcontentloaded", timeout=30000)
    try:
        page.wait_for_load_state("load", timeout=8000)
    except Exception:
        pass
    fonts = page.evaluate(FONTS_READY_JS, 4000)
    frame = None
    if kind == "graphic":
        frame = page.evaluate(FIND_FRAME_JS)
        if frame:
            vw = max(200, int(frame["x"] * 2 + frame["w"] + 0.999))
            vh = max(200, int(frame["y"] * 2 + frame["h"] + 0.999))
            page.set_viewport_size({"width": vw, "height": vh})
            page.evaluate(FONTS_READY_JS, 1500)
            frame = page.evaluate(FIND_FRAME_JS)
    return browser, page, fonts, frame


def fit(img, max_w=1600, max_h=2000):
    from PIL import Image
    w, h = img.size
    s = min(1.0, max_w / w, max_h / h)
    if s < 1:
        img = img.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    return img


def save_png(img, path):
    img = fit(img, 2000, 2000)
    img.save(path, optimize=True)
    return img.size


def shot(page, rect):
    from PIL import Image
    import io
    clip = {"x": rect["x"], "y": rect["y"], "width": max(1, rect["w"]), "height": max(1, rect["h"])}
    return Image.open(io.BytesIO(page.screenshot(clip=clip, full_page=True))).convert("RGB")


def label_font(size):
    from PIL import ImageFont
    for f in ("/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()


def make_sheet(page, kind, rects, err_units, path):
    """Returns list of (path, (w, h))."""
    from PIL import Image, ImageDraw
    RED, INK, GAP, LAB = (220, 38, 38), (60, 60, 60), 8, 26
    font = label_font(16)
    path = Path(path)
    outs = []
    if kind in ("graphic", "dashboard"):
        if kind == "graphic":
            img = shot(page, rects[0])
            if 0 in err_units:
                ImageDraw.Draw(img).rectangle([0, 0, img.width - 1, img.height - 1], outline=RED, width=4)
            img = fit(img, 1600, 1600)
        else:
            full = page.evaluate("({w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight})")
            img = shot(page, {"x": 0, "y": 0, "w": full["w"], "h": min(full["h"], 6000)})
            d = ImageDraw.Draw(img)
            for i, r in enumerate(rects):
                if i in err_units:
                    d.rectangle([r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]], outline=RED, width=4)
            img = fit(img, 1600, 2000)
        outs.append((path, save_png(img, path)))
        return outs
    # deck / brochure: tile units
    if kind == "deck":
        cols, tw = 4, (1600 - GAP * 5) // 4
    else:
        total = sum(r["h"] * (1584 / max(1, r["w"])) + LAB + GAP for r in rects)
        cols = 1 if total <= 2000 else 2
        tw = (1600 - GAP * (cols + 1)) // cols
    tiles = []
    for i, r in enumerate(rects):
        img = shot(page, r)
        s = tw / img.width
        th = max(1, int(img.height * s))
        if th > 2000 - LAB - GAP * 2:
            th = 2000 - LAB - GAP * 2
            img = img.resize((max(1, int(img.width * th / img.height)), th), Image.LANCZOS)
        else:
            img = img.resize((tw, th), Image.LANCZOS)
        tiles.append((i, img))
    pages, cur = [], []
    if kind == "deck":
        th = tiles[0][1].height if tiles else 0
        per_page = max(1, (2000 - GAP) // (th + LAB + GAP)) * cols
        pages = [tiles[k:k + per_page] for k in range(0, len(tiles), per_page)]
    else:
        # fill columns top-to-bottom, then next sheet
        col, colh, sheet = 0, GAP, []
        for t in tiles:
            need_h = t[1].height + LAB + GAP
            if colh + need_h > 2000 and colh > GAP:
                col += 1
                colh = GAP
                if col >= cols:
                    pages.append(sheet)
                    sheet, col = [], 0
            sheet.append((t, col, colh))
            colh += need_h
        if sheet:
            pages.append(sheet)
    for pi, pg in enumerate(pages):
        if kind == "deck":
            rows = (len(pg) + cols - 1) // cols
            th = pg[0][1].height
            H = GAP + rows * (th + LAB + GAP)
            W = GAP + cols * (tw + GAP)
            placed = [((i, im), k % cols, GAP + (k // cols) * (th + LAB + GAP)) for k, (i, im) in enumerate(pg)]
        else:
            H = max(y + t[1].height + LAB + GAP for t, c, y in pg)
            W = GAP + cols * (tw + GAP)
            placed = pg
        sheet = Image.new("RGB", (W, H), (236, 236, 236))
        d = ImageDraw.Draw(sheet)
        for (i, im), c, y in placed:
            x = GAP + c * (tw + GAP)
            err = i in err_units
            d.text((x + 2, y + 4), f"{'slide' if kind == 'deck' else 'sect'} {i + 1:02d}{'  ERROR' if err else ''}",
                   fill=RED if err else INK, font=font)
            sheet.paste(im, (x, y + LAB))
            if err:
                d.rectangle([x - 2, y + LAB - 2, x + im.width + 1, y + LAB + im.height + 1], outline=RED, width=4)
        p = path if len(pages) == 1 else path.with_name(f"{path.stem}-{pi + 1}{path.suffix}")
        outs.append((p, save_png(sheet, p)))
    return outs


def collapse(findings):
    agg = OrderedDict()
    for f in findings:
        k = (f["u"], f["lvl"], f["chk"], f["key"])
        if k in agg:
            agg[k]["n"] += 1
        else:
            agg[k] = dict(f, n=1)
    out = list(agg.values())
    out.sort(key=lambda f: (f["u"] if f["u"] >= 0 else 10 ** 6, 0 if f["lvl"] == "ERROR" else 1))
    return out


def emit(name, kind, nunits, items, as_json, extra_lines=(), sheets=(), zooms=()):
    errs = sum(1 for f in items if f["lvl"] == "ERROR")
    warns = len(items) - errs
    lab = UNIT_LABEL.get(kind, "unit")
    if as_json:
        print(json.dumps({"file": name, "kind": kind, "units": nunits, "errors": errs, "warnings": warns,
                          "findings": [{"unit": f["u"] + 1 if f["u"] >= 0 else None, "level": f["lvl"], "check": f["chk"],
                                        "detail": f["key"], "context": f.get("extra", ""), "count": f["n"]} for f in items],
                          "notes": list(extra_lines),
                          "sheets": [{"path": str(p), "size": list(s)} for p, s in sheets],
                          "zoom": [{"path": str(p), "size": list(s)} for p, s in zooms]}, ensure_ascii=False))
        return errs
    plural = {"slide": "slides", "sect": "sections", "frame": "frame", "card": "cards"}.get(lab, "units")
    print(f"check {name} ({kind}, {nunits} {plural}): {errs} error{'s' * (errs != 1)}, {warns} warning{'s' * (warns != 1)}")
    for line in extra_lines:
        print(f"note: {line}")
    for k, f in enumerate(items):
        if k >= MAX_LINES:
            print(f"… {len(items) - MAX_LINES} more (use --json)")
            break
        if kind == "graphic" and f["u"] == 0:
            u = "frame"
        else:
            u = f"{lab} {f['u'] + 1:02d}" if f["u"] >= 0 else ("doc" if kind == "docx" else "page")
        x = f" {f['extra']}" if f.get("extra") else ""
        n = f" ×{f['n']}" if f["n"] > 1 else ""
        print(f"{u:<9} {f['lvl']:<5} {f['chk']:<12} {f['key']}{x}{n}")
    for p, s in sheets:
        print(f"sheet {p} {s[0]}x{s[1]}")
    for p, s in zooms:
        print(f"zoom {p} {s[0]}x{s[1]}")
    return errs


# --------------------------------------------------------------------------- source scan
def source_scan(text):
    """Retired hexes in raw HTML, ignoring comments, custom-property definitions, and base64 payloads.
    Also decodes embedded SVG data URIs."""
    import base64
    masked = re.sub(r"<!--.*?-->|/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)
    svg_spans = [(m.start(), m.end()) for m in re.finditer(r"<svg\b.*?</svg>", masked, flags=re.S | re.I)]
    hits = defaultdict(list)  # (level, hex) -> lines
    for m in RE_RETIRED_SRC.finditer(masked):
        start = max(masked.rfind(c, 0, m.start()) for c in ";{\n\"'")
        decl = masked[start + 1:m.start()]
        pm = re.match(r"\s*([\w-]+)\s*:", decl)
        prop = pm.group(1).lower() if pm else ""
        if prop.startswith("--"):
            continue
        in_svg = any(a0 <= m.start() < b0 for a0, b0 in svg_spans)
        if in_svg or re.match(r"(color|fill|stroke|border|outline|stop-color|text-decoration)", prop):
            lvl = "ERROR"
        else:
            lvl = "WARN"   # background / background-color / other
        hexv = "#" + m.group(1).upper() if m.group(1) else ("#00989E" if m.group(2) == "152" else "#00C4CC")
        hits[(lvl, hexv)].append(masked.count("\n", 0, m.start()) + 1)
    emb = 0
    for m in re.finditer(r"data:image/svg\+xml;base64,([A-Za-z0-9+/=]+)", text):
        try:
            s = base64.b64decode(m.group(1)).decode("utf-8", "ignore")
        except Exception:
            continue
        emb += len(re.findall(r"#(00989E|00C4CC)\b", s, re.I))
    out = []
    for (lvl, hexv), lines in hits.items():
        ls = ", ".join(str(x) for x in lines[:6]) + ("…" if len(lines) > 6 else "")
        tail = "" if lvl == "ERROR" else " as background — allowed for graphic tiles only"
        out.append({"u": -1, "lvl": lvl, "chk": "color", "key": f"retired {hexv} in source ×{len(lines)} (lines {ls}){tail}", "extra": ""})
    if emb:
        out.append({"u": -1, "lvl": "ERROR", "chk": "color", "key": f"retired hex inside embedded SVG data URI ×{emb}", "extra": ""})
    return out


# --------------------------------------------------------------------------- docx
def check_docx(path, as_json):
    need(["docx"])
    import docx
    from docx.oxml.ns import qn
    d = docx.Document(str(path))
    F = []

    root_sz = None
    dd = d.styles.element.find(qn("w:docDefaults"))
    if dd is not None:
        sz = dd.find(".//" + qn("w:rPrDefault") + "/" + qn("w:rPr") + "/" + qn("w:sz"))
        if sz is not None:
            root_sz = int(sz.get(qn("w:val"))) / 2

    def style_size(st):
        while st is not None:
            if st.font is not None and st.font.size is not None:
                return st.font.size.pt
            st = st.base_style
        return None

    def run_size(run, para):
        if run.font.size is not None:
            return run.font.size.pt
        try:
            if run.style is not None and run.style.name != "Default Paragraph Font":
                s = style_size(run.style)
                if s:
                    return s
        except Exception:
            pass
        return style_size(para.style) or root_sz or 10.0

    def all_paras(container):
        for p in container.paragraphs:
            yield p
        for t in container.tables:
            for row in t.rows:
                for cell in row.cells:
                    yield from all_paras(cell)

    small = OrderedDict()
    for p in all_paras(d):
        sname = p.style.name if p.style is not None else "?"
        for r in p.runs:
            if not r.text.strip():
                continue
            sz = run_size(r, p)
            # Labels (all-caps or Plex Mono — eyebrows, table headers, IDs) may sit at 9pt;
            # everything readable has an 11pt floor.
            fam = (r.font.name or "").lower()
            is_label = bool(r.font.all_caps) or "mono" in fam or (r.text.strip().isupper() and len(r.text.strip()) >= 2)
            floor = 9 if is_label else 11
            if sz < floor:
                k = (sname, sz, floor)
                if k not in small:
                    small[k] = [0, r.text]
                small[k][0] += 1
    for (sname, sz, floor), (n, t) in small.items():
        F.append({"u": -1, "lvl": "WARN", "chk": "type-floor", "key": f"style '{sname}' {sz:g}pt < {floor}pt" + (" (label)" if floor == 9 else ""), "extra": f'"{t.strip()[:40]}"', "n": n})

    # sections by Heading 1, paragraph length, visuals
    body = d.element.body
    sec, sec_title, has_visual, secs = 0, None, False, []
    from docx.text.paragraph import Paragraph
    for child in body.iterchildren():
        tag = child.tag.split("}")[1]
        if tag == "p":
            p = Paragraph(child, d)
            sname = p.style.name if p.style is not None else ""
            ppr0 = child.find(qn("w:pPr"))
            olvl = ppr0.find(qn("w:outlineLvl")) if ppr0 is not None else None
            is_h1 = sname.lower() == "heading 1" or (olvl is not None and olvl.get(qn("w:val")) == "0" and p.text.strip())
            if is_h1:
                if sec_title is not None:
                    secs.append((sec, sec_title, has_visual))
                sec += 1
                sec_title, has_visual = p.text.strip(), False
                continue
            if child.findall(".//" + qn("w:drawing")) or child.findall(".//" + qn("w:pict")):
                has_visual = True
            ppr = child.find(qn("w:pPr"))
            if ppr is not None:
                shd = ppr.find(qn("w:shd"))
                if (shd is not None and (shd.get(qn("w:fill")) or "auto").upper() not in ("AUTO", "FFFFFF")) or ppr.find(qn("w:pBdr")) is not None:
                    has_visual = True
            words = len(re.findall(r"\w+", p.text))
            if words > 60 and "quote" not in sname.lower():
                F.append({"u": sec - 1 if sec else -1, "lvl": "WARN", "chk": "word-count", "key": f"paragraph {words} words",
                          "extra": f'"{p.text.strip()[:39]}…"'})
        elif tag == "tbl":
            has_visual = True
    if sec_title is not None:
        secs.append((sec, sec_title, has_visual))
    for n, title, vis in secs:
        if not vis:
            F.append({"u": n - 1, "lvl": "WARN", "chk": "no-visual", "key": f"no visual in section \"{title[:36]}\"", "extra": ""})

    # retired hex anywhere in the XML (run colors, shading, borders)
    with zipfile.ZipFile(str(path)) as z:
        for name in z.namelist():
            if name.startswith("word/") and name.endswith(".xml"):
                n = len(re.findall(r"(?i)\b(00989E|00C4CC)\b", z.read(name).decode("utf-8", "ignore")))
                if n:
                    F.append({"u": -1, "lvl": "ERROR", "chk": "color", "key": f"retired hex in {name} ×{n}", "extra": ""})
    for f in F:
        f.setdefault("n", 1)
    items = sorted(F, key=lambda f: (f["u"] if f["u"] >= 0 else 10 ** 6, 0 if f["lvl"] == "ERROR" else 1))
    errs = emit(path.name, "docx", len(secs), items, as_json)
    return 1 if errs else 0


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Metafore brand + layout lint.")
    ap.add_argument("file")
    ap.add_argument("--kind", choices=["deck", "brochure", "graphic", "dashboard"])
    ap.add_argument("--sheet")
    ap.add_argument("--zoom", type=int)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    path = Path(a.file)
    if not path.exists():
        print(f"error: {path} not found")
        return 2
    if path.suffix.lower() == ".docx":
        return check_docx(path, a.json)
    if not a.kind:
        print("error: --kind deck|brochure|graphic|dashboard required for HTML")
        return 2
    need(["playwright", "PIL"])
    from playwright.sync_api import sync_playwright

    src = path.read_text(encoding="utf-8", errors="ignore")
    notes = []
    with sync_playwright() as pw:
        browser, page, fonts, frame = load_page(pw, path, a.kind)
        try:
            fams = {f.lower() for f in fonts["families"]}
            if not fonts["loaded"] or not {"geist", "inter"} & fams:
                notes.append("web fonts not loaded (offline?) — metrics use fallbacks")
            if a.kind == "graphic" and not frame:
                notes.append("no fixed-size frame found (add data-frame or explicit width/height); using <body>")
            res = page.evaluate(CHECK_JS, {"kind": a.kind})
            items = collapse(res["findings"] + source_scan(src))
            rects = res["meta"]["rects"]
            if a.kind == "graphic" and not frame:
                full = page.evaluate("({w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight})")
                rects = [{"x": 0, "y": 0, "w": full["w"], "h": full["h"]}]
            err_units = {f["u"] for f in items if f["lvl"] == "ERROR" and f["u"] >= 0}
            sheets, zooms = [], []
            if a.sheet and rects:
                sheets = make_sheet(page, a.kind, rects, err_units, a.sheet)
            if a.zoom:
                if 1 <= a.zoom <= len(rects):
                    img = fit(shot(page, rects[a.zoom - 1]), 1600, 1600)
                    zp = path.with_name(f"{path.stem}.unit-{a.zoom:02d}.png")
                    zooms.append((zp, save_png(img, zp)))
                else:
                    notes.append(f"--zoom {a.zoom} out of range 1..{len(rects)}")
        finally:
            browser.close()
    errs = emit(path.name, a.kind, res["meta"]["units"], items, a.json, notes, sheets, zooms)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
