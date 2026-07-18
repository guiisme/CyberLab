# Changelog

## [1.0.0] - 2026-07-17

### Added

* Typer composition root with the `cyberlab lab` command group.
* Manifest-driven engine selection for Docker Compose, Podman, and Kubernetes.
* `lab deploy`, `exec`, `submit`, `proxy`, `harden`, and `setup-ctf` commands.
* Docker Compose shell execution through container discovery and `docker exec`.
* A runnable `xss-basic` DOM XSS laboratory served by Nginx.

### Changed

* Standardized lifecycle routing through `EngineLabLifecycle`.
* Aligned the Podman adapter with the lifecycle contract.
* Made the package registry export lazy to prevent import-time cycles.
* Updated CLI, architecture, and laboratory documentation for the new runtime.

### Compatibility

* The pre-migration command surface remains available temporarily through
  `cyberlab legacy`.

## [0.3.0] - Unreleased

### Added

* Novo comando `cyberlab doctor` para verificar a saúde do ambiente de desenvolvimento.
* `DoctorUseCase` como primeiro caso de uso completo da arquitetura.
* `DoctorReport` como primeiro Report do domínio.
* `CheckResult` para representar o resultado individual de cada verificação.
* `CommandRunnerProtocol` baseado em PEP 544.
* `FakeCommandRunner` para testes da camada de Application.
* Testes unitários cobrindo Domain, Application, Infrastructure e CLI.

### Changed

* `ProcessResult` foi movido da Infrastructure para o Domain por representar apenas dados imutáveis.
* A Application passou a depender exclusivamente de Protocols para execução de comandos.
* A estratégia oficial de testes passou a privilegiar Dependency Injection e Fakes em vez de Mocks.

### Documentation

* Documentada a arquitetura do Environment Doctor.
* Formalizada a estratégia de testes do projeto.
* Atualizadas as convenções para Use Cases, Reports e Dependency Injection.

### Internal

* Revisão da organização da PR #003 seguindo o fluxo RED → GREEN → REFACTOR.
* Consolidação das decisões arquiteturais da série v0.x.

## [0.4.0] - 2026-06-06

### Added

- Introduced the `Lab` domain model.
- Added `LabRepositoryProtocol`.
- Implemented `FilesystemLabRepository`.
- Added `FakeLabRepository` for unit tests.
- Added `ListLabsUseCase`.
- Added `cyberlab lab list` CLI command.

### Changed

- Standardized application use cases around the `execute()` convention.
- Improved CLI dependency composition.

### Tests

- Added unit tests for lab repository.
- Added unit tests for lab use case.
- Added CLI tests for lab listing.

## [0.5.0] - 2026-06-06

### Added

- Added `LabManifest` domain model.
- Added `LabManifestLoaderProtocol`.
- Added `YamlLabManifestLoader`.
- Added `FakeLabManifestLoader`.
- Added `LabInfoUseCase`.
- Added `cyberlab lab info` command.

### Changed

- Extended the CLI Composition Root to inject the manifest loader.
- Standardized metadata loading through application protocols.

### Tests

- Added unit tests for the YAML manifest loader.
- Added unit tests for the fake manifest loader.
- Added unit tests for `LabInfoUseCase`.
- Added CLI tests for `lab info`.

## [0.6.0] - 2026-07-06

### Added

* Added `LabValidationReport`.
* Added `LabValidatorProtocol`.
* Added `FilesystemLabValidator`.
* Added `FakeLabValidator`.
* Added `LabValidationUseCase`.
* Added `cyberlab lab validate` command.

### Changed

* Introduced a shared CLI rendering function for validation checks.
* Standardized laboratory validation through Application Protocols.
* Added support for reusable validation reports based on `CheckResult`.

### Tests

* Added unit tests for `FilesystemLabValidator`.
* Added unit tests for `FakeLabValidator`.
* Added unit tests for `LabValidationUseCase`.
* Added CLI tests for `lab validate`.
