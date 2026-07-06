from cyberlab.application.use_cases.version_use_case import shared_get_version as get_version
from cyberlab.shared.version import (
    get_version as shared_get_version,
)


def test_get_version_returns_shared_version() -> None:
    """The use case should delegate version retrieval."""

    assert get_version() == shared_get_version()
