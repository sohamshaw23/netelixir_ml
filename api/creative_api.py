"""
api/creative_api.py - Creative Performance Blueprint
======================================================
Marketing Intelligence AI Platform

REST API endpoints for the Creative Performance Scoring module.
"""

import logging

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

creative_blueprint = Blueprint("creative", __name__)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@creative_blueprint.route("/score", methods=["POST"])
def score_creatives():
    """
    Score ad creatives for predicted performance.

    Request Body (JSON):
        {
            "data": [ { creative record }, ... ]
        }

    Returns:
        JSON: { "scores": [ { "creative_id": str, "score": float,
                               "rank": int }, ... ] }

    TODO:
        - Validate and deserialise input payload.
        - Call creative_performance.inference.CreativeInferencer.predict().
        - Return ranked scores and feature importances.
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid or missing JSON body."}), 400

    logger.info("Creative scoring requested with %d records.", len(payload.get("data", [])))

    # TODO: Implement creative scoring pipeline.
    return jsonify({"scores": [], "message": "TODO: Creative scoring not yet integrated."}), 200


@creative_blueprint.route("/importance", methods=["POST"])
def feature_importance():
    """
    Return feature importance for creative performance predictions.

    TODO:
        - Call creative_performance.feature_importance.get_importance().
        - Return top-N features that drive creative performance.
    """
    # TODO: Implement feature importance endpoint.
    return jsonify({"importance": [], "message": "TODO: Feature importance not yet implemented."}), 200


@creative_blueprint.route("/top", methods=["GET"])
def top_creatives():
    """
    Return the top-performing creatives from the last scoring run.

    TODO:
        - Load data/outputs/creative_scores.csv.
        - Return top-N rows ordered by score descending.
    """
    # TODO: Implement top creatives retrieval.
    return jsonify({"top_creatives": [], "message": "TODO: Top creatives not yet implemented."}), 200
