# Metafore Graphic Design Tokens

## Color Palette

### Teal Stack (brand)
| Token | Hex | Usage |
|---|---|---|
| `tealDark` | `#004D50` | Deep emphasis, KPI band bg, large quarter of product mark |
| `teal` | `#006B6F` | Primary brand, eyebrow accents, links, active states, **light-surface strokes** |
| `tealOnDark` | `#88DCE0` | **Accents, strokes, labels & hero word on dark teal bands** |
| `tealLight` | `#E8F4F5` | Right-panel fill, tinted callouts, card backgrounds in dark panels |
| `tealAccent` | `#00989E` | **Retired** — low contrast. Use `teal` on light, `tealOnDark` on dark, `logoDark` for mid-stack tile fills. |
| `tealBright` | `#00C4CC` | **Retired** — too cyan. Do not use. |

### Logo Teals
| Token | Hex | Usage |
|---|---|---|
| `logoDark` | `#035657` | Headline accent word, chart series |
| `logoLight` | `#67A4A4` | Secondary chart series, gradient endpoint |

### Ink Stack
| Token | Hex | Usage |
|---|---|---|
| `ink` | `#1A1A1A` | Primary text, headlines |
| `ink-2` | `#404040` | Body text, lede |
| `ink-3` | `#666666` | Card headers, footer labels |
| `ink-4` | `#999999` | Muted labels, stalled states |

### Semantic
| Token | Hex | Usage |
|---|---|---|
| `coral` | `#D94A30` | Fail, bad, negative delta |
| `amber` | `#C48800` | Warning, at-risk |
| `success` | `#22C55E` | Pass, good, positive outcome |

### Surface
| Token | Hex | Usage |
|---|---|---|
| `bg` | `#FFFFFF` | Base background |
| `bgSolid` | `#F8FAFA` | Alternating section fill |
| `line` | `rgba(0,0,0,0.08)` | Dividers, borders |

## Typography Scale

### Headlines (Geist → Inter fallback)
- Blog hero: 56-60px, weight 400, line-height 1.04-1.06, tracking -0.025em
- OG image: 42-48px, same weight/tracking
- Pull-quote: 72px, weight 400, line-height 1.18, tracking -1.4px

### Eyebrows (IBM Plex Mono)
- 10-13px, weight 600, letter-spacing 0.14-0.18em, uppercase, teal color

### Body/Lede (Inter)
- 16px, weight 400, line-height 1.55, ink-2 color, max-width 460px

### Card Elements (IBM Plex Mono)
- Headers: 10px, 600 weight, 0.16em spacing, uppercase, ink-3
- Stats (large): 26-32px, 500 weight, tabular-nums, -0.02em tracking
- Stats (small): 10-12px, 600 weight, tabular-nums
- Pills: 9px, 600 weight, 1.2px spacing, uppercase, 999px radius
- Phase numbers: 9px, 600 weight, 0.12em spacing, uppercase, ink-4

### Card Labels (Inter)
- 11-13px, 500 weight, ink or ink-mid color

## Shared CSS Reset

```css
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  background: #FFFFFF;
  color: #1A1A1A;
  font-family: 'Geist', 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
}
```

## Card Construction

```css
.card {
  background: #FFFFFF;
  border-radius: 8px;
  padding: 32px 36px;
  border: 1px solid var(--line);   /* no shadow anywhere — solid surfaces (marketing 2026) */
}
```

Cards inside illustration blocks use the same 1px border — no elevation shadow.

## Status Pills

```css
.pill {
  display: inline-block;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1.2px;
  padding: 3px 8px;
  border-radius: 999px;
  text-transform: uppercase;
}
.pill.teal    { background: #E8F4F5; color: #006B6F; }
.pill.success { background: #DCFCE7; color: #166534; }
.pill.warning { background: #FEF3C7; color: #92400E; }
.pill.danger  { background: #FEE2E2; color: #991B1B; }
```

## Progress Bars

```css
.bar-track {
  height: 6px;
  border-radius: 3px;
  background: #F0F0F0;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  border-radius: 3px;
}
.bar-fill.fail  { background: #D94A30; }
.bar-fill.warn  { background: #C48800; }
.bar-fill.stall { background: #999999; }
.bar-fill.good  { background: #006B6F; }
```
