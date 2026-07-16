"""
predict.py
----------

Customer Segmentation Prediction Module

Loads trained KMeans model
Preprocesses incoming data
Predicts customer segments
Maps cluster IDs to business labels
Exports results
"""

import json
import joblib
import pandas as pd

from .preprocess import preprocess
from .feature_engineering import create_features

from .config import (
    MODEL_DIR,
    OUTPUT_DIR,
    FEATURE_COLUMNS
)


MODEL_PATH = MODEL_DIR / "kmeans.pkl"


class CustomerSegmentPredictor:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

        with open(
            MODEL_DIR / "cluster_labels.json",
            "r"
        ) as file:

            self.cluster_labels = json.load(file)

    ###############################################################

    def prepare(self, dataframe):
        dataframe = dataframe[FEATURE_COLUMNS]
        dataframe = create_features(dataframe)
        dataframe = preprocess(dataframe)
        return dataframe

    ###############################################################

    def predict(self, dataframe):

        processed = self.prepare(dataframe)

        clusters = self.model.predict(processed)

        result = dataframe.copy()

        result["Cluster"] = clusters

        result["Business_Label"] = result["Cluster"].astype(str).map(
            self.cluster_labels
        )

        return result

    ###############################################################

    def save(self, dataframe):

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        dataframe.to_csv(
            OUTPUT_DIR / "customer_segments.csv",
            index=False
        )

        print("Customer Segments Saved Successfully.")


###############################################################


if __name__ == "__main__":

    sample = pd.read_csv(
        "../data/processed/test.csv"
    )

    predictor = CustomerSegmentPredictor()

    results = predictor.predict(sample)

    predictor.save(results)

    print(results.head())