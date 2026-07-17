import pandas as pd
def calculate_aov(google_df, bing_df):
    total_revenue = (
        google_df["metrics_conversions_value"].sum()
        + bing_df["Revenue"].sum()
    )

    total_conversions = (
        google_df["metrics_conversions"].sum()
        + bing_df["Conversions"].sum()
    )

    if total_conversions == 0:
        return 0

    return total_revenue / total_conversions

def clean_google_data(df):
    df = df.copy()
    

    df.drop(columns=["Unnamed: 0"], inplace=True)

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

    df["budget"] = df["budget"].fillna(df["budget"].median())

    df["date"] = pd.to_datetime(df["date"])

    df["platform"] = "google"
    df["revenue_is_proxy"] = False

    return df

    


def clean_meta_data(df, revenue_per_click=None):
    df = df.copy()

    df.drop(columns=["Unnamed: 0"], inplace=True)

    df.rename(columns={
        "date_start": "date",
        "conversion": "conversions",
        "daily_budget": "budget"
    }, inplace=True)

    df["budget"] = df["budget"].fillna(
        df["budget"].median()
    )

    df["date"] = pd.to_datetime(df["date"])

    if revenue_per_click is not None:
        df["revenue"] = (
            df["clicks"] * revenue_per_click
        )
    else:
        df["revenue"] = None

    df["platform"] = "meta"
    df["revenue_is_proxy"] = True

    return df

def clean_bing_data(df):
    df = df.copy()

    df.drop(columns=["Unnamed: 0"], inplace=True)

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

    df["date"] = pd.to_datetime(df["date"])

    df["platform"] = "bing"
    df["revenue_is_proxy"] = False

    return df