import logging


def setup_logging() -> logging.Logger:
    """Return the application logger configured by Uvicorn."""
    return logging.getLogger("uvicorn.error")
