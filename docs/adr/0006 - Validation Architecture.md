# ADR-0006 — Validation Architecture

## Status

Accepted

## Context

CyberLab needs a reusable mechanism to validate different kinds of resources such as laboratories, packages and scenarios.

Validation logic should remain independent from the CLI and reusable across different commands.

## Decision

Validation responsibilities are divided into three components:

* Validator Protocol
* Validator Implementation
* Validation Report

Validation results are represented by immutable domain Reports composed of `CheckResult` objects.

CLI commands only render these reports.

## Consequences

Positive:

* Validation logic is reusable.
* CLI remains free of business rules.
* Validation reports can be reused by future commands.

Negative:

* Additional classes are introduced.
* Validation always requires a Report object instead of primitive values.
