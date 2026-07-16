import pandas as pd

from sklearn.preprocessing import LabelEncoder

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import StandardScaler

import joblib

from .config import MODEL_DIR


def preprocess(df):

    df = df.copy()

    import numpy as np
    df = df.fillna(value=np.nan)

    numerical = [c for c in df.select_dtypes(include=["int64", "float64"]).columns if c != "RevenueDrop"]


    categorical = df.select_dtypes(include=["object"]).columns

    num_imputer = SimpleImputer(strategy="median")

    df[numerical] = num_imputer.fit_transform(df[numerical])

    cat_imputer = SimpleImputer(strategy="most_frequent")

    df[categorical] = cat_imputer.fit_transform(df[categorical])

    encoders = {}

    for col in categorical:

        le = LabelEncoder()

        df[col] = le.fit_transform(df[col])

        encoders[col] = le

    scaler = StandardScaler()

    df[numerical] = scaler.fit_transform(df[numerical])

    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")

    joblib.dump(encoders, MODEL_DIR / "encoders.pkl")

    return df