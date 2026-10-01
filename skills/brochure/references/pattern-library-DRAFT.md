# Pattern Library — DRAFT

**Status:** Working draft, not loaded by `SKILL.md` by default. Read this when you want concrete HTML snippets for common section patterns, but do not treat it as exhaustive. If a section the content needs isn't here, compose it from the design tokens directly. If you find yourself using a pattern often that isn't documented, that's worth adding when the library is promoted out of draft.

**Why this is separate from `SKILL.md`:** Brochure structure should be content-determined. Bundling a fixed catalog of patterns into the skill would push the model toward template-matching rather than reading the content first. This file is for inspiration and copy-pasteable starting points, not for routing decisions.

> **Typography override — read first.** The canonical type system is defined in `../assets/tokens.css` and described in `../SKILL.md` under "Type scale". When a CSS snippet below conflicts with the canonical system, the canonical system wins. Specifically:
>
> - **Tracking is 0 everywhere.** Ignore any `letter-spacing` values in this file (negative on headers or positive on eyebrows/labels). Strip them.
> - **Line-height is 1.125 on headers, 1.200 on body, lede, eyebrow.** Replace any `line-height: 72px / 28px / 22px / 26px / 1` style values with the unitless ratios.
> - **Header sizes** follow the Perfect Fifth scale on an 18px body (H1 40 / H2 27 / H3 21, lede 21) with auto-shrink to the floor (H1 32 / H2 24). Body, lede, eyebrow (13px) and captions (15px) never shrink. Nothing essential below 15px.
> - **Every section carries a visual** (library line icon via `src="@icon:Name"`, diagram, UI card, KPI band, or pull quote), and no paragraph runs past three lines — see the brand pack §2.
> - **Margins** between H1, H2, and body are proportional to each element's font-size (see `tokens.css`); do not hand-tune.

---

## Table of contents

