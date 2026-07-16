"""
models/model_registry.py

Central Model Registry

Loads all trained models and preprocessing artifacts.

Author : Team AIgnition
Version : 1.0.0
"""

from pathlib import Path

import joblib
# pyrefly: ignore [missing-import]
from catboost import CatBoostClassifier


class ModelRegistry:

    def __init__(self):

        self.base_dir = Path(__file__).resolve().parent

        self.models = {}

        self.preprocessors = {}

    ##########################################################

    def load_xgboost(self):

        path = (

            self.base_dir /

            "revenue_drop_risk" /

            "xgboost.pkl"

        )

        self.models["xgboost"] = joblib.load(path)

        return self.models["xgboost"]

    ##########################################################

    def load_lightgbm(self):

        path = (

            self.base_dir /

            "revenue_drop_risk" /

            "lightgbm.pkl"

        )

        self.models["lightgbm"] = joblib.load(path)

        return self.models["lightgbm"]

    ##########################################################

    def load_isolation_forest(self):

        path = (

            self.base_dir /

            "anomaly_detection" /

            "isolation_forest.pkl"

        )

        self.models["isolation_forest"] = joblib.load(path)

        return self.models["isolation_forest"]

    ##########################################################

    def load_kmeans(self):

        path = (

            self.base_dir /

            "customer_segmentation" /

            "kmeans.pkl"

        )

        self.models["kmeans"] = joblib.load(path)

        return self.models["kmeans"]

    ##########################################################

    def load_catboost(self):

        path = (

            self.base_dir /

            "creative_performance" /

            "catboost.cbm"

        )

        model = CatBoostClassifier()

        model.load_model(path)

        self.models["catboost"] = model

        return model

    ##########################################################

    def load_scaler(self):

        path = (

            self.base_dir /

            "preprocessors" /

            "scaler.pkl"

        )

        self.preprocessors["scaler"] = joblib.load(path)

        return self.preprocessors["scaler"]

    ##########################################################

    def load_encoder(self):

        path = (

            self.base_dir /

            "preprocessors" /

            "encoder.pkl"

        )

        self.preprocessors["encoder"] = joblib.load(path)

        return self.preprocessors["encoder"]

    ##########################################################

    def load_imputer(self):

        path = (

            self.base_dir /

            "preprocessors" /

            "imputer.pkl"

        )

        self.preprocessors["imputer"] = joblib.load(path)

        return self.preprocessors["imputer"]

    ##########################################################

    def load_feature_columns(self):

        path = (

            self.base_dir /

            "preprocessors" /

            "feature_columns.pkl"

        )

        self.preprocessors["feature_columns"] = joblib.load(path)

        return self.preprocessors["feature_columns"]

    ##########################################################

    def load_shap_explainer(self):

        path = (

            self.base_dir /

            "revenue_drop_risk" /

            "shap_explainer.pkl"

        )

        self.models["shap"] = joblib.load(path)

        return self.models["shap"]

    ##########################################################

    def load_all(self):

        self.load_xgboost()

        self.load_lightgbm()

        self.load_isolation_forest()

        self.load_kmeans()

        self.load_catboost()

        self.load_scaler()

        self.load_encoder()

        self.load_imputer()

        self.load_feature_columns()

        self.load_shap_explainer()

        return self.models

    ##########################################################

    def get(self, name):

        if name not in self.models:

            raise ValueError(

                f"{name} model not loaded."

            )

        return self.models[name]


##############################################################

registry = ModelRegistry()

