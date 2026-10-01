# Metafore logo usage

The SVGs ship in the plugin at `assets/graphics/logos/` (`logo-light`, `logo-dark`, `icon-light`, `icon-dark`, `dashboard-icon`). **Insert them with a placeholder — never paste the paths:**

```html
<!-- @logo:logo-light width="155" height="36" -->   <!-- white / --bg-solid surfaces: Type 7 OG, Type 8 pull-quote -->
<!-- @logo:logo-dark width="142" height="32" -->    <!-- --teal-dark surfaces: Type 1B, 1C glass-card header (98×22) -->
```
`scripts/build_html.py` inlines the SVG and applies the attributes. Native ratio is 155×36 — scale both dimensions together: native for hero / OG / pull-quote, `142×32` for the Type 1B top-left wordmark, `98×22` inside glass-card headers.

## What NOT to do

- **Don't substitute CSS pseudo-element constructions.** The two-quarter-circle mark built with `border-top-left-radius:100%` is retired everywhere. The brand mark is an SVG.
- **Don't use the teal-bright `#00C4CC` variant on dark backgrounds.** The dark-bg variant uses white-at-50%-opacity for the two long curves — never `#00C4CC`.
- **Don't recolor the wordmark for "accent" effects.** The wordmark is `#0A0A0A` on light surfaces and `white` on dark surfaces — those are the only two valid renderings.
- **Don't apply opacity to the whole SVG element.** Opacity belongs only on the two curve paths in the dark-bg variant via `fill-opacity="0.5"`. Wrapping the whole SVG in `opacity:0.5` will fade the wordmark glyphs too, which is wrong.

## Metafore icon (for Type 2 conversational cards) — separate from the wordmark

Inside conversational demo cards (Type 2), the Metafore agent identity uses an **icon**, not the wordmark. The icon is a 36px dark-teal circle with a white chevron SVG:

```html
<div class="ico">
  <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4"
       stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
    <polyline points="6 10 12 16 18 10"/>
  </svg>
</div>
```

```css
.ico{
  width:36px;height:36px;border-radius:50%;
  background:var(--teal-dark);
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;
}
```

Don't substitute the wordmark for this icon, and don't construct it with CSS quarter-circles.
