"""
scripts/generate_features.py - Feature Engineering Pipeline
============================================================
Marketing Intelligence AI Platform

Loads the cleaned dataset, runs the full feature engineering pipeline,
and saves the feature store and preprocessor artefacts.

Usage
-----
    python scripts/generate_features.py
    python scripts/generate_features.py --input data/processed/cleaned_dataset.csv
    python scripts/generate_features.py --output data/features/feature_store.csv
    python scripts/generate_features.py --no-save-preprocessors

Steps
-----
    1. Load cleaned dataset from data/processed/cleaned_dataset.csv.
    2. Run FeatureEngineer.generate_all() — CTR, CPC, ROAS, rolling windows,
       date features, etc.
    3. Fit SharedPreprocessor (imputer, scaler, encoder) on the feature set.
    4. Transform the feature set.
    5. Save feature store to data/features/feature_store.csv.
    6. Save fitted preprocessor artefacts to models/preprocessors/.

TODO:
    - Implement each step once the feature list is defined after EDA.
    - Add feature selection (variance threshold, correlation pruning).
    - Add train/val/test split and save splits to data/processed/.
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------

def load_cleaned(input_path: str) -> "pd.DataFrame":  # type: ignore[name-defined]
    """Load the cleaned dataset. TODO: Implement."""
    import pandas as pd
    from shared.data_loader import DataLoader

    logger.info("Loading cleaned dataset from %s …", input_path)
    # TODO: return DataLoader.load_csv(input_path)
    return pd.DataFrame()


def engineer_features(df: "pd.DataFrame") -> "pd.DataFrame":  # type: ignore[name-defined]
    """Run the full feature engineering pipeline. TODO: Implement."""
    from shared.feature_engineering import FeatureEngineer

    logger.info("Engineering features … TODO: Implement.")
    engineer = FeatureEngineer()
    # TODO: return engineer.generate_all(df)
    return df


def fit_preprocessors(df: "pd.DataFrame") -> "pd.DataFrame":  # type: ignore[name-defined]
    """Fit and transform all shared preprocessors. TODO: Implement."""
    from shared.preprocess import SharedPreprocessor

    logger.info("Fitting preprocessors … TODO: Implement.")
    preprocessor = SharedPreprocessor()
    # TODO: Define numeric_cols and categorical_cols after EDA.
    numeric_cols: list = []
    categorical_cols: list = []
    # TODO: return preprocessor.fit_transform(df, numeric_cols, categorical_cols)
    return df


def save_feature_store(df: "pd.DataFrame", output_path: str) -> None:  # type: ignore[name-defined]
    """Save the feature store CSV. TODO: Implement."""
    import os
    os.makedirs(Path(output_path).parent, exist_ok=True)
    # TODO: df.to_csv(output_path, index=False)
    logger.info("Feature store saved to %s (placeholder). TODO: Implement.", output_path)


def save_preprocessor_artefacts() -> None:
    """Save fitted scaler, encoder, imputer and feature column list. TODO: Implement."""
    logger.info("Saving preprocessor artefacts … TODO: Implement.")
    # TODO: joblib.dump(preprocessor, SCALER_PATH)
    # TODO: joblib.dump(feature_columns, FEATURE_COLUMNS_PATH)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="generate_features.py",
        description="Run the feature engineering pipeline and save the feature store.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/processed/cleaned_dataset.csv",
        metavar="PATH",
        help="Path to cleaned dataset CSV (default: data/processed/cleaned_dataset.csv).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/features/feature_store.csv",
        metavar="PATH",
        help="Output path for the feature store CSV (default: data/features/feature_store.csv).",
    )
    parser.add_argument(
        "--no-save-preprocessors",
        action="store_true",
        default=False,
        help="Skip saving fitted preprocessor artefacts to models/preprocessors/.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger.info("=== Feature engineering pipeline started ===")

    df = load_cleaned(args.input)
    df = engineer_features(df)
    df = fit_preprocessors(df)
    save_feature_store(df, args.output)

    if not args.no_save_preprocessors:
        save_preprocessor_artefacts()

    logger.info("=== Feature engineering complete. Output: %s ===", args.output)


if __name__ == "__main__":
    main()
