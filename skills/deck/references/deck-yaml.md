# Deck content file (`deck.yaml`)

Author decks as YAML. `scripts/build_deck.py` turns it into the slide HTML (classes, chrome, footers, tiers, data attributes), then the usual check and PPTX steps run:

```
python3 scripts/build_deck.py Decks/<deck>/<deck>.yaml --check --pptx
```
→ `<deck>.html` + `_build/<deck>.sheet.png` + `<deck>.pptx`. The PPTX is skipped while the check has errors. `--src` also writes the generated HTML source.

**Edit the YAML with targeted edits and re-run the one command.** Don't edit the built `.html`.

## Text markup (every text field)
- `*accent words*` → the two-tone accent (switches to `--teal-on-dark` on dark slides)
- `` `code` `` → inline mono
- `[ADD: …]` / `[+ add yours]` → grey dotted placeholder
- raw HTML passes through (`<b>`, `&nbsp;` to keep the last two words of a title together)
- Quote strings that contain `: ` or start with `[`, `*`, `>`, `{` or `"`

## Top level
```yaml
title: Deck name — Metafore      # <title>
css: |                            # optional, short: per-deck tweaks only
  .s1 h4 { … }
slides: [ … ]
```

## Every slide
| Field | Meaning |
|---|---|
| `pattern` | template name below (or `P-06` style ids) |
| `label` | section label top-left; turns on auto chrome (label, icon, footer). Cover, divider, closing get chrome without one |
| `notes` | speaker notes → PPTX notes pane |
| `tier` | override `hybrid` / `semantic` / `image` |
| `dark` | `true` → teal-dark surface variant where the pattern has one |
| `style` | CSS vars/props on the slide, e.g. `{--cols: 4}` |
| `ignore` | waive checks for deliberate rule-breaking, e.g. `voice` on a slide that quotes banned words |
| `extra` / `html` | raw HTML appended / replacing the generated body (escape hatch) |

## Shared objects
- **card** (locked product mock-up): `{eyebrow, meta, title, kpis: [[n, label]], rows: [[k, v]] or [[k, text, high|watch|ok]], bars: [[k, pct, v]], trace: [[phase, text]], tree: [[dir, file], ["", file, muted]], changes: [[mark, text]], buttons: [..], cta, html, style}` — ≤ 3 rows of any one kind; vary the form across slides.
- **art** (statement right side, vertical media): `{icon: Name, size: lg}` · `{card: …}` · `{dead: [[label, n]]}` (problem slides) · `{hub: …}` · `{svg: "<svg…>"}` · `{html: …}` · `{specimen: …}`
- **hub** (one source feeding N outputs): `{center: BRAND PACK, sub: [..], items: [..], label}`
- **specimen** (deliberately off-brand training example): `{class, html, tag, style, ignore}` — checks waived by default except overlap/overflow/colour.

## Patterns
| `pattern` | Fields | Rules |
|---|---|---|
| `cover-1a` / `cover-1b` / `cover-1c` | `title` (string or list of lines), `subtitle`, `card`, `badge` (1b) | Title ≤ 6 words; 1a = metric, 1b = vision, 1c = definition |
| `divider` | `eyebrow`, `title`, `subtitle`, `progress: [..]`, `current: n` | 1–2 per deck; progress mirrors the agenda |
| `agenda` | `title`, `items: [[Title, one-sentence sub]]` | 4–10 Title Case items |
| `company` | `title`, `body`, `signature`, `facts: [[icon, label, value, sub]]` | body ≤ 3 lines |
| `track` | `title`, `body`, `cards: [{icon, title, body}]` | 4 cards |
| `statement` | `eyebrow`, `title`, `body`, `bullets`, `stats: [[n, label]]`, `small`, `art` | `dark: true` for the 84px dark version |
| `quiz` | `title`, `specimen`, `answers: [..]`, `notes` | training only |
| `grid4` | `title`, `body`, `tiles: [{icon, tag, title, body}]` | 3–4 tiles, distinct icons, body ≤ 3 lines |
| `grid8` | `title`, `body`, `cells: [{tag, icon, title or mono, body}]` | 5–8 cells (6 → 3 columns) |
| `modules` | `title`, `modules: [{for, name: "MetaWorks *Focus*", body}]` | 9–12 |
| `kpi` | `label`, `title`, `kpis: [[num, suffix, label]]`, `source` | 2–4 real numbers + source |
| `integrations` | `title`, `body`, `small`, `clusters: [{label, pills: [..]}]` | real system names |
| `timeline` | `title`, `body`, `steps: [{when, num, title, body}]`, `code`, `note` | 3–6 steps |
| `radial` | `title`, `body`, `bullets`, `stats`, `small`, `hub` or `svg` | `dark: true` for the dark version |
| `hero-card` | `eyebrow`, `title`, `body`, `bullets`, `scale: [{label, pct, text, tag}]`, `meta: [[label, value]]`, `card` | solid card; glass is cover-only |
| `scenario` | `title`, `body`, `card`, `traces: [{num, title, role, body}]`, `sources: {label, pills}` | vary the card per scenario |
| `anchor` | `title`, `anchor`, `body`, `traces`, `sources` | |
| `compare` | `title`, `cols: [{label, icon, stat: [n, label], bullets, body, card, specimen}]`, `note` | one real before/after |
| `quote` | `quote`, `attribution` | one per deck, real people only |
| `arch` | `title`, `layers: [{title, body, chips: [..]}]` | |
| `team` | `title`, `people: [[name, role, photo-url?]]`, `cols` | |
| `table` | `title`, `cols: "1fr 0.8fr 2fr"`, `head: [..]`, `rows: [[..]]`, `kinds` | 4–8 rows, cells ≤ 2 lines |
| `industries` | `title`, `cols`, `cards: [{icon, label, title, body or quote}]` | holds any N |
| `vertical` | `title`, `lede`, `rows: [[title, body]]`, `art` | Mira on telecom only |
| `closing` | `title` (ends with a period), `cta` | last slide |
| `raw` | `html`, `class`, `tier`, `pattern_id` | anything the templates can't express |

## Example
```yaml
title: Pulse for network ops — Metafore
slides:
- pattern: cover-1b
  title: [Introducing, "*MetaWorks*"]
  subtitle: The enterprise operating system that thinks, acts, and builds
  card: {eyebrow: Pulse · Network ops, meta: "09:42", title: Fibre cut, Metro East,
         rows: [[Subscribers affected, "18,204"], [Crew ETA, 38 min]], cta: Dispatch crew}
- pattern: kpi
  label: Outcomes · 90 days
  title: Measured across the first three *deployments*
  kpis: [[−38, "%", Mean time to resolution], [3, ×, Faster onboarding]]
  source: "Source: customer Pulse exports, Q1–Q2 2026"
- pattern: closing
  title: Let's design your first *cognitive workflow.*
  cta: hello@metafore.ai · metafore.ai
```
