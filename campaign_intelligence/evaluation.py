"""
campaign_intelligence/evaluation.py

Evaluation utilities for regression model performance.
"""

from sklearn.metrics import mean_absolute_error, r2_score


def evaluate_regression(y_true, y_pred):
    """
    Evaluate regression model using standard MAE and R2 score.
    """
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {
        "mae": round(float(mae), 4),
        "r2": round(float(r2), 4)
    }
