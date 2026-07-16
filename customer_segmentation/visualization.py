"""
customer_segmentation/visualization.py - Segmentation Visualisations
=====================================================================
Marketing Intelligence AI Platform
"""

import logging

import numpy as np
import pandas as pd
import plotly.graph_objects as go

logger = logging.getLogger(__name__)


def plot_cluster_scatter_2d(X_2d: np.ndarray, labels: np.ndarray, title: str = "Customer Segments") -> go.Figure:
    """
    2-D scatter plot of customer segments (after PCA/t-SNE).

    TODO: Implement with colour coding per segment.
    """
    # TODO: Implement.
    return go.Figure()


def plot_cluster_sizes(labels: np.ndarray) -> go.Figure:
    """
    Bar chart showing the size of each cluster.

    TODO: Implement.
    """
    return go.Figure()


def plot_segment_radar(profiles: pd.DataFrame) -> go.Figure:
    """
    Radar chart comparing segment profiles across key metrics.

    TODO: Implement spider/radar chart per segment.
    """
    return go.Figure()
