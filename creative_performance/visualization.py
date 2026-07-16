"""
visualization.py

Visualization utilities for Creative Performance Model
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.metrics import (
    RocCurveDisplay,
    PrecisionRecallDisplay,
    ConfusionMatrixDisplay
)

from .config import OUTPUT_DIR


class CreativeVisualizer:

    def __init__(self):

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    ###############################################################

    def feature_importance(

        self,

        model,

        feature_names

    ):

        importance = model.feature_importances_

        order = np.argsort(importance)

        plt.figure(figsize=(10,8))

        plt.barh(

            np.array(feature_names)[order],

            importance[order]

        )

        plt.title("Feature Importance")

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR/

            "feature_importance.png",

            dpi=300

        )

        plt.close()

    ###############################################################

    def confusion_matrix(

        self,

        model,

        X,

        y

    ):

        ConfusionMatrixDisplay.from_estimator(

            model,

            X,

            y

        )

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR/

            "confusion_matrix.png",

            dpi=300

        )

        plt.close()

    ###############################################################

    def roc_curve(

        self,

        model,

        X,

        y

    ):

        RocCurveDisplay.from_estimator(

            model,

            X,

            y

        )

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR/

            "roc_curve.png",

            dpi=300

        )

        plt.close()

    ###############################################################

    def precision_recall(

        self,

        model,

        X,

        y

    ):

        PrecisionRecallDisplay.from_estimator(

            model,

            X,

            y

        )

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR/

            "precision_recall.png",

            dpi=300

        )

        plt.close()

    ###############################################################

    def probability_distribution(

        self,

        probabilities

    ):

        plt.figure(figsize=(8,5))

        plt.hist(

            probabilities,

            bins=30

        )

        plt.title(

            "Prediction Probability"

        )

        plt.xlabel("Probability")

        plt.ylabel("Frequency")

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR/

            "probability_distribution.png",

            dpi=300

        )

        plt.close()

    ###############################################################

    def prediction_distribution(

        self,

        predictions

    ):

        values = pd.Series(

            predictions

        ).value_counts()

        plt.figure(figsize=(7,5))

        plt.bar(

            values.index.astype(str),

            values.values

        )

        plt.title(

            "Creative Performance"

        )

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR/

            "prediction_distribution.png",

            dpi=300

        )

        plt.close()

    ###############################################################

    def visualize_all(

        self,

        model,

        X,

        y,

        probabilities,

        predictions,

        feature_names

    ):

        self.feature_importance(

            model,

            feature_names

        )

        self.confusion_matrix(

            model,

            X,

            y

        )

        self.roc_curve(

            model,

            X,

            y

        )

        self.precision_recall(

            model,

            X,

            y

        )

        self.probability_distribution(

            probabilities

        )

        self.prediction_distribution(

            predictions

        )

        print("Visualizations Generated.")
