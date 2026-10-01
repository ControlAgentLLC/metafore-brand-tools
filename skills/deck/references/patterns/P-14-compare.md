# P-14 · Two-column comparison

**When:** one binary comparison where both states are real (before/after, without/with). Use sparingly. **Tier:** `semantic`.

```html
<section class="slide p-compare" data-pptx="semantic" data-pattern="P-14">
  <div class="section-label">Before and after</div>
  <!-- @logo:icon-light width="72" height="60" class="icon-tr" -->
  <div class="head"><h2>From signal triage to orchestrated <span class="accent">resolution</span></h2></div>
  <div class="cols">
    <div class="col"><div class="label">Today</div><img class="lineicon" src="@icon:Squares" alt="">
      <div class="stat"><div class="n">4 hrs</div><div class="label l">Median handling time</div></div>
      <p class="body">Alerts, signals, and exceptions land in separate queues.</p></div>
    <div class="col"><div class="label">With Metafore</div><img class="lineicon" src="@icon:Integration" alt="">
      <!-- … --></div>
  </div>
  <!-- @footer -->
</section>
```

- Header type matches P-05; numbers match P-09 but in `--logo-dark`. Body ≤ 3 lines per column.
