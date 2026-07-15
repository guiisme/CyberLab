# Plugin Template

## Purpose

`templates/plugin` is the canonical starting point for plugins created with:

```bash
uv run cyberlab plugin create my-plugin
```

The command copies the template, renames its Python package, and replaces the
template placeholders with values derived from the plugin ID.

## Generated Structure

For `my-plugin`, the generated project has this layout:

```text
my-plugin/
├── LICENSE
├── README.md
├── pyproject.toml
├── src/
│   └── cyberlab_plugin_my_plugin/
│       ├── __init__.py
│       └── plugin.py
└── tests/
    └── test_plugin.py
```

The template intentionally does not contain a `.venv` or `uv.lock`. Each
generated plugin owns its virtual environment and lock file.

## Template Values

The filesystem scaffolder replaces the following placeholders:

| Placeholder | `my-plugin` value |
| --- | --- |
| `{{PLUGIN_ID}}` | `my-plugin` |
| `{{PLUGIN_NAME}}` | `My Plugin` |
| `{{PLUGIN_PACKAGE}}` | `cyberlab_plugin_my_plugin` |
| `{{PLUGIN_CLASS}}` | `MyPlugin` |

It also renames `src/cyberlab_plugin_hello` to the generated package name and
updates the template test and plugin class references.

## Packaging

The generated `pyproject.toml` uses `uv_build` and maps the distribution to
the source package explicitly:

```toml
[tool.uv.build-backend]
module-name = "cyberlab_plugin_my_plugin"

[project.entry-points."cyberlab.plugins"]
"my-plugin" = "cyberlab_plugin_my_plugin.plugin:MyPlugin"
```

This mapping is required because the distribution ID can contain hyphens while
the Python package name uses underscores and the `cyberlab_plugin_` prefix.

Plugins created inside this repository use the local Core during development:

```toml
[tool.uv.sources]
cyberlab = { path = "..", editable = true }
```

This assumes the plugin directory is created directly under the CyberLab
repository root.

## Development Workflows

### Work in the plugin environment

From the generated plugin directory:

```bash
uv sync
uv run pytest
```

This creates and uses the plugin's own virtual environment. It is useful for
developing and testing the plugin, but does not make the plugin visible to
`uv run cyberlab` executed at the CyberLab repository root.

### Register the plugin in the Core environment

From the CyberLab repository root:

```bash
uv pip install --no-deps -e ./my-plugin
uv run cyberlab plugin list
```

`--no-deps` avoids resolving the Core again because the command installs the
plugin into the environment that already runs CyberLab. The plugin should then
appear in the `Installed Plugins` table.

## Plugin Implementation

Implement the plugin class in `src/cyberlab_plugin_<name>/plugin.py`. Plugin
code should use only the public SDK:

```python
from cyberlab.sdk import PluginManifest
```

The class exposed by the entry point must provide a `manifest` compatible with
`PluginProtocol`. Do not import from CyberLab's internal `application`,
`infrastructure`, `cli`, or `domain` packages.
