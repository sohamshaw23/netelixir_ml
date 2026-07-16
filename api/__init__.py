"""
api/__init__.py - API Package Initialiser
==========================================
Marketing Intelligence AI Platform

Exports all Blueprints so that app.py can register them via a single import.
"""

from api.anomaly_api import anomaly_blueprint
from api.creative_api import creative_blueprint
from api.revenue_api import revenue_blueprint
from api.segmentation_api import segmentation_blueprint
from api.upload import upload_blueprint

__all__ = [
    "revenue_blueprint",
    "anomaly_blueprint",
    "segmentation_blueprint",
    "creative_blueprint",
    "upload_blueprint",
]
