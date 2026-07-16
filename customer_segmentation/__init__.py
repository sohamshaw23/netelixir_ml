"""
Customer Segmentation Package
=============================

Provides:

• Data preprocessing
• Feature engineering
• KMeans clustering
• Cluster analysis
• Evaluation
• Prediction
• Inference API

Author : Team AIgnition
Version : 1.0.0
"""

from .config import *
from .model import build_model
from .preprocess import preprocess
from .feature_engineering import create_features

from .predict import CustomerSegmentPredictor
from .inference import segment_customers

from .cluster_analysis import ClusterAnalysis
from .visualization import ClusterVisualizer
from .evaluation import ClusterEvaluator

__version__ = "1.0.0"

__all__ = [

    "build_model",

    "preprocess",

    "create_features",

    "CustomerSegmentPredictor",

    "segment_customers",

    "ClusterAnalysis",

    "ClusterVisualizer",

    "ClusterEvaluator"

]

