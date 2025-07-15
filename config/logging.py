import logging
from logging.config import dictConfig

from config.settings import settings


def configure_logging() -> None:
    """Configure global logging for the application."""
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": settings.log_level.upper(),
        }
    }

    if settings.log_file:
        handlers["file"] = {
            "class": "logging.FileHandler",
            "filename": settings.log_file,
            "formatter": "default",
            "level": settings.log_level.upper(),
        }

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                }
            },
            "handlers": handlers,
            "root": {
                "level": settings.log_level.upper(),
                "handlers": list(handlers.keys()),
            },
        }
    )

