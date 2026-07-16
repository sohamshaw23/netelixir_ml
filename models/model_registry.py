"""
models/model_registry.py - Central Model Registry
===================================================
Marketing Intelligence AI Platform

Provides a single, lazy-loading registry for all trained model artefacts.
Each model is loaded from disk on first access and then cached in memory
so subsequent calls never hit disk again.

Usage
-----
    from models.model_registry import ModelRegistry

    registry = ModelRegistry()
    xgb   = registry.xgboost          # loads xgboost.pkl on first call
    lgbm  = registry.lightgbm         # loads lightgbm.pkl on first call
    shap  = registry.shap_explainer
    iso   = registry.isolation_forest
    km    = registry.kmeans
    cb    = registry.catboost          # loaded via CatBoost native API
    scaler        = registry.scaler
    encoder       = registry.encoder
    imputer       = registry.imputer
    feature_cols  = registry.feature_columns
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import joblib

from shared.constants import (
    CATBOOST_MODEL,
    ENCODER_PATH,
    FEATURE_COLUMNS_PATH,
    IMPUTER_PATH,
    ISOLATION_FOREST_MODEL,
    KMEANS_MODEL,
    LIGHTGBM_MODEL,
    SCALER_PATH,
    SHAP_EXPLAINER,
    XGBOOST_MODEL,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Artefact path registry
# ---------------------------------------------------------------------------

ARTEFACT_PATHS: Dict[str, str] = {
    # Revenue Drop Risk
    "xgboost":          XGBOOST_MODEL,
    "lightgbm":         LIGHTGBM_MODEL,
    "shap_explainer":   SHAP_EXPLAINER,
    # Anomaly Detection
    "isolation_forest": ISOLATION_FOREST_MODEL,
    # Customer Segmentation
    "kmeans":           KMEANS_MODEL,
    # Creative Performance (special — CatBoost native format, not pickle)
    "catboost":         CATBOOST_MODEL,
    # Preprocessors
    "scaler":           SCALER_PATH,
    "encoder":          ENCODER_PATH,
    "imputer":          IMPUTER_PATH,
    "feature_columns":  FEATURE_COLUMNS_PATH,
}


class ModelRegistry:
    """
    Lazy-loading, in-memory cache for all trained model artefacts.

    Models are loaded from disk **only on first access** and cached
    for the lifetime of the registry instance.

    Attributes
    ----------
    xgboost          : XGBoost revenue risk model.
    lightgbm         : LightGBM revenue risk model.
    shap_explainer   : SHAP TreeExplainer for revenue risk.
    isolation_forest : Isolation Forest anomaly detection model.
    kmeans           : K-Means customer segmentation model.
    catboost         : CatBoost creative performance model.
    scaler           : Fitted StandardScaler / MinMaxScaler.
    encoder          : Fitted LabelEncoder / OrdinalEncoder.
    imputer          : Fitted SimpleImputer.
    feature_columns  : List of feature column names used during training.

    TODO
    ----
    - Add model version metadata (model version, training date, metrics).
    - Add health check that verifies every artefact file exists and is non-empty.
    - Support loading CatBoost model via catboost.CatBoostRegressor.load_model().
    - Add thread-safety (threading.Lock) for multi-worker Gunicorn deployments.
    - Integrate with an MLflow Model Registry or AWS S3 for remote artefacts.
    """

    def __init__(self) -> None:
        """Initialise an empty cache. No files are read at construction time."""
        self._cache: Dict[str, Any] = {}
        logger.info("ModelRegistry initialised (lazy-loading enabled).")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load(self, key: str) -> Any:
        """
        Load artefact *key* from disk if not already cached.

        Args:
            key: One of the keys defined in :data:`ARTEFACT_PATHS`.

        Returns:
            The loaded model / preprocessor object.

        Raises:
            KeyError:         If *key* is not a registered artefact name.
            FileNotFoundError: If the artefact file does not exist on disk.
            RuntimeError:     If the file is empty (not yet trained).
        """
        if key in self._cache:
            return self._cache[key]

        if key not in ARTEFACT_PATHS:
            raise KeyError(f"Unknown model artefact: '{key}'. Known keys: {list(ARTEFACT_PATHS)}")

        path = ARTEFACT_PATHS[key]

        if not Path(path).exists():
            raise FileNotFoundError(
                f"Model artefact not found: {path}\n"
                f"Run the training pipeline first: python scripts/train_all.py"
            )

        if Path(path).stat().st_size == 0:
            logger.warning(
                "Artefact file '%s' is empty (0 bytes). "
                "The model has not been trained yet. Returning None.",
                path,
            )
            return None  # TODO: raise once training is wired up.

        # CatBoost uses its own native serialisation format (.cbm)
        if key == "catboost":
            obj = self._load_catboost(path)
        else:
            obj = joblib.load(path)

        self._cache[key] = obj
        logger.info("Loaded artefact '%s' from %s.", key, path)
        return obj

    @staticmethod
    def _load_catboost(path: str) -> Any:
        """
        Load a CatBoost model from its native .cbm format.

        TODO: Uncomment when CatBoost models are trained.
        """
        try:
            from catboost import CatBoostRegressor  # noqa: F401
            model = CatBoostRegressor()
            model.load_model(path)
            return model
        except ImportError:
            logger.warning("catboost package not installed. Returning None for catboost model.")
            return None
        except Exception as exc:
            logger.warning("Could not load CatBoost model from %s: %s", path, exc)
            return None

    # ------------------------------------------------------------------
    # Public properties — one per artefact
    # ------------------------------------------------------------------

    @property
    def xgboost(self) -> Optional[Any]:
        """Lazy-load and return the XGBoost revenue risk model."""
        return self._load("xgboost")

    @property
    def lightgbm(self) -> Optional[Any]:
        """Lazy-load and return the LightGBM revenue risk model."""
        return self._load("lightgbm")

    @property
    def shap_explainer(self) -> Optional[Any]:
        """Lazy-load and return the SHAP TreeExplainer."""
        return self._load("shap_explainer")

    @property
    def isolation_forest(self) -> Optional[Any]:
        """Lazy-load and return the Isolation Forest anomaly detection model."""
        return self._load("isolation_forest")

    @property
    def kmeans(self) -> Optional[Any]:
        """Lazy-load and return the K-Means segmentation model."""
        return self._load("kmeans")

    @property
    def catboost(self) -> Optional[Any]:
        """Lazy-load and return the CatBoost creative performance model."""
        return self._load("catboost")

    @property
    def scaler(self) -> Optional[Any]:
        """Lazy-load and return the fitted feature scaler."""
        return self._load("scaler")

    @property
    def encoder(self) -> Optional[Any]:
        """Lazy-load and return the fitted feature encoder."""
        return self._load("encoder")

    @property
    def imputer(self) -> Optional[Any]:
        """Lazy-load and return the fitted imputer."""
        return self._load("imputer")

    @property
    def feature_columns(self) -> Optional[Any]:
        """Lazy-load and return the saved feature column list."""
        return self._load("feature_columns")

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------

    def preload_all(self) -> None:
        """
        Eagerly load all model artefacts into memory.

        Call this at application startup (e.g. in ``create_app()``) to
        ensure the first real API request is not slowed by disk reads.

        TODO: Skip artefacts that are empty (not yet trained).
        """
        logger.info("Pre-loading all model artefacts …")
        for key in ARTEFACT_PATHS:
            try:
                self._load(key)
            except (FileNotFoundError, RuntimeError) as exc:
                logger.warning("Could not preload '%s': %s", key, exc)
        logger.info("Model preloading complete. Cached keys: %s", list(self._cache.keys()))

    def is_loaded(self, key: str) -> bool:
        """Return True if the artefact *key* is currently in the cache."""
        return key in self._cache and self._cache[key] is not None

    def status(self) -> Dict[str, Dict[str, Any]]:
        """
        Return a status dictionary for every registered artefact.

        Returns
        -------
        dict
            ``{ artefact_key: { "path": str, "exists": bool,
                                 "size_bytes": int, "loaded": bool } }``
        """
        report: Dict[str, Dict[str, Any]] = {}
        for key, path in ARTEFACT_PATHS.items():
            p = Path(path)
            report[key] = {
                "path":       path,
                "exists":     p.exists(),
                "size_bytes": p.stat().st_size if p.exists() else 0,
                "loaded":     self.is_loaded(key),
            }
        return report

    def invalidate(self, key: str) -> None:
        """
        Evict a single artefact from the cache so it reloads on next access.

        Args:
            key: Artefact key to evict.
        """
        if key in self._cache:
            del self._cache[key]
            logger.info("Cache invalidated for artefact '%s'.", key)

    def invalidate_all(self) -> None:
        """Clear the entire in-memory cache."""
        self._cache.clear()
        logger.info("All model artefacts evicted from cache.")

    def __repr__(self) -> str:  # pragma: no cover
        cached = [k for k, v in self._cache.items() if v is not None]
        return f"<ModelRegistry cached={cached}>"
