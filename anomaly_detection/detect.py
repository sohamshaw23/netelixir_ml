"""
detect.py
---------
Anomaly Detection Inference

Loads Isolation Forest
Detects anomalies
Assigns severity levels
Exports results
"""

import joblib
import pandas as pd

from .preprocess import preprocess
from .feature_engineering import create_features

from .config import MODEL_DIR, FEATURE_COLUMNS


MODEL_PATH = MODEL_DIR / "isolation_forest.pkl"


class AnomalyDetector:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

    ##########################################################

    def prepare(self, dataframe):
        df = dataframe[FEATURE_COLUMNS]
        df = create_features(df)
        df = preprocess(df)
        return df

    ##########################################################

    def detect(self, dataframe):

        processed = self.prepare(dataframe)

        labels = self.model.predict(processed)

        scores = self.model.decision_function(processed)

        result = dataframe.copy()

        result["Anomaly"] = labels

        result["Anomaly_Score"] = scores

        result["Severity"] = self.severity(scores)

        result["Status"] = result["Anomaly"].map({

            1: "Normal",

            -1: "Anomaly"

        })

        return result

    ##########################################################

    def severity(self, scores):

        severity = []

        for score in scores:

            if score < -0.20:

                severity.append("Critical")

            elif score < -0.10:

                severity.append("High")

            elif score < 0:

                severity.append("Medium")

            else:

                severity.append("Low")

        return severity

    ##########################################################

    def save(self, dataframe):

        dataframe.to_csv(

            "outputs/anomalies.csv",

            index=False

        )

        print("Results Saved.")
        

if __name__ == "__main__":

    sample = pd.read_csv(

        "../data/processed/test.csv"

    )

    detector = AnomalyDetector()

    result = detector.detect(sample)

    detector.save(result)

    print(result.head())

