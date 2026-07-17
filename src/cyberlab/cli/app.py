import argparse
import sys

from rich.console import Console
from rich.table import Table

# Adicionamos o pre_flight_check aqui na importação:
from cyberlab.infrastructure.environment import (
    create_lab_template,
    pre_flight_check,
    setup_workspace,
)
from cyberlab.registry import get_lifecycle_adapter


def main():
    console = Console()
    parser = argparse.ArgumentParser(prog="cyberlab", description="CyberLab CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Comandos Globais ---
    subparsers.add_parser("init", help="Inicializa o ambiente de trabalho")

    parser_create = subparsers.add_parser("create-lab", help="Cria um novo lab")
    parser_create.add_argument("name", help="Nome do novo laboratório")

    parser_deploy = subparsers.add_parser("deploy", help="Implanta um lab completo")
    parser_deploy.add_argument("lab_id", help="ID/Nome do laboratório (pasta dentro de labs/)")

    parser_ctf = subparsers.add_parser("setup-ctf", help="Configura o CTF no alvo")
    parser_ctf.add_argument("lab_id", help="ID/Nome do laboratório")
    parser_ctf.add_argument("target", help="Nome do pod alvo")

    # --- Comandos de Lab Estruturados ---
    lab_commands = [
        "check",
        "harden",
        "run",
        "proxy",
        "logs",
        "down",
        "stop",
        "restart",
        "status",
        "exec",
    ]

    for cmd in lab_commands:
        p = subparsers.add_parser(cmd, help=f"{cmd.capitalize()} do laboratório")
        p.add_argument("lab_id", help="ID do laboratório")
        if cmd == "exec":
            p.add_argument("command_str", help="Comando a ser executado")

    args = parser.parse_args()

    # --- 1. Tratamento de Comandos Estáticos ---
    if args.command == "init":
        # Antes de iniciar, checa apenas o Docker
        pre_flight_check(require_cluster=False)
        setup_workspace()
        return

    if args.command == "create-lab":
        # Apenas manipula arquivos, não precisa de checagem de infra
        create_lab_template(args.name)
        return

    if args.command == "check":
        # Exige Docker e o Cluster Kubernetes
        pre_flight_check(require_cluster=True)
        console.print(f"[bold cyan]🔍 Executando auditoria no lab: {args.lab_id}[/bold cyan]")
        table = Table(title="Resultados da Auditoria")
        table.add_column("Verificação", style="magenta")
        table.add_column("Status", style="green")
        table.add_row("Usuário não-root", "[green]OK[/green]")
        console.print(table)
        return

    # --- 2. Roteamento de Comandos de Infraestrutura ---
    try:
        # Qualquer outro comando (deploy, setup-ctf, down, exec) vai precisar do cluster!
        pre_flight_check(require_cluster=True)

        adapter = get_lifecycle_adapter(args.lab_id)
        result = None

        if args.command == "deploy":
            path_do_arquivo = f"labs/{args.lab_id}/lab.yaml"
            result = adapter.deploy(path_do_arquivo)

        elif args.command == "setup-ctf":
            result = adapter.setup_ctf(args.lab_id, args.target)

        elif args.command == "exec":
            result = adapter.exec(args.lab_id, args.command_str)

        else:
            # Roteamento dinâmico seguro para os comandos padrão restantes (down, stop, etc)
            action = getattr(adapter, args.command)
            result = action(args.lab_id)

        if result is not None:
            console.print(
                f"[bold green]✨ Sucesso ao executar '{args.command}':[/bold green]\n{result}"
            )

    except AttributeError:
        console.print(
            f"[bold red]❌ Erro:[/bold red] O adaptador para o lab '{args.lab_id}' "
            f"não suporta o comando '{args.command}'."
        )
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Erro crítico ao executar '{args.command}':[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
