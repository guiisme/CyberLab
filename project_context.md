# PROJECT_CONTEXT.md

# CyberLab — Project Context

> This document provides the architectural context, engineering principles, conventions and current project status. It is intended to quickly onboard new contributors (human or AI) and preserve design decisions across development sessions.

---

# Project Vision

CyberLab is a Python framework for building reproducible cybersecurity laboratories.

The project has two equally important goals:

* provide a practical tool for creating security labs;
* serve as a reference implementation of modern software engineering practices.

The project values code quality as much as functionality.

---

# Engineering Principles

The project follows these principles.

## Architecture First

Architecture decisions are made before implementation.

Every feature starts with a Design Review.

---

## Small Commits

Each commit introduces exactly one concept.

Avoid mixing architecture, business logic and CLI in the same commit.

---

## Test Driven Development

Every feature follows:

1. Design Review
2. RED
3. GREEN
4. REFACTOR
5. Code Review
6. Commit

---

## Simplicity First

Prefer:

* simple code
* explicit code
* readable code

Avoid abstractions before they become necessary (YAGNI).

---

## Dependency Injection

Dependencies are injected through constructors.

Avoid creating dependencies inside business logic.

---

## Prefer Fakes over Mocks

Tests should use in-memory implementations whenever possible.

Avoid:

* monkeypatch
* unittest.mock
* patch

Prefer deterministic fake implementations.

---

# Official Architecture

```text
CLI
│
▼
Application (Use Cases)
│
▼
Application Interfaces (Protocols)
▲
│
Infrastructure (Implementations)
│
▼
Domain
```

Dependency rules:

* Domain depends on nobody.
* Application depends only on Domain and Protocols.
* Infrastructure implements Protocols.
* CLI contains no business logic.

This architecture is considered frozen for the v0.x series.

---

# Layer Responsibilities

## Domain

Represents business concepts.

Contains:

* Entities
* Value Objects
* Reports

Domain models are immutable whenever possible.

```python
@dataclass(frozen=True, slots=True)
```

---

## Application

Coordinates business logic.

Contains:

* Use Cases
* Interfaces (Protocols)

Every Use Case exposes exactly one public method:

```python
execute()
```

---

## Infrastructure

Implements external integrations.

Examples:

* subprocess
* filesystem
* docker
* configuration

Infrastructure never contains business rules.

---

## CLI

Responsible only for:

* input
* output
* rendering

CLI never makes business decisions.

---

# Use Case Convention

Every use case follows:

```python
class SomeUseCase:

    def __init__(...)

    def execute(...)
```

Only `execute()` is public.

Helper methods remain private.

---

# Reports

Application never returns:

* dict
* tuple
* list

Application returns Domain Reports.

Examples:

* DoctorReport
* PackageReport
* LabReport

Reports aggregate domain information and expose derived properties.

---

# Testing Strategy

Tests follow Arrange → Act → Assert.

Each layer tests only its own responsibility.

Domain

* business rules

Infrastructure

* integrations

Application

* orchestration using Fakes

CLI

* command behavior

---

# Fake Implementations

Shared test doubles live under:

```text
tests/
└── fakes/
```

Example:

* FakeCommandRunner

Requirements:

* deterministic
* in-memory
* implements the production Protocol
* records executed operations when useful
* fails on unexpected behavior

---

# Git Workflow

Every feature follows:

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

Conventional Commits are mandatory.

---

# Definition of Ready

Before implementation:

* problem understood
* architecture approved
* public contract defined
* tests planned

---

# Definition of Done

Before merging:

```bash
make format
make verify
git status
git show --stat HEAD
```

Everything must be green.

---

# Current Architecture

Domain

* CheckResult
* ProcessResult
* DoctorReport

Application

* CommandRunnerProtocol
* DoctorUseCase

Infrastructure

* CommandRunner

Tests

* FakeCommandRunner

CLI

* Version command
* Doctor command (in progress)

---

# Project Roadmap

## Completed

Sprint 0

PR #001

Project bootstrap

PR #002

Version Provider

Version Use Case

Version CLI

PR #003 (almost complete)

CheckResult

ProcessResult

CommandRunner

CommandRunnerProtocol

DoctorReport

FakeCommandRunner

DoctorUseCase

Doctor CLI (final step)

---

# Engineering Philosophy

The project intentionally prefers:

* readability over cleverness
* explicitness over magic
* composition over inheritance
* protocols over concrete dependencies
* dependency injection over coupling
* immutable domain models
* incremental evolution

---

# Long-Term Goal

By v1.0, every new feature should follow the exact same implementation pattern:

1. Domain model
2. Protocol (if required)
3. Fake implementation
4. Unit tests
5. Use Case
6. Infrastructure implementation
7. CLI integration

No architectural redesign should be necessary for ordinary feature development.

---

# Notes for Future Sessions

Before implementing new functionality:

* review this document;
* follow the existing architecture;
* avoid introducing new patterns without a clear need;
* preserve consistency across the project.

Architecture changes should be exceptional and documented through ADRs.
