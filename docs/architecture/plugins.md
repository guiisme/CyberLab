# CyberLab Plugin Architecture

## Purpose

The CyberLab Plugin System allows third-party developers to extend CyberLab without modifying its core source code.

Plugins are discovered dynamically through Python Entry Points and interact with the framework exclusively through the public SDK.

This architecture provides:

- Stable extension points
- Loose coupling
- Independent plugin development
- Safe framework evolution
- Clean separation between the Core and external extensions

---

# Architecture

```
                +----------------------+
                |   CyberLab CLI       |
                +----------+-----------+
                           |
                           v
                  Application Use Cases
                           |
                           v
                 Plugin Registry Protocol
                           |
                           v
                Infrastructure Registry
                           |
                           v
                 Python Entry Points
                           |
                           v
                     External Plugins
```

The CyberLab Core never imports plugins directly.

Instead, plugins are discovered dynamically during application startup.

---

# Public SDK

Plugins must depend exclusively on the public SDK.

```
cyberlab.sdk
```

The SDK exposes the stable contracts required for plugin development, including:

- Plugin
- PluginManifest
- Capability
- Public protocols
- Shared value objects

Plugins must never import internal CyberLab modules.

Allowed:

```python
from cyberlab.sdk import Plugin
```

Not allowed:

```python
from cyberlab.infrastructure...
```

or

```python
from cyberlab.application...
```

The SDK represents the public API of CyberLab.

---

# Plugin Discovery

CyberLab discovers plugins using Python Entry Points.

Each plugin registers itself inside its own `pyproject.toml`.

Example:

```toml
[project.entry-points."cyberlab.plugins"]
example = "cyberlab_plugin_example.plugin:ExamplePlugin"
```

At startup, CyberLab loads all entry points from the `cyberlab.plugins` group.

Each discovered plugin is instantiated and registered in the Plugin Registry.

---

# Plugin Lifecycle

The discovery process follows these steps:

```
Application Startup
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
Application Use Cases
        │
        ▼
CLI
```

This keeps plugin loading isolated inside the Infrastructure layer.

---

# Plugin Registry

The Plugin Registry maintains all loaded plugins during application execution.

Responsibilities include:

- Register plugins
- Retrieve plugins by identifier
- Verify plugin existence
- Enumerate installed plugins

The registry is an Infrastructure component accessed through a protocol defined in the Application layer.

---

# Creating Plugins

CyberLab provides a scaffold generator.

```
cyberlab plugin create my-plugin
```

The generated project contains:

```
my-plugin/

├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── cyberlab_plugin_my_plugin/
└── tests/
```

The scaffold is immediately compatible with Python packaging standards.

---

# Installing Plugins

Plugins are installed as editable Python packages.

Example:

```bash
uv pip install -e ./my-plugin
```

Once installed, CyberLab discovers the plugin automatically.

Installed plugins can be listed using:

```bash
cyberlab plugin list
```

---

# Design Principles

The Plugin System follows the same architectural principles as the CyberLab Core.

## Dependency Inversion

The Core depends on protocols.

Plugins depend only on the SDK.

Neither side depends directly on the other.

---

## Stable Public API

Only the SDK is considered public.

Internal packages may evolve without breaking plugins.

---

## Independent Distribution

Plugins are standalone Python packages.

Each plugin owns:

- dependencies
- release cycle
- versioning
- tests
- documentation

---

## Runtime Discovery

Plugins are not hardcoded.

CyberLab discovers extensions dynamically through Python Entry Points.

This eliminates manual registration and allows independent deployment.

---

# Future Evolution

The current architecture intentionally leaves room for future capabilities, including:

- Multiple plugin templates
- Plugin capabilities
- Plugin configuration
- Dependency management
- Marketplace support
- Plugin compatibility validation
- Plugin enable/disable
- Plugin metadata validation

These features can be introduced without changing the public SDK.

---

# Summary

The CyberLab Plugin Architecture transforms CyberLab from a standalone framework into an extensible platform.

By combining:

- Public SDK
- Python Entry Points
- Plugin Registry
- Dependency Inversion
- Clean Architecture

CyberLab enables external extensions while preserving the independence and stability of the Core.
