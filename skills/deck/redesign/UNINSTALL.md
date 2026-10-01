# Uninstall — remove the redesign sub-workflow

1. Delete this folder: `skills/deck/redesign/`.
2. In `skills/deck/SKILL.md`, delete workflow step **0** ("Redesigning an existing deck?…").

Nothing else references this folder; the from-scratch deck workflow, patterns, tokens, and PPTX builder are unaffected. Verify with `grep -rn "redesign/" skills/deck/` (no results).
