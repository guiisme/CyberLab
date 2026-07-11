# CyberLab Testing Strategy

## Purpose

Testing is a fundamental architectural concern in CyberLab.

The project follows **Test-Driven Development (TDD)** and treats automated tests as the primary mechanism for validating business behavior, protecting architectural boundaries and enabling safe refactoring.

The goal is to ensure that every layer can evolve independently while preserving correctness.

---

# Testing Philosophy

CyberLab follows these principles:

* Test behavior rather than implementation.
* Keep tests deterministic.
* Prefer Fakes over mocks.
* Isolate infrastructure whenever possible.
* Keep unit tests fast.
* Build confidence through layered testing.

Tests should provide confidence without coupling themselves to implementation details.

---

# Testing Pyramid

```text id="l7d67r"
                Acceptance Tests
                       ▲
                       │
             Integration Tests
                       ▲
                       │
                 Unit Tests
```

Each layer has a different responsibility.

---

# Unit Tests

Unit tests validate a single component in isolation.

Examples include:

* Domain models
* Value objects
* Use cases
* Infrastructure adapters
* CLI command registration

Unit tests should never require external systems.

Dependencies must be replaced by Fakes whenever possible.

---

# Integration Tests

Integration tests verify collaboration between multiple components.

Typical examples include:

* Filesystem repositories
* YAML manifest loading
* Docker Compose services
* Process execution

Integration tests may exercise real implementations while still avoiding unnecessary external dependencies.

---

# Acceptance Tests

Acceptance tests validate complete user workflows.

Examples include:

```bash id="u5uxdz"
uv run cyberlab version

uv run cyberlab doctor

uv run cyberlab lab list

uv run cyberlab lab info xss-basic

uv run cyberlab lab validate xss-basic

uv run cyberlab lab run xss-basic
```

Acceptance tests verify that all architectural layers collaborate correctly.

---

# Test Doubles

CyberLab primarily uses **Fakes**.

Typical examples include:

* FakeCommandRunner
* FakeLabRepository
* FakeLabManifestLoader
* FakeLabValidator

Fakes provide predictable behavior while remaining close to production implementations.

Mocks should be used only when interaction verification cannot be expressed naturally through a Fake.

---

# Testing Infrastructure

Infrastructure components are tested independently from business rules.

Example:

```text id="vcpi88"
DockerComposeService
        │
        ▼
FakeCommandRunner
```

The service verifies:

* command construction;
* argument ordering;
* propagation of ProcessResult.

It does not test Docker itself.

---

# Testing Use Cases

Use cases are tested through their Protocols.

```text id="s73q8s"
LabRunUseCase
        │
        ▼
FakeLabRunner
```

The use case should remain completely unaware of infrastructure implementations.

---

# Testing CLI

CLI tests verify:

* command registration;
* command output;
* integration with use cases.

The CLI should never contain business logic.

---

# Test Organization

```text id="n6fx0r"
tests/
├── acceptance/
├── integration/
├── unit/
└── fakes/
```

Tests should mirror the production structure whenever practical.

---

# Test Naming

Test names should describe observable behavior.

Prefer:

```text id="q55k9k"
test_run_returns_success_report
```

instead of:

```text id="vjlwmf"
test_runner
```

Behavior-oriented names improve readability and documentation.

---

# Running Tests

Run the complete verification pipeline:

```bash id="yhl79s"
make verify
```

Format the code:

```bash id="jwl04d"
make format
```

Execute the full test suite:

```bash id="0m0wlw"
pytest
```

Individual test modules may also be executed directly during development.

---

# Architectural Boundaries

Tests should reinforce architectural rules.

Application tests must never depend directly on Infrastructure.

Infrastructure tests may depend on Application contracts but should not alter business behavior.

The Composition Root should remain thin and contain no business logic.

---

# Continuous Evolution

Whenever a new feature is introduced:

1. Write the failing test (RED).
2. Implement the minimum code required (GREEN).
3. Refactor while keeping all tests passing (REFACTOR).

This RED → GREEN → REFACTOR cycle is the standard development workflow throughout the project.

Maintaining a fast, reliable and expressive test suite is considered an essential part of CyberLab's architecture rather than an afterthought.
