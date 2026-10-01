# P-01 · Cover (1A / 1B / 1C)

**When:** slide 1, always. **Tier:** `hybrid` (headline + subtitle editable; panels, dot grid and cards baked).

**Cover text is minimal — title and subtitle only.** No eyebrow, no lede. The hero is the brand or product name ("Introducing MetaWorks"); the subtitle carries the descriptive sentence. Headline ≤ 6 words, two lines at most, at `--cover-size` (112px) — shorten, never shrink.

| Variant | Use when | Logo |
|---|---|---|
| **1A** split white / teal-light + data card | The opening argument is a hard metric or before/after | `logo-light` top-left |
| **1B** full teal + floating glass card | Positioning, vision, launch — no metric to anchor | `logo-dark` top-left |
| **1C** split white / solid teal + accent-term hero | Naming or defining a thing ("What is Mira") | `logo-light` top-left |

Default: 1B board/pitch, 1A customer-outcome, 1C product introduction. Glassmorphism appears **only** on the cover.

```html
<!-- 1A -->
<section class="slide p-cover-1a" data-pptx="hybrid" data-pattern="P-01">
  <!-- @logo:logo-light width="155" height="36" class="logo-tl" -->
  <div class="left">
    <h1><span class="line">47% less time</span><span class="line"><span class="accent">per ticket</span></span></h1>
    <p class="subtitle">How a North-American carrier orchestrated outage triage in 90 days</p>
  </div>
  <div class="right">
    <div class="ui-card datacard mini" data-pptx-lock data-decorative>
      <!-- one mini form: .mini-kpis / .mini-bar rows / .mini-row list / .mini-trace -->
    </div>
  </div>
  <!-- @footer -->
</section>

<!-- 1B -->
<section class="slide p-cover-1b" data-pptx="hybrid" data-pattern="P-01">
  <!-- @logo:logo-dark width="155" height="36" class="logo-tl" -->
  <div>
    <h1><span class="line">Introducing</span><span class="line"><span class="accent">MetaWorks</span></span></h1>
    <p class="subtitle">The enterprise operating system that thinks, acts, and builds</p>
  </div>
  <div class="glasscard mini" data-pptx-lock data-decorative>
    <div class="mini-head"><span class="mini-eyebrow">Pulse · Network ops</span><span class="mini-meta">09:42</span></div>
    <!-- mini rows / kpis / trace -->
  </div>
  <!-- @footer on-dark -->
</section>

<!-- 1C -->
<section class="slide p-cover-1c" data-pptx="hybrid" data-pattern="P-01">
  <!-- @logo:logo-light width="155" height="36" class="logo-tl" -->
  <div class="left">
    <h1><span class="line">What is</span><span class="line"><span class="bracket">Mira</span></span></h1>
    <p class="subtitle">A cognitive agent for every subscriber, deployed in carrier IMS</p>
  </div>
  <div class="right"><div class="glasscard mini" data-pptx-lock data-decorative><!-- … --></div></div>
  <!-- @footer -->
</section>
```

**Notes**
- Multi-line headlines use block `.line` spans with one shared line-height — never `flex-direction: column; gap`.
- The 1A dot grid lives only on the teal-*light* panel. 1B and the 1C right panel are solid `--teal-dark`, no pattern.
- 1B may add one `.badge-box` line (mono, 24px) under the subtitle — never brackets around the headline term.
- Card content follows the mini forms in `patterns.css` (`.mini-row`, `.mini-bar`, `.mini-kpis`, `.mini-trace`, `.mini-cta`); keep it to ≤ 3 rows.
