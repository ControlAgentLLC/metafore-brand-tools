---
name: dashboard
description: Build Metafore-branded internal dashboards, admin panels, and operator UIs in HTML/CSS. Use this skill whenever a Metafore teammate asks for a dashboard, admin tool, operator console, exec dashboard, supply chain panel, monitoring view, command-center mockup, or any internal Metafore-branded interface — even if they don't say "dashboard" explicitly (e.g. "build me a screen for X", "make a UI mockup for the Y team", "I need a Metafore-style admin page"). Encodes the Metafore dashboard look-and-feel: 64px icon sidebar, search-led topbar, large two-tone hero (`Word black + word teal`), rounded-card grid with status modifiers, IBM Plex Mono labels and KPI numbers in Brut Grotesque, logo-keyed teal chart palette, and an "I want to…" composer at the bottom.
---

# Metafore Dashboard Builder

You are helping a Metafore teammate produce a brand-compliant internal dashboard or admin UI. The default deliverable is a single self-contained `.html` file (no build step, fonts via Google Fonts CDN) that renders the Metafore dashboard look-and-feel and can be opened directly or served via `python3 -m http.server`. The same system maps cleanly to React/Tailwind if a real product surface is being built.

## Brand reference (read before producing)

Every Metafore artifact follows the same brand invariants. Before drafting, Read the shared brand pack at `../../assets/brand/metafore_brand.md` (voice rules, AI-tell blocklist, design tokens, type stack) and skim any relevant `../../assets/brand/feedback_*.md` files. These supersede anything older you may have seen.

## When this triggers

Any Metafore-internal request along the lines of:
- "Build me a dashboard / admin panel / operator console for [X]"
- "Make an internal UI for [team / product / scenario]"
- "Mock up a screen for [exec / supply chain / pipeline / fleet] view"
- "Add a [card / chart / table] to the dashboard"
- "Build a Metafore-style [admin / monitoring / command-center] interface"
- Any reference to existing Metafore dashboard surfaces (Enterprise Intelligence, Supply Chain, Mira ops view, Airline EOP, etc.)

Do **not** trigger for: marketing landing pages, brochures, slide decks, customer-facing product sites, or non-Metafore work. (Brochures live in `metafore:brochure`. Slide decks live in `metafore:deck`.)

## Hard rules — non-negotiable

These are the things that make a screen read as "Metafore dashboard" at a glance. Do not improvise around them.

1. **Two-tone hero.** Every page has one large `h1` at the top. The **first word(s)** are inky black `var(--ink)`, the **last word** is the logo dark teal `#035657`. Wrap the second word in `<span class="it">…</span>`. No italics, no serif, weight 400. Use the `--serif` stack (`Brut Grotesque, Geist, Inter`).
2. **Type stack.** Three fonts only:
   - **Headers / decorative numbers / hero** — `var(--serif)` (Brut Grotesque → Geist fallback). Always weight 400. **Never italic.**
   - **Body / nav / chips / buttons** — Inter.
   - **Labels / KPI units / mono callouts** — IBM Plex Mono.
3. **Logo, top-left.** The Metafore mark (inline SVG, see `../../assets/graphics/logos/dashboard-icon.svg` — the dashboard-specific 53×42 mark) sits in a 32×32 slot at the top of the 64px sidebar. Never a text wordmark. Never the legacy "Metaworks EGI" header.
4. **64px icon sidebar.** Vertical, icon-only nav. Active item is a black square (8px radius) with a white icon. Inactive items are gray, hover lightens. Workspace badge (2-letter) lives at the bottom.
5. **Search lives in the left of the topbar**, where a wordmark would normally go. The right side holds an `Activity` button + avatar. No brand text in the topbar.
6. **Card grid.** 4-column grid of rounded 14px cards with a 1px `--line` border and 18px gap. Wide cards span 2 or 4. No drop shadows on cards by default — borders only.
7. **No side accent bars on cards** in the default look. (We tried them, then removed them.) Status is conveyed by a small colored dot in the `.label` row, not by a left stripe.
8. **Toggle buttons** are the iOS-segment style: transparent inactive (`color: var(--ink-3)`), active is a white pill with a 1px border and a featherlight shadow. **Never** the old black-fill pill.
9. **Charts use logo teals**, not multi-hue palettes:
   - Primary series → `var(--logo-dark)` `#035657`
   - Secondary series → `var(--logo-light)` `#67A4A4`
   - Tertiary / accent series → `var(--teal-on-dark)` `#88DCE0` (was retired `#00C4CC`)
   - Sparkline up = `--logo-dark`, down = `--logo-light`, flat = `--teal` `#006B6F`
