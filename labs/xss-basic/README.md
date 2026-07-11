# XSS Basic Laboratory

## Overview

The **XSS Basic** laboratory is the first executable laboratory available in CyberLab.

Its purpose is to provide a reproducible environment for studying **Cross-Site Scripting (XSS)** in a safe and isolated Docker environment.

At the current stage of the project, this laboratory primarily validates the CyberLab execution infrastructure.

Future iterations will introduce intentionally vulnerable web applications covering different XSS scenarios.

---

# Objectives

This laboratory will progressively demonstrate:

* Reflected Cross-Site Scripting
* Stored Cross-Site Scripting
* DOM-based Cross-Site Scripting
* Context-aware output encoding
* Input validation
* Browser execution behavior
* Secure mitigation techniques

---

# Requirements

* Docker
* Docker Compose
* CyberLab

Verify your environment before executing the laboratory:

```bash
uv run cyberlab doctor
```

---

# Running the Laboratory

Start the laboratory:

```bash
uv run cyberlab lab run xss-basic
```

CyberLab will execute the Docker Compose environment defined by this laboratory.

After the environment starts, open:

```text
http://localhost:8000
```

---

# Stopping the Laboratory

Until lifecycle management commands are introduced, stop the laboratory manually:

```bash
docker compose \
    -f labs/xss-basic/compose.yaml \
    down
```

Future versions of CyberLab will provide:

```bash
uv run cyberlab lab stop xss-basic
```

---

# Laboratory Structure

```text
xss-basic/
├── README.md
├── compose.yaml
└── lab.yaml
```

## lab.yaml

Contains the laboratory metadata.

Examples include:

* identifier
* name
* category
* difficulty
* version

---

## compose.yaml

Defines the execution environment.

CyberLab delegates execution to Docker Compose through the Infrastructure layer.

---

# Current Status

Current implementation:

* Executable through CyberLab
* Docker Compose environment
* Infrastructure validation

Planned implementation:

* Vulnerable web application
* Guided exercises
* Exploitation scenarios
* Mitigation examples
* Educational walkthroughs

---

# Learning Goals

After completing this laboratory, users should understand:

* how Cross-Site Scripting works;
* why browsers execute injected JavaScript;
* how different XSS variants behave;
* common mitigation strategies;
* how CyberLab provisions isolated laboratory environments.

---

# Safety

This laboratory is intentionally designed for educational purposes.

It should only be executed inside controlled environments.

Never expose intentionally vulnerable applications to public networks.

---

# Related Documentation

Project documentation:

```text
docs/
```

Architecture overview:

```text
docs/architecture/
```

Architecture decisions:

```text
docs/adr/
```

Project roadmap:

```text
docs/roadmap/
```
