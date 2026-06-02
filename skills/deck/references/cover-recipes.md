# Cover Slide Recipes — 1A / 1B / 1C

The first slide of every Metafore deck is one of three Type 1 covers, adapted from `metafore-graphic` to the 1920×1080 slide canvas. All three are **hybrid tier** by default — the visual chrome (panels, dot grids, glass cards, logo) renders to PNG; the eyebrow, headline, accent span, and lede sit as native PPT text frames at their HTML bounding-box coordinates.

## Cover-specific rules

- **Logo position**: cover uses the **top-left** placement (every other slide uses top-right). This is the book-end signature.
- **Logo size**: cover uses the full 155×36 wordmark. Content slides use the smaller 110×26.
- **Footer line**: the cover carries the standard footer (`© <YEAR> METAFORE · ALL RIGHTS RESERVED · CONFIDENTIAL` bottom-left) with the page number `01 / NN` bottom-right.
- **No top-right slide-number marker.** The page number lives in the bottom-right of the footer, never top-right.

## Sizing — graphic → slide canvas

The Type 1 graphics are authored at 1422×800 in `metafore-graphic`. Adapted to 1920×1080:

- Native horizontal scale = 1920 / 1422 ≈ 1.35
- Native vertical scale = 1080 / 800 = 1.35
- Aspect ratio is identical (both 16:9) — proportional scale-up only, no recropping
- Multiply every pixel value in the original recipes by 1.35 (or use the values listed below, already scaled)

## Picking the variant

| Cover | Use when | Logo |
|---|---|---|
| **1A** — split white / teal-light + data card | The opening argument is a hard metric or before/after comparison and you have evidence to show in the cover | Light variant, top-left of white panel |
| **1B** — full teal + floating glass UI card | The opening argument is positioning, vision, or brand presence; no specific metric to anchor on | Dark variant, top-left of solid teal |
| **1C** — split white / solid teal + accent-term hero | The deck is naming or defining a thing ("What is Mira", "Introducing Pulse") | Light variant, top-left of white panel |

If unclear, default to 1B for board / pitch decks, 1A for customer-outcome decks, 1C for product-introduction decks.

---

## 1A — Split white / teal-light + data card

Two-column CSS grid, `1fr 1fr`. Slide is 1920 wide, so each column is 960px.

### Left panel (white, editable text)

```html
<section class="slide" data-pptx="hybrid" data-slide-id="cover">
  <div class="cover-1a">

    <!-- LEFT PANEL — white -->
    <div class="left">
      <!-- Logo — light variant, top-left, 56px from edges -->
      <div class="logo" data-pptx-image="logo-light">
        <!-- inline contents of assets/logo-light.svg -->
      </div>

      <!-- Text overlays — editable in PPTX -->
      <div class="textwell">
        <div class="eyebrow" data-pptx-text="eyebrow">
          Customer outcome · Telecom · 2026
        </div>
        <h1 data-pptx-text="headline">
          47% less time
          <span class="accent" data-pptx-accent>per ticket</span>
        </h1>
        <p class="lede" data-pptx-text="lede">
          How a North-American carrier orchestrated outage triage with Metafore
          cognitive agents — and what changed for their care team in 90 days.
        </p>
      </div>
    </div>

    <!-- RIGHT PANEL — teal-light + dot grid + data card -->
    <div class="right">
      <div class="dotgrid"></div>
      <div class="datacard">
        <!-- Pick ONE card variant from metafore-graphic's blog-hero-recipes.md:
             - Before/after timeline
             - KPI grid + horizontal bar chart
             - Phase bars
             - Sparkline / area chart + KPI strip
             - Process flow stepper
             Scale dimensions ×1.35 from the original recipe. -->
      </div>
    </div>

  </div>
</section>
```

### CSS

```css
.cover-1a {
  display: grid;
  grid-template-columns: 1fr 1fr;
  width: var(--slide-w);
  height: var(--slide-h);
}

.cover-1a .left {
  position: relative;
  background: var(--bg);
  padding: var(--slide-pad-y) var(--slide-pad-x);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.cover-1a .left .logo {
  position: absolute;
  top: var(--logo-offset);
  left: var(--logo-offset);
}
.cover-1a .left .textwell {
  max-width: 720px;
}
.cover-1a .left .eyebrow {
  margin-bottom: 28px;
}
.cover-1a .left h1 {
  font-family: var(--header);
  font-weight: 400;
  font-size: 96px;
  line-height: 1.04;
  letter-spacing: -2.4px;
  margin: 0 0 36px;
  color: var(--ink);
}
.cover-1a .left .lede {
  font-family: var(--body);
  font-size: 24px;
  line-height: 1.55;
  color: var(--ink-2);
  max-width: 620px;
  margin: 0;
}

.cover-1a .right {
  position: relative;
  background: var(--teal-light);
  overflow: hidden;
}
.cover-1a .right .dotgrid {
  position: absolute; inset: 0;
  background-image: radial-gradient(circle, rgba(0,107,111,0.32) 1px, transparent 1.5px);
  background-size: 8px 8px;
}
.cover-1a .right .datacard {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 760px;
  background: var(--bg);
  border-radius: 14px;
  padding: 40px;
  /* No drop shadow — use a 1px border instead */
  border: 1px solid var(--line);
}
```

