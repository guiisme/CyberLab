# CyberLab Architecture Overview

## Purpose

CyberLab is designed around the principles of Clean Architecture, Hexagonal Architecture and Test-Driven Development.

The primary goal is to keep business rules independent from infrastructure and presentation concerns, allowing the project to evolve with minimal coupling.

---

# Architectural Layers

The project is organized into four primary layers.

```text
CLI
│
▼
Application
│
▼
Infrastructure
│
▼
Domain
```

Dependencies always point toward the Domain.

The Domain never depends on any other layer.

---

# Layer Responsibilities

## Domain

The Domain contains the business concepts of CyberLab.

Examples:

* Models
* Reports
* Value Objects

Characteristics:

* Immutable whenever possible
* No infrastructure dependencies
* No framework dependencies

---

## Application

The Application coordinates business operations.

It contains:

* Use Cases
* Protocols (Interfaces)

Application depends only on the Domain and Protocols.

Use Cases orchestrate the execution flow but do not implement infrastructure concerns.

---

## Infrastructure

Infrastructure provides concrete implementations for the Protocols defined by the Application.

Examples:

* Filesystem
* Process execution
* Configuration
* Docker (future)

Infrastructure is the only layer allowed to interact with external resources.

---

## CLI

The CLI adapts user input into Application requests.

Responsibilities:

* Parse command-line arguments
* Compose dependencies
* Invoke Use Cases
* Render output

Business rules must never be implemented in the CLI.

---

# Dependency Flow

```text
CLI
    │
    ▼
Use Case
    │
    ▼
Protocol
    ▲
    │
Infrastructure
```

This dependency inversion allows Infrastructure implementations to be replaced without modifying business logic.

---

# Composition Root

Dependency construction is centralized in the Composition Root.

Currently:

```text
create_app()
```

Production dependencies:

* CommandRunner
* FilesystemLabRepository
* YamlLabManifestLoader
* FilesystemLabValidator

Tests replace these implementations with Fakes.

---

# Current Use Cases

The Application currently exposes:

* VersionUseCase
* DoctorUseCase
* ListLabsUseCase
* LabInfoUseCase
* LabValidationUseCase

Each Use Case exposes exactly one public method:

```python
execute(...)
```

---

# Testing Strategy

The architecture is designed to maximize testability.

Application tests depend exclusively on Protocols.

Infrastructure is tested independently.

CLI tests exercise command behavior using Fake implementations.

---

# Current Project Status

Implemented:

* Version
* Environment Doctor
* Laboratory Discovery
* Laboratory Metadata
* Laboratory Validation

Planned:

* Laboratory Runner
* Docker Orchestration
* Template Engine
* Package Manager

---

# Design Principles

The architecture follows these principles:

* Dependency Inversion
* Single Responsibility
* Explicit Dependency Injection
* Immutable Domain Models
* Composition over inheritance
* Testability first
* Small incremental changes
