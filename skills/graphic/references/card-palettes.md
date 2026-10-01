# Card Illustration Backgrounds — brand teal stack

Type 4 tile backgrounds stay inside the teal stack. The legacy rainbow palette (indigo, emerald, sky, slate, mint, violet, periwinkle) is **removed from the system**.

## Tile fills

| Class | Token | Hex | When to use |
|---|---|---|---|
| `.bg-dark` | `--teal-dark` | `#004D50` | Heaviest emphasis tiles |
| `.bg-teal` | `--teal` | `#006B6F` | Primary brand tiles |
| `.bg-acc` | `--logo-dark` | `#035657` | Mid-stack accent tiles — solid fill, white content on top. (Previously `#00989E`, now retired everywhere.) |
| `.bg-light` | `--teal-light` | `#E8F4F5` | Light accent tiles (pair with teal dots) |
| `.bg-solid` | `--bg-solid` | `#F8FAFA` | Quiet / neutral tiles (pair with teal dots) |

When arranging tiles in a row, order them so the fills read as a deliberate teal progression (e.g. `bg-dark → bg-teal → bg-acc → bg-light`) rather than a random mix. `#00989E` is retired — never use it, including as a fill.

## Dot-fade overlays

Each tile uses **one** duotone-fade dot pattern. Vary the corner-origin across tiles in the same row so the set reads as visual variety without leaving the brand.

Pick the dot color based on the fill:
- **WHITE dots** on `--teal-dark`, `--teal`, `--logo-dark`
- **TEAL dots** on `--teal-light`, `--bg-solid`

```css
/* WHITE dot variants — for dark teal fills */
.halftone-w-tl::before{
  content:"";position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(circle at 1px 1px,rgba(255,255,255,.32) 1px,transparent 1.4px);
  background-size:10px 10px;
  mask-image:radial-gradient(ellipse at 0% 0%,rgba(0,0,0,.9) 0%,transparent 55%);
  -webkit-mask-image:radial-gradient(ellipse at 0% 0%,rgba(0,0,0,.9) 0%,transparent 55%);
}
.halftone-w-tr::before{ /* same — change mask-image ellipse origin to 100% 0% */ }
.halftone-w-bl::before{ /* origin 0% 100% */ }
.halftone-w-br::before{ /* origin 100% 100% */ }

/* TEAL dot variants — for light fills */
.halftone-t-tl::before{
  content:"";position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(circle at 1px 1px,rgba(0,107,111,.35) 1px,transparent 1.4px);
  background-size:10px 10px;
  mask-image:radial-gradient(ellipse at 0% 0%,rgba(0,0,0,.9) 0%,transparent 55%);
  -webkit-mask-image:radial-gradient(ellipse at 0% 0%,rgba(0,0,0,.9) 0%,transparent 55%);
}
/* + halftone-t-tr / halftone-t-bl / halftone-t-br with rotated mask origins */
```

## Inner UI card variety

Each tile holds a small floating UI mockup depicting the capability. Across a 4-tile row, vary the UI form so the set doesn't look like four identical KV-row cards. Mix at least three of:

| Variant | When to use |
|---|---|
| **KV rows** | Multi-attribute capability (Plan / Status / Notified count) |
| **Vertical bar chart** | Daily / weekly trend across categories |
| **Donut chart** (conic-gradient) | Share / coverage percentage (e.g. 62% pre-cleared) |
| **Sparkline / area chart** | Continuous trend with a current value |
| **Horizontal bar chart** | Ranked categories (by hub, by region) |
| **Status timeline** | Multi-step process with current step pulsed (amber) |
| **Process flow stepper** | Sense / Reason / Act / Close |

### Base tile + UI card CSS

```css
.tile .ill{
  aspect-ratio:4/3; border-radius:14px; padding:24px;
  position:relative; overflow:hidden;
  display:flex; align-items:center; justify-content:center;
}
.tile .uic{
  position:relative; z-index:2;
  background:#fff; border-radius:10px;
  padding:14px 16px; width:90%;
  border:1px solid var(--line);   /* no shadow — solid surfaces only */
}
.tile .uic .h{
  font-family:'IBM Plex Mono',monospace;
  font-size:13px;font-weight:600;letter-spacing:.16em;
  text-transform:uppercase;color:var(--ink-3);
  margin-bottom:10px;display:flex;justify-content:space-between;
}
.tile .uic .h .p{
  font-size:13px;padding:2px 6px;border-radius:999px;
  background:var(--teal-light);color:var(--teal);
}
.tile .uic .h .p.warn{background:#FEF3C7;color:#92400E}
.tile .uic .h .p.bad{background:#FEE2E2;color:#991B1B}
```

### Donut recipe

```css
.donut{
  width:80px;height:80px;border-radius:50%;
  background:conic-gradient(var(--teal) 0 62%,var(--teal-light) 62% 100%);
  display:flex;align-items:center;justify-content:center;
}
.donut .ring{
  width:54px;height:54px;border-radius:50%;background:#fff;
  display:flex;align-items:center;justify-content:center;
  font-family:'IBM Plex Mono',monospace;
  font-size:15px;font-weight:600;color:var(--teal-dark);
}
```

### Sparkline recipe

```html
<svg viewBox="0 0 100 50" preserveAspectRatio="none">
  <defs>
    <linearGradient id="sparkArea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#006B6F" stop-opacity=".22"/>
      <stop offset="1" stop-color="#006B6F" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <path d="M0 36 L 14 32 L 28 28 L 42 24 L 56 22 L 70 18 L 84 14 L 100 10 L 100 50 L 0 50 Z" fill="url(#sparkArea)"/>
  <path d="M0 36 L 14 32 L 28 28 L 42 24 L 56 22 L 70 18 L 84 14 L 100 10" fill="none" stroke="#004D50" stroke-width="1.8" stroke-linejoin="round"/>
</svg>
```

## What NOT to use

- **No rainbow palettes** — indigo, emerald, sky, slate, mint, violet, periwinkle are retired
- **No diagonal stripes** — `repeating-linear-gradient` stripe overlays are forbidden anywhere on the surface
- **No double-stacking** — never combine a full dot grid with a duotone-fade on the same surface; pick one
- **No untextured tiles** — every tile needs ONE dot-fade overlay for tactile depth
- **No drop shadows anywhere** — the illustration block and the inner UI card both separate with a 1px border.
