# Blog Hero — Copy-Paste Recipes

Exact CSS patterns for the three Type 1 blog-hero formats and the right-panel data-card variants.

All hero recipes obey the Brand-critical rules in `SKILL.md`:
- No diagonal stripes
- No double-stacked dot patterns (full grid OR duotone-fade — never both)
- Full-screen dark surfaces are SOLID (no dots on Type 1B background, Type 1C right panel)
- Real Metafore SVG wordmark only (see `logo-svgs.md`)
- Arrow apex sits at the end of the line

---

## Format 1A: Split White / Halftone Data Card

### Base Frame + Left Panel

```css
:root{
  --ink:#1A1A1A; --ink-2:#404040; --ink-3:#666; --ink-4:#999;
  --teal:#006B6F; --teal-dark:#004D50; --teal-accent:#00989E;
  --teal-bright:#00C4CC; --teal-light:#E8F4F5;
  --logo-dark:#035657; --logo-light:#67A4A4;
  --coral:#D94A30; --amber:#C48800; --success:#00896A;
  --line:rgba(0,0,0,0.08); --bg-solid:#F8FAFA;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff;color:var(--ink);font-family:'Geist','Inter',sans-serif;-webkit-font-smoothing:antialiased}

.frame{width:1422px;height:800px;display:grid;grid-template-columns:1fr 1fr;background:#fff}
.left{padding:96px 72px 96px 96px;display:flex;flex-direction:column;justify-content:center}
.eyebrow{font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--teal);margin-bottom:32px}
h1{font-family:'Geist','Inter',sans-serif;font-weight:400;font-size:58px;line-height:1.05;letter-spacing:-.025em;margin-bottom:32px}
h1 .accent{color:var(--logo-dark)}  /* #035657 — NOT --teal */
.lede{font-family:'Inter',sans-serif;font-size:16px;line-height:1.55;color:var(--ink-2);max-width:460px}
```

### Right Panel (single full dot grid)

```css
.right{
  position:relative;
  background-color:var(--teal-light);
  background-image:radial-gradient(circle at 1px 1px,rgba(0,107,111,.32) 1px,transparent 1.6px);
  background-size:6px 6px;
  display:flex;align-items:center;justify-content:center;
  padding:48px;overflow:hidden;
}
```

**No additional `::before` overlay.** No duotone-fade. No diagonal stripes. The single full dot grid is the entire texture.

### White Data Card (shared base)

```css
.card{
  position:relative;background:#fff;border-radius:8px;
  padding:32px 36px;width:540px;
  border:1px solid rgba(0,0,0,.05);
  box-shadow:0 1px 2px rgba(0,0,0,.04);
}
.card-h{
  font-family:'IBM Plex Mono',monospace;
  font-size:10px;font-weight:600;letter-spacing:.16em;
  text-transform:uppercase;color:var(--ink-3);
  padding-bottom:18px;margin-bottom:24px;
  border-bottom:1px solid var(--line);
  display:flex;justify-content:space-between;align-items:baseline;
}
.card-h .tag{color:var(--coral)}
```

---

## Card Variant: Before / After Timeline

Use when the blog compares a fragmented vs orchestrated cycle time.

```html
<div class="card">
  <div class="card-h">
    <span>Recovery · BA2142 LHR → DXB</span>
    <span class="tag">WX Cancel · 14:42 GMT</span>
  </div>
  <div class="tl">
    <div class="rh"><span class="name muted">Without orchestration</span><span class="time bad">6h 14m</span></div>
    <div class="bar bad">
      <div class="seg"></div><div class="seg gap"></div><div class="seg"></div><div class="seg gap"></div><div class="seg"></div><div class="seg gap"></div><div class="seg"></div><div class="seg gap"></div><div class="seg"></div>
    </div>
    <div class="sys"><span>PSS</span><span>Ops Ctl</span><span>Crew</span><span>MRO</span><span>Care</span></div>
  </div>
  <div class="tl">
    <div class="rh"><span class="name">With cognitive orchestration</span><span class="time good">1h 52m</span></div>
    <div class="bar good"><div class="seg"></div><div class="seg"></div><div class="seg"></div><div class="seg"></div><div class="seg"></div></div>
    <div class="sys"><span>PSS</span><span>Ops Ctl</span><span>Crew</span><span>MRO</span><span>Care</span></div>
  </div>
  <div class="fstrip"><span>Cycle-time delta</span><span class="delta">−4h 22m · 70% faster</span></div>
</div>
```

