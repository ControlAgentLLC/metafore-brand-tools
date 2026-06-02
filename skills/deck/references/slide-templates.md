# Slide Templates — internal slides

Slides between the cover and the closing. Every template lists its default PPTX tier — pick the one that fits the content, don't force every slide into one template.

All templates assume the slide canvas is `1920×1080`, the `tokens.css` is inlined, and the Metafore wordmark **was placed top-left on the cover**. Every slide *after* the cover carries the icon-only mark (not the wordmark) in the top-right, a section-label eyebrow in the top-left, and the footer line at the bottom — all corner-aligned to `var(--chrome-offset)` (56px), not to content padding.

## Four chrome elements on every content slide

```html
<!-- Top-left — section label (eyebrow) -->
<div class="section-label">THE PROBLEM</div>

<!-- Top-right — icon-only mark.
     Use #icon-light on light surfaces, #icon-dark on --teal-dark surfaces. -->
<svg class="icon-tr" width="72" height="60"><use href="#icon-light"/></svg>

<!-- Footer — bottom, copyright left + page number right -->
<div class="deck-footer" data-pptx-text="footer">
  <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
  <span class="page-num">03 / 12</span>
</div>
```

On `--teal-dark` slides, add `class="on-dark"` to `.section-label` and `.deck-footer`, and switch the icon symbol to `#icon-dark`.

**The full wordmark only appears on slide 1 (cover).** Every subsequent slide — including the closing — uses the icon-only mark. The icon's larger relative weight (48×40 vs the wordmark's previous 110×26) is deliberate: a single mark needs a little more presence than a small wordmark.

**Page numbers live in the bottom-right of the footer**, never top-right.

## Content well rules

- **Vertical centering**: most content slides use `display: flex; flex-direction: column; justify-content: center` so the headline + body sit in the middle of the slide between the top and bottom chrome rows. Don't push content to the top.
- **Padding**: `var(--slide-pad-y)` (96px) top/bottom, `var(--slide-pad-x)` (120px) left/right for the content well. The chrome (icon, section label, footer) sits at the tighter `var(--chrome-offset)` (56px).

---

## Agenda (optional, typically slide 2)

**Tier: `semantic`.** A roadmap of the deck. Use a 2-column numbered grid — items are short titles with a one-line sub-description below each.

Aim for 4–6 items. Below 4 looks thin; above 6 looks like a table of contents for a textbook. **Never an odd-numbered grid of 3** (AI tell triplet).

```html
<section class="slide" data-pptx="semantic" data-slide-id="agenda">
  <div class="agenda">
    <div class="section-label">AGENDA</div>
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-light"><use href="#icon-light"/></svg>

    <div class="header">
      <h2 data-pptx-text="headline">What we'll <span class="accent" data-pptx-accent>cover.</span></h2>
    </div>

    <div class="items">
      <div class="item">
        <div class="a-num">01</div>
        <div class="a-text" data-pptx-text="i1">The Company<span class="a-sub" data-pptx-text="i1-sub">Who Metafore is and how we got here.</span></div>
      </div>
      <div class="item">
        <div class="a-num">02</div>
        <div class="a-text" data-pptx-text="i2">The Problem<span class="a-sub" data-pptx-text="i2-sub">Why a dozen dashboards still can't see the enterprise.</span></div>
      </div>
      <!-- 4–6 items total -->
    </div>

    <!-- Agenda item titles are Title-Case section labels ("The Company",
         "The Problem", "Platform & Integrations", "Deployment") — NOT
         sentences. This is the one place in a deck where headline-style
         sentence case doesn't apply: agenda items are labels, not statements.

         Use "The" where it reads naturally — "The Company", "The Problem",
         "The Architecture", "The MetaWorks Suite" — and drop it where it
         doesn't, typically on compound/plural labels ("Platform & Integrations")
         or standalone process nouns ("Deployment"). Read each title aloud;
         if "The X" sounds awkward, leave the article off. -->

    <div class="deck-footer" data-pptx-text="footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">02 / NN</span>
    </div>
  </div>
</section>
```

```css
.agenda {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--bg);
  padding: var(--slide-pad-y) var(--slide-pad-x);
  display: flex; flex-direction: column; justify-content: center;
}
.agenda .header { margin-bottom: 72px; }
.agenda h2 {
  font-family: var(--header);
  font-weight: 400; font-size: 80px;
  line-height: 1.04; letter-spacing: -2px;
  margin: 0; color: var(--ink);
}
.agenda .items {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 28px 80px; max-width: 1680px;
}
.agenda .item {
  display: grid; grid-template-columns: 100px 1fr;
  gap: 32px; align-items: baseline;
  padding: 24px 0; border-top: 1px solid var(--line);
}
.agenda .item .a-num {
  font-family: var(--mono); font-size: 18px;
  letter-spacing: 0.12em; color: var(--ink-4);
}
.agenda .item .a-text {
  font-family: var(--header); font-weight: 400;
  font-size: 30px; line-height: 1.2;
  letter-spacing: -0.6px; color: var(--ink);
}
.agenda .item .a-text .a-sub {
  display: block; font-family: var(--body);
  font-size: 15px; color: var(--ink-3);
  letter-spacing: 0; margin-top: 6px;
}
```

---

## Company (optional, typically slide 3)

**Tier: `semantic`.** "About Metafore" — mission + facts. Two-column layout: narrative left, fact cards right.

The facts are grey alternate-style cards (no border) — softer than the bordered cards used elsewhere, so the page reads as orientation, not data.

