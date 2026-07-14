# CyberLab Roadmap

*Last updated: July 2026 (PR #015)*

---

# Vision

CyberLab aims to become a reference implementation for reproducible cybersecurity
laboratories built on Clean Architecture, Hexagonal Architecture and
Protocol-Oriented Design.

The roadmap is organized by architectural capabilities rather than implementation
details.

---

# Current Milestone

## Core Laboratory Platform

### Discovery

- [x] Laboratory discovery
- [x] Laboratory metadata
- [x] Laboratory information

### Validation

- [x] Laboratory validation

### Lifecycle

- [x] Run
- [x] Stop
- [x] Status
- [x] Restart

### Environment

- [x] Environment doctor

### CLI

- [x] Version command
- [x] Rich terminal output
- [x] Plugin listing

---

# Next Milestone

## Laboratory Observability

### Logs

- [x] Show laboratory logs
- [x] Follow logs (`--follow`)
- [x] Tail logs (`--tail`)
- [x] Service filtering

---

# Future Milestones

## Laboratory Templates

- [x] Web applications
- [ ] API laboratories
- [ ] Authentication laboratories
- [ ] Cloud laboratories
- [ ] Container security laboratories

---

## Execution Backends

Current backend:

- [x] Docker Compose

Future adapters:

- [ ] Podman
- [ ] Kubernetes
- [ ] Remote execution
- [ ] Cloud-native execution

---

## Plugin Architecture

- [x] Plugin discovery
- [x] Plugin loading
- [x] Plugin registry
- [x] Plugin CLI
- [ ] Plugin SDK
- [ ] Official plugins
- [ ] Plugin discovery
- [ ] External laboratory packages
- [ ] Third-party execution adapters
- [ ] Capability extensions

---

## Documentation

- [ ] User Guide
- [ ] Laboratory Author Guide
- [ ] Plugin Development Guide
- [ ] Plugin Development Guide
- [ ] Architecture Handbook

---

# Long-Term Goals

- Stable architecture
- Reproducible laboratories
- Educational platform
- Extensible execution model
- Excellent developer experience

---

# Architectural Evolution

The project evolves by extending existing architectural capabilities instead of
creating isolated implementations.

CCurrent architectural capabilities include:

- Laboratory Discovery
- Laboratory Validation
- Laboratory Scaffolding
- Laboratory Lifecycle
- Plugin Architecture
- Environment Diagnostics

Future capabilities are expected to follow the same architectural principles.

---

# Architecture Roadmap

Future architectural evolution should continue following the incremental
development model established during PR #015.

Preferred capability evolution order:

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

Each Pull Request should introduce a single architectural concept while
preserving a releasable repository state.

---

# Development Principles

Every roadmap item should:

- preserve Clean Architecture;
- preserve Hexagonal Architecture;
- follow Protocol-Oriented Design;
- keep infrastructure replaceable;
- remain independently testable;
- evolve through small Pull Requests;
- introduce one architectural concept per Pull Request increment.
