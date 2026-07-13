from __future__ import annotations

from cyberlab.application.use_cases.lab_create_use_case import LabCreateUseCase
from tests.fakes.fake_lab_scaffolding import (
    FakeLabScaffolding,
)


def test_create_lab_executes_scaffolding() -> None:
    scaffolding = FakeLabScaffolding()

    use_case = LabCreateUseCase(
        scaffolding,
    )

    use_case.execute(
        lab_id="jwt-basic",
    )

    assert scaffolding.created_labs == [
        (
            "jwt-basic",
            "default",
        ),
    ]
