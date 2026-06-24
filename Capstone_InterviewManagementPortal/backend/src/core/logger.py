"""Logging setup for the backend application."""

import logging
import sys

from src.core.config import settings


def setup_logger():
    """Configure and return the root application logger.

    The logger writes to stdout for container/runtime visibility and to
    ``application.log`` for local troubleshooting.

    Returns:
        logging.Logger: Configured root logger.
    """
    logger = logging.getLogger()
    
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Stream logs to stdout so process managers and container runtimes can
    # collect application events without reading local files.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler("application.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
