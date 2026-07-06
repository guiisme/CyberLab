from __future__ import annotations

from typing import Protocol

from cyberlab.domain.models.lab_validation_report import (
    LabValidationReport,
)


class LabValidatorProtocol(Protocol):
    """Validate a CyberLab laboratory."""

    def validate(
        self,
        lab_id: str,
    ) -> LabValidationReport:
        """Validate a laboratory."""
        ...
