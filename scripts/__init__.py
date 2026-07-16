"""
scripts
=======

Utility scripts for the Marketing Intelligence Platform.

Available Pipelines
-------------------
1. Data Cleaning
2. Feature Generation
3. Model Training
4. Model Evaluation
5. Batch Prediction

Author: Team AIgnition
Version: 1.0.0
"""

from .clean_data import DataCleaner
from .generate_features import FeatureGenerator
from .train_all import TrainingPipeline
from .evaluate import EvaluationPipeline
from .predict_all import PredictionPipeline

__version__ = "1.0.0"

__all__ = [

    "DataCleaner",

    "FeatureGenerator",

    "TrainingPipeline",

    "EvaluationPipeline",

    "PredictionPipeline"

]

