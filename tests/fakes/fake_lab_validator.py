from __future__ import annotations

from cyberlab.application.interfaces.lab_validator_protocol import (
    LabValidatorProtocol,
)
from cyberlab.domain.models.lab_validation_report import (
    LabValidationReport,
)


class FakeLabValidator(LabValidatorProtocol):
    """In-memory implementation of LabValidatorProtocol."""

    def __init__(
        self,
        reports: dict[str, LabValidationReport],
    ) -> None:
        self._reports = reports
        self.requested_lab_ids: list[str] = []

    def validate(
        self,
        lab_id: str,
    ) -> LabValidationReport:
        """Validate a laboratory."""

        self.requested_lab_ids.append(lab_id)

        if lab_id not in self._reports:
            raise AssertionError(f"Unexpected lab id: {lab_id}")

        return self._reports[lab_id]
