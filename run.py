"""
run.py - Application Entry Point
=================================
Marketing Intelligence AI Platform

Use this file to start the application in development mode:
    python run.py

For production, prefer Gunicorn:
    gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
"""

from app import create_app
from config import DevelopmentConfig, ProductionConfig
import os

# ---------------------------------------------------------------------------
# Select configuration based on FLASK_ENV environment variable
# ---------------------------------------------------------------------------
env = os.getenv("FLASK_ENV", "development").lower()

if env == "production":
    config = ProductionConfig
else:
    config = DevelopmentConfig

app = create_app(config)

if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST", "0.0.0.0"),
        port=int(app.config.get("PORT", 5000)),
        debug=app.config.get("DEBUG", True),
    )
