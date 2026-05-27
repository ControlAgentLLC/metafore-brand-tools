---
name: brochure
description: Build Metafore-branded marketing brochures, product overviews, one-pagers, and multi-section sales collateral as self-contained HTML files. Use this skill whenever a Metafore teammate asks for a brochure, product overview, sales sheet, marketing one-pager, customer-facing PDF, "Metafore-ify this doc", or wants to turn a markdown product spec/BRD/feature doc into branded marketing HTML — even if they don't say "brochure" explicitly (e.g. "make this look like Metafore", "marketing version of this", "external-facing version", "give this the Metafore treatment"). Encodes Metafore's brand invariants — two-tone hero, teal-only accent palette, three-font type stack, voice rules, AI-tell blocklist, "Pulse" vocabulary — and explicitly leaves layout content-determined rather than template-fixed. Do NOT trigger for internal dashboards (use `metafore:dashboard`), DOCX documents, or PPTX decks.
---

# Metafore Brochure Builder

You are helping a Metafore teammate produce a brand-compliant customer-facing brochure. The deliverable is a single self-contained `.html` file (no build step, fonts loaded from Google Fonts CDN) that opens directly in a browser and prints cleanly to PDF.

## Brand reference (read before producing)

Every Metafore artifact follows the same brand invariants. Before drafting, Read the shared brand pack at `../../assets/brand/metafore_brand.md` (voice rules, AI-tell blocklist, design tokens, type stack) and skim any relevant `../../assets/brand/feedback_*.md` files (pattern overrides and calibrations). These supersede anything older you may have seen.

## The core idea — content determines structure

There is **no fixed section template**. Two brochures should not look interchangeable. Read the input content first, then choose section patterns that fit the shape of what you're presenting. A product overview with four parallel capabilities wants a different layout than a customer story with one quantified outcome, which wants a different layout than a head-to-head differentiation piece. Let the content tell you what it needs.

What stays constant across every brochure is the **brand surface** — type, color, voice, vocabulary, the two-tone hero, the footer. Those invariants are non-negotiable. Everything between the hero and the footer is yours to compose.

## The two invariants that bookend every brochure

1. **Open with a two-tone hero.** Always. Big `h1`, weight 400, no italic, no bold. First word(s) in `var(--ink)` (`#1A1A1A`), final word in `var(--logo-dark)` (`#035657`), wrapped in `<span class="accent">…</span>`. The contrast carries the brand at a glance.
2. **Close with the Metafore footer.** Top hairline (`1px solid var(--line)`), 28px vertical padding, two columns: left side reads `Powered by Metafore — AI-Native Transformation Platform` in IBM Plex Mono uppercase tracked; right side is `© 2026 Metafore · [Document name] · Confidential` in lighter Plex Mono.

Anything that doesn't open with the hero and close with the footer is not a Metafore brochure. Everything between those two anchors is content-driven.

## Design tokens — copy verbatim

The full token set lives in `assets/tokens.css`. Inline it into every brochure's `<style>` block. Token values:

```css
--bg: #FFFFFF;          --bg-solid: #F8FAFA;
--ink: #1A1A1A;         --ink-2: #404040;     --ink-3: #666666;     --ink-4: #999999;
--line: #ECECEC;        --panel: #FFFFFF;     --panel-hi: #FAFBFB;
--teal-dark: #004D50;   --teal: #006B6F;      --teal-accent: #00989E;
--teal-bright: #00C4CC; --teal-light: #E8F4F5;
--logo-dark: #035657;   --logo-light: #67A4A4;
--success: #00896A;     --warn: #C48800;      --danger: #D94A30;
--header: 'Geist', 'Inter', sans-serif;
--body: 'Inter', sans-serif;
--mono: 'IBM Plex Mono', monospace;
```

**Single accent family.** The teal stack is the only accent. Do not introduce a second hue — no mint, no accent blue, no warm tone. Status colors exist for state (a danger badge, a success indicator), never for decoration.

**White-first canvas.** Default background `#FFFFFF`. Alternate sections with `#F8FAFA` for vertical rhythm. Saturated teal (`#004D50` / `#006B6F`) only appears as a deliberate accent block — a KPI band, an outcome commitment, the hero's second word.

