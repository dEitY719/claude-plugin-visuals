# claude-skills

A curated marketplace of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills maintained by [@dEitY719](https://github.com/dEitY719).

Each plugin below is an independently installable skill. Pick what you need — no all-or-nothing.

## Installation (for colleagues)

Inside a Claude Code session:

```
/plugin marketplace add dEitY719/claude-skills
/plugin install visualize
```

That's it. Claude Code pulls the skill, registers it, and you can use it immediately.

To update later:

```
/plugin update visualize
```

To remove:

```
/plugin uninstall visualize
```

## Available plugins

| Plugin | Description | Version |
|--------|-------------|---------|
| [`visualize`](./plugins/visualize) | Bundles two skills: **`visualize`** (self-contained HTML — slide decks, infographics, dashboards, one-pagers) and **`excalidraw-diagram`** (Excalidraw architecture/concept diagrams that argue visually). See [excalidraw-diagram README](./plugins/visualize/skills/excalidraw-diagram/README.md) for the VSCode extension setup. | `0.4.0` |

## Repository structure

```
claude-skills/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest (catalogs all plugins)
├── plugins/
│   └── visualize/
│       ├── .claude-plugin/
│       │   └── plugin.json        # Plugin manifest
│       └── skills/
│           └── visualize/
│               ├── SKILL.md       # Skill definition (what Claude reads)
│               ├── examples/      # Reference outputs
│               └── references/    # Design/CSS/library notes
├── README.md
└── LICENSE
```

## Adding a new skill to this marketplace

1. Create `plugins/<skill-name>/.claude-plugin/plugin.json`
2. Put skill files under `plugins/<skill-name>/skills/<skill-name>/`
3. Append a new entry in `.claude-plugin/marketplace.json` → `plugins[]`
4. Update this README's table

## Credits

- `visualize` — original skill by [careerhackeralex](https://github.com/careerhackeralex), MIT licensed. Repackaged here for easier colleague distribution.
- `excalidraw-diagram` — original skill by [coleam00](https://github.com/coleam00/excalidraw-diagram-skill), MIT licensed. Bundled inside the `visualize` plugin.

## License

MIT — see [LICENSE](./LICENSE).
