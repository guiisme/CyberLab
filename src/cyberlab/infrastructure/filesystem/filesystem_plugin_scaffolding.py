from __future__ import annotations

import shutil
from pathlib import Path

from cyberlab.application.interfaces.plugin_scaffolding_protocol import (
    PluginScaffoldingProtocol,
)


class FilesystemPluginScaffolding(PluginScaffoldingProtocol):
    """Create plugins from filesystem scaffolds."""

    _TEMPLATE_ENTRY_POINT = "hello"

    def __init__(
        self,
        plugins_root: Path,
        plugin_scaffolds_root: Path,
    ) -> None:
        self._plugins_root = plugins_root
        self._plugin_scaffolds_root = plugin_scaffolds_root

    def create(
        self,
        plugin_id: str,
        plugin_scaffold: str = "default",
    ) -> None:
        """Create a new plugin project."""

        destination = self._destination_path(plugin_id)

        if destination.exists():
            raise FileExistsError(f'Plugin "{plugin_id}" already exists.')

        source = self._plugin_scaffold_path(plugin_scaffold)

        if not source.exists():
            raise FileNotFoundError(f'Plugin scaffold "{plugin_scaffold}" does not exist.')

        # 1. Copy template
        self._copy_scaffold(
            source,
            destination,
        )

        # 2. Rename Python package
        self._rename_python_package(
            destination,
            plugin_id,
        )

        # 3. Replace placeholders
        self._replace_placeholders(
            destination,
            self._placeholders(plugin_id),
        )

    def _plugin_scaffold_path(
        self,
        plugin_scaffold: str,
    ) -> Path:
        """Return the plugin scaffold path.

        Reserved for future support of multiple plugin scaffolds.
        """

        _ = plugin_scaffold

        return self._plugin_scaffolds_root

    def _destination_path(
        self,
        plugin_id: str,
    ) -> Path:
        return self._plugins_root / plugin_id

    def _copy_scaffold(
        self,
        source: Path,
        destination: Path,
    ) -> None:
        shutil.copytree(
            source,
            destination,
        )

    def _rename_python_package(
        self,
        root: Path,
        plugin_id: str,
    ) -> None:
        source = root / "src" / "cyberlab_plugin_hello"
        destination = root / "src" / self._package_name(plugin_id)

        if source.exists():
            source.rename(destination)

    def _replace_placeholders(
        self,
        root: Path,
        placeholders: dict[str, str],
    ) -> None:
        for path in root.rglob("*"):
            if path.is_file():
                self._replace_file(
                    path,
                    placeholders,
                )

    def _replace_file(
        self,
        file: Path,
        placeholders: dict[str, str],
    ) -> None:
        try:
            text = file.read_text(
                encoding="utf-8",
            )
        except UnicodeDecodeError:
            return

        if file.name == "pyproject.toml":
            text = self._update_pyproject(
                text=text,
                placeholders=placeholders,
            )

        #
        # Template-specific replacements
        #
        text = text.replace(
            "HelloPlugin",
            placeholders["{{PLUGIN_CLASS}}"],
        )

        text = text.replace(
            "hello-plugin",
            placeholders["{{PLUGIN_ID}}"],
        )

        text = text.replace(
            "Hello Plugin",
            placeholders["{{PLUGIN_NAME}}"],
        )

        #
        # Generic placeholders
        #
        for placeholder, value in placeholders.items():
            text = text.replace(
                placeholder,
                value,
            )

        file.write_text(
            text,
            encoding="utf-8",
        )

    def _update_pyproject(
        self,
        text: str,
        placeholders: dict[str, str],
    ) -> str:
        """Apply pyproject.toml specific replacements."""

        return text.replace(
            f"{self._TEMPLATE_ENTRY_POINT} = ",
            f'"{placeholders["{{PLUGIN_ID}}"]}" = ',
        )

    def _placeholders(
        self,
        plugin_id: str,
    ) -> dict[str, str]:
        return {
            "{{PLUGIN_ID}}": plugin_id,
            "{{PLUGIN_NAME}}": self._plugin_name(plugin_id),
            "{{PLUGIN_PACKAGE}}": self._package_name(plugin_id),
            "{{PLUGIN_CLASS}}": self._class_name(plugin_id),
            "{{PLUGIN_ENTRYPOINT}}": plugin_id.replace("-", "_"),
        }

    @staticmethod
    def _plugin_name(
        plugin_id: str,
    ) -> str:
        return plugin_id.replace(
            "-",
            " ",
        ).title()

    @staticmethod
    def _package_name(
        plugin_id: str,
    ) -> str:
        return f"cyberlab_plugin_{plugin_id.replace('-', '_')}"

    @staticmethod
    def _class_name(
        plugin_id: str,
    ) -> str:
        return "".join(word.capitalize() for word in plugin_id.replace("-", "_").split("_"))
