"""
app.py - Flask Application Factory
===================================
Marketing Intelligence AI Platform

Initializes and configures the Flask application, registers all Blueprints,
sets up logging, and prepares the app for production use via Gunicorn or
the built-in dev server.
"""

import logging
import os

from flask import Flask

from api import (
    anomaly_blueprint,
    creative_blueprint,
    revenue_blueprint,
    segmentation_blueprint,
    upload_blueprint,
)
from api.health import health_blueprint
from api.routes import routes_blueprint
from config import Config
from shared.logger import setup_logger


def create_app(config_object: object = Config) -> Flask:
    """
    Application factory function.

    Creates and configures the Flask application instance, registers all
    Blueprints, initialises logging, and ensures required directories exist.

    Args:
        config_object: A configuration class (defaults to :class:`config.Config`).

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    # ------------------------------------------------------------------
    # Load configuration
    # ------------------------------------------------------------------
    app.config.from_object(config_object)

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("Starting Marketing Intelligence AI Platform …")

    # ------------------------------------------------------------------
    # Ensure required runtime directories exist
    # ------------------------------------------------------------------
    _ensure_directories(app)

    # ------------------------------------------------------------------
    # Register Blueprints
    # ------------------------------------------------------------------
    _register_blueprints(app)

    logger.info("All Blueprints registered successfully.")
    return app


def _ensure_directories(app: Flask) -> None:
    """Create runtime directories that must exist before the first request."""
    dirs = [
        app.config.get("UPLOAD_FOLDER", "uploads"),
        "logs",
        os.path.join("data", "raw"),
        os.path.join("data", "processed"),
        os.path.join("data", "features"),
        os.path.join("data", "outputs"),
    ]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)


def _register_blueprints(app: Flask) -> None:
    """Register all application Blueprints with their URL prefixes."""
    app.register_blueprint(health_blueprint, url_prefix="/health")
    app.register_blueprint(routes_blueprint, url_prefix="/")
    app.register_blueprint(upload_blueprint, url_prefix="/api/upload")
    app.register_blueprint(revenue_blueprint, url_prefix="/api/revenue")
    app.register_blueprint(anomaly_blueprint, url_prefix="/api/anomaly")
    app.register_blueprint(segmentation_blueprint, url_prefix="/api/segmentation")
    app.register_blueprint(creative_blueprint, url_prefix="/api/creative")


# ---------------------------------------------------------------------------
# Module-level app instance (used by Gunicorn when running via run.py)
# ---------------------------------------------------------------------------
app = create_app()

if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST", "0.0.0.0"),
        port=int(app.config.get("PORT", 5000)),
        debug=app.config.get("DEBUG", False),
    )
