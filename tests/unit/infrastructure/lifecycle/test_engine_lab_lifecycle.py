from pathlib import Path

import pytest

from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
    LaboratoryState,
    LaboratoryStatus,
)
from cyberlab.domain.models.lab_logs import LabLogs
from cyberlab.infrastructure.lifecycle.engine_lab_lifecycle import EngineLabLifecycle


class SpyLifecycle:
    def __init__(self, label: str) -> None:
        self.label = label
        self.calls: list[tuple[str, str]] = []

    def run(self, lab_id: str) -> LabExecutionReport:
        self.calls.append(("run", lab_id))
        return LabExecutionReport(lab_id=lab_id, success=True, message=self.label)

    def stop(self, lab_id: str) -> LabExecutionReport:
        self.calls.append(("stop", lab_id))
        return LabExecutionReport(lab_id=lab_id, success=True, message=self.label)

    def restart(self, lab_id: str) -> LabExecutionReport:
        self.calls.append(("restart", lab_id))
        return LabExecutionReport(lab_id=lab_id, success=True, message=self.label)

    def status(self, lab_id: str) -> LaboratoryStatus:
        self.calls.append(("status", lab_id))
        return LaboratoryStatus(LaboratoryState.RUNNING)

    def logs(self, lab_id: str) -> LabLogs:
        self.calls.append(("logs", lab_id))
        return LabLogs(lab_id=lab_id, content=self.label)


class OperationsSpy(SpyLifecycle):
    def deploy(self, manifest_path: str) -> str:
        self.calls.append(("deploy", manifest_path))
        return "deployed"

    def exec(self, lab_id: str, command: str) -> str:
        self.calls.append(("exec", f"{lab_id}:{command}"))
        return "executed"

    def console(self, lab_id: str, shell: str) -> str:
        self.calls.append(("console", f"{lab_id}:{shell}"))
        return "closed"

    def validate_flag(self, lab_id: str, flag: str) -> bool:
        self.calls.append(("validate_flag", f"{lab_id}:{flag}"))
        return True

    def proxy(self, lab_id: str) -> str:
        self.calls.append(("proxy", lab_id))
        return "http://127.0.0.1:8080"


def write_manifest(labs_root: Path, lab_id: str, contents: str) -> None:
    manifest = labs_root / lab_id / "lab.yaml"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(contents, encoding="utf-8")


def test_delegates_to_manifest_engine(tmp_path: Path) -> None:
    write_manifest(tmp_path, "api", "engine: k8s\n")
    selected: list[str] = []
    lifecycle = SpyLifecycle("k8s")
    resolver = EngineLabLifecycle(
        tmp_path,
        {"k8s": lambda lab_id: selected.append(lab_id) or lifecycle},
    )

    report = resolver.run("api")

    assert report.message == "k8s"
    assert selected == ["api"]
    assert lifecycle.calls == [("run", "api")]


def test_uses_default_engine_when_manifest_omits_engine(tmp_path: Path) -> None:
    write_manifest(tmp_path, "web", "name: web\n")
    lifecycle = SpyLifecycle("docker")
    resolver = EngineLabLifecycle(tmp_path, {"docker": lambda _: lifecycle})

    assert resolver.logs("web").content == "docker"


def test_rejects_unsupported_engine(tmp_path: Path) -> None:
    write_manifest(tmp_path, "api", "engine: nomad\n")
    resolver = EngineLabLifecycle(tmp_path, {"docker": lambda _: SpyLifecycle("docker")})

    with pytest.raises(ValueError, match="Unsupported engine 'nomad'"):
        resolver.run("api")


def test_delegates_engine_specific_operations(tmp_path: Path) -> None:
    write_manifest(tmp_path, "api", "engine: k8s\n")
    lifecycle = OperationsSpy("k8s")
    resolver = EngineLabLifecycle(tmp_path, {"k8s": lambda _: lifecycle})

    assert resolver.deploy("api") == "deployed"
    assert resolver.exec("api", "id") == "executed"
    assert resolver.console("api", "/bin/bash") == "closed"
    assert resolver.submit("api", "flag") is True
    assert resolver.proxy("api") == "http://127.0.0.1:8080"
    assert lifecycle.calls == [
        ("deploy", str(tmp_path / "api" / "lab.yaml")),
        ("exec", "api:id"),
        ("console", "api:/bin/bash"),
        ("validate_flag", "api:flag"),
        ("proxy", "api"),
    ]


def test_rejects_an_unsupported_engine_operation(tmp_path: Path) -> None:
    write_manifest(tmp_path, "web", "engine: docker\n")
    resolver = EngineLabLifecycle(tmp_path, {"docker": lambda _: SpyLifecycle("docker")})

    with pytest.raises(NotImplementedError, match="does not support the 'harden' operation"):
        resolver.harden("web")
