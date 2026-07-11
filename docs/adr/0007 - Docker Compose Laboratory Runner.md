# ADR 0007 — Docker Compose Laboratory Runner

**Status:** Accepted

**Date:** July 2026

---

# Context

CyberLab introduces laboratory execution as a first-class capability.

The Application layer already defines the execution contract through `LabRunnerProtocol`, allowing the business workflow to remain independent from the underlying execution technology.

The project requires an initial execution backend capable of:

* starting laboratory environments;
* supporting multi-container laboratories;
* using reproducible infrastructure definitions;
* remaining replaceable in the future.

Docker Compose satisfies these requirements while remaining simple enough for local development and educational laboratories.

---

# Decision

CyberLab adopts Docker Compose as the initial laboratory execution backend.

The execution architecture is divided into two infrastructure components:

```text
LabRunnerProtocol
        │
        ▼
DockerComposeLabRunner
        │
        ▼
DockerComposeService
        │
        ▼
CommandRunnerProtocol
        │
        ▼
docker compose
```

Responsibilities are intentionally separated.

## DockerComposeLabRunner

Responsible for:

* adapting the `LabRunnerProtocol`;
* locating the laboratory Compose file;
* translating execution results into `LabExecutionReport`.

The runner does not know how Docker Compose commands are executed.

---

## DockerComposeService

Responsible for:

* constructing Docker Compose commands;
* invoking the `CommandRunnerProtocol`;
* returning `ProcessResult`.

The service contains all Docker Compose–specific behavior.

---

## CommandRunnerProtocol

Responsible for executing operating system commands.

Docker Compose remains only one possible consumer of this protocol.

---

# Rationale

This separation preserves the architectural boundaries established by Clean Architecture.

The Application layer remains completely unaware of:

* Docker;
* Docker Compose;
* subprocess execution;
* operating system details.

Replacing Docker Compose with another execution technology should require changes only inside the Infrastructure layer.

Examples include:

* Podman
* Kubernetes
* Remote runners
* Cloud execution services

---

# Consequences

## Positive

* Business rules remain infrastructure-independent.
* Execution technology is isolated.
* Components have a single responsibility.
* Docker Compose logic can evolve independently.
* Infrastructure can support additional lifecycle operations such as:

  * `down`
  * `logs`
  * `ps`
  * `restart`

without affecting the Application layer.

---

## Negative

The Infrastructure layer gains additional components.

This additional complexity is considered acceptable because it preserves long-term maintainability and extensibility.

---

# Alternatives Considered

## Execute Docker Compose directly from the Use Case

Rejected.

This would introduce infrastructure dependencies into the Application layer.

---

## Execute Docker Compose directly from the CLI

Rejected.

The CLI should remain responsible only for user interaction.

---

## Embed Docker Compose logic inside DockerComposeLabRunner

Rejected.

Separating command construction (`DockerComposeService`) from laboratory orchestration (`DockerComposeLabRunner`) results in clearer responsibilities and simplifies future extensions.

---

# Future Evolution

The current design allows additional execution backends to be introduced without modifying the Application layer.

Potential future implementations include:

* PodmanLabRunner
* KubernetesLabRunner
* RemoteLabRunner

All future runners are expected to implement the existing `LabRunnerProtocol`.
