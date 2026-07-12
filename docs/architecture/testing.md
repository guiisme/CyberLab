# CyberLab Testing Strategy

## Purpose

Testing is a first-class architectural concern in CyberLab.

The project is designed to maximize confidence while keeping tests fast, deterministic and easy to understand.

CyberLab follows Test-Driven Development (TDD) whenever practical.

Tests are organized to validate observable behavior rather than implementation details.

---

# Testing Principles

The testing strategy is guided by the following principles:

- Test behavior instead of implementation.
- Prefer Fakes over mocks.
- Keep tests deterministic.
- Test one responsibility at a time.
- Isolate architectural layers.
- Avoid infrastructure dependencies in unit tests.
- Every feature should be introduced together with its tests.

Testing is considered part of the implementation, not an afterthought.

---

# Testing Pyramid

CyberLab prioritizes fast feedback.

```text
            Manual Testing
                  ▲
                  │
         Integration Tests
                  ▲
                  │
            Unit Tests
```

Most tests should be unit tests.

Integration tests validate interactions between components.

Manual testing is reserved for validating the complete user experience.

---

# Layer Isolation

Each architectural layer is tested independently.

```text
CLI

↓

Application

↓

Domain

↓

Infrastructure
```

Every layer owns its own test suite.

Changes in one layer should have minimal impact on the others.

---

# Domain Testing

The Domain layer contains pure business models.

Tests verify:

- immutable models;
- value objects;
- validation rules;
- domain behavior.

Domain tests never depend on infrastructure.

---

# Application Testing

Application tests focus on Use Cases.

Use Cases are tested through Protocols using Fakes.

Example:

```text
LabRunUseCase

↓

FakeLabLifeCycle
```

Application tests verify:

- orchestration;
- delegation;
- returned results;
- propagated errors.

Application tests never execute Docker, filesystem operations or external commands.

---

# Protocol Testing

Protocols define architectural contracts.

They are validated indirectly through their implementations and Fakes.

Each Protocol has a canonical Fake implementation.

Examples:

- FakeLabLifeCycle
- FakeCommandRunner
- FakeLabManifestLoader
- FakeLabValidator

Fakes simulate behavior while remaining deterministic and lightweight.

---

# Infrastructure Testing

Infrastructure tests verify concrete implementations.

Examples include:

- DockerComposeService
- DockerComposeLabRunner
- Filesystem repositories
- YAML manifest loading
- Command execution

Infrastructure tests validate:

- command generation;
- filesystem interaction;
- adapter behavior;
- protocol implementation.

Infrastructure tests avoid depending on external services whenever possible.

---

# CLI Testing

CLI tests validate the user interface.

They verify:

- command registration;
- argument parsing;
- terminal output;
- integration with Use Cases.

CLI tests never validate Docker commands directly.

Those behaviors belong to the Infrastructure layer.

---

# Lifecycle Testing

Laboratory lifecycle operations are tested independently.

Current lifecycle operations include:

- Run Laboratory
- Stop Laboratory

Each lifecycle operation is validated across the architecture:

```text
CLI

↓

Application

↓

Protocol

↓

Infrastructure
```

Each layer has dedicated tests for its own responsibility.

---

# Fake Objects

CyberLab prefers Fakes over mocks.

Fakes provide deterministic behavior while preserving architectural contracts.

Each Protocol has a single canonical Fake implementation.

Examples:

```text
LabLifeCycleProtocol

↓

FakeLabLifeCycle

CommandRunnerProtocol

↓

FakeCommandRunner
```

As Protocols evolve, their corresponding Fakes evolve together.

This keeps the test suite consistent and minimizes duplication.

---

# Test Organization

Tests mirror the project architecture.

```text
tests/

├── unit/
│   ├── application/
│   ├── cli/
│   ├── domain/
│   ├── infrastructure/
│   └── fakes/
```

This structure makes it easy to locate tests related to each architectural layer.

---

# Verification Pipeline

Every commit must pass the complete verification pipeline.

```bash
make format

make verify
```

The verification pipeline includes:

- Ruff
- MyPy
- Pytest

A commit is considered complete only when the entire pipeline succeeds.

---

# Long-Term Strategy

As CyberLab evolves, new capabilities should follow the same testing approach.

Every new feature should introduce tests for:

- Infrastructure
- Application
- CLI

Documentation should evolve together with the implementation.

This strategy keeps the project maintainable while allowing new capabilities to be introduced with confidence.
