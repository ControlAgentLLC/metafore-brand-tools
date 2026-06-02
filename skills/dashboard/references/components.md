# Metafore Dashboard — Components

These are the building blocks. The starter template wires them together; this file documents the patterns so you can compose new pages without re-deriving anything.

> **Typography override — read first.** The canonical type system is defined in `design-tokens.md` (Perfect Fifth default, Perfect Fourth floor; LH 1.125 headers / 1.200 body; tracking 0). When a snippet below shows `letter-spacing` (negative or positive) or a `line-height` outside the 1.125–1.200 range, the canonical system wins — strip the value or replace it with the matching token.

## Shell

```
.app  →  64px sidebar | flex main
```

```css
.app { display: grid; grid-template-columns: 64px 1fr; min-height: 100vh; }
```

### Sidebar

- 64px wide, sticky to viewport, full height.
- Top: 32×32 logo slot (inline SVG — see `logo.svg`). 14px below it, the icon nav.
- Nav items are 36×36 squares, 8px radius, gray default, dark on hover, **active = solid black with white icon**.
- Bottom: workspace badge — 36×36, 8px radius, light gray fill, two-letter monogram (e.g. `AC`, `AM`).

### Topbar

- Sticky to viewport top, `1fr auto` grid, 14px / 28px padding.
- **Left slot**: search input, 280–520px wide, with a search icon and a `⌘K` mono kbd hint. **Not a brand wordmark.** The mark already lives in the sidebar.
- **Right slot**: optional `Activity` icon-text button, then the avatar circle (linear-gradient is fine).

### Hero

```html
<section class="hero">
  <div>
    <h1>First word <span class="it">last word</span></h1>
    <p>One editorial sentence under the headline.</p>
  </div>
  <div class="controls">
    <span class="live">Live · Source A + Source B</span>
    <button class="iconbtn icon-only">…</button>
    <span class="pill">…</span>
    <div class="seg">…</div>
  </div>
</section>
```

- `h1` follows the canonical scale: `font-size: clamp(var(--h1-floor), 6.5cqw, var(--h1-size))`, weight 400, `var(--serif)`, `line-height: var(--lh-header)`, `letter-spacing: 0`. The `.hero` wrapper carries `container-type: inline-size` so the header auto-shrinks toward the Perfect Fourth floor (28px) when copy is long. The body lede beneath it stays at 18px / 1.2 — it never shrinks.
- The `.it` span is **not italic** — it's just a teal-colored span (`color: var(--header-2)` = `#035657`).
- The hero is the only place in the document that uses the serif at this size. Don't repeat it.

## Card grid

```css
.grid {
  padding: 22px 28px 8px;
  display: grid; grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}
.card { /* see below */ }
.span-2 { grid-column: span 2; }
.span-4 { grid-column: span 4; }
@media (max-width: 1180px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
  .span-2, .span-4 { grid-column: span 2; }
}
@media (max-width: 720px) {
  .grid { grid-template-columns: 1fr; }
  .span-2, .span-4 { grid-column: auto; }
}
```

### Base card

```css
.card {
  position: relative;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: #fff;
  padding: 20px 20px 18px;
  min-height: 168px;
  display: flex; flex-direction: column; gap: 8px;
  transition: border-color .15s;
}
.card:hover { border-color: #d6d6d6; }
```

A **status modifier** can be added (`.card.warn`, `.card.bad`, `.card.ok`) — currently it changes nothing because the side bar is disabled. If the user re-enables the bar, that modifier becomes load-bearing.

### Card content slots

```html
<article class="card">
  <div class="label">
    <span class="nm">KPI Label</span>          <!-- mono uppercase -->
    <span class="trend">+3</span>              <!-- optional right side -->
  </div>
  <div class="spark"><svg>…</svg></div>        <!-- optional sparkline, abs-positioned top-right -->
  <div class="body">
    <div class="stat">$114.8M</div>            <!-- or 12, 4m 22s, 96.4%, etc. -->
  </div>
  <div class="footnote">NetSuite live</div>    <!-- one-line context -->
</article>
```