```html
<section class="slide" data-pptx="semantic" data-slide-id="company">
  <div class="company">
    <div class="section-label">THE COMPANY</div>
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-light"><use href="#icon-light"/></svg>

    <div class="left">
      <h2 data-pptx-text="headline">The AI transformation <span class="accent" data-pptx-accent>partner.</span></h2>
      <p class="mission" data-pptx-text="mission">
        Metafore builds cognitive systems that sense, reason, and act across the enterprise.
        We're an AI transformation partner — not a vendor — focused on topline growth, not
        margin cuts. Our platform turns fragmented data into one connected reality and gives
        every function a dedicated intelligence surface on top of it.
      </p>
      <p class="signature" data-pptx-text="signature">Amplify human intelligence.</p>
    </div>

    <div class="right">
      <div class="fact">
        <div class="f-label">HEADQUARTERS</div>
        <div class="f-value">San Francisco<span class="secondary">Global team across NA, EMEA, APAC</span></div>
      </div>
      <div class="fact">
        <div class="f-label">FOUNDED BY</div>
        <div class="f-value">Ori Sasson<span class="secondary">C-level leaders from Amazon, Genesys, Microsoft, VMware, Vodafone</span></div>
      </div>
      <div class="fact">
        <div class="f-label">FLAGSHIP PLATFORM</div>
        <div class="f-value">Metafore One<span class="secondary">MetaWorks operating system · Mira personal agent</span></div>
      </div>
      <div class="fact">
        <div class="f-label">INDUSTRIES</div>
        <div class="f-value">Telecom · Banking · Wealth<span class="secondary">Travel · Health · Supply chain · Public sector</span></div>
      </div>
    </div>

    <div class="deck-footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">03 / NN</span>
    </div>
  </div>
</section>
```

```css
.company {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--bg);
  padding: var(--slide-pad-y) var(--slide-pad-x);
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 80px; align-items: center;
}
.company .left h2 {
  font-family: var(--header); font-weight: 400;
  font-size: 72px; line-height: 1.06; letter-spacing: -1.8px;
  margin: 0 0 32px; color: var(--ink);
}
.company .left .mission {
  font-family: var(--body); font-size: 22px; line-height: 1.55;
  color: var(--ink-2); margin: 0 0 36px; max-width: 640px;
}
.company .left .signature {
  font-family: var(--header); font-weight: 400;
  font-size: 28px; letter-spacing: -0.5px;
  color: var(--logo-dark); margin: 0;
}
.company .right { display: flex; flex-direction: column; gap: 18px; }
.company .right .fact {
  background: var(--card-grey); border-radius: 14px;
  padding: 26px 28px;
  display: grid; grid-template-columns: 220px 1fr;
  gap: 28px; align-items: center;
}
.company .right .fact .f-label {
  font-family: var(--mono); font-weight: 600; font-size: 12px;
  letter-spacing: 0.18em; text-transform: uppercase; color: var(--teal);
}
.company .right .fact .f-value {
  font-family: var(--header); font-weight: 400;
  font-size: 22px; letter-spacing: -0.4px;
  line-height: 1.3; color: var(--ink);
}
.company .right .fact .f-value .secondary {
  font-family: var(--body); font-size: 14px;
  color: var(--ink-3); display: block; margin-top: 4px;
}
```

**What to put in the fact cards.** Pick four facts that orient a stranger to the company: HQ, founding/leadership, flagship product line, industries served. For an investor deck, swap one for funding stage. For a sales deck, swap one for customer count.

---

## Platform capabilities (optional, when the audience cares how)

**Tier: `image`.** A 4×2 grid of platform capability tiles. Use when the audience is technical (CIO, CAIO, architect) and wants to understand the infrastructure underneath the modules.

Cards use the alternate grey-fill style — eight identical tiles in a structured grid. Each carries a small inline SVG icon, a "CAPABILITY NN" eyebrow, a title, and a two-line description.

```html
<section class="slide" data-pptx="image" data-slide-id="platform">
  <div class="platform">
    <div class="section-label">PLATFORM</div>
    <svg class="icon-tr" width="72" height="60"><use href="#icon-light"/></svg>

    <div class="header">
      <h2>The infrastructure that makes the suite <span class="accent">cohesive.</span></h2>
      <p class="lede">Built once for the enterprise. Inherited automatically by every module you activate.</p>
    </div>

    <div class="grid">
      <div class="cap">
        <div class="c-num">CAPABILITY 01</div>
        <svg class="c-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><!-- icon paths --></svg>
        <div class="c-title">Graph Navigator</div>
        <p class="c-body">Visually trace root-cause chains through Reflex, Reflect, Resolve.</p>
      </div>
      <!-- ... 7 more capability tiles ... -->
    </div>

    <div class="deck-footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">NN / NN</span>
    </div>
  </div>
</section>
```

Key CSS:

```css
.platform .grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 18px; height: 480px;
}
.platform .cap {
  background: var(--card-grey); border-radius: 14px;
  padding: 28px; display: flex; flex-direction: column;
}
.platform .cap .c-num {
  font-family: var(--mono); font-size: 11px;
  letter-spacing: 0.18em; color: var(--teal); margin: 0 0 16px;
}
.platform .cap .c-icon {
  width: 32px; height: 32px; margin-bottom: auto; color: var(--logo-dark);
}
.platform .cap .c-title {
  font-family: var(--header); font-weight: 500;
  font-size: 20px; letter-spacing: -0.4px; line-height: 1.2;
  color: var(--ink); margin: 24px 0 8px;
}
.platform .cap .c-body {
  font-family: var(--body); font-size: 13px;
  line-height: 1.5; color: var(--ink-2); margin: 0;
}
```

**Icons are thin-stroke SVG**, inline, in `--logo-dark` color (which the `currentColor` reference picks up). Follow the metafore-graphic Type 9 line-icon spec: stroke-width 1.6, no fill, geometric shapes. **Never** use third-party icon libraries — every icon is hand-drawn SVG in the brand line style.

The canonical eight capabilities (use these, not invented variants):

1. Graph Navigator
2. Notebooks
3. Cognitive Agents
4. AI Copilot
5. Command Hub
6. Operating Plan Bridge
7. Integration layer
8. Industry Ontologies

