# CyberLab – Project Context

*Last updated after PR #006 (Laboratory Validation)*

---

# Project Overview

CyberLab is an open-source framework for building reproducible cybersecurity laboratories.

The project serves two complementary purposes:

* a practical platform for creating and running security labs;
* a reference implementation of modern Python software architecture.

The project follows:

* Clean Architecture
* Hexagonal Architecture
* SOLID
* Dependency Injection
* Test-Driven Development (TDD)
* Conventional Commits

Development is incremental and organized by Pull Requests.

Each PR introduces exactly one major capability.

---

# Development Workflow

Every feature follows the same lifecycle.

```text
Design Review

↓

RED

↓

GREEN

↓

REFACTOR

↓

Code Review

↓

Commit
```

No implementation begins before the Design Review.

Every commit must remain small, atomic and independently understandable.

---

# Architecture

```
CLI
│
├── Commands
├── Rendering
│
▼
Application
│
├── Use Cases
├── Interfaces (Protocols)
│
▼
Infrastructure
│
├── Filesystem
├── Process
├── Configuration
│
▼
Domain
│
├── Models
├── Reports
├── Value Objects
```

Dependencies always point toward the Domain.

The Domain never depends on any other layer.

---

# Layer Responsibilities

## Domain

Contains immutable business concepts.

Examples:

* Lab
* LabManifest
* CheckResult
* DoctorReport
* LabValidationReport

---

## Application

Contains:

* Use Cases
* Protocols

Every Use Case exposes exactly one public method:

```python
execute(...)
```

Application depends only on:

* Domain
* Protocols

---

## Infrastructure

Contains concrete implementations.

Examples:

* CommandRunner
* FilesystemLabRepository
* YamlLabManifestLoader
* FilesystemLabValidator

Infrastructure implements Application Protocols.

---

## CLI

Responsible only for:

* parsing arguments;
* composing dependencies;
* rendering output.

No business logic belongs in the CLI.

---

# Current Domain Models

Implemented:

* Lab
* LabManifest
* CheckResult
* ProcessResult
* DoctorReport
* LabValidationReport

All models are immutable whenever possible.

---

# Current Protocols

Application defines:

* CommandRunnerProtocol
* LabRepositoryProtocol
* LabManifestLoaderProtocol
* LabValidatorProtocol

Protocols define contracts only.

Protocols are not tested.

---

# Current Infrastructure

Implemented:

* CommandRunner
* FilesystemLabRepository
* YamlLabManifestLoader
* FilesystemLabValidator

All Infrastructure services receive dependencies through constructors.

No hardcoded paths.

---

# Current Use Cases

Implemented:

* VersionUseCase
* DoctorUseCase
* ListLabsUseCase
* LabInfoUseCase
* LabValidationUseCase

Each Use Case has one responsibility only.

---

# CLI Commands

Implemented:

```bash
uv run cyberlab version

uv run cyberlab doctor

uv run cyberlab lab list

uv run cyberlab lab info <lab-id>

uv run cyberlab lab validate <lab-id>
```

---

# Rendering

Shared rendering currently exists for:

* render_checks()

Doctor and Lab Validation reuse the same rendering function.

Future validation commands should reuse it as well.

---

# Fake Strategy

The project intentionally adopts Fakes instead of Mocks.

Implemented:

* FakeCommandRunner
* FakeLabRepository
* FakeLabManifestLoader
* FakeLabValidator

Every Fake:

* implements its Protocol;
* is fully in-memory;
* receives initial state via constructor;
* records requests;
* fails explicitly on unexpected input.

---

# Testing Strategy

AAA pattern.

```
Arrange

↓

Act

↓

Assert
```

Application tests always use Fakes.

Infrastructure tests verify external integrations.

CLI tests use:

```python
create_app(...)
```

with injected Fake dependencies.

No monkeypatch.

No mocks.

---

# Composition Root

Dependency construction is centralized in:

```python
create_app()
```

Production dependencies:

* CommandRunner
* FilesystemLabRepository
* YamlLabManifestLoader
* FilesystemLabValidator

Tests inject Fake implementations.

---

# Laboratory Structure

```
labs/
└── xss-basic/
    ├── lab.yaml
    ├── README.md
    └── compose.yaml
```

Current validation checks:

* lab.yaml
* README.md
* compose.yaml

---

# Documentation

Current documentation:

```
docs/
├── adr/
│   ├── 0001 - Project Conventions.md
│   ├── 0002 - Value Objects.md
│   ├── 0003 - Environment Doctor.md
│   ├── 0004 - Laboratory Discovery.md
│   ├── 0005 - Laboratory Metadata Model.md
│   └── 0006 - Validation Architecture.md
│
├── architecture/
│   ├── overview.md
│   ├── principles.md
│   └── testing.md
│
└── roadmap.md
```

README and CHANGELOG are synchronized at the end of every PR.

---

# Completed Pull Requests

## PR #001

Bootstrap

* project structure
* tooling
* Makefile
* Ruff
* MyPy
* Pytest

---

## PR #002

Version

* Version command
* VersionUseCase

---

## PR #003

Environment Doctor

* CheckResult
* DoctorReport
* CommandRunner
* DoctorUseCase

---

## PR #004

Laboratory Discovery

* Lab
* Repository Pattern
* ListLabsUseCase
* lab list

---

## PR #005

Laboratory Metadata

* LabManifest
* Manifest Loader
* LabInfoUseCase
* lab info

---

## PR #006

Laboratory Validation

* LabValidationReport
* LabValidatorProtocol
* FilesystemLabValidator
* FakeLabValidator
* LabValidationUseCase
* lab validate
* shared CLI rendering

---

# Roadmap

Completed:

* Bootstrap
* Version
* Doctor
* Laboratory Discovery
* Laboratory Metadata
* Laboratory Validation

Next planned PRs:

## PR #007

Laboratory Runner

Goal:

```bash
uv run cyberlab lab run <lab-id>
```

Initially without Docker orchestration.

Only the execution workflow and architecture.

---

## Future

* Docker Orchestration
* Template Engine
* Package Manager
* Scenario Engine
* Remote Catalog
* Plugin System

---

# Development Principles

Always preserve:

* Single Responsibility Principle
* Dependency Injection
* Dependency Inversion
* Immutable Domain Models
* Explicit Protocols
* Composition Root
* Small commits
* One responsibility per PR
* Fakes over Mocks
* YAGNI
* Rule of Three before extracting abstractions

Architecture consistency is preferred over introducing new patterns.

When proposing new features, reuse existing architectural conventions before creating new abstractions.
