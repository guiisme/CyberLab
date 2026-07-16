from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn


def get_progress_bar():
    """Retorna uma barra de progresso configurada."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        transient=True,  # Remove a barra ao terminar
    )
