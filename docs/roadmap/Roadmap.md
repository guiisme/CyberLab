# CyberLab Roadmap

*Last updated: July 2026 (PR #012)*

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

- [ ] Web applications
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

- [ ] Plugin discovery
- [ ] External laboratory packages
- [ ] Third-party execution adapters
- [ ] Capability extensions

---

## Documentation

- [ ] User Guide
- [ ] Laboratory Author Guide
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

Current architectural capabilities include:

- Laboratory Discovery
- Laboratory Validation
- Laboratory Lifecycle
- Environment Diagnostics

Future capabilities are expected to follow the same architectural principles.

---

# Development Principles

Every roadmap item should:

- preserve Clean Architecture;
- preserve Hexagonal Architecture;
- follow Protocol-Oriented Design;
- keep infrastructure replaceable;
- remain independently testable;
- evolve through small Pull Requests.
