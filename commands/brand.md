---
description: Start a Metafore-branded artifact (brochure, dashboard, deck, doc, or graphic) with brand rules pre-loaded
argument-hint: [artifact-type] [what to build]
---

You are the entry point for the Metafore brand-tools suite. The user invoked `/metafore:brand` with arguments: "$ARGUMENTS"

## Step 1 — Load the brand rules first

Before anything else, Read the shared brand pack so whatever you produce stays on-brand:

- `${CLAUDE_PLUGIN_ROOT}/assets/brand/metafore_brand.md` — voice rules, AI-tell blocklist, design tokens, three-font type stack, Pulse vocabulary

If the request turns out to be a deck, also skim the deck-specific calibrations in `${CLAUDE_PLUGIN_ROOT}/assets/brand/feedback_*.md`.

## Step 2 — Figure out which artifact to build

The suite produces five artifact types, each backed by a skill:

| Artifact | Skill | Use for |
|---|---|---|
| Brochure | `metafore:brochure` | Customer-facing HTML brochures, one-pagers, sales sheets |
| Dashboard | `metafore:dashboard` | Internal HTML dashboards, admin / operator UIs |
| Deck | `metafore:deck` | Slide decks (HTML draft → editable PPTX) |
| Doc | `metafore:doc` | Branded Word docs (white papers, proposals, SOWs, memos) |
| Graphic | `metafore:graphic` | Blog heroes, OG/social images, feature cards, line icons |

Decide based on the arguments:

- **Type named explicitly** (e.g. "brochure", "deck about Pulse") → proceed with that skill.
- **Content described but no type** (e.g. "something for a logistics CIO about Pulse") → infer the best-fit type, state your choice in one line, and proceed (the user can redirect).
- **No arguments** → show the table above and ask: which artifact, and what should it cover?

## Step 3 — Hand off to the matching skill

Once the type is settled, invoke the corresponding `metafore:*` skill and build the artifact according to that skill's rules, applying the brand pack you loaded in Step 1. Do not re-implement the skill's logic here — defer to it.
