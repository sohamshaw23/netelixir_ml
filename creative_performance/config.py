"""
creative_performance/config.py - Creative Performance Configuration
===================================================================
Marketing Intelligence AI Platform
"""

from shared.constants import CATBOOST_MODEL
from settings import CATBOOST_PARAMS

CATBOOST_MODEL_PATH: str = CATBOOST_MODEL
CATBOOST_DEFAULT_PARAMS: dict = CATBOOST_PARAMS

# Target column
TARGET_COLUMN: str = "creative_performance_score"

# Feature columns used for creative scoring
# TODO: Define after EDA and feature engineering.
FEATURE_COLUMNS: list = []

# Top-N creatives to surface in the dashboard
TOP_N_CREATIVES: int = 10

# Minimum impressions required for a creative to be scored
MIN_IMPRESSIONS_THRESHOLD: int = 1000
