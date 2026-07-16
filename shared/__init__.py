"""
shared
======

Shared utilities for the Marketing Intelligence Platform.

Modules
-------
• constants
• data_loader
• preprocess
• feature_engineering
• metrics
• visualization
• validation
• logger
• helper

Author : Team AIgnition
Version : 1.0.0
"""

############################################################
# Constants
############################################################

from .constants import *

############################################################
# Data Loader
############################################################

from .data_loader import (
    DataLoader,
    load_dataframe,
    save_dataframe,
    dataset_summary,
    split_dataset
)

############################################################
# Preprocessing
############################################################

from .preprocess import (
    Preprocessor,
    fit_transform,
    transform
)

############################################################
# Feature Engineering
############################################################

from .feature_engineering import (
    FeatureEngineer,
    create_features
)

############################################################
# Metrics
############################################################

from .metrics import (
    Metrics,
    classification_metrics,
    regression_metrics,
    clustering_metrics,
    anomaly_metrics
)

############################################################
# Visualization
############################################################

from .visualization import (
    Visualizer,
    get_visualizer
)

############################################################
# Validation
############################################################

from .validation import (
    DataValidator,
    validate_file,
    validate_dataset,
    validate_columns,
    validate_all
)

############################################################
# Logger
############################################################

from .logger import (
    get_logger,
    training_logger,
    inference_logger,
    api_logger,
    error_logger
)

############################################################
# Helper
############################################################

from .helper import (
    ensure_directory,
    save_json,
    load_json,
    save_object,
    load_object,
    generate_uuid,
    current_timestamp,
    allowed_file,
    readable_size,
    timer,
    Timer,
    merge_dicts,
    safe_float,
    safe_int,
    percentage
)

############################################################

__version__ = "1.0.0"

############################################################

__all__ = [

    # Data Loader
    "DataLoader",
    "load_dataframe",
    "save_dataframe",
    "dataset_summary",
    "split_dataset",

    # Preprocessing
    "Preprocessor",
    "fit_transform",
    "transform",

    # Feature Engineering
    "FeatureEngineer",
    "create_features",

    # Metrics
    "Metrics",
    "classification_metrics",
    "regression_metrics",
    "clustering_metrics",
    "anomaly_metrics",

    # Visualization
    "Visualizer",
    "get_visualizer",

    # Validation
    "DataValidator",
    "validate_file",
    "validate_dataset",
    "validate_columns",
    "validate_all",

    # Logger
    "get_logger",
    "training_logger",
    "inference_logger",
    "api_logger",
    "error_logger",

    # Helpers
    "ensure_directory",
    "save_json",
    "load_json",
    "save_object",
    "load_object",
    "generate_uuid",
    "current_timestamp",
    "allowed_file",
    "readable_size",
    "timer",
    "Timer",
    "merge_dicts",
    "safe_float",
    "safe_int",
    "percentage"
]

