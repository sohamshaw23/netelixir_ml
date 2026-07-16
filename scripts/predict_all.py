"""
predict_all.py

Runs inference using all trained models.

Models
------
1. Revenue Drop Risk
2. Anomaly Detection
3. Customer Segmentation
4. Creative Performance

Usage
-----
python scripts/predict_all.py
"""

from pathlib import Path

import pandas as pd

from revenue_drop_risk.predict import RevenueRiskPredictor
from anomaly_detection.detect import AnomalyDetector
from customer_segmentation.predict import CustomerSegmentPredictor
from creative_performance.predict import (
    CreativePerformancePredictor
)


###############################################################

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DATA = (
    BASE_DIR /
    "data" /
    "processed" /
    "features_dataset.csv"
)

OUTPUT_DIR = (
    BASE_DIR /
    "reports"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = (
    OUTPUT_DIR /
    "final_predictions.csv"
)

###############################################################


class PredictionPipeline:

    def __init__(self):

        self.revenue = RevenueRiskPredictor()

        self.anomaly = AnomalyDetector()

        self.segment = CustomerSegmentPredictor()

        self.creative = CreativePerformancePredictor()

    ###########################################################

    def load_data(self):

        print("Loading Dataset...")

        return pd.read_csv(INPUT_DATA)

    ###########################################################

    def predict_revenue(

        self,

        dataframe

    ):

        print("Revenue Prediction...")

        return self.revenue.predict(

            dataframe.copy()

        )

    ###########################################################

    def predict_anomaly(

        self,

        dataframe

    ):

        print("Anomaly Detection...")

        return self.anomaly.detect(

            dataframe.copy()

        )

    ###########################################################

    def predict_segment(

        self,

        dataframe

    ):

        print("Customer Segmentation...")

        return self.segment.predict(

            dataframe.copy()

        )

    ###########################################################

    def predict_creative(

        self,

        dataframe

    ):

        print("Creative Performance...")

        return self.creative.predict(

            dataframe.copy()

        )

    ###########################################################

    def combine(

        self,

        revenue,

        anomaly,

        segment,

        creative

    ):

        final = revenue.copy()

        ###################################################

        final["Anomaly"] = anomaly["Anomaly"]

        final["Severity"] = anomaly["Severity"]

        ###################################################

        final["Cluster"] = segment["Cluster"]

        final["Business_Label"] = (

            segment["Business_Label"]

        )

        ###################################################

        final["Performance_Score"] = (

            creative["Performance_Score"]

        )

        final["Recommendation"] = (

            creative["Recommendation"]

        )

        final["Creative_Rank"] = (

            creative["Rank"]

        )

        return final

    ###########################################################

    def save(

        self,

        dataframe

    ):

        dataframe.to_csv(

            OUTPUT_FILE,

            index=False

        )

        print()

        print("="*60)

        print("Prediction Completed")

        print("="*60)

        print(

            f"Saved : {OUTPUT_FILE}"

        )

        print("="*60)

    ###########################################################

    def run(self):

        dataframe = self.load_data()

        revenue = self.predict_revenue(

            dataframe

        )

        anomaly = self.predict_anomaly(

            dataframe

        )

        segment = self.predict_segment(

            dataframe

        )

        creative = self.predict_creative(

            dataframe

        )

        final = self.combine(

            revenue,

            anomaly,

            segment,

            creative

        )

        self.save(final)


###############################################################


def main():

    pipeline = PredictionPipeline()

    pipeline.run()


###############################################################

if __name__ == "__main__":

    main()

