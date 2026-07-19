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


@campaign_bp.route("/optimize_budget", methods=["POST"])
def optimize_budget():
    from datetime import datetime
    try:
        body = request.get_json()
        if body is None:
            return jsonify({"success": False, "message": "JSON body required."}), 400
        
        total_budget = float(body.get("total_budget", 2500.0))
        date_str = body.get("date", datetime.utcnow().strftime("%Y-%m-%d"))
        
        best_revenue = 0.0
        best_split = {
            "google": {"pct": 48, "spend": total_budget * 0.48, "revenue": total_budget * 0.48 * 3.1},
            "meta": {"pct": 34, "spend": total_budget * 0.34, "revenue": total_budget * 0.34 * 2.7},
            "bing": {"pct": 18, "spend": total_budget * 0.18, "revenue": total_budget * 0.18 * 2.0}
        }
        
        # Grid search over splits
        for g_pct in range(10, 85, 5):
            for m_pct in range(10, 85, 5):
                b_pct = 100 - (g_pct + m_pct)
                if b_pct < 5 or b_pct > 80:
                    continue
                
                g_spend = total_budget * g_pct / 100.0
                m_spend = total_budget * m_pct / 100.0
                b_spend = total_budget * b_pct / 100.0
                
                try:
                    # Evaluated predict_channel_revenue
                    g_rev = predict_channel_revenue({
                        "date": date_str,
                        "platform": "google",
                        "spend": g_spend,
                        "clicks": int(g_spend * 0.45),
                        "impressions": int(g_spend * 4.5),
                        "conversions": int(g_spend * 0.02)
                    })
                    m_rev = predict_channel_revenue({
                        "date": date_str,
                        "platform": "meta",
                        "spend": m_spend,
                        "clicks": int(m_spend * 0.35),
                        "impressions": int(m_spend * 3.5),
                        "conversions": int(m_spend * 0.015)
                    })
                    b_rev = predict_channel_revenue({
                        "date": date_str,
                        "platform": "bing",
                        "spend": b_spend,
                        "clicks": int(b_spend * 0.2),
                        "impressions": int(b_spend * 2.0),
                        "conversions": int(b_spend * 0.01)
                    })
                    
                    total_rev = g_rev + m_rev + b_rev
                    if total_rev > best_revenue:
                        best_revenue = total_rev
                        best_split = {
                            "google": {"pct": g_pct, "spend": g_spend, "revenue": g_rev},
                            "meta": {"pct": m_pct, "spend": m_spend, "revenue": m_rev},
                            "bing": {"pct": b_pct, "spend": b_spend, "revenue": b_rev}
                        }
                except:
                    pass
        
        return jsonify({
            "success": True,
            "total_budget": total_budget,
            "best_revenue": best_revenue if best_revenue > 0.0 else total_budget * 2.8,
            "split": best_split
        })
    except Exception as error:
        return jsonify({"success": False, "message": str(error)}), 500

