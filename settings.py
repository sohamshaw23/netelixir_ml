"""
settings.py - Global Runtime Settings
=======================================
Marketing Intelligence AI Platform

Centralised, non-configuration settings (feature flags, column name mappings,
model hyper-parameter defaults, etc.) that are independent of the deployment
environment.
"""

# ---------------------------------------------------------------------------
# Feature flags
# ---------------------------------------------------------------------------
ENABLE_SHAP_EXPLANATIONS: bool = True
ENABLE_ANOMALY_ALERTS: bool = True
ENABLE_SEGMENT_PROFILING: bool = True
ENABLE_CREATIVE_SCORING: bool = True

# ---------------------------------------------------------------------------
# Data column name constants
# ---------------------------------------------------------------------------
DATE_COLUMN: str = "date"
REVENUE_COLUMN: str = "revenue"
SPEND_COLUMN: str = "spend"
CLICKS_COLUMN: str = "clicks"
IMPRESSIONS_COLUMN: str = "impressions"
CONVERSIONS_COLUMN: str = "conversions"
CAMPAIGN_ID_COLUMN: str = "campaign_id"
CHANNEL_COLUMN: str = "channel"
CUSTOMER_ID_COLUMN: str = "customer_id"
CREATIVE_ID_COLUMN: str = "creative_id"

# ---------------------------------------------------------------------------
# Supported advertising channels
# ---------------------------------------------------------------------------
SUPPORTED_CHANNELS: list = [
    "google_ads",
    "meta_ads",
    "microsoft_ads",
]

# ---------------------------------------------------------------------------
# Default model hyper-parameters (placeholders)
# ---------------------------------------------------------------------------
# TODO: Tune these values after running experiments/HPO.

XGBOOST_PARAMS: dict = {
    "n_estimators": 300,
    "max_depth": 6,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": 42,
}

LIGHTGBM_PARAMS: dict = {
    "n_estimators": 300,
    "num_leaves": 63,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": 42,
}

CATBOOST_PARAMS: dict = {
    "iterations": 300,
    "depth": 6,
    "learning_rate": 0.05,
    "random_seed": 42,
    "verbose": 0,
}

ISOLATION_FOREST_PARAMS: dict = {
    "n_estimators": 100,
    "contamination": 0.05,
    "random_state": 42,
}

KMEANS_PARAMS: dict = {
    "n_clusters": 5,
    "random_state": 42,
    "n_init": 10,
}

# ---------------------------------------------------------------------------
# API response limits
# ---------------------------------------------------------------------------
MAX_PREDICTIONS_PER_REQUEST: int = 10_000
MAX_UPLOAD_ROWS: int = 500_000
