"""
Revenue Drop Risk Models
========================

Contains

• XGBoost
• LightGBM
• SHAP Explainer
"""

from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parent

XGBOOST_MODEL = MODEL_DIR / "xgboost.pkl"

LIGHTGBM_MODEL = MODEL_DIR / "lightgbm.pkl"

SHAP_EXPLAINER = MODEL_DIR / "shap_explainer.pkl"

__all__ = [

    "MODEL_DIR",

    "XGBOOST_MODEL",

    "LIGHTGBM_MODEL",

    "SHAP_EXPLAINER"

]

