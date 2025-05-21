import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

def setup_logger(name: str, log_file: str = "app.log", level=logging.INFO):
    """
    Sets up a logger with rotating file handler and console output.

    Args:
        name (str): The logger name.
        log_file (str): Path to log file.
        level (int): Logging level.
    Returns:
        logging.Logger: Configured logger instance.
    """
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # Rotating file handler: 1MB per file, keep 3 backups
    file_handler = RotatingFileHandler(
        f"logs/{log_file}", maxBytes=1_000_000, backupCount=3
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
