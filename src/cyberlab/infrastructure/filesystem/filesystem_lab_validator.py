from __future__ import annotations

from pathlib import Path

from cyberlab.application.interfaces.lab_validator_protocol import (
    LabValidatorProtocol,
)
from cyberlab.domain.models.check_result import CheckResult
from cyberlab.domain.models.lab_validation_report import (
    LabValidationReport,
)

_REQUIRED_LAB_FILES = (
    "lab.yaml",
    "README.md",
    "compose.yaml",
)


class FilesystemLabValidator(LabValidatorProtocol):
    """Validate the filesystem structure of a laboratory."""

    def __init__(
        self,
        labs_root: Path,
    ) -> None:
        self._labs_root = labs_root

    def validate(
        self,
        lab_id: str,
    ) -> LabValidationReport:
        """Validate a laboratory."""

        lab_path = self._labs_root / lab_id

        checks = tuple(
            self._check_file(
                lab_path / filename,
                filename,
            )
            for filename in _REQUIRED_LAB_FILES
        )

        return LabValidationReport(
            checks=checks,
        )

    def _check_file(
        self,
        path: Path,
        name: str,
    ) -> CheckResult:
        """Validate the existence of a required file."""

        exists = path.is_file()

        return CheckResult(
            name=name,
            success=exists,
            message="Found" if exists else "Missing",
        )
