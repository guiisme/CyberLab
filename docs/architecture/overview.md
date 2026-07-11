# CyberLab Architecture Overview

## Purpose

CyberLab is designed around the principles of **Clean Architecture**, **Hexagonal Architecture**, and **Test-Driven Development (TDD)**.

The primary objective is to build a framework capable of creating, validating and executing reproducible cybersecurity laboratories while keeping business rules independent from infrastructure.

The architecture emphasizes:

* clear separation of responsibilities;
* dependency inversion;
* infrastructure independence;
* high testability;
* incremental evolution through small, reviewable changes.

---

# Architectural Layers

```text
                CLI
                 │
                 ▼
         Application Layer
                 │
        Interfaces (Protocols)
                 ▲
                 │
      Infrastructure Layer
                 │
                 ▼
         External Systems
```

Dependencies always point toward the Application layer.

The Domain and Application layers never depend on Infrastructure.

---

# Layer Responsibilities

## CLI

Responsible for:

* parsing command-line arguments;
* registering commands;
* presenting results to users.

The CLI contains no business rules.

---

## Application

Responsible for:

* use cases;
* orchestration;
* business workflows;
* defining infrastructure contracts through Protocols.

The Application layer coordinates the execution of laboratories but never depends on Docker, the filesystem or external tools.

---

## Domain

Responsible for:

* business models;
* immutable value objects;
* execution reports;
* validation results.

Domain objects remain independent from any infrastructure concern.

---

## Infrastructure

Responsible for implementing the interfaces defined by the Application layer.

Examples include:

* filesystem repositories;
* YAML manifest loading;
* laboratory validation;
* process execution;
* Docker Compose integration.

Infrastructure may change without affecting business rules.

---

# Dependency Rule

The dependency flow is always:

```text
CLI
    │
    ▼
Application
    │
    ▼
Protocols
    ▲
    │
Infrastructure
```

Infrastructure implements contracts defined by the Application layer.

Application never imports Infrastructure.

---

# Composition Root

The Composition Root is responsible for wiring the application.

Currently this responsibility belongs to:

```text
cyberlab.cli.app.create_app()
```

It creates concrete infrastructure implementations and injects them into the CLI.

Business logic never creates infrastructure components directly.

---

# Laboratory Execution

Laboratory execution follows the flow below:

```text
CLI
    │
    ▼
LabRunUseCase
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
CommandRunnerProtocol
    │
    ▼
docker compose
```

This flow demonstrates the separation between business rules and execution technology.

Replacing Docker Compose with another execution backend should require changes only inside the Infrastructure layer.

---

# Protocol-Oriented Design

Communication between Application and Infrastructure occurs through Protocols.

Examples include:

* CommandRunnerProtocol
* LabRepositoryProtocol
* LabManifestLoaderProtocol
* LabValidatorProtocol
* LabRunnerProtocol

Protocols belong to the Application layer because they express application requirements rather than infrastructure implementations.

---

# Dependency Injection

All infrastructure dependencies are injected through constructors.

The project avoids service locators and global state.

Object creation is centralized in the Composition Root.

---

# Testing Strategy

Testing follows the testing pyramid.

```text
Acceptance Tests

Integration Tests

Unit Tests
```

Whenever possible:

* Fakes are preferred over mocks.
* Business rules are tested independently from infrastructure.
* Infrastructure is tested in isolation.
* External systems are validated through acceptance tests.

---

# Laboratory Model

Each laboratory is self-contained.

```text
labs/
└── xss-basic/
    ├── lab.yaml
    ├── compose.yaml
    └── README.md
```

Each laboratory owns:

* its metadata;
* its infrastructure;
* its documentation;
* its execution environment.

---

# Architectural Principles

The project follows these principles:

* Single Responsibility Principle
* Dependency Inversion Principle
* Explicit Composition Root
* Constructor Dependency Injection
* Protocol-Oriented Design
* Infrastructure Isolation
* Immutable Domain Models
* Small, Incremental Pull Requests
* Test-Driven Development

These principles are intended to remain stable as the project evolves.
