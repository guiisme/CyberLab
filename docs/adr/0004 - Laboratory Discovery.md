# ADR-0004 — Laboratory Discovery

## Status

Accepted

## Context

CyberLab requires a mechanism to discover the laboratories available in the local workspace.

The CLI must be able to list laboratories without reading their metadata or depending on implementation details such as the filesystem.

The discovery mechanism should remain independent from the command-line interface and easily replaceable by alternative implementations in the future (for example, remote repositories or packaged laboratory collections).

## Decision

Laboratory discovery is divided into three responsibilities:

* **Lab**: immutable domain model representing a discovered laboratory.
* **LabRepositoryProtocol**: Application contract responsible for listing available laboratories.
* **FilesystemLabRepository**: Infrastructure implementation that discovers laboratories from the local `labs/` directory.

The CLI delegates discovery to `ListLabsUseCase`, which depends only on `LabRepositoryProtocol`.

The dependency graph is therefore:

```text
CLI
    │
    ▼
ListLabsUseCase
    │
    ▼
LabRepositoryProtocol
    ▲
    │
FilesystemLabRepository
```

Tests use `FakeLabRepository`, allowing the Application layer to be tested without filesystem access.

## Consequences

### Positive

* The Application layer is independent from filesystem APIs.
* Laboratory discovery can be replaced by other implementations without modifying business logic.
* Unit tests remain deterministic and fast by using in-memory Fakes.
* The CLI contains no discovery logic.
* Discovery and metadata loading evolve independently.

### Negative

* Additional abstractions are introduced.
* Every new repository implementation must implement `LabRepositoryProtocol`.

## Alternatives Considered

### Access the filesystem directly from the CLI

Rejected because it couples presentation and infrastructure, making the CLI harder to test and maintain.

### Load laboratory metadata during discovery

Rejected because discovery and metadata are separate concerns.

Listing laboratories should remain lightweight and avoid unnecessary file parsing. Metadata is retrieved separately through `LabInfoUseCase` and `LabManifestLoaderProtocol`.

## Notes

This ADR establishes the standard repository pattern used throughout CyberLab:

* The **Application** defines repository contracts.
* The **Infrastructure** provides concrete implementations.
* The **CLI** depends exclusively on Use Cases.
* Tests rely on **Fake** implementations rather than real infrastructure.

This decision also prepares the architecture for future repository implementations, such as remote registries, packaged laboratories or cloud-based catalogs, without impacting the Application layer.
