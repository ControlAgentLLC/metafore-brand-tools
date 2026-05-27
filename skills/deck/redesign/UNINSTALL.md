# Uninstall — remove the redesign sub-workflow

The redesign workflow is fully removable. After uninstall, `metafore-deck` behaves exactly as it did before the redesign folder existed.

## Two steps

**1. Delete this folder.**

```bash
rm -rf ~/.claude/skills/metafore-deck/redesign
```

**2. Remove the fenced block from `../SKILL.md`.**

Open `~/.claude/skills/metafore-deck/SKILL.md` and delete everything between (and including) these two HTML comment markers:

```html
<!-- BEGIN REDESIGN MODE (optional, removable — see redesign/UNINSTALL.md) -->
...
<!-- END REDESIGN MODE -->
```

That block sits inside `## Workflow`, just above `### 1. Understand the request`. Removing it puts the workflow back to its original Step 1–5 sequence.

## Verify

After uninstall:

- `ls ~/.claude/skills/metafore-deck/` shows only `SKILL.md`, `assets/`, `references/`
- `grep -n "REDESIGN MODE" ~/.claude/skills/metafore-deck/SKILL.md` returns nothing
- `grep -n "redesign/" ~/.claude/skills/metafore-deck/SKILL.md` returns nothing

The skill description, pattern library, brand tokens, generation pipeline, and from-scratch workflow are all untouched — the uninstall only undoes what was added.
