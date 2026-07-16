"""
config.py

Application Configuration

Author : Team AIgnition
Version : 1.0.0
"""

import os
from pathlib import Path


############################################################
# Base Paths
############################################################

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

UPLOAD_DIR = BASE_DIR / "uploads"

REPORT_DIR = BASE_DIR / "reports"

MODEL_DIR = BASE_DIR / "models"

LOG_DIR = BASE_DIR / "logs"

STATIC_DIR = BASE_DIR / "static"

TEMPLATE_DIR = BASE_DIR / "templates"

OUTPUT_DIR = BASE_DIR / "outputs"


############################################################
# Flask
############################################################

class Config:

    SECRET_KEY = os.getenv(

        "SECRET_KEY",

        "marketing-intelligence-secret-key"

    )

    DEBUG = False

    TESTING = False

    JSON_SORT_KEYS = False

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    UPLOAD_FOLDER = str(UPLOAD_DIR)


############################################################

class DevelopmentConfig(Config):

    DEBUG = True


############################################################

class TestingConfig(Config):

    TESTING = True

    DEBUG = True


############################################################

class ProductionConfig(Config):

    DEBUG = False


############################################################
# ML Configuration
############################################################

RANDOM_STATE = 42

TEST_SIZE = 0.20

VALIDATION_SIZE = 0.10

MAX_CLUSTERS = 10

############################################################
# Allowed Uploads
############################################################

ALLOWED_EXTENSIONS = {

    "csv",

    "xlsx",

    "xls"

}

############################################################
# API
############################################################

API_VERSION = "v1"

PROJECT_NAME = "Marketing Intelligence Platform"

VERSION = "1.0.0"

AUTHOR = "Team AIgnition"

############################################################
# Logging
############################################################

LOG_LEVEL = "INFO"

############################################################
# Create Directories
############################################################

for folder in [

    DATA_DIR,

    RAW_DATA_DIR,

    PROCESSED_DATA_DIR,

    UPLOAD_DIR,

    REPORT_DIR,

    MODEL_DIR,

    LOG_DIR,

    STATIC_DIR,

    TEMPLATE_DIR,

    OUTPUT_DIR

]:

    folder.mkdir(

        parents=True,

        exist_ok=True

    )

############################################################
# Config Mapping
############################################################

config = {

    "development": DevelopmentConfig,

    "testing": TestingConfig,

    "production": ProductionConfig

}

