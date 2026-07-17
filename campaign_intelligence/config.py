"""
campaign_intelligence/config.py

Configuration parameters for the Campaign Intelligence models.
"""

from pathlib import Path

# Paths
PACKAGE_DIR = Path(__file__).resolve().parent
MODEL_DIR = PACKAGE_DIR / "models"
ROOT_DIR = PACKAGE_DIR.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "merged_ads_data.csv"

# Model parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2
MIN_HISTORY_DAYS = 14