### Editable nodes for PPTX

| `data-pptx-text` | What it is | Approx HTML rect (1920×1080 canvas) |
|---|---|---|
| `eyebrow` | Customer / context label | top ≈ 380, left ≈ 120, w ≈ 720 |
| `headline` | Two-line headline with accent span on last 1–3 words | top ≈ 432, left ≈ 120, w ≈ 720 |
| `lede` | Lede paragraph | top ≈ 632, left ≈ 120, w ≈ 620 |

(Exact rects are read live by the generator from `getBoundingClientRect()` — these are sanity-check approximations.)

---

## 1B — Full teal + floating glass card

Single panel, solid `--teal-dark`. **No dot pattern, no halftone, no overlay** — the surface is solid.

### HTML

```html
<section class="slide" data-pptx="hybrid" data-slide-id="cover">
  <div class="cover-1b">

    <!-- Logo — dark-bg variant, top-left -->
    <div class="logo" data-pptx-image="logo-dark">
      <!-- inline contents of assets/logo-dark.svg -->
    </div>

    <!-- Text overlays — editable in PPTX -->
    <div class="textwell">
      <div class="eyebrow" data-pptx-text="eyebrow">
        Vision · Metafore One · 2026
      </div>
      <h1 data-pptx-text="headline">
        The cognitive system
        <span class="accent-light" data-pptx-accent="light">for the enterprise</span>
      </h1>
      <div class="subtitle-box" data-pptx-text="subtitle">
        AMPLIFY HUMAN INTELLIGENCE
      </div>
    </div>

    <!-- Floating glass UI card — image-rendered, NOT editable -->
    <div class="glasscard">
      <div class="glass-header">
        <!-- inline dark-bg logo at width="98" height="22" -->
        <span class="glass-eyebrow">METAFORE · PULSE FOR NETWORK OPS</span>
      </div>
      <div class="glass-body">
        <!-- Realistic mini-UI: Sense / Reason / Act stepper, KPI strip,
             or dashboard fragment. Stays inside the rendered PNG. -->
      </div>
    </div>

  </div>
</section>
```

### CSS

```css
.cover-1b {
  position: relative;
  width: var(--slide-w);
  height: var(--slide-h);
  background: var(--teal-dark);     /* solid — NO dot pattern */
  color: #fff;
  overflow: hidden;
}
.cover-1b .logo {
  position: absolute;
  top: var(--logo-offset);
  left: var(--logo-offset);
}
.cover-1b .textwell {
  position: absolute;
  top: 50%;
  left: var(--slide-pad-x);
  transform: translateY(-50%);
  max-width: 880px;
}
.cover-1b .textwell .eyebrow {
  color: rgba(255,255,255,0.7);
  margin-bottom: 32px;
}
.cover-1b .textwell h1 {
  font-family: var(--header);
  font-weight: 400;
  font-size: 104px;
  line-height: 1.04;
  letter-spacing: -2.6px;
  margin: 0 0 40px;
  color: #fff;
}
/* Accent on dark backgrounds uses --teal-on-dark (#88DCE0); --logo-dark
   would be invisible on --teal-dark. */
.cover-1b .textwell h1 .accent-light {
  color: var(--teal-on-dark);
}
/* Subtitle box — small bracket-bordered badge.
   This corner-bracket TREATMENT is allowed only on 1B's subtitle badge.
   It is NOT used around headline accent terms (retired). */
.cover-1b .subtitle-box {
  font-family: var(--mono);
  font-size: 14px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.9);
  padding: 16px 24px;
  display: inline-block;
  position: relative;
}
.cover-1b .subtitle-box::before,
.cover-1b .subtitle-box::after {
  content: ""; position: absolute;
  width: 14px; height: 14px;
  border: 1.5px solid var(--teal-on-dark);
}
.cover-1b .subtitle-box::before {
  top: 0; left: 0; border-right: none; border-bottom: none;
}
.cover-1b .subtitle-box::after {
  bottom: 0; right: 0; border-left: none; border-top: none;
}

.cover-1b .glasscard {
  position: absolute;
  top: 50%;
  right: var(--slide-pad-x);
  transform: translateY(-50%);
  width: 640px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 16px;
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  padding: 36px;
}
```

### Editable nodes for PPTX

| `data-pptx-text` | What it is | Notes |
|---|---|---|
| `eyebrow` | Vision / context label, white@70% | Plex Mono, no tracking in PPTX |
| `headline` | Two-line hero with `accent-light` span (teal-on-dark) | Run-split: white + `#88DCE0` |
| `subtitle` | Optional badge text | Plex Mono, no tracking |

**Glass card content is NOT editable.** If the data inside the card has to change, regenerate the slide from updated HTML.

---

## 1C — Split white / solid teal with accent-term hero

Two-column split, white left / **solid `--teal-dark`** right. Headline highlights a key definitional term.

### HTML

