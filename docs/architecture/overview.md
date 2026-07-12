# CyberLab Architecture Overview

## Purpose

CyberLab is an open-source framework for building and executing reproducible cybersecurity laboratories.

The project is designed around the principles of:

- Clean Architecture
- Hexagonal Architecture (Ports and Adapters)
- Test-Driven Development (TDD)
- Protocol-Oriented Design
- Dependency Injection

The primary objective is to keep business rules independent from infrastructure and presentation concerns, allowing the framework to evolve with minimal coupling, high testability and clear separation of responsibilities.

This document provides a high-level overview of the project's architecture and the responsibilities of each layer.

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
- invoking Application Use Cases;
- formatting terminal output.

The CLI never contains business rules and never communicates directly with infrastructure components.

---

## Application

The Application layer orchestrates use cases.

Its responsibilities include:

- coordinating business workflows;
- invoking Protocols;
- exposing the system capabilities.

Application services do not know how operations are implemented.

Examples include:

- Run Laboratory
- Stop Laboratory
- Validate Laboratory
- Display Laboratory Information

---

## Protocols

Protocols define the contracts between the Application layer and Infrastructure.

They represent ports in the Hexagonal Architecture.

Examples include:

- LabRunnerProtocol
- LabRepositoryProtocol
- LabManifestLoaderProtocol
- LabValidatorProtocol
- CommandRunnerProtocol

Protocols make infrastructure replaceable without affecting business workflows.

---

## Infrastructure

Infrastructure implements the Protocols.

This layer contains all platform-specific code.

Examples include:

- Docker Compose execution
- Filesystem repositories
- YAML manifest loading
- Command execution
- Laboratory validation

Infrastructure never contains orchestration logic.

---

# Capability Flow

A system capability traverses the architecture through each layer.

For example, stopping a laboratory follows this flow:

```text
CLI

lab stop

        │

        ▼

LabStopUseCase

        │

        ▼

LabRunnerProtocol

        │

        ▼

DockerComposeLabRunner

        │

        ▼

DockerComposeService

        │

        ▼

docker compose down
```

Each layer performs a single responsibility while remaining independent from implementation details belonging to other layers.

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

This approach ensures that dependency wiring remains isolated from business logic.

---

# Laboratory Lifecycle

CyberLab models laboratory execution as a lifecycle.

Current lifecycle operations include:

- Run laboratory
- Stop laboratory

Future lifecycle operations may include:

- Status
- Restart
- Logs

The lifecycle abstraction allows different execution backends to provide the same behavior through a common protocol.

---

# Hexagonal Architecture

CyberLab follows the Ports and Adapters pattern.

```text
                    Application

          +---------------------------+
          |        Use Cases          |
          +-------------+-------------+
                        |
                 Protocols (Ports)
                        |
        +---------------+---------------+
        |                               |
 Docker Compose                 Future Adapters
 Infrastructure                  (Podman, Kubernetes,
                                 Remote Runner, ...)
```

Application depends only on Protocols.

Adapters implement those Protocols.

New execution technologies can be introduced without changing business workflows.

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
- Small and focused Use Cases
- Replaceable infrastructure
- Testability by design

These principles guide every architectural decision in the project.

---

# Long-Term Vision

CyberLab is designed as an extensible platform rather than a Docker-specific tool.

Future execution adapters may include:

- Podman
- Kubernetes
- Remote execution environments
- Cloud-native laboratory orchestration

Because the Application layer depends only on Protocols, these capabilities can be introduced without changing existing business workflows.

This architecture allows CyberLab to evolve while preserving stability, maintainability and testability.