```css
.tl{margin-bottom:28px} .tl:last-of-type{margin-bottom:0}
.rh{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}
.rh .name{font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-2)}
.rh .name.muted{color:var(--ink-4)}
.rh .time{font-family:'IBM Plex Mono',monospace;font-size:26px;font-weight:500;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.rh .time.bad{color:var(--coral)} .rh .time.good{color:var(--teal)}

.bar{display:grid;height:28px;border-radius:4px;overflow:hidden;margin-bottom:8px;background:#F3F6F6}
.bar.bad{grid-template-columns:25fr 55fr 35fr 45fr 30fr 60fr 30fr 50fr 40fr}
.bar.bad .seg{background:var(--teal-light);border-right:1px solid rgba(0,107,111,.18)}
.bar.bad .gap{background:repeating-linear-gradient(135deg,rgba(217,74,48,.22) 0 3px,rgba(217,74,48,.1) 3px 6px);border-right:1px solid rgba(217,74,48,.35)}
.bar.good{grid-template-columns:20fr 25fr 25fr 20fr 22fr;background:var(--teal-dark)}
.bar.good .seg{background:var(--teal-dark);border-right:1px solid rgba(0,196,204,.35)}
.bar.good .seg:nth-child(2n){background:var(--teal)}

.sys{display:flex;justify-content:space-between;font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
.sys span{flex:1;text-align:center}
.sys span:first-child{text-align:left} .sys span:last-child{text-align:right}

.fstrip{margin-top:28px;padding-top:18px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
.fstrip .delta{color:var(--teal);font-size:14px;letter-spacing:-.01em;font-variant-numeric:tabular-nums}
```

**Note:** the `repeating-linear-gradient` *inside* the segmented timeline bar is a small hatched-segment pattern (handoff waste). That's NOT a surface-level diagonal stripe — it lives inside a tiny 28px-tall data element, and is permitted. The rule "no diagonal stripes" applies to backgrounds and decorative overlays, not to micro UI elements like hatched bar segments.

---

## Card Variant: KPI Grid + Horizontal Bar Chart

Use when the headline rests on a comparative metric (e.g. on-time performance across hubs).

```html
<div class="card">
  <div class="card-h"><span>Network Pulse · D0 06:00</span><span style="color:var(--teal)">Today</span></div>
  <div class="kpig">
    <div class="kpi"><div class="l">On-time D-1</div><div class="v">82.4%</div><div class="d">+3.1 wow</div></div>
    <div class="kpi"><div class="l">Cx today</div><div class="v bad">14</div><div class="d bad">+6 vs plan</div></div>
    <div class="kpi"><div class="l">Crew exposure</div><div class="v">2.1%</div><div class="d">−0.8</div></div>
  </div>
  <div class="bcharth"><span>On-time arrivals · by hub</span><span class="scale">0 — 100%</span></div>
  <div class="bchart">
    <div class="brow"><span class="k">LHR</span><span class="t"><span class="fill gd" style="width:86%"></span></span><span class="v">86%</span></div>
    <div class="brow"><span class="k">DXB</span><span class="t"><span class="fill" style="width:91%"></span></span><span class="v">91%</span></div>
    <div class="brow"><span class="k">JFK</span><span class="t"><span class="fill warn" style="width:74%"></span></span><span class="v">74%</span></div>
    <div class="brow"><span class="k">SIN</span><span class="t"><span class="fill" style="width:88%"></span></span><span class="v">88%</span></div>
    <div class="brow"><span class="k">CDG</span><span class="t"><span class="fill bad" style="width:62%"></span></span><span class="v bad">62%</span></div>
  </div>
  <div class="fstrip"><span>Recommended actions</span><span class="delta">3 ready for sign-off</span></div>
</div>
```

