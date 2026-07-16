"""
clean_data.py

Data Cleaning Pipeline

Functions
---------
1. Remove duplicates
2. Handle missing values
3. Remove outliers
4. Standardize column names
5. Save cleaned dataset

Usage
-----
python scripts/clean_data.py
"""

from pathlib import Path
import numpy as np
import pandas as pd


##############################################################

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw" / "marketing_data.csv"

PROCESSED_DIR = BASE_DIR / "data" / "processed"

OUTPUT_FILE = PROCESSED_DIR / "cleaned_dataset.csv"

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

##############################################################


class DataCleaner:

    def __init__(self):

        self.df = None

    ##########################################################

    def load_data(self):

        print("Loading Dataset...")

        self.df = pd.read_csv(RAW_DATA)

        print(f"Rows : {len(self.df)}")

        print(f"Columns : {len(self.df.columns)}")

    ##########################################################

    def standardize_columns(self):

        self.df.columns = (

            self.df.columns

            .str.strip()

            .str.replace(" ", "_")

            .str.replace("-", "_")

        )

    ##########################################################

    def remove_duplicates(self):

        before = len(self.df)

        self.df.drop_duplicates(

            inplace=True

        )

        removed = before - len(self.df)

        print(f"Duplicates Removed : {removed}")

    ##########################################################

    def fill_missing(self):

        numeric = self.df.select_dtypes(

            include=np.number

        ).columns

        categorical = self.df.select_dtypes(

            exclude=np.number

        ).columns

        for col in numeric:

            self.df[col] = self.df[col].fillna(

                self.df[col].median()

            )

        for col in categorical:

            self.df[col] = self.df[col].fillna(

                self.df[col].mode()[0]

            )

    ##########################################################

    def remove_outliers(self):

        numeric = self.df.select_dtypes(

            include=np.number

        ).columns

        for col in numeric:

            q1 = self.df[col].quantile(0.25)

            q3 = self.df[col].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr

            upper = q3 + 1.5 * iqr

            self.df = self.df[

                (self.df[col] >= lower)

                &

                (self.df[col] <= upper)

            ]

    ##########################################################

    def convert_types(self):

        numeric = [

            "Spend",

            "Revenue",

            "Clicks",

            "Impressions",

            "CTR",

            "CPC",

            "Conversions",

            "ROAS"

        ]

        for col in numeric:

            if col in self.df.columns:

                self.df[col] = pd.to_numeric(

                    self.df[col],

                    errors="coerce"

                )

    ##########################################################

    def save(self):

        self.df.to_csv(

            OUTPUT_FILE,

            index=False

        )

        print()

        print("=" * 50)

        print("Cleaning Completed")

        print("=" * 50)

        print(f"Saved : {OUTPUT_FILE}")

        print(f"Rows : {len(self.df)}")

        print("=" * 50)

    ##########################################################

    def run(self):

        self.load_data()

        self.standardize_columns()

        self.remove_duplicates()

        self.convert_types()

        self.fill_missing()

        self.remove_outliers()

        self.save()


##############################################################


def main():

    cleaner = DataCleaner()

    cleaner.run()


##############################################################

if __name__ == "__main__":

    main()

