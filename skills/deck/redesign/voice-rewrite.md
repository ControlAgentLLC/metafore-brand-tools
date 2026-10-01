# Voice pass — extracted copy → Metafore voice

The customer's deck is the customer's words. Run this pass over every title, body, and bullet in `slide-manifest.json` **before** drafting HTML, in two parts. The canonical rules live in `../../../assets/brand/metafore_brand.md` §3.

## Part 1 — automatic: brand vocabulary

Terminology, not editorial judgment. Apply silently, but list what changed in the summary you show the user.

| Source term | Metafore term |
|---|---|
| dashboard | Pulse (define on first use) |
| AI bot, chatbot, virtual assistant | cognitive agent |
| automation | orchestration |
| data warehouse, data layer, data lake | knowledge fabric / enterprise knowledge graph |
| detect / process / respond | sense / reason / act |
| self-learning | self-evolving |
| replace (humans / staff) | amplify (human intelligence) |
| vendor / provider / supplier (describing Metafore) | AI transformation partner |
| AI platform (generic) | Enterprise Operating Platform (EOP) |
| Echo (legacy product name) | Mira — telecom decks only |

Also automatic: Mira references removed from non-telecom decks; MWC Barcelona March 2026 written as past; confidential partner names (Kloudspot, mimik, Airlinq) replaced with generic vertical framing.

## Part 2 — proposed, then approved: everything editorial

**Default: keep the source wording.** Flag candidates and show one numbered list before drafting:

```
Voice pass · 6 items · 2 applied · 4 awaiting you
✓ Applied  S03  dashboard → Pulse (first use defined)
✓ Applied  S07  chatbot → cognitive agent
? S02  "It isn't another dashboard. It's a true operating view." — negation pivot.
       Suggest: "Pulse is the operating view your team works from."
? S05  "Fast. Reliable. Scalable." — rhetorical triplet of fragments. Suggest: "Fast and reliable at enterprise scale."
? S09  Department roll call across three sentences. Suggest one sentence naming the scope.
? S11  Comfort words: leverage, end-to-end, disrupt. Suggest a plain restatement.
Apply all · apply selected (list numbers) · keep source wording
```

What to flag (from the brand pack's AI-tell list): negation pivots and "X, not Y"; rhetorical triplets (a factual list of three stays — set it as bullets); staccato fragments; comfort words; neat parallel opposition; department roll calls.

## Layout-driven suggestions (also proposed, never silent)

Slides are sparse, so some source copy won't fit a pattern at the type floors. Propose the shorter version; never shrink type and never drop items:
- Cover headline over 6 words → suggest the product/brand name as the hero and move the description to the subtitle.
- Paragraphs over three lines → suggest bullets (three or more parallel facts) or a split.
- KPI labels over two lines, tile labels over ~3 words → suggest a trimmed label.
- Agenda verb phrases → suggest noun phrases ("Reviewing customer outcomes" → "Customer outcomes").
- Several closing CTAs → ask which one to keep.

## Vertical guardrails

- **Banking / wealth:** never turn "automated insights" into "automated decisions" — the legal distinction matters.
- **Supply chain:** "exception" is preferred over "alert" or "issue" — propose, don't force.

## Done when

- [ ] Every Part 1 swap applied and listed
- [ ] Part 2 list shown and the user's choice applied (or source wording kept)
- [ ] No source item dropped; layout-driven cuts approved
