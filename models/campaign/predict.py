import joblib
import pandas as pd
import numpy as np

from utils.feature_engineering import create_features

# ---------------------------------------------------
# Load Model
# ---------------------------------------------------

model = joblib.load(
    "pickle/campaign_model.pkl"
)

feature_columns = joblib.load(
    "pickle/campaign_features.pkl"
)


def predict_campaign(input_data):

    df = pd.DataFrame([input_data])

    # ----------------------------------------
    # Date conversion
    # ----------------------------------------

    df["date"] = pd.to_datetime(df["date"])

    # ----------------------------------------
    # Feature Engineering
    # ----------------------------------------

    df = create_features(df)

    # ----------------------------------------
    # Lag features placeholders
    # Required because train model expects them
    # These should later come from historical DB
    # ----------------------------------------

    lag_columns = [
        "revenue_lag_1",
        "revenue_lag_7",
        "revenue_roll_mean_7",
        "revenue_roll_std_7",
        "revenue_roll_std_14",
        "spend_lag_1",
        "spend_roll_mean_7"
    ]

    for col in lag_columns:
        if col not in df.columns:
            df[col] = 0

    # ----------------------------------------
    # Remove unused columns
    # ----------------------------------------

    drop_columns = [
        "revenue",
        "roas",
        "revenue_is_proxy",
        "date",
        "campaign_id"
    ]

    df.drop(
        columns=drop_columns,
        errors="ignore",
        inplace=True
    )

    # ----------------------------------------
    # One Hot Encoding
    # ----------------------------------------

    df = pd.get_dummies(df)

    # ----------------------------------------
    # Add Missing Columns
    # ----------------------------------------

    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    # ----------------------------------------
    # Correct order
    # ----------------------------------------

    df = df[feature_columns]

    prediction = np.expm1(
        model.predict(df)
    )[0]

    return {
        "predicted_campaign_revenue":
            round(float(prediction), 2),

        "confidence":
            "High" if prediction > 500
            else "Medium" if prediction > 100
            else "Low"
    }


# ---------------------------------------------------
# Example Run
# ---------------------------------------------------

if __name__ == "__main__":

    sample = {
        "campaign_name": "Search_TM_Campaign_02",
        "date": "2026-07-15",
        "clicks": 120,
        "impressions": 15000,
        "conversions": 15,
        "spend": 450,
        "budget": 500,
        "platform": "google"
    }

    result = predict_campaign(sample)

    print(result)