from pathlib import Path

from rich.console import Console

from cyberlab.utils.ui import get_progress_bar

console = Console()


def setup_workspace():
    """Prepara a estrutura de pastas e verifica dependências."""
    console.print("[bold blue]🚀 Iniciando configuração do CyberLab...[/bold blue]")

    base_path = Path.home() / "CyberLab"
    dirs_to_create = ["labs", "config", "templates"]

    with get_progress_bar() as progress:
        task = progress.add_task(
            "[cyan]Criando estrutura de diretórios...", total=len(dirs_to_create)
        )

        for folder in dirs_to_create:
            path = base_path / folder
            path.mkdir(parents=True, exist_ok=True)
            progress.update(task, advance=1)

    console.print("[bold green]✅ Ambiente configurado em ~/CyberLab/[/bold green]")
    console.print("Dica: Coloque seus novos laboratórios na pasta [bold]~/CyberLab/labs/[/bold]")


def create_lab_template(lab_name: str):
    """Cria a estrutura de um novo lab com README e .gitignore."""
    base_path = Path.home() / "CyberLab/labs" / lab_name

    if base_path.exists():
        console.print(f"[red]Erro: O lab '{lab_name}' já existe![/red]")
        return

    # Cria as pastas
    (base_path / "k8s").mkdir(parents=True, exist_ok=True)

    # Cria o README.md
    readme_path = base_path / "README.md"
    readme_path.write_text(
        f"# Laboratório: {lab_name}\n\n## Descrição\nCriado "
        "em {datetime.now().strftime('%d/%m/%Y')}."
    )

    # Cria o .gitignore
    gitignore_path = base_path / ".gitignore"
    gitignore_path.write_text(".venv/\n__pycache__/\n*.log\n")

    console.print(
        f"[bold green]✅ Lab '{lab_name}' criado com sucesso em "
        "~/CyberLab/labs/{lab_name}![/bold green]"
    )
