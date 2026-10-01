# P-22 · Industries (grouped or per-vertical)

## Mode A — grouped (one slide)
**When:** the deck is short and verticals aren't the focus. **Tier:** `semantic`. Holds any N — set `--cols` (3×2 for six, 4×2 for eight); never drop a vertical to fit.

```html
<section class="slide p-industries" data-pptx="semantic" data-pattern="P-22">
  <div class="section-label">Industries</div>
  <!-- @logo:icon-light width="72" height="60" class="icon-tr" -->
  <div class="head"><h2>Six industries, one <span class="accent">platform</span></h2></div>
  <div class="grid" style="--cols: 3">
    <div class="card alt"><img class="lineicon" src="@icon:Connected" alt=""><h3>Telecom</h3><p class="small">Network operations, subscriber care, Mira.</p></div>
    <!-- one card per industry -->
  </div>
  <!-- @footer -->
</section>
```

## Mode B — per vertical (one slide each)
**Tier:** `hybrid`.

```html
<section class="slide p-vertical" data-pptx="hybrid" data-pattern="P-22">
  <div class="section-label">Industries</div>
  <!-- @logo:icon-light width="72" height="60" class="icon-tr" -->
  <div>
    <h1>Banking</h1>
    <p class="lede">Self-evolving agents across service, compliance, and operations.</p>
    <div class="rows card alt">
      <div class="row"><strong>Built-in governance</strong><p class="small">Every action explainable and auditable.</p></div>
      <!-- 3–4 rows, one line each -->
    </div>
  </div>
  <div class="media"><img class="lineicon lg" src="@icon:Axis" alt=""><!-- or a locked .ui-card mini --></div>
  <!-- @footer -->
</section>
```

Mira appears on the telecom card only.
