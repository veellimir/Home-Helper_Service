import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .config import settings

LOG_DIR = Path("logs") if settings.ENV == "dev" else Path("/logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:"
    "%(lineno)-3d %(levelname)-7s - %(message)s"
)


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    log_file = LOG_DIR / f"{name}.txt"

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        fmt=LOG_DEFAULT_FORMAT,
        datefmt="%d-%m-%Y %H:%M:%S",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.propagate = False

    return logger
