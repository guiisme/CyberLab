# CyberLab — Project Context

Last updated: July 2026

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
- Plugin architecture
    - Public SDK
    - Plugin discovery
    - Plugin loading
    - Plugin registry
    - Plugin scaffolding
    - Plugin CLI
    - Standardized plugin template
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
- Filesystem plugin scaffolding
- Python Entry Point provider
- Plugin loader
- Plugin registry

Future execution adapters may include:

- Podman
- Kubernetes
- Remote execution
- Cloud-native orchestration

---

# Plugin Architecture

CyberLab plugins are independent Python distributions discovered through the
`cyberlab.plugins` Python Entry Point group. At application startup,
`EntryPointProvider` discovers entry points, `PluginLoader` instantiates them,
and `PluginRegistry` makes the loaded plugins available to application use
cases and the CLI.

The public plugin API is `cyberlab.sdk`. Plugins should import only public SDK
symbols, such as `Plugin`, `PluginManifest`, and `PluginProtocol`; they must
not depend on internal `application`, `infrastructure`, `cli`, or `domain`
modules.

The canonical template is `templates/plugin`. Create a plugin from the
repository root with:

```bash
uv run cyberlab plugin create my-plugin
```

For an ID of `my-plugin`, the generated distribution, Python package, and
entry point are:

| Concern | Value |
| --- | --- |
| Distribution ID | `my-plugin` |
| Python package | `cyberlab_plugin_my_plugin` |
| Plugin class | `MyPlugin` |
| Entry point group | `cyberlab.plugins` |
| Entry point name | `my-plugin` |

The generated `pyproject.toml` uses `uv_build` and must explicitly set:

```toml
[tool.uv.build-backend]
module-name = "cyberlab_plugin_my_plugin"
```

This is necessary because the distribution ID can contain hyphens while the
Python package uses underscores. The template also configures the local Core
as an editable `uv` source using `path = ".."`; therefore plugins created by
the CLI are expected to be direct children of the CyberLab checkout.

For local plugin development, `uv sync` inside the plugin creates that
plugin's own virtual environment. To make a generated plugin discoverable by
the CyberLab command executed from the repository root, install it into the
Core environment instead:

```bash
uv pip install --no-deps -e ./my-plugin
uv run cyberlab plugin list
```

`--no-deps` is used because the Core environment already provides CyberLab and
its dependencies. Installing from inside the plugin directory does not make
the plugin visible to the root project's `uv run cyberlab` command.

The template contains no `.venv` or `uv.lock`; each generated plugin creates
and owns those artifacts. See `docs/plugins/template.md` for the complete
template reference and `docs/adr/0012 - Plugin Architecture` for the
architectural decision.

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
Capability Proposal

↓

Architecture Brief

↓

Architecture Review

↓

Impact Analysis

↓

Dependency Graph

↓

Contract Design

↓

Commit Plan

↓

Implementation

↓

Code Review

↓

Architecture Audit

↓

Documentation

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
Contracts

↓

Infrastructure

↓

Consumer

↓

Composition Root

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
    │   └── commands/
    │       ├── lab/
    │       └── plugin/
    │
    ├── domain/
    │   ├── models/
    │   └── value_objects/
    │
    ├── infrastructure/
    │   ├── docker/
    │   ├── filesystem/
    │   ├── plugins/
    │   ├── process/
    │   └── runner/
    │
    └── sdk/

docs/
├── adr/
├── architecture/
├── reviews/
└── roadmap/

labs/

templates/
└── plugin/

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

# Current Plugin Commands

```bash
cyberlab plugin list

cyberlab plugin create <plugin-id>
```

---

# Next Development Priorities

Current priorities:

1. Official plugins
2. Multiple plugin templates
3. Additional official laboratories
4. Multiple laboratory scaffolds
5. New execution adapters

The architecture is prepared for these capabilities.

---

# Plugin Architecture

CyberLab now provides a complete plugin platform.

Plugins are developed as standalone Python packages that depend exclusively on the public SDK.

The discovery pipeline is:

```text
Python Entry Points

↓

EntryPointProvider

↓

PluginLoader

↓

PluginRegistry

↓

Application Use Cases

↓

CLI
```

CyberLab provides:

- Public SDK (`cyberlab.sdk`)
- Dynamic plugin discovery
- Plugin Registry
- Official plugin scaffold
- Plugin CLI

Plugins are created using:

```bash
cyberlab plugin create <plugin-id>
```

Installed plugins are discovered automatically through Python Entry Points.

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

CCurrent architectural capabilities:

- Laboratory Discovery
- Laboratory Validation
- Laboratory Scaffolding
- Laboratory Lifecycle
- Plugin SDK
- Plugin Architecture
- Plugin Scaffolding
- Environment Diagnostics

The architecture is considered stable.

Future development should extend existing capabilities before introducing new architectural abstractions.
