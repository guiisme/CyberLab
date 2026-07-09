# CyberLab Architecture Overview

## Purpose

CyberLab is designed around the principles of Clean Architecture, Hexagonal Architecture and Test-Driven Development (TDD).

The primary goal is to keep business rules independent from infrastructure and presentation concerns, allowing the project to evolve with minimal coupling, high testability and clear separation of responsibilities.

This document describes the technical architecture of the project. Engineering philosophy, architectural principles, architectural decisions and product planning are documented separately.

---

# Architectural Concepts

CyberLab distinguishes two different structural concepts.

## Architectural Layer

An architectural layer defines a logical boundary with a well-defined responsibility.

The CyberLab architecture contains exactly four layers:

* CLI
* Application
* Domain
* Infrastructure

---

## Component

A component is a logical element that belongs to an architectural layer.

Examples include:

* Use Cases
* Protocols (Ports)
* Models
* Reports
* Value Objects

Components are not architectural layers.

---

# Architectural Layers

CyberLab is organized into four architectural layers.

```text
                 CLI
                  │
                  ▼
            Application
      ┌─────────────────────┐
      │     Use Cases       │
      │     Protocols       │
      └─────────────────────┘
                  │
                  ▼
                Domain

Infrastructure
       │
       └────────────► implements Application Protocols
```

The architecture isolates core business logic from technical concerns through explicit architectural boundaries, dependency inversion and well-defined contracts.

* The Domain is the core of the system.
* The Application orchestrates business operations.
* Protocols are defined within the Application layer.
* Infrastructure depends on the Protocols defined by the Application and provides their concrete implementations.
* The CLI adapts user interaction into Application requests.

---

# Layer Responsibilities

## Domain

The Domain contains the core business concepts of CyberLab.

Examples:

* Models
* Reports
* Value Objects

Responsibilities:

* Represent business concepts.
* Enforce business invariants.
* Define immutable business models whenever possible.

The Domain:

* is independent from infrastructure;
* is independent from presentation concerns;
* never performs technical operations.

---

## Application

The Application coordinates business operations.

It contains:

* Use Cases
* Protocols (Ports)

Responsibilities:

* Orchestrate business workflows.
* Invoke Domain concepts.
* Delegate external operations through Protocols.
* Define abstractions for external behavior.

The Application may depend only on:

* the Domain;
* its own Protocol interfaces.

The Application never:

* performs technical operations directly;
* depends on Infrastructure implementations;
* contains infrastructure-specific logic.

---

## Infrastructure

Infrastructure provides concrete implementations for the Protocols defined by the Application.

Examples include:

* filesystem adapters;
* process execution;
* configuration;
* external platform integrations.

Responsibilities:

* Implement Application Protocols.
* Interact with external systems.
* Isolate technical details from business logic.

Infrastructure depends on the Protocol interfaces defined by the Application but never contains business rules.

---

## CLI

The CLI adapts user interaction into Application requests.

Responsibilities:

* Parse command-line arguments.
* Compose dependencies.
* Invoke Use Cases.
* Render output.

Business rules must never be implemented in the CLI.

---

# Dependency Rules

The following dependency rules must always be respected.

| Layer          | May Depend On                 |
| -------------- | ----------------------------- |
| CLI            | Application¹                  |
| Application    | Domain, its own Protocols     |
| Infrastructure | Domain, Application Protocols |
| Domain         | None                          |

¹ Except for the Composition Root, which is intentionally allowed to assemble Infrastructure implementations.

---

## Protocol Rules

Protocols define the contracts between the Application and external systems.

Protocols should be introduced only when a Use Case depends on external behavior.

Typical examples include:

* filesystem access;
* process execution;
* manifest loading;
* external platform integration.

Protocols must not be created for pure business logic.

Protocols belong to the Application layer.

Infrastructure provides concrete implementations of those Protocols.

Automated tests assemble alternative dependency graphs using **Test Doubles** that implement the same Protocol contracts.

---

## Forbidden Dependencies

The following dependencies are explicitly forbidden.

| Layer          | Must Not Depend On                                            |
| -------------- | ------------------------------------------------------------- |
| Domain         | Presentation layers, Infrastructure and external technologies |
| Application    | Concrete Infrastructure implementations                       |
| Infrastructure | CLI                                                           |
| CLI            | Business rules and Domain implementation details              |

These rules preserve architectural boundaries and prevent coupling between unrelated concerns.

---

# Composition Root

The Composition Root centralizes dependency construction.

Its responsibilities include:

* assembling production dependencies;
* wiring Application Protocols to their concrete Infrastructure implementations;
* constructing the application's object graph;
* injecting dependencies into the Application layer.

The Composition Root is the only intentional exception to the dependency rules.

Because of this responsibility, it is allowed to depend on both the Application and Infrastructure layers.

Outside the Composition Root:

* the CLI depends only on the Application layer;
* the Application never instantiates Infrastructure;
* Infrastructure is never assembled inside Use Cases.

The current Composition Root is implemented by `create_app()`.

Production and test environments assemble different dependency graphs while preserving the same architectural boundaries.

---

# Project Structure

The project structure mirrors the architectural boundaries defined by CyberLab.

```text
src/cyberlab/
├── application/
├── cli/
├── domain/
└── infrastructure/
```

Supporting packages that do not represent architectural layers are documented separately through the project's Architecture Decision Records.

---

# References

Additional architectural information is available in:

* `docs/AI_CONTEXT.md`
* `docs/architecture/principles.md`
* `docs/architecture/testing.md`
* `docs/adr/`
* `docs/roadmap/`
