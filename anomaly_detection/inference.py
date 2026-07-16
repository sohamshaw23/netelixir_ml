"""
inference.py
------------

Inference pipeline for Anomaly Detection.

This module loads the trained Isolation Forest model,
detects anomalies, summarizes results, and prepares
JSON-compatible output for the Flask API.
"""

import pandas as pd

from .detect import AnomalyDetector


class AnomalyInference:

    def __init__(self):

        self.detector = AnomalyDetector()

    # --------------------------------------------------

    def analyze(self, dataframe):

        results = self.detector.detect(dataframe)

        total = len(results)

        normal = len(results[results["Status"] == "Normal"])

        anomalies = len(results[results["Status"] == "Anomaly"])

        critical = len(results[
            results["Severity"] == "Critical"
        ])

        high = len(results[
            results["Severity"] == "High"
        ])

        medium = len(results[
            results["Severity"] == "Medium"
        ])

        low = len(results[
            results["Severity"] == "Low"
        ])

        average_score = float(
            results["Anomaly_Score"].mean()
        )

        top_anomalies = (

            results

            .sort_values(

                "Anomaly_Score"

            )

            .head(10)

            .to_dict(

                orient="records"

            )

        )

        response = {

            "summary": {

                "total_campaigns": total,

                "normal_campaigns": normal,

                "anomalous_campaigns": anomalies,

                "critical": critical,

                "high": high,

                "medium": medium,

                "low": low,

                "average_score": average_score

            },

            "top_anomalies": top_anomalies,

            "results": results.to_dict(

                orient="records"

            )

        }

        return response


# ------------------------------------------------------


_detector = None


def detect_anomalies(df: pd.DataFrame):

    """
    Function used by Flask app.py

    Example:

    from anomaly_detection.inference
    import detect_anomalies

    result = detect_anomalies(df)
    """

    global _detector

    if _detector is None:

        _detector = AnomalyInference()

    return _detector.analyze(df)


# ------------------------------------------------------


if __name__ == "__main__":

    sample = pd.read_csv(

        "../data/processed/test.csv"

    )

    response = detect_anomalies(sample)

    print(response["summary"])
