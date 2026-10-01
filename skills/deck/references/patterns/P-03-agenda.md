# P-03 · Agenda

**When:** slide 2 of decks longer than ~8 slides; skip in short decks. **Tier:** `semantic`.

```html
<section class="slide p-agenda" data-pptx="semantic" data-pattern="P-03">
  <div class="section-label">Agenda</div>
  <!-- @logo:icon-light width="72" height="60" class="icon-tr" -->
  <div class="head"><h2>What we'll <span class="accent">cover</span></h2></div>
  <div class="items" data-visual style="--rows: 4">
    <div class="item"><span class="a-num">01</span><div class="a-title">The Company<span class="a-sub">Who Metafore is and how we got here.</span></div></div>
    <!-- 4–10 items; --rows = ceil(items / 2) -->
  </div>
  <!-- @footer -->
</section>
```

- Column-major order (01 top-left, then down the left column). `--rows` controls the split.
- Items are Title Case noun phrases ("The Problem", "Platform & Integrations"); use "The" only where it reads naturally. The sub-line is one sentence with a period.
- 11+ items reads as a book TOC — group consecutive slides into named sections. Update the agenda whenever slides move.
