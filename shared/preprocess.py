"""
shared/preprocess.py - Shared Preprocessing Utilities
======================================================
Marketing Intelligence AI Platform

Provides a shared preprocessing pipeline (imputation, scaling, encoding)
that can be reused by all ML modules.
"""

import logging
from typing import List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler

from shared.constants import ENCODER_PATH, IMPUTER_PATH, SCALER_PATH

logger = logging.getLogger(__name__)


class SharedPreprocessor:
    """
    Shared feature preprocessing pipeline.

    Handles:
        - Missing value imputation
        - Categorical label encoding
        - Numeric feature scaling

    TODO:
        - Add support for TargetEncoder and OneHotEncoder.
        - Add outlier clipping before scaling.
        - Persist preprocessor state to disk after fitting.
    """

    def __init__(
        self,
        numeric_strategy: str = "mean",
        categorical_strategy: str = "most_frequent",
        scaler_type: str = "standard",
    ) -> None:
        """
        Initialise preprocessor components.

        Args:
            numeric_strategy: Imputation strategy for numeric columns.
            categorical_strategy: Imputation strategy for categorical columns.
            scaler_type: ``"standard"`` (z-score) or ``"minmax"``.
        """
        self.numeric_imputer = SimpleImputer(strategy=numeric_strategy)
        self.categorical_imputer = SimpleImputer(strategy=categorical_strategy)
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler() if scaler_type == "standard" else MinMaxScaler()
        self._is_fitted: bool = False

    def fit(self, df: pd.DataFrame, numeric_cols: List[str], categorical_cols: List[str]) -> "SharedPreprocessor":
        """
        Fit all preprocessors on the training data.

        Args:
            df: Training DataFrame.
            numeric_cols: Columns to impute and scale.
            categorical_cols: Columns to impute and encode.

        Returns:
            self (fluent API).

        TODO: Implement actual fitting logic.
        """
        # TODO: Implement fit logic for imputer, encoder and scaler.
        logger.info("Fitting SharedPreprocessor. numeric=%d, categorical=%d", len(numeric_cols), len(categorical_cols))
        self._is_fitted = True
        return self

    def transform(self, df: pd.DataFrame, numeric_cols: List[str], categorical_cols: List[str]) -> pd.DataFrame:
        """
        Apply the fitted preprocessors to a DataFrame.

        Args:
            df: DataFrame to transform.
            numeric_cols: Numeric columns to process.
            categorical_cols: Categorical columns to process.

        Returns:
            pd.DataFrame: Transformed DataFrame.

        TODO: Implement actual transform logic.
        """
        if not self._is_fitted:
            raise RuntimeError("Call fit() before transform().")
        # TODO: Implement transform logic.
        logger.info("Transforming DataFrame with shape %s.", df.shape)
        return df.copy()

    def fit_transform(self, df: pd.DataFrame, numeric_cols: List[str], categorical_cols: List[str]) -> pd.DataFrame:
        """Fit then transform in a single call."""
        return self.fit(df, numeric_cols, categorical_cols).transform(df, numeric_cols, categorical_cols)

    def save(self, path: str = SCALER_PATH) -> None:
        """Persist the fitted preprocessor to disk using joblib. TODO: Implement."""
        # TODO: Save all sub-components to their respective paths.
        logger.info("Saving preprocessor to %s", path)

    @classmethod
    def load(cls, path: str = SCALER_PATH) -> "SharedPreprocessor":
        """Load a fitted preprocessor from disk. TODO: Implement."""
        # TODO: Load sub-components from disk.
        logger.info("Loading preprocessor from %s", path)
        instance = cls()
        instance._is_fitted = True
        return instance
