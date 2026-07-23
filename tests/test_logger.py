import logging

from src.logger import setup_logger


def test_setup_logger():
    logger = setup_logger()

    assert isinstance(logger, logging.Logger)
    assert logger.name == "disk_cleanup"

    # Call it again and verify we don't duplicate handlers
    handler_count_1 = len(logger.handlers)
    logger2 = setup_logger()
    handler_count_2 = len(logger2.handlers)

    assert handler_count_1 == handler_count_2
    assert handler_count_1 >= 1
