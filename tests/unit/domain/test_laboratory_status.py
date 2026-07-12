from cyberlab.domain.models.laboratory_state import LaboratoryState
from cyberlab.domain.models.laboratory_status import LaboratoryStatus


def test_running_status() -> None:
    status = LaboratoryStatus(LaboratoryState.RUNNING)

    assert status.is_running
    assert not status.is_stopped


def test_stopped_status() -> None:
    status = LaboratoryStatus(LaboratoryState.STOPPED)

    assert status.is_stopped
    assert not status.is_running


def test_status_keeps_state() -> None:
    status = LaboratoryStatus(LaboratoryState.RUNNING)

    assert status.state is LaboratoryState.RUNNING
