# Testing Strategy

## Philosophy

CyberLab follows Test-Driven Development (TDD).

Every feature is developed using the same workflow:

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

---

# Test Organization

```text
tests/
├── unit/
└── fakes/
```

Unit tests are organized following the project structure.

---

# Arrange – Act – Assert

Every unit test follows the AAA pattern.

```text
Arrange

↓

Act

↓

Assert
```

The sections should be explicitly separated whenever practical.

---

# Test Doubles

CyberLab adopts **Fakes** as the preferred testing strategy.

Mocks are intentionally avoided.

Every Fake:

* implements the corresponding Protocol;
* is fully in-memory;
* receives its state through the constructor;
* records relevant interactions;
* fails explicitly for unexpected input.

Examples:

* FakeCommandRunner
* FakeLabRepository
* FakeLabManifestLoader
* FakeLabValidator

---

# Protocol Testing

Protocols define contracts.

Protocols themselves are **not tested**.

Their implementations are tested instead.

---

# Domain Testing

Domain tests verify:

* immutability;
* derived properties;
* business rules;
* equality semantics.

Domain tests never interact with infrastructure.

---

# Application Testing

Application tests verify orchestration.

Use Cases:

* receive Protocol implementations;
* call the expected dependency;
* propagate errors when appropriate.

Application tests always use Fakes.

---

# Infrastructure Testing

Infrastructure tests verify interaction with external resources.

Examples:

* filesystem
* process execution
* YAML loading

Temporary resources should use pytest fixtures such as:

```python
tmp_path
```

No real project files should be modified during tests.

---

# CLI Testing

CLI tests use Typer's CliRunner.

Dependencies are injected through:

```python
create_app(...)
```

CLI tests verify:

* exit code;
* rendered output;
* command behavior.

Business logic is never tested through the CLI.

---

# Assertions

Prefer explicit assertions.

Example:

```python
assert report.success is True
assert report.failed_checks == 0
```

Avoid indirect assertions whenever possible.

---

# Test Naming

Test names should describe observable behavior.

Examples:

```text
test_execute_returns_validation_report

test_validate_returns_failure_when_required_file_is_missing

test_lab_info_displays_manifest
```

Avoid implementation-oriented names.

---

# Fixtures

Use pytest fixtures only when they improve readability.

Prefer local helper functions for simple object construction.

Builders or factories should only be introduced when duplication becomes significant.

---

# Quality Gates

Every commit must pass:

```bash
make format
make verify
```

The project is considered healthy only when:

* Ruff passes
* MyPy passes
* Pytest passes

No commit should be created with failing quality checks.

---

# Long-Term Goal

Tests should remain:

* deterministic;
* isolated;
* fast;
* easy to understand;
* independent from external services.

The architecture is intentionally designed so that the majority of tests execute without requiring Docker, network access or real laboratory environments.
