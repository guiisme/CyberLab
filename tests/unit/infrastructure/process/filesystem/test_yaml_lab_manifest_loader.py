from pathlib import Path

import pytest

from cyberlab.domain.models.lab_manifest import LabManifest
from cyberlab.infrastructure.filesystem.yaml_lab_manifest_loader import (
    YamlLabManifestLoader,
)


def test_load_returns_lab_manifest(tmp_path: Path) -> None:
    # Arrange
    lab_dir = tmp_path / "xss-basic"
    lab_dir.mkdir()

    (lab_dir / "lab.yaml").write_text(
        """
id: xss-basic
name: Basic XSS
description: Basic reflected XSS laboratory.
category: web
difficulty: easy
version: 1.0.0
""".strip()
    )

    loader = YamlLabManifestLoader(tmp_path)

    # Act
    manifest = loader.load("xss-basic")

    # Assert
    assert manifest == LabManifest(
        id="xss-basic",
        name="Basic XSS",
        description="Basic reflected XSS laboratory.",
        category="web",
        difficulty="easy",
        version="1.0.0",
    )


def test_load_raises_file_not_found_when_manifest_does_not_exist(
    tmp_path: Path,
) -> None:
    # Arrange
    loader = YamlLabManifestLoader(tmp_path)

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        loader.load("unknown")