## Logo

Inline the Metafore logo SVG from `../../assets/graphics/logos/logo-light.svg` (shared across all skills in this plugin) in the topbar of every brochure. It's a 155×36 viewBox mark. Don't substitute, don't resize the viewBox, don't recolor — the SVG carries the brand colors itself.

## Typography — three fonts, three roles

| Role | Font | Notes |
|---|---|---|
| Headers, decorative numbers, hero | `var(--header)` (Geist → Inter fallback; Brut Grotesque is the design intent) | **Weight 400 only.** Never bold. Never italic. Size carries weight, not weight. |
| Body, lede, card body | `var(--body)` (Inter) | Weight 400–500. |
| Labels, eyebrows, KPI captions, mono callouts | `var(--mono)` (IBM Plex Mono) | Uppercase. No tracking. |

### Type scale — Perfect Fifth default, Perfect Fourth floor

Every Metafore artifact uses the same scale, line-heights, and zero tracking. The token values are in `assets/tokens.css`. The rules are:

| Role | Default | Floor | Line-height | Tracking |
|---|---|---|---|---|
| H1 | 36px | 28px | 1.125 | 0 |
| H2 | 24px | 21px | 1.125 | 0 |
| H3 | 18px | — | 1.125 | 0 |
| Body | 16px | **never shrinks** | 1.200 | 0 |
| Lede | 18px | **never shrinks** | 1.200 | 0 |
| Eyebrow | 11px Plex Mono | — | 1.200 | 0 |

**Auto-shrink ladder.** Headers (H1, H2) may render anywhere between their default and floor depending on container width and copy length — this is built into `tokens.css` via `clamp()` + container queries. Headers must fit on **max 2 lines**. If a header would wrap to 3+ lines at the default, it shrinks toward the Perfect Fourth floor. If it still doesn't fit at the floor, the container's `max-width` enforces a 2-line cap — at that point the copy must be revised.

**Body, lede, and eyebrow never participate in the shrink ladder.** Their sizes are fixed; readability of paragraphs is not sacrificed to fit a long headline.

**Margins are proportional to each element's own size.** When a header shrinks, its margins shrink with it — this guarantees H1, H2, and body never overlap regardless of where on the ladder the header lands. Do not hand-tune margins; trust the `tokens.css` rules.

**Letter-spacing is 0 everywhere.** No negative tracking on headlines, no positive tracking on eyebrows. This supersedes any older guidance you may have seen.

## What never appears

- Gradients on text, backgrounds, or borders
- Drop shadows on cards
- Italic anywhere (especially headers)
- Bold hero text
- Underlined or accent-bar-decorated section titles (an underline below an `h2` is an AI tell — skip it)
- Centered body copy (left-align everything)
- A second accent color outside the teal stack

## Voice — preferred vocabulary

These are not stylistic preferences; they are the Metafore positioning. Use them.

| Use | Not |
|---|---|
| **Pulse** (define on first use as "a live, role-scoped operating view assembled from widgets") | dashboard |
| Cognitive agents | AI bots, chatbots, virtual assistants |
| Orchestration | automation |
| Knowledge fabric, enterprise knowledge graph | data layer, data warehouse |
| Sense, reason, and act | detect, process, respond |
| Self-evolving | self-learning |
| Amplify human intelligence | replace humans |
| AI transformation partner | vendor, provider, supplier |
| **Metafore** (the brand name in customer-facing copy) | Metafore One (use only when the platform-product distinction matters) |

**Confidentiality.** Never name Kloudspot, mimik, or Airlinq as partners. Use generic vertical framing (airports, edge AI, telco IoT) without identifying the partner.

## AI-tell blocklist — patterns the human eye catches immediately

Marketing copy that follows these patterns reads as machine-written. Avoid them. The reason matters: each pattern is what AI writers reach for because it sounds rhythmic, but at scale humans recognize it and tune out.