```css
.kpig{display:grid;grid-template-columns:1fr 1fr 1fr;gap:0;margin-bottom:22px;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.kpig .kpi{padding:16px 18px;border-right:1px solid var(--line)} .kpig .kpi:last-child{border-right:0}
.kpig .kpi .l{font-family:'IBM Plex Mono',monospace;font-size:9px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);margin-bottom:8px}
.kpig .kpi .v{font-family:'IBM Plex Mono',monospace;font-size:28px;font-weight:500;font-variant-numeric:tabular-nums;letter-spacing:-.02em;color:var(--logo-dark)}
.kpig .kpi .v.bad{color:var(--coral)}
.kpig .kpi .d{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--teal);font-weight:600;letter-spacing:.04em;margin-top:4px}
.kpig .kpi .d.bad{color:var(--coral)}

.bcharth{font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);margin-bottom:14px;display:flex;justify-content:space-between}
.bcharth .scale{color:var(--ink-4);font-weight:500}
.bchart{display:grid;grid-template-columns:1fr;gap:10px;margin-bottom:6px}
.brow{display:grid;grid-template-columns:54px 1fr 56px;align-items:center;gap:12px;font-family:'IBM Plex Mono',monospace;font-size:11px}
.brow .k{font-weight:500;color:var(--ink-2);letter-spacing:.04em;text-transform:uppercase;font-size:9.5px}
.brow .v{font-weight:600;color:var(--ink);text-align:right;font-variant-numeric:tabular-nums}
.brow .v.bad{color:var(--coral)}
.brow .t{height:14px;background:#F3F6F6;border-radius:3px;overflow:hidden}
.brow .fill{display:block;height:100%;border-radius:3px;background:var(--teal-dark)}
.brow .fill.gd{background:var(--teal)} .brow .fill.warn{background:var(--amber)} .brow .fill.bad{background:var(--coral)}
```

---

## Card Variant: Phase Bars

Use for multi-step processes where each step has a cost (time, exposure, throughput).

```html
<div class="card">
  <div class="card-h"><span>Incident · Metro Ring 4</span><span class="tag">Fibre cut · 03:18 GMT</span></div>
  <div class="tl">
    <div class="rh"><span class="name muted">Manual workflow</span><span class="time bad">4h 06m</span></div>
    <div class="bcharth"><span>Time per phase</span><span class="scale">Minutes</span></div>
    <div class="bchart">
      <div class="brow"><span class="k">Detect</span><span class="t"><span class="fill bad" style="width:14%"></span></span><span class="v">34m</span></div>
      <div class="brow"><span class="k">Triage</span><span class="t"><span class="fill bad" style="width:32%"></span></span><span class="v">78m</span></div>
      <div class="brow"><span class="k">Isolate</span><span class="t"><span class="fill bad" style="width:22%"></span></span><span class="v">54m</span></div>
      <div class="brow"><span class="k">Notify</span><span class="t"><span class="fill bad" style="width:18%"></span></span><span class="v">44m</span></div>
      <div class="brow"><span class="k">Credit</span><span class="t"><span class="fill bad" style="width:30%"></span></span><span class="v">76m</span></div>
    </div>
  </div>
  <div class="fstrip"><span>With cognitive orchestration</span><span class="delta">11m total · 95% faster</span></div>
</div>
```

Reuses the `kpig` / `bchart` / `brow` / `fstrip` CSS from above.

---

## Card Variant: Sparkline / Area Chart + KPI Strip

Use for trend stories or "before they call" narratives.

