# Changelog

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