---

## Integration ecosystem (optional)

**Tier: `image`.** Split-panel slide on `--teal-dark`. Left: hero text framing the integration story. Right: 4 grouped pill clusters showing what Metafore connects to.

Use when the audience cares about *what* the platform integrates with — procurement, IT, technical evaluation. Skip for vision/strategy decks.

```html
<section class="slide" data-pptx="image" data-slide-id="integrate">
  <div class="integrate">
    <div class="section-label on-dark">INTEGRATIONS</div>
    <svg class="icon-tr" width="72" height="60"><use href="#icon-dark"/></svg>

    <div class="left">
      <h2>Built on the stack you <span class="accent-light">already run.</span></h2>
      <p class="body">
        Metafore connects to the systems of record the enterprise already operates. No
        migration, no rip-and-replace. The knowledge graph ingests continuously across
        every connected source, and the agent fleet reasons over them in real time —
        alongside whichever LLM providers fit the deployment.
      </p>
    </div>

    <div class="right">
      <div class="cluster">
        <div class="cl-label">ENTERPRISE SYSTEMS</div>
        <div class="cl-row">
          <span class="pill">Salesforce</span>
          <span class="pill">SAP</span>
          <span class="pill">ServiceNow</span>
          <span class="pill">Workday</span>
          <span class="pill">Oracle</span>
        </div>
      </div>
      <div class="cluster">
        <div class="cl-label">SUPPLY CHAIN</div>
        <div class="cl-row">
          <span class="pill">Kinaxis</span>
          <span class="pill">MercuryGate</span>
          <span class="pill">project44</span>
          <span class="pill">FourKites</span>
        </div>
      </div>
      <div class="cluster">
        <div class="cl-label">LLM PROVIDERS</div>
        <div class="cl-row">
          <span class="pill">Claude</span>
          <span class="pill">Perplexity</span>
          <span class="pill">DeepSeek</span>
          <span class="pill">Custom models</span>
        </div>
      </div>
      <div class="cluster">
        <div class="cl-label">SOURCES</div>
        <div class="cl-row">
          <span class="pill">Company sites</span>
          <span class="pill">File stores</span>
          <span class="pill">REST · GraphQL · gRPC</span>
        </div>
      </div>
    </div>

    <div class="deck-footer on-dark">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">NN / NN</span>
    </div>
  </div>
</section>
```

```css
.integrate {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--teal-dark); color: #fff;
  padding: var(--slide-pad-y) var(--slide-pad-x);
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 80px; align-items: center;
}
.integrate h2 {
  font-family: var(--header); font-weight: 400;
  font-size: 64px; line-height: 1.06; letter-spacing: -1.6px;
  margin: 0 0 32px; color: #fff;
}
.integrate h2 .accent-light { color: var(--teal-on-dark); }
.integrate .body {
  font-family: var(--body); font-size: 20px; line-height: 1.55;
  color: rgba(255,255,255,0.84); margin: 0;
}
.integrate .right { display: flex; flex-direction: column; gap: 22px; }
.integrate .cluster {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 14px; padding: 22px 26px;
}
.integrate .cluster .cl-label {
  font-family: var(--mono); font-size: 12px;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--teal-on-dark); margin: 0 0 16px;
}
.integrate .cluster .cl-row { display: flex; flex-wrap: wrap; gap: 8px; }
.integrate .cluster .pill {
  font-family: var(--mono); font-size: 14px;
  letter-spacing: 0.04em; color: rgba(255,255,255,0.92);
  padding: 9px 14px;
  border: 1px solid rgba(255,255,255,0.18); border-radius: 999px;
  background: rgba(255,255,255,0.04);
}
```

**Use real system names**, not categories — "Salesforce" not "CRM system", "Claude" not "LLM provider". The credibility of this slide is in the specific names.

---

## Section divider

**Tier: `semantic`** by default.

A full-bleed teal panel announcing a section. Left-aligned hero — keep my divider gravity (left), not centered.

```html
<section class="slide" data-pptx="semantic" data-slide-id="sec-01">
  <div class="divider">
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-dark"><use href="#icon-dark"/></svg>

    <div class="textwell">
      <div class="eyebrow" data-pptx-text="eyebrow">SECTION 01 · WHERE THE WORK BREAKS</div>
      <h1 data-pptx-text="headline">
        Care teams spend more time
        <span class="accent-light" data-pptx-accent="light">finding context</span>
        than resolving tickets.
      </h1>
    </div>

    <div class="deck-footer on-dark" data-pptx-text="footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">03 / 12</span>
    </div>
  </div>
</section>
```

```css
.divider {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--teal-dark);
  color: #fff;
  padding: var(--slide-pad-y) var(--slide-pad-x);
  display: flex; flex-direction: column; justify-content: center;
}
.divider .eyebrow { color: rgba(255,255,255,0.7); margin-bottom: 28px; }
.divider h1 {
  font-family: var(--header);
  font-weight: 400;
  font-size: 80px;
  line-height: 1.08;
  letter-spacing: -2px;
  margin: 0;
  max-width: 1480px;
}
.divider h1 .accent-light { color: var(--teal-on-dark); }
```

**Why `--teal-on-dark` for the accent on dark.** `--logo-dark` (`#035657`) is too close to `--teal-dark` (`#004D50`) to read on a teal background. `--teal-on-dark` (`#88DCE0`) is the dark-surface equivalent (replacing the retired `#00C4CC`/`#00989E`). The PPTX run-split uses `#FFFFFF` + `#88DCE0` for these (the standard light-surface pair is ink + `--logo-dark`).

---

## Title + body

**Tier: `semantic`.** The most common internal slide. Single big idea, supporting paragraph.

