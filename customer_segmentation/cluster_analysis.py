"""
cluster_analysis.py

Cluster Analysis Utilities

Features
--------
1. Elbow Method
2. Silhouette Score
3. Optimal Cluster Selection
4. Cluster Profiling
5. Business Labels
6. Recommendations
"""

import json

import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from .config import (
    MAX_CLUSTERS,
    OUTPUT_DIR,
    RANDOM_STATE
)


class ClusterAnalysis:

    def __init__(self):

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    ##############################################################

    def elbow_method(self, X):

        inertia = []

        for k in range(2, MAX_CLUSTERS + 1):

            model = KMeans(

                n_clusters=k,

                random_state=RANDOM_STATE,

                n_init=20

            )

            model.fit(X)

            inertia.append(model.inertia_)

        return inertia

    ##############################################################

    def silhouette_scores(self, X):

        scores = []

        for k in range(2, MAX_CLUSTERS + 1):

            model = KMeans(

                n_clusters=k,

                random_state=RANDOM_STATE,

                n_init=20

            )

            labels = model.fit_predict(X)

            score = silhouette_score(

                X,

                labels

            )

            scores.append(score)

        return scores

    ##############################################################

    def best_cluster(self, scores):

        return scores.index(max(scores)) + 2

    ##############################################################

    def cluster_profile(self, dataframe):

        profile = dataframe.groupby(

            "Cluster"

        ).mean(numeric_only=True)

        profile.to_csv(

            OUTPUT_DIR /

            "cluster_profiles.csv"

        )

        return profile

    ##############################################################

    def cluster_size(self, dataframe):

        summary = dataframe["Cluster"].value_counts()

        summary.to_csv(

            OUTPUT_DIR /

            "cluster_summary.csv"

        )

        return summary

    ##############################################################

    def business_labels(self, profile):

        labels = {}

        revenue_avg = profile["Revenue"].mean()

        spend_avg = profile["Spend"].mean()

        roas_avg = profile["ROAS"].mean()

        for cluster, row in profile.iterrows():

            if (

                row["Revenue"] > revenue_avg

                and

                row["ROAS"] > roas_avg

            ):

                labels[int(cluster)] = "High Value"

            elif (

                row["Spend"] > spend_avg

                and

                row["ROAS"] < roas_avg

            ):

                labels[int(cluster)] = "Budget Drain"

            elif (

                row["Revenue"] < revenue_avg

            ):

                labels[int(cluster)] = "Growth Opportunity"

            else:

                labels[int(cluster)] = "Stable"

        with open(

            OUTPUT_DIR /

            "cluster_labels.json",

            "w"

        ) as file:

            json.dump(

                labels,

                file,

                indent=4

            )

        return labels

    ##############################################################

    def recommendations(self, labels):

        recommendations = {}

        for cluster, label in labels.items():

            if label == "High Value":

                recommendations[cluster] = (

                    "Increase budget and prioritize retention."

                )

            elif label == "Budget Drain":

                recommendations[cluster] = (

                    "Optimize spend and improve creatives."

                )

            elif label == "Growth Opportunity":

                recommendations[cluster] = (

                    "Increase engagement campaigns."

                )

            else:

                recommendations[cluster] = (

                    "Maintain current strategy."

                )

        df = pd.DataFrame({

            "Cluster": recommendations.keys(),

            "Recommendation": recommendations.values()

        })

        df.to_csv(

            OUTPUT_DIR /

            "recommendations.csv",

            index=False

        )

        return recommendations

    ##############################################################

    def analyze(self, dataframe):

        profile = self.cluster_profile(

            dataframe

        )

        self.cluster_size(

            dataframe

        )

        labels = self.business_labels(

            profile

        )

        recommendations = self.recommendations(

            labels

        )

        return {

            "profile": profile,

            "labels": labels,

            "recommendations": recommendations

        }

