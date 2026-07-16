"""
shared/feature_engineering.py

Universal Feature Engineering Pipeline

Features
--------
✓ Revenue Features
✓ Marketing Features
✓ Campaign Features
✓ Log Features
✓ Ratio Features
✓ Interaction Features
"""

import numpy as np
import pandas as pd


class FeatureEngineer:

    def __init__(self):

        pass

    ########################################################

    def revenue_features(self, df):

        if {"Revenue", "Clicks"}.issubset(df.columns):

            df["Revenue_per_Click"] = (

                df["Revenue"]

                /

                (df["Clicks"] + 1)

            )

        if {"Revenue", "Spend"}.issubset(df.columns):

            df["Revenue_to_Spend"] = (

                df["Revenue"]

                /

                (df["Spend"] + 1)

            )

        if {"Revenue", "Impressions"}.issubset(df.columns):

            df["Revenue_per_Impression"] = (

                df["Revenue"]

                /

                (df["Impressions"] + 1)

            )

        return df

    ########################################################

    def conversion_features(self, df):

        if {"Conversions", "Clicks"}.issubset(df.columns):

            df["Conversion_Rate"] = (

                df["Conversions"]

                /

                (df["Clicks"] + 1)

            )

        if {"Spend", "Conversions"}.issubset(df.columns):

            df["Spend_per_Conversion"] = (

                df["Spend"]

                /

                (df["Conversions"] + 1)

            )

        return df

    ########################################################

    def ctr_features(self, df):

        if {"CTR", "ROAS"}.issubset(df.columns):

            df["CTR_ROAS"] = (

                df["CTR"]

                *

                df["ROAS"]

            )

        if {"Clicks", "Impressions"}.issubset(df.columns):

            df["Clicks_per_Impression"] = (

                df["Clicks"]

                /

                (df["Impressions"] + 1)

            )

        if {"Spend", "Impressions"}.issubset(df.columns):

            df["Cost_per_Impression"] = (

                df["Spend"]

                /

                (df["Impressions"] + 1)

            )

        return df

    ########################################################

    def logarithmic_features(self, df):

        for column in [

            "Revenue",

            "Spend",

            "Clicks",

            "Impressions",

            "Conversions"

        ]:

            if column in df.columns:

                df[f"Log_{column}"] = np.log1p(

                    df[column]

                )

        return df

    ########################################################

    def binary_features(self, df):

        if "ROAS" in df.columns:

            df["High_ROAS"] = (

                df["ROAS"] > 3

            ).astype(int)

        if "CTR" in df.columns:

            df["High_CTR"] = (

                df["CTR"] >

                df["CTR"].median()

            ).astype(int)

        if "Revenue" in df.columns:

            df["High_Revenue"] = (

                df["Revenue"] >

                df["Revenue"].median()

            ).astype(int)

        return df

    ########################################################

    def interaction_features(self, df):

        if {"Spend", "CTR"}.issubset(df.columns):

            df["Spend_x_CTR"] = (

                df["Spend"]

                *

                df["CTR"]

            )

        if {"Revenue", "ROAS"}.issubset(df.columns):

            df["Revenue_x_ROAS"] = (

                df["Revenue"]

                *

                df["ROAS"]

            )

        if {"Clicks", "Conversions"}.issubset(df.columns):

            df["Clicks_x_Conversions"] = (

                df["Clicks"]

                *

                df["Conversions"]

            )

        return df

    ########################################################

    def statistical_features(self, df):

        numeric = df.select_dtypes(

            include=np.number

        ).columns

        if len(numeric) > 0:

            df["Row_Mean"] = df[numeric].mean(axis=1)

            df["Row_STD"] = df[numeric].std(axis=1)

            df["Row_Max"] = df[numeric].max(axis=1)

            df["Row_Min"] = df[numeric].min(axis=1)

        return df

    ########################################################

    def date_features(self, df):

        if "Date" in df.columns:

            df["Date"] = pd.to_datetime(

                df["Date"]

            )

            df["Year"] = df["Date"].dt.year

            df["Month"] = df["Date"].dt.month

            df["Day"] = df["Date"].dt.day

            df["Weekday"] = df["Date"].dt.weekday

            df["Quarter"] = df["Date"].dt.quarter

        return df

    ########################################################

    def create_features(self, dataframe):

        dataframe = dataframe.copy()

        dataframe = self.revenue_features(

            dataframe

        )

        dataframe = self.conversion_features(

            dataframe

        )

        dataframe = self.ctr_features(

            dataframe

        )

        dataframe = self.logarithmic_features(

            dataframe

        )

        dataframe = self.binary_features(

            dataframe

        )

        dataframe = self.interaction_features(

            dataframe

        )

        dataframe = self.statistical_features(

            dataframe

        )

        dataframe = self.date_features(

            dataframe

        )

        return dataframe


############################################################

_engineer = FeatureEngineer()


def create_features(dataframe):

    return _engineer.create_features(

        dataframe

    )

