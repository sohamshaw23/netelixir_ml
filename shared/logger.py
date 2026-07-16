"""
shared/logger.py - Centralised Logging Setup
=============================================
Marketing Intelligence AI Platform

Configures the root logger and per-module file handlers so that all
application logs are written to the logs/ directory.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(
    log_dir: str = "logs",
    log_level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
) -> None:
    """
    Configure application-wide logging.

    Sets up:
        - A streaming handler (stdout) for all log messages.
        - Rotating file handlers for ``app.log``, ``api.log``, and
          ``model.log``.

    Args:
        log_dir: Directory where log files will be written.
        log_level: Minimum log level (e.g. ``"DEBUG"``, ``"INFO"``).
        max_bytes: Maximum size in bytes before rotation.
        backup_count: Number of rotated log files to retain.
    """
    os.makedirs(log_dir, exist_ok=True)

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    formatter = logging.Formatter(log_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers to avoid duplicate log entries on reload.
    root_logger.handlers.clear()

    # ------------------------------------------------------------------
    # Stream handler (console)
    # ------------------------------------------------------------------
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    # ------------------------------------------------------------------
    # File handlers
    # ------------------------------------------------------------------
    log_files = {
        "app": os.path.join(log_dir, "app.log"),
        "api": os.path.join(log_dir, "api.log"),
        "model": os.path.join(log_dir, "model.log"),
    }

    for _name, path in log_files.items():
        handler = RotatingFileHandler(path, maxBytes=max_bytes, backupCount=backup_count)
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

    logging.getLogger(__name__).info(
        "Logging initialised. Level=%s, LogDir=%s", log_level, log_dir
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger instance.

    Args:
        name: Logger name (typically ``__name__``).

    Returns:
        logging.Logger: Configured logger.
    """
    return logging.getLogger(name)
