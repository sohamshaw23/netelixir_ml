"""
tests/test_models.py - ML Model Unit Tests
==========================================
Marketing Intelligence AI Platform

Unit tests for model class instantiation and placeholder methods.
"""

import numpy as np
import pytest

from revenue_drop_risk.model import EnsembleRevenueModel, LightGBMRevenueModel, XGBoostRevenueModel
from anomaly_detection.model import IsolationForestModel
from customer_segmentation.model import KMeansSegmentationModel
from creative_performance.model import CatBoostCreativeModel


# ---------------------------------------------------------------------------
# Revenue models
# ---------------------------------------------------------------------------


def test_xgboost_revenue_model_instantiates():
    model = XGBoostRevenueModel(params={"n_estimators": 10})
    assert model is not None


def test_xgboost_predict_returns_array():
    model = XGBoostRevenueModel()
    X = np.random.rand(5, 10)
    result = model.predict(X)
    assert isinstance(result, np.ndarray)


def test_lightgbm_revenue_model_instantiates():
    model = LightGBMRevenueModel()
    assert model is not None


def test_ensemble_model_instantiates():
    model = EnsembleRevenueModel()
    assert model.xgb_model is not None
    assert model.lgbm_model is not None


# ---------------------------------------------------------------------------
# Anomaly detection model
# ---------------------------------------------------------------------------


def test_isolation_forest_instantiates():
    model = IsolationForestModel()
    assert model is not None


def test_isolation_forest_predict_returns_array():
    model = IsolationForestModel()
    X = np.random.rand(10, 5)
    result = model.predict(X)
    assert isinstance(result, np.ndarray)
    assert len(result) == 10


# ---------------------------------------------------------------------------
# Segmentation model
# ---------------------------------------------------------------------------


def test_kmeans_instantiates():
    model = KMeansSegmentationModel(n_clusters=3)
    assert model.n_clusters == 3


def test_kmeans_predict_returns_zeros_placeholder():
    model = KMeansSegmentationModel()
    X = np.random.rand(8, 4)
    labels = model.predict(X)
    assert len(labels) == 8


# ---------------------------------------------------------------------------
# Creative performance model
# ---------------------------------------------------------------------------


def test_catboost_model_instantiates():
    model = CatBoostCreativeModel()
    assert model is not None


def test_catboost_predict_returns_zeros():
    model = CatBoostCreativeModel()
    X = np.random.rand(6, 8)
    scores = model.predict(X)
    assert len(scores) == 6
