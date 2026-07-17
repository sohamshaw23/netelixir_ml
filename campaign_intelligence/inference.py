"""
campaign_intelligence/inference.py

Lazy-loaded wrapper functions for the Flask API layer.
"""

from .predict import CampaignIntelligencePredictor

_predictor = None


def get_predictor():
    """
    Lazy instantiates the predictor class to avoid import-time file system overhead.
    """
    global _predictor
    if _predictor is None:
        _predictor = CampaignIntelligencePredictor()
    return _predictor


def predict_revenue_lgbm(data):
    """
    Predict total revenue using LGBM model.
    """
    predictor = get_predictor()
    return predictor.predict_revenue(data)


def predict_roas_lgbm(data):
    """
    Predict ROAS using LGBM model.
    """
    predictor = get_predictor()
    return predictor.predict_roas(data)


def predict_campaign_revenue(data):
    """
    Predict Campaign Revenue and get recommendation using LGBM.
    """
    predictor = get_predictor()
    return predictor.predict_campaign(data)


def predict_channel_revenue(data):
    """
    Predict Channel Revenue using LGBM model.
    """
    predictor = get_predictor()
    return predictor.predict_channel(data)
