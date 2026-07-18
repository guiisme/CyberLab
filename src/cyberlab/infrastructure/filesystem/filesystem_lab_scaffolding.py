from __future__ import annotations

import shutil
from pathlib import Path

from cyberlab.application.interfaces.lab_scaffolding_protocol import (
    LabScaffoldingProtocol,
)


class FilesystemLabScaffolding(LabScaffoldingProtocol):
    """Create laboratories from filesystem scaffolds."""

    def __init__(
        self,
        labs_root: Path,
        scaffolds_root: Path,
    ) -> None:
        self._labs_root = labs_root
        self._scaffolds_root = scaffolds_root

    def create(
        self,
        lab_id: str,
        scaffold: str = "default",
        profile: str = "web",
    ) -> None:
        """Create a laboratory from a scaffold."""

        destination = self._destination_path(lab_id)

        if destination.exists():
            raise FileExistsError(f'Laboratory "{lab_id}" already exists.')

        source = self._scaffold_path(scaffold)

        if not source.exists():
            raise FileNotFoundError(f'Scaffold "{scaffold}" does not exist.')

        self._copy_scaffold(
            source,
            destination,
        )

        self._replace_placeholders(
            destination,
            self._placeholders(lab_id, profile),
        )

    def _scaffold_path(
        self,
        scaffold: str,
    ) -> Path:
        return self._scaffolds_root / scaffold

    def _destination_path(
        self,
        lab_id: str,
    ) -> Path:
        return self._labs_root / lab_id

    def _copy_scaffold(
        self,
        source: Path,
        destination: Path,
    ) -> None:
        shutil.copytree(
            source,
            destination,
        )

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
            text = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return

        for placeholder, value in placeholders.items():
            text = text.replace(
                placeholder,
                value,
            )

        file.write_text(
            text,
            encoding="utf-8",
        )

    def _placeholders(
        self,
        lab_id: str,
        profile: str,
    ) -> dict[str, str]:
        return {
            "{{LAB_ID}}": lab_id,
            "{{LAB_NAME}}": self._lab_name(lab_id),
            "{{KALI_PROFILE}}": profile,
        }

    @staticmethod
    def _lab_name(
        lab_id: str,
    ) -> str:
        return lab_id.replace(
            "-",
            " ",
        ).title()
