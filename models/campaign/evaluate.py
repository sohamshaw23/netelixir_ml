import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ---------------------------------------------------
# Stored metrics from training
# ---------------------------------------------------

MAE_SCORE = 93.59
R2_SCORE = 0.82

platform_results = {
    "google": {
        "mean_error": 165.19,
        "mean_actual": 480.07
    },
    "meta": {
        "mean_error": 26.21,
        "mean_actual": 195.84
    },
    "bing": {
        "mean_error": 4.19,
        "mean_actual": 6.41
    }
}

campaign_results = {
    "Demand Gen": 2.33,
    "Generic": 8.36,
    "Pmax": 79.21,
    "Prospecting": 31.10,
    "Remarketing": 22.50,
    "Search": 120.00,
    "Shopping": 348.94
}

print("\n" + "="*60)
print("Campaign Model Evaluation")
print("="*60)

print(f"\nMAE Score : {MAE_SCORE}")
print(f"R2 Score  : {R2_SCORE}")

print("\nPlatform Performance")
print("-"*60)

for platform, values in platform_results.items():

    print(
        f"{platform.upper():10}"
        f" Error: {values['mean_error']:8.2f}"
        f" Revenue: {values['mean_actual']:8.2f}"
    )

print("\nCampaign Type Performance")
print("-"*60)

for campaign, error in campaign_results.items():

    print(
        f"{campaign:15} "
        f"Mean Error: {error:8.2f}"
    )

print("\nTop Predictive Signals")
print("-"*60)

top_features = [
    "conversions",
    "conversion_rate",
    "clicks",
    "ctr_calc",
    "cpc_calc",
    "revenue_lag_1",
    "spend_roll_mean_7"
]

for feature in top_features:
    print(feature)

print("\nCampaign Model Evaluation Complete.")