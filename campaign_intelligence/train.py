"""
campaign_intelligence/train.py

Training pipeline for Campaign Intelligence regression models.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from lightgbm import LGBMRegressor

from .config import MODEL_DIR, DATA_PATH, RANDOM_STATE, TEST_SIZE, MIN_HISTORY_DAYS
from .feature_engineering import create_features, extract_campaign_type


class CampaignIntelligenceTrainer:
    """
    Retrains and updates the LightGBM regression models.
    """

    def __init__(self):
        self.data_path = DATA_PATH
        self.model_dir = MODEL_DIR
        self.model_dir.mkdir(exist_ok=True, parents=True)

    def load_data(self):
        """
        Load processed merged ad data.
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Historical dataset not found at {self.data_path}")
        df = pd.read_csv(self.data_path)
        df["date"] = pd.to_datetime(df["date"])
        return df

    def train_revenue(self, df):
        """
        Train Revenue model.
        """
        print("Training Revenue model...")
        df = df[df["revenue"].notnull()].copy()
        df = create_features(df)

        drop_cols = [
            "revenue", "roas", "revenue_is_proxy", "date",
            "campaign_name", "campaign_id"
        ]
        X = df.drop(columns=drop_cols)
        y = np.log1p(df["revenue"])

        X = pd.get_dummies(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )

        model = LGBMRegressor(n_estimators=500, learning_rate=0.05, random_state=RANDOM_STATE)
        model.fit(X_train, y_train)

        joblib.dump(model, self.model_dir / "revenue_model.pkl")
        joblib.dump(X.columns.tolist(), self.model_dir / "revenue_features.pkl")
        print("Revenue model trained and saved successfully.")

    def train_roas(self, df):
        """
        Train ROAS model.
        """
        print("Training ROAS model...")
        df = df[df["roas"].notnull()].copy()
        df = create_features(df)

        drop_cols = [
            "roas", "revenue", "date", "campaign_name",
            "campaign_id", "revenue_is_proxy"
        ]
        X = df.drop(columns=drop_cols)
        y = np.log1p(df["roas"])

        X = pd.get_dummies(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )

        model = LGBMRegressor(n_estimators=500, learning_rate=0.05, random_state=RANDOM_STATE)
        model.fit(X_train, y_train)

        joblib.dump(model, self.model_dir / "roas_model.pkl")
        joblib.dump(X.columns.tolist(), self.model_dir / "roas_features.pkl")
        print("ROAS model trained and saved successfully.")

    def train_campaign(self, df):
        """
        Train Campaign Time Series model.
        """
        print("Training Campaign model...")
        df = df[df["revenue"].notnull()].copy()

        agg = (
            df.groupby(["platform", "campaign_name", "date"])
            .agg(
                revenue=("revenue", "sum"),
                spend=("spend", "sum"),
                clicks=("clicks", "sum"),
                impressions=("impressions", "sum"),
                conversions=("conversions", "sum"),
                budget=("budget", "sum"),
            )
            .reset_index()
            .sort_values(["platform", "campaign_name", "date"])
        )

        agg["campaign_type"] = agg["campaign_name"].apply(extract_campaign_type)
        agg["is_brand_campaign"] = (
            agg["campaign_name"].str.contains("Brand", case=False, na=False)
            | (
                agg["campaign_name"].str.contains("TM", case=False, na=False)
                & ~agg["campaign_name"].str.contains("NTM", case=False, na=False)
            )
        ).astype(int)

        agg["ctr_calc"] = agg["clicks"] / (agg["impressions"] + 1)
        agg["conversion_rate"] = agg["conversions"] / (agg["clicks"] + 1)
        agg["cpc_calc"] = agg["spend"] / (agg["clicks"] + 1)

        history_len = agg.groupby(["platform", "campaign_name"])["date"].transform("count")
        agg = agg[history_len >= MIN_HISTORY_DAYS].copy()

        group_key = ["platform", "campaign_name"]
        g = agg.groupby(group_key)["revenue"]

        for lag in [1, 7]:
            agg[f"revenue_lag_{lag}"] = g.shift(lag)

        for window in [7, 14]:
            agg[f"revenue_roll_mean_{window}"] = g.shift(1).rolling(window, min_periods=1).mean()
            agg[f"revenue_roll_std_{window}"] = g.shift(1).rolling(window, min_periods=1).std()

        gs = agg.groupby(group_key)["spend"]
        agg["spend_lag_1"] = gs.shift(1)
        agg["spend_roll_mean_7"] = gs.shift(1).rolling(7, min_periods=1).mean()

        agg = agg.dropna(subset=["revenue_lag_1", "revenue_lag_7"])

        agg["year"] = agg["date"].dt.year
        agg["month"] = agg["date"].dt.month
        agg["day_of_week"] = agg["date"].dt.dayofweek
        agg["quarter"] = agg["date"].dt.quarter
        agg["week_of_year"] = agg["date"].dt.isocalendar().week.astype(int)

        agg = pd.get_dummies(agg, columns=["platform", "campaign_type"], drop_first=True)

        drop_columns = ["revenue", "date", "campaign_name"]
        X = agg.drop(columns=drop_columns)
        y = np.log1p(agg["revenue"])

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )

        model = LGBMRegressor(n_estimators=500, learning_rate=0.05, random_state=RANDOM_STATE)
        model.fit(X_train, y_train)

        joblib.dump(model, self.model_dir / "campaign_model.pkl")
        joblib.dump(X.columns.tolist(), self.model_dir / "campaign_features.pkl")
        print("Campaign model trained and saved successfully.")

    def train_channel(self, df):
        """
        Train Channel Time Series model.
        """
        print("Training Channel model...")
        df = df[df["revenue"].notnull()].copy()

        agg = (
            df.groupby(["platform", "date"])
            .agg(
                revenue=("revenue", "sum"),
                spend=("spend", "sum"),
                clicks=("clicks", "sum"),
                impressions=("impressions", "sum"),
                conversions=("conversions", "sum"),
                budget=("budget", "sum"),
            )
            .reset_index()
            .sort_values(["platform", "date"])
        )

        agg["ctr_calc"] = agg["clicks"] / (agg["impressions"] + 1)
        agg["conversion_rate"] = agg["conversions"] / (agg["clicks"] + 1)
        agg["cpc_calc"] = agg["spend"] / (agg["clicks"] + 1)

        group_key = ["platform"]
        g = agg.groupby(group_key)["revenue"]

        for lag in [1, 7]:
            agg[f"revenue_lag_{lag}"] = g.shift(lag)

        for window in [7, 14]:
            agg[f"revenue_roll_mean_{window}"] = g.shift(1).rolling(window, min_periods=1).mean()
            agg[f"revenue_roll_std_{window}"] = g.shift(1).rolling(window, min_periods=1).std()

        gs = agg.groupby(group_key)["spend"]
        agg["spend_lag_1"] = gs.shift(1)
        agg["spend_roll_mean_7"] = gs.shift(1).rolling(7, min_periods=1).mean()

        agg = agg.dropna(subset=["revenue_lag_1", "revenue_lag_7"])

        agg["year"] = agg["date"].dt.year
        agg["month"] = agg["date"].dt.month
        agg["day_of_week"] = agg["date"].dt.dayofweek
        agg["quarter"] = agg["date"].dt.quarter
        agg["week_of_year"] = agg["date"].dt.isocalendar().week.astype(int)

        agg = pd.get_dummies(agg, columns=["platform"], drop_first=True)

        drop_columns = ["revenue", "date"]
        X = agg.drop(columns=drop_columns)
        y = np.log1p(agg["revenue"])

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )

        model = LGBMRegressor(n_estimators=500, learning_rate=0.05, random_state=RANDOM_STATE)
        model.fit(X_train, y_train)

        joblib.dump(model, self.model_dir / "channel_model.pkl")
        joblib.dump(X.columns.tolist(), self.model_dir / "channel_features.pkl")
        print("Channel model trained and saved successfully.")

    def retrain_all(self):
        """
        Retrain all 4 models sequentially.
        """
        df = self.load_data()
        self.train_revenue(df)
        self.train_roas(df)
        self.train_campaign(df)
        self.train_channel(df)
        print("All Campaign Intelligence Models Retrained Successfully.")


if __name__ == "__main__":
    trainer = CampaignIntelligenceTrainer()
    trainer.retrain_all()
