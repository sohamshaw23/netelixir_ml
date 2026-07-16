"""
generate_features.py

Feature Engineering Pipeline

Steps
-----
1. Load cleaned dataset
2. Generate derived features
3. Encode categorical variables
4. Scale numerical features
5. Save feature dataset

Usage
-----
python scripts/generate_features.py
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


##############################################################

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DATA = (
    BASE_DIR /
    "data" /
    "processed" /
    "cleaned_dataset.csv"
)

OUTPUT_DIR = (
    BASE_DIR /
    "data" /
    "processed"
)

MODEL_DIR = (
    BASE_DIR /
    "shared" /
    "artifacts"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = OUTPUT_DIR / "features_dataset.csv"

##############################################################


class FeatureGenerator:

    def __init__(self):

        self.df = None

    ##########################################################

    def load_dataset(self):

        print("Loading cleaned dataset...")

        self.df = pd.read_csv(INPUT_DATA)

    ##########################################################

    def create_features(self):

        df = self.df

        ##################################################

        df["Revenue_per_Click"] = (

            df["Revenue"]

            /

            (df["Clicks"] + 1)

        )

        df["Conversion_Rate"] = (

            df["Conversions"]

            /

            (df["Clicks"] + 1)

        )

        df["Revenue_to_Spend"] = (

            df["Revenue"]

            /

            (df["Spend"] + 1)

        )

        df["Spend_per_Conversion"] = (

            df["Spend"]

            /

            (df["Conversions"] + 1)

        )

        df["CTR_ROAS"] = (

            df["CTR"]

            *

            df["ROAS"]

        )

        df["Revenue_per_Impression"] = (

            df["Revenue"]

            /

            (df["Impressions"] + 1)

        )

        df["Clicks_per_Impression"] = (

            df["Clicks"]

            /

            (df["Impressions"] + 1)

        )

        df["Cost_per_Impression"] = (

            df["Spend"]

            /

            (df["Impressions"] + 1)

        )

        df["Log_Revenue"] = np.log1p(

            df["Revenue"]

        )

        df["Log_Spend"] = np.log1p(

            df["Spend"]

        )

        df["Log_Clicks"] = np.log1p(

            df["Clicks"]

        )

        df["High_ROAS"] = (

            df["ROAS"] > 3

        ).astype(int)

        self.df = df

    ##########################################################

    def encode_features(self):

        categorical = self.df.select_dtypes(

            include="object"

        ).columns

        encoders = {}

        for column in categorical:

            encoder = LabelEncoder()

            self.df[column] = encoder.fit_transform(

                self.df[column]

            )

            encoders[column] = encoder

        joblib.dump(

            encoders,

            MODEL_DIR /

            "encoders.pkl"

        )

    ##########################################################

    def scale_features(self):

        numeric = self.df.select_dtypes(

            include=np.number

        ).columns

        scaler = StandardScaler()

        self.df[numeric] = scaler.fit_transform(

            self.df[numeric]

        )

        joblib.dump(

            scaler,

            MODEL_DIR /

            "scaler.pkl"

        )

    ##########################################################

    def save(self):

        self.df.to_csv(

            OUTPUT_FILE,

            index=False

        )

        joblib.dump(

            list(self.df.columns),

            MODEL_DIR /

            "feature_columns.pkl"

        )

        print()

        print("=" * 50)

        print("Feature Engineering Completed")

        print("=" * 50)

        print(f"Saved : {OUTPUT_FILE}")

        print(f"Features : {len(self.df.columns)}")

        print("=" * 50)

    ##########################################################

    def run(self):

        self.load_dataset()

        self.create_features()

        self.encode_features()

        self.scale_features()

        self.save()


##############################################################


def main():

    generator = FeatureGenerator()

    generator.run()


##############################################################

if __name__ == "__main__":

    main()

