"""
creative_performance/feature_importance.py - Creative Feature Importance
========================================================================
Marketing Intelligence AI Platform
"""

import logging
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def get_importance(model, feature_names: List[str], top_n: int = 20) -> Dict[str, float]:
    """
    Extract and return top-N feature importances from a trained CatBoost model.

    Args:
        model: Trained CatBoostRegressor / CatBoostClassifier.
        feature_names: List of feature names in the training data.
        top_n: Number of top features to return.

    Returns:
        dict: { feature_name: importance_score } sorted descending.

    TODO:
        - Call model.get_feature_importance().
        - Pair with feature_names.
        - Return top-N sorted by importance.
    """
    # TODO: Implement feature importance extraction.
    logger.info("Extracting feature importance. TODO: Implement.")
    return {}


def plot_importance(importances: Dict[str, float], top_n: int = 20):
    """
    Generate a Plotly bar chart of feature importances.

    TODO: Use shared.visualization.plot_feature_importance().
    """
    # TODO: Implement importance visualisation.
    pass
