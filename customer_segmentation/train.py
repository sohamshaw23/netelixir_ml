"""
train.py

Customer Segmentation Training Pipeline

Steps
-----

1. Load Dataset
2. Preprocess Data
3. Feature Engineering
4. Find Best K
5. Train KMeans
6. Save Model
7. Generate Reports
8. Visualizations
"""

import json
import joblib
import pandas as pd

from .preprocess import preprocess
from .feature_engineering import create_features

from .model import build_model

from .visualization import ClusterVisualizer
from .cluster_analysis import ClusterAnalysis
from .evaluation import ClusterEvaluator

from .config import (

    DATA_PATH,

    MODEL_DIR,

    FEATURE_COLUMNS

)


class CustomerSegmentationTrainer:

    def __init__(self):

        self.analysis = ClusterAnalysis()

        self.visualizer = ClusterVisualizer()

        self.evaluator = ClusterEvaluator()

    #########################################################

    def load_dataset(self):

        print("Loading Dataset...")

        df = pd.read_csv(DATA_PATH)

        print(df.shape)

        return df

    #########################################################

    def prepare(self, dataframe):
        dataframe = dataframe[FEATURE_COLUMNS]
        dataframe = create_features(dataframe)
        dataframe = preprocess(dataframe)
        return dataframe

    #########################################################

    def train(self):

        df = self.load_dataset()

        X = self.prepare(df)

        print("Finding Optimal Clusters...")

        inertia = self.analysis.elbow_method(X)

        silhouette = self.analysis.silhouette_scores(X)

        best_k = self.analysis.best_cluster(

            silhouette

        )

        print(f"Best K = {best_k}")

        model = build_model(best_k)

        labels = model.fit_predict(X)

        X["Cluster"] = labels

        MODEL_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        joblib.dump(

            model,

            MODEL_DIR /

            "kmeans.pkl"

        )

        joblib.dump(

            list(X.columns),

            MODEL_DIR /

            "feature_columns.pkl"

        )

        profile = self.analysis.cluster_profile(X)

        cluster_labels = self.analysis.business_labels(profile)

        with open(
            MODEL_DIR / "cluster_labels.json",
            "w"
        ) as file:
            json.dump(cluster_labels, file, indent=4)

        self.analysis.cluster_size(X)

        self.analysis.recommendations(cluster_labels)

        self.evaluator.evaluate_all(

            X.drop(columns=["Cluster"]),

            labels,

            model

        )

        self.visualizer.visualize_all(

            X.drop(columns=["Cluster"]),

            labels,

            inertia,

            silhouette,

            model.cluster_centers_

        )

        X.to_csv(

            "outputs/customer_segments.csv",

            index=False

        )

        print()

        print("="*50)

        print("Customer Segmentation Completed")

        print("="*50)

        print(f"Optimal Clusters : {best_k}")

        print(f"Customers : {len(X)}")

        print("="*50)


#########################################################


def main():

    trainer = CustomerSegmentationTrainer()

    trainer.train()


#########################################################

if __name__ == "__main__":

    main()

