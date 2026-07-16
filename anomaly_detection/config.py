"""
anomaly_detection/config.py - Anomaly Detection Configuration
=============================================================
Marketing Intelligence AI Platform
"""

from shared.constants import ISOLATION_FOREST_MODEL
from settings import ISOLATION_FOREST_PARAMS

# Model path
ISOLATION_FOREST_MODEL_PATH: str = ISOLATION_FOREST_MODEL

# Default hyperparameters
ISOLATION_FOREST_DEFAULT_PARAMS: dict = ISOLATION_FOREST_PARAMS

# Anomaly score threshold
# TODO: Calibrate threshold on labelled validation data.
ANOMALY_SCORE_THRESHOLD: float = 0.0  # IsolationForest uses decision_function score

# Features used for anomaly detection
# TODO: Populate after feature engineering.
ANOMALY_FEATURE_COLUMNS: list = []

# Number of samples to use for training (set None to use all)
MAX_TRAINING_SAMPLES: int = None
