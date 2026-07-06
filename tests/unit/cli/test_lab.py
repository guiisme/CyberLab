from typer.testing import CliRunner

from cyberlab.cli.app import create_app
from cyberlab.domain.models.lab_manifest import LabManifest
from tests.fakes.fake_lab_manifest_loader import (
    FakeLabManifestLoader,
)

runner = CliRunner()


def test_lab_info_displays_manifest() -> None:
    # Arrange
    manifest = LabManifest(
        id="xss-basic",
        name="Basic XSS",
        description="Basic reflected XSS laboratory.",
        category="web",
        difficulty="easy",
        version="1.0.0",
    )

    app = create_app(
        manifest_loader=FakeLabManifestLoader(
            {
                manifest.id: manifest,
            }
        )
    )

    # Act
    result = runner.invoke(
        app,
        [
            "lab",
            "info",
            manifest.id,
        ],
    )

    # Assert
    assert result.exit_code == 0
    assert "Basic XSS" in result.stdout
    assert "web" in result.stdout
    assert "easy" in result.stdout
    assert "1.0.0" in result.stdout
