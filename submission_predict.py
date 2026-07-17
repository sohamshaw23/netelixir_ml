"""
submission_predict.py

CLI entry point for automated hackathon evaluation.
Generates predictions from raw campaign data and saves to CSV.
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
import joblib


def main():
    parser = argparse.ArgumentParser(description="Hackathon Submission Predictor")
    parser.add_argument("data_dir", nargs="?", default="./data", help="Path to input data folder")
    parser.add_argument("model_path", nargs="?", default="./pickle/revenue_model.pkl", help="Path to pickled model")
    parser.add_argument("output_path", nargs="?", default="./output/predictions.csv", help="Path to write predictions")
    args = parser.parse_args()

    data_dir = args.data_dir
    model_path = args.model_path
    output_path = args.output_path

    print(f"Data Dir: {data_dir}")
    print(f"Model Path: {model_path}")
    print(f"Output Path: {output_path}")

    # 1. Load data
    google_file = None
    meta_file = None
    bing_file = None

    # First pass: prefer files containing "stats" or "campaign_stats"
    for root, dirs, files in os.walk(data_dir):
        for f in files:
            fl = f.lower()
            if "google" in fl and "stats" in fl and fl.endswith(".csv"):
                google_file = os.path.join(root, f)
            elif "meta" in fl and "stats" in fl and fl.endswith(".csv"):
                meta_file = os.path.join(root, f)
            elif "bing" in fl and "stats" in fl and fl.endswith(".csv"):
                bing_file = os.path.join(root, f)

    # Second pass: fallback to generic matches
    for root, dirs, files in os.walk(data_dir):
        for f in files:
            fl = f.lower()
            if not google_file and "google" in fl and fl.endswith(".csv"):
                google_file = os.path.join(root, f)
            elif not meta_file and "meta" in fl and fl.endswith(".csv"):
                meta_file = os.path.join(root, f)
            elif not bing_file and ("bing" in fl or "microsoft" in fl or "ms" in fl) and fl.endswith(".csv"):
                bing_file = os.path.join(root, f)

    if not google_file or not meta_file or not bing_file:
        print("Error: Could not find raw campaign CSV files (google, meta, bing) in data directory.")
        sys.exit(1)

    print(f"Found Google data: {google_file}")
    print(f"Found Meta data: {meta_file}")
    print(f"Found Bing data: {bing_file}")

    google_df = pd.read_csv(google_file)
    meta_df = pd.read_csv(meta_file)
    bing_df = pd.read_csv(bing_file)

    # 2. Preprocess and merge
    from utils.clean_data import clean_google_data, clean_meta_data, clean_bing_data
    
    google_clean = clean_google_data(google_df)
    bing_clean = clean_bing_data(bing_df)
    
    g_rev = google_clean['revenue'].sum()
    g_clicks = google_clean['clicks'].sum()
    revenue_per_click = g_rev / g_clicks if g_clicks > 0 else 0.0
    
    meta_clean = clean_meta_data(meta_df, revenue_per_click)
    
    merged_df = pd.concat([google_clean, meta_clean, bing_clean], ignore_index=True)
    
    merged_df["roas"] = 0.0
    valid_spend = merged_df["spend"] >= 1.0
    merged_df.loc[valid_spend, "roas"] = merged_df.loc[valid_spend, "revenue"] / merged_df.loc[valid_spend, "spend"]

    # 3. Load model and detect type
    if not os.path.exists(model_path):
        print(f"Error: Model file {model_path} does not exist.")
        sys.exit(1)

    model = joblib.load(model_path)
    
    if not hasattr(model, "feature_name_"):
        print("Error: Loaded model is not a valid LightGBM model with feature_name_ attribute.")
        sys.exit(1)

    features = model.feature_name_
    has_revenue_lag = any("revenue_lag" in f for f in features)
    has_campaign_type = any("campaign_type" in f for f in features)

    model_type = "revenue"
    if has_revenue_lag:
        if has_campaign_type:
            model_type = "campaign"
        else:
            model_type = "channel"
    else:
        if "roas" in model_path.lower():
            model_type = "roas"

    print(f"Detected model type: {model_type}")

    # 4. Generate features
    merged_df["date"] = pd.to_datetime(merged_df["date"])
    
    if model_type in ["campaign", "channel"]:
        if model_type == "campaign":
            merged_df.sort_values(by=["platform", "campaign_name", "date"], inplace=True)
            gp = merged_df.groupby(["platform", "campaign_name"])
        else:
            merged_df.sort_values(by=["platform", "date"], inplace=True)
            gp = merged_df.groupby(["platform"])
            
        merged_df["revenue_lag_1"] = gp["revenue"].shift(1).fillna(0)
        merged_df["revenue_lag_7"] = gp["revenue"].shift(7).fillna(0)
        merged_df["revenue_roll_mean_7"] = gp["revenue"].transform(lambda x: x.shift(1).rolling(7, min_periods=1).mean()).fillna(0)
        merged_df["revenue_roll_std_7"] = gp["revenue"].transform(lambda x: x.shift(1).rolling(7, min_periods=1).std()).fillna(0)
        merged_df["revenue_roll_std_14"] = gp["revenue"].transform(lambda x: x.shift(1).rolling(14, min_periods=1).std()).fillna(0)
        merged_df["spend_lag_1"] = gp["spend"].shift(1).fillna(0)
        merged_df["spend_roll_mean_7"] = gp["spend"].transform(lambda x: x.shift(1).rolling(7, min_periods=1).mean()).fillna(0)

    from utils.feature_engineering import create_features
    df_feat = create_features(merged_df.copy())

    drop_cols = ["revenue", "roas", "revenue_is_proxy", "date", "campaign_name", "campaign_id"]
    df_pred = df_feat.drop(columns=drop_cols, errors="ignore")
    df_pred = pd.get_dummies(df_pred)
    
    for col in features:
        if col not in df_pred.columns:
            df_pred[col] = 0
    df_pred = df_pred[features]

    # 5. Predict
    preds = np.expm1(model.predict(df_pred))
    preds = np.clip(preds, 0, None)

    # 6. Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    out_dict = {
        "prediction": preds,
        f"predicted_{model_type}": preds
    }
    if model_type == "campaign":
        out_dict["predicted_campaign_revenue"] = preds
    elif model_type == "channel":
        out_dict["predicted_channel_revenue"] = preds
    elif model_type == "revenue":
        out_dict["predicted_revenue"] = preds
    elif model_type == "roas":
        out_dict["predicted_roas"] = preds
        
    df_out = pd.DataFrame(out_dict)
    df_out.to_csv(output_path, index=False)
    print(f"Successfully wrote {len(preds)} predictions to {output_path}!")


if __name__ == "__main__":
    main()
