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

All skills read one shared brand pack, `assets/brand/metafore_brand.md` (voice, legibility floors, density, visual coverage, tokens, content preservation). Update it once and every skill picks up the change. Skill files only hold format-specific rules.

## Requirements

Once per machine:

```
pip install playwright pillow python-pptx python-docx pymupdf pyyaml
python3 -m playwright install chromium
```

LibreOffice is optional (only for thumbnails when redesigning an existing `.pptx`).

## How the skills work

Claude authors a small `name.src.html` with placeholders (`<!-- @fonts -->`, `/* @tokens:deck */`, `<!-- @logo:logo-light -->`, `src="@icon:Nodes"`, `<!-- @footer -->`) and the bundled scripts do the heavy lifting:

| Script | Does |
|---|---|
| `scripts/build_html.py` | Assembles the self-contained HTML (tokens, pattern CSS, logos, icons, footers) |
| `skills/deck/scripts/build_deck.py` | Deck YAML content file → HTML → check → PPTX in one command |
| `scripts/office_check.py` | Exports a .pptx/.docx through PowerPoint/Word (macOS) and makes one overview sheet |
| `scripts/check.py` | Brand + layout lint as text (type floors, 3-line paragraphs, overflow, overlap, missing visuals, retired colors, voice flags) plus one ≤1600px contact sheet; also checks `.docx` |
| `scripts/render.py` | Final PNG (2×) or PDF export, plus a small preview |
| `skills/deck/scripts/build_pptx.py` | HTML deck → editable PPTX (renders only image/hybrid slides, caches unchanged ones) |
| `skills/deck/redesign/extract.py` | Existing deck (PPTX/PDF/MD) → text manifest + one contact sheet |
| `skills/doc/assets/build_doc.py` | python-docx library for branded Word docs |

This replaces re-typing build code, CSS, and SVG on every run, and replaces screenshot-based checking with a text report.

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
│   ├── deck/       (SKILL.md + assets/patterns.css + references/patterns/ + scripts + redesign)
│   ├── doc/        (SKILL.md + assets + references)
│   └── graphic/    (SKILL.md + assets + references)
├── scripts/        (build_html.py, check.py, render.py, office_check.py — shared toolchain)
├── assets/
│   ├── brand/      (metafore_brand.md — the shared brand pack)
│   └── graphics/   (logos, 29 line icons)
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
