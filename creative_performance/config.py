from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR.parent /
    "data" /
    "processed" /
    "cleaned_dataset.csv"
)

MODEL_DIR = BASE_DIR / "models"

OUTPUT_DIR = BASE_DIR / "outputs"

LOG_DIR = BASE_DIR / "logs"

RANDOM_STATE = 42

TEST_SIZE = 0.2

TARGET_COLUMN = "CreativePerformance"

FEATURE_COLUMNS = [

    "Spend",

    "Revenue",

    "Clicks",

    "Impressions",

    "CTR",

    "CPC",

    "Conversions",

    "ROAS",

    "CampaignType",

    "Device",

    "Channel",

    "Audience",

    "CreativeType"

]

