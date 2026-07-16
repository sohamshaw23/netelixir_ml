"""
shared/constants.py - Project-Wide Constants
=============================================
Marketing Intelligence AI Platform

Centralised definitions for column names, file paths, supported values, and
other constants used across all modules.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Base paths
# ---------------------------------------------------------------------------
BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = BASE_DIR / "data"
MODELS_DIR: Path = BASE_DIR / "models"
LOGS_DIR: Path = BASE_DIR / "logs"

# ---------------------------------------------------------------------------
# Data file paths
# ---------------------------------------------------------------------------
RAW_GOOGLE_ADS: str = str(DATA_DIR / "raw" / "google_ads.csv")
RAW_META_ADS: str = str(DATA_DIR / "raw" / "meta_ads.csv")
RAW_MICROSOFT_ADS: str = str(DATA_DIR / "raw" / "microsoft_ads.csv")
RAW_GA4: str = str(DATA_DIR / "raw" / "ga4_data.csv")
RAW_SHOPIFY: str = str(DATA_DIR / "raw" / "shopify_orders.csv")
RAW_CAMPAIGN_METADATA: str = str(DATA_DIR / "raw" / "campaign_metadata.csv")

MERGED_DATASET: str = str(DATA_DIR / "processed" / "merged_dataset.csv")
CLEANED_DATASET: str = str(DATA_DIR / "processed" / "cleaned_dataset.csv")
TRAIN_DATA: str = str(DATA_DIR / "processed" / "train.csv")
VALIDATION_DATA: str = str(DATA_DIR / "processed" / "validation.csv")
TEST_DATA: str = str(DATA_DIR / "processed" / "test.csv")

FEATURE_STORE: str = str(DATA_DIR / "features" / "feature_store.csv")
ENCODED_FEATURES: str = str(DATA_DIR / "features" / "encoded_features.pkl")
SCALED_FEATURES: str = str(DATA_DIR / "features" / "scaled_features.pkl")

PREDICTIONS_OUTPUT: str = str(DATA_DIR / "outputs" / "predictions.csv")
ANOMALIES_OUTPUT: str = str(DATA_DIR / "outputs" / "anomalies.csv")
SEGMENTS_OUTPUT: str = str(DATA_DIR / "outputs" / "customer_segments.csv")
CREATIVE_SCORES_OUTPUT: str = str(DATA_DIR / "outputs" / "creative_scores.csv")
REVENUE_RISK_OUTPUT: str = str(DATA_DIR / "outputs" / "revenue_risk.csv")

# ---------------------------------------------------------------------------
# Model artefact paths
# ---------------------------------------------------------------------------
XGBOOST_MODEL: str = str(MODELS_DIR / "revenue_drop_risk" / "xgboost.pkl")
LIGHTGBM_MODEL: str = str(MODELS_DIR / "revenue_drop_risk" / "lightgbm.pkl")
SHAP_EXPLAINER: str = str(MODELS_DIR / "revenue_drop_risk" / "shap_explainer.pkl")
ISOLATION_FOREST_MODEL: str = str(MODELS_DIR / "anomaly_detection" / "isolation_forest.pkl")
KMEANS_MODEL: str = str(MODELS_DIR / "customer_segmentation" / "kmeans.pkl")
CATBOOST_MODEL: str = str(MODELS_DIR / "creative_performance" / "catboost.cbm")

SCALER_PATH: str = str(MODELS_DIR / "preprocessors" / "scaler.pkl")
ENCODER_PATH: str = str(MODELS_DIR / "preprocessors" / "encoder.pkl")
IMPUTER_PATH: str = str(MODELS_DIR / "preprocessors" / "imputer.pkl")
FEATURE_COLUMNS_PATH: str = str(MODELS_DIR / "preprocessors" / "feature_columns.pkl")

# ---------------------------------------------------------------------------
# Standard column names
# ---------------------------------------------------------------------------
DATE_COL: str = "date"
REVENUE_COL: str = "revenue"
SPEND_COL: str = "spend"
CLICKS_COL: str = "clicks"
IMPRESSIONS_COL: str = "impressions"
CONVERSIONS_COL: str = "conversions"
CAMPAIGN_ID_COL: str = "campaign_id"
CHANNEL_COL: str = "channel"
CUSTOMER_ID_COL: str = "customer_id"
CREATIVE_ID_COL: str = "creative_id"
CTR_COL: str = "ctr"
CPC_COL: str = "cpc"
ROAS_COL: str = "roas"

# ---------------------------------------------------------------------------
# Supported channels
# ---------------------------------------------------------------------------
CHANNELS: list = ["google_ads", "meta_ads", "microsoft_ads"]

# ---------------------------------------------------------------------------
# Risk labels
# ---------------------------------------------------------------------------
RISK_LABELS: dict = {
    0: "Low Risk",
    1: "Medium Risk",
    2: "High Risk",
}

# ---------------------------------------------------------------------------
# Anomaly labels
# ---------------------------------------------------------------------------
ANOMALY_LABEL_NORMAL: str = "normal"
ANOMALY_LABEL_ANOMALY: str = "anomaly"
