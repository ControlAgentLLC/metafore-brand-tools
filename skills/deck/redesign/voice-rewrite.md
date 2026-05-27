# Voice rewrite — extracted copy → Metafore voice

Run **every** title, body paragraph, and bullet in `slide-manifest.json` through this checklist **before** drafting HTML. Source decks carry their own voice; if you ignore this step, the redesign will look Metafore but read like the customer's vendor.

This file does **not** redefine the rules — it lists the transformations to apply. The canonical rules live in `../SKILL.md` under "Voice — preferred vocabulary" and "AI writing tells — zero tolerance". Read those first if you haven't.

---

## Lexical replacements (find/replace pass)

| Source word                              | Metafore replacement                                     |
|------------------------------------------|----------------------------------------------------------|
| dashboard                                | Pulse (define on first use)                              |
| AI bot, chatbot, virtual assistant       | cognitive agent                                          |
| automation                               | orchestration                                            |
| data warehouse, data layer, data lake    | knowledge fabric / enterprise knowledge graph            |
| detect / process / respond               | sense / reason / act                                     |
| self-learning                            | self-evolving                                            |
| replace (humans / staff / agents)        | amplify (human intelligence)                             |
| vendor / provider / supplier             | AI transformation partner                                |
| AI platform (generic)                    | Enterprise Operating Platform (EOP)                      |
| Echo (legacy product name)               | Mira — and only on telecom decks                         |

If the source mentions MWC Barcelona March 2026 as a future event, rewrite as past tense. The event has happened.

---

## Structural transformations (rewrite pass)

These come from the "AI writing tells — zero tolerance" list. The text in extracted slides has usually been written by a human in a hurry, then "polished" by an LLM, which means the tells are almost always present. Strip them all.

1. **Kill "isn't X. It's Y." negation-pivots.** Replace with a direct positive claim.
   - Source: "It isn't another dashboard. It's a true operating view."
   - Metafore: "Pulse is the operating view your team works from."

2. **Kill "X, not Y." inline contrasts.** Same fix — make the positive claim, drop the contrast.

3. **Demote triplets to pairs (or promote to fours).** Three parallel bullets become two or four. This is the most common slide-level violation in source decks.
   - Source: "Fast. Reliable. Scalable."
   - Metafore: either pick the two that matter, or expand to four with substance.

4. **Strip AI comfort words.** Search-and-cut these in every line: *compounding, fundamentally different, impactful, leverage, synergy, disrupt, seamless, end-to-end, solutions*. If a sentence collapses without them, it was empty anyway.

5. **Break staccato fragments.** Source decks love three-fragment lines for "punch." Join with commas, em dashes, or conjunctions.
   - Source: "Faster decisions. Less waste. Happier customers."
   - Metafore: "Faster decisions, less waste, and a better customer experience." (or pick two and trim)

6. **No neat parallel opposition.** Phrases like "scaling costs without scaling returns" are reliably AI-tell. Rewrite directly.

7. **No department roll calls.** "Customer service runs X. Network ops has Y. Billing has Z." → one sentence naming the scope, not a list of departments.

---

## Slide-element-specific rules

**Cover headlines** — strict cap of 6 words. Two-tone hero (first word(s) in `--ink`, last word in `--logo-dark`). If the source cover headline is 8 words of feature soup, cut it to 6 of vision.

**Agenda items** — noun phrases, not verb phrases.
- Source: "We will discuss the platform" → Metafore: "The platform"
- Source: "Reviewing customer outcomes" → Metafore: "Customer outcomes"

**KPI labels** — 2 lines max under the number. Source labels are usually too long ("Increase in operational efficiency across regions"). Trim to "Operational efficiency."

**Capability tile labels** — ≤3 words. Source decks often have full sentences here. Cut to a noun phrase.

**Statement slides** — one sentence, ≤14 words. Source statement slides are usually a paragraph; the redesign keeps the sentence the customer would have ended on.

**Closing CTAs** — one CTA, one verb. Source closings often have three CTAs (book a demo, read the case study, follow us). Pick one.

---

## Vertical-specific guardrails

- **Telecom decks**: Mira naming is allowed and encouraged for the personal-agent product. Do not use Mira on banking, wealth, travel, health, or supply chain decks — strip any Mira references the source picks up from cross-vertical material.
- **Banking / wealth**: extra care on compliance phrasing — never claim "automated decisions" where the source said "automated insights"; the legal distinction matters.
- **Supply chain**: "exception" is the preferred term over "alert" or "issue."

---

## Quick checklist (run after rewrite)

Before declaring rewrite done, every slide passes:

- [ ] Zero instances of "dashboard" — all replaced with Pulse
- [ ] Zero negation-pivots ("isn't X, it's Y")
- [ ] Zero triplet bullet lists (everything is 2, 4, or more)
- [ ] Zero AI comfort words (`leverage`, `seamless`, `end-to-end`, etc.)
- [ ] Cover headline ≤6 words
- [ ] Agenda items are noun phrases
- [ ] Statement slides are one sentence ≤14 words
- [ ] One CTA on closing, not multiple
- [ ] No future-tense references to MWC Barcelona March 2026
- [ ] Correct vertical-specific naming (Mira only on telecom)

If any of these fail, the rewrite isn't done — don't hand off to HTML drafting yet.
