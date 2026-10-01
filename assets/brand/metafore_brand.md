---
name: Metafore brand system
description: The single source of truth for Metafore positioning, voice, legibility floors, density, visual coverage, design tokens, and content-preservation rules. Every metafore:* skill reads this file; skill files only add format-specific deltas.
type: reference
---

# Metafore brand pack

Read this once per task. Skill files (`skills/*/SKILL.md`) add only what is specific to their format; if a skill file and this pack disagree, this pack wins unless the skill names the rule as a deliberate format exception.

## 1. Positioning

- **Metafore** is the AI-Native transformation platform for the enterprise. The platform product is **Metafore One**; the operating system is **MetaWorks**. **Mira** is the personal AI twin for mobile subscribers, deployed in carrier IMS (renamed from Echo on 2026-04-24) — **Mira naming appears on telecom material only**.
- Metafore is an AI transformation **partner**, focused on topline growth as well as margin.
- CEO: Ori Sasson. HQ: San Francisco. Industries: Telecom, Banking, Wealth, Travel, Health, Finance.
- **Confidential partnerships — never name publicly:** Kloudspot (airports), mimik (edge AI), Airlinq (telco IoT). Use generic vertical framing.
- MWC Barcelona (2–5 March 2026) is in the past. Never pitch it as forward-looking.
- Signature lines: "Amplify human intelligence", "Sense, reason, and act", "Living cognitive system", "Grow the topline, not just protect the margin".

## 2. Universal rules — every format

### Legibility floor
Nothing essential renders below **15px on screen** or **11pt in print**. On slides, nothing essential renders below **22px**. Decorative labels are the only exception (and still have a floor, below).

| Format | Body default | Floor for anything readable | Labels / eyebrows |
|---|---|---|---|
| Deck (1920×1080) | **32px** | 22px | **24px** |
| Brochure (1440 wide) | **18px**; lede 20–22px | 15px | 13px |
| Word doc | **11pt / 17pt leading** (12pt for executive memos) | 11pt | 9pt mono labels |
| Graphic | **16px** card body; **18px** lede | 15px | 13px |
| Dashboard | **16px** content | 14px (UI chrome only) | 14px |

**When type overflows, widen the well or cut words. Shrinking type is never the fix.** Headlines fit on two lines or the copy gets shorter.

### Density
- Body paragraphs run **at most three lines** at rendered width (roughly 45–60 words).
- **Three or more parallel facts become bullets**, not one running sentence.

### Visual coverage
- **Every section carries at least one visual** — a line icon, diagram, UI card, KPI band, or pull-quote block. In Word docs, every two facing pages. No section stands on text alone.
- The bundled **29-icon LineIcons library** (`assets/graphics/line-icons/`, index in `skills/graphic/references/line-icons-library.md`) is the first reach in every format. Reference icons by name (`@icon:Name`, see §6) — never redraw an icon the library already has, never recolor one.
- A graphic must explain the headline. If you can remove it and lose nothing, it was decoration. Charts show real numbers or are clearly marked as placeholders.

### Layout
- Stack content with **flex or grid and gaps**, never absolute offsets. Absolute positioning is for corner chrome only (logo, section label, footer). Every text block owns its own space; if two blocks touch, the copy is too long for the layout.
- **White-first canvas** (`#FFFFFF`, alternate `#F8FAFA`). Saturated teal is a deliberate accent block (KPI band, outcome commitment, hero second word, divider), never the default surface.
- **One accent family** — the teal stack. Solid fills. **No gradients, no drop shadows, no accent line under titles, no centered body copy.** Everything left-aligned except deliberate quote/KPI layouts.
- Tile and card eyebrows in a row all use the **same `--teal`** — never step through the teal stack across tiles.

### Typography — three families, three roles
| Role | Design intent | Web / Office fallback | Rules |
|---|---|---|---|
| Headers, hero, KPI numbers | Brut Grotesque | **Geist** → Inter (Arial in Word) | **Weight 400 only. Never bold, never italic.** Size carries weight; weight never does. Sentence case. |
| Body | GT America | **Inter** (Calibri in Word) | 400–500. Inline bold only for proper nouns / key terms. |
| Labels, eyebrows, data | IBM Plex Mono | IBM Plex Mono (Consolas in Word) | Uppercase. Never bold, never italic. **Never letter-spaced in PPTX.** |

