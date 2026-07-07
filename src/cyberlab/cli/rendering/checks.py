from __future__ import annotations

import typer

from cyberlab.domain.models.check_result import CheckResult


def render_checks(
    checks: tuple[CheckResult, ...],
) -> None:
    """Render a collection of check results."""

    for check in checks:
        icon = "✔" if check.success else "✘"
        typer.echo(f"{icon} {check.name}")
