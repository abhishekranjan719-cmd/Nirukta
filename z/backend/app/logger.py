"""
Backend Logger Configuration

Centralized logging configuration using Loguru with settings from YAML.
Provides consistent, colorful, and structured logging across the backend service.
"""

import sys
from pathlib import Path

from loguru import logger

from app.config import settings


def setup_logger():
    """
    Configure loguru logger with settings from backend.yaml

    Features:
    - Consistent format across all services
    - Colorized output for development
    - File rotation and retention
    - Backtrace and diagnose for debugging
    - Mode-aware configuration (local vs dev)
    """

    # Remove default handler
    logger.remove()

    # Get logging config from YAML
    log_config = settings.constants.get("logging", {})
    log_level = log_config.get("level", "INFO")
    log_format = log_config.get("format", "{time} | {level} | {message}")
    colorize = log_config.get("colorize", True)

    # Console handler with colorization (for local mode)
    if settings.mode == "local":
        logger.add(
            sys.stderr,
            format=log_format,
            level=log_level,
            colorize=colorize,
            backtrace=log_config.get("backtrace", True),
            diagnose=log_config.get("diagnose", True),
        )
    else:
        # Dev/production mode - no colors, structured for log aggregation
        logger.add(
            sys.stderr,
            format=log_format,
            level=log_level,
            colorize=False,
            serialize=log_config.get("serialize", False),
            backtrace=log_config.get("backtrace", False),
            diagnose=log_config.get("diagnose", False),
        )

    # File handler (optional, disabled in dev mode by default)
    if settings.mode == "local":
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        logger.add(
            log_dir / "backend.log",
            format=log_format,
            level=log_level,
            rotation=log_config.get("rotation", "100 MB"),
            retention=log_config.get("retention", "10 days"),
            compression=log_config.get("compression", "zip"),
            colorize=False,
            backtrace=True,
            diagnose=True,
        )

    logger.info(f"Backend logger initialized | Mode: {settings.mode} | Level: {log_level}")

    return logger


# Initialize logger on import
setup_logger()
