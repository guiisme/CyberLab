from __future__ import annotations

from cyberlab.application.interfaces.lab_validator_protocol import (
    LabValidatorProtocol,
)
from cyberlab.domain.models.lab_validation_report import (
    LabValidationReport,
)


class LabValidationUseCase:
    """Validate a CyberLab laboratory."""

    def __init__(
        self,
        validator: LabValidatorProtocol,
    ) -> None:
        self._validator = validator

    def execute(
        self,
        lab_id: str,
    ) -> LabValidationReport:
        """Validate a laboratory."""

        return self._validator.validate(lab_id)
