import sys
import os
import numpy as np
import pandas as pd
import joblib

from sklearn.metrics import mean_absolute_error, r2_score
from lightgbm import LGBMRegressor

# ==========================================================
# Add project root to path
# ==========================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)

# ==========================================================
# Load Data
# ==========================================================

df = pd.read_csv(
    "data/processed/merged_ads_data.csv"
)

df["date"] = pd.to_datetime(df["date"])

# ==========================================================
# Aggregate to Platform-Day Level
# ==========================================================

agg = (
    df.groupby(
        ["platform", "date"]
    )
    .agg(
        revenue=("revenue", "sum"),
        spend=("spend", "sum"),
        clicks=("clicks", "sum"),
        impressions=("impressions", "sum"),
        conversions=("conversions", "sum"),
        budget=("budget", "sum"),
        campaign_count=("campaign_name", "nunique")
    )
    .reset_index()
)

agg = agg.sort_values(
    ["platform", "date"]
)

# ==========================================================
# Derived Marketing Features
# ==========================================================

agg["ctr_calc"] = (
    agg["clicks"] /
    (agg["impressions"] + 1)
)

agg["conversion_rate"] = (
    agg["conversions"] /
    (agg["clicks"] + 1)
)

agg["cpc_calc"] = (
    agg["spend"] /
    (agg["clicks"] + 1)
)

agg["roas"] = (
    agg["revenue"] /
    agg["spend"].clip(lower=1)
)

# ==========================================================
# Revenue Lag Features
# ==========================================================

revenue_group = agg.groupby(
    "platform"
)["revenue"]

for lag in [1, 7, 14, 30]:
    agg[f"revenue_lag_{lag}"] = (
        revenue_group.shift(lag)
    )

# ==========================================================
# Revenue Rolling Features
# ==========================================================

for window in [7, 14, 30]:

    agg[f"revenue_roll_mean_{window}"] = (
        revenue_group
        .shift(1)
        .rolling(
            window,
            min_periods=1
        )
        .mean()
    )

    agg[f"revenue_roll_std_{window}"] = (
        revenue_group
        .shift(1)
        .rolling(
            window,
            min_periods=1
        )
        .std()
    )

# ==========================================================
# Spend Lag Features
# ==========================================================

spend_group = agg.groupby(
    "platform"
)["spend"]

for lag in [1, 7]:
    agg[f"spend_lag_{lag}"] = (
        spend_group.shift(lag)
    )

agg["spend_roll_mean_7"] = (
    spend_group
    .shift(1)
    .rolling(
        7,
        min_periods=1
    )
    .mean()
)

# ==========================================================
# Growth Features
# ==========================================================

agg["revenue_growth_7"] = (
    agg["revenue_lag_1"] -
    agg["revenue_lag_7"]
) / (
    agg["revenue_lag_7"] + 1
)

agg["spend_growth_7"] = (
    agg["spend_lag_1"] -
    agg["spend_lag_7"]
) / (
    agg["spend_lag_7"] + 1
)

# ==========================================================
# Date Features
# ==========================================================

agg["year"] = agg["date"].dt.year
agg["month"] = agg["date"].dt.month
agg["quarter"] = agg["date"].dt.quarter
agg["day_of_week"] = agg["date"].dt.dayofweek
agg["week_of_year"] = (
    agg["date"]
    .dt
    .isocalendar()
    .week
    .astype(int)
)

# ==========================================================
# Remove rows without sufficient history
# ==========================================================

agg = agg.dropna(
    subset=[
        "revenue_lag_30"
    ]
)

# ==========================================================
# Revenue Statistics
# ==========================================================

print("\nAggregated Channel-Day Revenue Statistics\n")

print(
    agg["revenue"].describe()
)

print(
    "\nAverage Revenue:",
    agg["revenue"].mean()
)

print(
    "Median Revenue:",
    agg["revenue"].median()
)

print(
    "Maximum Revenue:",
    agg["revenue"].max()
)

# ==========================================================
# Save labels before encoding
# ==========================================================

platform_labels = agg["platform"].copy()

# ==========================================================
# Encode Platform
# ==========================================================

agg = pd.get_dummies(
    agg,
    columns=["platform"],
    drop_first=True
)

# ==========================================================
# Features and Target
# ==========================================================

drop_columns = [
    "revenue",
    "date",
    "roas"
]

X = agg.drop(
    columns=drop_columns
)

y = np.log1p(
    agg["revenue"]
)

# ==========================================================
# Chronological Split
# ==========================================================

split_date = agg["date"].quantile(
    0.80
)

train_mask = (
    agg["date"] <= split_date
)

test_mask = (
    agg["date"] > split_date
)

X_train = X[train_mask]
X_test = X[test_mask]

y_train = y[train_mask]
y_test = y[test_mask]

print(
    "\nTrain Rows:",
    len(X_train)
)

print(
    "Test Rows:",
    len(X_test)
)

# ==========================================================
# Train Model
# ==========================================================

model = LGBMRegressor(
    n_estimators=500,
    learning_rate=0.05,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# ==========================================================
# Predictions
# ==========================================================

predictions = np.expm1(
    model.predict(X_test)
)

actual = np.expm1(
    y_test
)

mae = mean_absolute_error(
    actual,
    predictions
)

r2 = r2_score(
    actual,
    predictions
)

print(
    "\nMAE:",
    mae
)

print(
    "R2:",
    r2
)

# ==========================================================
# Per Platform Diagnostics
# ==========================================================

test_df = agg.loc[
    test_mask
].copy()

test_df["platform"] = (
    platform_labels.loc[
        test_mask
    ].values
)

test_df["actual"] = actual
test_df["predicted"] = predictions

test_df["abs_error"] = (
    test_df["actual"] -
    test_df["predicted"]
).abs()

print(
    "\nPer Platform Performance\n"
)

print(
    test_df.groupby(
        "platform"
    ).agg(
        mean_error=("abs_error", "mean"),
        median_error=("abs_error", "median"),
        mean_actual=("actual", "mean"),
        median_actual=("actual", "median"),
        count=("abs_error", "count")
    )
)

# ==========================================================
# Feature Importance
# ==========================================================

importance_df = pd.DataFrame(
    {
        "feature": X.columns,
        "importance": model.feature_importances_
    }
)

print(
    "\nTop Features\n"
)

print(
    importance_df.sort_values(
        by="importance",
        ascending=False
    ).head(20)
)

# ==========================================================
# Save Model
# ==========================================================

joblib.dump(
    model,
    "pickle/channel_model.pkl"
)

joblib.dump(
    X.columns.tolist(),
    "pickle/channel_features.pkl"
)

print(
    "\nChannel Model Saved Successfully."
)