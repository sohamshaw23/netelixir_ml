import sys
import os
import re
import numpy as np
import pandas as pd
import joblib

from sklearn.metrics import mean_absolute_error, r2_score
from lightgbm import LGBMRegressor

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
)

MIN_HISTORY_DAYS = 14  # need enough history per campaign to compute lag/rolling
                        # features meaningfully; shorter series get excluded
                        # and documented as a limitation

def extract_campaign_type(name):
    base = re.sub(r"_Campaign_\d+$", "", str(name))
    base = base.replace("_Adv_Plus", "").replace(" Adv_Plus", "")
    for mod in ["_NTM", "_TM", "_Brand", "_DPA"]:
        base = base.replace(mod, "")
    return base.strip()

df = pd.read_csv("data/processed/merged_ads_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df[df["revenue"].notnull()]

# ------------------------
# Aggregate to platform x campaign x date
# (defensive sum, in case of any duplicate rows per key)
# ------------------------
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

# ------------------------
# Filter out campaigns with too little history
# ------------------------
history_len = agg.groupby(["platform", "campaign_name"])["date"].transform("count")
before = len(agg)
agg = agg[history_len >= MIN_HISTORY_DAYS].copy()
print(f"Dropped {before - len(agg)} rows from campaigns with < {MIN_HISTORY_DAYS} days of history")
print(f"Remaining campaigns: {agg.groupby(['platform','campaign_name']).ngroups}")

# ------------------------
# Lag / rolling features PER (platform, campaign_name) — past only
# ------------------------
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

# ------------------------
# Date features
# ------------------------
agg["year"] = agg["date"].dt.year
agg["month"] = agg["date"].dt.month
agg["day_of_week"] = agg["date"].dt.dayofweek
agg["quarter"] = agg["date"].dt.quarter
agg["week_of_year"] = agg["date"].dt.isocalendar().week.astype(int)

print("\nCampaign-Day Revenue Statistics")
print(agg["revenue"].describe())

# Keep labels for post-hoc segmentation BEFORE dummy encoding
platform_labels = agg["platform"].copy()
campaign_type_labels = agg["campaign_type"].copy()

agg = pd.get_dummies(agg, columns=["platform", "campaign_type"], drop_first=True)

drop_columns = ["revenue", "date", "campaign_name"]
X = agg.drop(columns=drop_columns)
y = np.log1p(agg["revenue"])

# Chronological split — same reasoning as channel model
agg = agg.sort_values("date")
split_date = agg["date"].quantile(0.8, interpolation="nearest")
train_mask = agg["date"] <= split_date
test_mask = agg["date"] > split_date

train_indices = agg.index[train_mask]
test_indices = agg.index[test_mask]

X_train = X.loc[train_indices]
X_test = X.loc[test_indices]

y_train = y.loc[train_indices]
y_test = y.loc[test_indices]
print(f"\nTrain rows: {len(X_train)}, Test rows: {len(X_test)}")

model = LGBMRegressor(n_estimators=500, learning_rate=0.05, random_state=42)
model.fit(X_train, y_train)

pred = np.expm1(model.predict(X_test))
pred = np.expm1(model.predict(X_test))
y_test_actual = np.expm1(y_test)

test_df = agg.loc[test_mask].copy()

test_df["platform"] = platform_labels.loc[test_mask]
test_df["campaign_type"] = campaign_type_labels.loc[test_mask]

test_df["pred"] = pd.Series(
    pred,
    index=X_test.index
)

test_df["actual"] = pd.Series(
    y_test_actual,
    index=X_test.index
)

test_df["abs_error"] = (
    test_df["actual"] -
    test_df["pred"]
).abs()
test_df["abs_error"] = (test_df["actual"] - test_df["pred"]).abs()

print("\nPer campaign_type performance:")
print(test_df.groupby("campaign_type").agg(
    mean_error=("abs_error", "mean"),
    mean_actual=("actual", "mean"),
    count=("abs_error", "count"),
))

print("\nPer platform performance:")
print(test_df.groupby("platform").agg(
    mean_error=("abs_error", "mean"),
    mean_actual=("actual", "mean"),
    count=("abs_error", "count"),
))

feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)
print("\nTop Features")
print(feature_importance.head(15))

joblib.dump(model, "pickle/campaign_model.pkl")
joblib.dump(X.columns.tolist(), "pickle/campaign_features.pkl")

print("\nCampaign Model Saved Successfully.")