# P-05 · Statement / Problem / Why

**When:** a slide whose job is to land one message — the problem, the insight, the claim. **Tier:** `hybrid`.

```html
<section class="slide p-statement" data-pptx="hybrid" data-pattern="P-05">   <!-- add "dark" for the --teal-dark version (84px h2) -->
  <div class="section-label">The problem</div>
  <!-- @logo:icon-light width="72" height="60" class="icon-tr" -->
  <div>
    <h2>Each function sees its own view, never the <span class="accent">whole</span></h2>
    <p class="body">One paragraph, three lines at most.</p>
    <!-- optional: <div class="stats"><div class="stat"><div class="n">47%</div><div class="label l">Less time per ticket</div></div>…</div> -->
  </div>
  <div class="art"><img class="lineicon lg" src="@icon:Venn" alt=""></div>
  <!-- @footer -->
</section>
```

**The right-hand art carries the argument:**
- **Problem — "dead-end views":** a 2×2 `.dead-grid` of disconnected function cards (`.dead` with `.mini-eyebrow`, `.n`, `.foot "—"`), no connectors. Muted greys are intentional here — the point is that these surfaces are dead. Wrap in `data-pptx-lock data-decorative`.
- **Insight:** one radial / knowledge-graph composition (see P-12 SVG).
- **Convergence:** many surfaces collapsing to one mark, or a library icon (`Venn`, `ThroughLine`, `Integration`).

- Never put a polished Pulse card on the Problem slide — the Pulse is the solution; save it for P-17/P-18.
- No chart fragments as decoration (donuts, gauges, multi-color bars), no rotated or scattered cards.