```css
.card .label {
  display: flex; align-items: center; justify-content: space-between;
  font-family: 'IBM Plex Mono', monospace;
  font-size: var(--eyebrow-size); line-height: var(--lh-body); letter-spacing: 0;
  text-transform: uppercase; color: var(--ink-3); padding-left: 10px;
}
.card .label .nm { display: inline-flex; align-items: center; gap: 8px; }
.card .label .nm::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: #1f7a4d; }
.card .label.warn .nm::before { background: #c89321; }
.card .label.bad  .nm::before { background: #a02b1d; }

.card .body { padding-left: 10px; flex: 1; container-type: inline-size; }
.card .stat {
  font-family: var(--serif); font-weight: 400;
  font-size: clamp(var(--h1-floor), 6.5cqw, var(--h1-size));
  line-height: var(--lh-header); letter-spacing: 0;
  color: var(--header); margin-top: 4px;
}
.card .stat .unit {
  font-family: 'Inter', sans-serif; font-size: var(--body-size); color: var(--ink-3);
  line-height: var(--lh-body); margin-left: 6px; font-weight: 500;
}
.card .footnote { padding-left: 10px; color: var(--ink-3); font-size: 12px; margin-top: 6px; }
.card .footnote.warn { color: #8a5a13; }
.card .footnote.bad  { color: #8a2a1f; }

.card .spark { position: absolute; right: 16px; top: 18px; width: 80px; height: 28px; }
```

### Status dot at top-left of label

The colored dot at the start of the label is the **only** place status color is conveyed at the card level by default. Don't add icon trays, badges, or red borders.

## Status list (Active Agents, Connected Systems, Active Users…)

```html
<article class="card">
  <div class="label">Active Agents</div>
  <div class="list">
    <div class="row"><span class="dot"></span><span class="name">O2C Agent</span><span class="tag">LIVE</span></div>
    <div class="row"><span class="dot"></span><span class="name">Tariff Agent</span><span class="tag">LIVE</span></div>
    <div class="row"><span class="dot gray"></span><span class="name">Carrier Agent</span><span class="tag">IDLE</span></div>
  </div>
  <div class="footlink"><a href="#">Manage agents →</a></div>
</article>
```

```css
.list { padding-left: 10px; display: flex; flex-direction: column; gap: 8px; margin-top: 4px; }
.list .row { display: grid; grid-template-columns: 10px 1fr auto; gap: 10px; align-items: center; font-size: 13px; }
.list .dot { width: 7px; height: 7px; border-radius: 50%; background: #1f7a4d; }
.list .dot.amber { background: #c89321; }
.list .dot.red   { background: #a02b1d; }
.list .dot.gray  { background: #b8b8b8; }
.list .name { color: var(--ink); }
.list .tag {
  color: var(--ink-4); font-family: 'IBM Plex Mono', monospace;
  font-size: var(--eyebrow-size); line-height: var(--lh-body); letter-spacing: 0;
}
```

## Decision feed (timeline-style list)

Same skeleton as the status list, with two-line rows:

```html
<article class="card span-2 decisions">
  <div class="label">Recent Decisions</div>
  <div class="list">
    <div class="row">
      <span class="dot amber"></span>
      <div>
        <div class="name">Order SO-48291</div>
        <div class="desc">Agent flagged carrier delay. Awaiting approval.</div>
      </div>
      <span class="when">4m</span>
    </div>
    …
  </div>
</article>
```

```css
.decisions .row { grid-template-columns: 10px 1fr auto; align-items: start; padding: 6px 0; border-bottom: 1px dashed var(--line-2); }
.decisions .row:last-child { border-bottom: 0; }
.decisions .name { font-weight: 500; }
.decisions .desc { color: var(--ink-3); font-size: var(--body-size); line-height: var(--lh-body); letter-spacing: 0; margin-top: 2px; }
.decisions .when { color: var(--ink-4); font-size: 11px; font-family: 'IBM Plex Mono', monospace; }
```

## Table card

```html
<article class="card span-4 issues">
  <div class="label"><span class="nm">Top Priority Issues — Live Jira</span></div>
  <h3>Top Priority Issues <span class="rows-pill">5 rows</span></h3>
  <table>
    <thead>
      <tr><th class="first-col">Key</th><th>Issue</th><th>Assignee</th><th style="text-align:right">Priority</th></tr>
    </thead>
    <tbody>
      <tr>
        <td class="key first-col">RE-492</td>
        <td>Expanding the dataset…</td>
        <td class="assignee unassigned">Unassigned</td>
        <td style="text-align:right"><span class="pri">High</span></td>
      </tr>
    </tbody>
  </table>
</article>
```

- `td.key` uses IBM Plex Mono, weight 500, `var(--ink)`.
- `td.assignee.unassigned` is italic gray.
- `.pri` is a small mono pill — soft warn fill `#fbf3df` / `#8a5a13`.
- `.rows-pill` is a small mono pill — gray fill, `var(--ink-3)`.

Full CSS in starter template.

## Bar chart card

```html
<article class="card span-4 work">
  <div class="label"><span class="nm">Engineering Workload — Live Jira</span></div>
  <h3>Engineering Workload</h3>
  <div class="sub">Real-time from Jira</div>
  <div class="legend">
    <span class="ip"><i></i>In Progress</span>
    <span class="td"><i></i>To Do</span>
    <span class="bk"><i></i>Blocked</span>
  </div>
  <div class="chart">
    <div class="axis-y"><span>40%</span><span>30%</span><span>20%</span><span>10%</span><span>0</span></div>
    <div class="gridlines"><span></span><span></span><span></span><span></span><span></span></div>
    <div class="bars-grid">
      <div class="col"><div class="b ip" style="height:92%"></div></div>
      …
    </div>
    <div class="x"><span>Aditya</span>…</div>
  </div>
</article>
```

