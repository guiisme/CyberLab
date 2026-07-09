# CyberLab Testing Architecture

## Purpose

This document describes the testing architecture adopted by CyberLab.

Its purpose is to explain how the project's architecture supports reliable, isolated and maintainable automated tests.

Implementation details, testing frameworks and individual test cases are intentionally outside the scope of this document.

---

# Testing Philosophy

Testing is considered an architectural concern rather than a final validation step.

CyberLab is designed so that business logic can be validated independently from technical implementations and external resources.

The architecture prioritizes:

* deterministic behavior;
* isolated business logic;
* explicit dependencies;
* reproducible tests;
* fast feedback.

---

# Testing Pyramid

CyberLab follows a testing strategy based on the Testing Pyramid.

```text
                 E2E
                  ▲
             Integration
                  ▲
               Unit Tests
```

The majority of automated tests should be unit tests.

* Unit tests validate isolated behavior.
* Integration tests validate interactions between architectural components.
* End-to-end tests validate complete user workflows.

---

# Testing by Architectural Layer

## Domain

Domain tests execute independently from infrastructure, external resources and presentation concerns.

Their purpose is to validate business concepts, business rules and domain behavior.

---

## Application

Application tests validate business orchestration.

External behavior is replaced by implementations of the same Protocol contracts, allowing Use Cases to be tested independently from technical implementations.

Application tests validate:

* business workflows;
* interactions with Protocols;
* application behavior;
* business outcomes.

---

## Infrastructure

Infrastructure tests verify that technical adapters correctly implement the contracts defined by the Application.

These tests may interact with external resources when required to validate technical integrations.

---

## CLI

CLI tests validate the presentation layer.

Typical responsibilities include:

* command parsing;
* dependency composition;
* output rendering;
* exit codes.

Business rules are validated by the Application rather than by the CLI.

---

# Dependency Isolation

Architectural dependencies are isolated through Protocols.

Production environments use concrete implementations.

Test environments replace those implementations with test doubles that satisfy the same contracts.

```text
Production

Use Case
    │
    ▼
Protocol
    ▲
    │
Infrastructure

------------------------------------

Tests

Use Case
    │
    ▼
Protocol
    ▲
    │
Test Double

(e.g. Fake)
```

This architectural boundary allows business logic to be tested without relying on technical implementations.

---

# Test Doubles

Test environments replace production implementations with Test Doubles.

Test doubles should:

* implement the same Protocol contracts;
* behave deterministically;
* remain simple and predictable;
* support isolated testing.

The choice of a specific testing technique (Fake, Mock, Stub or Spy) is an implementation concern rather than an architectural requirement.

---

# Composition Root

Production and test environments assemble different dependency graphs while preserving the same architectural boundaries.

Production uses concrete infrastructure implementations.

Tests compose equivalent graphs using test doubles.

This allows the same Application code to execute in different environments without architectural changes.

---


# Architectural Goals

The testing architecture supports the following goals:

* confidence during refactoring;
* rapid feedback;
* isolated validation of business logic;
* replaceable technical implementations;
* long-term maintainability.

Testing is considered a natural consequence of a well-designed architecture rather than a separate engineering activity.

---

## Terminology

This document uses the term **Test Double** as the generic name for testing implementations that replace production dependencies.

Examples include:

- Fake
- Stub
- Mock
- Spy

CyberLab currently favors Fake implementations because they provide predictable behavior while preserving architectural boundaries.

---

# References

Additional architectural context is available in:

* `docs/AI_CONTEXT.md`
* `docs/architecture/overview.md`
* `docs/architecture/principles.md`
* `docs/adr/`
