# CyberLab — Project Context

*Last updated: July 2026*

## Project Overview

CyberLab is an open-source framework for building and executing reproducible cybersecurity laboratories.

The project is being developed with a strong emphasis on software engineering practices rather than rapid feature delivery. The architecture is intended to remain maintainable for many years while supporting future capabilities such as Docker orchestration, laboratory packaging, plugins and reusable templates.

The project follows an incremental development process, where architecture is stabilized before introducing significant new functionality.

---

# Architecture

The project adopts:

* Clean Architecture
* Hexagonal Architecture
* Test-Driven Development (TDD)
* SOLID principles
* Explicit Dependency Injection
* Composition Root
* Protocol-based Dependency Inversion
* Immutable Domain Models whenever possible

Current architectural layers:

```text
CLI
    │
    ▼
Application
    │
    ▼
Domain

Infrastructure
    │
    └── implements Application Protocols
```

Dependency construction is centralized in the Composition Root (`create_app()`).

Infrastructure implementations are intentionally assembled only in the Composition Root.

---

# Documentation Baseline

The architecture documentation has been reviewed and refined through multiple Design Reviews.

Current baseline:

```text
docs/

AI_CONTEXT.md
architecture/
    overview.md
    principles.md
    testing.md
adr/
roadmap/
```

Document responsibilities:

### AI_CONTEXT.md

Defines the engineering philosophy and long-term project vision.

---

### overview.md

Describes the technical architecture.

Topics include:

* architectural concepts
* layers
* dependency rules
* protocols
* composition root
* project structure

---

### principles.md

Defines the permanent engineering principles that govern the architecture.

Examples include:

* Clean Architecture
* Dependency Inversion
* Low Coupling
* High Cohesion
* Domain Independence
* Dependency Injection
* Simplicity
* Incremental Evolution

This document intentionally avoids implementation details.

---

### testing.md

Defines the testing architecture.

Topics include:

* testing philosophy
* testing by architectural layer
* protocol-based isolation
* dependency graphs
* composition root in tests

It does not describe testing frameworks or implementation details.

---

### ADRs

Architecture Decision Records document concrete architectural decisions.

Current ADRs:

* 0001 — Project Conventions
* 0002 — Value Objects
* 0003 — Environment Doctor
* 0004 — Laboratory Discovery
* 0005 — Laboratory Metadata Model
* 0006 — Validation Architecture
* 0007 — Shared Package

ADRs are the only source of truth for architectural decisions.

Architecture documents should reference ADRs rather than duplicate them.

---

# Documentation Principles

The project follows these documentation rules:

* Each document has a single responsibility.
* Avoid duplicated information.
* Prefer references over duplication.
* Architecture documentation must remain technology-independent whenever practical.
* Principles should outlive implementations.
* Overview documents describe architecture, not implementation.
* ADRs justify architectural decisions.
* AI_CONTEXT defines philosophy rather than architecture.

---

# Current Code Architecture

The project currently contains the following architectural areas:

```text
src/cyberlab/

application/
cli/
domain/
infrastructure/
shared/
```

The `shared` package is **not** an architectural layer.

Its purpose and usage are governed exclusively by ADR-0007.

---

# Current Development Status

Completed:

* Project foundation
* CLI architecture
* Version command
* Doctor command
* Laboratory discovery
* Laboratory metadata
* Laboratory validation
* Composition Root
* Architecture documentation baseline

Architecture documentation has been reviewed with Codex and refined until the responsibilities of each document became explicit and non-overlapping.

---

# Documentation Review Outcomes

The architecture documentation reached the following conclusions:

* `overview.md` is considered an appropriate architectural overview.
* `principles.md` is considered a long-term engineering principles document.
* `testing.md` is considered a long-term testing architecture document.

The remaining improvements suggested by Codex relate primarily to future contributor documentation rather than architectural corrections.

---

# Future Documentation Backlog

The following documents may be introduced as the project evolves:

* `DEVELOPMENT.md`
* `CONTRIBUTING.md`
* `architecture/error-handling.md`
* `architecture/plugins.md`
* `architecture/laboratory-lifecycle.md`

These are intentionally outside the scope of the current architecture baseline.

---

# Current Development Priority

The documentation baseline (Wave 2) is considered complete.

Future work should focus on implementing new features while preserving the approved architecture.

Any architectural change should:

1. Respect the Architecture Baseline.
2. Preserve dependency rules.
3. Be documented through an ADR when appropriate.
4. Keep documentation synchronized with implementation.

The preferred development workflow is:

1. Design.
2. Architecture review.
3. Implementation.
4. Tests.
5. Documentation update.
6. Commit.
7. Design review.
