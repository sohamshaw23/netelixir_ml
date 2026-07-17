import joblib
import pandas as pd
import numpy as np

from utils.feature_engineering import create_features

model = joblib.load(
    "pickle/revenue_model.pkl"
)

feature_columns = joblib.load(
    "pickle/revenue_features.pkl"
)


def predict_revenue(input_data):

    df = pd.DataFrame([input_data])

    df["date"] = pd.to_datetime(df["date"])

    df = create_features(df)

    drop_columns = [
        "revenue",
        "roas",
        "revenue_is_proxy",
        "date",
        "campaign_name",
        "campaign_id"
    ]

    df.drop(
        columns=drop_columns,
        errors="ignore",
        inplace=True
    )

    df = pd.get_dummies(df)

    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_columns]

    prediction = np.expm1(
        model.predict(df)
    )[0]

    return float(prediction)