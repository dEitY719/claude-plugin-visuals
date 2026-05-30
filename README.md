# claude-plugin-visuals

A [Claude Code](https://docs.claude.com/en/docs/claude-code) skills marketplace by [@dEitY719](https://github.com/dEitY719). Each plugin installs independently — pick what you need.

## Installation

In a Claude Code session:

```
/plugin marketplace add dEitY719/claude-plugin-visuals
/plugin install visuals
```

Update with `/plugin update visuals`, remove with `/plugin uninstall visuals`.

### From the shell (npx)

To install the skills from your terminal — works with Claude, Codex, Gemini, and opencode:

```
npx skills add https://github.com/dEitY719/claude-plugin-visuals
```

## Available plugins

- [`visuals`](./plugins/visuals) `v0.4.0` — two skills:
  - **`visualize`** — self-contained HTML decks, infographics, dashboards ([visual guide ↗](https://deity719.github.io/claude-plugin-visuals/skill-guides/visualize.html))
  - **`excalidraw-diagram`** — Excalidraw architecture/concept diagrams ([visual guide ↗](https://deity719.github.io/claude-plugin-visuals/skill-guides/excalidraw-diagram.html)). See the [README](./plugins/visuals/skills/excalidraw-diagram/README.md) for VSCode setup, or a real [usage example ↗](https://deity719.github.io/claude-plugin-visuals/skill-output/excalidraw-diagram-usage.html) (prompt → diagram).

## Repository structure

- `.claude-plugin/marketplace.json` — marketplace manifest (catalogs all plugins)
- `plugins/<name>/.claude-plugin/plugin.json` — per-plugin manifest
- `plugins/<name>/skills/<name>/` — skill files (`SKILL.md`, `examples/`, `references/`)

## Adding a new skill

1. Create `plugins/<name>/.claude-plugin/plugin.json`
2. Add skill files under `plugins/<name>/skills/<name>/`
3. Append an entry to `.claude-plugin/marketplace.json` → `plugins[]`
4. Update the list above

## License

MIT — see [LICENSE](./LICENSE).
