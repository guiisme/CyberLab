"""Executable dependency rules for CyberLab's hexagonal architecture."""

from __future__ import annotations

import ast
from collections.abc import Iterator
from pathlib import Path

import pytest

SOURCE_ROOT = Path("src/cyberlab")


def _imports(path: Path) -> Iterator[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=path)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from (alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module


def _module(path: Path) -> str:
    return ".".join(path.relative_to("src").with_suffix("").parts)


@pytest.mark.parametrize(
    ("layer", "forbidden"),
    [
        ("domain", ("cyberlab.application", "cyberlab.cli", "cyberlab.infrastructure")),
        ("application", ("cyberlab.cli", "cyberlab.infrastructure")),
        ("infrastructure", ("cyberlab.cli",)),
    ],
)
def test_inner_layers_do_not_depend_on_outer_layers(layer: str, forbidden: tuple[str, ...]) -> None:
    for path in (SOURCE_ROOT / layer).rglob("*.py"):
        invalid = [
            imported
            for imported in _imports(path)
            if any(imported == prefix or imported.startswith(f"{prefix}.") for prefix in forbidden)
        ]
        assert not invalid, f"{_module(path)} imports outer-layer modules: {invalid}"


def test_only_the_composition_root_may_import_infrastructure_from_the_cli() -> None:
    for path in (SOURCE_ROOT / "cli").rglob("*.py"):
        if path == SOURCE_ROOT / "cli/app.py":
            continue

        invalid = [
            imported
            for imported in _imports(path)
            if imported == "cyberlab.infrastructure"
            or imported.startswith("cyberlab.infrastructure.")
        ]
        assert not invalid, f"{_module(path)} bypasses the composition root: {invalid}"
