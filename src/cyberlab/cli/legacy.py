"""Temporary compatibility CLI retained during the Typer migration.

New automation must target :mod:`cyberlab.cli.app`.  This module preserves the
pre-migration command surface behind ``cyberlab legacy`` until it is removed in
a later, explicit breaking-change release.
"""

from __future__ import annotations

import argparse

from rich.console import Console
from rich.table import Table

from cyberlab.legacy_services import (
    create_lab_template,
    get_lifecycle_adapter,
    pre_flight_check,
    setup_workspace,
    validate_flag,
)


def main(argv: list[str] | None = None) -> None:
    """Run the pre-Typer CLI with an explicit argument list."""

    console = Console()
    parser = argparse.ArgumentParser(prog="cyberlab legacy", description="Legacy CyberLab CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init", help="Inicializa o ambiente de trabalho")

    parser_create = subparsers.add_parser("create-lab", help="Cria um novo lab")
    parser_create.add_argument("name")
    parser_exec = subparsers.add_parser("exec", help="Exec do laboratório")
    parser_exec.add_argument("lab_id")
    parser_exec.add_argument("command_str", nargs="?", default="/bin/bash")
    parser_submit = subparsers.add_parser("submit", help="Envia flag para validação")
    parser_submit.add_argument("lab_id")
    parser_submit.add_argument("--flag", required=True)
    parser_deploy = subparsers.add_parser("deploy", help="Implanta um lab completo")
    parser_deploy.add_argument("lab_id")
    parser_ctf = subparsers.add_parser("setup-ctf", help="Configura o CTF no alvo")
    parser_ctf.add_argument("lab_id")
    parser_ctf.add_argument("target")

    commands = ("check", "harden", "run", "proxy", "logs", "down", "stop", "restart", "status")
    for command in commands:
        command_parser = subparsers.add_parser(
            command,
            help=f"{command.capitalize()} do laboratório",
        )
        command_parser.add_argument("lab_id")

    args = parser.parse_args(argv)
    if args.command == "init":
        pre_flight_check(require_cluster=False)
        setup_workspace()
        return
    if args.command == "create-lab":
        create_lab_template(args.name)
        return
    if args.command == "check":
        pre_flight_check(require_cluster=True)
        table = Table(title="Resultados da Auditoria")
        table.add_column("Verificação", style="magenta")
        table.add_column("Status", style="green")
        table.add_row("Usuário não-root", "[green]OK[/green]")
        console.print(table)
        return
    if args.command == "submit":
        if validate_flag(args.lab_id, args.flag):
            console.print("[bold green]🎉 Flag correta! Lab concluído.[/bold green]")
            return
        console.print("[bold red]❌ Flag incorreta, tente novamente.[/bold red]")
        raise SystemExit(1)

    try:
        pre_flight_check(require_cluster=True)
        adapter = get_lifecycle_adapter(args.lab_id)
        if args.command == "deploy":
            result = adapter.deploy(f"labs/{args.lab_id}/lab.yaml")
        elif args.command == "setup-ctf":
            result = adapter.setup_ctf(args.lab_id, args.target)
        elif args.command == "exec":
            if not hasattr(adapter, "exec_in_pod"):
                raise AttributeError("exec_in_pod")
            adapter.exec_in_pod(args.lab_id, args.command_str)
            result = None
        else:
            result = getattr(adapter, args.command)(args.lab_id)
        if result is not None:
            console.print(
                f"[bold green]✨ Sucesso ao executar '{args.command}':[/bold green]\n{result}"
            )
    except AttributeError:
        console.print(
            f"[bold red]❌ Erro:[/bold red] O adaptador para o lab '{args.lab_id}' "
            f"não suporta o comando '{args.command}'."
        )
        raise SystemExit(1) from None
    except Exception as error:
        console.print(f"[bold red]❌ Erro crítico ao executar '{args.command}':[/bold red] {error}")
        raise SystemExit(1) from error
