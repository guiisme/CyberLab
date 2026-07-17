import logging
from pathlib import Path


def setup_logger():
    log_dir = Path.home() / ".cyberlab" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "cyberlab.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),  # Opcional: mantém o log no console também
        ],
    )
    return logging.getLogger("cyberlab")


logger = setup_logger()
