from typer.testing import CliRunner

from cyberlab.cli.app import create_app
from cyberlab.domain.models.check_result import CheckResult
from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)
from cyberlab.domain.models.lab_logs import LabLogs
from cyberlab.domain.models.lab_manifest import LabManifest
from cyberlab.domain.models.lab_validation_report import LabValidationReport
from tests.fakes.fake_lab_lifecycle import (
    FakeLabLifeCycle,
)
from tests.fakes.fake_lab_manifest_loader import (
    FakeLabManifestLoader,
)
from tests.fakes.fake_lab_validator import FakeLabValidator

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


def _create_execution_report() -> LabExecutionReport:
    return LabExecutionReport(
        lab_id="xss-basic",
        success=True,
        message="Laboratory started successfully.",
    )


def _create_stop_report() -> LabExecutionReport:
    return LabExecutionReport(
        lab_id="xss-basic",
        success=True,
        message="Laboratory stopped successfully.",
    )


def _create_validation_report() -> LabValidationReport:
    return LabValidationReport(
        checks=(
            CheckResult(
                name="lab.yaml",
                success=True,
                message="Found",
            ),
            CheckResult(
                name="README.md",
                success=True,
                message="Found",
            ),
            CheckResult(
                name="compose.yaml",
                success=True,
                message="Found",
            ),
        )
    )


def test_lab_validate_displays_validation_report() -> None:
    # Arrange
    report = _create_validation_report()

    app = create_app(
        manifest_loader=FakeLabManifestLoader({}),
        validator=FakeLabValidator(
            {
                "xss-basic": report,
            }
        ),
    )

    # Act
    result = runner.invoke(
        app,
        [
            "lab",
            "validate",
            "xss-basic",
        ],
    )

    # Assert
    assert result.exit_code == 0

    assert "lab.yaml" in result.stdout
    assert "README.md" in result.stdout
    assert "compose.yaml" in result.stdout

    assert "Laboratory is valid." in result.stdout


def test_lab_run_displays_execution_report() -> None:
    # Arrange
    app = create_app(
        manifest_loader=FakeLabManifestLoader({}),
        validator=FakeLabValidator({}),
        lab_runner=FakeLabLifeCycle(
            {
                "xss-basic": _create_execution_report(),
            }
        ),
    )

    # Act
    result = runner.invoke(
        app,
        [
            "lab",
            "run",
            "xss-basic",
        ],
    )

    # Assert
    assert result.exit_code == 0

    assert 'Running laboratory "xss-basic"...' in result.stdout

    assert "✔ Laboratory started successfully." in result.stdout


def test_lab_stop_displays_execution_report() -> None:
    # Arrange
    app = create_app(
        manifest_loader=FakeLabManifestLoader({}),
        validator=FakeLabValidator({}),
        lab_runner=FakeLabLifeCycle(
            run_reports={},
            stop_reports={
                "xss-basic": _create_stop_report(),
            },
        ),
    )

    # Act
    result = runner.invoke(
        app,
        [
            "lab",
            "stop",
            "xss-basic",
        ],
    )

    # Assert
    assert result.exit_code == 0

    assert 'Stopping laboratory "xss-basic"...' in result.stdout

    assert "✔ Laboratory stopped successfully." in result.stdout


def _create_logs_report() -> LabLogs:
    return LabLogs(
        lab_id="xss-basic",
        content="Sample log content for xss-basic laboratory.",
    )


def test_lab_logs_displays_execution_report() -> None:
    app = create_app(
        manifest_loader=FakeLabManifestLoader({}),
        validator=FakeLabValidator({}),
        lab_runner=FakeLabLifeCycle(
            run_reports={},
            logs_output={
                "xss-basic": LabLogs(
                    lab_id="xss-basic",
                    content="nginx\nphp\nmysql",
                ),
            },
        ),
    )

    result = runner.invoke(
        app,
        [
            "lab",
            "logs",
            "xss-basic",
        ],
    )

    assert result.exit_code == 0

    assert 'Showing logs for laboratory "xss-basic"...' in result.stdout

    assert "nginx\nphp\nmysql" in result.stdout
