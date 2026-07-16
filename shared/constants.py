"""
shared/constants.py

Global constants used across the project.
"""

from pathlib import Path

##############################################################
# Project Paths
##############################################################

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = BASE_DIR / "models"

UPLOADS_DIR = BASE_DIR / "uploads"

REPORTS_DIR = BASE_DIR / "reports"

LOGS_DIR = BASE_DIR / "logs"

STATIC_DIR = BASE_DIR / "static"

TEMPLATES_DIR = BASE_DIR / "templates"

##############################################################
# Default Files
##############################################################

RAW_DATASET = RAW_DATA_DIR / "marketing_data.csv"

CLEAN_DATASET = PROCESSED_DATA_DIR / "cleaned_dataset.csv"

FEATURE_DATASET = PROCESSED_DATA_DIR / "features_dataset.csv"

##############################################################
# Model Files
##############################################################

REVENUE_MODEL = (
    BASE_DIR /
    "revenue_drop_risk" /
    "models" /
    "xgboost.pkl"
)

ANOMALY_MODEL = (
    BASE_DIR /
    "anomaly_detection" /
    "models" /
    "isolation_forest.pkl"
)

SEGMENT_MODEL = (
    BASE_DIR /
    "customer_segmentation" /
    "models" /
    "kmeans.pkl"
)

CREATIVE_MODEL = (
    BASE_DIR /
    "creative_performance" /
    "models" /
    "catboost.cbm"
)

##############################################################
# Preprocessing Artifacts
##############################################################

SCALER_FILE = (
    MODELS_DIR /
    "scaler.pkl"
)

ENCODER_FILE = (
    MODELS_DIR /
    "encoders.pkl"
)

FEATURE_COLUMNS_FILE = (
    MODELS_DIR /
    "feature_columns.pkl"
)

##############################################################
# Random Seed
##############################################################

RANDOM_STATE = 42

##############################################################
# ML Parameters
##############################################################

TEST_SIZE = 0.20

VALIDATION_SIZE = 0.10

MAX_CLUSTERS = 10

##############################################################
# File Upload
##############################################################

ALLOWED_EXTENSIONS = {

    "csv",

    "xlsx",

    "xls"

}

MAX_UPLOAD_SIZE = 50 * 1024 * 1024

##############################################################
# Target Columns
##############################################################

REVENUE_TARGET = "RevenueDropRisk"

CREATIVE_TARGET = "CreativePerformance"

##############################################################
# Feature Lists
##############################################################

NUMERIC_FEATURES = [

    "Spend",

    "Revenue",

    "Clicks",

    "Impressions",

    "CTR",

    "CPC",

    "Conversions",

    "ROAS"

]

CATEGORICAL_FEATURES = [

    "CampaignType",

    "Channel",

    "Device",

    "Audience",

    "CreativeType"

]

##############################################################
# Generated Features
##############################################################

ENGINEERED_FEATURES = [

    "Revenue_per_Click",

    "Conversion_Rate",

    "Revenue_to_Spend",

    "Spend_per_Conversion",

    "CTR_ROAS",

    "Revenue_per_Impression",

    "Clicks_per_Impression",

    "Cost_per_Impression",

    "Log_Revenue",

    "Log_Spend",

    "Log_Clicks",

    "High_ROAS"

]

##############################################################
# Dashboard Colors
##############################################################

SUCCESS_COLOR = "#4CAF50"

WARNING_COLOR = "#FFC107"

ERROR_COLOR = "#F44336"

PRIMARY_COLOR = "#1976D2"

##############################################################
# API
##############################################################

API_VERSION = "v1"

PROJECT_NAME = "Marketing Intelligence Platform"

AUTHOR = "Team AIgnition"

VERSION = "1.0.0"

##############################################################
# Create Required Directories
##############################################################

for directory in [

    DATA_DIR,

    RAW_DATA_DIR,

    PROCESSED_DATA_DIR,

    MODELS_DIR,

    UPLOADS_DIR,

    REPORTS_DIR,

    LOGS_DIR

]:

    directory.mkdir(

        parents=True,

        exist_ok=True

    )

