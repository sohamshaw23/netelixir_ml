"""
revenue_drop_risk/utils.py - Revenue Risk Utilities
====================================================
Marketing Intelligence AI Platform
"""

import logging
from typing import List

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def compute_revenue_change(df: pd.DataFrame, revenue_col: str, period: int = 7) -> pd.Series:
    """
    Compute period-over-period revenue change percentage.

    Args:
        df: DataFrame with revenue column.
        revenue_col: Name of the revenue column.
        period: Look-back period in rows (e.g., 7 for weekly).

    Returns:
        pd.Series: Percentage change values.

    TODO: Implement revenue change computation.
    """
    # TODO: return df[revenue_col].pct_change(periods=period) * 100
    logger.debug("Computing revenue change. TODO: Implement.")
    return pd.Series(dtype=float)


def threshold_to_label(scores: np.ndarray, low: float = 0.3, high: float = 0.7) -> List[str]:
    """
    Convert continuous risk scores to categorical labels.

    Args:
        scores: Array of risk probability scores.
        low: Threshold below which risk is "Low".
        high: Threshold above which risk is "High".

    Returns:
        List[str]: Risk labels.

    TODO: Use settings.RISK_LABELS for label lookup.
    """
    # TODO: Implement label assignment.
    return []