```html
<section class="slide" data-pptx="semantic" data-slide-id="04-what">
  <div class="title-body">
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-light"><use href="#icon-light"/></svg>

    <div class="textwell">
      <div class="eyebrow" data-pptx-text="eyebrow">WHAT METAFORE DOES</div>
      <h2 data-pptx-text="headline">
        Sense, reason, and act —
        <span class="accent" data-pptx-accent>at enterprise scale.</span>
      </h2>
      <p class="body" data-pptx-text="body">
        Metafore One is a cognitive system. It senses signals across your
        operating estate, reasons over them with a knowledge fabric grounded
        in your policies and data, and acts through orchestrated workflows
        across your existing systems. Every action carries a trace and a
        reason — auditable by design.
      </p>
    </div>

    <div class="deck-footer" data-pptx-text="footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">04 / 12</span>
    </div>
  </div>
</section>
```

```css
.title-body {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--bg);
  padding: 140px var(--slide-pad-x);
}
.title-body .textwell { max-width: 1320px; }
.title-body .eyebrow { margin-bottom: 28px; }
.title-body h2 {
  font-family: var(--header);
  font-weight: 400;
  font-size: 64px;
  line-height: 1.08;
  letter-spacing: -1.8px;
  margin: 0 0 40px;
  color: var(--ink);
}
.title-body .body {
  font-family: var(--body);
  font-size: 26px;
  line-height: 1.55;
  color: var(--ink-2);
  max-width: 1180px;
}
```

---

## Two-column

**Tier: `semantic`.** Two ideas in parallel — comparison, before/after, definition + example.

Avoid **three** columns (triplet AI tell). If you need three things, use a 2x2 grid with the fourth cell as a takeaway, or split across two slides.

```html
<section class="slide" data-pptx="semantic" data-slide-id="05-compare">
  <div class="two-col">
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-light"><use href="#icon-light"/></svg>

    <div class="header">
      <div class="eyebrow" data-pptx-text="eyebrow">BEFORE VS. WITH METAFORE</div>
      <h2 data-pptx-text="headline">From signal triage to orchestrated resolution.</h2>
    </div>

    <div class="cols">
      <div class="col">
        <div class="col-label" data-pptx-text="col-1-label">TODAY</div>
        <p class="col-body" data-pptx-text="col-1-body">
          Network alerts route to one queue, customer signals to another,
          billing exceptions to a third. Each team chases its own slice.
          The customer waits while context is reassembled across systems.
        </p>
      </div>
      <div class="col">
        <div class="col-label" data-pptx-text="col-2-label">WITH METAFORE</div>
        <p class="col-body" data-pptx-text="col-2-body">
          One cognitive agent reasons across every signal stream with the
          carrier knowledge fabric. The customer hears from Mira before
          they notice the outage. Resolution arrives ahead of the call.
        </p>
      </div>
    </div>

    <div class="deck-footer" data-pptx-text="footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">05 / 12</span>
    </div>
  </div>
</section>
```

```css
.two-col {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--bg);
  padding: 120px var(--slide-pad-x) var(--slide-pad-y);
}
.two-col .header { margin-bottom: 80px; max-width: 1320px; }
.two-col .header .eyebrow { margin-bottom: 24px; }
.two-col .header h2 {
  font-family: var(--header);
  font-weight: 400;
  font-size: 52px;
  line-height: 1.08;
  letter-spacing: -1.4px;
  margin: 0;
  color: var(--ink);
}
.two-col .cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
}
.two-col .col-label {
  font-family: var(--mono);
  font-size: 13px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--teal);
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--line);
}
.two-col .col-body {
  font-family: var(--body);
  font-size: 22px;
  line-height: 1.55;
  color: var(--ink-2);
  margin: 0;
}
```

---

## KPI band

**Tier: `image`.** A full-bleed `--teal-dark` band with 2 or 4 stat cells. Use after a customer-outcome section to anchor the outcome.

Never **three** KPI cells. Two or four.

```html
<section class="slide" data-pptx="image" data-slide-id="06-kpi">
  <div class="kpi-band">
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-dark"><use href="#icon-dark"/></svg>

    <div class="eyebrow eyebrow-light">OUTCOMES · 90 DAYS</div>

    <div class="grid">
      <div class="cell">
        <div class="num">47%</div>
        <div class="label">Less time per ticket</div>
      </div>
      <div class="cell">
        <div class="num">3.2×</div>
        <div class="label">First-contact resolution</div>
      </div>
      <div class="cell">
        <div class="num">88%</div>
        <div class="label">Proactive contact rate</div>
      </div>
      <div class="cell">
        <div class="num">$4.1M</div>
        <div class="label">Annualized OpEx delta</div>
      </div>
    </div>

    <div class="deck-footer on-dark">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">06 / 12</span>
    </div>
  </div>
</section>
```

```css
.kpi-band {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--teal-dark);
  color: #fff;
  padding: 140px var(--slide-pad-x);
  display: flex; flex-direction: column; justify-content: center;
}
.kpi-band .eyebrow-light {
  color: rgba(255,255,255,0.7);
  margin-bottom: 80px;
}
.kpi-band .grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 64px;
}
.kpi-band .num {
  font-family: var(--header);
  font-weight: 400;
  font-size: 132px;
  line-height: 0.95;
  letter-spacing: -3px;
  margin-bottom: 28px;
  color: #fff;
}
.kpi-band .label {
  font-family: var(--mono);
  font-size: 14px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--teal-on-dark);
  max-width: 240px;
  line-height: 1.4;
}
```

**Tier rationale.** The KPI band is a visual composition — the giant numbers, the teal field, the labels are the entire slide. Rendering as PNG preserves typography fidelity better than fighting PowerPoint's text rendering at 132px.

---

## Illustrated tile grid (adapted from the brochure pattern library)

**Tier: `image`.** A 3-up or 4-up grid where each tile carries a thin-line SVG diagram above the copy. Adapted from the brochure's "3-up illustrated" capability pattern (see `metafore-brochure/references/pattern-library-DRAFT.md`).

