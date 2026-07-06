from __future__ import annotations

import pytest

from cyberlab.application.use_cases.lab_info_use_case import (
    LabInfoUseCase,
)
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


def test_execute_returns_lab_manifest() -> None:
    # Arrange
    manifest = _create_manifest()

    loader = FakeLabManifestLoader(
        {
            manifest.id: manifest,
        }
    )

    use_case = LabInfoUseCase(loader)

    # Act
    result = use_case.execute(manifest.id)

    # Assert
    assert result == manifest


def test_execute_requests_manifest_from_loader() -> None:
    # Arrange
    manifest = _create_manifest()

    loader = FakeLabManifestLoader(
        {
            manifest.id: manifest,
        }
    )

    use_case = LabInfoUseCase(loader)

    # Act
    use_case.execute(manifest.id)

    # Assert
    assert loader.requested_lab_ids == [
        manifest.id,
    ]


def test_execute_propagates_loader_error() -> None:
    # Arrange
    loader = FakeLabManifestLoader({})

    use_case = LabInfoUseCase(loader)

    # Act / Assert
    with pytest.raises(
        AssertionError,
        match="Unexpected lab id: unknown",
    ):
        use_case.execute("unknown")
