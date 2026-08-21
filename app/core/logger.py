"""
logger.py

Centralized logging configuration for the AI Research Assistant.
Every module in the project should import and use this logger.
"""

import logging


def setup_logger(
    name: str = "ResearchAssistant",
    log_level: int = logging.INFO,
) -> logging.Logger:
    """
    Create and configure a logger.

    Parameters
    ----------
    name : str
        Name of the logger.

    log_level : int
        Logging level.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(log_level)

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Prevent duplicate log messages
    # through the root logger / Uvicorn.
    logger.propagate = False

    return logger


# Global logger instance
logger = setup_logger()