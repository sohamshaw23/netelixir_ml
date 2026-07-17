"""
utils/clean_data.py

Preprocessing and cleaning pipelines for Google, Meta, and Bing ads datasets.
"""

import pandas as pd


def get_rev_per_conversions(df):
    """
    Helper to calculate average revenue per conversion.
    """
    total_revenue = df["revenue"].sum()
    total_conversions = df["conversions"].sum()

    return total_revenue / total_conversions


def clean_google_data(df):
    df = df.copy()
    df.drop(columns=["Unnamed: 0"], errors="ignore", inplace=True)

    # Check if it has teammate's raw columns
    if "campaign_budget_amount" in df.columns:
        df.rename(columns={
            "campaign_id": "campaign_id",
            "segments_date": "date",
            "metrics_clicks": "clicks",
            "metrics_conversions": "conversions",
            "metrics_cost_micros": "spend",
            "metrics_impressions": "impressions",
            "metrics_video_views": "video_views",
            "metrics_conversions_value": "revenue",
            "campaign_advertising_channel_type": "campaign_type",
            "campaign_budget_amount": "budget",
            "campaign_name": "campaign_name"
        }, inplace=True)
        df["spend"] = df["spend"] / 1_000_000
    else:
        # Simplified schema
        rename_map = {
            "segments_date": "date",
            "metrics_clicks": "clicks",
            "metrics_conversions": "conversions",
            "metrics_cost_micros": "spend",
            "metrics_impressions": "impressions",
            "metrics_video_views": "video_views",
            "metrics_conversions_value": "revenue",
            "channel": "campaign_type"
        }
        df.rename(columns=rename_map, inplace=True)

    # Fill default columns for LightGBM compatibility
    if "budget" not in df.columns:
        df["budget"] = 50.0
    if "campaign_type" not in df.columns:
        df["campaign_type"] = "Search"
    if "video_views" not in df.columns:
        df["video_views"] = 0

    df["budget"] = df["budget"].fillna(50.0)
    df["date"] = pd.to_datetime(df["date"])
    df["platform"] = "google"
    df["revenue_is_proxy"] = False

    return df


def clean_meta_data(df, revenue_per_click=None):
    df = df.copy()
    df.drop(columns=["Unnamed: 0"], errors="ignore", inplace=True)

    if "daily_budget" in df.columns:
        df.rename(columns={
            "date_start": "date",
            "conversion": "conversions",
            "daily_budget": "budget"
        }, inplace=True)
    else:
        df.rename(columns={
            "date_start": "date",
            "conversion": "conversions",
            "daily_budget": "budget"
        }, inplace=True)

    if "budget" not in df.columns:
        df["budget"] = 50.0
    if "conversions" not in df.columns:
        df["conversions"] = 0

    df["budget"] = df["budget"].fillna(50.0)
    df["date"] = pd.to_datetime(df["date"])

    if "revenue" not in df.columns or df["revenue"].isnull().all():
        if revenue_per_click is not None:
            df["revenue"] = df["clicks"] * revenue_per_click
        else:
            df["revenue"] = 0.0

    df["platform"] = "meta"
    df["revenue_is_proxy"] = True

    return df


def clean_bing_data(df):
    df = df.copy()
    df.drop(columns=["Unnamed: 0"], errors="ignore", inplace=True)

    if "DailyBudget" in df.columns:
        df.rename(columns={
            "CampaignId": "campaign_id",
            "TimePeriod": "date",
            "Revenue": "revenue",
            "Spend": "spend",
            "Clicks": "clicks",
            "Impressions": "impressions",
            "Conversions": "conversions",
            "CampaignType": "campaign_type",
            "DailyBudget": "budget",
            "CampaignName": "campaign_name"
        }, inplace=True)
    else:
        df.rename(columns={
            "date": "date",
            "channel": "campaign_type"
        }, inplace=True)

    if "budget" not in df.columns:
        df["budget"] = 10.0
    if "campaign_type" not in df.columns:
        df["campaign_type"] = "Search"

    df["budget"] = df["budget"].fillna(10.0)
    df["date"] = pd.to_datetime(df["date"])
    df["platform"] = "bing"
    df["revenue_is_proxy"] = False

    return df