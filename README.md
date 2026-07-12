# CyberLab

> Build, validate and execute reproducible cybersecurity laboratories.

CyberLab is an open-source framework for building reproducible cybersecurity laboratories using **Clean Architecture**, **Hexagonal Architecture**, and **Test-Driven Development (TDD)**.

The project is designed to keep business rules independent from infrastructure, making laboratories easy to maintain, extend and automate.

---

# Features

* Clean Architecture
* Hexagonal Architecture
* Dependency Injection
* Protocol-based design (PEP 544)
* Test-Driven Development
* Docker Compose laboratory execution
* YAML laboratory manifests
* Modular CLI
* Infrastructure-independent Application layer

---

# Project Architecture

```text
                   +--------------------+
                   |        CLI         |
                   +---------+----------+
                             |
                             v
                   +--------------------+
                   |    Use Cases       |
                   +---------+----------+
                             |
             +---------------+---------------+
             |                               |
             v                               v
      Repository Protocol             Runner Protocol
             |                               |
             v                               v
 Filesystem Repository         Docker Compose Runner
             |                               |
             +---------------+---------------+
                             |
                             v
                     Docker Compose
```

The Application layer never depends on Infrastructure.

Infrastructure implements the interfaces defined by the Application layer.

---

# Project Structure

```text
.
├── docs/
├── labs/
├── src/
│   └── cyberlab/
│       ├── application/
│       ├── cli/
│       ├── domain/
│       ├── infrastructure/
│       └── shared/
├── tests/
├── pyproject.toml
└── README.md
```

---

# Installation

## Requirements

* Python 3.12+
* Docker
* Docker Compose
* uv

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

# Verify the Environment

```bash
uv run cyberlab doctor
```

---

# CLI

Show version:

```bash
uv run cyberlab version
```

List laboratories:

```bash
uv run cyberlab lab list
```

Show laboratory information:

```bash
uv run cyberlab lab info xss-basic
```

Validate a laboratory:

```bash
uv run cyberlab lab validate xss-basic
```

Run a laboratory:

```bash
uv run cyberlab lab run xss-basic
```

Stop a laboratory

```bash
uv run cyberlab lab stop xss-basic

---

# Running Laboratories

CyberLab executes laboratories through Docker Compose.

Each laboratory contains its own infrastructure definition.

Example:

```text
labs/
└── xss-basic/
    ├── lab.yaml
    ├── compose.yaml
    └── README.md
```

Executing:

```bash
uv run cyberlab lab run xss-basic
```

internally runs:

```bash
docker compose \
    -f labs/xss-basic/compose.yaml \
    up -d
```

---

# Laboratory Manifest

Each laboratory is described by a YAML manifest.

Example:

```yaml
id: xss-basic
name: Basic Cross-Site Scripting
category: web
difficulty: beginner
version: "1.0.0"
```

---

# Development

Format code:

```bash
make format
```

Run all checks:

```bash
make verify
```

Run tests:

```bash
pytest
```

---

# Design Principles

CyberLab follows these principles:

* Single Responsibility Principle
* Dependency Inversion Principle
* Composition Root
* Protocol-oriented design
* Constructor Dependency Injection
* Infrastructure isolation
* Fakes preferred over mocks
* Small and reviewable pull requests

---

# Current Status

Implemented:

* Project bootstrap
* Version command
* Environment doctor
* Laboratory discovery
* Laboratory metadata
* Laboratory validation
* Laboratory runner abstraction
* Docker Compose runner
* Modular CLI

Planned:

* Stop laboratories
* Laboratory logs
* Laboratory status
* Shell access
* Multi-container laboratories
* Podman support
* Kubernetes runner
* Remote execution
* Laboratory marketplace

---

# Documentation

Additional documentation is available in:

```text
docs/
├── adr/
├── architecture/
└── roadmap/
```

---

# Contributing

Contributions are welcome.

Before opening a Pull Request:

```bash
make verify
```

All new functionality should:

* follow TDD;
* keep Application independent from Infrastructure;
* include unit tests;
* preserve backward compatibility whenever possible.

---

# License

This project is licensed under the MIT License.
