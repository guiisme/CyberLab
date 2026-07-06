# ADR-0001 — Project Conventions

* **Status:** Accepted
* **Date:** 2026-07-05

## Context

Durante a Sprint 0 e as PRs iniciais do CyberLab foram definidas convenções de arquitetura, qualidade e desenvolvimento que servirão como base para todo o projeto.

Este ADR documenta essas decisões para garantir consistência, facilitar contribuições futuras e reduzir retrabalho.

---

# Decision

## 1. Project Layout

O CyberLab utilizará o padrão **src layout**.

```text
src/
└── cyberlab/
```

Todo código de produção deverá permanecer dentro de `src/cyberlab`.

---

## 2. Package Convention

Todos os diretórios da árvore `src/` que representam pacotes Python deverão conter um arquivo `__init__.py`.

Exemplo:

```text
src/cyberlab/
    application/
        __init__.py
        use_cases/
            __init__.py
```

A árvore `tests/` não utilizará `__init__.py`, salvo necessidade técnica devidamente justificada.

---

## 3. Architecture

O projeto adota uma arquitetura em camadas.

```text
CLI
    ↓
Application
    ↓
Shared
```

Responsabilidades:

* **CLI**: interface com o usuário.
* **Application**: casos de uso.
* **Shared**: funcionalidades reutilizáveis sem dependência de interface.

Dependências sempre apontam para baixo.

Camadas inferiores nunca conhecem camadas superiores.

---

## 4. CLI Architecture

A interface de linha de comando utiliza Typer.

Estrutura:

```text
cli/
    app.py
    registry.py
    commands/
```

Responsabilidades:

* `app.py` cria a aplicação.
* `registry.py` registra os comandos.
* Cada módulo em `commands/` registra apenas seus próprios comandos.

---

## 5. Testing Strategy

O desenvolvimento segue TDD.

Fluxo obrigatório:

```text
RED
GREEN
REFACTOR
```

Todo comportamento novo deve ser acompanhado por testes automatizados.

---

## 6. Pytest Configuration

O projeto utiliza:

```toml
addopts = ["--import-mode=importlib"]
```

Essa configuração evita conflitos entre módulos de teste com o mesmo nome.

---

## 7. Quality Gate

Nenhum commit deve ser realizado sem que o pipeline de qualidade esteja totalmente verde.

Checklist obrigatório:

* Ruff
* Ruff Format
* MyPy
* Pytest

Executado através de:

```bash
make verify
```

---

## 8. Pre-commit

Todos os commits passam pelos hooks do pre-commit.

Os hooks fazem parte da qualidade do projeto e não devem ser ignorados.

---

## 9. Git Workflow

Cada commit deve possuir apenas uma responsabilidade.

Convenções:

* `feat`
* `fix`
* `refactor`
* `test`
* `docs`
* `chore`

Mensagens seguem o padrão Conventional Commits.

---

## 10. Development Workflow

Fluxo oficial:

```text
Issue

↓

Design Review

↓

RED

↓

GREEN

↓

REFACTOR

↓

make format

↓

make verify

↓

git status

↓

git add .

↓

git commit

↓

Pull Request
```

---

## Consequences

### Benefícios

* Arquitetura consistente.
* Baixo acoplamento.
* Facilidade para testes.
* Histórico Git organizado.
* Qualidade automatizada.
* Escalabilidade para novos módulos.

### Custos

* Processo de desenvolvimento mais disciplinado.
* Pequeno aumento no tempo de implementação devido às validações automáticas.

---

## Future Revisions

Este ADR deverá ser revisado quando houver mudanças significativas na arquitetura, na estratégia de testes ou no fluxo de desenvolvimento.
