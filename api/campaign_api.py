"""
api/campaign_api.py

Campaign Intelligence API endpoints for Revenue, ROAS, Campaign, and Channel predictions.
"""

from werkzeug.exceptions import HTTPException
from flask import Blueprint, jsonify, request

from campaign_intelligence.inference import (
    predict_revenue_lgbm,
    predict_roas_lgbm,
    predict_campaign_revenue,
    predict_channel_revenue
)

campaign_bp = Blueprint(
    "campaign",
    __name__
)

MODEL_METRICS = {
    "revenue": {"r2": 0.9161, "mae": 106.51},
    "roas": {"r2": 0.7157, "mae": 2.88},
    "campaign": {"r2": 0.82, "mae": 93.59},
    "channel": {"r2": 0.9060, "mae": 711.79}
}


@campaign_bp.route("/predict_revenue", methods=["POST"])
def predict_revenue():
    try:
        body = request.get_json()
        if body is None:
            return jsonify({"success": False, "message": "JSON body required."}), 400

        prediction = predict_revenue_lgbm(body)
        return jsonify({
            "success": True,
            "predicted_revenue": prediction,
            "model_metrics": MODEL_METRICS["revenue"]
        })
    except HTTPException as error:
        return jsonify({
            "success": False,
            "message": error.description
        }), error.code
    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


@campaign_bp.route("/predict_roas", methods=["POST"])
def predict_roas():
    try:
        body = request.get_json()
        if body is None:
            return jsonify({"success": False, "message": "JSON body required."}), 400

        prediction = predict_roas_lgbm(body)
        return jsonify({
            "success": True,
            "predicted_roas": prediction,
            "model_metrics": MODEL_METRICS["roas"]
        })
    except HTTPException as error:
        return jsonify({
            "success": False,
            "message": error.description
        }), error.code
    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


@campaign_bp.route("/predict_campaign", methods=["POST"])
def predict_campaign():
    try:
        body = request.get_json()
        if body is None:
            return jsonify({"success": False, "message": "JSON body required."}), 400

        prediction, rec = predict_campaign_revenue(body)
        return jsonify({
            "success": True,
            "predicted_campaign_revenue": prediction,
            "recommendation": rec,
            "model_metrics": MODEL_METRICS["campaign"]
        })
    except HTTPException as error:
        return jsonify({
            "success": False,
            "message": error.description
        }), error.code
    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


@campaign_bp.route("/predict_channel", methods=["POST"])
def predict_channel():
    try:
        body = request.get_json()
        if body is None:
            return jsonify({"success": False, "message": "JSON body required."}), 400

        prediction = predict_channel_revenue(body)
        return jsonify({
            "success": True,
            "predicted_channel_revenue": prediction,
            "model_metrics": MODEL_METRICS["channel"]
        })
    except HTTPException as error:
        return jsonify({
            "success": False,
            "message": error.description
        }), error.code
    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
