# CyberLab — Project Context

Last updated: July 2026 (PR #014)

---

# Project Overview

CyberLab is an open-source framework for creating, building, executing, learning and distributing reproducible cybersecurity laboratories.

The project combines:

- Clean Architecture
- Hexagonal Architecture
- Test-Driven Development (TDD)
- Protocol-Oriented Design
- Dependency Injection

The primary objective is to provide a highly maintainable platform where new laboratory capabilities can be added with minimal coupling, maximum testability and long-term architectural stability.

CyberLab is designed as a long-term extensible platform rather than a Docker-specific tool.

---

# Current Development Status

Current milestone:

```text
Core Laboratory Platform
```

Implemented capabilities:

- Laboratory discovery
- Laboratory information
- Laboratory validation
- Laboratory scaffolding
- Laboratory lifecycle
    - Run
    - Stop
    - Status
    - Restart
    - Logs
- Environment diagnostics
- Version management

The project architecture is considered stable.

Recent development has confirmed that new capabilities can be introduced by extending the existing architecture rather than modifying established layers.

Future work is expected to expand the platform incrementally while preserving architectural consistency.

---

# Architectural Layers

```text
CLI

↓

Application

↓

Protocols

↓

Infrastructure
```

Dependencies always point downward.

---

# Architectural Principles

The project follows these architectural principles:

- Clean Architecture
- Hexagonal Architecture
- Dependency Inversion
- Protocol-Oriented Design
- Composition Root
- Explicit Dependency Injection
- Small Use Cases
- Replaceable Infrastructure
- Capability Consolidation

Architecture is considered a first-class concern.
Model capabilities around domain concepts rather than individual operations.
---

# Design Philosophy

CyberLab favors simplicity over premature abstraction.

Whenever possible:

- prefer extension over modification;
- prefer explicit code over hidden magic;
- prefer small duplication over unnecessary abstraction;
- prefer Protocols over inheritance;
- prefer Fakes over mocks;
- keep commits small and independently releasable.

Architectural consistency is valued more than implementation cleverness.

---

# Composition Root

Dependency creation is centralized inside the Composition Root.

Responsibilities include:

- infrastructure creation;
- protocol wiring;
- dependency injection;
- CLI composition.

Business logic never creates infrastructure objects directly.

---

# Current Infrastructure

Current execution backend:

- Docker Compose

Infrastructure components include:

- DockerComposeService
- DockerComposeLabLifecycle
- CommandRunner
- Filesystem repositories
- YAML manifest loader
- Filesystem laboratory scaffolding

Future execution adapters may include:

- Podman
- Kubernetes
- Remote execution
- Cloud-native orchestration

---

# Laboratory Lifecycle

Current lifecycle operations:

```text
Run

Status

Restart

Stop
```

Planned operations:

Logs
```

Lifecycle operations are exposed through Application Use Cases and implemented through Infrastructure adapters.

---

# Testing Strategy

Testing mirrors the architecture.

```text
CLI

↓

Application

↓

Domain

↓

Infrastructure
```

Current testing principles:

- TDD whenever practical
- Fakes instead of mocks
- One canonical Fake per Protocol
- Deterministic unit tests
- Fast feedback
- Layer isolation

Every architectural layer owns its own test suite.

---

# Development Workflow

Every Pull Request follows the official workflow.

```text
Architecture Brief

↓

Architecture Review

↓

Impact Analysis

↓

Dependency Graph

↓

Contract Review

↓

Commit Plan

↓

Implementation

↓

Verification

↓

Sprint Review

↓

Retrospective
```

This workflow is considered part of the project's architecture.

---

# Quality Gates

Every commit must successfully execute:

```bash
make format

make verify
```

The verification pipeline includes:

- Ruff
- MyPy
- Pytest

No commit is considered complete before passing every quality gate.

---

# Commit Strategy

Every Pull Request is divided into small architectural increments.

General evolution order:

```text
Infrastructure

↓

Application

↓

CLI

↓

Documentation
```

Each commit introduces a single architectural responsibility.

Every commit should leave the repository in a releasable state.

---

# Project Conventions

The project follows these conventions.

## Architecture

- One responsibility per layer.
- One architectural concern per commit.
- Business rules independent from infrastructure.
- Explicit dependency injection.
- Protocols define architectural contracts.
- Group related operations around a single domain capability whenever they belong to the same lifecycle or business concept.

---

## Testing

- One canonical Fake per Protocol.
- Test behavior rather than implementation.
- Infrastructure tested independently.
- CLI tested independently.

---

## Documentation

Documentation evolves together with implementation.

Documentation explains decisions rather than code.

Architecture documents remain timeless whenever possible.

---

# Project Structure (Permanent)

CyberLab follows a stable directory organization based on Clean Architecture and
Hexagonal Architecture. New capabilities should integrate into this structure
instead of introducing new top-level modules.

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
    │   │   ├── registry.py
    │   │   └── lab/
    │   │       ├── registry.py
    │   │       ├── list.py
    │   │       ├── info.py
    │   │       ├── validate.py
    │   │       ├── run.py
    │   │       ├── stop.py
    |   |       ├── restart.py
    │   │       └── status.py
    │   │
    │   └── rendering/
    │
    ├── domain/
    │   ├── models/
    │   └── value_objects/
    │
    ├── infrastructure/
    │   ├── docker/
    │   ├── filesystem/
    │   ├── process/
    │   └── runner/
    │
    └── shared/

docs/
├── adr/
├── architecture/
├── reviews/
└── roadmap/

scaffolds/
└── default/

labs/

tests/
├── fakes/
├── integration/
└── unit/
```

The directory organization is considered stable and should evolve incrementally.
Individual files may change over time, but the architectural organization should
remain consistent.

---

# Current Laboratory

Reference laboratory:

```text
labs/xss-basic

labs/sqli-basic
```

Current lifecycle:

```bash
cyberlab lab run xss-basic

cyberlab lab restart xss-basic

cyberlab lab stop xss-basic

cyberlab lab status xss-basic

cyberlab lab logs xss-basic

cyberlab lab create <lab-id>
```

This laboratory serves as the reference implementation for future laboratories.

---

# Next Development Priorities

Current priorities:

1. Additional official laboratories
2. Multiple laboratory scaffolds
3. New execution adapters
4. Plugin architecture

The architecture is prepared for these capabilities.

---

# Long-Term Vision

CyberLab aims to become a reference implementation for:

- cybersecurity laboratory automation;
- Clean Architecture in Python;
- Protocol-Oriented Design;
- reproducible offensive security laboratories.

The long-term objective is to evolve the platform without requiring architectural redesign.

Every new capability should integrate naturally into the existing architecture while preserving simplicity, maintainability and testability.

Official laboratory scaffolds provide a standardized foundation for future
laboratories, ensuring architectural consistency while allowing individual
laboratories to evolve independently.

# Starting a New Development Session

To continue CyberLab development in a new conversation:

1. Share this document (`project_context.md`).

2. Describe the objective of the next Pull Request.

3. Follow the official development workflow:

- Capability Review
- Architecture Brief
- Architecture Review
- Impact Analysis
- Dependency Graph
- Contract Review
- Commit Plan
- Implementation
- Verification
- Quality Audit
- Sprint Review
- Retrospective

Implementation should only begin after the planning stages have been completed.

---
# Architecture Status

Current architectural capabilities:

- Laboratory Discovery
- Laboratory Validation
- Laboratory Scaffolding
- Laboratory Lifecycle
- Environment Diagnostics

The architecture is considered stable.

Future development should evolve these capabilities before introducing new
architectural abstractions.
