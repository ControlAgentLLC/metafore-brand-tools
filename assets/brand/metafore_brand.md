---
name: Metafore brand system
description: Canonical Metafore voice, AI-tell blocklist, design tokens, and layout blueprints for brochures, dashboards, decks, and docs
type: reference
originSessionId: e6765f71-516d-4239-b31f-ac8cc956509f
---
# Canonical positioning
- **Metafore** = AI-Native transformation platform for enterprise. Product is **Metafore One**. Second product: **Mira** (personal AI twin for mobile subscribers, deployed in carrier IMS — renamed from Echo 2026-04-24).
- Differentiator: AI transformation **partner** (not vendor). Looks for topline growth, not just margin/cost reduction.
- CEO: Ori Sasson. HQ: San Francisco. Industries: Telecom, Banking, Wealth, Travel, Health, Finance.
- CONFIDENTIAL partnerships (do NOT name publicly): Kloudspot (airports), mimik (edge AI), Airlinq (telco IoT). Use generic vertical framing.
- MWC Barcelona March 2-5 2026 is in the past — never pitch as forward-looking.

# Voice — preferred vocab
- Cognitive agents (not AI bots/chatbots/virtual assistants)
- Orchestration (not automation)
- Knowledge fabric, enterprise knowledge graph (not data layer/warehouse)
- Self-evolving (not self-learning)
- Sense, reason, and act (not detect/process/respond)
- Cognitive system, Enterprise General Intelligence (EGI), Enterprise Operating Platform (EOP)
- Amplify human intelligence (not replace humans)
- AI transformation partner (not vendor/provider/supplier)
- **Pulse** = Metafore's term for what others call a dashboard. NEVER use "dashboard" — always "Pulse". A Pulse is a live, role-scoped operating view assembled from Bricks widgets. Define on first use in customer-facing copy. Confirmed 2026-05-15.
- Signature lines: "Amplify Human Intelligence", "Sense, reason, and act", "Living cognitive system", "Grow the topline, not just protect the margin"

# AI WRITING TELLS — ZERO TOLERANCE (Elana's flagged list)
- **NO "isn't X. It's Y."** negation-pivot. Includes softer versions ("aren't waiting…", "The gap isn't X — it's Y"). Most-flagged pattern.
- **NO "X, not Y"** inline contrasts
- **NO "[Subject] doesn't need X — it needs Y"** pivots
- **NO short staccato fragment sentences** — join with commas, em dashes, conjunctions
- **NO triplet structural lists** — three parallel items/sentences as recurring device. Use 2 or 4 instead.
- **NO department roll calls** — "Customer service runs X. Network ops has Y. Billing has Z."
- **NO "compounding" / "fundamentally different" / "impactful" / "collectively unintelligent"** — AI comfort words
- **NO neat parallel opposition** — "scaling costs without scaling returns"
- **NO leverage, synergy, disrupt, seamless (overuse), end-to-end, solutions (vague)**

# Design system — white-first, single-accent teal
- **No dark-first mode.** Default bg `#FFFFFF`. Alternating `#F8FAFA` (`bgSolid`) for vertical rhythm. Saturated teal only as deliberate accent block (KPI band, outcome commitment, hero second word).
- **One accent family.** Teal stack only. No mint `#A9E0DF`, no accent blue `#80A3F8`, no second hue.
- **No gradients. No drop shadows on cards. No accent line under titles** (AI tell). **No centered body copy. No italic headers. No bold hero text.**

## Teal stack
| Token | Hex | Use |
|---|---|---|
| tealDark | #004D50 | Deep emphasis, KPI band bg |
| teal | #006B6F | Primary brand, active, links, **light-surface accents, strokes & dots** |
| tealOnDark | #88DCE0 | **Accents, strokes, labels & two-tone-hero second word on `tealDark` surfaces** |
| tealLight | #E8F4F5 | Tinted callouts, table headers |
| logoDark | #035657 | Hero second-word on light surfaces, default chart series |
| logoLight | #67A4A4 | Secondary chart series |
| tealAccent | #00989E | **Legacy — not for text, strokes, or accents.** Low contrast on both white and `tealDark`. Use `teal #006B6F` on light, `tealOnDark #88DCE0` on dark. Decorative/gradient mid-stop only. |
| tealBright | #00C4CC | **Retired** — too cyan. Do not use. |

**Contrast floor (legibility).** Essential elements — accent text, strokes, labels, KPI numbers, two-tone-hero second word — must read at a distance. On white use `teal #006B6F` (or `logoDark #035657` for hero text); on `tealDark` use `tealOnDark #88DCE0`. Never `#00989E`/`#00C4CC` for these. Light tints (`tealLight`, `textFaint #999999`) are for decoration and muted/inert elements only, never for text the reader must parse.

## Text
- text/ink `#1A1A1A` (brochure) or `#0A0A0A` (dashboard); body color in docx `#111111`
- textMid `#404040`, textDim `#666666`, textFaint `#999999`

## Status (state only, never decoration)
- success #00896A, warn #C48800, danger #D94A30

## Typography — three families, three roles
- Headers: **Brut Grotesque** → web fallback `'Geist', 'Inter'`
- Body: **GT America** → fallback `'Inter'`
- Labels/Mono: **IBM Plex Mono** (Google Fonts)
- Hero is always weight 400, never bold, never italic. Size carries weight.
- Negative letter-spacing only above ~22px on header font.
- All-caps tracked labels = IBM Plex Mono only.
- Eyebrows get +1.0–1.6 tracking.
- Plex Mono NEVER bold and NEVER letter-spaced in PPTX (different rule).

## Signature: two-tone hero
- First word(s) inky black, **last word** in logoDark `#035657` (or tealDark `#004D50`). No italic, no underline. Most distinctive type moment.

## Brochure layout blueprint (1440px wide, ~3400-3600 tall)
1. Hero — white, 88/96 padding, top bar + headline + lede + stat split
2. Three transformation pillars — bgSolid, 3 equal 402px cards, accent rotation teal/tealAccent/tealDark
3. What [Product] Delivers — white, capability table + KPI band (tealDark bg, 4 cells)
4. Why Metafore — bgSolid, 3 value-prop cards + outcome commitment band (teal fill, white text)
5. Footer — white, top hairline, small product logo + "Powered by METAFORE" + confidential line
- Usable width 1248px. Card gap 18-20px. Card radius 6px, pills 999px.

## Dashboard rules (when building HTML dashboards, not brochures)
- 64px icon sidebar, search in topbar left, "I want to…" composer at bottom (domain-specific prompts), 4-col card grid, 14px radius, 18px gap, no drop shadows. Toggle = white pill active (never black-fill). Charts use logo teals only.

## Doc (DOCX) rules
- US Letter, 1" margins, all left-aligned, body color `#111111`.
- Plex Mono eyebrow above every H1 (`01 - SUMMARY` format), H1 carries 1/2pt teal underline `#005354`.
- Two cover styles: light (white + two-tone hero) or dark (full-bleed teal + white/mint hero).
- Field Note callouts: tealLight `#E8F4F5` fill, Plex Mono "FIELD NOTE" header.

## Logo
- Two overlapping quarter-circles (large tealDark + small tealAccent) + wordmark in BLACK Brut Grotesque Medium 48px, tracking -1.4, 12px gap between mark and word.
- Dashboard inline SVG provided in setup (53x42 viewBox).
