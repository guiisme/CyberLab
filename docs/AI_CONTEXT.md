# AI_CONTEXT.md
> **Status:** Version 1.2
> **Projeto:** CyberLab
> **Objetivo:** Fornecer o contexto arquitetural e as decisões de engenharia necessárias para que desenvolvedores e assistentes de IA possam contribuir com o projeto de forma consistente.

---

# 1. Sobre este documento

Este documento é a principal referência arquitetural do CyberLab.

Seu propósito é registrar não apenas **o que** foi desenvolvido, mas principalmente **por que** determinadas decisões foram tomadas. Ele deve permitir que qualquer colaborador — humano ou assistente de IA — compreenda rapidamente os princípios do projeto antes de implementar novas funcionalidades.

Este documento deve evoluir junto com o código-fonte e ser atualizado sempre que uma decisão arquitetural relevante for tomada.

## 1.1 Hierarquia da Documentação

O CyberLab adota uma documentação organizada por responsabilidades. Cada documento possui um propósito específico e deve evitar duplicar informações pertencentes a outro documento.

Quando houver conflito entre documentos, deve-se respeitar a seguinte ordem de precedência:

1. **Architecture Decision Records (ADRs)** — Decisões arquiteturais oficiais e suas justificativas.
2. **AI_CONTEXT.md** — Princípios arquiteturais, filosóficos e organizacionais que orientam a evolução do projeto.
3. **Architecture** (`docs/architecture/`) — Descrição técnica da arquitetura, das camadas e dos fluxos do sistema.
4. **Roadmap** (`docs/roadmap/`) — Planejamento da evolução do produto e das funcionalidades.
5. **README** — Informações de instalação, uso e contribuição.

Cada documento responde a uma pergunta diferente:

| Documento    | Pergunta que responde                         |
| ------------ | --------------------------------------------- |
| ADR          | **Por que esta decisão foi tomada?**          |
| AI_CONTEXT   | **Quais princípios orientam o projeto?**      |
| Architecture | **Como o sistema foi projetado?**             |
| Roadmap      | **Para onde o projeto está evoluindo?**       |
| README       | **Como utilizar e contribuir com o projeto?** |

Como regra geral, decisões arquiteturais permanentes devem ser registradas em um ADR e apenas referenciadas pelos demais documentos.

Por exemplo, a utilização do pacote `shared` é definida pelo **ADR-0007 — Shared Package**. O `AI_CONTEXT.md` referencia essa decisão, mas sua definição oficial permanece no ADR.


---

# 2. Visão Geral

O CyberLab é uma plataforma open source para criação, padronização, execução e gerenciamento de laboratórios de cibersegurança reproduzíveis.

O projeto fornece uma arquitetura extensível para construir, distribuir e executar laboratórios utilizando uma estrutura consistente baseada em scaffolds oficiais, protocolos arquiteturais e componentes desacoplados.

Mais do que um conjunto de laboratórios, o CyberLab é uma plataforma extensível capaz de evoluir para suportar diferentes ambientes de execução, plugins, scaffolds e provedores de infraestrutura sem comprometer sua arquitetura.

A Plugin Architecture introduzida na PR #015 consolida esse objetivo, permitindo que novas capacidades sejam adicionadas através de Python Entry Points sem modificar o Core da aplicação.

---

# 3. Missão

Tornar a criação, padronização e execução de laboratórios de cibersegurança simples, reproduzíveis e consistentes, fornecendo uma base sólida para estudo, treinamento, pesquisa e demonstração de cenários reais.

---

# 4. Objetivos

O CyberLab busca:

* facilitar a criação de laboratórios reproduzíveis;
* estabelecer um padrão oficial para novos laboratórios;
* reduzir o tempo necessário para preparar ambientes de estudo;
* fornecer uma CLI intuitiva e consistente;
* permitir a expansão da plataforma sem alterar sua arquitetura principal;
* priorizar qualidade de código, tipagem, testes automatizados e documentação;
* servir como referência de boas práticas em engenharia de software aplicada à cibersegurança.

---

# 5. Público-alvo

O projeto foi pensado para atender principalmente:

* estudantes de cibersegurança;
* profissionais de segurança ofensiva;
* profissionais de segurança defensiva;
* pesquisadores;
* instrutores;
* criadores de conteúdo técnico;
* equipes de treinamento;
* desenvolvedores de laboratórios.

