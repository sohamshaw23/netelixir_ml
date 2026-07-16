"""
anomaly_detection/visualization.py - Anomaly Visualisations
============================================================
Marketing Intelligence AI Platform
"""

import logging
from typing import List

import pandas as pd
import plotly.graph_objects as go

logger = logging.getLogger(__name__)


def plot_anomaly_scores(df: pd.DataFrame, score_col: str, date_col: str, threshold: float = 0.0) -> go.Figure:
    """
    Plot anomaly scores over time with threshold line.

    TODO: Implement with anomaly markers and threshold line.
    """
    # TODO: Implement anomaly score timeline chart.
    logger.debug("Generating anomaly score plot. TODO: Implement.")
    return go.Figure()


def plot_anomaly_distribution(scores: List[float]) -> go.Figure:
    """
    Plot the distribution of anomaly scores as a histogram.

    TODO: Implement with vertical threshold marker.
    """
    # TODO: Implement score distribution histogram.
    return go.Figure()
