# Metafore Dashboard — Design Tokens

These are the tokens. Don't improvise colors, fonts, or radii. Pull these into the `<style>` block of every dashboard.

## Color palette

```css
:root {
  /* Surface — primarily B&W */
  --bg: #ffffff;
  --panel: #ffffff;
  --ink: #0a0a0a;
  --ink-2: #2a2a2a;
  --ink-3: #6b6b6b;
  --ink-4: #9a9a9a;
  --line: #ececec;
  --line-2: #f3f3f3;
  --hover: #f7f7f7;
  --chip: #f4f4f4;

  /* Logo teals — exact colors from the Metafore mark */
  --logo-dark: #035657;       /* primary brand teal — second-word headers, default chart series */
  --logo-light: #67A4A4;      /* secondary brand teal — secondary chart series, lighter accents */

  /* Extended Metafore teal stack — use only when --logo-dark/light aren't enough.
     Accents/strokes/labels: --teal on light, --teal-on-dark on dark. */
  --teal-dark: #004D50;
  --teal: #006B6F;
  --teal-on-dark: #88DCE0;    /* accents/strokes/labels on dark; tertiary chart series */
  --teal-light: #E8F4F5;      /* tinted callout fills, light table headers */
  --teal-accent: #00989E;     /* DEPRECATED — use --teal (light) / --teal-on-dark (dark) */
  --teal-bright: #88DCE0;     /* DEPRECATED alias — repointed to --teal-on-dark (was retired #00C4CC) */

  /* Status — for state, not decoration */
  --success: #00896A;
  --success-bg: #E6F2EE;
  --warn: #C48800;
  --warn-bg: #FBF3DF;
  --danger: #D94A30;
  --danger-bg: #FBEAE5;

  /* Header coloring shortcuts */
  --header: var(--ink);            /* first-word color */
  --header-2: var(--logo-dark);    /* second-word color (the teal) */

  /* Type stack */
  --serif: 'Brut Grotesque', 'Geist', 'Inter', sans-serif;
}
```

### Color rules

- **Primary palette is B&W.** Teal shows up only in: hero second word, KPI numbers (optional), chart series, the live indicator dot, and link hover states.
- **No semantic colors as decoration.** `--warn` / `--danger` exist for actual state changes (overdue items, blocked builds). Don't use them to "spice up" a layout.
- **No gradients.** Flat fields only.
- **One accent family per chart.** Use the teal stack with shape/weight to differentiate series, not a second hue.

## Typography

### Google Fonts import

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

Brut Grotesque is the licensed Pangram Pangram face — it won't load on the web. Geist is the closest free fallback and is what will actually render. Don't apologize for this in the file; the stack handles it.

### Three roles

| Role | Font | Weights | Used for |
|---|---|---|---|
| **Headers / decorative** | `var(--serif)` | 400 only | Hero h1, KPI numbers, large stat callouts, big section heads |
| **Body** | Inter | 400, 500, 600 | Topbar text, nav, body copy, table cells, chips, buttons |
| **Labels / mono** | IBM Plex Mono | 400, 500, 600 | KPI labels (`OPEN ISSUES`), tags, numeric badges, monospace UI |

### Canonical type scale — Perfect Fifth default, Perfect Fourth floor

The dashboard uses the same canonical scale as every other Metafore artifact. Headers auto-shrink between default and floor to fit max 2 lines; body, lede, and labels never shrink.

```css
:root {
  --h1-size: 36px;      /* default */
  --h1-floor: 28px;     /* floor — Perfect Fourth */
  --h2-size: 24px;      /* default — section heads */
  --h2-floor: 21px;     /* floor */
  --h3-size: 18px;      /* fixed */
  --body-size: 16px;    /* FIXED — never shrinks */
  --lede-size: 18px;    /* FIXED — never shrinks */
  --eyebrow-size: 14px; /* Plex Mono — UI-chrome floor */

  --lh-header: 1.125;
  --lh-body:   1.200;
  --tracking:  0;       /* zero letter-spacing everywhere */
  --h1-max-width: 24em; /* container max-width when header hits floor and still wraps */
}
```

