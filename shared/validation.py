"""
shared/validation.py - Input Validation Utilities
==================================================
Marketing Intelligence AI Platform

Request payload validation helpers used by the API Blueprints.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when a validation check fails."""


def validate_required_keys(payload: Dict[str, Any], required_keys: List[str]) -> None:
    """
    Validate that all required keys are present in *payload*.

    Args:
        payload: Dictionary to validate.
        required_keys: Keys that must be present.

    Raises:
        ValidationError: If any required key is missing.

    TODO: Extend with type-checking per key.
    """
    missing = [k for k in required_keys if k not in payload]
    if missing:
        raise ValidationError(f"Missing required fields: {missing}")


def validate_non_empty(df: pd.DataFrame, context: str = "") -> None:
    """
    Ensure *df* is not empty.

    Args:
        df: DataFrame to check.
        context: Contextual label for error messages.

    Raises:
        ValidationError: If the DataFrame has no rows.
    """
    if df.empty:
        raise ValidationError(f"Input DataFrame is empty. Context: {context}")


def validate_required_columns(df: pd.DataFrame, required_cols: List[str], context: str = "") -> None:
    """
    Validate that *df* contains all *required_cols*.

    Args:
        df: DataFrame to validate.
        required_cols: Columns that must be present.
        context: Contextual label for error messages.

    Raises:
        ValidationError: If any required column is missing.

    TODO: Add dtype validation per column.
    """
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValidationError(f"Missing required columns {missing}. Context: {context}")


def validate_no_nulls(df: pd.DataFrame, cols: List[str]) -> None:
    """
    Validate that *cols* in *df* contain no null values.

    Args:
        df: DataFrame to validate.
        cols: Columns to check.

    Raises:
        ValidationError: If nulls are found.

    TODO: Return per-column null counts in the error message.
    """
    for col in cols:
        if df[col].isnull().any():
            raise ValidationError(f"Null values found in column '{col}'.")


def validate_positive_values(df: pd.DataFrame, cols: List[str]) -> None:
    """
    Validate that numeric *cols* contain only positive values.

    Args:
        df: DataFrame to validate.
        cols: Columns to check.

    Raises:
        ValidationError: If non-positive values are found.

    TODO: Allow configurable lower bound.
    """
    for col in cols:
        if (df[col] <= 0).any():
            raise ValidationError(f"Non-positive values found in column '{col}'.")
