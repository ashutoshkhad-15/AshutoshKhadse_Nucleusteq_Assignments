from unittest.mock import MagicMock, patch

from src.core.logger import setup_logger


def test_setup_logger_adds_console_and_file_handlers():
    root_logger = MagicMock()
    with patch("src.core.logger.logging.getLogger", return_value=root_logger), \
         patch("src.core.logger.logging.StreamHandler"), \
         patch("src.core.logger.logging.FileHandler"):
        logger = setup_logger()

    assert logger is root_logger
    assert root_logger.addHandler.call_count == 2
    root_logger.setLevel.assert_called_once()

