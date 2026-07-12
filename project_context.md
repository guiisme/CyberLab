# CyberLab — Project Context

*Last updated: July 2026*

---

# Project Overview

CyberLab is an open-source framework for building, executing and distributing reproducible cybersecurity laboratories.

The project combines:

- Clean Architecture
- Hexagonal Architecture
- Test-Driven Development (TDD)
- Protocol-Oriented Design
- Dependency Injection

The primary objective is to provide a highly maintainable platform where new laboratory capabilities can be added with minimal coupling and maximum testability.

CyberLab is designed as a long-term platform rather than a Docker-specific tool.

---

# Current Development Status

Current milestone:

```text
Laboratory Lifecycle
```

Implemented capabilities:

- Laboratory discovery
- Laboratory information
- Laboratory validation
- Laboratory execution
- Laboratory stop
- Environment diagnostics
- Version management

The project architecture is considered stable.

Future work is expected to extend existing capabilities rather than redesign core architecture.

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

Architecture is considered a first-class concern.

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
- DockerComposeLabRunner
- CommandRunner
- Filesystem repositories
- YAML manifest loader

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

Stop
```

Planned operations:

```text
Status

Restart

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

# Current Project Structure

```text
src/
└── cyberlab/
    ├── application/
    ├── cli/
    ├── domain/
    ├── infrastructure/
    └── shared/

docs/
├── adr/
├── architecture/
└── roadmap.md

labs/
└── xss-basic/

tests/
├── unit/
└── fakes/
```

---

# Current Laboratory

Reference laboratory:

```text
labs/xss-basic
```

Current lifecycle:

```bash
cyberlab lab run xss-basic

cyberlab lab stop xss-basic
```

This laboratory serves as the reference implementation for future laboratories.

---

# Next Development Priorities

Current priorities:

1. Laboratory Status
2. Laboratory Restart
3. Laboratory Logs
4. Additional laboratory templates
5. New execution adapters

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

# Starting a New Development Session

To continue CyberLab development in a new conversation:

1. Share this document (`project_context.md`).

2. Describe the objective of the next Pull Request.

3. Follow the official development workflow:

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
