"""
evaluate.py

Master Evaluation Script

Evaluates:
1. Revenue Drop Risk
2. Anomaly Detection
3. Customer Segmentation
4. Creative Performance

Usage
-----
python scripts/evaluate.py
"""

import json
import time
from pathlib import Path

import pandas as pd

from revenue_drop_risk.train import RevenueTrainer
from anomaly_detection.train import AnomalyTrainer
from customer_segmentation.train import CustomerSegmentationTrainer
from creative_performance.train import CreativeTrainer


##############################################################

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "reports"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REPORT_FILE = OUTPUT_DIR / "evaluation_report.json"

##############################################################


class EvaluationPipeline:

    def __init__(self):

        self.results = {}

        self.start = time.time()

    ##########################################################

    def separator(self):

        print("=" * 70)

    ##########################################################

    def evaluate_revenue(self):

        self.separator()

        print("Evaluating Revenue Drop Risk...")

        trainer = RevenueTrainer()

        metrics = trainer.train()

        self.results["Revenue Drop Risk"] = {

            "Status": "Completed",

            "Metrics": str(metrics)

        }

    ##########################################################

    def evaluate_anomaly(self):

        self.separator()

        print("Evaluating Anomaly Detection...")

        trainer = AnomalyTrainer()

        metrics = trainer.train()

        self.results["Anomaly Detection"] = {

            "Status": "Completed",

            "Metrics": str(metrics)

        }

    ##########################################################

    def evaluate_segmentation(self):

        self.separator()

        print("Evaluating Customer Segmentation...")

        trainer = CustomerSegmentationTrainer()

        metrics = trainer.train()

        self.results["Customer Segmentation"] = {

            "Status": "Completed",

            "Metrics": str(metrics)

        }

    ##########################################################

    def evaluate_creative(self):

        self.separator()

        print("Evaluating Creative Performance...")

        trainer = CreativeTrainer()

        metrics = trainer.train()

        self.results["Creative Performance"] = {

            "Status": "Completed",

            "Metrics": str(metrics)

        }

    ##########################################################

    def save_report(self):

        with open(

            REPORT_FILE,

            "w"

        ) as file:

            json.dump(

                self.results,

                file,

                indent=4

            )

    ##########################################################

    def summary(self):

        elapsed = time.time() - self.start

        self.separator()

        print()

        print("Evaluation Completed")

        print()

        print(f"Report : {REPORT_FILE}")

        print(f"Time : {elapsed:.2f} sec")

        self.separator()

    ##########################################################

    def run(self):

        self.evaluate_revenue()

        self.evaluate_anomaly()

        self.evaluate_segmentation()

        self.evaluate_creative()

        self.save_report()

        self.summary()


##############################################################


def main():

    pipeline = EvaluationPipeline()

    pipeline.run()


##############################################################

if __name__ == "__main__":

    main()

