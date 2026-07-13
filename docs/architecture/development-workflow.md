# CyberLab Development Workflow

*Official development workflow for all Pull Requests.*

---

# Philosophy

CyberLab evolves through small, independently releasable Pull Requests.

Every Pull Request should improve the project while preserving architectural
stability.

The workflow exists to encourage thoughtful design before implementation and to
keep the Git history clean, reviewable and maintainable.

Implementation is the result of architectural decisions, not the starting point.

---

# Core Principles

Every Pull Request should:

- preserve Clean Architecture;
- preserve Hexagonal Architecture;
- respect Protocol-Oriented Design;
- evolve existing capabilities before creating new ones;
- keep commits small and independently releasable;
- maintain a green repository after every commit.

---

# Official Workflow

Every Pull Request follows the same sequence.

```text
Capability Review
        │
        ▼
Architecture Brief
        │
        ▼
Architecture Review
        │
        ▼
Impact Analysis
        │
        ▼
Dependency Graph
        │
        ▼
Contract Review
        │
        ▼
Commit Plan
        │
        ▼
Implementation
        │
        ▼
Verification
        │
        ▼
Quality Audit
        │
        ▼
Sprint Review
        │
        ▼
Retrospective
```

No implementation should begin before the planning stages have been completed.

---

# Workflow Stages

## 1. Capability Review

Identify whether the new feature belongs to an existing architectural capability.

Questions:

- Does a similar capability already exist?
- Can an existing abstraction evolve naturally?
- Is a refactor preferable before adding the feature?

The preferred approach is to extend existing domain concepts rather than
introducing new abstractions.

---

## 2. Architecture Brief

Define:

- objective;
- architectural scope;
- affected layers;
- expected responsibilities.

No implementation decisions should be made at this stage.

---

## 3. Architecture Review

Validate:

- Clean Architecture;
- Hexagonal Architecture;
- Dependency Inversion;
- Single Responsibility;
- architectural consistency.

Architectural issues should be resolved before implementation.

---

## 4. Impact Analysis

Identify every affected component.

Typical analysis includes:

- protocols;
- infrastructure;
- CLI;
- documentation;
- tests.

The objective is to minimize change surface.

---

## 5. Dependency Graph

Review dependency direction.

Dependencies must always point downward.

```text
CLI

↓

Application

↓

Protocols

↓

Infrastructure
```

No layer may violate dependency inversion.

---

## 6. Contract Review

Review public contracts.

Typical checks:

- protocol responsibilities;
- naming;
- return types;
- consistency with existing interfaces.

Contracts should evolve conservatively.

---

## 7. Commit Plan

Split the Pull Request into small architectural increments.

Typical evolution order:

```text
Infrastructure

↓

Application

↓

CLI

↓

Documentation
```

Every commit must leave the repository in a releasable state.

---

## 8. Implementation

Implement one planned commit at a time.

Every commit should introduce one architectural responsibility.

Avoid mixing refactoring and new functionality unless the refactor is required
to support the feature.

Whenever a new capability creates permanent artifacts (such as scaffolds or reference labs), they must be included in the architecture documentation before the merge.

---

## 9. Verification

After every commit execute:

```bash
make format

make verify
```

No commit is complete before every quality gate succeeds.

---

## 10. Quality Audit

Review:

- architecture;
- naming;
- cohesion;
- coupling;
- testability;
- documentation;
- consistency with project conventions.

The objective is to validate implementation quality beyond automated tests.

---

## 11. Sprint Review

Summarize:

- what was implemented;
- architectural improvements;
- lessons learned;
- impact on future development.

---

## 12. Retrospective

Review the development process itself.

Typical questions:

- What worked well?
- What could improve?
- Should the workflow evolve?
- Were architectural decisions validated?

Continuous improvement applies to both software and process.

---

# Definition of Done

A Pull Request is complete only when:

- all planned commits are merged;
- documentation is updated;
- tests are passing;
- architecture remains consistent;
- `make format` succeeds;
- `make verify` succeeds;
- Quality Audit is approved.

---

# Commit Guidelines

Every commit should:

- have one responsibility;
- compile successfully;
- pass every test;
- be independently reviewable;
- keep the repository releasable.

Small commits are preferred over large commits.

---

# Review Guidelines

Every review validates:

- architecture before implementation;
- implementation before merge;
- design before optimization.

Reviews should prioritize maintainability over cleverness.

---

# Long-Term Goal

CyberLab should evolve without requiring architectural redesign.

Every Pull Request should leave the project slightly better than it was before.
