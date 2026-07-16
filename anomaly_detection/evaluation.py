"""
evaluation.py
-------------
Evaluation utilities for Isolation Forest
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd

from .config import OUTPUT_DIR


class AnomalyEvaluator:

    def __init__(self):

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    ####################################################

    def evaluate(
        self,
        dataframe,
        anomaly_labels,
        anomaly_scores
    ):

        total = len(dataframe)

        anomalies = int(
            np.sum(anomaly_labels == -1)
        )

        normal = int(
            np.sum(anomaly_labels == 1)
        )

        percentage = round(
            anomalies / total * 100,
            2
        )

        summary = {

            "Total Samples": total,

            "Normal Samples": normal,

            "Anomalies": anomalies,

            "Anomaly Percentage": percentage,

            "Average Score":
                float(np.mean(anomaly_scores)),

            "Minimum Score":
                float(np.min(anomaly_scores)),

            "Maximum Score":
                float(np.max(anomaly_scores))

        }

        return summary

    ####################################################

    def save_summary(
        self,
        summary
    ):

        with open(

            OUTPUT_DIR /
            "anomaly_summary.json",

            "w"

        ) as file:

            json.dump(

                summary,

                file,

                indent=4

            )

    ####################################################

    def save_scores(
        self,
        scores
    ):

        df = pd.DataFrame({

            "Anomaly Score": scores

        })

        df.to_csv(

            OUTPUT_DIR /

            "anomaly_scores.csv",

            index=False

        )

    ####################################################

    def feature_statistics(
        self,
        dataframe
    ):

        stats = dataframe.describe().T

        stats.to_csv(

            OUTPUT_DIR /

            "feature_statistics.csv"

        )

    ####################################################

    def anomaly_dataset(
        self,
        dataframe,
        labels,
        scores
    ):

        result = dataframe.copy()

        result["Anomaly"] = labels

        result["Score"] = scores

        result.to_csv(

            OUTPUT_DIR /

            "anomalies.csv",

            index=False

        )

    ####################################################

    def print_summary(
        self,
        summary
    ):

        print("\n")

        print("="*50)

        print("ANOMALY DETECTION REPORT")

        print("="*50)

        for key, value in summary.items():

            print(f"{key:<25}: {value}")

        print("="*50)

    ####################################################

    def evaluate_all(

        self,

        dataframe,

        labels,

        scores

    ):

        summary = self.evaluate(

            dataframe,

            labels,

            scores

        )

        self.save_summary(

            summary

        )

        self.save_scores(

            scores

        )

        self.feature_statistics(

            dataframe

        )

        self.anomaly_dataset(

            dataframe,

            labels,

            scores

        )

        self.print_summary(

            summary

        )

        return summary
