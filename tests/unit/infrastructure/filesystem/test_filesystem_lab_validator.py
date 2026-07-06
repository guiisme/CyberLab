from __future__ import annotations

from pathlib import Path

from cyberlab.domain.models.check_result import CheckResult
from cyberlab.infrastructure.filesystem.filesystem_lab_validator import (
    FilesystemLabValidator,
)


def _create_lab_structure(root: Path) -> None:
    lab = root / "xss-basic"
    lab.mkdir()

    (lab / "lab.yaml").write_text("", encoding="utf-8")
    (lab / "README.md").write_text("", encoding="utf-8")
    (lab / "compose.yaml").write_text("", encoding="utf-8")


def test_validate_returns_success_when_all_required_files_exist(
    tmp_path: Path,
) -> None:
    # Arrange
    _create_lab_structure(tmp_path)

    validator = FilesystemLabValidator(tmp_path)

    # Act
    report = validator.validate("xss-basic")

    # Assert
    assert report.success is True
    assert report.total_checks == 3
    assert report.successful_checks == 3
    assert report.failed_checks == 0


def test_validate_returns_failure_when_required_file_is_missing(
    tmp_path: Path,
) -> None:
    # Arrange
    lab = tmp_path / "xss-basic"
    lab.mkdir()

    (lab / "lab.yaml").write_text("", encoding="utf-8")
    (lab / "compose.yaml").write_text("", encoding="utf-8")

    validator = FilesystemLabValidator(tmp_path)

    # Act
    report = validator.validate("xss-basic")

    # Assert
    assert report.success is False
    assert report.failed_checks == 1

    assert (
        CheckResult(
            name="README.md",
            success=False,
            message="Missing",
        )
        in report.checks
    )


def test_validate_returns_failure_when_lab_directory_does_not_exist(
    tmp_path: Path,
) -> None:
    # Arrange
    validator = FilesystemLabValidator(tmp_path)

    # Act
    report = validator.validate("unknown")

    # Assert
    assert report.success is False
    assert report.total_checks == 3
    assert report.failed_checks == 3
