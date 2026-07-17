import pandas as pd
import numpy as np
import joblib

import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)

from utils.feature_engineering import create_features

model = joblib.load(
    "pickle/roas_model.pkl"
)

features = joblib.load(
    "pickle/roas_features.pkl"
)

df = pd.read_csv(
    "data/processed/merged_ads_data.csv"
)

df = df[df["roas"].notnull()]

platforms = df["platform"]

df["date"] = pd.to_datetime(df["date"])

df = create_features(df)

drop_columns = [
    "roas",
    "revenue",
    "date",
    "campaign_name",
    "campaign_id",
    "revenue_is_proxy"
]

X = df.drop(
    columns=drop_columns,
    errors="ignore"
)

X = pd.get_dummies(X)

for col in features:
    if col not in X.columns:
        X[col] = 0

X = X[features]

predictions = np.expm1(
    model.predict(X)
)

df["predicted_roas"] = predictions

df["absolute_error"] = (
    df["roas"] -
    df["predicted_roas"]
).abs()

df["platform_original"] = platforms.values

print("\nPlatform Error Analysis\n")

print(
    df.groupby(
        "platform_original"
    )["absolute_error"].agg(
        ["mean", "median", "count"]
    )
)