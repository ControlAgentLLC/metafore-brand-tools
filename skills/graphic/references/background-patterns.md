# Metafore Graphic Background Patterns

The system uses ONLY dot-based textures. Two patterns:

1. **Full dot grid** — small evenly-spaced dots (~6–8px) covering the surface
2. **Duotone-fade dot pattern** — dots that fade out via a radial mask anchored to one corner

**Never combine the two on the same surface. Never use diagonal stripes — those have been removed from the system.**

## When to use which (and when to use neither)

| Surface | Texture |
|---|---|
| Type 1A right panel (teal-light) | Full dot grid (signature) |
| Type 1B (1422×800 solid dark teal) | **Solid — no dots** |
| Type 1C right panel (solid dark teal) | **Solid — no dots** |
| Type 2 conversational card background (solid dark teal) | **Solid — no dots** |
| Type 3 small data card | One duotone-fade dot pattern (over soft wash) |
| Type 4 capability tiles | One duotone-fade dot pattern, varied corner per tile |
| Type 5 dark concept illustrations | One full dot grid on the dark backdrop |
| Type 6 horizontal feature | One duotone-fade dot pattern (over soft wash) |

**Rule of thumb:** the larger / more dominant the dark-teal surface, the cleaner it should be. Full-bleed dark-teal heroes are SOLID. Smaller surfaces or light-tinted surfaces can carry a single dot pattern.

## Pattern recipes

### 1. Full dot grid (Type 1A right panel)

```css
.surface{
  background-color:var(--teal-light);  /* #E8F4F5 */
  background-image:radial-gradient(circle at 1px 1px,rgba(0,107,111,.32) 1px,transparent 1.6px);
  background-size:6px 6px;
}
```

That's the entire texture. **No additional layered pattern.**

### 2. Duotone-fade dot patterns

Dots fade out from one corner via a radial mask. Vary the corner across surfaces for visual interest.

**Teal dots on light backgrounds:**

```css
.surface{position:relative;overflow:hidden;background:#F0F5F5}
.surface::before{
  content:"";position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(circle at 1.5px 1.5px,rgba(0,107,111,.32) 1.5px,transparent 2px);
  background-size:10px 10px;
  mask-image:radial-gradient(ellipse at 100% 100%,rgba(0,0,0,.85) 0%,transparent 55%);
  -webkit-mask-image:radial-gradient(ellipse at 100% 100%,rgba(0,0,0,.85) 0%,transparent 55%);
}
```

Available mask origins:
- `0% 0%` (top-left)
- `100% 0%` (top-right)
- `0% 100%` (bottom-left)
- `100% 100%` (bottom-right)

**White dots on dark backgrounds:**

```css
.surface{position:relative;overflow:hidden;background:var(--teal-dark)}
.surface::before{
  content:"";position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(circle at 1px 1px,rgba(255,255,255,.32) 1px,transparent 1.4px);
  background-size:10px 10px;
  mask-image:radial-gradient(ellipse at 0% 0%,rgba(0,0,0,.9) 0%,transparent 55%);
  -webkit-mask-image:radial-gradient(ellipse at 0% 0%,rgba(0,0,0,.9) 0%,transparent 55%);
}
```

Use white-on-dark sparingly — full-screen dark heroes prefer SOLID (no dots at all).

### 3. Soft atmospheric wash (color base for small cards)

Type 3 small data cards and Type 6 horizontal features start with a very soft layered radial-gradient wash as their BASE color. This is permitted alongside ONE duotone-fade dot pattern — the wash is a color base, not a dot texture, so it doesn't violate the "one pattern" rule:

```css
.frame{
  background:#F0F5F5;
  background-image:
    radial-gradient(ellipse at 18% 80%,rgba(0,107,111,.10) 0%,transparent 55%),
    radial-gradient(ellipse at 85% 18%,rgba(0,107,111,.07) 0%,transparent 60%);
}
```

A single duotone-fade dot pattern can be layered on top via `::before` — still just one dot pattern total.

## Forbidden patterns

- **Diagonal stripes** — `repeating-linear-gradient(135deg, ...)` and similar. Removed entirely from the system. Do not reintroduce.
- **Two dot layers on one surface** — never combine a full dot grid + a duotone fade. Pick one.
- **Photography backgrounds** (with glass overlay) for Type 2 conversational cards. The current system uses solid `--teal-dark` instead.
- **Decorative non-teal gradients on cards** — no aurora gradients, no rainbow washes. The teal stack carries all branded color.

## Background-to-vertical mapping

The general guidance for each vertical's small-card surface (Type 3 / Type 6):

| Vertical / Theme | Atmospheric base | Dot pattern color |
|---|---|---|
| Travel / Airlines | Soft teal wash (`#F0F5F5`) | Teal duotone-fade |
| Banking | Soft neutral wash | Teal duotone-fade (use sparingly) |
| Telecom | Soft teal wash | Teal duotone-fade |
| Supply Chain | Soft teal wash + per-tile teal-stack fills | Per-tile (see `card-palettes.md`) |
| Health | Soft neutral wash | Teal duotone-fade |
| Dev / Integration | Soft teal wash | Teal duotone-fade |
| General / Horizontal | Soft teal wash | Teal duotone-fade |
