import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import sys
import os
import pandas as pd
import joblib
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

thresholds = [1, 5, 10]

for threshold in thresholds:

    print("\n" + "="*50)
    print(f"Testing Threshold: ${threshold}")
    print("="*50)

    df = pd.read_csv(
        "data/processed/merged_ads_data.csv"
    )

    # Create ROAS dynamically
    df["roas_test"] = np.nan

    valid = df["spend"] >= threshold

    df.loc[valid, "roas_test"] = (
        df.loc[valid, "revenue"] /
        df.loc[valid, "spend"]
    )

    df = df[df["roas_test"].notnull()]

    print("Rows Used:", len(df))

    df["date"] = pd.to_datetime(df["date"])

    df = create_features(df)

    drop_columns = [
        "roas",
        "roas_test",
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

    y = np.log1p(df["roas_test"])

    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = LGBMRegressor(
        n_estimators=500,
        learning_rate=0.05,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = np.expm1(
        model.predict(X_test)
    )

    y_true = np.expm1(y_test)

    mae = mean_absolute_error(
        y_true,
        predictions
    )

    r2 = r2_score(
        y_true,
        predictions
    )

    print("MAE:", mae)
    print("R2:", r2)