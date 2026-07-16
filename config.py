"""
config.py - Application Configuration
=======================================
Marketing Intelligence AI Platform

Provides configuration classes for development, testing, and production
environments.  Values are read from environment variables first, falling back
to sensible defaults.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Base directory (project root)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base configuration shared by all environments."""

    # -----------------------------------------------------------------------
    # Flask core
    # -----------------------------------------------------------------------
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    DEBUG: bool = False
    TESTING: bool = False

    # -----------------------------------------------------------------------
    # Server
    # -----------------------------------------------------------------------
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 5000))

    # -----------------------------------------------------------------------
    # File uploads
    # -----------------------------------------------------------------------
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    MAX_CONTENT_LENGTH: int = 50 * 1024 * 1024  # 50 MB

    # -----------------------------------------------------------------------
    # Paths
    # -----------------------------------------------------------------------
    DATA_DIR: str = str(BASE_DIR / "data")
    MODELS_DIR: str = str(BASE_DIR / "models")
    LOGS_DIR: str = str(BASE_DIR / "logs")

    # -----------------------------------------------------------------------
    # Database (placeholder — configure for production)
    # -----------------------------------------------------------------------
    # TODO: Replace with actual database URI when integrating a database.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///marketing_ai.db")

    # -----------------------------------------------------------------------
    # ML / Model settings
    # -----------------------------------------------------------------------
    MODEL_VERSION: str = os.getenv("MODEL_VERSION", "v1.0")
    RANDOM_STATE: int = 42
    TEST_SIZE: float = 0.2
    VALIDATION_SIZE: float = 0.1

    # -----------------------------------------------------------------------
    # Logging
    # -----------------------------------------------------------------------
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


class DevelopmentConfig(Config):
    """Development-specific configuration."""

    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    # TODO: Set a development-specific DATABASE_URL if needed.


class TestingConfig(Config):
    """Testing-specific configuration."""

    TESTING: bool = True
    DEBUG: bool = True
    # Use in-memory database for tests.
    DATABASE_URL: str = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Production-specific configuration."""

    DEBUG: bool = False
    # TODO: Ensure SECRET_KEY, DATABASE_URL, and other secrets are provided
    #       via environment variables in production.
