"""
test_utils.py

Tests utility/helper functions.

Run:
pytest tests/test_utils.py
"""

import logging
from pathlib import Path
import tempfile
import pandas as pd
import pytest

from revenue_drop_risk.utils import get_logger as revenue_logger
from anomaly_detection.utils import get_logger as anomaly_logger
from customer_segmentation.utils import get_logger as segmentation_logger
from creative_performance.utils import get_logger as creative_logger


###############################################################
# Logger Tests
###############################################################

def test_revenue_logger():

    logger = revenue_logger("logs/revenue.log")

    assert isinstance(logger, logging.Logger)


def test_anomaly_logger():

    logger = anomaly_logger("logs/anomaly.log")

    assert isinstance(logger, logging.Logger)


def test_segmentation_logger():

    logger = segmentation_logger("logs/segment.log")

    assert isinstance(logger, logging.Logger)


def test_creative_logger():

    logger = creative_logger("logs/creative.log")

    assert isinstance(logger, logging.Logger)


###############################################################
# Logger Name
###############################################################

def test_logger_name():

    logger = revenue_logger("logs/test.log")

    assert logger.name is not None


###############################################################
# Log File Creation
###############################################################

def test_log_file_creation():

    temp = tempfile.NamedTemporaryFile(
        suffix=".log",
        delete=False
    )

    logger = revenue_logger(temp.name)

    logger.info("Testing logger")

    assert Path(temp.name).exists()


###############################################################
# CSV Read Test
###############################################################

def test_csv_creation(sample_dataframe):

    temp = tempfile.NamedTemporaryFile(
        suffix=".csv",
        delete=False
    )

    sample_dataframe.to_csv(
        temp.name,
        index=False
    )

    df = pd.read_csv(temp.name)

    assert len(df) == len(sample_dataframe)


###############################################################
# Excel Read Test
###############################################################

def test_excel_creation(sample_dataframe):

    temp = tempfile.NamedTemporaryFile(
        suffix=".xlsx",
        delete=False
    )

    sample_dataframe.to_excel(
        temp.name,
        index=False
    )

    df = pd.read_excel(temp.name)

    assert len(df) == len(sample_dataframe)


###############################################################
# Directory Creation
###############################################################

def test_directory_creation():

    path = Path("temp_test_directory")

    path.mkdir(exist_ok=True)

    assert path.exists()

    path.rmdir()


###############################################################
# Temporary File Exists
###############################################################

def test_temp_file():

    temp = tempfile.NamedTemporaryFile(
        delete=False
    )

    assert Path(temp.name).exists()


###############################################################
# DataFrame Type
###############################################################

def test_dataframe(sample_dataframe):

    assert isinstance(
        sample_dataframe,
        pd.DataFrame
    )


###############################################################
# DataFrame Shape
###############################################################

def test_dataframe_shape(sample_dataframe):

    assert sample_dataframe.shape[0] > 0

    assert sample_dataframe.shape[1] > 0


###############################################################
# Duplicate Detection
###############################################################

def test_duplicates(sample_dataframe):

    duplicated = pd.concat(

        [sample_dataframe, sample_dataframe],

        ignore_index=True

    )

    assert duplicated.duplicated().sum() > 0


###############################################################
# Numeric Columns
###############################################################

def test_numeric_columns(sample_dataframe):

    numeric = sample_dataframe.select_dtypes(

        include="number"

    )

    assert len(numeric.columns) > 0


###############################################################
# String Columns
###############################################################

def test_categorical_columns(sample_dataframe):

    categorical = sample_dataframe.select_dtypes(

        include="object"

    )

    assert len(categorical.columns) > 0


###############################################################
# Missing Values
###############################################################

def test_missing_values(sample_dataframe):

    assert sample_dataframe.isnull().sum().sum() == 0


###############################################################
# Path Object
###############################################################

def test_path_object():

    path = Path("README.md")

    assert isinstance(path, Path)


###############################################################
# Exception Test
###############################################################

def test_invalid_file():

    with pytest.raises(FileNotFoundError):

        pd.read_csv("does_not_exist.csv")
