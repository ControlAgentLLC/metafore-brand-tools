# Metafore Brand Tools

A Claude Code plugin that bundles Metafore's branded-content skills so any teammate gets the same on-brand brochures, decks, docs, dashboards, and graphics without setup.

## What's inside

| Skill | Invoke as | Output |
|---|---|---|
| Brochure | `metafore:brochure` | Self-contained HTML brochure / one-pager / sales sheet |
| Dashboard | `metafore:dashboard` | HTML internal dashboard / admin / operator UI |
| Deck | `metafore:deck` | HTML deck (1920×1080) + generated editable PPTX |
| Doc | `metafore:doc` | Branded `.docx` (white paper, proposal, SOW, memo) |
| Graphic | `metafore:graphic` | Brand-compliant HTML graphics rendered to PNG |

All skills read shared brand rules from `assets/brand/metafore_brand.md` and the deck-specific calibrations in `assets/brand/feedback_*.md`. Update those files once and every skill picks up the new rules.

## Slash command

`/metafore:brand` — guided entry point. Run it with no arguments to see the five artifact types and pick one, or pass what you want directly:

```
/metafore:brand brochure introducing Pulse to a logistics CIO
/metafore:brand deck for the Q3 board review
/metafore:brand            ← lists the options and asks
```

It loads the brand pack first, infers (or asks for) the right artifact type, then hands off to the matching skill. The individual skills also auto-trigger on their own — the command is just a discovery surface and a guaranteed brand-pack load.

## Install (teammates)

You need read access to the `ControlAgentLLC/metafore-brand-tools` GitHub repo and a GitHub account authenticated locally (`gh auth login` or SSH key).

Inside Claude Code:

```
/plugin marketplace add ControlAgentLLC/metafore-brand-tools
/plugin install metafore@metafore
```

That's it — restart Claude Code and the skills will appear as `metafore:brochure`, `metafore:dashboard`, etc.

To auto-pull updates, add this to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "metafore": {
      "source": { "source": "github", "repo": "ControlAgentLLC/metafore-brand-tools" },
      "autoUpdate": true
    }
  }
}
```

Otherwise pull manually with `/plugin marketplace update metafore`.

## Layout

```
metafore-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── brochure/   (SKILL.md + assets + references)
│   ├── dashboard/  (SKILL.md + references)
│   ├── deck/       (SKILL.md + assets + redesign + references)
│   ├── doc/        (SKILL.md + assets + references)
│   └── graphic/    (SKILL.md + references)
├── assets/
│   └── brand/      (shared brand pack — voice, tokens, calibrations)
└── README.md
```

## Maintainers

For day-to-day authoring, clone this repo and run Claude with `--plugin-dir`:

```bash
git clone git@github.com:ControlAgentLLC/metafore-brand-tools.git
claude --plugin-dir ./metafore-brand-tools
```

Your edits are live without needing to reinstall. When you're ready to ship:

1. Bump `version` in `.claude-plugin/plugin.json` (semver).
2. Commit and push.
3. Teammates pull on next `/plugin marketplace update metafore` (or automatically if `autoUpdate: true`).

To grant a collaborator edit access: GitHub repo Settings → Collaborators → add their handle with **Write** permission. All other readers stay at **Read**.

## Versioning

We use semver:
- **Patch** (0.1.0 → 0.1.1) — typo fixes, prompt tweaks, calibration updates.
- **Minor** (0.1.0 → 0.2.0) — new patterns, new skills, brand-pack additions.
- **Major** (0.x → 1.0) — breaking changes (renamed skills, removed patterns, restructured assets).