- Negative letter-spacing only on headers above ~22px.
- **Two-tone hero:** first word(s) in ink, last word(s) in `--logo-dark #035657` (on dark surfaces `--teal-on-dark #88DCE0`). Same font and size; only color changes. No italic, no underline, no brackets.
- Slide/section titles do not end in a period (deck closing slide excepted).

### Logo
- Always the shipped SVG (`assets/graphics/logos/`) at its native ratio — never stretched, recolored, or rebuilt from CSS quarter-circles. Light variant on light surfaces, dark variant on dark.
- Insert with `<!-- @logo:logo-light -->` etc. (§6) instead of pasting SVG paths.
- Placement is format-specific (deck: wordmark top-left on the cover only, icon-only 72×60 top-right everywhere else; brochure: wordmark in the topbar).

## 3. Voice

### Brand vocabulary — applied automatically
These are terminology, not editorial judgment. Apply them in every piece, including customer-supplied copy.

| Use | Instead of |
|---|---|
| **Pulse** (define on first customer-facing use: "a live, role-scoped operating view assembled from widgets") | dashboard |
| Cognitive agents | AI bots, chatbots, virtual assistants |
| Orchestration | automation |
| Knowledge fabric, enterprise knowledge graph | data layer, data warehouse, data lake |
| Sense, reason, and act | detect, process, respond |
| Self-evolving | self-learning |
| Amplify human intelligence | replace humans |
| AI transformation partner | vendor, provider, supplier |
| Enterprise General Intelligence (EGI), Enterprise Operating Platform (EOP) | generic AI platform |
| Mira (telecom only) | Echo |

"Dashboard" may appear only as the antagonist concept being replaced.

### AI writing tells
When **you write original copy**, avoid all of these. When the copy **came from the user or a source document**, flag them and propose fixes; never rewrite silently (see "Editing someone else's words").

- "**isn't X. It's Y.**" negation pivots, including soft versions ("aren't waiting…", "the gap isn't X — it's Y"). Most-flagged pattern.
- "**X, not Y**" inline contrasts, and "**[Subject] doesn't need X — it needs Y**" pivots.
- **Rhetorical triplets** — three parallel items or sentences used for rhythm ("Fast. Reliable. Scalable."). A *factual* list of three things is fine, set as bullets.
- **Staccato fragments** — join with commas, em dashes, or conjunctions.
- **Department roll calls** — "Customer service runs X. Network ops has Y. Billing has Z."
- **Comfort words** — compounding, fundamentally different, impactful, collectively unintelligent, leverage, synergy, disrupt, seamless, end-to-end, solutions (when vague).
- **Neat parallel opposition** — "scaling costs without scaling returns".

The fix is almost always: state what is true and stop.

### Editing someone else's words
Customer decks, source docs, and teammate drafts are their authors' words. Two passes:

1. **Automatic:** the brand-vocabulary table above (dashboard → Pulse, chatbot → cognitive agent, automation → orchestration…). Note what you swapped.
2. **Proposed, then approved:** everything editorial — triplet-breaking, negation-pivot removal, comfort-word stripping, sentence joining, restructuring, shortening. Show a numbered change list ("Applied: … / Suggest: …") and wait for the user to pick *apply all / apply selected / keep source wording*. **Default is to keep the source wording.**

Exception: a hard layout constraint (a cover title that cannot fit in two lines at the floor) — propose the shorter version; don't shrink the type.

## 4. Content preservation

Redesigning or converting someone's material is brand application, not editorial.

- **Never trim content to fit a pattern.** If the source has N items, find a layout that holds N or split it across sections/slides. Slide and section count are flexible; content is not.
- Keep every source slide/section and every named item unless it is true chrome (blank divider, "thank you" placeholder, navigational filler).
- **Audit before drafting.** For each source slide/section, list every named axis, column, list, callout, and sub-tagline, and confirm where each lands in the new outline (`S04 — Problems (4), Products (4), Value (9) → new 04, 05, 06 ✓`). Any gap: split, re-pattern, or ask the user before drafting.
- Length targets (e.g. "15–25 slides") cap bloat; they are not a floor to compress toward. If the source is far longer, ask before compressing.

## 5. Design tokens

