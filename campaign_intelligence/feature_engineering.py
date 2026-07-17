"""
campaign_intelligence/feature_engineering.py

Feature engineering and lag calculations for Campaign Intelligence regression models.
"""

import re
import numpy as np
import pandas as pd


def extract_campaign_type(name):
    """
    Extract clean campaign type from campaign name.
    """
    base = re.sub(r"_Campaign_\d+$", "", str(name))
    base = base.replace("_Adv_Plus", "").replace(" Adv_Plus", "")
    for mod in ["_NTM", "_TM", "_Brand", "_DPA"]:
        base = base.replace(mod, "")
    return base.strip()


def create_features(df):
    """
    Compute date features, brand campaign flag, and simple calculated metrics.
    """
    df = df.copy()

    # Date Features
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.dayofweek
    df["quarter"] = df["date"].dt.quarter
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)

    # Marketing Features
    df["ctr_calc"] = df["clicks"] / (df["impressions"] + 1)
    df["conversion_rate"] = df["conversions"] / (df["clicks"] + 1)
    df["cpc_calc"] = df["spend"] / (df["clicks"] + 1)
    df["cpm_calc"] = df["spend"] * 1000 / (df["impressions"] + 1)

    # Brand Campaign Feature
    df["is_brand_campaign"] = (
        df["campaign_name"].str.contains("Brand", case=False, na=False)
        | (
            df["campaign_name"].str.contains("TM", case=False, na=False)
            & ~df["campaign_name"].str.contains("NTM", case=False, na=False)
        )
    ).astype(int)

    # One Hot Encode platform (retaining dummy compatibility)
    df = pd.get_dummies(df, columns=["platform"], drop_first=True)

    return df


def compute_lag_features(history_df, platform, request_date, campaign_name=None):
    """
    Compute rolling averages and lag features from historical data.
    """
    mask = history_df["platform"] == platform

    if campaign_name is not None:
        mask &= history_df["campaign_name"] == campaign_name

    hist_raw = history_df[
        mask & (history_df["date"] < request_date)
    ].sort_values("date")

    hist = (
        hist_raw.groupby("date")
        .agg(
            revenue=("revenue", "sum"),
            spend=("spend", "sum")
        )
        .reset_index()
    )

    revenue = hist["revenue"]
    spend = hist["spend"]

    features = {
        "revenue_lag_1": revenue.iloc[-1] if len(revenue) >= 1 else 0,
        "revenue_lag_7": revenue.iloc[-7] if len(revenue) >= 7 else 0,
        "revenue_lag_14": revenue.iloc[-14] if len(revenue) >= 14 else 0,
        "revenue_lag_30": revenue.iloc[-30] if len(revenue) >= 30 else 0,
        "revenue_roll_mean_7": revenue.tail(7).mean() if len(revenue) else 0,
        "revenue_roll_mean_14": revenue.tail(14).mean() if len(revenue) else 0,
        "revenue_roll_mean_30": revenue.tail(30).mean() if len(revenue) else 0,
        "revenue_roll_std_7": revenue.tail(7).std() if len(revenue) > 1 else 0,
        "revenue_roll_std_14": revenue.tail(14).std() if len(revenue) > 1 else 0,
        "revenue_roll_std_30": revenue.tail(30).std() if len(revenue) > 1 else 0,
        "spend_lag_1": spend.iloc[-1] if len(spend) >= 1 else 0,
        "spend_lag_7": spend.iloc[-7] if len(spend) >= 7 else 0,
        "spend_roll_mean_7": spend.tail(7).mean() if len(spend) else 0,
    }

    features["revenue_growth_7"] = (
        (features["revenue_lag_1"] - features["revenue_lag_7"])
        / (features["revenue_lag_7"] + 1)
    )

    features["spend_growth_7"] = (
        (features["spend_lag_1"] - features["spend_lag_7"])
        / (features["spend_lag_7"] + 1)
    )

    features["campaign_count"] = hist_raw["campaign_name"].nunique()

    return features
