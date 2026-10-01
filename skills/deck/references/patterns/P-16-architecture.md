# P-16 · Architecture diagram

**When:** platform/system layers. Deck-specific; this is a layered-column scaffold. **Tier:** `hybrid` (or `image` when the diagram is the whole slide).

```html
<section class="slide p-arch" data-pptx="hybrid" data-pattern="P-16">   <!-- add "dark" for the teal surface -->
  <div class="section-label">Architecture</div>
  <!-- @logo:icon-light width="72" height="60" class="icon-tr" -->
  <div class="head"><h2>How the platform is <span class="accent">built</span></h2></div>
  <div class="layers" data-visual style="--cols: 5">
    <div class="layer"><h3>Experience</h3><p class="small">Generative and branded interfaces</p>
      <div class="chip">Generative UI</div><div class="chip">Pulse</div><div class="chip">Voice gateway</div></div>
    <!-- 4–6 layers, 3–5 chips each -->
  </div>
  <!-- @footer -->
</section>
```

- Teal stack only; Plex Mono / Inter labels at ≥ 22px. Replace the scaffold with a designed diagram when the deck needs one.