The illustration is the carrier of meaning — each diagram should be specific to its tile's concept, not generic decoration. Use this pattern when the tiles represent abstract architectural ideas that benefit from a visual mark (e.g. the four-graph foundation, platform principles, transformation pillars). Don't use it for operational content that's already prose-heavy.

```html
<div class="tile-grid">
  <div class="tile t1">
    <div class="t-illust">
      <svg viewBox="0 0 400 140" fill="none" stroke="#999" stroke-width="1.4" aria-hidden="true">
        <!-- Concept-specific line-art SVG goes here.
             See illustration style notes below. -->
      </svg>
    </div>
    <div class="t-num">PILLAR 01 — TAG</div>
    <div class="t-name">Pillar headline.</div>
    <p class="t-body">Body copy that takes the diagram's idea and applies it operationally.</p>
  </div>
  <!-- 2–3 more tiles -->
</div>
```

```css
.tile-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; height: 600px; }
.tile {
  background: var(--panel); border: 1px solid var(--line); border-radius: 14px;
  padding: 32px 32px 36px; display: flex; flex-direction: column;
}
.tile .t-illust {
  width: 100%; height: 140px;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 28px; padding-bottom: 24px;
  border-bottom: 1px solid var(--line);
}
.tile .t-illust svg {
  max-width: 100%; max-height: 100%;
  stroke-linecap: round; stroke-linejoin: round;
}
.tile .t-num {
  font-family: var(--mono); font-size: 12px;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--teal); margin: 0 0 16px;
}
/* All tile eyebrows share a single color — see pattern-library.md P-06 for the rationale */
.tile .t-num { color: var(--teal); }
.tile .t-name {
  font-family: var(--header); font-weight: 400;
  font-size: 28px; line-height: 1.1; letter-spacing: -0.7px;
  color: var(--ink); margin: 0 0 16px;
}
.tile .t-body {
  font-family: var(--body); font-size: 14px; line-height: 1.55;
  color: var(--ink-2); margin: 0;
}
```

### Illustration sourcing — pull from `Graphics/LineIcons/` FIRST

A library of pre-designed line-art icons lives at `Marketing Design/Graphics/LineIcons/`. These are the canonical illustration set for Metafore decks and brochures — sharing them across pieces is the whole point of having the library.

**Before generating a new SVG, scan the library.** Read the relevant PNGs and pick the closest match. Only fall back to a custom SVG when no library icon fits.

Library catalog (PNG, ~1400×800 each, thin grey strokes with occasional filled black square accent):

| Icon file | Visual | Best for |
|---|---|---|
| `Amplify.png` | Concentric radiating arcs | Amplification, broadcast, growth |
| `Axis.png` | Coordinate plane + crossed ellipses + center mark | Measurement, governance, oversight, control |
| `Collaborate.png` | Interlocking figures | Teamwork, multi-agent coordination |
| `Connect.png` | Two shapes joined | Integration, pairing, handshake |
| `Connected.png` | Multi-point connection | Network, ecosystem |
| `CrossSell.png` | Crossing arrows / X pattern | Cross-functional, intersection |
| `Cycle.png` | Circular flow | Loop, iteration, continuous process |
| `Detection.png` | Radar / scan visual | Sensing, anomaly detection |
| `Ellipses.png` | Stacked / overlapping ellipses | Layers, abstraction |
| `Ensemble.png` | Group of shapes | Collection, fleet, suite |
| `Fan.png` | Radiating lines | Distribution, broadcast |
| `Integration.png` | Joined systems | Stack integration, pipes |
| `Measure.png` | Ruler / gauge | Metrics, benchmarking |
| `NestedSquares.png` | Concentric squares | Scope, containment, framing |
| `Nodes.png` | Connected dots in a circle | Knowledge graph, network |
| `Nodes2.png` | Alternate node network | Distributed system |
| `Orbit.png` | Orbiting paths | Coverage, sweep, rotation |
| `Process.png` | Stepped flow | Workflow, pipeline |
| `Scale.png`, `Scale2.png` | Growth / step progression | Scaling, expansion |
| `Squares.png`, `Squares2.png` | Square grids | Structure, modules |
| `Stack.png` | Isometric layered diamonds | Architecture, layers, structural foundation |
| `ThroughLine.png` | Stacked ovals + arrow through | Signal-to-context, filter, lens |
| `Transform.png` | Shape morphing | Change, transformation |
| `Venn.png` | Overlapping circles | Intersection, shared scope |

**Workflow:**

1. For each tile, write the concept in one phrase ("connective tissue", "signal in / context out", "structural layers", "action layer + measurement").
2. Scan the catalog table above for a match.
3. View the PNG (Read the file) to confirm the visual reads as the concept intends.
4. Copy the PNG into the deck's `_assets/icons/` folder.
5. Reference via `<img src="_assets/icons/Nodes.png" alt="" aria-hidden="true">` inside the `.t-illust` container.

Only fall back to writing a custom SVG when **no** library icon reads as the concept — and even then, match the library's style: `#999` default stroke, `#666` emphasis, no fills except a small filled black square (~12×12) as the recurring focal-point accent. ViewBox roughly 400×140 for a 4-up tile.

### Example: four-graph slide illustrations (MetaWorks deck slide 5)

All four pulled from the LineIcons library, no custom SVGs needed:

| Tile | Icon | Concept |
|---|---|---|
| Knowledge | `Nodes.png` | Network of connected nodes in a containing circle |
| Context | `ThroughLine.png` | Stacked translucent lenses with dashed signal passing through, arrow exiting right |
| Meta | `Stack.png` | Three isometric diamonds layered, middle emphasized in black |
| Control | `Axis.png` | Parallelogram plane intersected by crossed ellipses and a coordinate axis, filled square at origin |

Don't reuse the same icon across multiple tiles in the same slide. Spread the library — each tile earns a distinct visual.

