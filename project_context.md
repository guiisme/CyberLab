# CyberLab - Project Context

## Visão Geral
O CyberLab é uma plataforma modular e extensível para gerenciamento, orquestração e execução de laboratórios práticos. O núcleo do projeto é projetado para ser agnóstico em relação à infraestrutura, delegando a execução real para plugins (como Docker, Podman, etc.) através de uma forte adesão à Arquitetura Hexagonal.

## Arquitetura
O projeto segue estritamente a **Arquitetura Hexagonal (Ports and Adapters)**, garantindo que o Domínio e as Regras de Negócio fiquem isolados das ferramentas de infraestrutura e da interface de linha de comando.

* **Domain:** Entidades centrais e contratos (Ports) do sistema.
* **Application:** Casos de uso (Use Cases) que orquestram as regras de negócio.
* **Infrastructure:** Adaptadores que implementam os contratos do Domínio (ex: `PodmanComposeLabLifecycle`).
* **CLI:** Interface de linha de comando construída com Typer, injetando dependências nos Casos de Uso.

## Tech Stack
* **Linguagem:** Python >= 3.12
* **CLI Framework:** Typer
* **Scaffolding Engine:** Jinja2
* **Linting & Formatting:** Ruff
* **Type Checking:** MyPy

## Funcionalidades Principais (Atuais)

### 1. Sistema de Plugins
O Core descobre e carrega plugins dinamicamente utilizando *entry points* do Python (`project.entry-points."cyberlab.plugins"`). Cada plugin declara suas "capabilities" (capacidades), como gerenciar o ciclo de vida de laboratórios (`lab_lifecycle`).

### 2. Motor Universal de Scaffolding (`TemplateGenerator`)
Um motor agnóstico baseado em Jinja2 responsável por gerar estruturas de diretórios e arquivos.
* **Templates de Plugins:** Localizados em `templates/plugins/`.
    * `empty`: Estrutura básica de um plugin.
    * `lab_lifecycle`: Estrutura avançada com base na Arquitetura Hexagonal (Portos e Adaptadores de infraestrutura).
* **Templates de Laboratórios:** Localizados em `templates/labs/`.
    * `docker_compose`: Gera manifesto, infraestrutura via Docker Compose e instruções em Markdown.

## Comandos da CLI

### Ecossistema de Plugins (`cyberlab plugin`)
* `init [PLUGIN_ID]`: Realiza o scaffolding de um novo plugin. Suporta injeção de parâmetros como `--author`, `--description` e seleção de `--template`.

### Ecossistema de Laboratórios (`cyberlab lab`)
* `init [LAB_ID]`: Inicializa a base estrutural de um novo laboratório (scaffolding). Aceita parâmetros como `--difficulty`, `--service-name` e `--template`.
* `create [LAB_ID]`: Mapeia a criação do laboratório através do `LabCreateUseCase`, acionando o protocolo de scaffolding no core da aplicação.

## Padrões de Desenvolvimento
* **Injeção de Dependências (CLI):** O registro de comandos Typer é feito via passagem do app (`register_init_command(app: typer.Typer)`), garantindo escopo seguro e facilidade em testes.
* **

