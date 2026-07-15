import os
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader


class PluginGenerator:
    """Motor de scaffolding estrito para criação de novos plugins do CyberLab."""

    def __init__(self, templates_dir: Path) -> None:
        self.templates_dir = templates_dir
        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Diretório de templates não encontrado: {self.templates_dir}")
        # O Jinja2 precisa saber a raiz de onde buscar os arquivos
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=False,  # Não estamos gerando HTML, segurança de escape não se aplica
            # Essencial para o MyPy e Ruff não reclamarem de arquivos sem linha final
            keep_trailing_newline=True,
        )

    def generate(self, template_name: str, target_dir: Path, context: dict[str, Any]) -> None:
        """
        Gera a estrutura de diretórios e arquivos baseados no template escolhido.
        """
        template_base_path = self.templates_dir / template_name

        if not template_base_path.exists():
            raise ValueError(f"Template '{template_name}' não encontrado em {self.templates_dir}.")

        # Caminhamos por todos os arquivos e pastas dentro do template base
        for root, _, files in os.walk(template_base_path):
            current_dir = Path(root)
            # Calculamos o caminho relativo para espelhar na pasta de destino
            rel_path = current_dir.relative_to(template_base_path)

            # Renderiza variáveis no nome das pastas (ex: pasta "{{module_name}}")
            rendered_rel_path_str = str(rel_path)
            for key, value in context.items():
                rendered_rel_path_str = rendered_rel_path_str.replace("{{" + key + "}}", str(value))

            target_current_dir = target_dir / rendered_rel_path_str
            target_current_dir.mkdir(parents=True, exist_ok=True)

            for file_name in files:
                if file_name.endswith(".jinja"):
                    # Prepara o caminho do template para o ambiente Jinja
                    template_env_path = str(rel_path / file_name).replace("\\", "/")
                    jinja_template = self.env.get_template(f"{template_name}/{template_env_path}")

                    # O motor do Jinja substitui as variáveis no CONTEÚDO do arquivo
                    rendered_content = jinja_template.render(context)

                    # Define o nome final do arquivo, removendo a extensão .jinja
                    # e substituindo variáveis no nome do arquivo, se existirem
                    final_file_name = file_name.replace(".jinja", "")
                    for key, value in context.items():
                        final_file_name = final_file_name.replace("{{" + key + "}}", str(value))

                    target_file_path = target_current_dir / final_file_name

                    # Escreve o arquivo no destino
                    target_file_path.write_text(rendered_content, encoding="utf-8")
