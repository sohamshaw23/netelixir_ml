"""
revenue_drop_risk/preprocess.py - Revenue Risk Preprocessing
=============================================================
Marketing Intelligence AI Platform

Data preprocessing specific to the Revenue Drop Risk module.
"""

import logging
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from revenue_drop_risk.config import FEATURE_COLUMNS, TARGET_COLUMN
from shared.preprocess import SharedPreprocessor

logger = logging.getLogger(__name__)


class RevenuePreprocessor:
    """
    Preprocessing pipeline for the Revenue Drop Risk module.

    TODO:
        - Define feature columns after EDA.
        - Implement label engineering (create binary drop flag).
        - Add class-imbalance handling (SMOTE, class_weight).
    """

    def __init__(self) -> None:
        self.shared_preprocessor = SharedPreprocessor()
        self.feature_columns: List[str] = FEATURE_COLUMNS
        self.target_column: str = TARGET_COLUMN
        logger.info("RevenuePreprocessor initialised.")

    def engineer_target(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create the binary revenue drop flag target column.

        Logic: flag = 1 if revenue drops by > X% week-over-week.

        TODO: Implement target engineering logic.
        """
        # TODO: Implement revenue drop flag creation.
        logger.info("Engineering target column. TODO: Implement.")
        df[self.target_column] = 0  # placeholder
        return df

    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Separate features and target from *df*.

        Returns:
            Tuple[pd.DataFrame, pd.Series]: (X, y)

        TODO: Implement feature selection and target extraction.
        """
        # TODO: Implement feature/target split.
        X = df.drop(columns=[self.target_column], errors="ignore")
        y = df.get(self.target_column, pd.Series(dtype=int))
        return X, y

    def split_data(
        self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, val_size: float = 0.1
    ) -> Tuple:
        """
        Split data into train, validation, and test sets.

        Returns:
            Tuple: (X_train, X_val, X_test, y_train, y_val, y_test)

        TODO: Implement time-based splitting for time-series data.
        """
        # TODO: Implement time-aware train/val/test split.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=val_size, random_state=42)
        return X_train, X_val, X_test, y_train, y_val, y_test

    def fit_transform(self, df: pd.DataFrame) -> Tuple:
        """
        Full preprocessing pipeline on training data.

        TODO: Implement end-to-end preprocessing.
        """
        logger.info("Running RevenuePreprocessor.fit_transform(). TODO: Implement.")
        return df, pd.Series(dtype=int)
