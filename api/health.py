"""
api/health.py - Health Check Blueprint
========================================
Marketing Intelligence AI Platform

Provides a lightweight health-check endpoint used by load balancers,
container orchestrators (Kubernetes), and uptime monitors.
"""

import logging
import platform
import sys
import time

from flask import Blueprint, jsonify

logger = logging.getLogger(__name__)

health_blueprint = Blueprint("health", __name__)

# Application start time (used to compute uptime)
_START_TIME: float = time.time()


@health_blueprint.route("/", methods=["GET"])
def health_check():
    """
    Liveness probe endpoint.

    Returns:
        JSON: status, uptime, Python version, and platform info.
    """
    uptime_seconds = round(time.time() - _START_TIME, 2)
    payload = {
        "status": "ok",
        "uptime_seconds": uptime_seconds,
        "python_version": sys.version,
        "platform": platform.platform(),
        "service": "Marketing Intelligence AI Platform",
    }
    logger.debug("Health check requested. Uptime: %s seconds.", uptime_seconds)
    return jsonify(payload), 200


@health_blueprint.route("/ready", methods=["GET"])
def readiness_check():
    """
    Readiness probe endpoint.

    TODO: Add real checks (DB connection, model files present, etc.).

    Returns:
        JSON: ready status and component checks.
    """
    # TODO: Implement real readiness checks per component.
    checks = {
        "models_loaded": False,  # TODO: verify model artefacts are loaded
        "data_available": False,  # TODO: verify data directories exist
    }
    all_ready = all(checks.values())
    status_code = 200 if all_ready else 503
    return jsonify({"ready": all_ready, "checks": checks}), status_code
