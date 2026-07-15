# CyberLab Podman Plugin

## Descrição
Plugin oficial do CyberLab para execução e gerenciamento de laboratórios utilizando o `podman-compose`.

Ele implementa o `LabLifeCycleProtocol` do Core, atuando como um Adaptador de Infraestrutura (Hexagonal Architecture) para traduzir os comandos de domínio em chamadas de subprocesso do Podman.

## Requisitos
* [Podman](https://podman.io/) instalado e configurado.
* `podman-compose` disponível no PATH do sistema.
* CyberLab Core (SDK).

## Instalação

Para instalar o plugin no ambiente virtual do CyberLab (utilizando o `uv` e em modo editável para desenvolvimento):

```bash
uv pip install --no-deps -e ./podman
