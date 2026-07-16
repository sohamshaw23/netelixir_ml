"""
Creative Performance Prediction Package
=======================================

Provides

• Data preprocessing
• Feature engineering
• CatBoost Training
• Prediction
• Evaluation
• Explainability
• Flask API

Author : Team AIgnition
Version : 1.0.0
"""

from .config import *
from .model import build_model
from .preprocess import preprocess
from .feature_engineering import create_features

from .predict import CreativePerformancePredictor
from .inference import predict_creative_performance

from .feature_importance import FeatureImportance
from .evaluation import CreativeEvaluator
from .visualization import CreativeVisualizer

__version__ = "1.0.0"

__all__ = [

    "build_model",

    "preprocess",

    "create_features",

    "CreativePerformancePredictor",

    "predict_creative_performance",

    "FeatureImportance",

    "CreativeEvaluator",

    "CreativeVisualizer"

]

