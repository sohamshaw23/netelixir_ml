import pandas as pd

df = pd.read_csv(
    "data/processed/merged_ads_data.csv"
)

df = df[df["roas"].notnull()]

zero_count = (
    df["roas"] == 0
).sum()

total = len(df)

print(
    f"Zero ROAS rows: {zero_count}"
)

print(
    f"Total rows: {total}"
)

print(
    f"Percentage Zero: "
    f"{100*zero_count/total:.2f}%"
)