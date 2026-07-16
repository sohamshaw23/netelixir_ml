"""
test_preprocessing.py

Tests preprocessing and feature engineering.
"""

import pandas as pd
import numpy as np
import pytest

# Revenue Model
from revenue_drop_risk.preprocess import preprocess as revenue_preprocess
from revenue_drop_risk.feature_engineering import create_features as revenue_features

# Anomaly Model
from anomaly_detection.preprocess import preprocess as anomaly_preprocess
from anomaly_detection.feature_engineering import create_features as anomaly_features

# Segmentation Model
from customer_segmentation.preprocess import preprocess as segmentation_preprocess
from customer_segmentation.feature_engineering import create_features as segmentation_features

# Creative Model
from creative_performance.preprocess import preprocess as creative_preprocess
from creative_performance.feature_engineering import create_features as creative_features


###########################################################
# Revenue Tests
###########################################################

def test_revenue_preprocess(sample_dataframe):

    df = revenue_preprocess(sample_dataframe.copy())

    assert isinstance(df, pd.DataFrame)

    assert df.isnull().sum().sum() == 0

    assert len(df.columns) > 0


def test_revenue_feature_engineering(sample_dataframe):

    df = revenue_features(sample_dataframe.copy())

    assert "Revenue_per_Click" in df.columns

    assert "Conversion_Rate" in df.columns

    assert "Revenue_to_Spend" in df.columns

    assert "Spend_per_Conversion" in df.columns

    assert "CTR_ROAS" in df.columns

    assert "Log_Revenue" in df.columns


###########################################################
# Anomaly Tests
###########################################################

def test_anomaly_preprocess(sample_dataframe):

    df = anomaly_preprocess(sample_dataframe.copy())

    assert df.isnull().sum().sum() == 0


def test_anomaly_feature_engineering(sample_dataframe):

    df = anomaly_features(sample_dataframe.copy())

    assert "Revenue_per_Click" in df.columns

    assert "Log_Spend" in df.columns


###########################################################
# Segmentation Tests
###########################################################

def test_segmentation_preprocess(sample_dataframe):

    df = segmentation_preprocess(sample_dataframe.copy())

    assert df.isnull().sum().sum() == 0


def test_segmentation_features(sample_dataframe):

    df = segmentation_features(sample_dataframe.copy())

    assert "CTR_ROAS" in df.columns

    assert "Log_Revenue" in df.columns


###########################################################
# Creative Tests
###########################################################

def test_creative_preprocess(sample_dataframe):

    df = creative_preprocess(sample_dataframe.copy())

    assert df.isnull().sum().sum() == 0


def test_creative_features(sample_dataframe):

    df = creative_features(sample_dataframe.copy())

    assert "Revenue_to_Spend" in df.columns

    assert "Spend_per_Conversion" in df.columns


###########################################################
# Missing Values
###########################################################

def test_missing_values():

    df = pd.DataFrame({

        "Spend":[1000, None],

        "Revenue":[None,5000],

        "Clicks":[120,None],

        "CampaignType":["Search",None]

    })

    processed = revenue_preprocess(df)

    assert processed.isnull().sum().sum() == 0


###########################################################
# Empty DataFrame
###########################################################

def test_empty_dataframe():

    df = pd.DataFrame()

    with pytest.raises(Exception):

        revenue_preprocess(df)


###########################################################
# Numeric Scaling
###########################################################

def test_numeric_scaling(sample_dataframe):

    processed = revenue_preprocess(sample_dataframe.copy())

    numeric = processed.select_dtypes(

        include=np.number

    )

    assert len(numeric.columns) > 0


###########################################################
# Feature Count
###########################################################

def test_feature_count(sample_dataframe):

    original = len(sample_dataframe.columns)

    engineered = revenue_features(sample_dataframe.copy())

    assert len(engineered.columns) > original


###########################################################
# Data Type Validation
###########################################################

def test_return_dataframe(sample_dataframe):

    df = revenue_preprocess(sample_dataframe.copy())

    assert isinstance(df, pd.DataFrame)


###########################################################
# Duplicate Rows
###########################################################

def test_duplicate_rows(sample_dataframe):

    duplicated = pd.concat(

        [sample_dataframe, sample_dataframe],

        ignore_index=True

    )

    processed = revenue_preprocess(duplicated)

    assert len(processed) == len(duplicated)

