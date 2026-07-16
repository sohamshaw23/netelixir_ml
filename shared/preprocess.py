"""
shared/preprocess.py

Universal preprocessing pipeline for all ML models.

Features
--------
✔ Missing value handling
✔ Label Encoding
✔ Standard Scaling
✔ Save preprocessing artifacts
✔ Load preprocessing artifacts
✔ Training & Inference modes
"""

from pathlib import Path

import joblib
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from shared.constants import (
    MODELS_DIR,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES
)


class Preprocessor:

    def __init__(self):

        MODELS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.scaler = StandardScaler()

        self.numeric_imputer = SimpleImputer(
            strategy="median"
        )

        self.categorical_imputer = SimpleImputer(
            strategy="most_frequent"
        )

        self.encoders = {}

    ########################################################

    @property
    def scaler_path(self):

        return MODELS_DIR / "scaler.pkl"

    ########################################################

    @property
    def encoder_path(self):

        return MODELS_DIR / "encoders.pkl"

    ########################################################

    def fit(self, dataframe):

        dataframe = dataframe.copy()

        ####################################################
        # Missing Values
        ####################################################

        available_numeric = [
            col for col in NUMERIC_FEATURES
            if col in dataframe.columns
        ]

        available_categorical = [
            col for col in CATEGORICAL_FEATURES
            if col in dataframe.columns
        ]

        if available_numeric:

            dataframe[available_numeric] = (
                self.numeric_imputer.fit_transform(
                    dataframe[available_numeric]
                )
            )

        if available_categorical:

            dataframe[available_categorical] = (
                self.categorical_imputer.fit_transform(
                    dataframe[available_categorical]
                )
            )

        ####################################################
        # Label Encoding
        ####################################################

        for column in available_categorical:

            encoder = LabelEncoder()

            dataframe[column] = encoder.fit_transform(
                dataframe[column].astype(str)
            )

            self.encoders[column] = encoder

        ####################################################
        # Scaling
        ####################################################

        if available_numeric:

            dataframe[available_numeric] = (
                self.scaler.fit_transform(
                    dataframe[available_numeric]
                )
            )

        ####################################################
        # Save Artifacts
        ####################################################

        joblib.dump(
            self.scaler,
            self.scaler_path
        )

        joblib.dump(
            self.encoders,
            self.encoder_path
        )

        return dataframe

    ########################################################

    def transform(self, dataframe):

        dataframe = dataframe.copy()

        ####################################################
        # Load Artifacts
        ####################################################

        self.scaler = joblib.load(
            self.scaler_path
        )

        self.encoders = joblib.load(
            self.encoder_path
        )

        ####################################################
        # Missing Values
        ####################################################

        available_numeric = [
            col for col in NUMERIC_FEATURES
            if col in dataframe.columns
        ]

        available_categorical = [
            col for col in CATEGORICAL_FEATURES
            if col in dataframe.columns
        ]

        if available_numeric:

            dataframe[available_numeric] = (
                self.numeric_imputer.fit_transform(
                    dataframe[available_numeric]
                )
            )

        if available_categorical:

            dataframe[available_categorical] = (
                self.categorical_imputer.fit_transform(
                    dataframe[available_categorical]
                )
            )

        ####################################################
        # Apply Encoders
        ####################################################

        for column in available_categorical:

            encoder = self.encoders[column]

            values = []

            for item in dataframe[column].astype(str):

                if item in encoder.classes_:

                    values.append(
                        encoder.transform([item])[0]
                    )

                else:
                    values.append(-1)

            dataframe[column] = values

        ####################################################
        # Apply Scaler
        ####################################################

        if available_numeric:

            dataframe[available_numeric] = (
                self.scaler.transform(
                    dataframe[available_numeric]
                )
            )

        return dataframe

    ########################################################

    def fit_transform(self, dataframe):

        return self.fit(dataframe)


############################################################

_preprocessor = Preprocessor()


def fit_transform(dataframe):

    return _preprocessor.fit_transform(
        dataframe
    )


def transform(dataframe):

    return _preprocessor.transform(
        dataframe
    )