---

## Card grid — default and alternate card styles

Two card styles. Use the default (white + 1px border) by default. Use the alternate (grey fill, no border) when you want a softer, less rule-heavy surface — typically for problem/team/value-prop slides where the cards carry icon-headline-body content rather than data.

### Default card

```css
.card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 36px;
}
```

### Alternate card (grey fill)

```css
.card.alt {
  background: var(--card-grey);      /* #F4F4F4 */
  border: none;
  border-radius: 16px;
  padding: 36px;
}
```

The default card sits cleanly on white or `--bg-solid`. The alternate card needs a white or `--bg-solid` background to read as elevated — don't put grey-fill cards on a grey-fill section background.

---

## Team / track record

**Tier: `semantic`.** A near-the-top slide that establishes credibility before the product pitch. Copy block left, 2×2 grid of credibility cards right (companies the team came from, prior product categories defined, customer counts, etc.).

```html
<section class="slide" data-pptx="semantic" data-slide-id="01-team">
  <div class="team">
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-light"><use href="#icon-light"/></svg>

    <div class="left">
      <div class="eyebrow" data-pptx-text="eyebrow">TEAM</div>
      <h2 data-pptx-text="headline">
        A proven
        <span class="accent" data-pptx-accent>track record.</span>
      </h2>
      <p class="body" data-pptx-text="body">
        Our core team holds C-level experience at Amazon, Genesys, Jitterbit,
        Microsoft, Mobileum, Scopus, VMware, and Vodafone.
      </p>
    </div>

    <div class="right">
      <div class="grid">
        <div class="card alt">
          <div class="c-num" data-pptx-text="c1-num">01</div>
          <h3 class="c-title" data-pptx-text="c1-title">Defined the CRM solution industry</h3>
          <p class="c-body" data-pptx-text="c1-body">Spearheaded the creation and evolution of Customer Relationship Management as a core enterprise function.</p>
        </div>
        <div class="card alt">
          <div class="c-num" data-pptx-text="c2-num">02</div>
          <h3 class="c-title" data-pptx-text="c2-title">Invented enterprise application integration</h3>
          <p class="c-body" data-pptx-text="c2-body">Developed the frameworks that enabled complex systems to work together — laying the groundwork for modern enterprise stacks.</p>
        </div>
        <div class="card alt">
          <div class="c-num" data-pptx-text="c3-num">03</div>
          <h3 class="c-title" data-pptx-text="c3-title">Transformed enterprise call centers</h3>
          <p class="c-body" data-pptx-text="c3-body">Built foundational call-center technologies that set the standard for global customer-support operations.</p>
        </div>
        <div class="card alt">
          <div class="c-num" data-pptx-text="c4-num">04</div>
          <h3 class="c-title" data-pptx-text="c4-title">Led the world's largest mobile operator group</h3>
          <p class="c-body" data-pptx-text="c4-body">Oversaw growth and innovation at unparalleled scale in the telecommunications industry.</p>
        </div>
      </div>
    </div>

    <div class="deck-footer" data-pptx-text="footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">02 / 12</span>
    </div>
  </div>
</section>
```

```css
.team {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--bg);
  padding: var(--slide-pad-y) var(--slide-pad-x);
  display: grid;
  grid-template-columns: 480px 1fr;
  gap: 80px;
  align-items: center;
}
.team .left .eyebrow { margin-bottom: 28px; }
.team .left h2 {
  font-family: var(--header);
  font-weight: 400;
  font-size: 72px;
  line-height: 1.06;
  letter-spacing: -1.8px;
  margin: 0 0 32px;
  color: var(--ink);
}
.team .left .body {
  font-family: var(--body);
  font-size: 20px;
  line-height: 1.55;
  color: var(--ink-3);
}
.team .right .grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.team .card.alt { min-height: 280px; display: flex; flex-direction: column; }
.team .card.alt .c-num {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.16em;
  color: var(--ink-3);
  margin: 0 0 auto;          /* anchors the rest to the bottom */
}
.team .card.alt .c-title {
  font-family: var(--header);
  font-weight: 500;
  font-size: 22px;
  line-height: 1.25;
  letter-spacing: -0.4px;
  color: var(--ink);
  margin: 32px 0 12px;
}
.team .card.alt .c-body {
  font-family: var(--body);
  font-size: 14px;
  line-height: 1.5;
  color: var(--ink-2);
  margin: 0;
}
```

**When to place.** Typically slide 02 (right after the cover) on outbound sales decks. Skip on internal decks where credibility isn't the gate.

---

## Industries — single slide OR per-vertical

**Two modes.** Use whichever fits the deck length:

### Mode A — grouped (single slide)

**Tier: `semantic`** with `image` for the visual right panel.

One slide listing the verticals as cards (Banking, Telecom, Travel, Health, Supply Chain). Use when the deck is short and verticals are not the focus.

```html
<section class="slide" data-pptx="semantic" data-slide-id="04-industries">
  <div class="industries-grouped">
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-light"><use href="#icon-light"/></svg>

    <div class="header">
      <div class="eyebrow" data-pptx-text="eyebrow">INDUSTRIES</div>
      <h2 data-pptx-text="headline">
        Cognitive agents across every
        <span class="accent" data-pptx-accent>regulated industry.</span>
      </h2>
    </div>

    <div class="grid">
      <div class="card alt">
        <h3 class="i-name" data-pptx-text="b-name">Banking</h3>
        <p class="i-body" data-pptx-text="b-body">Self-evolving agents that reason, plan, and act across customer service, compliance, and operations.</p>
      </div>
      <div class="card alt">
        <h3 class="i-name" data-pptx-text="t-name">Telecommunications</h3>
        <p class="i-body" data-pptx-text="t-body">Service, billing, and network operations through cognitive orchestration.</p>
      </div>
      <div class="card alt">
        <h3 class="i-name" data-pptx-text="r-name">Travel</h3>
        <p class="i-body" data-pptx-text="r-body">Booking, preparedness, and disruption resolution across the full travel lifecycle.</p>
      </div>
      <div class="card alt">
        <h3 class="i-name" data-pptx-text="h-name">Health</h3>
        <p class="i-body" data-pptx-text="h-body">Patient navigation, care coordination, and revenue-cycle management.</p>
      </div>
    </div>

    <div class="deck-footer" data-pptx-text="footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">04 / 12</span>
    </div>
  </div>
</section>
```

