"""
shared/visualization.py

Universal Visualization Utilities

Supports
--------
✓ Confusion Matrix
✓ ROC Curve
✓ Precision-Recall Curve
✓ Feature Importance
✓ Correlation Heatmap
✓ Histogram
✓ Bar Chart
✓ Scatter Plot
✓ Cluster Visualization (PCA)
✓ Save Figures
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    PrecisionRecallDisplay
)


class Visualizer:

    def __init__(self, output_dir="reports/plots"):

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

    ##########################################################

    def save(

        self,

        filename

    ):

        plt.tight_layout()

        plt.savefig(

            self.output_dir / filename,

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    ##########################################################

    def confusion_matrix(

        self,

        model,

        X,

        y,

        filename="confusion_matrix.png"

    ):

        ConfusionMatrixDisplay.from_estimator(

            model,

            X,

            y

        )

        self.save(filename)

    ##########################################################

    def roc_curve(

        self,

        model,

        X,

        y,

        filename="roc_curve.png"

    ):

        RocCurveDisplay.from_estimator(

            model,

            X,

            y

        )

        self.save(filename)

    ##########################################################

    def precision_recall(

        self,

        model,

        X,

        y,

        filename="precision_recall.png"

    ):

        PrecisionRecallDisplay.from_estimator(

            model,

            X,

            y

        )

        self.save(filename)

    ##########################################################

    def feature_importance(

        self,

        importance,

        feature_names,

        filename="feature_importance.png"

    ):

        order = np.argsort(importance)

        plt.figure(figsize=(10,8))

        plt.barh(

            np.array(feature_names)[order],

            np.array(importance)[order]

        )

        plt.title("Feature Importance")

        self.save(filename)

    ##########################################################

    def histogram(

        self,

        values,

        title,

        xlabel,

        filename

    ):

        plt.figure(figsize=(8,5))

        plt.hist(

            values,

            bins=30

        )

        plt.title(title)

        plt.xlabel(xlabel)

        plt.ylabel("Frequency")

        self.save(filename)

    ##########################################################

    def bar_chart(

        self,

        labels,

        values,

        title,

        filename

    ):

        plt.figure(figsize=(8,5))

        plt.bar(

            labels,

            values

        )

        plt.title(title)

        self.save(filename)

    ##########################################################

    def scatter(

        self,

        x,

        y,

        xlabel,

        ylabel,

        filename

    ):

        plt.figure(figsize=(7,6))

        plt.scatter(

            x,

            y,

            alpha=0.7

        )

        plt.xlabel(xlabel)

        plt.ylabel(ylabel)

        self.save(filename)

    ##########################################################

    def correlation_heatmap(

        self,

        dataframe,

        filename="correlation.png"

    ):

        corr = dataframe.corr(

            numeric_only=True

        )

        plt.figure(figsize=(12,10))

        plt.imshow(

            corr,

            interpolation="nearest",

            aspect="auto"

        )

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

        plt.title("Correlation Matrix")

        self.save(filename)

    ##########################################################

    def pca_clusters(

        self,

        X,

        labels,

        filename="clusters.png"

    ):

        pca = PCA(

            n_components=2

        )

        reduced = pca.fit_transform(X)

        plt.figure(figsize=(8,6))

        plt.scatter(

            reduced[:,0],

            reduced[:,1],

            c=labels,

            alpha=0.8

        )

        plt.title("Customer Clusters (PCA)")

        self.save(filename)

    ##########################################################

    def probability_distribution(

        self,

        probabilities,

        filename="probability_distribution.png"

    ):

        self.histogram(

            probabilities,

            "Prediction Probability",

            "Probability",

            filename

        )

    ##########################################################

    def prediction_distribution(

        self,

        predictions,

        filename="prediction_distribution.png"

    ):

        values = pd.Series(

            predictions

        ).value_counts()

        self.bar_chart(

            values.index.astype(str),

            values.values,

            "Prediction Distribution",

            filename

        )


##############################################################

_visualizer = Visualizer()


def get_visualizer():

    return _visualizer

