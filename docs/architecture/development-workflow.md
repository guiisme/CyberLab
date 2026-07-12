# CyberLab Development Workflow

## Purpose

This document defines the standard development workflow used throughout the CyberLab project.

The objective is to ensure that every contribution is:

- architecturally consistent;
- independently reviewable;
- fully testable;
- easy to understand;
- safe to merge.

The development workflow is considered part of the project's architecture.

Every Pull Request should improve not only the codebase, but also the engineering quality of the project.

---

# Core Principles

Every contribution follows these principles:

- Architecture before implementation.
- Small and focused Pull Requests.
- Atomic and reviewable commits.
- One architectural responsibility per commit.
- Every commit leaves the repository in a releasable state.
- Documentation evolves together with the implementation.
- Quality gates must pass before a commit is finalized.

---

# Development Lifecycle

Every Pull Request follows the same lifecycle.

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

Implementation never begins before the planning stages are complete.

---

# 1. Architecture Brief

Every Pull Request begins with a concise architectural overview.

The Architecture Brief answers:

- Why does this feature exist?
- Which capability is being introduced?
- Which architectural layers are affected?
- What is the expected outcome?

The objective is to establish a shared understanding before implementation begins.

---

# 2. Architecture Review

Before writing code, review the existing architecture.

Questions include:

- Does the feature fit the current architecture?
- Can an existing abstraction be reused?
- Does this preserve Clean Architecture?
- Does this introduce unnecessary coupling?

Architectural inconsistencies should be resolved before implementation.

---

# 3. Impact Analysis

Identify every component affected by the change.

Example:

| Layer | Component | Changes |
|--------|-----------|---------|
| Domain | Models | No |
| Application | Use Cases | Yes |
| Application | Protocols | Yes |
| Infrastructure | Services | Yes |
| CLI | Commands | Yes |
| Tests | Fakes | Yes |
| Documentation | Architecture | Yes |

Implementation should only modify components identified during this analysis.

---

# 4. Dependency Graph

Map the dependency flow before implementation.

Example:

```text
DockerComposeService

↓

DockerComposeLabRunner

↓

LabRunnerProtocol

↓

LabStopUseCase

↓

CLI
```

The dependency graph prevents incomplete implementations and helps define the correct implementation order.

---

# 5. Contract Review

Whenever a Protocol changes, every implementation must be reviewed.

Typical questions include:

- Which classes implement this Protocol?
- Which Fakes implement this Protocol?
- Which Use Cases depend on this Protocol?
- Which CLI commands use these Use Cases?

Reviewing contracts before implementation significantly reduces integration problems.

---

# 6. Commit Plan

Every Pull Request is divided into small, self-contained commits.

Each commit should:

- introduce a single logical change;
- remain independently reviewable;
- preserve a working repository;
- include tests for the implemented behavior.

Large changes should be split into smaller architectural increments.

---

# 7. Implementation

Implementation begins only after planning.

During implementation:

- preserve architectural boundaries;
- avoid unnecessary abstractions;
- keep responsibilities focused;
- follow existing project conventions;
- evolve existing patterns instead of introducing competing ones.

Implementation should never redefine established architectural decisions without discussion.

---

# 8. Verification

Every commit must pass the complete verification pipeline.

```bash
make format

make verify
```

Verification includes:

- Ruff
- MyPy
- Pytest

No commit is considered complete until the entire verification pipeline succeeds.

---

# 9. Sprint Review

Before closing a Pull Request, review the delivered work.

Typical questions include:

- Was the objective achieved?
- Did the architecture improve?
- Are tests complete?
- Was documentation updated?
- Is the repository releasable?

The Sprint Review validates both functionality and engineering quality.

---

# 10. Retrospective

Every completed Pull Request is an opportunity to improve the workflow.

Questions include:

- What worked well?
- What created unnecessary friction?
- What architectural decisions proved valuable?
- What should change for the next Pull Request?

Lessons learned should be incorporated into this workflow whenever appropriate.

---

# Commit Guidelines

Every commit should:

- compile successfully;
- pass every quality gate;
- implement a single architectural responsibility;
- avoid unrelated modifications;
- remain understandable in isolation.

A commit should tell a complete and coherent story.

---

# Quality Gates

