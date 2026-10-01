# P-06 · Capability grid (4-up)

**When:** exactly 4 parallel items with illustrations (four graphs, four pillars, four stages). `.cols-3` holds 3. **Tier:** `hybrid`.

```html
<section class="slide p-grid4" data-pptx="hybrid" data-pattern="P-06">
  <div class="section-label">Platform</div>
  <!-- @logo:icon-light width="72" height="60" class="icon-tr" -->
  <div class="head"><h2>Four graphs, one operating <span class="accent">platform</span></h2></div>
  <div class="tiles">
    <div class="tile"><img class="lineicon" src="@icon:Stack" alt="">
      <div class="t-num">Meta · Ontology</div><h3>What things are</h3>
      <p class="small">How entities relate across the enterprise.</p></div>
    <!-- 4 tiles. Four-graph canonical order: Meta → Knowledge → Context → Control
         (icons Stack, Nodes, ThroughLine, Axis) -->
  </div>
  <!-- @footer -->
</section>
```

- Every tile eyebrow (`.t-num`) is the same `--teal` — never step through the teal stack.
- Tile body ≤ 3 lines (~14 words). Distinct library icon per tile; don't reuse one icon twice on a slide.
- A Pulse-tile variant puts a locked `.mini` card in place of the icon (`<div class="t-illust mini" data-pptx-lock data-decorative>`).
- More than 4 items → P-07 or P-08. Never emoji or photos in the illustration block.
