from __future__ import annotations

from pathlib import Path

import pytest

from cyberlab.infrastructure.filesystem.filesystem_lab_scaffolding import (
    FilesystemLabScaffolding,
)


def _create_default_scaffold(
    scaffolds_root: Path,
) -> None:
    scaffold = scaffolds_root / "default"

    (scaffold / "application").mkdir(parents=True)
    (scaffold / "scripts").mkdir()
    (scaffold / "seed").mkdir()

    (scaffold / "lab.yaml").write_text(
        "id: {{LAB_ID}}\nname: {{LAB_NAME}}\n",
        encoding="utf-8",
    )

    (scaffold / "README.md").write_text(
        "# {{LAB_NAME}}\n\nCyberLab\n",
        encoding="utf-8",
    )

    (scaffold / "compose.yaml").write_text(
        "services: {}\n",
        encoding="utf-8",
    )


def test_create_creates_lab_directory(
    tmp_path: Path,
) -> None:
    labs_root = tmp_path / "labs"
    scaffolds_root = tmp_path / "scaffolds"

    labs_root.mkdir()

    _create_default_scaffold(
        scaffolds_root,
    )

    scaffolding = FilesystemLabScaffolding(
        labs_root=labs_root,
        scaffolds_root=scaffolds_root,
    )

    scaffolding.create(
        "jwt-basic",
    )

    assert (labs_root / "jwt-basic").is_dir()


def test_create_replaces_lab_id_placeholder(
    tmp_path: Path,
) -> None:
    labs_root = tmp_path / "labs"
    scaffolds_root = tmp_path / "scaffolds"

    labs_root.mkdir()

    _create_default_scaffold(
        scaffolds_root,
    )

    scaffolding = FilesystemLabScaffolding(
        labs_root=labs_root,
        scaffolds_root=scaffolds_root,
    )

    scaffolding.create(
        "jwt-basic",
    )

    manifest = (labs_root / "jwt-basic" / "lab.yaml").read_text(
        encoding="utf-8",
    )

    assert "jwt-basic" in manifest
    assert "{{LAB_ID}}" not in manifest


def test_create_replaces_lab_name_placeholder(
    tmp_path: Path,
) -> None:
    labs_root = tmp_path / "labs"
    scaffolds_root = tmp_path / "scaffolds"

    labs_root.mkdir()

    _create_default_scaffold(
        scaffolds_root,
    )

    scaffolding = FilesystemLabScaffolding(
        labs_root=labs_root,
        scaffolds_root=scaffolds_root,
    )

    scaffolding.create(
        "jwt-basic",
    )

    readme = (labs_root / "jwt-basic" / "README.md").read_text(
        encoding="utf-8",
    )

    assert "# Jwt Basic" in readme
    assert "{{LAB_NAME}}" not in readme


def test_create_creates_directory_structure(
    tmp_path: Path,
) -> None:
    labs_root = tmp_path / "labs"
    scaffolds_root = tmp_path / "scaffolds"

    labs_root.mkdir()

    _create_default_scaffold(
        scaffolds_root,
    )

    scaffolding = FilesystemLabScaffolding(
        labs_root=labs_root,
        scaffolds_root=scaffolds_root,
    )

    scaffolding.create(
        "jwt-basic",
    )

    lab = labs_root / "jwt-basic"

    assert (lab / "application").is_dir()
    assert (lab / "scripts").is_dir()
    assert (lab / "seed").is_dir()


def test_create_preserves_non_placeholder_content(
    tmp_path: Path,
) -> None:
    labs_root = tmp_path / "labs"
    scaffolds_root = tmp_path / "scaffolds"

    labs_root.mkdir()

    _create_default_scaffold(
        scaffolds_root,
    )

    scaffolding = FilesystemLabScaffolding(
        labs_root=labs_root,
        scaffolds_root=scaffolds_root,
    )

    scaffolding.create(
        "jwt-basic",
    )

    readme = (labs_root / "jwt-basic" / "README.md").read_text(
        encoding="utf-8",
    )

    assert "CyberLab" in readme


def test_create_fails_when_lab_exists(
    tmp_path: Path,
) -> None:
    labs_root = tmp_path / "labs"
    scaffolds_root = tmp_path / "scaffolds"

    labs_root.mkdir()

    _create_default_scaffold(
        scaffolds_root,
    )

    (labs_root / "jwt-basic").mkdir()

    scaffolding = FilesystemLabScaffolding(
        labs_root=labs_root,
        scaffolds_root=scaffolds_root,
    )

    with pytest.raises(FileExistsError):
        scaffolding.create(
            "jwt-basic",
        )


def test_create_fails_when_scaffold_does_not_exist(
    tmp_path: Path,
) -> None:
    labs_root = tmp_path / "labs"

    labs_root.mkdir()

    scaffolding = FilesystemLabScaffolding(
        labs_root=labs_root,
        scaffolds_root=tmp_path / "scaffolds",
    )

    with pytest.raises(FileNotFoundError):
        scaffolding.create(
            "jwt-basic",
            scaffold="default",
        )