### Mode B — per-vertical (one slide each)

**Tier: `hybrid`.** One slide per vertical. Bullet list left + a placeholder area right for a screenshot or composite image.

```html
<section class="slide" data-pptx="hybrid" data-slide-id="04a-banking">
  <div class="industry">
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-light"><use href="#icon-light"/></svg>

    <div class="left">
      <div class="eyebrow" data-pptx-text="eyebrow">INDUSTRIES</div>
      <h1 data-pptx-text="headline">Banking.</h1>
      <p class="lede" data-pptx-text="lede">
        Self-evolving agents that reason, plan, and act across customer
        service, compliance, and operations.
      </p>
      <div class="bullets card alt">
        <div class="b-row">
          <strong data-pptx-text="b1-title">Accelerated time-to-value.</strong>
          <p data-pptx-text="b1-body">Modular agents deploy in weeks, not years.</p>
        </div>
        <div class="b-row">
          <strong data-pptx-text="b2-title">Built-in governance.</strong>
          <p data-pptx-text="b2-body">Every action is explainable, auditable, and compliant.</p>
        </div>
        <div class="b-row">
          <strong data-pptx-text="b3-title">Domain rewiring.</strong>
          <p data-pptx-text="b3-body">High-impact subdomains like lending, onboarding, or risk capture 70–80% of value.</p>
        </div>
        <div class="b-row">
          <strong data-pptx-text="b4-title">Cognitive decisioning hub.</strong>
          <p data-pptx-text="b4-body">Reasoning embedded in processes for 20–60% productivity gains.</p>
        </div>
      </div>
    </div>

    <div class="right">
      <!-- Image placeholder — drop a screenshot, conversational mock, or product capture.
           This area renders as part of the PNG background for the hybrid tier. -->
      <div class="placeholder">SCREENSHOT / PRODUCT CAPTURE</div>
    </div>

    <div class="deck-footer" data-pptx-text="footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">04 / 12</span>
    </div>
  </div>
</section>
```

```css
.industry {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--bg);
  padding: var(--slide-pad-y) var(--slide-pad-x);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}
.industry h1 {
  font-family: var(--header);
  font-weight: 400;
  font-size: 120px;
  letter-spacing: -3px;
  margin: 24px 0 32px;
  color: var(--ink);
}
.industry .lede {
  font-family: var(--body);
  font-size: 22px;
  line-height: 1.45;
  color: var(--ink-3);
  margin: 0 0 40px;
  max-width: 580px;
}
.industry .bullets.alt { padding: 32px; }
.industry .b-row { padding: 16px 0; border-top: 1px solid var(--line); }
.industry .b-row:first-child { border-top: 0; padding-top: 0; }
.industry .b-row strong {
  font-family: var(--header);
  font-weight: 500;
  font-size: 17px;
  color: var(--ink);
  display: block;
  margin-bottom: 4px;
}
.industry .b-row p {
  font-family: var(--body);
  font-size: 14px;
  line-height: 1.5;
  color: var(--ink-3);
  margin: 0;
}
.industry .placeholder {
  background: var(--card-grey);
  border-radius: 16px;
  aspect-ratio: 4 / 3;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: 0.16em;
  color: var(--ink-4);
}
```

---

## System architecture — placeholder only

**Tier: `image`.** A dense multi-column layout for showing platform/system architecture (User Experience / Orchestration / Intelligence / Integration / Platform / Deployment style). Used in the prior corp deck.

**This is a placeholder template, intentionally low-fidelity.** Use it as a stand-in when a deck needs an architecture slide; replace with a real, designed diagram before delivery. **Do not reuse this layout for any non-architecture slide.**

```html
<section class="slide" data-pptx="image" data-slide-id="11-arch">
  <div class="arch">
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-dark"><use href="#icon-dark"/></svg>

    <div class="header">
      <div class="eyebrow on-dark">SYSTEM ARCHITECTURE</div>
      <h2>CtrlAgent architecture.</h2>
    </div>

    <div class="cols">
      <div class="col">
        <div class="col-head">User Experience</div>
        <p class="col-sub">Generative and branded interfaces across all touchpoints</p>
        <div class="chip">Generative UI</div>
        <div class="chip">Text Interface</div>
        <div class="chip">Pulse</div>
        <div class="chip">Voice Gateway</div>
        <div class="chip">Branded UI</div>
        <div class="chip">Extensible UI Controls</div>
      </div>
      <!-- ...repeat for Orchestration / Intelligence / Integration / Platform / Deployment... -->
    </div>

    <div class="deck-footer on-dark">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">11 / 12</span>
    </div>
  </div>
</section>
```

```css
.arch {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--teal-dark);
  color: #fff;
  padding: 96px var(--slide-pad-x);
}
.arch .header h2 {
  font-family: var(--header);
  font-weight: 400;
  font-size: 72px;
  letter-spacing: -1.8px;
  margin: 16px 0 56px;
}
.arch .cols { display: grid; grid-template-columns: repeat(6, 1fr); gap: 18px; }
.arch .col-head {
  font-family: var(--header);
  font-size: 22px;
  margin-bottom: 6px;
}
.arch .col-sub {
  font-family: var(--body);
  font-size: 12px;
  line-height: 1.4;
  color: rgba(255,255,255,0.6);
  margin: 0 0 20px;
  min-height: 48px;
}
.arch .chip {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.10em;
  text-transform: none;
  color: rgba(255,255,255,0.85);
  padding: 10px 14px;
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 8px;
  margin-bottom: 8px;
}
```

