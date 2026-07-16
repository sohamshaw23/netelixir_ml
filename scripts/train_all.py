"""
train_all.py

Master Training Script

Pipeline
--------
1. Revenue Drop Risk (XGBoost)
2. Anomaly Detection (Isolation Forest)
3. Customer Segmentation (KMeans)
4. Creative Performance (CatBoost)

Usage
-----
python scripts/train_all.py
"""

import time
import traceback
from pathlib import Path

##############################################################

from revenue_drop_risk.train import RevenueRiskTrainer

from anomaly_detection.train import AnomalyTrainer

from customer_segmentation.train import CustomerSegmentationTrainer

from creative_performance.train import CreativeTrainer

##############################################################


class TrainingPipeline:

    def __init__(self):

        self.start = time.time()

    ##########################################################

    def separator(self):

        print("\n")

        print("=" * 70)

    ##########################################################

    def train_revenue(self):

        self.separator()

        print("Training Revenue Drop Risk Model")

        trainer = RevenueRiskTrainer()


        trainer.train()

        print("Revenue Model Completed")

    ##########################################################

    def train_anomaly(self):

        self.separator()

        print("Training Anomaly Detection Model")

        trainer = AnomalyTrainer()

        trainer.train()

        print("Anomaly Model Completed")

    ##########################################################

    def train_segmentation(self):

        self.separator()

        print("Training Customer Segmentation")

        trainer = CustomerSegmentationTrainer()

        trainer.train()

        print("Segmentation Completed")

    ##########################################################

    def train_creative(self):

        self.separator()

        print("Training Creative Performance")

        trainer = CreativeTrainer()

        trainer.train()

        print("Creative Model Completed")

    ##########################################################

    def summary(self):

        elapsed = time.time() - self.start

        self.separator()

        print("ALL MODELS TRAINED SUCCESSFULLY")

        print(f"Total Time : {elapsed:.2f} sec")

        self.separator()

    ##########################################################

    def run(self):

        try:

            self.train_revenue()

            self.train_anomaly()

            self.train_segmentation()

            self.train_creative()

            self.summary()

        except Exception:

            print()

            print("Training Failed")

            traceback.print_exc()


##############################################################


def main():

    pipeline = TrainingPipeline()

    pipeline.run()


##############################################################

if __name__ == "__main__":

    main()