"""
routes.py

Registers all Blueprints
"""

from flask import Blueprint

from .health import health_bp
from .upload import upload_bp

from .revenue_api import revenue_bp
from .anomaly_api import anomaly_bp
from .segmentation_api import segmentation_bp
from .creative_api import creative_bp
from .campaign_api import campaign_bp


def register_routes(app):

    app.register_blueprint(

        health_bp,

        url_prefix="/health"

    )

    app.register_blueprint(

        upload_bp,

        url_prefix="/upload"

    )

    app.register_blueprint(

        revenue_bp,

        url_prefix="/revenue"

    )

    app.register_blueprint(

        anomaly_bp,

        url_prefix="/anomaly"

    )

    app.register_blueprint(

        segmentation_bp,

        url_prefix="/segment"

    )

    app.register_blueprint(

        creative_bp,

        url_prefix="/creative"

    )

    app.register_blueprint(

        campaign_bp,

        url_prefix="/campaign"

    )

    return app