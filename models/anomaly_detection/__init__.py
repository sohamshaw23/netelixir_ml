"""
Anomaly Detection Models
========================

Contains

• Isolation Forest
"""

from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parent

ISOLATION_FOREST_MODEL = (

    MODEL_DIR /

    "isolation_forest.pkl"

)

__all__ = [

    "MODEL_DIR",

    "ISOLATION_FOREST_MODEL"

]

