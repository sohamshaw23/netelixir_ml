import sys
import os
import pandas as pd
import numpy as np
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

# Load processed data
df = pd.read_csv(
    "data/processed/merged_ads_data.csv"
)
print("\nROAS Statistics")
print(df["roas"].describe())

print("\nROAS Quantiles")
print(
    df["roas"].quantile(
        [0.50, 0.75, 0.90, 0.95, 0.99]
    )
)

df["date"] = pd.to_datetime(df["date"])

# Remove rows with missing ROAS
df = df[df["roas"].notnull()]

print("\nROAS Statistics")
print(df["roas"].describe())

# Feature engineering
df = create_features(df)

drop_columns = [
    "roas",
    "revenue",
    "date",
    "campaign_name",
    "campaign_id",
    "revenue_is_proxy"
]

X = df.drop(columns=drop_columns)

# Log transform target
y = np.log1p(df["roas"])

# One hot encoding
X = pd.get_dummies(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = LGBMRegressor(
    n_estimators=500,
    learning_rate=0.05,
    random_state=42
)

# Train
model.fit(
    X_train,
    y_train
)

# Predict
predictions = np.expm1(
    model.predict(X_test)
)

y_test_original = np.expm1(y_test)

# Metrics
print(
    "\nMAE:",
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

# Save model
joblib.dump(
    model,
    "pickle/roas_model.pkl"
)

joblib.dump(
    X.columns.tolist(),
    "pickle/roas_features.pkl"
)
print("\nROAS Model Saved Successfully.")
importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

print(
    "\nTop Features:\n"
)

print(
    importance_df.sort_values(
        by="importance",
        ascending=False
    ).head(15)
)