"""
shared/helper.py - General Helper Utilities
============================================
Marketing Intelligence AI Platform

Miscellaneous utility functions (file I/O, JSON helpers, date utilities,
model serialisation) used across the project.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
import pandas as pd

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Model serialisation
# ---------------------------------------------------------------------------


def save_model(model: Any, path: str) -> None:
    """
    Serialise a model to disk using joblib.

    Args:
        model: Any picklable model object.
        path: Destination file path (should end in .pkl).

    TODO: Add versioning and metadata alongside the model file.
    """
    os.makedirs(Path(path).parent, exist_ok=True)
    joblib.dump(model, path)
    logger.info("Model saved to %s", path)


def load_model(path: str) -> Any:
    """
    Load a serialised model from disk.

    Args:
        path: Path to the .pkl file.

    Returns:
        Loaded model object.

    Raises:
        FileNotFoundError: If the model file does not exist.
    """
    if not Path(path).exists():
        logger.error("Model file not found: %s", path)
        raise FileNotFoundError(f"Model not found: {path}")
    model = joblib.load(path)
    logger.info("Model loaded from %s", path)
    return model


# ---------------------------------------------------------------------------
# DataFrame utilities
# ---------------------------------------------------------------------------


def dataframe_to_records(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert a DataFrame to a list of dicts for JSON serialisation."""
    return df.to_dict(orient="records")


def records_to_dataframe(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert a list of dicts (e.g., from a JSON payload) to a DataFrame."""
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# JSON utilities
# ---------------------------------------------------------------------------


def save_json(data: Dict[str, Any], path: str) -> None:
    """Save a dictionary as a JSON file."""
    os.makedirs(Path(path).parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    logger.info("JSON saved to %s", path)


def load_json(path: str) -> Dict[str, Any]:
    """Load a JSON file as a dictionary."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Date utilities
# ---------------------------------------------------------------------------


def today_str(fmt: str = "%Y-%m-%d") -> str:
    """Return today's date as a formatted string."""
    return datetime.now().strftime(fmt)


def timestamp_str(fmt: str = "%Y%m%d_%H%M%S") -> str:
    """Return current timestamp as a formatted string (useful for filenames)."""
    return datetime.now().strftime(fmt)
