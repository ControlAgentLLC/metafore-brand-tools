# PPTX build — `scripts/build_pptx.py`

```
python3 scripts/build_pptx.py Decks/<deck>/<deck>.html [--out deck.pptx] [--build-dir _build] [--no-cache] [--scale 2]
```
Input is the **built** HTML (placeholders resolved by `build_html.py`). Output `<deck>.pptx` next to it; renders and `cache.json` in `<deck dir>/_build/`. Exit 0 ok · 1 input error · 2 missing dependency (prints the `pip install` line). A fresh 15-slide build takes well under a minute; unchanged slides are cached.

stdout is one line per slide plus warnings — this is the verification. Don't open the PNGs.
```
01 hybrid   cover         frames=5 pictures=0
02 semantic company       frames=12 pictures=4 shapes=6
   ! 1 run(s) under 22px (smallest 16px: 'Source: internal & partner…')
```

## What each tier becomes

| Tier | PPTX |
|---|---|
| `hybrid` | Full-bleed 2× background PNG rendered with editable text made transparent (backgrounds, borders, pills, bullets keep their colors) + native text frames on top |
| `semantic` | No screenshot: slide fill from the computed background; native rectangles/rounded rectangles for every filled or bordered box (1px borders → 9525-EMU lines); each `<img>`/non-text `<svg>` as a picture with its alt text; native text frames |
| `image` | One full-bleed 2× PNG; nothing editable |

`[data-pptx-lock]` containers stay baked (hybrid) or become one picture (semantic). Text inside `<svg>` is always baked. `<aside class="speaker-notes">` → notes.

## Text frames — automatic

Any element that carries text (headings, paragraphs, list items, plain blocks whose children are inline) becomes one frame at its content box; `.line` spans and block children become paragraphs; each run takes its **computed** font, size, color, tracking, and case — so any accent class works, no class map. Legacy decks that mark `[data-pptx-text]` keep explicit mode (only marked nodes become frames).

Brand rules the builder enforces: 1920px → 13.333" at 6350 EMU/px and 0.5 pt/px; exact line spacing from CSS line-height; Plex Mono never bold and never tracked; negative tracking clamped to 0 under 22px; headers (Geist) never bold; italics written upright (with a warning); semi-transparent colors blended to solid; every shape's shadow and theme style stripped; single-line frames get 2% width slack against font substitution.

## Warnings worth acting on

- `run(s) under 22px` — raise the size in the source (only locked mockup text may be smaller).
- `italic run(s)` — remove the italic in the source.
- `font not available` / `fonts.ready > 10s` — Google Fonts didn't load; positions may be off. Re-run online.
- `::before/::after dropped` (semantic) — move the decoration into real markup, or make the slide `hybrid`.
- `visible text outside [data-pptx-text]` — explicit-mode slide missing a marker; remove the markers to use automatic mode.
- `centred … text frame(s) with a ::before marker` — left-aligned text frames start after CSS bullets/counters automatically; centred ones can't, so check those in PowerPoint (`office_check.py`).

## Limits

- `z-index`, transforms, and overflow clipping aren't modeled on semantic slides (shapes follow DOM order at their on-screen boxes) — use `hybrid` for layered compositions.
- Edits to external stylesheets need `--no-cache` (inline `<style>` is hashed).
- Text positions are measured in Chromium; PowerPoint without Geist/Inter installed falls back to system fonts and may reflow slightly.
- No animations, transitions, embedded media, themes, or live charts — decks are static; charts are baked.
