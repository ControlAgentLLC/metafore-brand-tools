# P-04 · Company / About (and P-04B · Track record)

**When:** one "about us" slide, usually slide 3. **Tier:** `semantic`.

```html
<section class="slide p-company" data-pptx="semantic" data-pattern="P-04">
  <div class="section-label">The company</div>
  <!-- @logo:icon-light width="72" height="60" class="icon-tr" -->
  <div>
    <h2>The AI transformation <span class="accent">partner</span></h2>
    <p class="body">Metafore builds cognitive systems that sense, reason, and act across the enterprise.</p>
    <p class="signature">Amplify human intelligence</p>
  </div>
  <div class="facts">
    <div class="fact"><img class="lineicon" src="@icon:Orbit" alt="">
      <div><div class="f-label">Headquarters</div><div class="f-value">San Francisco</div><div class="f-sub">Team across NA, EMEA, APAC</div></div></div>
    <!-- 3–5 facts: HQ, leadership, flagship platform, industries (swap one for funding stage / customer count) -->
  </div>
  <!-- @footer -->
</section>
```

Mission body ≤ 3 lines (~25 words in the half-width column). Facts are label/value rows, not bullets.

## P-04B · Track record
Copy left, 2×2 credibility cards right. Usually slide 2 of outbound sales decks.

```html
<section class="slide p-track" data-pptx="semantic" data-pattern="P-04">
  <div class="section-label">Team</div>
  <!-- @logo:icon-light width="72" height="60" class="icon-tr" -->
  <div><h2>A proven <span class="accent">track record</span></h2>
    <p class="body">C-level experience at Amazon, Genesys, Microsoft, VMware, and Vodafone.</p></div>
  <div class="grid">
    <div class="card alt"><img class="lineicon" src="@icon:Connected" alt=""><h3>Invented enterprise application integration</h3>
      <p class="small">Frameworks that let complex systems work together.</p></div>
    <!-- 4 cards -->
  </div>
  <!-- @footer -->
</section>
```
