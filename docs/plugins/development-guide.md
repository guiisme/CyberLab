# Plugin Development Guide

## Purpose

CyberLab provides a native plugin architecture that allows new capabilities to
be added without modifying the Core application.

This document describes the recommended way to develop plugins using the
official CyberLab SDK.

---

# Plugin Architecture

CyberLab discovers plugins through Python Entry Points.

The plugin loading pipeline is intentionally simple.

```text
Python Package

        │

        ▼

Python Entry Points

        │

        ▼

EntryPointProvider

        │

        ▼

PluginLoader

        │

        ▼

PluginRegistry

        │

        ▼

CyberLab
```

Plugin developers do not need to interact directly with this pipeline.

---

# Public SDK

The only supported API for plugin development is:

```python
from cyberlab.sdk import (
    Plugin,
    PluginManifest,
    PluginProtocol,
)
```

Everything exported by `cyberlab.sdk` is considered the stable public API for
plugin developers.

Internal modules may change without notice and should not be imported
directly.

---

# Project Structure

The official template follows this structure:

```text
plugin/

├── README.md
├── LICENSE
├── pyproject.toml
├── src/
│   └── cyberlab_plugin_hello/
│       ├── __init__.py
│       └── plugin.py
└── tests/
```

New plugins should follow the same organization.

---

# Packaging Standard

CyberLab adopts the following conventions.

| Element | Convention |
|---------|------------|
| Distribution | `cyberlab-plugin-<name>` |
| Python package | `cyberlab_plugin_<name>` |
| Entry Point Group | `cyberlab.plugins` |
| Plugin class | `<Name>Plugin` |
| Build backend | `uv_build` |

These conventions should be followed by both official and third-party plugins.

---

# Entry Points

Plugins are registered using Python Entry Points.

Example:

```toml
[project.entry-points."cyberlab.plugins"]
hello = "cyberlab_plugin_hello.plugin:HelloPlugin"
```

---

# Plugin Manifest

Every plugin exposes a manifest describing its metadata.

Example:

```python
@property
def manifest(self) -> PluginManifest:
    return PluginManifest(
        id="hello-plugin",
        name="Hello Plugin",
        version="0.1.0",
        description="Example CyberLab plugin.",
        author="CyberLab",
        capabilities=(),
    )
```

---

# Development Workflow

The recommended workflow is:

```text
Create Plugin

        │

        ▼

Implement Manifest

        │

        ▼

Install Editable

        │

        ▼

Validate

        │

        ▼

Test
```

---

# Local Validation

From the CyberLab repository root, install the generated plugin into the
CyberLab development environment. The Core is already installed there, so its
dependencies do not need to be resolved again.

```bash
uv pip install --no-deps -e ./my-plugin
```

Validate that CyberLab discovers the plugin.

```bash
uv run cyberlab plugin list
```

If the plugin appears in the list, the installation was successful.

---

# Best Practices

- Import exclusively from `cyberlab.sdk`.
- Do not import internal CyberLab modules.
- Keep plugins independent from infrastructure details.
- Follow the official template.
- Keep plugins focused on a single responsibility.

---

# Future Evolution

The current architecture is designed to support future capabilities, including:

- Official plugins
- Community plugins
- Plugin marketplace
- Plugin creation command
- Plugin SDK evolution

These capabilities should extend the platform without requiring modifications
to the Core application.

# Design Principles

Plugin development follows the same architectural principles as the CyberLab Core.

- Prefer protocols over inheritance.
- Prefer composition over coupling.
- Keep plugins independent from infrastructure.
- Extend the platform instead of modifying the Core.
- Use the public SDK exclusively.
