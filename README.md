
🚀 Quickstart

Clone & Install:Bashgit

clone https://github.com/<seu-user>/CyberLab.git && cd CyberLab
uv sync

Setup:
```
Bash
uv run cyberlab init
```
Execute:
```
Bash
uv run cyberlab deploy <lab_id>
```

🛡️ Por que usar CyberLab?Arquitetura Desacoplada:

- Aplicação agnóstica à infraestrutura, com suporte nativo a Docker e Kubernetes.
- Desenvolvimento Profissional: Construído com TDD, Injeção de Dependência e princípios SOLID.
- Gamificação CTF: Sistema integrado de envio e validação de flags para laboratórios de desafio.

🏗️ Project Architecture

Plaintext

                   +--------------------+
                   |        CLI         |
                   +---------+----------+
                             |
                             v
                   +--------------------+
                   |    Use Cases       |
                   +---------+----------+
                             |
             +---------------+---------------+
             |                               |
             v                               v
      Repository Protocol             Runner Protocol
             |                               |
             v                               v
 Filesystem Repository         Docker/K8s Runner
             |                               |
             +---------------+---------------+


🛠️ CLI Features

- init: Inicializa o ambiente de trabalho.
- deploy <lab_id>: Implanta um lab completo no cluster.
- submit <lab_id> --flag <VALOR>: Envia e valida flag de desafios CTF.
- status <lab_id>: Verifica o estado atual dos pods do lab.
- exec <lab_id> <comando>: Acesso direto via shell ao pod do laboratório.

📈 Current Status
- Implementado: Arquitetura limpa, CLI modular, sistema de logs estruturados, auditoria de deploy, suporte a Kubernetes e validação de flags CTF.
- Roadmap: Marketplace de laboratórios e suporte a execução remota.

🤝 Contributing
Antes de abrir um Pull Request, certifique-se de rodar:
```
Bash
make verify
```

Novas funcionalidades devem seguir o TDD e manter o isolamento da camada de infraestrutura.

⚖️ License
Este projeto está licenciado sob a licença MIT.
