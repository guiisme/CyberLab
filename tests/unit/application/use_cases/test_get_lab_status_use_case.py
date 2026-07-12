from cyberlab.application.use_cases.get_lab_status_use_case import GetLabStatusUseCase
from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
    LaboratoryState,
    LaboratoryStatus,
)
from tests.fakes.fake_lab_lifecycle import FakeLabLifeCycle


def test_returns_running_status() -> None:
    status = FakeLabLifeCycle(
        {
            "xss-basic": LabExecutionReport(
                "xss-basic",
                True,
                "running",
            ),
        },
        status_to_return=LaboratoryStatus(
            LaboratoryState.RUNNING,
        ),
    )

    use_case = GetLabStatusUseCase(status)

    result = use_case.execute("xss-basic")

    assert result.is_running


def test_returns_stopped_status() -> None:
    status = FakeLabLifeCycle(
        {
            "xss-basic": LabExecutionReport(
                "xss-basic",
                False,
                "stopped",
            ),
        }
    )

    status.status_to_return = LaboratoryStatus(
        LaboratoryState.STOPPED,
    )

    use_case = GetLabStatusUseCase(status)

    result = use_case.execute("xss-basic")

    assert result.is_stopped


def test_passes_lab_id_to_status_service() -> None:
    status = FakeLabLifeCycle({})

    use_case = GetLabStatusUseCase(status)

    use_case.execute("xss-basic")

    assert status.received_lab_id == "xss-basic"