10. **Bottom of every dashboard** has an "I want to…" prompt block over a composer input. This is the dashboard's voice — it tells the user the surface is interrogable in plain English.

## File scaffolding

Default output path: `<project>/mockups/<slug>.html`. If the project already has a mockups folder, drop it in there. If not, create one.

After writing, start (or reuse) a local server:

```bash
lsof -ti :8765 | xargs -r kill -9 2>/dev/null
cd "<absolute path to mockups folder>" && python3 -m http.server 8765
```

Then `open "http://localhost:8765/<slug>.html"`. If multiple dashboards live in the folder, add a small tab switcher in the top-right of each page that links to the other files (see `references/components.md` for the snippet).

## Workflow

### 1. Gather what's on the page

Before writing CSS, get the content blocks. Ask the user only for what you can't infer. Defaults you should fill in yourself:
- Hero headline (always two-tone — pick the natural break, e.g. "Enterprise *Intelligence*", "Supply *Chain*", "Morning *Elana*")
- Subtitle (one editorial sentence under the hero)
- 4–8 KPI cards (each: monospace label, big serif number, tiny unit/delta, one-line footnote)
- 1–2 wide blocks (executive summary, table, chart, recent activity, or a featured record)
- 4–6 suggestion chips
- 3 "I want to…" prompts that are domain-specific

If the user hands you a messy spec, **you** do the structuring.

### 2. Build from the starter template

Copy `references/starter-template.html`, then edit content in place. Do **not** re-derive CSS from scratch — the tokens, layout, and component recipes in the template are load-bearing. If you need a component that isn't there (kanban, calendar, log stream), build it on top of the same tokens, don't fork.

For each KPI card, decide on a status: default (teal bar / no bar), `.warn`, `.bad`, or `.ok`. The current default is **no left bar**. If you re-enable bars (only if the user asks), they go flush with the card's left edge, vertically centered, 38px tall.

### 3. Verify before reporting done

After writing the file, do all of:
- `curl -sI http://localhost:8765/<slug>.html` returns `200`
- The hero second word is rendering in `#035657` (not gray, not black)
- All chart strokes/fills resolve to a teal token (no leftover `#1a1a1a`, `#c89321`, `#8aa1d6`)
- No `'Instrument Serif'` or `'JetBrains Mono'` references slipped through
- The Metafore SVG mark is in the sidebar (not a placeholder `<svg><path d="M3 20…"/></svg>`)

If a UI affordance is observable (button hover, toggle, table row), confirm it via the browser preview before saying it works — don't just trust the markup.

## References

- [`references/design-tokens.md`](references/design-tokens.md) — full token table (colors, typography, spacing, radii)
- [`references/components.md`](references/components.md) — card variants, hero, topbar, toggle, table, chart, composer
- [`references/starter-template.html`](references/starter-template.html) — copy-paste scaffold
- [`../../assets/graphics/logos/dashboard-icon.svg`](../../assets/graphics/logos/dashboard-icon.svg) — the inline Metafore mark (shared)

## What to push back on

- Requests for **gradients** on cards or backgrounds. The system is flat.
- Requests for **multiple chromatic families** in a single chart. Use the teal stack with shape/weight to differentiate.
- Requests to **center-align** body content. Everything is left-aligned except pill tags.
- Requests for **bold (700+) hero text**. Hero is always weight 400; the size carries the weight.
- Requests for **italic** anywhere in headers. We removed it on purpose.
- Requests to bring back the **"Metaworks EGI"** wordmark in the topbar. The logo + workspace badge in the sidebar is the brand statement.

If the user asks for any of the above, gently flag the rule and ask if they want to override before doing it.
