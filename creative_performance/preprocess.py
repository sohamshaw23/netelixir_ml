"""
creative_performance/preprocess.py - Creative Performance Preprocessing
=======================================================================
Marketing Intelligence AI Platform
"""

import logging
from typing import List, Tuple

import numpy as np
import pandas as pd

from creative_performance.config import FEATURE_COLUMNS, MIN_IMPRESSIONS_THRESHOLD, TARGET_COLUMN
from shared.preprocess import SharedPreprocessor

logger = logging.getLogger(__name__)


class CreativePreprocessor:
    """
    Preprocessing pipeline for the Creative Performance module.

    TODO:
        - Implement filter_by_impressions() to remove low-traffic creatives.
        - Implement engineer_target() to create the performance score.
        - Implement encode_categoricals() for ad format, platform, etc.
        - Implement select_features() for model-ready feature matrix.
    """

    def __init__(self) -> None:
        self.shared_preprocessor = SharedPreprocessor()
        self.feature_columns: List[str] = FEATURE_COLUMNS
        self.target_column: str = TARGET_COLUMN
        logger.info("CreativePreprocessor initialised.")

    def filter_by_impressions(self, df: pd.DataFrame, threshold: int = MIN_IMPRESSIONS_THRESHOLD) -> pd.DataFrame:
        """Remove creatives with insufficient impressions. TODO: Implement."""
        # TODO: return df[df["impressions"] >= threshold]
        logger.info("Filtering by impressions threshold=%d. TODO: Implement.", threshold)
        return df

    def engineer_target(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute the creative performance score target.

        Ideas: ROAS, CTR-normalised conversions, revenue per impression.

        TODO: Implement target engineering.
        """
        # TODO: Define and compute performance score.
        df[self.target_column] = 0.0
        return df

    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Separate features and target. TODO: Implement."""
        X = df.drop(columns=[self.target_column], errors="ignore")
        y = df.get(self.target_column, pd.Series(dtype=float))
        return X, y

    def fit_transform(self, df: pd.DataFrame) -> Tuple:
        """Full preprocessing on training data. TODO: Implement."""
        logger.info("Running CreativePreprocessor.fit_transform(). TODO: Implement.")
        df = self.filter_by_impressions(df)
        df = self.engineer_target(df)
        return self.prepare_features(df)
