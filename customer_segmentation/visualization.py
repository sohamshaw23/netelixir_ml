"""
visualization.py
----------------
Visualization utilities for Customer Segmentation
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from .config import OUTPUT_DIR


class ClusterVisualizer:

    def __init__(self):

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    ##########################################################

    def elbow_curve(self, inertia):

        plt.figure(figsize=(8,5))

        plt.plot(

            range(2, len(inertia)+2),

            inertia,

            marker="o"

        )

        plt.title("Elbow Curve")

        plt.xlabel("Number of Clusters")

        plt.ylabel("WCSS")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR /

            "elbow_curve.png",

            dpi=300

        )

        plt.close()

    ##########################################################

    def silhouette_curve(self, scores):

        plt.figure(figsize=(8,5))

        plt.plot(

            range(2, len(scores)+2),

            scores,

            marker="o"

        )

        plt.title("Silhouette Scores")

        plt.xlabel("Clusters")

        plt.ylabel("Score")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR /

            "silhouette_scores.png",

            dpi=300

        )

        plt.close()

    ##########################################################

    def pca_plot(self, X, labels):

        pca = PCA(n_components=2)

        reduced = pca.fit_transform(X)

        plt.figure(figsize=(10,7))

        plt.scatter(

            reduced[:,0],

            reduced[:,1],

            c=labels,

            s=25

        )

        plt.title("Customer Segments (PCA)")

        plt.xlabel("PC1")

        plt.ylabel("PC2")

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR /

            "pca_clusters.png",

            dpi=300

        )

        plt.close()

    ##########################################################

    def tsne_plot(self, X, labels):

        tsne = TSNE(

            n_components=2,

            random_state=42

        )

        reduced = tsne.fit_transform(X)

        plt.figure(figsize=(10,7))

        plt.scatter(

            reduced[:,0],

            reduced[:,1],

            c=labels,

            s=25

        )

        plt.title("Customer Segments (t-SNE)")

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR /

            "tsne_clusters.png",

            dpi=300

        )

        plt.close()

    ##########################################################

    def cluster_distribution(self, labels):

        values = pd.Series(labels).value_counts().sort_index()

        plt.figure(figsize=(7,5))

        plt.bar(

            values.index.astype(str),

            values.values

        )

        plt.title("Cluster Distribution")

        plt.xlabel("Cluster")

        plt.ylabel("Customers")

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR /

            "cluster_distribution.png",

            dpi=300

        )

        plt.close()

    ##########################################################

    def centroid_heatmap(self, centroids):

        plt.figure(figsize=(12,8))

        plt.imshow(

            centroids,

            aspect="auto"

        )

        plt.colorbar()

        plt.xlabel("Features")

        plt.ylabel("Clusters")

        plt.title("Cluster Centroids")

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR /

            "cluster_centroids.png",

            dpi=300

        )

        plt.close()

    ##########################################################

    def visualize_all(

        self,

        X,

        labels,

        inertia,

        silhouette,

        centroids

    ):

        self.elbow_curve(inertia)

        self.silhouette_curve(silhouette)

        self.pca_plot(X, labels)

        self.tsne_plot(X, labels)

        self.cluster_distribution(labels)

        self.centroid_heatmap(centroids)

        print("Visualizations Generated.")
        

