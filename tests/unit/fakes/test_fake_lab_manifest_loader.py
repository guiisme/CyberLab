from __future__ import annotations

import pytest

from cyberlab.domain.models.lab_manifest import LabManifest
from tests.fakes.fake_lab_manifest_loader import (
    FakeLabManifestLoader,
)


def _create_manifest() -> LabManifest:
    return LabManifest(
        id="xss-basic",
        name="Basic XSS",
        description="Basic reflected XSS laboratory.",
        category="web",
        difficulty="easy",
        version="1.0.0",
    )


def test_load_returns_manifest() -> None:
    # Arrange
    manifest = _create_manifest()

    loader = FakeLabManifestLoader(
        {
            manifest.id: manifest,
        }
    )

    # Act
    result = loader.load(manifest.id)

    # Assert
    assert result == manifest


def test_load_records_requested_lab_id() -> None:
    # Arrange
    manifest = _create_manifest()

    loader = FakeLabManifestLoader(
        {
            manifest.id: manifest,
        }
    )

    # Act
    loader.load(manifest.id)

    # Assert
    assert loader.requested_lab_ids == [
        manifest.id,
    ]


def test_load_raises_assertion_error_for_unknown_lab() -> None:
    # Arrange
    loader = FakeLabManifestLoader({})

    # Act / Assert
    with pytest.raises(
        AssertionError,
        match="Unexpected lab id: unknown",
    ):
        loader.load("unknown")