```html
<div class="card">
  <div class="card-h"><span>Churn signal · 14:30 GMT</span><span style="color:var(--teal)">Live</span></div>
  <div class="kpig">
    <div class="kpi"><div class="l">At-risk</div><div class="v">14,206</div><div class="d">+812 today</div></div>
    <div class="kpi"><div class="l">Offers sent</div><div class="v">9,841</div><div class="d">68% of pool</div></div>
    <div class="kpi"><div class="l">Save rate</div><div class="v">62%</div><div class="d">+11pp vs Q1</div></div>
  </div>
  <div class="bcharth"><span>Daily save rate · 14 days</span><span class="scale">% saved</span></div>
  <svg viewBox="0 0 480 110" style="width:100%;height:110px;display:block;margin-bottom:6px">
    <defs>
      <linearGradient id="tArea" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#006B6F" stop-opacity=".22"/>
        <stop offset="1" stop-color="#006B6F" stop-opacity="0"/>
      </linearGradient>
    </defs>
    <g stroke="#E8F4F5" stroke-width="1">
      <line x1="0" y1="20" x2="480" y2="20"/>
      <line x1="0" y1="55" x2="480" y2="55"/>
      <line x1="0" y1="90" x2="480" y2="90"/>
    </g>
    <path d="M0 78 L 35 70 L 70 76 L 105 58 L 140 64 L 175 50 L 210 56 L 245 42 L 280 48 L 315 36 L 350 40 L 385 28 L 420 32 L 455 22 L 480 26 L 480 110 L 0 110 Z" fill="url(#tArea)"/>
    <path d="M0 78 L 35 70 L 70 76 L 105 58 L 140 64 L 175 50 L 210 56 L 245 42 L 280 48 L 315 36 L 350 40 L 385 28 L 420 32 L 455 22 L 480 26" fill="none" stroke="#004D50" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
    <circle cx="455" cy="22" r="4" fill="#004D50"/><circle cx="455" cy="22" r="2" fill="#fff"/>
  </svg>
  <div class="sys"><span>D-14</span><span>D-10</span><span>D-6</span><span>D-2</span><span>Today</span></div>
</div>
```

---

## Format 1B: Full Teal + Floating UI Card

**Background is SOLID `--teal-dark`.** No dot grid. No halftone overlay. No stripes. The dark teal surface is a deliberate brand accent block — the floating glass card is the only visual interest.

```css
.hero1B{
  width:1422px;height:800px;
  background:var(--teal-dark);   /* SOLID. No ::before / ::after pattern. */
  position:relative;overflow:hidden;
  font-family:'Geist','Inter',sans-serif;color:#fff;
}

.hero1B .grid{
  position:relative;height:100%;
  display:grid;grid-template-columns:1fr 1fr;align-items:center;
  padding:64px 96px;z-index:2;
}
.hero1B .eb{font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--teal-bright);margin-bottom:28px}
.hero1B h1{font-weight:400;font-size:54px;line-height:1.08;letter-spacing:-.025em;margin-bottom:28px}
.hero1B .lede{font-family:'Inter',sans-serif;font-size:16px;line-height:1.55;color:rgba(255,255,255,.78);max-width:480px;margin-bottom:24px}

/* Wordmark — top-left. USE THE DARK-BG SVG VARIANT from logo-svgs.md */
.hero1B .wordmark{position:absolute;top:40px;left:48px;z-index:3}

/* Subtitle box with L-bracket corners (small UI badge, NOT headline framing) */
.hero1B .subbox{
  position:relative;display:inline-block;
  padding:10px 22px;
  background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.16);
  font-family:'IBM Plex Mono',monospace;font-size:12px;
  font-weight:600;letter-spacing:.16em;text-transform:uppercase;
  color:rgba(255,255,255,.9);
}
.hero1B .subbox::before,.hero1B .subbox::after,
.hero1B .subbox .br1,.hero1B .subbox .br2{
  content:"";position:absolute;width:10px;height:10px;
  border:1.5px solid var(--teal-bright);
}
.hero1B .subbox::before{top:-1px;left:-1px;border-right:0;border-bottom:0}
.hero1B .subbox::after{top:-1px;right:-1px;border-left:0;border-bottom:0}
.hero1B .subbox .br1{bottom:-1px;left:-1px;border-right:0;border-top:0;display:block}
.hero1B .subbox .br2{bottom:-1px;right:-1px;border-left:0;border-top:0;display:block}

/* Floating glass card on the right */
.hero1B .glass{
  background:rgba(255,255,255,.08);
  backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);
  border:1px solid rgba(255,255,255,.14);
  border-radius:16px;padding:28px;
  box-shadow:0 24px 60px rgba(0,0,0,.28);
  justify-self:end;width:520px;
}
```

