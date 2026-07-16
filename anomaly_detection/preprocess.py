"""
anomaly_detection/preprocess.py - Anomaly Detection Preprocessing
==================================================================
Marketing Intelligence AI Platform
"""

import logging
from typing import List

import numpy as np
import pandas as pd

from anomaly_detection.config import ANOMALY_FEATURE_COLUMNS
from shared.preprocess import SharedPreprocessor

logger = logging.getLogger(__name__)


class AnomalyPreprocessor:
    """
    Preprocessing pipeline for the Anomaly Detection module.

    TODO:
        - Implement select_features() to extract anomaly detection features.
        - Implement scale() using StandardScaler.
        - Add time-window aggregation features.
    """

    def __init__(self) -> None:
        self.shared_preprocessor = SharedPreprocessor()
        self.feature_columns: List[str] = ANOMALY_FEATURE_COLUMNS
        logger.info("AnomalyPreprocessor initialised.")

    def select_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Select features relevant for anomaly detection. TODO: Implement."""
        # TODO: Return df[self.feature_columns]
        logger.info("Selecting anomaly features. TODO: Implement.")
        return df

    def scale(self, df: pd.DataFrame, fit: bool = True) -> np.ndarray:
        """Scale features. TODO: Implement using SharedPreprocessor."""
        # TODO: Implement scaling.
        logger.info("Scaling anomaly features. TODO: Implement.")
        return df.values

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        """Full preprocessing on training data. TODO: Implement."""
        df = self.select_features(df)
        return self.scale(df, fit=True)

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Apply fitted preprocessing on new data. TODO: Implement."""
        df = self.select_features(df)
        return self.scale(df, fit=False)
