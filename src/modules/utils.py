import logging


def get_logger() -> logging.Logger:
    """
    Returns a logger instance for the application.

    The logger is configured to log messages to the console with a specific format.
    """
    logger = logging.getLogger("VoidWarSaveEditor")
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def enforce_positive_float(value: float) -> float:
    """Enforce that a value is a positive float."""
    if not isinstance(value, (int, float)):
        raise ValueError("Value must be a number.")
    if value < 0:
        raise ValueError("Value cannot be negative.")
    return float(value)
