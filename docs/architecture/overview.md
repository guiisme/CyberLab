# CyberLab Architecture Overview

## Purpose

CyberLab is an open-source framework for building, executing, learning and
distributing reproducible cybersecurity laboratories.

The project is designed around the principles of:

- Clean Architecture
- Hexagonal Architecture (Ports and Adapters)
- Test-Driven Development (TDD)
- Protocol-Oriented Design
- Dependency Injection

The primary objective is to keep business rules independent from
infrastructure and presentation concerns, allowing the framework to evolve
with minimal coupling, high testability and clear separation of
responsibilities.

This document provides a high-level overview of the project's architecture and
the responsibilities of each layer.

---

# Architectural Layers

CyberLab is organized into four primary architectural layers.

```text
                CLI
                 │
                 ▼
          Application
                 │
                 ▼
             Protocols
                 │
                 ▼
          Infrastructure
```

Dependencies always point downward.

Lower layers never depend on higher layers.

---

# Layer Responsibilities

## CLI

The CLI is the presentation layer.

Its responsibilities are intentionally minimal.

It is responsible for:

- parsing user input;
- invoking Application use cases;
- formatting terminal output.

The CLI never contains business rules and never communicates directly with
infrastructure components.

---

## Application

The Application layer orchestrates business capabilities.

Its responsibilities include:

- coordinating workflows;
- invoking Protocols;
- exposing application capabilities.

Application services never know how operations are implemented.

Examples include:

- Laboratory Discovery
- Laboratory Validation
- Laboratory Lifecycle
- Environment Diagnostics

---

## Protocols

Protocols define the contracts between the Application layer and
Infrastructure.

They represent Ports in the Hexagonal Architecture.

Examples include:

- LabLifecycleProtocol
- LabRepositoryProtocol
- LabManifestLoaderProtocol
- LabValidatorProtocol
- CommandRunnerProtocol

Protocols make infrastructure replaceable without affecting business
workflows.

---

## Infrastructure

Infrastructure implements the Protocols.

This layer contains all platform-specific code.

Examples include:

- DockerComposeLabLifecycle
- DockerComposeService
- Filesystem repositories
- YAML manifest loading
- Command execution
- Laboratory validation

Infrastructure never contains orchestration logic.

---

# Architectural Capabilities

CyberLab organizes related operations around architectural capabilities rather
than individual commands.

Current architectural capabilities include:

- Laboratory Discovery
- Laboratory Validation
- Laboratory Lifecycle
- Environment Diagnostics

Each capability owns its own protocols, infrastructure adapters and business
workflow while remaining independent from the others.

This approach favors cohesive domain concepts over isolated command-oriented
implementations.

---

# Capability Flow

Every capability traverses the architecture through the same layers.

For example, restarting a laboratory follows this flow:

```text
CLI

lab restart

        │

        ▼

RestartLabUseCase

        │

        ▼

LabLifecycleProtocol

        │

        ▼

DockerComposeLabLifecycle

        │

        ▼

DockerComposeService

        │

        ▼

docker compose restart
```

Each layer performs a single responsibility while remaining independent from
implementation details belonging to other layers.

---

# Dependency Direction

Dependencies always follow the same direction.

```text
Presentation

        │

        ▼

Application

        │

        ▼

Protocols

        │

        ▼

Infrastructure
```

Infrastructure never depends on the CLI.

Application never depends on Docker, filesystems or external technologies.

Business workflows remain independent from implementation details.

---

# Composition Root

Object creation is centralized in the Composition Root.

The Composition Root is responsible for:

- creating infrastructure services;
- wiring protocol implementations;
- injecting dependencies into the CLI.

This approach ensures that dependency wiring remains isolated from business
logic.

---

# Laboratory Lifecycle

CyberLab models laboratory execution as a lifecycle capability.

Current lifecycle operations include:

- Run laboratory
- Stop laboratory
- Status laboratory
- Restart laboratory
- Laboratory logs

The lifecycle abstraction allows different execution backends to provide the
same behavior through a common protocol.

---

# Hexagonal Architecture

CyberLab follows the Ports and Adapters pattern.

```text
                    Application

          +-----------------------------+
          |      Business Capabilities  |
          +--------------+--------------+
                         |
                 Protocols (Ports)
                         |
        +----------------+----------------+
        |                                 |
DockerComposeLabLifecycle        Future Adapters
                                 (Podman, Kubernetes,
                                 Remote Runner, ...)
```

Application depends only on Protocols.

Adapters implement those Protocols.

New execution technologies can be introduced without changing business
workflows.

---

# Testing Strategy

Testing mirrors the architecture.

```text
CLI Tests

↓

Application Tests

↓

Domain Tests

↓

Infrastructure Tests
```

Each layer is tested independently.

Protocols are tested using Fakes.

Infrastructure components are tested through their concrete implementations.

---

# Architectural Principles

The architecture follows these principles:

- Single Responsibility Principle
- Dependency Inversion Principle
- Explicit dependency injection
- Protocol-oriented interfaces
- Capability-oriented architecture
- Small and focused use cases
- Replaceable infrastructure
- Testability by design

These principles guide every architectural decision in the project.

---

# Long-Term Vision

CyberLab is designed as an extensible platform rather than a Docker-specific
tool.

Future execution adapters may include:

- Podman
- Kubernetes
- Remote execution environments
- Cloud-native laboratory orchestration

Because the Application layer depends only on Protocols, these capabilities can
be introduced without changing existing business workflows.

As new features are introduced, CyberLab evolves existing architectural
capabilities whenever possible instead of creating isolated abstractions.

This approach keeps the architecture cohesive, reduces unnecessary complexity
and allows the framework to grow without architectural redesign.