Before every commit:

```bash
make format

make verify
```

Quality gates include:

- Ruff
- MyPy
- Pytest

Documentation updates are required whenever architectural behavior changes.

---

# Architectural Evolution

New capabilities should evolve from lower-level infrastructure toward higher-level interfaces.

The preferred evolution order is:

```text
Infrastructure

↓

Application

↓

CLI

↓

Documentation
```

This order minimizes dependency conflicts and allows every intermediate commit to remain functional.

---

# Development Philosophy

CyberLab values engineering discipline over implementation speed.

Architectural consistency is preferred over convenience.

Small, reviewable changes are preferred over large feature branches.

Documentation is considered part of the implementation.

Engineering decisions should remain explicit, documented and easy to understand.

---

# Definition of Done

A Pull Request is considered complete only when:

- Architecture has been reviewed.
- Impact Analysis has been completed.
- Dependency Graph has been validated.
- Contract Review has been completed.
- Implementation is finished.
- Ruff passes.
- MyPy passes.
- Pytest passes.
- Documentation has been updated.
- The repository is ready to merge.

---

# Continuous Improvement

The workflow itself is part of the project.

Whenever a better engineering practice is identified, this document should evolve.

The goal is not only to build a well-architected application, but also to maintain a well-architected engineering process.

---

# Engineering Checklists

The following checklists help ensure that every Pull Request meets the project's engineering standards.

They complement the development workflow and should be used before implementation and before merging a Pull Request.

---

## Pre-Implementation Checklist

Before writing code, verify that the feature has been properly planned.

### Architecture

- [ ] Architecture Brief completed.
- [ ] Architecture Review completed.
- [ ] Impact Analysis documented.
- [ ] Dependency Graph validated.
- [ ] Contract Review completed.

### Planning

- [ ] Commit Plan defined.
- [ ] Scope clearly limited.
- [ ] Architectural responsibilities identified.

Implementation should only begin after this checklist has been completed.

---

## Pre-Merge Checklist

Before merging a Pull Request, perform a complete quality audit.

### Verification

- [ ] `make format`
- [ ] `make verify`

### Quality Audit

- [ ] VS Code Problems reviewed.
- [ ] Protocol Review completed.
- [ ] Fake Review completed.
- [ ] Composition Root reviewed.
- [ ] CLI reviewed for architectural consistency.

### Documentation

- [ ] README updated.
- [ ] Architecture documentation updated.
- [ ] Testing documentation updated.
- [ ] Project Context updated.
- [ ] Roadmap updated when applicable.

### Final Review

- [ ] Sprint Review completed.
- [ ] Retrospective completed.
- [ ] Definition of Done satisfied.

A Pull Request is considered ready to merge only after every applicable item has been reviewed.

---

## Quality Audit

The Quality Audit is the final engineering review performed before merging a Pull Request.

Its objective is to identify architectural inconsistencies, contract violations and quality issues that may not be detected by automated tooling.

The audit includes:

### Protocol Review

Verify that:

- every Protocol defines a complete and consistent contract;
- method signatures remain coherent;
- type annotations are complete;
- Protocol methods use explicit ellipsis (`...`).

### Fake Review

Verify that:

- every Protocol has a canonical Fake implementation;
- Fakes evolve together with their Protocols;
- no duplicated Fake implementations exist;
- behavior remains deterministic.

### Composition Root Review

Verify that:

- dependency creation remains centralized;
- infrastructure is not instantiated outside the Composition Root;
- dependency injection remains explicit.

### CLI Review

Verify that:

- commands remain thin;
- Use Cases perform orchestration;
- infrastructure details do not leak into the presentation layer.

### Documentation Review

Verify that architectural documentation reflects the implemented behavior.

Documentation should explain architectural decisions rather than implementation details.

### VS Code Problems

Review every warning reported by the IDE.

Each warning should be classified as one of the following:

- Fix before merge
- Technical Debt
- False Positive

Warnings should never be ignored without understanding their cause.

---

## Definition of Done

A Pull Request is complete only when:

- Architecture has been reviewed.
- Implementation is complete.
- Tests pass successfully.
- Documentation has been updated.
- Quality Audit has been completed.
- Sprint Review has been completed.
- The repository is ready to merge.
