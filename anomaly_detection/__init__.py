"""
Anomaly Detection Package
=========================

This package provides:

• Data preprocessing
• Feature engineering
• Isolation Forest training
• Anomaly detection
• Visualization
• Evaluation
• Inference API

Author : Team AIgnition
Version : 1.0.0
"""

from .config import *
from .model import build_model
from .preprocess import preprocess
from .feature_engineering import create_features

from .detect import AnomalyDetector
from .inference import detect_anomalies

from .evaluation import AnomalyEvaluator
from .visualization import AnomalyVisualizer

__version__ = "1.0.0"

__all__ = [

    "build_model",

    "preprocess",

    "create_features",

    "AnomalyDetector",

    "detect_anomalies",

    "AnomalyEvaluator",

    "AnomalyVisualizer"

]

