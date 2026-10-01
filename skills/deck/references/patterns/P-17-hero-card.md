# P-17 · Content hero with right product card

**When:** "here's what it looks like" — one product surface (Pulse view, workflow, agent moment) on the right, explanation left. **Tier:** `hybrid`.

```html
<section class="slide p-hero-card" data-pptx="hybrid" data-pattern="P-17">
  <div class="section-label">Pulse in action</div>
  <!-- @logo:icon-dark width="72" height="60" class="icon-tr" -->   <!-- icon sits over the dark stage -->
  <div class="left">
    <div class="eyebrow">Pulse for network ops</div>
    <h2>The incident, the reasoning, and the <span class="accent">next action</span></h2>
    <p class="body">Engineers see live state and the trace behind every recommendation.</p>
    <div class="meta"><div><div class="label">MTTR</div><div class="v">−38%</div></div></div>
  </div>
  <div class="stage">
    <div class="ui-card mini" data-pptx-lock data-decorative>
      <div class="mini-head"><span class="mini-eyebrow">Incident · P1</span><span class="mini-meta">09:42</span></div>
      <div class="mini-title">Fibre cut, Metro East</div>
      <div class="mini-row"><span class="k">Subscribers affected</span><span class="v">18,204</span></div>
      <div class="mini-cta">Dispatch crew</div>
    </div>
  </div>
  <!-- @footer -->
</section>
```

- Solid white card on the dark stage — glass is cover-only. The stage is solid, never patterned.
- The whole card is locked (visual proof). If the customer must edit its numbers, move them into the left column.
