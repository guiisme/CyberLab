from cyberlab.application.interfaces.lab_status_protocol import (
    LabStatusProtocol,
)
from cyberlab.domain.models.laboratory_state import LaboratoryState
from cyberlab.domain.models.laboratory_status import LaboratoryStatus


class FakeLabStatus(LabStatusProtocol):
    def __init__(self) -> None:
        self.status_to_return = LaboratoryStatus(
            LaboratoryState.STOPPED,
        )
        self.received_lab_id: str | None = None

    def status(
        self,
        lab_id: str,
    ) -> LaboratoryStatus:
        self.received_lab_id = lab_id
        return self.status_to_return