## Estrutura de Diretórios
```text
.
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── demo-plugin
│   ├── LICENSE
│   ├── pyproject.toml
│   ├── README.md
│   ├── src
│   │   └── cyberlab_plugin_demo_plugin
│   │       ├── __init__.py
│   │       └── plugin.py
│   └── tests
│       └── test_plugin.py
├── docker-adapter
│   ├── pyproject.toml
│   └── src
│       └── cyberlab_plugin_docker_adapter
│           ├── infrastructure
│           │   ├── adapter.py
│           │   └── __init__.py
│           ├── __init__.py
│           └── plugin.py
├── docs
│   ├── adr
│   │   ├── 0001 - Project Conventions.md
│   │   ├── 0002 - Value-objects.md
│   │   ├── 0003 - Environment Doctor.md
│   │   ├── 0004 - Laboratory Discovery.md
│   │   ├── 0005 - Laboratory Metadata Model.md
│   │   ├── 0006 - Validation Architecture.md
│   │   ├── 0007 - Docker Compose Laboratory Runner.md
│   │   ├── 0008 - Plugin Architecture
│   │   ├── 0010 - Domain Return Models
│   │   ├── 0011 - Laboratory Scaffolding.md
│   │   └── 0012 - Plugin Architecture
│   ├── AI_CONTEXT.md
│   ├── architecture
│   │   ├── development-workflow.md
│   │   ├── overview.md
│   │   ├── plugins.md
│   │   ├── principles.md
│   │   └── testing.md
│   ├── plugins
│   │   ├── development-guide.md
│   │   └── template.md
│   ├── reviews
│   │   ├── 2026-07-07-codex-architecture-review.md
│   │   └── PR #015.md
│   └── roadmap
│       └── Roadmap.md
├── infrastructure
│   └── system
├── labs
│   ├── sqli-basic
│   │   ├── application
│   │   ├── compose.yaml
│   │   ├── lab.yaml
│   │   ├── README.md
│   │   ├── scripts
│   │   └── seed
│   └── xss-basic
│       ├── application
│       ├── compose.yaml
│       ├── lab.yaml
│       ├── README.md
│       ├── scripts
│       └── seed
├── LICENSE
├── Makefile
├── podman
│   ├── cyberlab_plugin_podman
│   ├── LICENSE
│   ├── pyproject.toml
│   ├── README.md
│   ├── src
│   │   └── cyberlab_plugin_podman
│   │       ├── infrastructure
│   │       │   └── podman_compose.py
│   │       ├── __init__.py
│   │       └── plugin.py
│   ├── tests
│   │   └── test_plugin.py
│   └── uv.lock
├── project_context.md
├── project_tree.txt
├── pyproject.toml
├── README.md
├── scaffolds
│   └── default
│       ├── application
│       ├── compose.yaml
│       ├── lab.yaml
│       ├── README.md
│       ├── scripts
│       └── seed
├── scripts
│   └── create_lab_templates.sh
├── SECURITY.md
├── sqli-basico
│   ├── docker-compose.yml
│   ├── manifest.yaml
│   └── README.md
├── src
│   └── cyberlab
│       ├── application
│       │   ├── __init__.py
│       │   ├── interfaces
│       │   │   ├── command_runner_protocol.py
│       │   │   ├── __init__.py
│       │   │   ├── lab_lifecycle_protocol.py
│       │   │   ├── lab_manifest_loader_protocol.py
│       │   │   ├── lab_repository_protocol.py
│       │   │   ├── lab_scaffolding_protocol.py
│       │   │   ├── lab_validator_protocol.py
│       │   │   ├── plugin_loader_protocol.py
│       │   │   ├── plugin_protocol.py
│       │   │   ├── plugin_registry_protocol.py
│       │   │   └── plugin_scaffolding_protocol.py
│       │   └── use_cases
│       │       ├── create_plugin_use_case.py
│       │       ├── doctor_use_case.py
│       │       ├── get_lab_status_use_case.py
│       │       ├── __init__.py
│       │       ├── lab_create_use_case.py
│       │       ├── lab_info_use_case.py
│       │       ├── lab_logs_use_case.py
│       │       ├── lab_restart_use_case.py
│       │       ├── lab_run_use_case.py
│       │       ├── lab_validation_use_case.py
│       │       ├── list_labs_use_case.py
│       │       ├── list_plugins_use_case.py
│       │       ├── stop_lab_use_case.py
│       │       └── version_use_case.py
│       ├── cli
│       │   ├── app.py
│       │   ├── commands
│       │   │   ├── doctor.py
│       │   │   ├── lab
│       │   │   │   ├── create.py
│       │   │   │   ├── info.py
│       │   │   │   ├── __init__.py
│       │   │   │   ├── init.py
│       │   │   │   ├── list.py
│       │   │   │   ├── logs.py
│       │   │   │   ├── registry.py
│       │   │   │   ├── restart.py
│       │   │   │   ├── run.py
│       │   │   │   ├── status.py
│       │   │   │   ├── stop.py
│       │   │   │   └── validate.py
│       │   │   ├── plugin
│       │   │   │   ├── create.py
│       │   │   │   ├── __init__.py
│       │   │   │   ├── init.py
│       │   │   │   ├── plugin_list.py
│       │   │   │   └── registry.py
│       │   │   ├── registry.py
│       │   │   └── version.py
│       │   ├── generator.py
│       │   ├── __init__.py
│       │   ├── rendering
│       │   │   └── checks.py
│       │   └── templates
│       │       └── labs
│       │           └── docker_compose
│       │               ├── docker-compose.yml.jinja
│       │               ├── manifest.yaml.jinja
│       │               └── README.md.jinja
│       ├── domain
│       │   ├── __init__.py
│       │   ├── interfaces
│       │   │   └── __init__.py
│       │   ├── models
│       │   │   ├── check_result.py
│       │   │   ├── doctor_report.py
│       │   │   ├── __init__.py
│       │   │   ├── lab_execution_report.py
│       │   │   ├── lab_execution_result.py
│       │   │   ├──  lab_list_report.py
│       │   │   ├── lab_logs.py
│       │   │   ├── lab_manifest.py
│       │   │   ├── lab.py
│       │   │   ├── lab_validation_report.py
│       │   │   ├── plugin_manifest.py
│       │   │   ├── plugin.py
│       │   │   └── process_result.py
│       │   ├── reports
│       │   └── value_objects
│       │       ├── __init__.py
│       │       └── version.py
│       ├── infrastructure
│       │   ├── configuration
│       │   │   └── __init__.py
│       │   ├── docker
│       │   │   ├── docker_compose_lab_lifecycle.py
│       │   │   ├── docker_compose_service.py
│       │   │   └── __init__.py
│       │   ├── filesystem
│       │   │   ├── filesystem_lab_repository.py
│       │   │   ├── filesystem_lab_scaffolding.py
│       │   │   ├── filesystem_lab_validator.py
│       │   │   ├── filesystem_plugin_scaffolding.py
│       │   │   ├── __init__.py
│       │   │   └── yaml_lab_manifest_loader.py
│       │   ├── __init__.py
│       │   ├── plugins
│       │   │   ├── entry_point_provider.py
│       │   │   ├── __init__.py
│       │   │   ├── plugin_loader.py
│       │   │   └── plugin_registry.py
│       │   ├── process
│       │   │   ├── command_runner.py
│       │   │   └── __init__.py
│       │   └── runner
│       │       └── noop_lab_runner.py
│       ├── __init__.py
│       ├── __main__.py
│       ├── plugins
│       │   └── __init__.py
│       ├── sdk
│       │   └── __init__.py
│       └── shared
│           ├── __init__.py
│           └── version.py
├── templates
│   └── plugin
│       ├── LICENSE
│       ├── pyproject.toml
│       ├── README.md
│       ├── src
│       │   └── cyberlab_plugin_hello
│       │       ├── __init__.py
│       │       └── plugin.py
│       └── tests
│           └── test_plugin.py
├── tests
│   ├── fakes
│   │   ├── fake_command_runner.py
│   │   ├── fake_docker_compose_service.py
│   │   ├── fake_entry_point_provider.py
│   │   ├── fake_entry_point.py
│   │   ├── fake_lab_lifecycle.py
│   │   ├── fake_lab_manifest_loader.py
│   │   ├── fake_lab_repository.py
│   │   ├── fake_lab_scaffolding.py
│   │   ├── fake_lab_validator.py
│   │   └── fake_plugin.py
│   ├── fixtures
│   ├── integration
│   └── unit
│       ├── application
│       │   ├── test_lab_create_use_case.py
│       │   └── use_cases
│       │       ├── test_create_plugin_use_case.py
│       │       ├── test_get_lab_status_use_case.py
│       │       ├── test_lab_run_use_case.py
│       │       ├── test_lab_validation_use_case.py
│       │       ├── test_logs_lab.py
│       │       ├── test_stop_lab_use_case.py
│       │       └── use_cases
│       │           ├── test_doctor.py
│       │           ├── test_lab_info_use_case.py
│       │           ├── test_list_labs_use_case.py
│       │           └── test_version.py
│       ├── cli
│       │   ├── commands
│       │   │   └── plugin
│       │   │       └── test_list.py
│       │   ├── test_app.py
│       │   ├── test_doctor.py
│       │   ├── test_lab.py
│       │   └── test_version.py
│       ├── domain
│       │   ├── models
│       │   │   ├── test_check_result.py
│       │   │   ├── test_doctor_report.py
│       │   │   ├── test_lab_execution_report.py
│       │   │   ├── test_lab_execution_result.py
│       │   │   ├── test_lab_manifest.py
│       │   │   ├── test_lab.py
│       │   │   ├── test_lab_validation_report.py
│       │   │   ├── test_plugin_manifest.py
│       │   │   └── test_plugin.py
│       │   └── test_laboratory_status.py
│       ├── fakes
│       │   ├── test_fake_command_runner.py
│       │   ├── test_fake_lab_manifest_loader.py
│       │   ├── test_fake_lab_runner.py
│       │   └── test_fake_lab_validator.py
│       ├── infrastructure
│       │   ├── docker
│       │   │   ├── test_docker_compose_lab_lifecycle.py
│       │   │   ├── test_docker_compose_lab_status.py
│       │   │   └── test_docker_compose_service.py
│       │   ├── filesystem
│       │   │   ├── test_filesystem_lab_scaffolding.py
│       │   │   ├── test_filesystem_lab_validator.py
│       │   │   └── test_filesystem_plugin_scaffolding.py
│       │   ├── process
│       │   │   ├── filesystem
│       │   │   │   ├── test_filesystem_lab_repository.py
│       │   │   │   └── test_yaml_lab_manifest_loader.py
│       │   │   ├── test_command_runner.py
│       │   │   └── test_process_result.py
│       │   └── runner
│       │       └── test_noop_lab_runner.py
│       ├── plugins
│       │   └── test_plugin_registry.py
│       ├── sdk
│       │   └── test_sdk_exports.py
│       └── shared
└── uv.lock

95 directories, 218 files
```
