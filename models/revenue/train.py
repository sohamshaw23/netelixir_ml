import sys
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from lightgbm import LGBMRegressor

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


df = pd.read_csv(
    "data/processed/merged_ads_data.csv"
)

df["date"] = pd.to_datetime(df["date"])

# Revenue only exists for Google and Bing
df = df[df["revenue"].notnull()]
print("\nRevenue Statistics")
print(df["revenue"].describe())

print("\nAverage Revenue:", df["revenue"].mean())
print("Median Revenue:", df["revenue"].median())
print("Maximum Revenue:", df["revenue"].max())

df = create_features(df)

drop_columns = [
    "revenue",
    "roas",
    "revenue_is_proxy",
    "date",
    "campaign_name",
    "campaign_id"
]
X = df.drop(columns=drop_columns)

import numpy as np

y = np.log1p(df["revenue"])

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

model.fit(X_train, y_train)

predictions = np.expm1(
    model.predict(X_test)
)

y_test_original = np.expm1(y_test)

print(
    "MAE:",
    mean_absolute_error(
        y_test_original,
        predictions
    )
)

print(
    "R2:",
    r2_score(
        y_test_original,
        predictions
    )
)

joblib.dump(
    model,
    "pickle/revenue_model.pkl"
)

joblib.dump(
    X.columns.tolist(),
    "pickle/revenue_features.pkl"
)

print("\nRevenue Model Saved Successfully.")