```html
<section class="slide" data-pptx="hybrid" data-slide-id="cover">
  <div class="cover-1c">

    <!-- LEFT PANEL — white -->
    <div class="left">
      <div class="logo" data-pptx-image="logo-light">
        <!-- inline contents of assets/logo-light.svg -->
      </div>

      <div class="textwell">
        <div class="eyebrow" data-pptx-text="eyebrow">
          Definition · Metafore for Telecom
        </div>

        <!-- Block-flow headline — each line is display:block.
             Do NOT use flex-column-with-gap; line-height carries spacing. -->
        <h1 data-pptx-text="headline">
          <span class="line">What is</span>
          <span class="line"><span class="bracket" data-pptx-accent>Mira</span></span>
          <span class="line">the personal twin</span>
        </h1>

        <p class="subtitle" data-pptx-text="subtitle">
          A cognitive agent for every subscriber, deployed in carrier IMS.
        </p>
        <p class="lede" data-pptx-text="lede">
          Mira senses subscriber signals across the network, reasons about
          intent with the carrier knowledge fabric, and acts on the
          subscriber's behalf — across billing, support, and service.
        </p>
      </div>
    </div>

    <!-- RIGHT PANEL — solid teal-dark, NO dot pattern -->
    <div class="right">
      <div class="glasscard">
        <div class="glass-header">
          <!-- inline dark-bg logo at width="98" height="22" -->
          <span class="glass-eyebrow">PULSE · CARE OPS</span>
        </div>
        <div class="glass-body">
          <!-- Workflow or Pulse fragment, stays in rendered PNG -->
        </div>
      </div>
    </div>

  </div>
</section>
```

### CSS

```css
.cover-1c {
  display: grid;
  grid-template-columns: 1fr 1fr;
  width: var(--slide-w);
  height: var(--slide-h);
}
.cover-1c .left {
  position: relative;
  background: var(--bg);
  padding: var(--slide-pad-y) var(--slide-pad-x);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.cover-1c .left .logo {
  position: absolute;
  top: var(--logo-offset);
  left: var(--logo-offset);
}
.cover-1c .left .textwell {
  max-width: 720px;
}
.cover-1c .left .eyebrow {
  margin-bottom: 28px;
}
.cover-1c .left h1 {
  font-family: var(--header);
  font-weight: 400;
  font-size: 96px;
  line-height: 1.12;        /* shared line-height carries row spacing */
  letter-spacing: -2.2px;
  margin: 0 0 32px;
  color: var(--ink);
  /* IMPORTANT: do NOT use display:flex; flex-direction:column; gap.
     Descenders (g, p, y) would break row alignment. */
}
.cover-1c .left h1 .line { display: block; }
.cover-1c .left h1 .bracket {
  /* Color wrapper only. NO corner brackets, NO mono font,
     NO tinted background. Same Geist size as the rest of the headline. */
  color: var(--logo-dark);
}
.cover-1c .left .subtitle {
  font-family: var(--body);
  font-size: 26px;
  line-height: 1.4;
  color: var(--ink-3);
  margin: 0 0 24px;
  max-width: 680px;
}
.cover-1c .left .lede {
  font-family: var(--body);
  font-size: 20px;
  line-height: 1.55;
  color: var(--ink-2);
  margin: 0;
  max-width: 640px;
}

.cover-1c .right {
  position: relative;
  background: var(--teal-dark);     /* solid — NO dot pattern */
  overflow: hidden;
}
.cover-1c .right .glasscard {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 640px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 16px;
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  padding: 36px;
}
```

### Editable nodes for PPTX

| `data-pptx-text` | What it is | Notes |
|---|---|---|
| `eyebrow` | Definition / context label | Plex Mono, no tracking in PPTX |
| `headline` | Block-flow headline with accent term wrapped in `.bracket` span | Run-split: ink + logo-dark, single text frame, block flow preserved as line breaks |
| `subtitle` | Secondary line | Inter 26px |
| `lede` | Body paragraph | Inter 20px |

---

## Cross-cover invariants

These apply to **every** cover regardless of variant.

- **Logo placement is consistent.** Top-left, `var(--logo-offset)` from both edges (~56px). Variant matches the panel (light on white / `--bg-solid`, dark on `--teal-dark`).
- **Two-tone hero is the brand signature.** Cover 1A and 1C use `--logo-dark` (`#035657`) on a light panel. Cover 1B uses `--teal-on-dark` (`#88DCE0`) because `--logo-dark` would disappear on `--teal-dark`. `#88DCE0` is the canonical light-on-dark accent (replacing the retired `#00C4CC`/`#00989E`).
- **No bracket-box around headline accent terms.** The `.bracket` class on 1C is a color wrapper *only*. No corner brackets, no monospace font, no tinted background. The corner-bracket box on 1B's `subtitle-box` is a separate, allowed pattern — applied to a small badge, never to a headline.
- **No dot pattern on full-screen dark surfaces.** 1B's whole surface and 1C's right panel are solid `--teal-dark`. The dot grid only appears on 1A's teal-*light* right panel.
- **No drop shadows.** Data cards (1A) and glass cards (1B/1C) get 1px borders instead.
