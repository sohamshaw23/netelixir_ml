"""
settings.py

Global Project Settings

Author : Team AIgnition
Version : 1.0.0
"""

import os
from pathlib import Path

############################################################
# Base Directory
############################################################

BASE_DIR = Path(__file__).resolve().parent

############################################################
# Environment
############################################################

ENVIRONMENT = os.getenv(

    "APP_ENV",

    "development"

)

DEBUG = ENVIRONMENT == "development"

TESTING = ENVIRONMENT == "testing"

############################################################
# Flask
############################################################

HOST = os.getenv(

    "HOST",

    "0.0.0.0"

)

PORT = int(

    os.getenv(

        "PORT",

        5000

    )

)

SECRET_KEY = os.getenv(

    "SECRET_KEY",

    "marketing-intelligence-secret"

)

############################################################
# API
############################################################

API_NAME = "Marketing Intelligence Platform"

API_VERSION = "1.0.0"

API_PREFIX = "/api"

############################################################
# Upload Settings
############################################################

UPLOAD_FOLDER = BASE_DIR / "uploads"

MAX_UPLOAD_SIZE = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = {

    "csv",

    "xlsx",

    "xls"

}

############################################################
# ML Configuration
############################################################

RANDOM_STATE = 42

TEST_SIZE = 0.20

VALIDATION_SIZE = 0.10

MAX_CLUSTERS = 10

############################################################
# Model Paths
############################################################

MODEL_DIR = BASE_DIR / "models"

REVENUE_MODEL = (

    MODEL_DIR /

    "revenue_drop_risk" /

    "xgboost.pkl"

)

LIGHTGBM_MODEL = (

    MODEL_DIR /

    "revenue_drop_risk" /

    "lightgbm.pkl"

)

ISOLATION_FOREST_MODEL = (

    MODEL_DIR /

    "anomaly_detection" /

    "isolation_forest.pkl"

)

KMEANS_MODEL = (

    MODEL_DIR /

    "customer_segmentation" /

    "kmeans.pkl"

)

CATBOOST_MODEL = (

    MODEL_DIR /

    "creative_performance" /

    "catboost.cbm"

)

############################################################
# Preprocessors
############################################################

PREPROCESSOR_DIR = MODEL_DIR / "preprocessors"

SCALER = PREPROCESSOR_DIR / "scaler.pkl"

ENCODER = PREPROCESSOR_DIR / "encoder.pkl"

IMPUTER = PREPROCESSOR_DIR / "imputer.pkl"

FEATURE_COLUMNS = (

    PREPROCESSOR_DIR /

    "feature_columns.pkl"

)

############################################################
# Data
############################################################

DATA_DIR = BASE_DIR / "data"

RAW_DATA = (

    DATA_DIR /

    "raw"

)

PROCESSED_DATA = (

    DATA_DIR /

    "processed"

)

############################################################
# Reports
############################################################

REPORT_DIR = BASE_DIR / "reports"

PLOTS_DIR = REPORT_DIR / "plots"

############################################################
# Logging
############################################################

LOG_DIR = BASE_DIR / "logs"

LOG_LEVEL = "INFO"

############################################################
# Feature Flags
############################################################

ENABLE_SHAP = True

ENABLE_VISUALIZATION = True

ENABLE_API_LOGGING = True

ENABLE_BATCH_PREDICTION = True

############################################################
# Dashboard
############################################################

TOP_CUSTOMERS = 20

TOP_ANOMALIES = 20

TOP_CREATIVES = 20

############################################################
# Database (Future)
############################################################

DATABASE_URL = os.getenv(

    "DATABASE_URL",

    ""

)

############################################################
# Create Directories
############################################################

directories = [

    UPLOAD_FOLDER,

    REPORT_DIR,

    PLOTS_DIR,

    LOG_DIR,

    DATA_DIR,

    RAW_DATA,

    PROCESSED_DATA,

]

for directory in directories:

    directory.mkdir(

        parents=True,

        exist_ok=True

    )

############################################################
# Project Metadata
############################################################

PROJECT = {

    "name": API_NAME,

    "version": API_VERSION,

    "author": "Team AIgnition",

    "environment": ENVIRONMENT

}

