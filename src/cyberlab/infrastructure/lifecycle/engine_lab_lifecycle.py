"""Resolve the lifecycle adapter declared by a laboratory manifest."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import yaml

from cyberlab.application.interfaces.lab_lifecycle_protocol import LabLifeCycleProtocol
from cyberlab.domain.models.lab_execution_report import LabExecutionReport, LaboratoryStatus
from cyberlab.domain.models.lab_logs import LabLogs

LifecycleFactory = Callable[[str], LabLifeCycleProtocol]


class EngineLabLifecycle:
    """Delegate each operation to the engine selected in ``lab.yaml``."""

    def __init__(
        self,
        labs_root: Path,
        factories: Mapping[str, LifecycleFactory],
        *,
        default_engine: str = "docker",
    ) -> None:
        self._labs_root = labs_root
        self._factories = dict(factories)
        self._default_engine = default_engine

    def run(self, lab_id: str) -> LabExecutionReport:
        return self._lifecycle(lab_id).run(lab_id)

    def stop(self, lab_id: str) -> LabExecutionReport:
        return self._lifecycle(lab_id).stop(lab_id)

    def restart(self, lab_id: str) -> LabExecutionReport:
        return self._lifecycle(lab_id).restart(lab_id)

    def status(self, lab_id: str) -> LaboratoryStatus:
        return self._lifecycle(lab_id).status(lab_id)

    def logs(self, lab_id: str) -> LabLogs:
        return self._lifecycle(lab_id).logs(lab_id)

    def deploy(self, lab_id: str) -> str:
        manifest_path = self._labs_root / lab_id / "lab.yaml"
        return self._operation(lab_id, "deploy", str(manifest_path))

    def exec(self, lab_id: str, command: str) -> str:
        return self._operation(lab_id, "exec", lab_id, command)

    def console(self, lab_id: str, shell: str) -> str:
        return self._operation(lab_id, "console", lab_id, shell)

    def submit(self, lab_id: str, flag: str) -> bool:
        return self._operation(lab_id, "validate_flag", lab_id, flag)

    def proxy(self, lab_id: str) -> str | None:
        return self._operation(lab_id, "proxy", lab_id)

    def harden(self, lab_id: str) -> str:
        return self._operation(lab_id, "harden", lab_id)

    def setup_ctf(self, lab_id: str, target: str) -> str:
        return self._operation(lab_id, "setup_ctf", lab_id, target)

    def _lifecycle(self, lab_id: str) -> LabLifeCycleProtocol:
        engine = self._engine(lab_id)
        try:
            factory = self._factories[engine]
        except KeyError as error:
            available = ", ".join(sorted(self._factories))
            raise ValueError(
                f"Unsupported engine '{engine}' for laboratory '{lab_id}'. "
                f"Available engines: {available}."
            ) from error
        return factory(lab_id)

    def _operation(self, lab_id: str, name: str, *args: str) -> Any:
        lifecycle = self._lifecycle(lab_id)
        operation = type(lifecycle).__dict__.get(name)
        if not callable(operation):
            engine = self._engine(lab_id)
            raise NotImplementedError(
                f"Engine '{engine}' does not support the '{name}' operation "
                f"for laboratory '{lab_id}'."
            )
        return operation(lifecycle, *args)

    def _engine(self, lab_id: str) -> str:
        manifest_path = self._labs_root / lab_id / "lab.yaml"
        try:
            with manifest_path.open(encoding="utf-8") as manifest_file:
                manifest: Any = yaml.safe_load(manifest_file) or {}
        except FileNotFoundError as error:
            raise FileNotFoundError(f'Laboratory manifest not found: "{manifest_path}".') from error

        if not isinstance(manifest, dict):
            raise ValueError(f'Laboratory manifest must be a mapping: "{manifest_path}".')

        engine = manifest.get("engine", self._default_engine)
        if not isinstance(engine, str) or not engine.strip():
            raise ValueError(f'Laboratory engine must be a non-empty string: "{manifest_path}".')
        return engine.strip().lower()
