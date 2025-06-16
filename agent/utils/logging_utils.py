import logging
from agent.config.settings import settings


def get_logger(name: str = "agent") -> logging.Logger:
    """
    Returns a pre-configured logger with consistent formatting.
    """
    logger = logging.getLogger(name)

    if not logger.hasHandlers():  # Prevent duplicate handlers
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
