import logging
from pathlib import Path


def setup_logger() -> logging.Logger:
    """Set up and return the application logger, ensuring no duplicate handlers are added."""
    Path("logs").mkdir(exist_ok=True)

    logger = logging.getLogger("disk_cleanup")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler("logs/scanner.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
