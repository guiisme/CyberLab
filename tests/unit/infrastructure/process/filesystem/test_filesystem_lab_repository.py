from pathlib import Path

from cyberlab.domain.models.lab import Lab
from cyberlab.infrastructure.filesystem.filesystem_lab_repository import (
    FilesystemLabRepository,
)
from tests.fakes.fake_lab_repository import FakeLabRepository


def test_list_returns_labs_from_directories(tmp_path: Path) -> None:
    (tmp_path / "xss-basic").mkdir()
    (tmp_path / "sqli-basic").mkdir()

    repository = FilesystemLabRepository(tmp_path)

    assert repository.list() == (
        Lab("sqli-basic"),
        Lab("xss-basic"),
    )


def test_list_ignores_files(tmp_path: Path) -> None:
    (tmp_path / "xss-basic").mkdir()

    (tmp_path / "README.md").write_text("example")

    repository = FilesystemLabRepository(tmp_path)

    assert repository.list() == (Lab("xss-basic"),)


def test_list_returns_empty_tuple_when_no_labs_exist(
    tmp_path: Path,
) -> None:
    repository = FilesystemLabRepository(tmp_path)

    assert repository.list() == ()


def test_list_returns_configured_labs() -> None:
    repository = FakeLabRepository(
        labs=(
            Lab("xss-basic"),
            Lab("sqli-basic"),
        )
    )

    assert repository.list() == (
        Lab("xss-basic"),
        Lab("sqli-basic"),
    )


def test_list_returns_empty_tuple_by_default() -> None:
    repository = FakeLabRepository()

    assert repository.list() == ()
