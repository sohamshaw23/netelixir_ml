"""
Creative Performance Models
===========================

Contains

• CatBoost Model
"""

from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parent

CATBOOST_MODEL = (

    MODEL_DIR /

    "catboost.cbm"

)

__all__ = [

    "MODEL_DIR",

    "CATBOOST_MODEL"

]

