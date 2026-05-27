---
name: When redesigning a deck, preserve source content
description: Default to keeping every source slide and every bullet within those slides. Only cut true chrome. Aggressive content compression was wrong.
type: feedback
originSessionId: f3b1bf3c-f294-4748-a10f-ad3aa8f6bb09
---
When redesigning an existing deck, default to **preserving the source content** — every slide, every bullet, every named item. Do not collapse, merge, or trim unless the source slide is true chrome (a blank section divider, a "thank you" placeholder with no content, a duplicate page-break slide that adds nothing).

**Why:** On the May 2026 telecom corp deck redesign, I cut 3 of 18 source slides (Leadership, Solutions, Functional Architecture overview) under the "merge weak singles / cut duplicates" guidance from `skills/deck/redesign/source-mapping.md`. Each of those slides existed in the source for a reason — the redesign should not be the moment that judgment gets second-guessed. The customer's deck is the customer's content; the redesign's job is brand application, not editorial.

I also dropped a 5th use case ("Workforce & Skills") to fit a 4-up grid, and trimmed Mira from 6 capabilities to 4 for the same reason. Both were wrong. Use a different pattern that fits the source count instead of cutting items to fit the pattern.

**How to apply:**

1. Treat each source slide as load-bearing unless you can articulate a non-aesthetic reason to cut it (e.g., truly blank chrome slide). "Overlaps with another slide" is not a reason to cut — slides exist at different angles.
2. When the source has N items (5 use cases, 6 solutions, 9 industries), find a pattern that accommodates N — don't trim N to fit the pattern's default count.
3. The existing source-mapping rules around content collapsing apply only when the source deck is meaningfully longer than the Metafore target (30+ slides). For source decks in the 15–25 range, preserve 1:1.
4. If you're tempted to merge or cut, ask first. Do not assume editorial authority over the source.

The Metafore length target ("15–25 slides") is a *cap* on bloat, not a *floor* to hit. A faithful 18-slide redesign is better than an 18→16 compressed redesign.
