"""
visualization.py
----------------
Visualization utilities for Anomaly Detection

Generates:
1. Anomaly Distribution
2. PCA Visualization
3. t-SNE Visualization
4. Boxplots
5. Feature Histograms
6. Correlation Heatmap
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from .config import OUTPUT_DIR


class AnomalyVisualizer:

    def __init__(self):

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    ############################################################

    def anomaly_distribution(self, scores):

        plt.figure(figsize=(10,6))

        plt.hist(
            scores,
            bins=40
        )

        plt.title("Anomaly Score Distribution")

        plt.xlabel("Score")

        plt.ylabel("Frequency")

        plt.tight_layout()

        plt.savefig(
            OUTPUT_DIR /
            "anomaly_distribution.png",
            dpi=300
        )

        plt.close()

    ############################################################

    def pca_plot(self, X, labels):

        pca = PCA(n_components=2)

        reduced = pca.fit_transform(X)

        plt.figure(figsize=(10,8))

        plt.scatter(

            reduced[:,0],

            reduced[:,1],

            c=labels,

            s=20

        )

        plt.title("PCA Projection")

        plt.xlabel("PC1")

        plt.ylabel("PC2")

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR /

            "pca_visualization.png",

            dpi=300

        )

        plt.close()

    ############################################################

    def tsne_plot(self, X, labels):

        tsne = TSNE(

            n_components=2,

            random_state=42

        )

        reduced = tsne.fit_transform(X)

        plt.figure(figsize=(10,8))

        plt.scatter(

            reduced[:,0],

            reduced[:,1],

            c=labels,

            s=20

        )

        plt.title("t-SNE Projection")

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR /

            "tsne_visualization.png",

            dpi=300

        )

        plt.close()

    ############################################################

    def boxplots(self, dataframe):

        numerical = dataframe.select_dtypes(

            include=np.number

        ).columns

        for col in numerical:

            plt.figure(figsize=(7,5))

            dataframe.boxplot(column=col)

            plt.title(col)

            plt.tight_layout()

            plt.savefig(

                OUTPUT_DIR /

                f"{col}_boxplot.png",

                dpi=300

            )

            plt.close()

    ############################################################

    def feature_histograms(self, dataframe):

        numerical = dataframe.select_dtypes(

            include=np.number

        ).columns

        for col in numerical:

            plt.figure(figsize=(7,5))

            dataframe[col].hist(

                bins=30

            )

            plt.title(col)

            plt.tight_layout()

            plt.savefig(

                OUTPUT_DIR /

                f"{col}_histogram.png",

                dpi=300

            )

            plt.close()

    ############################################################

    def correlation_heatmap(self, dataframe):

        corr = dataframe.corr(numeric_only=True)

        plt.figure(figsize=(12,10))

        plt.imshow(corr)

        plt.xticks(

            range(len(corr.columns)),

            corr.columns,

            rotation=90

        )

        plt.yticks(

            range(len(corr.columns)),

            corr.columns

        )

        plt.colorbar()

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR /

            "correlation_heatmap.png",

            dpi=300

        )

        plt.close()

    ############################################################

    def visualize_all(

        self,

        dataframe,

        anomaly_scores,

        labels

    ):

        self.anomaly_distribution(

            anomaly_scores

        )

        self.pca_plot(

            dataframe,

            labels

        )

        self.tsne_plot(

            dataframe,

            labels

        )

        self.boxplots(

            dataframe

        )

        self.feature_histograms(

            dataframe

        )

        self.correlation_heatmap(

            dataframe

        )

        print("Visualizations Generated Successfully.")

