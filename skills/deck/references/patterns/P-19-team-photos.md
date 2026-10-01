# P-19 · Team photos

**When:** "meet the team". Pair with P-04B. **Tier:** `semantic`.

```html
<section class="slide p-team-photos" data-pptx="semantic" data-pattern="P-19">
  <div class="section-label">Team</div>
  <!-- @logo:icon-light width="72" height="60" class="icon-tr" -->
  <div class="head"><h2>The people behind <span class="accent">Metafore</span></h2></div>
  <div class="people" style="--cols: 4">
    <div><div class="photo"><svg class="ph" viewBox="0 0 100 100" preserveAspectRatio="none"><line x1="0" y1="100" x2="100" y2="0"/></svg><span class="ph-label">Photo</span></div>
      <div class="name">Name Surname</div><div class="role">Role · Company</div></div>
    <!-- 4 per row; 5–6 people → --cols: 3 and a second row -->
  </div>
  <!-- @footer -->
</section>
```

- Placeholder = diagonal slash + "PHOTO" label (reads as "photo goes here"). Replace with `<img>` inside `.photo` for real headshots. Never stock silhouettes.
