"""
Preprocessing Artifacts
=======================

Contains

• Standard Scaler
• Label Encoder
• Simple Imputer
• Feature Columns
"""

from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parent

SCALER = MODEL_DIR / "scaler.pkl"

ENCODER = MODEL_DIR / "encoder.pkl"

IMPUTER = MODEL_DIR / "imputer.pkl"

FEATURE_COLUMNS = (

    MODEL_DIR /

    "feature_columns.pkl"

)

__all__ = [

    "MODEL_DIR",

    "SCALER",

    "ENCODER",

    "IMPUTER",

    "FEATURE_COLUMNS"

]

