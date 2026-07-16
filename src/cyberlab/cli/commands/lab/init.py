from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from cyberlab.cli.generator import TemplateGenerator


def register_init_command(
    app: typer.Typer,
) -> None:
    """Register the 'lab init' command."""

    @app.command("init")
    def init(
        lab_id: Annotated[str, typer.Argument(help="ID único do laboratório (ex: web-sqli-01)")],
        lab_name: Annotated[
            str, typer.Option(help="Nome legível do laboratório")
        ] = "Novo Laboratório",
        author: Annotated[
            str, typer.Option(help="Autor ou organização criadora")
        ] = "CyberLab User",
        difficulty: Annotated[
            str, typer.Option(help="Nível de dificuldade (ex: beginner, intermediate, advanced)")
        ] = "beginner",
        description: Annotated[
            str, typer.Option(help="Descrição curta do desafio")
        ] = "Um laboratório interativo de segurança.",
        service_name: Annotated[
            str, typer.Option(help="Nome do serviço principal no compose")
        ] = "target_app",
        template: Annotated[
            str, typer.Option(help="Nome do template base a ser utilizado")
        ] = "docker_compose",
    ) -> None:
        """Initialize a new laboratory scaffold from a template."""

        context = {
            "lab_id": lab_id,
            "lab_name": lab_name,
            "author": author,
            "difficulty": difficulty,
            "description": description,
            "service_name": service_name,
        }

        # Resolução de caminho: init.py -> lab/ -> commands/ -> cli/ -> templates/labs/
        cli_root_dir = Path(__file__).resolve().parent.parent.parent
        templates_dir = cli_root_dir / "templates" / "labs"

        target_dir = Path.cwd() / lab_id

        typer.secho(f"Iniciando a criação do laboratório '{lab_id}'...", fg=typer.colors.CYAN)
        typer.secho(f"Utilizando o template: {template}\n", fg=typer.colors.CYAN)

        try:
            generator = TemplateGenerator(templates_dir=templates_dir)
            generator.generate(template_name=template, target_dir=target_dir, context=context)

            typer.secho(
                f"✨ Laboratório '{lab_id}' gerado com sucesso em: {target_dir.absolute()}",
                fg=typer.colors.GREEN,
                bold=True,
            )
            typer.secho("\nPróximos passos:", fg=typer.colors.YELLOW)
            typer.secho(f"  cd {lab_id}")
            typer.secho("  docker-compose up -d")

        except ValueError as e:
            typer.secho(f"❌ Erro de validação: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1) from e
        except Exception as e:
            typer.secho(
                f"❌ Erro inesperado ao gerar o laboratório: {e}", fg=typer.colors.RED, err=True
            )
            raise typer.Exit(code=1) from e
