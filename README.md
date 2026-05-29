# claude-skills

A [Claude Code](https://docs.claude.com/en/docs/claude-code) skills marketplace by [@dEitY719](https://github.com/dEitY719). Each plugin installs independently — pick what you need.

## Installation

In a Claude Code session:

```
/plugin marketplace add dEitY719/claude-skills
/plugin install visuals
```

Update with `/plugin update visuals`, remove with `/plugin uninstall visuals`.

## Available plugins

| Plugin | Description | Version |
|--------|-------------|---------|
| [`visuals`](./plugins/visuals) | Two skills: **`visualize`** (self-contained HTML decks, infographics, dashboards) and **`excalidraw-diagram`** (Excalidraw architecture/concept diagrams). See its [README](./plugins/visuals/skills/excalidraw-diagram/README.md) for VSCode setup. | `0.4.0` |

## Repository structure

- `.claude-plugin/marketplace.json` — marketplace manifest (catalogs all plugins)
- `plugins/<name>/.claude-plugin/plugin.json` — per-plugin manifest
- `plugins/<name>/skills/<name>/` — skill files (`SKILL.md`, `examples/`, `references/`)

## Adding a new skill

1. Create `plugins/<name>/.claude-plugin/plugin.json`
2. Add skill files under `plugins/<name>/skills/<name>/`
3. Append an entry to `.claude-plugin/marketplace.json` → `plugins[]`
4. Update the table above

## Credits

- `visualize` — by [careerhackeralex](https://github.com/careerhackeralex), MIT.
- `excalidraw-diagram` — by [coleam00](https://github.com/coleam00/excalidraw-diagram-skill), MIT.

## License

MIT — see [LICENSE](./LICENSE).
