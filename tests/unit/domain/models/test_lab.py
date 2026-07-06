import pytest

from cyberlab.domain.models.lab import Lab


def test_lab_stores_name() -> None:
    lab = Lab(name="xss-basic")

    assert lab.name == "xss-basic"


def test_lab_instances_with_same_name_are_equal() -> None:
    assert Lab("xss-basic") == Lab("xss-basic")


def test_lab_is_immutable() -> None:
    lab = Lab("xss-basic")

    with pytest.raises(AttributeError):
        lab.name = "new-name"  # type: ignore[misc]
