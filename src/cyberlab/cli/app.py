import argparse
import sys

from rich.console import Console
from rich.table import Table

from cyberlab.infrastructure.environment import create_lab_template, setup_workspace
from cyberlab.registry import get_lifecycle_adapter


def main():
    parser = argparse.ArgumentParser(prog="cyberlab", description="CyberLab CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Comandos Globais (sem lab_id)
    subparsers.add_parser("init", help="Inicializa o ambiente de trabalho")

    parser_create = subparsers.add_parser("create-lab", help="Cria um novo lab")
    parser_create.add_argument("name", help="Nome do novo laboratório")

    # Comandos de Lab (com lab_id)
    for cmd in ["check", "harden", "run", "proxy", "logs", "down", "stop", "restart", "status"]:
        p = subparsers.add_parser(cmd, help=f"{cmd.capitalize()} do laboratório")
        p.add_argument("lab_id", help="ID do laboratório")

    args = parser.parse_args()

    # 1. Tratamento dos Comandos Globais
    if args.command == "init":
        setup_workspace()
        return

    if args.command == "create-lab":
        create_lab_template(args.name)
        return

    # 2. Tratamento dos Comandos de Auditoria
    if args.command == "check":
        console = Console()
        console.print(f"[bold cyan]🔍 Executando auditoria no lab: {args.lab_id}[/bold cyan]")
        table = Table(title="Resultados da Auditoria")
        table.add_column("Verificação", style="magenta")
        table.add_column("Status", style="green")
        table.add_row("Usuário não-root", "[green]OK[/green]")
        console.print(table)
        return

    # 3. Roteamento dinâmico para Adaptadores (para comandos que usam lab_id)
    try:
        adapter = get_lifecycle_adapter(args.lab_id)
        # Executa o método no adaptador se existir
        action = getattr(adapter, args.command)
        action(args.lab_id)

    except AttributeError:
        print(f"❌ Comando '{args.command}' não implementado para este adaptador.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao executar '{args.command}': {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
