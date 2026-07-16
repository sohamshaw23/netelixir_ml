"""
shared/data_loader.py - Data Loading Utilities
===============================================
Marketing Intelligence AI Platform

Provides functions to load raw, processed, and feature data from the
data/ directory into pandas DataFrames.
"""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

from shared.constants import (
    CLEANED_DATASET,
    FEATURE_STORE,
    MERGED_DATASET,
    RAW_CAMPAIGN_METADATA,
    RAW_GA4,
    RAW_GOOGLE_ADS,
    RAW_META_ADS,
    RAW_MICROSOFT_ADS,
    RAW_SHOPIFY,
    TEST_DATA,
    TRAIN_DATA,
    VALIDATION_DATA,
)

logger = logging.getLogger(__name__)


class DataLoader:
    """
    Centralised data loader for all CSV datasets.

    TODO:
        - Add support for loading from cloud storage (S3, GCS).
        - Add caching layer (e.g., Redis or in-memory LRU cache).
        - Add schema validation after loading each source.
    """

    # ------------------------------------------------------------------
    # Raw data loaders
    # ------------------------------------------------------------------

    @staticmethod
    def load_google_ads(path: str = RAW_GOOGLE_ADS) -> pd.DataFrame:
        """Load Google Ads raw data. TODO: Add dtype enforcement."""
        logger.info("Loading Google Ads data from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    @staticmethod
    def load_meta_ads(path: str = RAW_META_ADS) -> pd.DataFrame:
        """Load Meta Ads raw data. TODO: Add dtype enforcement."""
        logger.info("Loading Meta Ads data from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    @staticmethod
    def load_microsoft_ads(path: str = RAW_MICROSOFT_ADS) -> pd.DataFrame:
        """Load Microsoft Ads raw data. TODO: Add dtype enforcement."""
        logger.info("Loading Microsoft Ads data from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    @staticmethod
    def load_ga4(path: str = RAW_GA4) -> pd.DataFrame:
        """Load GA4 raw data. TODO: Add dtype enforcement."""
        logger.info("Loading GA4 data from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    @staticmethod
    def load_shopify(path: str = RAW_SHOPIFY) -> pd.DataFrame:
        """Load Shopify orders raw data. TODO: Add dtype enforcement."""
        logger.info("Loading Shopify orders data from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    @staticmethod
    def load_campaign_metadata(path: str = RAW_CAMPAIGN_METADATA) -> pd.DataFrame:
        """Load campaign metadata. TODO: Add dtype enforcement."""
        logger.info("Loading campaign metadata from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    # ------------------------------------------------------------------
    # Processed data loaders
    # ------------------------------------------------------------------

    @staticmethod
    def load_merged(path: str = MERGED_DATASET) -> pd.DataFrame:
        """Load the merged (but unclean) dataset."""
        logger.info("Loading merged dataset from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    @staticmethod
    def load_cleaned(path: str = CLEANED_DATASET) -> pd.DataFrame:
        """Load the cleaned dataset."""
        logger.info("Loading cleaned dataset from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    @staticmethod
    def load_train(path: str = TRAIN_DATA) -> pd.DataFrame:
        """Load the training split."""
        logger.info("Loading training data from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    @staticmethod
    def load_validation(path: str = VALIDATION_DATA) -> pd.DataFrame:
        """Load the validation split."""
        logger.info("Loading validation data from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    @staticmethod
    def load_test(path: str = TEST_DATA) -> pd.DataFrame:
        """Load the test split."""
        logger.info("Loading test data from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    # ------------------------------------------------------------------
    # Feature data loaders
    # ------------------------------------------------------------------

    @staticmethod
    def load_feature_store(path: str = FEATURE_STORE) -> pd.DataFrame:
        """Load the feature store CSV."""
        logger.info("Loading feature store from %s", path)
        # TODO: Implement loading logic.
        return pd.DataFrame()

    # ------------------------------------------------------------------
    # Generic loader
    # ------------------------------------------------------------------

    @staticmethod
    def load_csv(path: str, **kwargs) -> pd.DataFrame:
        """
        Generic CSV loader with error handling.

        Args:
            path: Absolute or relative path to CSV file.
            **kwargs: Additional kwargs forwarded to :func:`pandas.read_csv`.

        Returns:
            pd.DataFrame: Loaded data.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        file = Path(path)
        if not file.exists():
            logger.error("File not found: %s", path)
            raise FileNotFoundError(f"Data file not found: {path}")
        df = pd.read_csv(file, **kwargs)
        logger.info("Loaded %d rows × %d columns from %s", *df.shape, path)
        return df
