"""
Definições de exceções do domínio CyberLab.
Todas as exceções de negócio devem herdar de CyberLabError.
"""


class CyberLabError(Exception):
    """Classe base para todas as exceções do domínio."""

    pass


class LabExecutionError(CyberLabError):
    """
    Exceção levantada quando ocorre um erro crítico
    na execução do ciclo de vida de um laboratório (ex: falha no Podman/Docker).
    """

    pass


class LabNotFoundError(CyberLabError):
    """Exceção levantada quando um laboratório solicitado não é encontrado."""

    pass


class TemplateGenerationError(CyberLabError):
    """Exceção levantada quando falha a geração de arquivos via template."""

    pass
