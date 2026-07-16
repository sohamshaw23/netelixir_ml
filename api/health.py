"""
health.py
----------

Health Check API

Endpoint:
GET /health
"""

from flask import Blueprint
from flask import jsonify
from datetime import datetime

health_bp = Blueprint(
    "health",
    __name__
)


@health_bp.route("/", methods=["GET"])
def health():

    response = {

        "status": "healthy",

        "message": "Marketing Intelligence API is running.",

        "timestamp": datetime.utcnow().isoformat() + "Z",

        "version": "1.0.0",

        "available_models": [

            "Revenue Drop Risk",

            "Anomaly Detection",

            "Customer Segmentation",

            "Creative Performance"

        ]

    }

    return jsonify(response), 200