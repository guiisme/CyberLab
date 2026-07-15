from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Annotated

import typer

from cyberlab.cli.generator import PluginGenerator


def init_plugin_command() -> Callable[..., None]:
    """Create the plugin init command."""

    def command(
        plugin_id: Annotated[str, typer.Argument(help="ID do novo plugin (ex: meu-novo-plugin)")],
        description: Annotated[
            str, typer.Option(help="Descrição curta do plugin")
        ] = "Um novo plugin para o CyberLab",
        author: Annotated[
            str, typer.Option(help="Nome do autor ou organização")
        ] = "CyberLab Developer",
        template: Annotated[
            str, typer.Option(help="Nome do template base a ser utilizado")
        ] = "empty",
    ) -> None:
        """Initialize a new plugin structure from a template."""

        safe_id = plugin_id.replace("-", "_").lower()

        context = {
            "plugin_id": plugin_id,
            "plugin_name": plugin_id.replace("-", " ").title(),
            "module_name": f"cyberlab_plugin_{safe_id}",
            "class_name": f"{plugin_id.replace('-', ' ').title().replace(' ', '')}Plugin",
            "description": description,
            "author": author,
        }

        # Resolução de caminho partindo deste arquivo de comando até a pasta templates
        # Ajuste a quantidade de '.parent' dependendo da estrutura exata
        cli_root_dir = Path(__file__).resolve().parent.parent.parent
        templates_dir = cli_root_dir / "templates"

        target_dir = Path.cwd() / plugin_id

        typer.secho(f"Iniciando a criação do plugin '{plugin_id}'...", fg=typer.colors.CYAN)
        typer.secho(f"Utilizando o template: {template}\n", fg=typer.colors.CYAN)

        try:
            # Nota: Em um futuro refatoramento para DDD estrito, o PluginGenerator
            # poderia ser encapsulado em um InitPluginUseCase e injetado via parâmetro
            # na função init_plugin_command(), assim como você faz no list_command.
            generator = PluginGenerator(templates_dir=templates_dir)
            generator.generate(template_name=template, target_dir=target_dir, context=context)

            typer.secho(
                f"✨ Plugin '{plugin_id}' gerado com sucesso em: {target_dir.absolute()}",
                fg=typer.colors.GREEN,
                bold=True,
            )
            typer.secho("\nPróximos passos:", fg=typer.colors.YELLOW)
            typer.secho(f"  cd {plugin_id}")
            typer.secho("  uv pip install -e .")

        except ValueError as e:
            typer.secho(f"❌ Erro de validação: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1) from e
        except Exception as e:
            typer.secho(f"❌ Erro inesperado ao gerar o plugin: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1) from e

    return command
