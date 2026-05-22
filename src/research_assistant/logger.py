"""Logging configuration for AI Research Assistant."""

import logging

LOGGER_NAME = "research_assistant"


def setup_logger(verbose: bool = False) -> logging.Logger:
    """Configure and return the project logger.

    Args:
        verbose: If True, set level to DEBUG. Otherwise WARNING.

    Returns:
        The configured logger instance.
    """
    logger = logging.getLogger(LOGGER_NAME)

    level = logging.DEBUG if verbose else logging.WARNING
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)

        if verbose:
            fmt = "[%(levelname)s] %(name)s: %(message)s"
        else:
            fmt = "%(message)s"

        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)
    else:
        for handler in logger.handlers:
            handler.setLevel(level)

    return logger


def get_logger() -> logging.Logger:
    """Get the project logger.

    Returns:
        The project logger instance.
    """
    return logging.getLogger(LOGGER_NAME)
