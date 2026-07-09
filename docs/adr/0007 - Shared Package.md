# ADR-0007 — Shared Package

**Status:** Accepted
**Data:** 2026-07-07

---

# Contexto

À medida que o CyberLab evolui, torna-se natural o surgimento de componentes reutilizáveis por diferentes partes do sistema.

Em muitos projetos, diretórios como `shared`, `common`, `utils` ou `core` acabam se tornando um repositório genérico para qualquer tipo de código, resultando em:

* responsabilidades mal definidas;
* aumento do acoplamento;
* dificuldade para localizar componentes;
* degradação gradual da arquitetura.

Para evitar esse problema desde o início do projeto, o CyberLab estabelece regras explícitas para a utilização do pacote `shared`.

---

# Decisão

O pacote `shared` **não faz parte da arquitetura do CyberLab**.

Ele existe exclusivamente como um mecanismo de organização de código para componentes técnicos reutilizáveis que **não pertencem legitimamente a nenhuma camada arquitetural**.

A arquitetura oficial do projeto permanece composta apenas pelas seguintes camadas:

* Domain
* Application
* Infrastructure
* CLI

O pacote `shared` é um recurso de organização do código-fonte e não deve ser tratado como uma camada arquitetural.

---

# Critério de Utilização

Antes de criar qualquer componente em `shared`, deve-se responder, obrigatoriamente, às seguintes perguntas, nesta ordem:

1. O componente pertence ao **Domain**?
2. O componente pertence à **Application**?
3. O componente pertence à **Infrastructure**?
4. O componente pertence à **CLI**?

Se a resposta for **"sim"** para qualquer uma dessas perguntas, o componente **deve** ser implementado na camada correspondente.

Somente quando a resposta for **"não" para todas as perguntas** o componente poderá ser colocado em `shared`.

Esse processo garante que `shared` seja utilizado apenas quando nenhuma camada arquitetural representar corretamente a responsabilidade do componente.

---

# Componentes Permitidos

O pacote `shared` pode conter apenas componentes técnicos independentes da arquitetura, tais como:

* constantes genéricas;
* tipos compartilhados;
* aliases de tipos;
* exceções técnicas reutilizáveis;
* informações de versão da aplicação;
* utilitários puros e determinísticos;
* pequenos helpers sem dependência de infraestrutura.

Todos esses componentes devem ser independentes de regras de negócio e de tecnologias específicas.

---

# Componentes Proibidos

O pacote `shared` **não deve conter**:

* regras de negócio;
* entidades;
* value objects;
* casos de uso;
* protocolos (Ports);
* repositories;
* serviços de domínio;
* acesso ao Docker;
* acesso ao sistema de arquivos;
* acesso ao banco de dados;
* chamadas de rede;
* execução de processos externos;
* implementações específicas de infraestrutura;
* código dependente da CLI.

Sempre que um componente possuir uma responsabilidade claramente associada a uma camada da arquitetura, ele deverá ser movido para essa camada.

---

# Justificativa

Esta decisão busca preservar a clareza arquitetural do CyberLab e impedir que `shared` se transforme em um diretório genérico de utilidades.

Ao exigir que toda nova classe seja avaliada contra as camadas arquiteturais antes de ser adicionada a `shared`, o projeto mantém:

* baixo acoplamento;
* alta coesão;
* responsabilidades bem definidas;
* facilidade de manutenção;
* previsibilidade na organização do código.

Além disso, essa regra reduz ambiguidades para novos colaboradores e assistentes de IA.

---

# Consequências

## Benefícios

* preserva a arquitetura ao longo do crescimento do projeto;
* evita o acúmulo de código sem responsabilidade clara;
* facilita a localização de componentes;
* melhora a experiência de manutenção;
* reduz o risco de dependências inadequadas entre camadas;
* fornece um critério objetivo para revisão de código.

## Trade-offs

Alguns componentes inicialmente implementados em `shared` poderão ser movidos futuramente para uma camada específica conforme a arquitetura evoluir.

Esse custo é considerado aceitável para manter a organização e a consistência arquitetural do projeto.

---

# Regra de Ouro

> **O pacote `shared` é o último destino possível, nunca o primeiro.**

Em outras palavras:

> **Somente quando um componente não pertencer ao Domain, à Application, à Infrastructure ou à CLI ele poderá ser implementado em `shared`.**

Essa regra deve orientar todas as futuras decisões relacionadas à organização do código no CyberLab.
