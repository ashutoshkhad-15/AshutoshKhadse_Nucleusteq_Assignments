import logging
import sys
from src.core.config import settings

def setup_logger():
    logger = logging.getLogger()
    
    # Set log level based on environment config
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Define log format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    file_handler = logging.FileHandler("application.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger