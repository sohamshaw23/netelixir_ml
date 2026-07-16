"""
tests/test_preprocessing.py - Preprocessing Unit Tests
=======================================================
Marketing Intelligence AI Platform

Unit tests for preprocessing classes in all ML modules.
"""

import pandas as pd
import numpy as np
import pytest

from shared.preprocess import SharedPreprocessor
from revenue_drop_risk.preprocess import RevenuePreprocessor
from anomaly_detection.preprocess import AnomalyPreprocessor
from customer_segmentation.preprocess import SegmentationPreprocessor
from creative_performance.preprocess import CreativePreprocessor


# ---------------------------------------------------------------------------
# Shared preprocessor
# ---------------------------------------------------------------------------


def test_shared_preprocessor_instantiates():
    preprocessor = SharedPreprocessor()
    assert preprocessor is not None


def test_shared_preprocessor_transform_before_fit_raises():
    preprocessor = SharedPreprocessor()
    preprocessor._is_fitted = False
    with pytest.raises(RuntimeError):
        preprocessor.transform(pd.DataFrame(), [], [])


# ---------------------------------------------------------------------------
# Revenue preprocessor
# ---------------------------------------------------------------------------


def test_revenue_preprocessor_instantiates():
    preprocessor = RevenuePreprocessor()
    assert preprocessor is not None


def test_revenue_engineer_target_adds_column():
    preprocessor = RevenuePreprocessor()
    df = pd.DataFrame({"revenue": [100, 200, 150, 80]})
    result = preprocessor.engineer_target(df)
    assert preprocessor.target_column in result.columns


# ---------------------------------------------------------------------------
# Anomaly preprocessor
# ---------------------------------------------------------------------------


def test_anomaly_preprocessor_instantiates():
    preprocessor = AnomalyPreprocessor()
    assert preprocessor is not None


def test_anomaly_select_features_returns_dataframe():
    preprocessor = AnomalyPreprocessor()
    df = pd.DataFrame({"clicks": [10, 20], "impressions": [100, 200]})
    result = preprocessor.select_features(df)
    assert isinstance(result, pd.DataFrame)


# ---------------------------------------------------------------------------
# Segmentation preprocessor
# ---------------------------------------------------------------------------


def test_segmentation_preprocessor_instantiates():
    preprocessor = SegmentationPreprocessor()
    assert preprocessor is not None


# ---------------------------------------------------------------------------
# Creative preprocessor
# ---------------------------------------------------------------------------


def test_creative_preprocessor_instantiates():
    preprocessor = CreativePreprocessor()
    assert preprocessor is not None


def test_creative_engineer_target_adds_column():
    preprocessor = CreativePreprocessor()
    df = pd.DataFrame({"impressions": [1000, 5000], "clicks": [50, 200], "revenue": [300.0, 1500.0]})
    result = preprocessor.engineer_target(df)
    assert preprocessor.target_column in result.columns