---

## Pulse / capability grid

**Tier: `image`.** A grid of 4 or 6 capability tiles, each with a small mock UI. Always uses one of the Type 4 illustrations from `metafore-graphic` — call into that skill's recipes rather than duplicating them. Renders as PNG.

The slide's title and eyebrow may be `hybrid` (editable) if the grid below them is the visual payload.

```html
<section class="slide" data-pptx="hybrid" data-slide-id="07-cap">
  <div class="cap-grid">
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-light"><use href="#icon-light"/></svg>

    <div class="header">
      <div class="eyebrow" data-pptx-text="eyebrow">PULSE FOR CARE OPS</div>
      <h2 data-pptx-text="headline">
        Six surfaces, one
        <span class="accent" data-pptx-accent>operating view.</span>
      </h2>
    </div>

    <div class="tiles"><!-- 4 or 6 capability tiles per metafore-graphic Type 4 --></div>

    <div class="deck-footer" data-pptx-text="footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">07 / 12</span>
    </div>
  </div>
</section>
```

---

## Pull-quote

**Tier: `image`.** Big quote from a customer or analyst. White background, solid 8px `--teal-dark` left edge.

```html
<section class="slide" data-pptx="image" data-slide-id="08-quote">
  <div class="pull-quote">
    <svg class="icon-tr" width="72" height="60" data-pptx-image="icon-light"><use href="#icon-light"/></svg>

    <div class="bar"></div>

    <div class="content">
      <div class="quote-glyph">"</div>
      <p class="quote">
        Metafore didn't just automate our tier-one work — it changed
        what tier-one <span class="accent">means</span>.
      </p>
      <div class="attribution">
        <span class="who">Maya Reyes</span>
        <span class="role">VP, Customer Operations · Carrier X</span>
      </div>
    </div>

    <div class="deck-footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">08 / 12</span>
    </div>
  </div>
</section>
```

```css
.pull-quote {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--bg);
  padding: var(--slide-pad-y) var(--slide-pad-x);
  display: flex; align-items: center;
}
.pull-quote .bar {
  position: absolute;
  left: 0; top: 0;
  width: 8px; height: 100%;
  background: var(--teal-dark);
}
.pull-quote .content { max-width: 1480px; }
.pull-quote .quote-glyph {
  font-family: var(--header);
  font-size: 180px;
  line-height: 0.6;
  color: var(--teal);
  margin-bottom: 24px;
}
.pull-quote .quote {
  font-family: var(--header);
  font-weight: 400;
  font-size: 72px;
  line-height: 1.18;
  letter-spacing: -1.6px;
  color: var(--ink);
  margin: 0 0 48px;
}
.pull-quote .quote .accent { color: var(--logo-dark); }
.pull-quote .attribution {
  display: flex; align-items: baseline; gap: 16px;
}
.pull-quote .attribution .who {
  font-family: var(--header);
  font-size: 24px;
  color: var(--ink);
}
.pull-quote .attribution .role {
  font-family: var(--body);
  font-size: 20px;
  color: var(--ink-3);
}
```

---

## Closing slide

**Tier: `semantic`.** The final slide. CTA + Metafore wordmark. The logo on the closing slide returns to **top-left** (it's the closing book-end, mirroring the cover).

```html
<section class="slide" data-pptx="semantic" data-slide-id="closing">
  <div class="closing">

    <!-- Closing logo returns top-left, like the cover -->
    <div class="logo" data-pptx-image="logo-light">
      <!-- logo-light.svg @ 155×36 -->
    </div>

    <div class="textwell">
      <div class="eyebrow" data-pptx-text="eyebrow">NEXT STEP</div>
      <h1 data-pptx-text="headline">
        Let's design your
        <span class="accent" data-pptx-accent>first cognitive workflow.</span>
      </h1>
      <p class="cta-line" data-pptx-text="cta-line">
        david.sasson@metafore.ai · metafore.ai
      </p>
    </div>

    <div class="deck-footer" data-pptx-text="footer">
      <span class="copy-line">© 2026 METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL</span>
      <span class="page-num">12 / 12</span>
    </div>
  </div>
</section>
```

```css
.closing {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  background: var(--bg);
  padding: var(--slide-pad-y) var(--slide-pad-x);
  display: flex; flex-direction: column; justify-content: center;
}
.closing .logo {
  position: absolute;
  top: var(--logo-offset);
  left: var(--logo-offset);
}
.closing .textwell { max-width: 1480px; }
.closing .eyebrow { margin-bottom: 32px; }
.closing h1 {
  font-family: var(--header);
  font-weight: 400;
  font-size: 96px;
  line-height: 1.04;
  letter-spacing: -2.4px;
  margin: 0 0 48px;
  color: var(--ink);
}
.closing .cta-line {
  font-family: var(--mono);
  font-size: 24px;
  letter-spacing: 0.04em;
  color: var(--teal);
  margin: 0;
}
```

---

## When to make a slide `image` vs `semantic`

**Default to `semantic`** — text stays editable, file size is small, accessibility works, speaker notes integrate.

**Promote to `image` when:**

- A typographic element is large enough that PowerPoint's text rendering would look noticeably different from the HTML (anything over ~96px display type).
- The slide is a composition (KPI band, pull-quote, capability grid, complex chart) where editing one piece without the others would break the design.
- The slide contains glassmorphism, dot grids, or custom SVG visualizations that PPT can't reproduce natively.

**Promote to `hybrid` when:**

- The background visual must stay locked but at least one text node (usually the title) needs to remain editable for client customization.
- A cover slide — always.
- An industry slide where the screenshot/photo area stays locked but the bullet copy must be editable.