- [Hero variants](#hero-variants)
  - Hero A — Left text + right UI-card
  - Hero B — Full-width centered
  - Hero C — Text + 3-stat split
- [Pillar cards](#pillar-cards) — 2–4 thematic cards, single teal bar
- [Capability grids](#capability-grids) — 2×2, 3-up, 4-up, 3-up illustrated
- [Comparison table](#comparison-table) — "with Metafore" vs status quo
- [KPI band](#kpi-band) — tealDark fill, 3 or 4 cells
- [Process timeline](#process-timeline) — numbered step sequence
- [Quote pull](#quote-pull) — customer voice
- [Callout strip](#callout-strip) — Shadow Panel-style eyebrow + body grid
- [Outcome band](#outcome-band) — teal fill, white text
- [FAQ block](#faq-block)
- [Footer](#footer)

---

## Hero variants

### Hero A — Left text + right UI-card
**When to use:** When the brochure has a hero product story plus a representative artifact worth showing (a card, a metric, a live mockup). Most product overviews.
**When to skip:** When there's no obvious "right side" artifact — a forced empty card looks worse than a centered hero.
**Min/max:** 1 headline + 1 lede + (optional) stat split, plus a single right-side card.

```html
<div class="hero">
  <div class="hero-left">
    <p class="audience-tag">Eyebrow / audience tag</p>
    <h1>Lead phrase in ink, last word in <span class="accent">teal</span>.</h1>
    <p class="lede">Lede paragraph. Keep to one substantive sentence or two short ones — no negation pivots, no "X, not Y" framing.</p>
  </div>
  <div class="hero-right">
    <!-- UI card or representative artifact -->
  </div>
</div>
```

CSS pattern:
```css
.hero { display: grid; grid-template-columns: 1fr 480px; gap: 80px; align-items: start; container-type: inline-size; }
.hero h1 { font-family: var(--header); font-weight: 400;
           font-size: clamp(var(--h1-floor), 6.5cqw, var(--h1-size));
           line-height: var(--lh-header); letter-spacing: var(--tracking); margin: 0;
           max-width: var(--h1-max-width); }
.hero h1 .accent { color: var(--logo-dark); }
.lede { font-size: var(--lede-size); line-height: var(--lh-body); color: var(--ink-2);
        margin: calc(var(--lede-size) * 0.8) 0 0; max-width: 620px; }
```

### Hero B — Full-width centered
**When to use:** Manifesto-style pieces, single-thesis statements, vertical-specific briefs where the message is the artifact.
**When to skip:** Anything operationally detailed — a centered hero suggests minimalism, which fights with a content-dense brochure.
**Min/max:** 1 headline + 1 lede only. No card.

Notes: Even though body copy is never centered, a single hero block can be center-aligned for this variant. Keep max-width ≤ 1100px so it doesn't sprawl.

### Hero C — Text + 3-stat split
**When to use:** When three quantified facts are part of the hero's punch (e.g. "0 lines of code · 100% governance · 1 conversation"). The stat split sits under the lede, separated by a hairline.
**When to skip:** When the stats are weak or noisy — forcing three numbers when only one is impressive dilutes all of them.

```html
<div class="stat-split">
  <div class="stat"><div class="s-num">0</div><div class="s-cap">Lines of code</div></div>
  <div class="stat"><div class="s-num">100%</div><div class="s-cap">Governance</div></div>
  <div class="stat"><div class="s-num">1</div><div class="s-cap">Conversation</div></div>
</div>
```

---

## Pillar cards

Cards introducing the major themes the brochure will cover. Every card carries the same 3px `--teal` top bar and a library line icon — no color rotation across cards (it reads as inconsistency, and `--teal-accent` is retired).

**When to use:** When the brochure has 3 thematic chapters worth previewing up front.
**When to skip:** When the themes don't preview the rest of the brochure.
**Min/max:** As many cards as there are themes (2–4); a factual three is fine. Body ≤ 3 lines each.

```html
<div class="pillars">
  <div class="pillar p1"><span class="p-bar"></span>
    <p class="p-tag">01 — Tag</p>
    <h3 class="p-title">Pillar headline.</h3>
    <p class="p-body">Pillar body.</p>
    <div class="p-foot">Footer label</div>
  </div>
  <!-- one card per theme; same --teal bar on every card -->
</div>
```

---

## Capability grids

Equal-weight cards listing capabilities, features, or service lines.

**2×2** — when there are exactly 4 parallel items.
**3-up** — when there are 3, *and* a triplet structural pattern isn't already being used elsewhere in the document.
**4-up** — for 4 items where a 2×2 looks too chunky (works at narrower card heights).
**3-up illustrated** — variant where each card carries a line-art SVG diagram above the copy. Use when the cards represent abstract principles or platform-shape ideas that benefit from a diagrammatic mark. Skip when the content is operational and prose-heavy — the graphic is tone, not information.

**When to skip:** Lists of 5+ — break into two grids or use a comparison table. Lists of 1–2 — just write prose.

```html
<div class="caps-grid"><!-- grid-template-columns: repeat(2, 1fr) for 2x2 -->
  <div class="cap">
    <p class="cap-tag"><span class="dot"></span>01 — Capability name</p>
    <h3 class="cap-title">Capability headline.</h3>
    <p class="cap-body">What it does and why it matters in plain language.</p>
    <div class="cap-tools">
      <span class="tp">Tool tag</span>
      <span class="tp">Tool tag</span>
    </div>
  </div>
</div>
```

### 3-up illustrated variant

Each card opens with an inline SVG diagram in a fixed-height container, separated from the copy by a hairline. The SVGs should be black-on-white line-art with occasional faint gray strokes for depth — geometric, abstract, never decorative. A small filled square accent inside the SVG is a recurring visual signature.

```html
<div class="caps-grid cg-3">
  <div class="cap-ill">
    <div class="cap-ill-graphic">
      <svg viewBox="0 0 577 320" fill="none"><!-- line-art SVG --></svg>
    </div>
    <p class="cap-tag">01 — Theme</p>
    <h3 class="cap-title">Card headline.</h3>
    <p class="cap-body">Body copy that takes the diagram's idea and applies it operationally.</p>
  </div>
  <!-- two more cards -->
</div>
```

```css
.cap-ill { background: var(--panel); border: 1px solid var(--line); border-radius: 6px; padding: 36px 32px 32px; display: flex; flex-direction: column; }
.cap-ill-graphic { width: 100%; height: 130px; display: flex; align-items: center; justify-content: center; margin-bottom: 28px; }
.cap-ill-graphic svg { max-width: 100%; max-height: 100%; width: auto; height: auto; }
.cap-ill .cap-tag { font-family: var(--mono); font-size: var(--eyebrow-size); font-weight: 500;
                    letter-spacing: var(--tracking); line-height: var(--lh-body);
                    text-transform: uppercase; color: var(--teal); margin: 0 0 16px; }
.cap-ill .cap-title { font-family: var(--header); font-weight: 400;
                      font-size: var(--h3-size); line-height: var(--lh-header);
                      letter-spacing: var(--tracking);
                      color: var(--ink); margin: 0 0 calc(var(--h3-size) * 0.4); }
.cap-ill .cap-body { font-family: var(--body); font-size: var(--body-size);
                     line-height: var(--lh-body); letter-spacing: var(--tracking);
                     color: var(--ink-2); margin: 0; }
```

**Source SVGs** ship with the skill under `assets/graphics/` (`Mission Graphic1.svg`, `Scale with Clarity.svg`, `Variant9.svg`). When a new brochure needs an illustrated grid, reuse from this set rather than generating new diagrams — visual consistency across pieces is the point. To embed, inline the SVG contents directly into the HTML (don't link as files) so the brochure stays a single self-contained deliverable.

---

## Comparison table

Side-by-side "with Metafore" vs status quo (or "with the platform" vs legacy approach).

**When to use:** When the value of the offering only lands by contrast — replatforming pitches, displacement stories, modernization narratives.
**When to skip:** When there's no obvious antagonist. Forced comparison tables ("status quo" as a strawman) read as weak.
**Min/max:** 4–8 rows. Fewer than 4 isn't worth a table; more than 8 invites skimming.

```html
<table class="vs-table">
  <thead>
    <tr><th></th><th class="vs-them">Conventional approach</th><th class="vs-us">With Metafore</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">Time to deploy</th><td>Months of integration work</td><td>Conversation to production</td></tr>
    <!-- ... -->
  </tbody>
</table>
```

CSS pattern:
```css
.vs-table { width: 100%; border-collapse: collapse; margin-top: 40px; }
.vs-table th, .vs-table td { padding: 18px 22px; text-align: left; border-bottom: 1px solid var(--line);
                              font-size: var(--body-size); line-height: var(--lh-body);
                              letter-spacing: var(--tracking); }
.vs-table thead th { font-family: var(--mono); font-size: var(--eyebrow-size); font-weight: 500;
                     letter-spacing: var(--tracking); line-height: var(--lh-body);
                     text-transform: uppercase; color: var(--ink-3); padding-bottom: 14px; }
.vs-table .vs-us { color: var(--logo-dark); }
```

---

## KPI band

Wide saturated-teal band with 3 or 4 large numerical cells, separated by thin vertical dividers.

**When to use:** When the content has quantified outcomes worth headlining — adoption numbers, time savings, coverage percentages, deal sizes.
**When to skip:** When the numbers don't exist or aren't clean enough to publish.
**Min/max:** 3 or 4 cells. 2 cells looks sparse; 5+ doesn't fit at 1440px.

```html
<div class="kpi-band">
  <div class="kpi-cell">
    <p class="kpi-lbl">Eyebrow</p>
    <div class="kpi-num">100<span class="unit">%</span></div>
    <p class="kpi-cap">Caption explaining what the number represents.</p>
  </div>
  <!-- 2–3 more cells -->
</div>
```

CSS:
```css
.kpi-band { margin-top: 40px; background: var(--teal-dark); border-radius: 6px; padding: 36px 44px;
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 32px; }
.kpi-cell { border-left: 1px solid rgba(255,255,255,0.18); padding-left: 26px; }
.kpi-cell:first-child { border-left: 0; padding-left: 0; }
.kpi-cell .kpi-num { font-family: var(--header); font-weight: 400;
                     font-size: clamp(var(--h1-floor), 6.5cqw, var(--h1-size));
                     line-height: var(--lh-header); letter-spacing: var(--tracking); color: #fff; }
.kpi-cell .kpi-cap { font-size: var(--body-size); line-height: var(--lh-body);
                     letter-spacing: var(--tracking); color: rgba(255,255,255,0.82);
                     margin: 14px 0 0; max-width: 240px; }
```

---

## Process timeline

Numbered horizontal sequence on `var(--teal-dark)`, with large outlined numerals, "Verb and Verb" step titles, and a hairline + tick mark above each step.

**When to use:** When the content describes how something happens over time — onboarding flows, deployment phases, the build-then-deploy-then-evolve arc.
**When to skip:** When the order doesn't matter. A process timeline implies sequence.
**Min/max:** 3 steps is the canonical shape. 4 works if the content really needs it; 5+ doesn't read at 1440px and should be split into two timelines or compressed.

**Title convention:** Pair two verbs ("Ingest and Model", "Generate and Verify", "Deploy and Evolve"). Single-verb titles look thin in this treatment.

```html
<div class="timeline">
  <div class="tl-step">
    <div class="tl-rule"></div>
    <div class="tl-num">01</div>
    <h4 class="tl-title">Ingest and Model</h4>
    <p class="tl-body">Step body, ~25–35 words. Keep it operational.</p>
  </div>
  <!-- 02, 03 -->
</div>
```

```css
.timeline { background: var(--teal-dark); border-radius: 6px; padding: 56px 56px 72px;
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 64px; }
.tl-step { display: flex; flex-direction: column; }
.tl-rule { position: relative; height: 1px; background: rgba(255,255,255,0.22); margin-bottom: 52px; }
.tl-rule::before { content: ""; position: absolute; left: 0; top: 0; width: 8px; height: 8px; background: rgba(255,255,255,0.55); }
/* The 8px tick square is top-aligned with the hairline — its top edge sits on the line, body extends downward. Not centered. */
.tl-num { font-family: var(--mono); font-weight: 300;
          font-size: clamp(var(--h1-floor), 6.5cqw, var(--h1-size));
          line-height: var(--lh-header); letter-spacing: var(--tracking);
          color: #fff; margin: 0 0 36px; font-variant-numeric: tabular-nums; }
/* Numerals are IBM Plex Mono Light (300) at the H1 scale — never the header font, never bold. */
.tl-title { font-family: var(--header); font-weight: 400;
            font-size: clamp(var(--h2-floor), 4.2cqw, var(--h2-size));
            line-height: var(--lh-header); letter-spacing: var(--tracking);
            color: #fff; margin: 0 0 calc(var(--h2-size) * 0.3); }
.tl-body { font-family: var(--body); font-size: var(--body-size);
           line-height: var(--lh-body); letter-spacing: var(--tracking);
           color: rgba(255,255,255,0.72); margin: 0; }
```

---

## Quote pull

A customer or executive quote, with attribution. Treats voice as content, not as ornament.

**When to use:** When there is real, attributable customer voice. Approved testimonials. Public executive statements.
**When to skip:** Anything you'd have to invent or paraphrase. Fictional quotes attributed to fictional customers are an instant credibility failure.
**Min/max:** One quote per pull. Max ~40 words.

```html
<figure class="quote">
  <blockquote>The full quote text in the body font, set large and left-aligned.</blockquote>
  <figcaption>
    <span class="q-name">Person Name</span>
    <span class="q-role">Title, Company</span>
  </figcaption>
</figure>
```

---

## Callout strip

Eyebrow on the left, 2–3 supporting cells on the right. Used in the Maker brochure for the Shadow Panel section — a single concept on the left, a few aspects on the right.

**When to use:** When one feature or theme has 2–3 distinct facets worth surfacing but doesn't deserve a full pillar/capability grid.
**Min/max:** 2 or 3 cells on the right.

```html
<div class="shadow-strip">
  <div class="ss-left">
    <p class="ss-eyebrow">Eyebrow</p>
    <h3 class="ss-title">Single concept headline.</h3>
  </div>
  <div class="ss-right">
    <div class="ss-cell"><p class="sc-lbl">Aspect</p><p class="sc-body">Explanation.</p></div>
    <!-- 2 more cells -->
  </div>
</div>
```

---

## Outcome band

Full-width band on `var(--teal)`, white text, used as a single big commitment statement near the end of the brochure.

**When to use:** Once per brochure, near the end, as the closing thesis. Never twice.
**When to skip:** When the brochure doesn't have one big consolidating idea to state. A weak outcome band drags the whole piece down.

```html
<div class="outcome">
  <p class="out-eyebrow">Eyebrow</p>
  <h3>The single big commitment, stated plainly.</h3>
  <p>One supporting paragraph. Not three. Not five.</p>
  <div class="out-foot"><!-- optional 3-cell label/value strip --></div>
</div>
```

---

## FAQ block

A few Q&A pairs near the end of the brochure for sales-objection handling.

**When to use:** When the brochure is sales-facing and the audience predictably asks 3–6 questions before signing. Skip for upper-funnel awareness pieces.
**Min/max:** 3–6 Q&A pairs.

(Snippet TBD when first real use case appears.)

---

## Footer

The closing invariant. Always present. Always last.

```html
<footer class="footer">
  <span class="foot-brand">Powered by Metafore — AI-Native Transformation Platform</span>
  <span class="foot-meta">© 2026 Metafore · [Document name] · Confidential</span>
</footer>
```

```css
.footer { border-top: 1px solid var(--line); padding: 28px 96px; display: flex; justify-content: space-between; align-items: center; background: var(--panel); }
.footer .foot-brand { font-family: var(--mono); font-size: var(--eyebrow-size); font-weight: 500;
                      letter-spacing: var(--tracking); line-height: var(--lh-body);
                      text-transform: uppercase; color: var(--ink-3); }
.footer .foot-meta { font-family: var(--mono); font-size: var(--eyebrow-size); font-weight: 400;
                     letter-spacing: var(--tracking); line-height: var(--lh-body); color: var(--ink-4); }
```

---

## Open questions for the next promotion pass

When this library moves out of draft, work through:
- Should the comparison table get a "with Metafore" header treatment (teal column highlight) or stay neutral?
- Is the process timeline horizontal-only, or do we want a vertical variant for narrower content?
- Quote pulls — single quote vs. multi-quote band? Existing brochures don't yet have a precedent.
- FAQ blocks — accordion (JS) vs. always-open (HTML-only). Skill output is currently HTML-only, so accordion would break the no-JS constraint.
- Hero variant D — text + inline chart? Some product stories want a visualization in place of a UI card.
