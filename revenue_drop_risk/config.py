from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR.parent / "data" / "processed" / "cleaned_dataset.csv"

MODEL_DIR = BASE_DIR / "models"

OUTPUT_DIR = BASE_DIR / "outputs"

LOG_DIR = BASE_DIR / "logs"

MODEL_NAME = "xgboost.pkl"

RANDOM_STATE = 42

TEST_SIZE = 0.2

TARGET_COLUMN = "RevenueDrop"

FEATURE_COLUMNS = [
    "Spend",
    "Clicks",
    "Impressions",
    "CTR",
    "CPC",
    "Conversions",
    "Revenue",
    "ROAS",
    "CampaignType",
    "Device",
    "Channel"
]