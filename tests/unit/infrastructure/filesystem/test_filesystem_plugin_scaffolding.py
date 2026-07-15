from __future__ import annotations

from pathlib import Path

import pytest

from cyberlab.infrastructure.filesystem.filesystem_plugin_scaffolding import (
    FilesystemPluginScaffolding,
)


def test_create_creates_plugin(
    tmp_path: Path,
) -> None:
    plugins_root = tmp_path / "plugins"
    scaffolds_root = tmp_path / "scaffolds"

    plugins_root.mkdir()
    (scaffolds_root / "default").mkdir(parents=True)

    scaffolding = FilesystemPluginScaffolding(
        plugins_root=plugins_root,
        plugin_scaffolds_root=scaffolds_root,
    )

    scaffolding.create("demo")

    assert (plugins_root / "demo").exists()


def test_create_existing_plugin_raises_error(
    tmp_path: Path,
) -> None:
    plugins_root = tmp_path / "plugins"
    scaffolds_root = tmp_path / "scaffolds"

    plugins_root.mkdir()
    (plugins_root / "demo").mkdir()

    (scaffolds_root / "default").mkdir(parents=True)

    scaffolding = FilesystemPluginScaffolding(
        plugins_root=plugins_root,
        plugin_scaffolds_root=scaffolds_root,
    )

    with pytest.raises(FileExistsError):
        scaffolding.create("demo")


def test_missing_scaffold_raises_error(
    tmp_path: Path,
) -> None:
    plugins_root = tmp_path / "plugins"

    plugins_root.mkdir()

    scaffolding = FilesystemPluginScaffolding(
        plugins_root=plugins_root,
        plugin_scaffolds_root=tmp_path / "scaffolds",
    )

    with pytest.raises(FileNotFoundError):
        scaffolding.create(
            "demo",
            "missing",
        )


def create_scaffold(
    root: Path,
) -> None:
    (root / "src" / "cyberlab_plugin_hello").mkdir(
        parents=True,
    )

    (root / "tests").mkdir()

    (root / "README.md").write_text(
        "{{PLUGIN_ID}}",
        encoding="utf-8",
    )

    (root / "pyproject.toml").write_text(
        """[tool.uv.build-backend]
module-name = \"{{PLUGIN_PACKAGE}}\"
""",
        encoding="utf-8",
    )

    (root / "src" / "cyberlab_plugin_hello" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )

    (root / "src" / "cyberlab_plugin_hello" / "plugin.py").write_text(
        "{{PLUGIN_PACKAGE}}\n{{PLUGIN_CLASS}}\n",
        encoding="utf-8",
    )


def test_create_replaces_placeholders(
    tmp_path: Path,
) -> None:
    plugins_root = tmp_path / "plugins"
    scaffolds_root = tmp_path / "scaffolds"

    plugins_root.mkdir()

    create_scaffold(scaffolds_root)

    scaffolding = FilesystemPluginScaffolding(
        plugins_root=plugins_root,
        plugin_scaffolds_root=scaffolds_root,
    )

    scaffolding.create("demo-plugin")

    readme = plugins_root / "demo-plugin" / "README.md"

    assert "{{PLUGIN_ID}}" not in readme.read_text()

    assert "demo-plugin" in readme.read_text()

    pyproject = plugins_root / "demo-plugin" / "pyproject.toml"

    assert 'module-name = "cyberlab_plugin_demo_plugin"' in pyproject.read_text()


def test_create_renames_python_package(
    tmp_path: Path,
) -> None:
    plugins_root = tmp_path / "plugins"
    scaffolds_root = tmp_path / "scaffolds"

    plugins_root.mkdir()

    create_scaffold(scaffolds_root)

    scaffolding = FilesystemPluginScaffolding(
        plugins_root=plugins_root,
        plugin_scaffolds_root=scaffolds_root,
    )

    scaffolding.create("demo-plugin")

    assert (plugins_root / "demo-plugin" / "src" / "cyberlab_plugin_demo_plugin").exists()

    assert not (plugins_root / "demo-plugin" / "src" / "cyberlab_plugin_hello").exists()
