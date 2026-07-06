# ADR-0002 — Value Objects

* **Status:** Accepted
* **Date:** 2026-07-05

## Context

À medida que o CyberLab evolui, novos objetos passam a representar conceitos importantes do domínio e da infraestrutura.

Exemplos:

* CheckResult
* ProcessResult

Esses objetos não possuem identidade própria nem ciclo de vida. Eles representam apenas um valor em um determinado momento.

É importante estabelecer uma convenção consistente para sua implementação.

---

# Decision

Todos os **Value Objects** do CyberLab deverão seguir as seguintes regras.

## 1. Utilizar dataclasses

Todo Value Object será implementado utilizando:

```python
@dataclass(...)
```

---

## 2. Ser imutável

Todo Value Object deverá utilizar:

```python
frozen=True
```

Após criado, seu estado não poderá ser alterado.

---

## 3. Utilizar slots

Todo Value Object deverá utilizar:

```python
slots=True
```

Objetivos:

* reduzir consumo de memória;
* impedir atributos dinâmicos;
* tornar o modelo mais previsível.

---

## 4. Representar apenas estado

Um Value Object representa apenas dados relacionados ao próprio conceito.

Ele não executa operações de infraestrutura.

Exemplo:

Correto:

* CheckResult
* ProcessResult

Incorreto:

* executar Docker;
* executar Git;
* abrir arquivos;
* acessar banco de dados.

---

## 5. Não possuir identidade

Dois Value Objects com os mesmos atributos representam exatamente o mesmo valor.

Exemplo:

```python
ProcessResult(0, "ok", "") ==
ProcessResult(0, "ok", "")
```

---

## 6. Não depender de frameworks

Value Objects não conhecem:

* Typer
* Rich
* Docker
* Git
* subprocess

Eles pertencem exclusivamente ao modelo do CyberLab.

---

## Consequences

### Benefícios

* Objetos previsíveis.
* Facilidade de testes.
* Igualdade automática.
* Baixo acoplamento.
* Melhor legibilidade.
* Menor consumo de memória.

### Custos

* Objetos imutáveis exigem criação de novas instâncias quando alterações forem necessárias.
* Algumas operações exigirão transformação em novos objetos em vez de mutação.

---

## Examples

```python
@dataclass(frozen=True, slots=True)
class CheckResult:
    name: str
    success: bool
    message: str
```

```python
@dataclass(frozen=True, slots=True)
class ProcessResult:
    exit_code: int
    stdout: str
    stderr: str
```

---

## Future Revisions

Caso o projeto passe a utilizar entidades de domínio com identidade própria, elas seguirão um padrão diferente deste ADR.
