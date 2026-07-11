# CyberLab — Project Context

*Last updated: July 2026*

---

# Project Overview

CyberLab is an open-source framework for building, validating and executing reproducible cybersecurity laboratories.

The project follows:

* Clean Architecture
* Hexagonal Architecture
* Test-Driven Development (TDD)
* Protocol-Oriented Design
* Constructor Dependency Injection

The primary objective is to isolate business rules from infrastructure, allowing execution technologies to evolve without impacting the Application or Domain layers.

---

# Current Architecture

```text
CLI
 │
 ▼
Application (Use Cases)
 │
 ▼
Protocols
 ▲
 │
Infrastructure
 │
 ▼
External Systems
```

All dependencies point toward the Application layer.

---

# Current Project Structure

```text
src/
└── cyberlab/
    ├── application/
    │   ├── interfaces/
    │   └── use_cases/
    │
    ├── cli/
    │   ├── app.py
    │   ├── commands/
    │   └── rendering/
    │
    ├── domain/
    │   └── models/
    │
    ├── infrastructure/
    │   ├── docker/
    │   ├── filesystem/
    │   ├── process/
    │   └── runner/
    │
    └── shared/
```

---

# Current Features

Implemented:

* version
* doctor
* laboratory discovery
* laboratory metadata
* laboratory validation
* laboratory execution
* Docker Compose integration

---

# Laboratory Execution

Laboratories are executed through Docker Compose.

Execution flow:

```text
CLI

↓

LabRunUseCase

↓

LabRunnerProtocol

↓

DockerComposeLabRunner

↓

DockerComposeService

↓

CommandRunnerProtocol

↓

docker compose
```

Business rules remain completely independent from Docker.

---

# Infrastructure Components

Filesystem:

* FilesystemLabRepository
* FilesystemLabValidator
* YamlLabManifestLoader

Process:

* CommandRunner

Docker:

* DockerComposeService
* DockerComposeLabRunner

---

# Current Laboratory

```
labs/
└── xss-basic/
    ├── lab.yaml
    ├── compose.yaml
    └── README.md
```

The first executable laboratory is available through:

```bash
uv run cyberlab lab run xss-basic
```

---

# CLI Commands

Environment:

```bash
uv run cyberlab doctor
```

Version:

```bash
uv run cyberlab version
```

Discovery:

```bash
uv run cyberlab lab list
```

Metadata:

```bash
uv run cyberlab lab info xss-basic
```

Validation:

```bash
uv run cyberlab lab validate xss-basic
```

Execution:

```bash
uv run cyberlab lab run xss-basic
```

---

# Testing Strategy

Project follows:

RED

↓

GREEN

↓

REFACTOR

Testing pyramid:

* Unit Tests
* Integration Tests
* Acceptance Tests

Fakes are preferred over mocks.

---

# Architectural Rules

The project follows several mandatory rules.

## Application

Application never imports Infrastructure.

## Domain

Domain never depends on any external technology.

## Infrastructure

Infrastructure implements Protocols defined by the Application layer.

## CLI

CLI contains no business logic.

## Composition Root

Infrastructure implementations are created only inside:

```
cyberlab.cli.app.create_app()
```

---

# Current Protocols

* CommandRunnerProtocol
* LabRepositoryProtocol
* LabManifestLoaderProtocol
* LabValidatorProtocol
* LabRunnerProtocol

---

# Current Pull Requests

Completed

* PR #001 — Project Bootstrap
* PR #002 — Version Command
* PR #003 — Environment Doctor
* PR #004 — Laboratory Discovery
* PR #005 — Laboratory Metadata
* PR #006 — Laboratory Validation
* PR #007 — Laboratory Runner Abstraction
* PR #008 — CLI Modularization
* PR #009 — Docker Compose Runner

---

# Development Workflow

Every feature follows:

1. Design Review
2. RED
3. GREEN
4. REFACTOR
5. Documentation Update
6. Pull Request

Each commit should remain small, reviewable and independently testable.

---

# Next Planned Pull Request

## PR #010 — Laboratory Lifecycle

Initial scope:

* `lab stop`
* `lab status`
* `lab logs`

Future evolution:

* restart
* shell
* destroy

The existing `DockerComposeService` should be extended to support:

* `down`
* `ps`
* `logs`

without modifying the Application layer.

---

# Long-Term Roadmap

Future execution backends:

* Podman
* Kubernetes
* Remote Runner

Future laboratory capabilities:

* Multi-container laboratories
* Environment snapshots
* Automatic cleanup
* Marketplace
* Laboratory templates

The current architecture was intentionally designed so these capabilities can be added by introducing new Infrastructure implementations while preserving the existing Application layer.
