import datetime
import os
import subprocess
import sys
from pathlib import Path

from rich.console import Console

from cyberlab.utils.ui import get_progress_bar

console = Console()

# Resolve o Card 3: Caminho dinâmico baseado em Variável de Ambiente
CYBERLAB_HOME = Path(os.getenv("CYBERLAB_HOME", Path.home() / "CyberLab"))


def setup_workspace():
    """Prepara a estrutura de pastas e verifica dependências."""
    console.print("[bold blue]🚀 Iniciando configuração do CyberLab...[/bold blue]")

    # Substituímos o hardcode pela constante global
    dirs_to_create = ["labs", "config", "templates"]

    with get_progress_bar() as progress:
        task = progress.add_task(
            "[cyan]Criando estrutura de diretórios...", total=len(dirs_to_create)
        )

        for folder in dirs_to_create:
            path = CYBERLAB_HOME / folder
            path.mkdir(parents=True, exist_ok=True)
            progress.update(task, advance=1)

    console.print(f"[bold green]✅ Ambiente configurado em {CYBERLAB_HOME}[/bold green]")
    console.print(
        f"Dica: Coloque seus novos laboratórios na pasta [bold]{CYBERLAB_HOME}/labs/[/bold]"
    )


def create_lab_template(lab_name: str):
    """Cria a estrutura de um novo lab com README, .gitignore e lab.yaml."""
    # Aqui está a nossa variável dinâmica
    base_path = CYBERLAB_HOME / "labs" / lab_name

    if base_path.exists():
        console.print(f"[red]Erro: O lab '{lab_name}' já existe![/red]")
        return

    # Cria pastas
    (base_path / "k8s").mkdir(parents=True, exist_ok=True)

    # Cria o lab.yaml com metadados básicos
    lab_yaml_path = base_path / "lab.yaml"
    lab_yaml_content = f"""name: {lab_name}
created_at: {datetime.datetime.now().strftime("%Y-%m-%d")}
description: "Laboratório de segurança para testes de {lab_name}"
tags:
  - security
  - training
"""
    lab_yaml_path.write_text(lab_yaml_content)

    # Cria README.md e .gitignore
    (base_path / "README.md").write_text(
        f"# Laboratório: {lab_name}\n\n## Descrição\n{lab_name} criado via CLI."
    )
    (base_path / ".gitignore").write_text(".venv/\n__pycache__/\n*.log\n")

    console.print(
        f"[bold green]✅ Lab '{lab_name}' criado com lab.yaml, README e .gitignore![/bold green]"
    )


def is_docker_running() -> bool:
    """Verifica se o daemon do Docker está respondendo."""
    try:
        # Tenta rodar um comando leve para ver se o Docker responde
        subprocess.run(["docker", "info"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def is_kind_cluster_running(cluster_name: str = "cyberlab") -> bool:  # Altere o padrão aqui
    """Verifica se o cluster KIND específico está de pé."""
    try:
        result = subprocess.run(
            ["kind", "get", "clusters"], capture_output=True, text=True, check=True
        )
        # Verifica se o nome do cluster aparece na lista
        clusters = result.stdout.splitlines()
        return cluster_name in clusters
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def pre_flight_check(require_cluster: bool = False):
    """Executa a checagem completa e interrompe se algo falhar."""
    with console.status(
        "[bold yellow]Verificando pré-requisitos do sistema...[/bold yellow]", spinner="dots"
    ):
        # 1. Checa o Docker
        if not is_docker_running():
            console.print(
                "[bold red]❌ Erro Crítico:[/bold red] "
                "O Docker não está rodando ou não está instalado. "
                "Inicie o Docker antes de usar o CyberLab."
            )
            sys.exit(1)

        # 2. Checa o Kind (apenas para comandos que exigem o cluster ativo, como deploy)
        if require_cluster and not is_kind_cluster_running(cluster_name="cyberlab"):
            console.print(
                "[bold red]❌ Erro Crítico:[/bold red] "
                "O cluster Kubernetes (KIND) não está rodando. "
                "Execute 'cyberlab init' primeiro para provisionar o ambiente base."
            )
            sys.exit(1)
