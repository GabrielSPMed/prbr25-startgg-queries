import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    """
    Sets up and returns a logger with the specified name.

    If the logger does not already have handlers, a StreamHandler is added that outputs
    to stdout with a specific log message format. The logger's level is set to INFO,
    and propagation is disabled to prevent duplicate log messages.

    Args:
    name (str): The name of the logger.

    Returns:
    logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger
