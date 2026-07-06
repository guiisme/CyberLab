from dataclasses import FrozenInstanceError

import pytest

from cyberlab.domain.models.lab_manifest import LabManifest
from tests.fakes.fake_lab_manifest_loader import FakeLabManifestLoader


def test_create_lab_manifest() -> None:
    manifest = LabManifest(
        id="xss-basic",
        name="Basic XSS",
        description="Basic reflected XSS laboratory.",
        category="web",
        difficulty="easy",
        version="1.0.0",
    )

    assert manifest.id == "xss-basic"
    assert manifest.name == "Basic XSS"
    assert manifest.description == "Basic reflected XSS laboratory."
    assert manifest.category == "web"
    assert manifest.difficulty == "easy"
    assert manifest.version == "1.0.0"


def test_lab_manifest_is_immutable() -> None:
    # Arrange
    manifest = LabManifest(
        id="xss-basic",
        name="Basic XSS",
        description="Basic reflected XSS laboratory.",
        category="web",
        difficulty="easy",
        version="1.0.0",
    )

    # Act / Assert
    with pytest.raises(FrozenInstanceError):
        manifest.name = "New Name"


def test_lab_manifests_with_same_values_are_equal() -> None:
    first = LabManifest(
        id="xss-basic",
        name="Basic XSS",
        description="Basic reflected XSS laboratory.",
        category="web",
        difficulty="easy",
        version="1.0.0",
    )

    second = LabManifest(
        id="xss-basic",
        name="Basic XSS",
        description="Basic reflected XSS laboratory.",
        category="web",
        difficulty="easy",
        version="1.0.0",
    )

    assert first == second


def test_load_returns_manifest() -> None:
    # Arrange
    manifest = LabManifest(
        id="xss-basic",
        name="Basic XSS",
        description="Basic reflected XSS laboratory.",
        category="web",
        difficulty="easy",
        version="1.0.0",
    )

    loader = FakeLabManifestLoader(
        {
            "xss-basic": manifest,
        }
    )

    # Act
    result = loader.load("xss-basic")

    # Assert
    assert result == manifest
