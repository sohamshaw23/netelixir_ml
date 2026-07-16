"""
test_models.py

Tests all trained ML models.

Run:
pytest tests/test_models.py
"""

from pathlib import Path

import joblib
import pandas as pd
import pytest

from revenue_drop_risk.predict import RevenueRiskPredictor
from anomaly_detection.detect import AnomalyDetector
from customer_segmentation.predict import CustomerSegmentPredictor
from creative_performance.predict import CreativePerformancePredictor


###############################################################
# Revenue Drop Risk
###############################################################

def test_revenue_model_exists():

    path = Path(
        "revenue_drop_risk/models/xgboost.pkl"
    )

    assert path.exists()


def test_revenue_predict(sample_dataframe):

    predictor = RevenueRiskPredictor()

    result = predictor.predict(sample_dataframe.copy())

    assert len(result) == len(sample_dataframe)

    assert "Revenue_Drop_Risk" in result.columns

    assert "Risk_Probability" in result.columns


###############################################################
# Isolation Forest
###############################################################

def test_anomaly_model_exists():

    path = Path(
        "anomaly_detection/models/isolation_forest.pkl"
    )

    assert path.exists()


def test_anomaly_prediction(sample_dataframe):

    detector = AnomalyDetector()

    result = detector.detect(sample_dataframe.copy())

    assert len(result) == len(sample_dataframe)

    assert "Anomaly" in result.columns

    assert "Severity" in result.columns

    assert "Anomaly_Score" in result.columns


###############################################################
# Customer Segmentation
###############################################################

def test_segmentation_model_exists():

    path = Path(
        "customer_segmentation/models/kmeans.pkl"
    )

    assert path.exists()


def test_segmentation_prediction(sample_dataframe):

    predictor = CustomerSegmentPredictor()

    result = predictor.predict(sample_dataframe.copy())

    assert len(result) == len(sample_dataframe)

    assert "Cluster" in result.columns

    assert "Business_Label" in result.columns


###############################################################
# Creative Performance
###############################################################

def test_creative_model_exists():

    path = Path(
        "creative_performance/models/catboost.cbm"
    )

    assert path.exists()


def test_creative_prediction(sample_dataframe):

    predictor = CreativePerformancePredictor()

    result = predictor.predict(sample_dataframe.copy())

    assert len(result) == len(sample_dataframe)

    assert "Performance_Score" in result.columns

    assert "Recommendation" in result.columns

    assert "Rank" in result.columns


###############################################################
# Generic Model Loading
###############################################################

@pytest.mark.parametrize(

    "model_path",

    [

        "revenue_drop_risk/models/xgboost.pkl",

        "anomaly_detection/models/isolation_forest.pkl",

        "customer_segmentation/models/kmeans.pkl",

    ]

)

def test_joblib_models(model_path):

    model = joblib.load(model_path)

    assert model is not None


###############################################################
# Feature Columns
###############################################################

@pytest.mark.parametrize(

    "path",

    [

        "revenue_drop_risk/models/feature_columns.pkl",

        "anomaly_detection/models/feature_columns.pkl",

        "customer_segmentation/models/feature_columns.pkl",

        "creative_performance/models/feature_columns.pkl",

    ]

)

def test_feature_columns(path):

    columns = joblib.load(path)

    assert isinstance(columns, list)

    assert len(columns) > 0


###############################################################
# Prediction Row Count
###############################################################

def test_prediction_row_count(sample_dataframe):

    revenue = RevenueRiskPredictor().predict(
        sample_dataframe.copy()
    )

    anomaly = AnomalyDetector().detect(
        sample_dataframe.copy()
    )

    segment = CustomerSegmentPredictor().predict(
        sample_dataframe.copy()
    )

    creative = CreativePerformancePredictor().predict(
        sample_dataframe.copy()
    )

    assert len(revenue) == len(sample_dataframe)

    assert len(anomaly) == len(sample_dataframe)

    assert len(segment) == len(sample_dataframe)

    assert len(creative) == len(sample_dataframe)


###############################################################
# Probability Range
###############################################################

def test_probability_range(sample_dataframe):

    revenue = RevenueRiskPredictor().predict(
        sample_dataframe.copy()
    )

    creative = CreativePerformancePredictor().predict(
        sample_dataframe.copy()
    )

    assert revenue["Risk_Probability"].between(
        0,
        1
    ).all()

    assert creative["Probability"].between(
        0,
        1
    ).all()


###############################################################
# Cluster Values
###############################################################

def test_cluster_values(sample_dataframe):

    prediction = CustomerSegmentPredictor().predict(
        sample_dataframe.copy()
    )

    assert prediction["Cluster"].dtype.kind in "iu"


###############################################################
# Anomaly Labels
###############################################################

def test_anomaly_labels(sample_dataframe):

    prediction = AnomalyDetector().detect(
        sample_dataframe.copy()
    )

    assert prediction["Anomaly"].isin(
        [-1, 1]
    ).all()