- **No "X isn't Y. It's Z." negation pivots.** The single most-flagged pattern. Includes softer variants ("aren't waiting…", "The gap isn't X — it's Y"). Rewrite as a positive assertion of what is.
- **No "X, not Y" inline contrasts.** Same family. State the thing directly.
- **No "[Subject] doesn't need X — it needs Y" pivots.** Same family.
- **No triplet structural lists** — three parallel items or three parallel sentences used as a recurring device. Use 2 items or 4. A grocery list of three nouns is fine; a rhetorical triplet pattern is not.
- **No short staccato fragment sentences.** Two-word sentences strung together are an AI tic. Join with commas, em dashes, or conjunctions.
- **No department roll calls.** "Customer service runs X. Network ops has Y. Billing has Z." reads as filler.
- **No comfort words.** Compounding, fundamentally different, impactful, collectively unintelligent, leverage, synergy, disrupt, seamless (overuse), end-to-end, solutions (when vague).
- **No neat parallel opposition.** "Scaling costs without scaling returns" — too rhythmic, reads as constructed.

When you catch yourself reaching for one of these, the fix is usually to state what's actually true and stop trying to be rhetorical about it.

## How content drives structure

Read the input content end to end before you decide what to build. Then for each major content theme, pick the section pattern that fits its shape:

| Content shape | Section pattern |
|---|---|
| 3+ parallel items presented at equal weight | Grid (2×2, 3-up, or 4-up cards) |
| Numbered or sequential progression (step 1 → step 2 → step 3) | Process timeline / numbered steps |
| Quantified outcomes worth headlining | KPI band on `--teal-dark`, 3 or 4 cells |
| Head-to-head differentiation against an alternative | Comparison table |
| Big singular commitment or thesis statement | Outcome band on `--teal`, white text |
| Customer voice or third-party validation | Quote pull |
| One primary thing + one supporting artifact | Hero with side UI-card |
| A few thematic pillars introducing the rest of the doc | 3-up pillar cards with accent rotation |
| Operational mechanics the reader will skim | Callout strip (eyebrow + body cells) |

Do not pre-commit to a section count. A short product story may need three sections between hero and footer; a dense product overview may need six. **One-pagers (~1880px tall) vs multi-section brochures (~3000–3600px tall) is a content-volume decision, not a template decision.**

A draft pattern library with HTML snippets lives at `references/pattern-library-DRAFT.md` — it is not loaded by default and may be referenced for examples, but treat it as a working draft, not a definitive catalog. If a section pattern you need is not in the draft, compose it from the design tokens directly.

## Page mechanics

- Page width: `1440px`, centered.
- Section padding: `88px 96px` (vertical breathing matters more than horizontal — these brochures look airless if you tighten this).
- Card border radius: `6px` for content cards; `999px` for pills/badges; `14px` only for inline UI-card mockups (preserving the dashboard treatment).
- Card borders: `1px solid var(--line)`. No drop shadows.
- Card gap inside grids: `18px` to `20px`.
- Usable content width inside sections: ~1248px.

## Print/PDF safety

Every brochure must include this in `<style>`:

```css
@page { size: 1440px auto; margin: 0; }
@media print {
  html, body { background: var(--bg) !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .page { box-shadow: none !important; }
}
```

Without this, the saturated teal bands (KPI bands, outcome bands) come out as light gray in PDF exports.

## Output format

- Single self-contained `.html` file. No external CSS, no JS framework, no build step.
- Fonts via the Google Fonts CDN link block in `<head>`.
- Save to the user's current working directory unless they specify otherwise.
- Filename pattern: `metafore-<topic>-<audience-or-format>.html`. Examples: `metafore-maker-brochure.html`, `metafore-supply-chain-brief.html`, `metafore-focus-ceo-onepager.html`.

After writing, tell the user the file is visible in the Launch preview panel (this is a hook-injected message — surface it; don't suppress it).

## Anti-patterns to skip

- Don't trigger on requests for internal dashboards, operator consoles, or admin UIs (`metafore:dashboard` owns those).
- Don't trigger on DOCX deliverables, slide decks, or PPTX (each has its own ruleset in the brand memory).
- Don't trigger on generic non-Metafore marketing work.
- Don't recreate the structure of an existing brochure unless the user explicitly asks for it. Two brochures looking interchangeable is a failure mode, not a goal.
- Don't add a section just because a pattern exists. If the content does not call for a KPI band, do not invent one.
