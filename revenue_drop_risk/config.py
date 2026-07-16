"""
revenue_drop_risk/config.py - Revenue Drop Risk Module Configuration
=====================================================================
Marketing Intelligence AI Platform
"""

from shared.constants import LIGHTGBM_MODEL, SHAP_EXPLAINER, XGBOOST_MODEL
from settings import LIGHTGBM_PARAMS, XGBOOST_PARAMS

# Model paths
XGBOOST_MODEL_PATH: str = XGBOOST_MODEL
LIGHTGBM_MODEL_PATH: str = LIGHTGBM_MODEL
SHAP_EXPLAINER_PATH: str = SHAP_EXPLAINER

# Training parameters
XGBOOST_DEFAULT_PARAMS: dict = XGBOOST_PARAMS
LIGHTGBM_DEFAULT_PARAMS: dict = LIGHTGBM_PARAMS

# Risk thresholds
# TODO: Calibrate these thresholds on a hold-out validation set.
LOW_RISK_THRESHOLD: float = 0.3
HIGH_RISK_THRESHOLD: float = 0.7

# Target column
TARGET_COLUMN: str = "revenue_drop_flag"

# Feature columns used by this module
# TODO: Populate after feature engineering is complete.
FEATURE_COLUMNS: list = []

# Cross-validation folds
CV_FOLDS: int = 5

# SHAP settings
SHAP_BACKGROUND_SAMPLES: int = 100
