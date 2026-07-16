"""
api/routes.py - Main Web Routes Blueprint
==========================================
Marketing Intelligence AI Platform

Serves HTML page templates (index, dashboard, upload, result).
"""

import logging

from flask import Blueprint, render_template

logger = logging.getLogger(__name__)

routes_blueprint = Blueprint("routes", __name__)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------


@routes_blueprint.route("/", methods=["GET"])
def index():
    """Render the landing / home page."""
    logger.debug("Serving index page.")
    return render_template("index.html")


@routes_blueprint.route("/dashboard", methods=["GET"])
def dashboard():
    """Render the main analytics dashboard."""
    logger.debug("Serving dashboard page.")
    # TODO: Pass real KPI data fetched from the DB / cache.
    return render_template("dashboard.html")


@routes_blueprint.route("/upload", methods=["GET"])
def upload_page():
    """Render the data upload page."""
    logger.debug("Serving upload page.")
    return render_template("upload.html")


@routes_blueprint.route("/result", methods=["GET"])
def result_page():
    """Render the results / prediction output page."""
    logger.debug("Serving result page.")
    # TODO: Pass prediction results from session or query params.
    return render_template("result.html")
