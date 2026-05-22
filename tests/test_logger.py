"""Tests for logger module."""

import logging

from research_assistant.logger import LOGGER_NAME, get_logger, setup_logger


def test_setup_logger_returns_logger():
    """Test that setup_logger returns a Logger instance."""
    logger = setup_logger()
    assert isinstance(logger, logging.Logger)


def test_setup_logger_name():
    """Test that logger uses the correct name."""
    logger = setup_logger()
    assert logger.name == LOGGER_NAME


def test_default_level_is_warning():
    """Test that default log level is WARNING."""
    logger = setup_logger(verbose=False)
    assert logger.level == logging.WARNING


def test_verbose_sets_debug():
    """Test that verbose=True sets level to DEBUG."""
    logger = setup_logger(verbose=True)
    assert logger.level == logging.DEBUG


def test_get_logger_returns_same_logger():
    """Test that get_logger returns the same logger as setup_logger."""
    setup_logger()
    logger = get_logger()
    assert logger.name == LOGGER_NAME


def test_no_duplicate_handlers():
    """Test that calling setup_logger twice does not add duplicate handlers."""
    logger = setup_logger()
    handler_count = len(logger.handlers)
    setup_logger()
    assert len(logger.handlers) == handler_count
