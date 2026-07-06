# CyberLab Architecture Principles

> These principles define how the CyberLab project is designed, implemented and evolved.
>
> Every contribution should respect these principles unless a documented Architecture Decision Record (ADR) explicitly states otherwise.

---

# 1. Architecture First

Architecture is considered a product feature.

Every implementation must preserve the architectural integrity of the project.

Short-term convenience must never compromise long-term maintainability.

---

# 2. Layered Architecture

The project follows a layered architecture.

```text
CLI
    ↓
Application
    ↓
Domain
    ↑
Infrastructure
```

Responsibilities:

* **CLI** provides the user interface.
* **Application** orchestrates use cases.
* **Domain** models business concepts.
* **Infrastructure** integrates with external systems.

Dependencies must always point toward lower-level abstractions.

Lower layers must never depend on upper layers.

---

# 3. Single Responsibility

Every module should have one clear responsibility.

Examples:

* CLI renders output.
* Application coordinates workflows.
* Infrastructure executes external operations.
* Domain models concepts.

---

# 4. Domain-Centric Design

Business concepts belong to the Domain layer.

Infrastructure exists only to support the domain.

The domain must remain independent from frameworks and external technologies.

---

# 5. Infrastructure Has No Business Rules

Infrastructure may:

* execute commands;
* access the filesystem;
* communicate with Docker;
* invoke Git;
* read configuration.

Infrastructure must never decide whether a result is acceptable.

Business decisions belong to the Application layer.

---

# 6. Value Objects Are Immutable

All Value Objects follow ADR-0002.

Default implementation:

```python
@dataclass(frozen=True, slots=True)
```

Value Objects:

* have no identity;
* represent values;
* are immutable;
* are comparable by value.

---

# 7. Test-Driven Development

New functionality follows the TDD cycle.

```text
RED

↓

GREEN

↓

REFACTOR
```

No production code should be introduced without corresponding automated tests.

---

# 8. Small, Atomic Commits

Each commit should represent a single logical change.

Commits should be:

* understandable;
* reversible;
* independently reviewable.

Conventional Commits are mandatory.

---

# 9. Automated Quality

Every contribution must pass the project's quality gate.

Minimum requirements:

* Ruff
* Ruff Format
* MyPy
* Pytest

The canonical validation command is:

```bash
make verify
```

---

# 10. Explicit APIs

Public APIs should be intentional.

Names should communicate purpose.

Prefer:

* `get_version()`
* `run()`
* `validate_environment()`

Avoid generic names when they reduce readability.

---

# 11. Simplicity Before Flexibility

The project follows the YAGNI principle.

Features are introduced only when justified by real use cases.

Premature abstractions should be avoided.

---

# 12. Composition Over Coupling

Modules communicate through well-defined contracts.

Whenever possible:

* compose;
* inject dependencies;
* isolate responsibilities.

Avoid hidden dependencies.

---

# 13. Developer Experience Matters

Developer productivity is considered part of product quality.

The project should provide:

* fast feedback;
* predictable tooling;
* consistent formatting;
* reliable automated checks.

---

# 14. Documentation Is Part of the Architecture

Architecture is documented continuously.

The project maintains:

* ADRs for architectural decisions;
* architecture principles;
* contributor guidelines;
* project roadmap.

Documentation evolves together with the codebase.

---

# 15. Build for the Long Term

CyberLab is designed as a reusable framework rather than a collection of scripts.

Design decisions should prioritize:

* maintainability;
* extensibility;
* readability;
* testability;
* consistency.

Long-term quality always takes precedence over short-term convenience.
