# P-02 · Section divider

**When:** a phase change in the narrative. One or two per deck. **Tier:** `semantic`.

```html
<section class="slide p-divider" data-pptx="semantic" data-pattern="P-02">
  <!-- @logo:icon-dark width="72" height="60" class="icon-tr" -->
  <div class="eyebrow">Section 02</div>
  <h1>Where the work <span class="accent">breaks</span></h1>   <!-- add class="sentence" for a full sentence (88px) -->
  <p class="subtitle">One optional line, never a paragraph</p>
  <div class="progress" data-visual><span>01 The problem</span><span class="on">02 The platform</span><span>03 Proof</span></div>
  <!-- @footer on-dark -->
</section>
```

- The `.progress` rail (deck sections, current one highlighted) is the slide's visual — keep it in sync with the agenda.
- More than one line of subtitle means it is a statement slide (P-05), not a divider.