```css
.chart .col .b.ip { background: var(--logo-dark); }
.chart .col .b.td { background: var(--logo-light); }
.chart .col .b.bk { background: var(--teal-bright); }
```

Series colors are **always** the logo teals. If the user asks for "more colors", push back: tell them we differentiate with order/weight, not a second hue.

## Sparkline

Inline SVG inside `.spark`, 80×28 abs-positioned top-right of the card. Three flavors:

```html
<svg viewBox="0 0 80 28" preserveAspectRatio="none">
  <path class="up" d="M0 22 L12 20 L24 18 L36 19 L48 14 L60 9 L72 6 L80 4" fill="none" stroke-width="1.6"/>
</svg>
```

```css
.spark .up   { stroke: var(--logo-dark); }
.spark .down { stroke: var(--logo-light); }
.spark .flat { stroke: var(--teal); }
```

## Recommended-action callout

For any agent-suggested action that needs a human approval. Inline copy on the left ("**Recommended action.** …"), Edit/Approve buttons on the right. Keep this **understated** — the recommendation reads as part of the surrounding context, not as a shouty interruption. No left bar, no eyebrow, no confidence indicator by default.

```html
<div class="reco">
  <div class="copy"><b>Recommended action.</b> Re-tender to Werner at +$5.9K — preserves $148K order and SLA.</div>
  <div class="actions">
    <button class="btn">Edit</button>
    <button class="btn primary">Approve</button>
  </div>
</div>
```

```css
.reco {
  margin-top: 12px; margin-left: 10px;
  border: 1px solid var(--line); border-radius: 10px;
  padding: 12px 14px;
  display: flex; align-items: center; justify-content: space-between; gap: 14px;
  background: #fafafa;
}
.reco .copy { font-size: var(--body-size); color: var(--ink-2); line-height: var(--lh-body); letter-spacing: 0; }
.reco .copy b { color: var(--ink); }
.reco .actions { display: flex; gap: 8px; }

.btn {
  border: 1px solid var(--line); background: #fff;
  height: 32px; padding: 0 14px; border-radius: 8px;
  font: 500 12px 'Inter', sans-serif; cursor: pointer; color: var(--ink-2);
}
.btn:hover { background: var(--hover); }
.btn.primary { background: #0a0a0a; color: #fff; border-color: #0a0a0a; }
.btn.primary:hover { background: #222; }
```

Resist the urge to add eyebrows, sparkle icons, confidence indicators, gradient backgrounds, or left accent bars to this block. The simple version is intentional — the recommendation is one of many things a user is reading, not the hero of the page.

## Toggle / segment / pill / icon button

```css
.iconbtn {
  border: 1px solid var(--line); background: #fff; height: 36px; padding: 0 12px; border-radius: 10px;
  display: inline-flex; align-items: center; gap: 8px; color: var(--ink-2); cursor: pointer;
  font: 500 13px 'Inter', sans-serif;
}
.iconbtn:hover { background: var(--hover); }
.iconbtn.icon-only { width: 36px; padding: 0; justify-content: center; }
.iconbtn svg { width: 14px; height: 14px; }
.iconbtn.icon-only svg { width: 16px; height: 16px; }

.pill {
  display: inline-flex; align-items: center; gap: 8px; height: 36px; padding: 0 12px;
  border: 1px solid var(--line); border-radius: 10px; background: #fff;
  font: 500 13px/1 'Inter', sans-serif; color: var(--ink-2); cursor: pointer;
}
.pill svg { width: 14px; height: 14px; color: var(--ink-3); }
.pill .caret { width: 10px; height: 10px; }

.seg { display: inline-flex; gap: 6px; height: 36px; align-items: center; }
.seg button {
  height: 36px; padding: 0 14px;
  background: #f4f4f4; border: 1px solid transparent;
  font: 500 13px 'Inter', sans-serif; color: var(--ink-3);
  border-radius: 8px; cursor: pointer;
  transition: background .15s, border-color .15s, color .15s;
}
.seg button:hover { background: #ececec; color: var(--ink-2); }
.seg button.on {
  background: #fff; border-color: var(--line); color: var(--ink);
}

.live {
  display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px;
  border: 1px solid var(--line); border-radius: 999px;
  font: 500 12px 'Inter', sans-serif; color: var(--ink-2); background: #fff;
}
.live::before {
  content: ""; width: 7px; height: 7px; border-radius: 50%;
  background: #1f7a4d; box-shadow: 0 0 0 4px rgba(31,122,77,.12);
}
```

