import pandas as pd

df = pd.read_csv(
    "data/processed/merged_ads_data.csv"
)

bing = df[df["platform"] == "bing"]

print(
    bing.sort_values(
        by="roas",
        ascending=False
    )[
        [
            "campaign_name",
            "spend",
            "revenue",
            "roas"
        ]
    ].head(20)
)