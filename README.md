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
* Docker Compose, Podman and Kubernetes laboratory execution
* Engine selection through the laboratory manifest
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
 Filesystem Repository         Engine Lifecycle Resolver
             |                               |
             +---------------+---------------+
                             |
                             v
         Docker Compose / Podman / Kubernetes
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

For commands that use the laboratories in this checkout, point CyberLab at the
repository root:

```bash
export CYBERLAB_HOME="$PWD"
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

Create a lab from the default scaffold:

```bash
uv run cyberlab lab create jwt-basic
```

This creates `labs/jwt-basic/` with a valid starter manifest, documentation,
and `application/`, `scripts/`, and `seed/` directories. Add services to its
`compose.yaml` before running it.

For a ready-to-use Kali workspace, choose the official Kali scaffold and a
tool profile:

```bash
uv run cyberlab lab create kali-pentest --template kali --profile web
uv run cyberlab lab run kali-pentest
uv run cyberlab lab exec kali-pentest
```

Available profiles are `minimal`, `web`, and `network`. Use this workspace only
against laboratories and systems you are authorized to assess.

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
```

Show a laboratory status or its logs:

```bash
uv run cyberlab lab status xss-basic
uv run cyberlab lab logs xss-basic
```

Engine-specific commands are exposed under `lab` as well:

```bash
uv run cyberlab lab deploy <lab-id>
uv run cyberlab lab exec <lab-id>             # abre uma console interativa
uv run cyberlab lab exec <lab-id> -c "id"     # executa um comando
uv run cyberlab lab submit <lab-id> --flag '<flag>'
uv run cyberlab lab proxy <lab-id>
uv run cyberlab lab harden <lab-id>
uv run cyberlab lab setup-ctf <lab-id> <target>
```

For Docker Compose and Podman, `lab proxy` displays the host ports already
published by the running containers. For Kubernetes, it starts a local
`kubectl port-forward` session.

The pre-migration command surface remains available temporarily through
`uv run cyberlab legacy …`. New automation should use `cyberlab lab …`.

---

# Running Laboratories

CyberLab selects an execution engine from `lab.yaml`:

| `engine` value | Adapter |
| --- | --- |
| omitted, `docker`, or `compose` | Docker Compose |
| `podman` | Podman Compose |
| `k8s` | Kubernetes |

Each laboratory contains its own infrastructure definition.

Example:

```text
labs/
└── xss-basic/
    ├── lab.yaml
    ├── compose.yaml
    ├── web/
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

## XSS Basics example

`xss-basic` is a runnable DOM XSS training lab. It starts an Nginx target on
`http://localhost:8080` and deliberately renders the `q` query parameter with
`innerHTML`.

```bash
uv run cyberlab lab run xss-basic
uv run cyberlab lab status xss-basic
uv run cyberlab lab exec xss-basic -c "id"
```

Open `http://localhost:8080/?q=hello` in a browser to use the target. Stop it
after the exercise with `uv run cyberlab lab stop xss-basic`.

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
engine: docker
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
* Docker Compose runner and shell execution
* Podman and Kubernetes engine adapters
* Manifest-driven engine resolver
* Modular CLI

Planned:

* Multi-container laboratories
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
