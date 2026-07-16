"""
evaluation.py
-------------

Evaluation utilities for K-Means Customer Segmentation
"""

import json
import numpy as np
import pandas as pd

from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score
)

from .config import OUTPUT_DIR


class ClusterEvaluator:

    def __init__(self):

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    ##############################################################

    def evaluate(

        self,

        X,

        labels,

        model

    ):

        metrics = {

            "Number of Clusters":

                len(np.unique(labels)),

            "Silhouette Score":

                float(

                    silhouette_score(

                        X,

                        labels

                    )

                ),

            "Calinski Harabasz":

                float(

                    calinski_harabasz_score(

                        X,

                        labels

                    )

                ),

            "Davies Bouldin":

                float(

                    davies_bouldin_score(

                        X,

                        labels

                    )

                ),

            "Inertia":

                float(

                    model.inertia_

                )

        }

        return metrics

    ##############################################################

    def cluster_distribution(

        self,

        labels

    ):

        unique, counts = np.unique(

            labels,

            return_counts=True

        )

        distribution = {

            int(k): int(v)

            for k, v in zip(unique, counts)

        }

        return distribution

    ##############################################################

    def save_metrics(

        self,

        metrics

    ):

        df = pd.DataFrame(

            metrics.items(),

            columns=[

                "Metric",

                "Value"

            ]

        )

        df.to_csv(

            OUTPUT_DIR /

            "cluster_metrics.csv",

            index=False

        )

    ##############################################################

    def save_distribution(

        self,

        distribution

    ):

        df = pd.DataFrame({

            "Cluster":

                distribution.keys(),

            "Count":

                distribution.values()

        })

        df.to_csv(

            OUTPUT_DIR /

            "cluster_distribution.csv",

            index=False

        )

    ##############################################################

    def save_json(

        self,

        metrics,

        distribution

    ):

        report = {

            "metrics":

                metrics,

            "distribution":

                distribution

        }

        with open(

            OUTPUT_DIR /

            "cluster_report.json",

            "w"

        ) as file:

            json.dump(

                report,

                file,

                indent=4

            )

    ##############################################################

    def print_report(

        self,

        metrics,

        distribution

    ):

        print("\n")

        print("=" * 50)

        print("CUSTOMER SEGMENTATION REPORT")

        print("=" * 50)

        for k, v in metrics.items():

            print(f"{k:<30}: {v}")

        print("\n")

        print("Cluster Distribution")

        print("--------------------")

        for k, v in distribution.items():

            print(

                f"Cluster {k}: {v}"

            )

        print("=" * 50)

    ##############################################################

    def evaluate_all(

        self,

        X,

        labels,

        model

    ):

        metrics = self.evaluate(

            X,

            labels,

            model

        )

        distribution = self.cluster_distribution(

            labels

        )

        self.save_metrics(

            metrics

        )

        self.save_distribution(

            distribution

        )

        self.save_json(

            metrics,

            distribution

        )

        self.print_report(

            metrics,

            distribution

        )

        return metrics
