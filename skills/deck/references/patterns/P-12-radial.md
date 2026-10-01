# P-12 · Radial diagram / knowledge graph

**When:** topology, connectivity, "one connected reality". Pairs with a Why-style left column, often on dark. **Tier:** `hybrid`.

```html
<section class="slide p-radial dark" data-pptx="hybrid" data-pattern="P-12">
  <div class="section-label on-dark">Why Metafore</div>
  <!-- @logo:icon-dark width="72" height="60" class="icon-tr" -->
  <div><h2>One connected <span class="accent">reality</span></h2>
    <p class="body">Every system of record feeds one governed knowledge graph.</p>
    <div class="stats"><div class="stat"><div class="n">12</div><div class="label l">Source systems</div></div></div></div>
  <div class="diagram">
    <svg viewBox="0 0 800 800" fill="none" aria-label="Knowledge graph">
      <g stroke="#88DCE0" stroke-width="2">
        <line x1="400" y1="400" x2="400" y2="120"/><!-- spokes to each satellite; peripheral links stroke-dasharray="6 8" -->
      </g>
      <circle cx="400" cy="400" r="70" stroke="#88DCE0" stroke-width="2"/><circle cx="400" cy="400" r="12" fill="#88DCE0"/>
      <circle cx="400" cy="120" r="34" stroke="#88DCE0" stroke-width="2"/><circle cx="400" cy="120" r="6" fill="#88DCE0"/>
      <text x="400" y="62" text-anchor="middle" fill="rgba(255,255,255,0.88)">Billing</text>
      <!-- 6–8 satellites at compass positions -->
    </svg>
  </div>
  <!-- @footer on-dark -->
</section>
```

- Diagram labels are 22px (they carry meaning). On dark, strokes and dots use `#88DCE0`; on light, `#006B6F`. Never `#00989E` / `#00C4CC` — check.py greps inline SVG for them.
- Outlined satellites with a small filled inner dot, not solid bright fills.
