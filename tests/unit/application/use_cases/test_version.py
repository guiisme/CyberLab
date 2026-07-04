from cyberlab.application.use_cases.version import get_version


def test_get_version_returns_string() -> None:
    result = get_version()

    assert isinstance(result, str)


def test_get_version_is_not_empty() -> None:
    result = get_version()

    assert result
