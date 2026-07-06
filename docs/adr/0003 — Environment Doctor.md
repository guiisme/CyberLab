# ADR-0003 — Environment Doctor

## Status

Accepted

## Contexto

O CyberLab precisava de um mecanismo simples para validar se o ambiente do usuário está preparado para executar os laboratórios.

Também era necessário exercitar, pela primeira vez, toda a arquitetura definida para o projeto:

* Domain
* Application
* Infrastructure
* CLI
* Dependency Injection
* Protocols

## Decisão

Foi implementado o comando `cyberlab doctor`.

O fluxo oficial é:

```text
CLI
    ↓
DoctorUseCase
    ↓
CommandRunnerProtocol
    ↓
CommandRunner
```

O caso de uso depende apenas de um `CommandRunnerProtocol`, permitindo diferentes implementações sem alterar a lógica da Application.

O resultado da execução é representado por um `DoctorReport`, composto por diversos `CheckResult`.

`ProcessResult` foi promovido ao Domain por representar exclusivamente dados imutáveis, sem dependência tecnológica.

## Consequências

### Benefícios

* Forte desacoplamento entre camadas.
* Testes determinísticos usando Fakes.
* Facilidade para adicionar novas verificações.
* Baixo acoplamento com a Infrastructure.

### Trade-offs

* Maior número de objetos em comparação com uma implementação procedural.
* Necessidade de criar Protocols para pontos de integração.

## Decisões relacionadas

* Uso de Protocols (PEP 544) em vez de classes abstratas.
* Dependency Injection obrigatória para Use Cases.
* Preferência por Fakes em vez de Mocks.
* Reports como retorno oficial dos casos de uso.
* Modelos de domínio imutáveis utilizando `@dataclass(frozen=True, slots=True)`.