Inside the glass card: workflow stepper (Sense / Reason / Act), KPI strip, or dashboard fragment.

---

## Format 1C: Split White / Teal with Color-Accent Term

The "What is [term]?" definitional hero. Left side highlights a key term in `--logo-dark`. Right side carries a glass UI on **solid** `--teal-dark`.

**The retired bracket-frame treatment** (four corner L-brackets, gray tinted background, IBM Plex Mono font around the key term) is NOT used. The accent term is plain headline text in `--logo-dark`.

```css
.hero1C{
  width:1422px;height:800px;
  display:grid;grid-template-columns:1fr 1fr;background:#fff;
  font-family:'Geist','Inter',sans-serif;color:var(--ink);
}
.hero1C .left{
  padding:96px 80px;
  display:flex;flex-direction:column;justify-content:center;gap:24px;
}
.hero1C .eb{
  font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;
  letter-spacing:.18em;text-transform:uppercase;color:var(--teal);
}

/* Headline — natural block flow. NO flex-column-with-gap. */
.hero1C h1{
  font-weight:400;font-size:60px;line-height:1.12;
  letter-spacing:-.025em;color:var(--ink);
}
.hero1C h1 .pre,
.hero1C h1 .post,
.hero1C h1 .bracket{
  display:block;font-weight:400;line-height:1.12;
}

/* `.bracket` is just a color wrapper — no padding, no background, no corner brackets */
.hero1C .bracket{color:var(--logo-dark)}

.hero1C .sub{
  font-family:'Inter',sans-serif;font-size:18px;
  color:var(--ink-3);font-weight:500;letter-spacing:-.01em;
}

/* Right panel — SOLID teal-dark. No dots. */
.hero1C .right{
  position:relative;background:var(--teal-dark);
  display:flex;align-items:center;justify-content:center;
  padding:56px;overflow:hidden;
}

/* Glass card inside the right panel (same as 1B's glass) */
.hero1C .glass{
  position:relative;z-index:2;
  background:rgba(255,255,255,.08);
  backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);
  border:1px solid rgba(255,255,255,.14);
  border-radius:14px;padding:24px;width:480px;color:#fff;
  box-shadow:0 20px 50px rgba(0,0,0,.28);
}
```

```html
<div class="hero1C">
  <div class="left">
    <div class="eb">Definition · Metafore for Airlines</div>
    <h1>
      <span class="pre">What is</span>
      <span class="bracket">cognitive ops?</span>
      <span class="post">A guide for airline leaders.</span>
    </h1>
    <p class="sub">Reading every airport, every aircraft and every customer from one shared knowledge fabric — and acting before the duty manager has to ask.</p>
  </div>
  <div class="right">
    <div class="glass">
      <!-- dark-bg Metafore SVG logo + workflow stepper -->
    </div>
  </div>
</div>
```

**Forbidden in 1C:**
- ❌ `display:flex; flex-direction:column; gap:14px` on `h1` (creates inconsistent row heights when lines contain descenders)
- ❌ Monospace font on the accent term
- ❌ Tinted background fill on `.bracket`
- ❌ Four corner L-bracket spans around the accent term
- ❌ Any dot pattern on the right panel — it's solid

---

## Choosing the Right Format

| Blog type | Recommended format | Why |
|---|---|---|
| Data-driven argument (stats, failure rates, comparisons) | **1A — timeline / KPI+bar chart / phase bars** | The card IS the argument |
| Trend or signal story ("before they call") | **1A — sparkline / area chart** | Continuous data with current value |
| General thought leadership, no specific data hook | **1B — solid teal + glass UI card** | Visual interest without requiring specific stats |
| Conceptual / definitional ("What is X?") | **1C — color-accent term** | Emphasizes the key term as plain headline |
