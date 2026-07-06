# CyberLab

> **Reproducible Cybersecurity Labs built with Clean Architecture, Hexagonal Architecture and Test-Driven Development.**

CyberLab is an open-source framework for creating, managing and executing reproducible cybersecurity laboratories.

The project is designed to be both a practical platform for security research and an educational reference for modern Python software engineering.

---

# Goals

CyberLab is built around a few fundamental principles:

* Reproducible laboratory environments
* Clean Architecture
* Hexagonal Architecture
* Dependency Injection
* Test-Driven Development (TDD)
* High testability
* Low coupling
* Small, incremental commits
* Production-quality Python code

---

# Features

Current capabilities include:

* Environment diagnostics
* Project version information
* Laboratory discovery
* Laboratory metadata inspection
* Strong architectural separation
* Comprehensive automated tests

---

# Architecture

CyberLab follows a layered architecture.

```text
CLI
│
▼
Application (Use Cases)
│
▼
Application Interfaces (Protocols)
▲
│
Infrastructure (Implementations)
│
▼
Domain (Models, Value Objects, Reports)
```

## Layer Responsibilities

### Domain

Represents business concepts.

Contains:

* Models
* Value Objects
* Reports

The Domain never depends on any other layer.

---

### Application

Coordinates the business flow.

Contains:

* Use Cases
* Protocols

Application depends only on:

* Domain
* Protocols

---

### Infrastructure

Implements external integrations.

Examples:

* Filesystem
* Process execution
* Docker
* Configuration

Infrastructure implements the Protocols defined by the Application.

---

### CLI

Responsible only for:

* input adaptation
* dependency composition
* output rendering

No business logic is implemented in the CLI.

---

# Project Structure

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
    │
    ├── domain/
    │   ├── models/
    │   ├── interfaces/
    │   └── value_objects/
    │
    ├── infrastructure/
    │   ├── configuration/
    │   ├── docker/
    │   ├── filesystem/
    │   └── process/
    │
    └── shared/

tests/
├── fakes/
└── unit/

labs/
└── <lab-id>/
    ├── lab.yaml
    ├── README.md
    └── compose.yaml
```

---

# Requirements

* Python 3.12+
* uv

---

# Installation

Clone the repository:

```bash
git clone https://github.com/<your-user>/CyberLab.git
cd CyberLab
```

Install dependencies:

```bash
uv sync
```

---

# Development

Format the source code:

```bash
make format
```

Run all quality checks:

```bash
make verify
```

`make verify` executes:

* Ruff
* Ruff Format
* MyPy (Strict)
* Pytest

---

# CLI Commands

## Version

Display the current version.

```bash
uv run cyberlab version
```

---

## Doctor

Validate the local development environment.

```bash
uv run cyberlab doctor
```

Example:

```text
✔ Git
✔ Docker
✔ Python
✔ uv

Environment OK
```

---

## List Laboratories

List every available laboratory.

```bash
uv run cyberlab lab list
```

Example:

```text
Available laboratories:

- csrf-basic
- sqli-basic
- xss-basic
```

---

## Show Laboratory Information

Display the metadata of a laboratory.

```bash
uv run cyberlab lab info xss-basic
```

Example:

```text
Name: Basic XSS
ID: xss-basic
Category: web
Difficulty: easy
Version: 1.0.0

Description:
Basic reflected XSS laboratory.
```

---

# Laboratory Manifest

Every laboratory is described by a `lab.yaml` file.

Example:

```yaml
id: xss-basic
name: Basic XSS
description: Basic reflected XSS laboratory.
category: web
difficulty: easy
version: 1.0.0
```

The manifest is the single source of truth for laboratory metadata.

---

# Laboratory Layout

A laboratory follows the structure below:

```text
labs/
└── xss-basic/
    ├── lab.yaml
    ├── README.md
    └── compose.yaml
```

Future versions may include additional resources such as:

* templates
* scenarios
* datasets
* validation rules

---

# Development Principles

CyberLab follows a few architectural rules.

## Dependency Injection

External dependencies are injected through constructors.

Example:

```python
DoctorUseCase(runner)
```

---

## Protocols

Application depends only on Protocols.

Infrastructure provides concrete implementations.

---

## Use Cases

Every Use Case exposes a single public method:

```python
execute(...)
```

---

## Domain Models

Domain models are immutable whenever possible.

```python
@dataclass(frozen=True, slots=True)
```

---

## Fakes

Application tests use Fakes instead of Mocks.

Every Fake:

* implements the corresponding Protocol;
* is fully in-memory;
* receives its initial state through the constructor;
* records relevant requests;
* fails explicitly on unexpected input.

---

## Testing Strategy

The project follows the AAA pattern.

```text
Arrange

↓

Act

↓

Assert
```

Layer responsibilities:

| Layer          | Responsibility         |
| -------------- | ---------------------- |
| Domain         | Business rules         |
| Application    | Orchestration          |
| Infrastructure | External integrations  |
| CLI            | Input/output rendering |

---

# Git Workflow

Each feature follows the same development cycle.

```text
Design Review

↓

RED

↓

GREEN

↓

REFACTOR

↓

Code Review

↓

Commit
```

Commits follow the Conventional Commits specification.

---

# Quality Standards

Every commit must pass:

```bash
make format
make verify
```

The working tree should be clean before merging:

```bash
git status
git show --stat HEAD
```

---

# Roadmap

Completed:

* Bootstrap
* Version command
* Environment Doctor
* Laboratory Discovery
* Laboratory Metadata

Planned:

* Laboratory Validation
* Laboratory Runner
* Docker Orchestration
* Template Engine
* Package Manager
* Scenario Engine

---

# Core Technologies

| Tool        | Purpose                     |
| ----------- | --------------------------- |
| Python 3.12 | Programming language        |
| uv          | Dependency management       |
| Typer       | CLI                         |
| PyYAML      | Laboratory manifest parsing |
| Ruff        | Linting and formatting      |
| MyPy        | Static type checking        |
| Pytest      | Testing                     |
| Coverage    | Test coverage               |

---

# License

This project is released under the MIT License.

See the `LICENSE` file for details.
