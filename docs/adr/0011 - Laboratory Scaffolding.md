# ADR 0011 — Laboratory Scaffolding

- Status: Accepted
- Date: July 2026

---

# Context

Prior to this decision, new laboratories were created manually by copying an
existing laboratory and adapting its files.

This approach presented several drawbacks:

- inconsistent directory structures;
- duplicated boilerplate;
- increased maintenance effort;
- no official reference for laboratory layout.

As CyberLab evolves into a long-term framework for reproducible cybersecurity
laboratories, creating new laboratories should become a first-class capability
rather than a manual process.

---

# Decision

CyberLab introduces an official laboratory scaffolding capability.

Laboratories are now created from an official scaffold through the command:

```bash
cyberlab lab create <lab-id>
```

The implementation follows the existing architecture:

```text
CLI
    ↓
Application
    ↓
LabScaffoldingProtocol
    ↓
FilesystemLabScaffolding
    ↓
Filesystem
```

The official scaffold is stored under:

```text
scaffolds/
└── default/
```

The scaffold defines the canonical directory structure for every new laboratory.

Placeholder replacement is performed during scaffold generation.

The initial supported placeholders are:

- `{{LAB_ID}}`
- `{{LAB_NAME}}`

Dependency creation remains centralized inside the Composition Root.

The Application layer remains independent from filesystem concerns.

---

# Consequences

## Positive

- Standardized laboratory structure.
- Reduced boilerplate.
- Lower maintenance cost.
- Consistent onboarding experience.
- Infrastructure remains replaceable.
- Future scaffolds can reuse the same protocol.

## Negative

A scaffold becomes a permanent project artifact and must evolve together with
the architecture.

Changes to the scaffold should be carefully reviewed because they affect every
future laboratory.

---

# Future Evolution

The current implementation intentionally supports future extensions without
architectural changes.

Possible future capabilities include:

- multiple official scaffolds;
- community scaffolds;
- plugin-provided scaffolds;
- remote scaffold repositories;
- scaffold versioning.

These extensions should reuse the existing `LabScaffoldingProtocol` whenever
possible.

---

# Alternatives Considered

## Manual laboratory creation

Rejected because it duplicates project structure and encourages divergence
between laboratories.

## Generating files programmatically

Rejected because the laboratory structure becomes embedded in Python code,
making templates harder to review and evolve.

Filesystem-based scaffolds provide a simpler and more maintainable solution.

---

# Architectural Notes

Laboratory scaffolding is considered an infrastructure capability.

The scaffold itself is not a laboratory.

Official laboratories are independent artifacts created from the scaffold and
serve as reference implementations for the project.

The introduction of laboratory scaffolding reinforces CyberLab's goal of being
both a laboratory execution platform and a laboratory creation framework.
