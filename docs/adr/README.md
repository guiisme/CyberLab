# Architecture Decision Records (ADR)

This directory contains the Architecture Decision Records (ADRs) for the CyberLab project.

ADRs document significant architectural decisions, their context, rationale and consequences.

## What is an ADR?

An Architecture Decision Record captures:

* the problem being solved;
* the decision that was made;
* the reasoning behind the decision;
* the expected consequences.

ADRs are immutable historical records. New decisions should be documented in new ADRs rather than modifying existing ones.

---

# Index

| ADR      | Title               | Status   |
| -------- | ------------------- | -------- |
| ADR-0001 | Project Conventions | Accepted |
| ADR-0002 | Value Objects       | Accepted |

---

# Writing Guidelines

Each ADR should follow this structure:

1. Status
2. Date
3. Context
4. Decision
5. Consequences
6. Future Revisions (optional)

---

# Status Definitions

| Status     | Description               |
| ---------- | ------------------------- |
| Proposed   | Under discussion          |
| Accepted   | Official project decision |
| Superseded | Replaced by another ADR   |
| Deprecated | No longer recommended     |

---

# Naming Convention

ADR files use sequential numbering.

Example:

```text
0001-project-conventions.md
0002-value-objects.md
0003-process-runner.md
```

Numbers are never reused.

---

# Relationship with Architecture Documentation

The documentation is organized as follows:

```text
docs/
├── adr/
│   ├── README.md
│   ├── 0001-project-conventions.md
│   ├── 0002-value-objects.md
│   └── ...
│
└── architecture/
    ├── principles.md
    ├── overview.md
    └── ...
```

* **Architecture Principles** define long-term engineering principles.
* **ADRs** record individual architectural decisions.
* **Overview** describes the current system architecture.

Together, these documents provide a complete picture of the project's evolution.

## Environment Doctor

O CyberLab fornece o comando `doctor` para validar se o ambiente possui os requisitos necessários para executar os laboratórios.

### Uso

```bash
cyberlab doctor
```

O comando executa uma série de verificações e apresenta um relatório resumido do ambiente.

Exemplo:

```text
✔ Python
✔ Git
✔ Docker

Environment OK
```

### Arquitetura

O fluxo segue a arquitetura oficial do projeto:

```text
CLI
    ↓
DoctorUseCase
    ↓
CommandRunnerProtocol
    ↓
CommandRunner
```

Cada camada possui responsabilidade única:

* **CLI**: recebe argumentos e renderiza a saída.
* **Application**: orquestra as verificações.
* **Infrastructure**: executa comandos do sistema operacional.
* **Domain**: representa os resultados das verificações.

O `DoctorUseCase` retorna um `DoctorReport`, que agrega todos os `CheckResult` produzidos durante a execução.