| Role | Size | Line-height | Tracking | Notes |
|---|---|---|---|---|
| Hero h1 | clamp(28px, 6.5cqw, 36px) | 1.125 | 0 | Auto-shrinks. Use `container-type: inline-size` on the hero wrapper. |
| KPI stat number | clamp(28px, 6.5cqw, 36px) | 1.125 | 0 | Treated as an H1; auto-shrinks within the KPI card. |
| KPI unit/delta | 16px | 1.200 | 0 | Inter, `var(--ink-3)`, weight 500. |
| Section h2 | clamp(21px, 4.2cqw, 24px) | 1.125 | 0 | Auto-shrinks. |
| Section h3 | 18px | 1.125 | 0 | Fixed. |
| Body lede | 18px | 1.200 | 0 | Never shrinks. |
| Body | 16px | 1.200 | 0 | Never shrinks. |
| KPI label | 14px | 1.200 | 0 | UPPERCASE, IBM Plex Mono, no tracking. |
| Eyebrow / pill | 14px | 1.200 | 0 | UPPERCASE, IBM Plex Mono, no tracking. |

### Typography rules

- **Hero is always weight 400.** Never bold. The size carries the weight.
- **Hero is never italic.** The two-tone treatment carries the editorial feel.
- **Tracking is 0 everywhere.** No negative letter-spacing on the hero. No positive tracking on Plex Mono labels — they were tracked +0.06–0.08em historically, that rule is retired.
- **Line-height is 1.125 on every header and KPI number; 1.200 on body, lede, eyebrow, and label.** No more `line-height: 1` on stat numbers.
- **Headers fit on max 2 lines.** Auto-shrink via `clamp()` + container queries; never let H1 overlap H2 or body.
- **Margins between H1, H2, and body are proportional to each element's own font-size.** When a header shrinks, its margins shrink with it.
- **All-caps labels are always Plex Mono**, never Inter.
- **Tabular numerics on stat numbers.** Add `font-variant-numeric: tabular-nums;` to `.stat` if comparing aligned numbers in a column.

## Spacing

| Token | Value | Used for |
|---|---|---|
| Sidebar width | 64px | Fixed, vertical icon nav |
| Topbar height | ~64px | Padding 14px 28px |
| Hero vertical | 36px top, 18px bottom | Padding above/below the h1 block |
| Grid horizontal | 28px | Padding around the card grid |
| Card gap | 18px | Between cards in the grid |
| Card padding | 20px 20px 18px | Inside each card |
| Card inner padding-left | 10px | Legacy from the bar era; keep so existing left-rule alignment still works |

## Radii

| Element | Radius |
|---|---|
| Cards, composer, prompt block | 14px |
| Buttons, pills, segment buttons | 8px–10px |
| Sidebar nav items, icon buttons | 8px |
| Status badges, mono tags | 4px |
| Capsule pills | 999px |
| Avatar | 50% |

## Borders & elevation

- Default card border: `1px solid var(--line)` (`#ececec`).
- Hover card border: `1px solid #d6d6d6`.
- **No drop shadows on cards.** A `0 1px 2px rgba(0,0,0,.04)` shadow is allowed on the active toggle pill and nowhere else.

## Status mapping (for KPI cards & dots)

| Status | Dot color | Bar (if enabled) | Footnote text |
|---|---|---|---|
| default / ok | `#1f7a4d` | `var(--success)` | `var(--ink-3)` |
| warn | `#c89321` | `var(--warn)` | `#8a5a13` |
| bad / danger | `#a02b1d` | `var(--danger)` | `#8a2a1f` |
| idle | `#b8b8b8` | n/a | `var(--ink-4)` |

The colored bar on the left edge of cards is currently **off** in the default look. If the user wants it back, see `components.md`.
