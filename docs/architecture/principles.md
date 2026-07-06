# CyberLab Engineering Principles

## Purpose

O CyberLab é um framework para criação de laboratórios reproduzíveis de Cybersecurity.

Este documento define os princípios de engenharia que orientam toda a evolução do projeto. Alterações nestes princípios devem ser raras e justificadas por meio de uma ADR.

---

# Core Principles

## Simplicidade

Preferimos soluções simples antes de introduzir abstrações.

Toda abstração deve resolver um problema existente, não um problema hipotético.

Aplicamos o princípio **YAGNI (You Aren't Gonna Need It)** sempre que possível.

---

## Evolução Incremental

O projeto evolui por meio de pequenos commits e Pull Requests.

Cada commit deve introduzir apenas um novo conceito.

Cada Pull Request deve possuir um objetivo claro e bem definido.

---

## Clean Architecture

As dependências sempre apontam para o centro da aplicação.

Fluxo oficial:

```text
CLI
│
▼
Application (Use Cases)
│
▼
Application Interfaces (Protocols)
▲
│
Infrastructure
│
▼
Domain
```

Regras:

* Domain não depende de nenhuma camada.
* Application depende apenas do Domain e de Protocols.
* Infrastructure implementa os Protocols.
* CLI adapta entrada e saída, sem conter regras de negócio.

---

# Domain First

O Domain representa apenas conceitos do negócio.

Não deve conhecer:

* subprocess
* Docker
* Typer
* sistema de arquivos
* variáveis de ambiente
* bibliotecas externas

Os modelos do domínio devem ser preferencialmente:

* imutáveis;
* pequenos;
* previsíveis.

Sempre que possível:

```python
@dataclass(frozen=True, slots=True)
```

---

# Use Cases

Toda regra de negócio deve estar em um Use Case.

Convenção oficial:

```python
class SomeUseCase:

    def __init__(...)

    def execute(...)
```

`execute()` é o único método público.

Toda lógica auxiliar permanece privada.

---

# Dependency Injection

Use Cases nunca instanciam dependências diretamente.

Todas as integrações são recebidas pelo construtor.

Exemplo:

```python
DoctorUseCase(CommandRunnerProtocol)
```

Essa abordagem reduz o acoplamento e facilita testes.

---

# Protocols

Interfaces entre Application e Infrastructure devem utilizar Protocols (PEP 544).

Preferimos Protocols a classes abstratas sempre que apenas um contrato é necessário.

---

# Reports

Casos de uso retornam objetos de domínio que representam o resultado da operação.

Evitamos retornar:

* dict
* tuple
* list

Preferimos Reports explícitos, como:

* DoctorReport
* PackageReport
* LabReport

---

# Testing Strategy

Cada camada testa apenas sua responsabilidade.

## Domain

Testa regras de negócio.

## Application

Testa orquestração.

## Infrastructure

Testa integração com tecnologias externas.

## CLI

Testa entrada, saída e adaptação.

---

# Fakes over Mocks

Preferimos Fakes a Mocks.

Fakes:

* são determinísticos;
* implementam os mesmos Protocols da Infrastructure;
* tornam os testes mais legíveis;
* reduzem acoplamento aos detalhes de implementação.

O uso de `unittest.mock` deve ser exceção, não regra.

---

# Commit Philosophy

Todo desenvolvimento segue o fluxo:

```text
Design Review
↓
RED
↓
GREEN
↓
REFACTOR
↓
Code Review
↓
Commit
```

Todos os commits seguem o padrão Conventional Commits.

---

# Definition of Ready

Antes de iniciar uma implementação:

* problema compreendido;
* escopo definido;
* arquitetura definida;
* contrato definido;
* estratégia de testes planejada.

---

# Definition of Done

Antes de concluir qualquer Pull Request:

```bash
make format

make verify

git status

git show --stat HEAD
```

Além disso:

* todos os testes devem estar verdes;
* nenhuma camada deve violar a arquitetura oficial;
* todas as dependências devem ser injetadas;
* a documentação deve estar atualizada quando houver mudanças de arquitetura ou comportamento.

---

# Long-term Vision

O CyberLab deve permanecer:

* simples de compreender;
* fácil de testar;
* desacoplado;
* evolutivo;
* consistente entre todas as funcionalidades.

Novas funcionalidades devem seguir estes princípios, preservando a arquitetura estabelecida para a série v0.x.

## Fake Objects

The project adopts Fakes as the preferred test double strategy.

Every Fake should:

- implement the corresponding Protocol;
- be fully in-memory;
- receive its initial state through the constructor;
- record relevant interactions performed by the system under test;
- fail explicitly when receiving unexpected input;
- never depend on the filesystem, network or subprocesses.

Fakes should remain simple and deterministic.
