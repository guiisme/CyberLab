# CyberLab Architecture Principles

## Purpose

This document defines the architectural principles that guide the evolution of CyberLab.

These principles are intended to remain stable over time, regardless of infrastructure choices or implementation details.

---

# 1. Clean Architecture

Business rules must remain independent from infrastructure.

Infrastructure may evolve without requiring changes to the Domain or Application layers.

Dependencies always point inward.

---

# 2. Hexagonal Architecture

External technologies communicate with the application exclusively through well-defined interfaces (Protocols).

The Application layer defines the contracts.

Infrastructure provides the implementations.

---

# 3. Dependency Inversion

High-level policies never depend on low-level implementations.

Examples include:

* LabRepositoryProtocol
* LabManifestLoaderProtocol
* LabValidatorProtocol
* LabRunnerProtocol
* CommandRunnerProtocol

Concrete implementations belong exclusively to the Infrastructure layer.

---

# 4. Composition Root

Object creation is centralized in a single location.

Currently this responsibility belongs to:

```text id="x0d4qv"
cyberlab.cli.app.create_app()
```

Business logic must never instantiate infrastructure implementations directly.

---

# 5. Single Responsibility

Each component should have a single, clearly defined responsibility.

Examples:

* DockerComposeService executes Docker Compose commands.
* DockerComposeLabRunner adapts laboratory execution to Docker Compose.
* FilesystemLabRepository discovers available laboratories.
* YamlLabManifestLoader loads laboratory metadata.

---

# 6. Constructor Dependency Injection

Dependencies are supplied through constructors.

Global state and service locators are intentionally avoided.

---

# 7. Protocol-Oriented Design

Protocols define application requirements.

Infrastructure implements those requirements.

Protocols belong to the Application layer because they describe what the application needs, not how those needs are fulfilled.

---

# 8. Infrastructure Isolation

Infrastructure contains all technology-specific implementations.

Examples include:

* filesystem access;
* YAML parsing;
* process execution;
* Docker Compose integration.

Business rules remain unaware of implementation details.

---

# 9. Laboratory Execution

Laboratory execution follows the same architectural boundaries as every other feature.

```text id="udg0vb"
LabRunUseCase
        │
        ▼
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
Docker Compose
```

The Application layer defines the execution contract through `LabRunnerProtocol`.

The Infrastructure layer provides the execution mechanism.

Replacing Docker Compose with another technology should require changes only inside the Infrastructure layer.

---

# 10. Testability

Every architectural decision should improve testability.

The project follows these practices:

* Test-Driven Development (TDD)
* deterministic unit tests
* constructor injection
* Protocol-based boundaries
* Fakes preferred over mocks

External systems should be isolated whenever practical.

---

# 11. Incremental Evolution

The project evolves through small, reviewable Pull Requests.

Each Pull Request should:

* implement a single architectural concern;
* preserve backward compatibility whenever practical;
* keep the project in a releasable state;
* update documentation when architectural decisions change.

---

# 12. Documentation as Architecture

Architecture documentation is treated as part of the system.

Whenever an architectural decision changes, the corresponding documentation should be updated together with the implementation.

The documentation is expected to evolve continuously alongside the codebase.
