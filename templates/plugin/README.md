# CyberLab Plugin Template

This template demonstrates the recommended structure for developing a
CyberLab plugin.

## Requirements

- Python 3.12+
- uv
- CyberLab source repository

## Installation

From the CyberLab repository root:

```bash
uv pip install -e templates/plugin
```

## Validate

```bash
uv run cyberlab plugin list
```

If the plugin appears in the list, the installation was successful.
