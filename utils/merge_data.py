import pandas as pd

from load_data import load_data

from clean_data import (
    clean_google_data,
    clean_meta_data,
    clean_bing_data
)

# Load raw datasets
google_df, meta_df, bing_df = load_data()

# Clean Google and Bing first
google_clean = clean_google_data(google_df)
bing_clean = clean_bing_data(bing_df)

# Calculate Revenue Per Click
known = pd.concat(
    [google_clean, bing_clean],
    ignore_index=True
)

clicking = known[known["clicks"] > 0]

revenue_per_click = (
    clicking["revenue"] / clicking["clicks"]
).median()

print("Revenue Per Click:", revenue_per_click)

# Clean Meta using RPC proxy
meta_clean = clean_meta_data(
    meta_df,
    revenue_per_click
)

# Merge all datasets
merged_df = pd.concat(
    [google_clean, meta_clean, bing_clean],
    ignore_index=True,
    sort=False
)
# Avoid division by zero
MIN_SPEND_FOR_ROAS = 1.0

merged_df["roas"] = None

valid_spend = (
    merged_df["spend"] >= MIN_SPEND_FOR_ROAS
)

merged_df.loc[
    valid_spend,
    "roas"
] = (
    merged_df.loc[valid_spend, "revenue"] /
    merged_df.loc[valid_spend, "spend"]
)

print(
    f"Rows excluded from ROAS training: "
    f"{(~valid_spend).sum()} / {len(merged_df)}"
)
# Save merged dataset
merged_df.to_csv(
    "data/processed/merged_ads_data.csv",
    index=False
)

print("\nMerged Dataset Shape:", merged_df.shape)

print("\nRevenue Null Values:")
print(merged_df["revenue"].isnull().sum())

print("\nRows per Platform:")
print(merged_df["platform"].value_counts())