The toggle's **active state is a white pill, never a black fill.** This is non-negotiable — the old black-fill segmented control reads as "marketing site CTA" and is wrong here.

## Suggestion chips

```html
<div class="chips">
  <button class="chip"><svg>…</svg>Revenue</button>
  <button class="chip">…</button>
</div>
```

```css
.chips { display: flex; flex-wrap: wrap; gap: 8px; padding: 22px 28px 6px; justify-content: center; }
.chip {
  display: inline-flex; align-items: center; gap: 8px; padding: 8px 14px;
  border: 1px solid var(--line); border-radius: 999px;
  font: 500 13px 'Inter', sans-serif; color: var(--ink-2); background: #fff; cursor: pointer;
}
.chip:hover { background: var(--hover); }
```

## "I want to…" + composer

```html
<div class="prompt-wrap">
  <div class="iwant">
    <div class="row"><b>I want to</b> see why gross margin slipped 1.8pp this quarter</div>
    <div class="row"><b>I want to</b> understand who owns the 17 overdue Jira items</div>
    <div class="row"><b>I want to</b> model the revenue impact of a 6-week APAC delay</div>
  </div>

  <div class="composer">
    <input placeholder="I want to…" />
    <div class="row">
      <div class="tools">
        <button title="Attach"><svg>…</svg></button>
        <button title="Run"><svg>…</svg></button>
        <button title="Web"><svg>…</svg></button>
        <button title="History"><svg>…</svg></button>
      </div>
      <button class="send"><svg>↑</svg></button>
    </div>
  </div>
</div>
```

```css
.prompt-wrap { padding: 12px 28px 0; max-width: 980px; margin: 0 auto; }
.iwant { background: #f6f6f6; border-radius: 14px; padding: 6px 14px; }
.iwant .row { padding: 10px 6px; border-bottom: 1px solid #ececec; color: var(--ink-3); font-size: 14px; }
.iwant .row:last-child { border-bottom: 0; }
.iwant .row b { color: var(--ink); font-weight: 500; }

.composer {
  margin: 14px auto 0; max-width: 980px;
  border: 1px solid var(--line); border-radius: 14px; background: #fff; padding: 14px 16px;
}
.composer input {
  width: 100%; border: 0; outline: 0; font: 500 16px 'Inter', sans-serif; color: var(--ink); background: transparent;
}
.composer input::placeholder { color: var(--ink-3); font-weight: 500; }
.composer .row {
  display: flex; align-items: center; justify-content: space-between; margin-top: 12px;
}
.composer .tools button {
  width: 28px; height: 28px; border-radius: 6px; background: transparent; border: 0;
  display: grid; place-items: center; color: var(--ink-3); cursor: pointer;
}
.composer .tools button:hover { background: var(--hover); color: var(--ink); }
.composer .send {
  width: 32px; height: 32px; border-radius: 8px; background: #0a0a0a; color: #fff;
  border: 0; display: grid; place-items: center; cursor: pointer;
}
```

The "I want to…" prompts must be **domain-specific**. Generic ones ("see my dashboard", "look at metrics") are filler — pick three real questions a user of this surface would actually ask.

## Multi-page tab switcher

When the project has more than one dashboard file, drop this in the top-right corner of each one:

```html
<div class="switcher">
  <a href="dashboard-bw.html" class="on">Enterprise Intelligence</a>
  <a href="dashboard-bw-supplychain.html">Supply Chain</a>
</div>
```

```css
.switcher {
  position: fixed; top: 14px; right: 28px; z-index: 10;
  display: inline-flex; border: 1px solid var(--line); border-radius: 10px;
  overflow: hidden; background: #fff;
}
.switcher a { padding: 8px 14px; font: 500 12px 'Inter', sans-serif; color: var(--ink-3); text-decoration: none; }
.switcher a.on { background: #0a0a0a; color: #fff; }
```

Mark the current page with `.on` so the user knows where they are.

## Optional: side accent bar (currently disabled)

The system originally had a 3px logo-teal vertical bar flush with the left edge of every card, vertically centered, color-keyed to status. It was removed because it felt redundant with the status dot. If the user asks to bring it back:

```css
.card::before {
  content: ""; position: absolute; left: 0; top: 50%; transform: translateY(-50%);
  width: 3px; height: 38px;
  background: var(--accent); border-radius: 0 2px 2px 0;
  transition: background .2s;
}
.card.warn::before, .card:has(.label.warn)::before { background: var(--warn); }
.card.bad::before,  .card:has(.label.bad)::before  { background: var(--danger); }
.card.ok::before                                    { background: var(--success); }
```

Default `--accent` is `var(--teal)`.
