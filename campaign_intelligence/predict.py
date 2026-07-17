"""
campaign_intelligence/predict.py

Prediction module for Campaign Intelligence models.
"""

import numpy as np
import pandas as pd
import joblib

from .config import MODEL_DIR, DATA_PATH
from .feature_engineering import (
    create_features,
    compute_lag_features,
    extract_campaign_type
)


class CampaignIntelligencePredictor:
    """
    Predictor coordinating the loading of the 4 LightGBM models and generating forecasts.
    """

    def __init__(self):
        # Lazy load data on first time-series query, but init models
        self.revenue_model = joblib.load(MODEL_DIR / "revenue_model.pkl")
        self.revenue_features = joblib.load(MODEL_DIR / "revenue_features.pkl")

        self.roas_model = joblib.load(MODEL_DIR / "roas_model.pkl")
        self.roas_features = joblib.load(MODEL_DIR / "roas_features.pkl")

        self.campaign_model = joblib.load(MODEL_DIR / "campaign_model.pkl")
        self.campaign_features = joblib.load(MODEL_DIR / "campaign_features.pkl")

        self.channel_model = joblib.load(MODEL_DIR / "channel_model.pkl")
        self.channel_features = joblib.load(MODEL_DIR / "channel_features.pkl")

        self._history_df = None

    @property
    def history_df(self):
        """
        Lazy load historical ads data for time-series features.
        """
        if self._history_df is None:
            if DATA_PATH.exists():
                df = pd.read_csv(DATA_PATH)
                df["date"] = pd.to_datetime(df["date"])
                self._history_df = df
            else:
                # Fallback to empty df with columns to prevent crash
                self._history_df = pd.DataFrame(
                    columns=[
                        "platform",
                        "campaign_name",
                        "date",
                        "revenue",
                        "spend",
                        "clicks",
                        "impressions",
                        "conversions"
                    ]
                )
        return self._history_df

    def prepare_static_input(self, data, feature_columns):
        """
        Preprocess input data for static models (Revenue & ROAS).
        """
        df = pd.DataFrame([data])
        df["date"] = pd.to_datetime(df["date"])
        df = create_features(df)

        drop_cols = [
            "revenue",
            "roas",
            "revenue_is_proxy",
            "campaign_id",
            "campaign_name",
            "date"
        ]
        df.drop(columns=drop_cols, errors="ignore", inplace=True)
        df = pd.get_dummies(df)

        # Pad missing columns with 0
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0

        return df[feature_columns]

    def prepare_timeseries_input(self, data, feature_columns, campaign=False):
        """
        Preprocess input data and calculate rolling lag features for time series models.
        """
        request_date = pd.to_datetime(data["date"])

        # Calculate lag features from historical data
        lag_features = compute_lag_features(
            history_df=self.history_df,
            platform=data["platform"],
            request_date=request_date,
            campaign_name=data.get("campaign_name") if campaign else None
        )

        row = dict(data)
        row.update(lag_features)
        df = pd.DataFrame([row])

        if "campaign_name" in df.columns:
            df["campaign_type"] = df["campaign_name"].apply(extract_campaign_type)
            df["is_brand_campaign"] = (
                df["campaign_name"].str.contains("Brand", case=False, na=False)
                | (
                    df["campaign_name"].str.contains("TM", case=False, na=False)
                    & ~df["campaign_name"].str.contains("NTM", case=False, na=False)
                )
            ).astype(int)

        df["date"] = request_date
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["quarter"] = df["date"].dt.quarter
        df["day_of_week"] = df["date"].dt.dayofweek
        df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)

        if "impressions" in df.columns:
            df["ctr_calc"] = df["clicks"] / (df["impressions"] + 1)
            df["cpm_calc"] = df["spend"] * 1000 / (df["impressions"] + 1)

        if "clicks" in df.columns:
            df["conversion_rate"] = df.get("conversions", 0) / (df["clicks"] + 1)
            df["cpc_calc"] = df["spend"] / (df["clicks"] + 1)

        drop_cols = [
            "revenue",
            "roas",
            "revenue_is_proxy",
            "campaign_id",
            "campaign_name",
            "date"
        ]
        df.drop(columns=drop_cols, errors="ignore", inplace=True)
        df = pd.get_dummies(df)

        # Pad missing columns with 0
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0

        return df[feature_columns]

    def predict_revenue(self, data):
        """
        Predict total revenue.
        """
        df = self.prepare_static_input(data, self.revenue_features)
        prediction = np.expm1(self.revenue_model.predict(df))[0]
        return round(float(prediction), 2)

    def predict_roas(self, data):
        """
        Predict return on ad spend.
        """
        df = self.prepare_static_input(data, self.roas_features)
        prediction = np.expm1(self.roas_model.predict(df))[0]
        return round(float(prediction), 2)

    def predict_campaign(self, data):
        """
        Predict campaign performance.
        """
        df = self.prepare_timeseries_input(data, self.campaign_features, campaign=True)
        prediction = np.expm1(self.campaign_model.predict(df))[0]
        rec = "Increase Budget" if prediction > 500 else "Maintain Budget"
        return round(float(prediction), 2), rec

    def predict_channel(self, data):
        """
        Predict channel performance.
        """
        df = self.prepare_timeseries_input(data, self.channel_features, campaign=False)
        prediction = np.expm1(self.channel_model.predict(df))[0]
        return round(float(prediction), 2)