### Teal stack
| Token | Hex | Use |
|---|---|---|
| `--teal-dark` | `#004D50` | Deep emphasis, KPI bands, dark surfaces |
| `--teal` | `#006B6F` | Primary brand; eyebrows, links, light-surface accents, strokes, dots |
| `--teal-on-dark` | `#88DCE0` | Accents, strokes, labels, and hero word on `--teal-dark` |
| `--teal-light` | `#E8F4F5` | Tinted callouts, table headers (decoration, never essential text) |
| `--logo-dark` | `#035657` | Hero second word on light surfaces; default chart series |
| `--logo-light` | `#67A4A4` | Secondary chart series |
| ~~`--teal-accent`~~ | `#00989E` | **Retired** for text, strokes, labels, accents (low contrast). Legacy alias only. |
| ~~`--teal-bright`~~ | `#00C4CC` | **Retired.** Do not use. |

**Contrast floor:** accent text, strokes, labels, KPI numbers, and the hero word must read at a distance — `--teal`/`--logo-dark` on white, `--teal-on-dark` on `--teal-dark`. Light tints and `#999999` are for decoration and deliberately inert elements only. A CSS-variable swap does not reach hex hardcoded inside inline SVG — `check.py` greps for it.

### Neutrals and status
- Ink `#1A1A1A` (web), `#0A0A0A` (dashboard), `#111111` (docx). `--ink-2 #404040`, `--ink-3 #666666`, `--ink-4 #999999`, `--line #ECECEC`, `--bg-solid #F8FAFA`, `--card-grey #F4F4F4`.
- Status — **state only, never decoration**: success `#00896A`, warn `#C48800`, danger `#D94A30`.
- Forbidden hues: mint `#A9E0DF`, accent blue `#80A3F8`, indigo, violet, coral as decoration, any second accent.

## 6. Build and verify — the shared toolchain

Scripts live in the plugin's `scripts/` folder (paths below are relative to the plugin root; skills reference them as `../../scripts/…`). Requirements, once per machine: `pip install playwright pillow python-pptx python-docx && python3 -m playwright install chromium`.

**Author a small source file, let the script assemble it.** Write `name.src.html` with placeholders instead of pasting assets:

| Placeholder | Becomes |
|---|---|
| `<!-- @fonts -->` | Google Fonts links for Geist, Inter, IBM Plex Mono |
| `/* @tokens:deck */`, `/* @tokens:brochure */` (inside `<style>`) | that skill's `assets/tokens.css` |
| `<!-- @logo:logo-light width="155" height="36" class="logo-tl" -->` | inline SVG (`logo-light`, `logo-dark`, `icon-light`, `icon-dark`, `dashboard-icon`) |
| `src="@icon:Nodes"` / `url('@icon:Nodes')` | the line icon as an embedded data URI |
| `@asset:graphics/…` | any file under plugin `assets/` as a data URI |

```
python3 scripts/build_html.py name.src.html          # → name.html, self-contained
python3 scripts/check.py name.html --kind deck --sheet name.sheet.png
```

**Edit `name.src.html` with targeted edits, then rebuild.** Don't rewrite the whole file to change one slide or section, and don't Read the built `name.html` (it carries embedded assets).

**Verify with `check.py`, not screenshots.** It reports, as text: type below the floors in §2, paragraphs over three lines, clipped/overflowing text, text overlapping text, absolutely positioned text, sections or slides with no visual, retired colors, gradients/shadows/italics, off-stack fonts, and voice flags (flags only — never auto-fixed). Fix every ERROR; judge each WARN. Then **Read the one contact sheet once** (≤1600px wide; units with errors are outlined red). Zoom only into a flagged unit with `--zoom N`.

**Image budget.** Never Read a PNG larger than ~2000px on its long edge — it breaks the session's image budget. Final 2× renders (decks, graphics) are for delivery, not for looking at; `scripts/render.py` writes a `.preview.png` for that.

## 7. Before you deliver — every format

- [ ] Brand vocabulary applied; AI tells avoided in your copy and *flagged, not silently fixed* in source copy
- [ ] Nothing essential below the floor (§2 table); no type shrunk to fit
- [ ] No paragraph over three lines; parallel facts of three or more are bullets
- [ ] Every section (every two facing pages in a doc) carries a visual; library icons used first
- [ ] Teal stack only, solid fills, no gradients/shadows/italics/bold heroes; retired hexes absent
- [ ] Real logo SVG at native ratio, correct light/dark variant
- [ ] Source content preserved; any cut was approved by the user
- [ ] `check.py` reports zero ERRORs
