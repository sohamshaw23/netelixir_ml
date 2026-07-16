"""
customer_segmentation/preprocess.py - Segmentation Preprocessing
================================================================
Marketing Intelligence AI Platform
"""

import logging
from typing import List

import numpy as np
import pandas as pd

from customer_segmentation.config import SEGMENTATION_FEATURE_COLUMNS
from shared.preprocess import SharedPreprocessor

logger = logging.getLogger(__name__)


class SegmentationPreprocessor:
    """
    Preprocessing pipeline for the Customer Segmentation module.

    TODO:
        - Implement select_features().
        - Implement scale() using MinMaxScaler or StandardScaler.
        - Add PCA dimensionality reduction for visualisation.
    """

    def __init__(self) -> None:
        self.shared_preprocessor = SharedPreprocessor(scaler_type="minmax")
        self.feature_columns: List[str] = SEGMENTATION_FEATURE_COLUMNS
        logger.info("SegmentationPreprocessor initialised.")

    def select_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Select and return segmentation-relevant features. TODO: Implement."""
        logger.info("Selecting segmentation features. TODO: Implement.")
        return df

    def scale(self, df: pd.DataFrame, fit: bool = True) -> np.ndarray:
        """Scale features. TODO: Implement."""
        logger.info("Scaling segmentation features. TODO: Implement.")
        return df.values

    def reduce_dimensions(self, X: np.ndarray, n_components: int = 2) -> np.ndarray:
        """Apply PCA for 2-D visualisation. TODO: Implement."""
        # TODO: from sklearn.decomposition import PCA; pca = PCA(n_components); return pca.fit_transform(X)
        logger.info("Reducing dimensions to %d. TODO: Implement.", n_components)
        return X[:, :n_components] if X.shape[1] >= n_components else X

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        """Full preprocessing on training data. TODO: Implement."""
        df = self.select_features(df)
        return self.scale(df, fit=True)
