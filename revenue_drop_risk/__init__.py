"""
Revenue Drop Risk Prediction Package
------------------------------------

This package provides utilities for:

• Data preprocessing
• Feature engineering
• Model training
• Prediction
• SHAP explainability
• Model evaluation
"""

from .config import *
from .model import build_model
from .preprocess import preprocess
from .feature_engineering import create_features
from .predict import RevenueRiskPredictor
from .inference import predict_revenue_risk
from .evaluation import ModelEvaluator
from .shap_analysis import SHAPAnalyzer

__version__ = "1.0.0"
__author__ = "Team AIgnition"

__all__ = [
    "build_model",
    "preprocess",
    "create_features",
    "RevenueRiskPredictor",
    "predict_revenue_risk",
    "ModelEvaluator",
    "SHAPAnalyzer",
]

