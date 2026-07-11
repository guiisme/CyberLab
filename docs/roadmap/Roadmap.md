# CyberLab Roadmap

This roadmap describes the planned evolution of CyberLab.

The roadmap is organized by capabilities rather than implementation details.

Completed milestones represent architectural foundations. Future milestones focus on expanding laboratory functionality while preserving the existing architecture.

---

# Completed

## PR #001 — Project Bootstrap

* Initial project structure
* Development tooling
* Code quality pipeline
* Testing infrastructure

---

## PR #002 — Version Command

* Version provider
* CLI version command

---

## PR #003 — Environment Doctor

* Environment verification
* Dependency checks

---

## PR #004 — Laboratory Discovery

* Filesystem repository
* Laboratory discovery
* CLI laboratory listing

---

## PR #005 — Laboratory Metadata

* YAML laboratory manifests
* Laboratory information
* Metadata model

---

## PR #006 — Laboratory Validation

* Laboratory validation
* Validation reports
* Validation renderer

---

## PR #007 — Laboratory Runner Abstraction

* LabRunnerProtocol
* Execution reports
* Infrastructure abstraction

---

## PR #008 — CLI Modularization

* Improved CLI organization
* Better command separation
* Cleaner Composition Root

---

## PR #009 — Docker Compose Runner

* DockerComposeService
* DockerComposeLabRunner
* Docker Compose execution
* First executable laboratory

---

# Next Milestone

## PR #010 — Laboratory Lifecycle

Goals:

* `lab stop`
* `lab status`
* `lab logs`

Infrastructure additions:

* Docker Compose down
* Docker Compose ps
* Docker Compose logs

No changes should be required in the Application layer.

---

# Short-Term Roadmap

## Laboratory Lifecycle

* Stop laboratories
* Restart laboratories
* Destroy laboratories
* Laboratory status
* Container logs

---

## CLI Improvements

* Better progress reporting
* Rich terminal output
* Colored execution summaries
* Interactive confirmations

---

## Laboratory Development

* Complete XSS laboratory
* SQL Injection laboratory
* SSRF laboratory
* Command Injection laboratory
* File Upload laboratory

Each laboratory should remain self-contained.

---

# Medium-Term Roadmap

## Laboratory Platform

* Multiple containers per laboratory
* Shared laboratory components
* Network isolation
* Persistent laboratory volumes

---

## Execution Backends

Introduce additional infrastructure implementations:

* Podman
* Kubernetes
* Remote execution

The Application layer should remain unchanged.

---

## Validation Improvements

* Compose validation
* Port conflict detection
* Resource validation
* Laboratory dependency validation

---

# Long-Term Roadmap

## Laboratory Marketplace

* Community laboratories
* Laboratory templates
* Versioned laboratory catalog
* Digital signatures

---

## Automation

* CI laboratory validation
* Automatic environment provisioning
* Automated cleanup
* Scheduled execution

---

## Educational Features

* Guided laboratory walkthroughs
* Integrated hints
* Learning objectives
* Progress tracking

---

# Architectural Direction

Future development should preserve the following principles:

* Clean Architecture
* Hexagonal Architecture
* Protocol-Oriented Design
* Constructor Dependency Injection
* Test-Driven Development

New capabilities should be implemented by extending Infrastructure whenever possible while keeping the Application and Domain layers stable.

The existing architectural boundaries are expected to remain valid as the project grows.
