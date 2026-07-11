# CyberLab Development Workflow

## Purpose

This document defines the standard development workflow used throughout the CyberLab project.

The objective is to ensure that every contribution is:

* architecturally consistent;
* independently reviewable;
* fully testable;
* easy to understand;
* safe to merge.

Development workflow is considered part of the project's architecture.

---

# Core Principles

Every change should follow these principles:

* Architecture before implementation.
* Small and focused Pull Requests.
* Small and reviewable commits.
* Single responsibility per commit.
* Every commit must leave the project in a releasable state.
* Documentation evolves together with the implementation.

---

# Development Lifecycle

Every Pull Request follows the same lifecycle.

```text
Architecture Review

↓

Impact Analysis

↓

Dependency Graph

↓

Commit Plan

↓

Implementation

↓

Verification

↓

Documentation

↓

Pull Request
```

No implementation should begin before the previous stages have been completed.

---

# 1. Architecture Review

Every feature starts with an architectural discussion.

Questions include:

* Does this feature fit the current architecture?
* Which layer should own this responsibility?
* Are new abstractions required?
* Can an existing component be reused?
* Does this preserve Clean Architecture?

The goal is to minimize unnecessary changes before writing code.

---

# 2. Impact Analysis

Before implementing a feature, identify every affected component.

Example:

| Layer          | Component    | Changes |
| -------------- | ------------ | ------- |
| Domain         | Models       | No      |
| Application    | Protocols    | Yes     |
| Application    | Use Cases    | Yes     |
| Infrastructure | Services     | Yes     |
| CLI            | Commands     | Yes     |
| Tests          | Fakes        | Yes     |
| Documentation  | Architecture | Yes     |

Only after this analysis should implementation begin.

---

# 3. Dependency Graph

Changes should be planned according to the dependency flow.

Example:

```text
DockerComposeService

↓

DockerComposeLabRunner

↓

LabRunnerProtocol

↓

Use Case

↓

CLI
```

The dependency graph helps prevent incomplete implementations and compilation failures.

---

# 4. Commit Plan

Each Pull Request is divided into small, self-contained commits.

Every commit should have:

* one architectural responsibility;
* one clear objective;
* a meaningful commit message;
* complete implementation for its scope.

Commits should remain independently reviewable.

---

# 5. Implementation

Implementation begins only after the previous planning steps.

During implementation:

* preserve architectural boundaries;
* avoid unnecessary abstractions;
* keep classes focused;
* prefer composition over duplication;
* follow existing project conventions.

---

# 6. Verification

Every commit must pass the complete verification pipeline.

```bash
make format

make verify
```

Verification includes:

* Ruff
* MyPy
* Pytest

A commit is considered complete only when the verification pipeline succeeds.

---

# 7. Documentation

Architecture documentation evolves together with the code.

Whenever an architectural decision changes, update the relevant documents.

Typical updates include:

* README
* Architecture Overview
* Principles
* Testing
* ADRs
* Project Context
* Roadmap

Documentation is treated as part of the implementation.

---

# Pull Request Rules

Each Pull Request should:

* address a single architectural concern;
* remain reasonably small;
* preserve backward compatibility whenever practical;
* include automated tests;
* update documentation when required.

Large Pull Requests should be divided into smaller iterations.

---

# Commit Rules

Every commit should:

* compile successfully;
* pass all automated checks;
* introduce a single logical change;
* avoid unrelated modifications.

Commits should never leave the repository in a broken state.

---

# Test Strategy

Development follows Test-Driven Development whenever practical.

Tests should:

* describe observable behavior;
* remain deterministic;
* avoid implementation details;
* prefer Fakes over mocks.

Infrastructure and business rules should be tested independently.

---

# Architectural Evolution

Architectural changes should proceed from lower-level infrastructure toward higher-level application features whenever introducing new platform capabilities.

Typical evolution order:

```text
Infrastructure Service

↓

Infrastructure Adapter

↓

Application Protocol

↓

Use Case

↓

CLI

↓

Documentation
```

This order minimizes dependency conflicts and keeps the project buildable throughout development.

---

# Continuous Improvement

The workflow itself is part of the project.

Whenever a better development practice is identified, this document should be updated so future contributors benefit from the improvement.

The goal is not only to build a well-architected application, but also to maintain a well-architected development process.
