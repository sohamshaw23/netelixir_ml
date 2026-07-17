import pandas as pd


def create_features(df):

    df = df.copy()

    # ------------------------
    # Date Features
    # ------------------------

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.dayofweek
    df["quarter"] = df["date"].dt.quarter
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)

    # ------------------------
    # Marketing Features
    # ------------------------

    df["ctr_calc"] = (
        df["clicks"] /
        (df["impressions"] + 1)
    )

    df["conversion_rate"] = (
        df["conversions"] /
        (df["clicks"] + 1)
    )

    df["cpc_calc"] = (
        df["spend"] /
        (df["clicks"] + 1)
    )

    df["cpm_calc"] = (
        df["spend"] * 1000 /
        (df["impressions"] + 1)
    )

    # ------------------------
    # Platform Encoding
    # ------------------------
    # ------------------------
    # Brand Campaign Feature
    # ------------------------

    df["is_brand_campaign"] = (
        df["campaign_name"].str.contains(
            "Brand",
            case=False,
            na=False
        )
        |
        (
            df["campaign_name"].str.contains(
                "TM",
                case=False,
                na=False
            )
            &
            ~df["campaign_name"].str.contains(
                "NTM",
                case=False,
                na=False
            )
        )
    ).astype(int)

    df = pd.get_dummies(
        df,
        columns=["platform"],
        drop_first=True
    )

    return df