---

# 6. Princípios Fundamentais

Todos os componentes do CyberLab devem respeitar os seguintes princípios.

## 6.1 Arquitetura em primeiro lugar

A arquitetura possui prioridade sobre atalhos de implementação.

Quando existir conflito entre velocidade de desenvolvimento e qualidade arquitetural, deve prevalecer a arquitetura.

---

## 6.2 Reprodutibilidade

Um laboratório deve produzir resultados previsíveis e consistentes em qualquer ambiente compatível.

---

## 6.3 Extensibilidade

Novas funcionalidades devem ser adicionadas com impacto mínimo sobre o código existente.

O projeto deve favorecer evolução incremental.

---

## 6.4 Testabilidade

Toda regra de negócio deve ser facilmente testável.

Dependências externas devem permanecer isoladas da lógica principal da aplicação.

---

## 6.5 Baixo Acoplamento

Cada camada deve conhecer apenas os contratos necessários para desempenhar sua responsabilidade.

Implementações concretas nunca devem vazar para as camadas superiores.

---

## 6.6 Experiência do Desenvolvedor

A experiência de desenvolvimento deve ser simples, consistente e previsível.

Isso inclui:

* organização do projeto;
* convenções claras;
* mensagens de erro úteis;
* documentação atualizada;
* comandos intuitivos.

---

## 6.7 Qualidade Contínua

Qualidade não é uma etapa final.

Ela faz parte do desenvolvimento diário através de:

* tipagem estática;
* linting;
* testes automatizados;
* revisão de código;
* documentação.

---

## 6.8 Consistência Arquitetural

Novas capacidades devem reutilizar a arquitetura existente sempre que possível.

O projeto favorece evolução por extensão em vez de substituição de componentes já consolidados.

Scaffolds oficiais representam a estrutura canônica de novos laboratórios e devem evoluir juntamente com a arquitetura da plataforma.

---

## 6.9 Evolução por Extensão

O CyberLab prioriza evolução por extensão em vez de modificação do Core.

Novas capacidades devem, sempre que possível:

* reutilizar contratos existentes;
* introduzir novos adaptadores em vez de alterar componentes consolidados;
* manter o Composition Root como único ponto de composição da aplicação.

A Plugin Architecture estabeleceu este princípio como uma diretriz permanente do projeto.

---

# 7. O que o CyberLab NÃO é

Para manter um escopo claro, o CyberLab não pretende:

* ser um framework de exploração de vulnerabilidades;
* substituir plataformas completas de virtualização;
* concentrar regras de negócio na CLI;
* acoplar o domínio a tecnologias específicas de infraestrutura;
* sacrificar arquitetura em favor de implementações rápidas.

Esses limites ajudam a preservar a identidade e a sustentabilidade técnica do projeto.

---

# 8. Filosofia de Engenharia

O CyberLab é desenvolvido seguindo uma filosofia de engenharia orientada por decisões.

Sempre que possível, novas capacidades devem ser validadas através de sua própria utilização.

Novas capacidades devem ser implementadas incrementalmente, introduzindo um único conceito arquitetural por commit. Esse processo reduz retrabalho, facilita revisões e preserva a estabilidade do Core.

O CyberLab utiliza seus próprios scaffolds para gerar seus laboratórios de referência, reduzindo duplicação e garantindo que as funcionalidades permaneçam continuamente exercitadas.

Isso significa que decisões importantes devem ser registradas juntamente com sua motivação e consequências, permitindo compreender o raciocínio por trás da arquitetura e facilitando a evolução do projeto.

Sempre que possível, decisões relevantes devem responder às seguintes perguntas:

* Qual problema estamos resolvendo?
* Qual decisão foi tomada?
* Por que ela foi escolhida?
* Quais consequências ela traz?

---

# 9. Objetivo deste documento

Este documento deve ser a primeira referência consultada antes de qualquer alteração significativa no projeto.

Ele existe para preservar a consistência arquitetural do CyberLab durante toda a sua evolução, independentemente de quem esteja contribuindo com o código.

Este documento complementa os ADRs ao registrar os princípios permanentes que orientam a evolução da plataforma, enquanto as decisões específicas continuam sendo documentadas individualmente através dos rchitecture Decision Records.

**Fim da Versão 1.2**
