from cyberlab.application.use_cases.list_labs_use_case import (
    ListLabsUseCase,
)
from cyberlab.domain.models.lab import Lab
from tests.fakes.fake_lab_repository import FakeLabRepository


def test_execute_returns_available_labs() -> None:
    repository = FakeLabRepository(
        labs=(
            Lab("xss-basic"),
            Lab("sqli-basic"),
        )
    )

    use_case = ListLabsUseCase(repository)

    assert use_case.execute() == (
        Lab("xss-basic"),
        Lab("sqli-basic"),
    )


def test_execute_returns_empty_tuple_when_no_labs_exist() -> None:
    repository = FakeLabRepository()

    use_case = ListLabsUseCase(repository)

    assert use_case.execute() == ()
