---
name: Capability-grid tile eyebrows — single color, not stepped
description: On P-06 / P-07 capability-grid tiles, every tile's eyebrow uses --teal. Do not step through the teal stack across tiles.
type: feedback
originSessionId: f3b1bf3c-f294-4748-a10f-ad3aa8f6bb09
---
On capability-grid patterns (P-06 4-up, P-07 8-up, and by extension P-08 module grid), every tile's eyebrow text uses the same color: `--teal` (#006B6F).

**Why:** Visual consistency across tiles reads cleaner than a subtle color rhythm. The stepped teal rhythm called for in the current `references/pattern-library.md` for P-06 ("each card's eyebrow color steps through the teal stack") was tested on the May 2026 telecom corp deck redesign and rejected — the differentiation reads as inconsistency, not subtlety. Single-color eyebrows let the tile content carry the rhythm.

**How to apply:** When authoring or modifying any tile-grid slide (P-06/P-07/P-08), set every tile's eyebrow (`.t-num` / `.c-num`) to `--teal`. Do not add per-tile overrides like `.tile.t2 .t-num { color: var(--teal-accent); }`. This applies to both new decks and any redesign of existing decks.

The canonical `pattern-library.md` in the `deck` skill still documents the stepped rhythm — if you're modifying the skill itself, update P-06's "Type" section to match this rule.
