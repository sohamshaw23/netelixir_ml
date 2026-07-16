"""
shared/metrics.py

Universal Evaluation Metrics

Supports
--------
✓ Classification
✓ Regression
✓ Clustering
✓ Anomaly Detection
"""

import numpy as np
import pandas as pd

from sklearn.metrics import (

    accuracy_score,
    precision_score,
    recall_score,
    f1_score,

    roc_auc_score,

    mean_absolute_error,
    mean_squared_error,
    r2_score,

    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score,

    confusion_matrix,
    classification_report
)


class Metrics:

    ##########################################################
    # Classification
    ##########################################################

    def classification(

        self,

        y_true,

        y_pred,

        probabilities=None

    ):

        results = {

            "Accuracy":

                accuracy_score(

                    y_true,

                    y_pred

                ),

            "Precision":

                precision_score(

                    y_true,

                    y_pred,

                    zero_division=0

                ),

            "Recall":

                recall_score(

                    y_true,

                    y_pred,

                    zero_division=0

                ),

            "F1 Score":

                f1_score(

                    y_true,

                    y_pred,

                    zero_division=0

                )

        }

        if probabilities is not None:

            results["ROC AUC"] = roc_auc_score(

                y_true,

                probabilities

            )

        return results

    ##########################################################
    # Regression
    ##########################################################

    def regression(

        self,

        y_true,

        y_pred

    ):

        rmse = np.sqrt(

            mean_squared_error(

                y_true,

                y_pred

            )

        )

        return {

            "MAE":

                mean_absolute_error(

                    y_true,

                    y_pred

                ),

            "RMSE":

                rmse,

            "R2":

                r2_score(

                    y_true,

                    y_pred

                )

        }

    ##########################################################
    # Clustering
    ##########################################################

    def clustering(

        self,

        X,

        labels,

        model=None

    ):

        results = {

            "Silhouette":

                silhouette_score(

                    X,

                    labels

                ),

            "Calinski Harabasz":

                calinski_harabasz_score(

                    X,

                    labels

                ),

            "Davies Bouldin":

                davies_bouldin_score(

                    X,

                    labels

                )

        }

        if model is not None and hasattr(

            model,

            "inertia_"

        ):

            results["Inertia"] = model.inertia_

        return results

    ##########################################################
    # Isolation Forest
    ##########################################################

    def anomaly(

        self,

        predictions

    ):

        predictions = np.asarray(

            predictions

        )

        anomalies = np.sum(

            predictions == -1

        )

        normal = np.sum(

            predictions == 1

        )

        return {

            "Total":

                len(predictions),

            "Normal":

                int(normal),

            "Anomalies":

                int(anomalies),

            "Anomaly Percentage":

                round(

                    anomalies

                    /

                    len(predictions)

                    * 100,

                    2

                )

        }

    ##########################################################
    # Classification Report
    ##########################################################

    def report(

        self,

        y_true,

        y_pred

    ):

        return pd.DataFrame(

            classification_report(

                y_true,

                y_pred,

                output_dict=True,

                zero_division=0

            )

        ).transpose()

    ##########################################################
    # Confusion Matrix
    ##########################################################

    def confusion(

        self,

        y_true,

        y_pred

    ):

        cm = confusion_matrix(

            y_true,

            y_pred

        )

        return pd.DataFrame(cm)

    ##########################################################
    # Save Metrics
    ##########################################################

    def save(

        self,

        metrics,

        filepath

    ):

        pd.DataFrame(

            metrics.items(),

            columns=[

                "Metric",

                "Value"

            ]

        ).to_csv(

            filepath,

            index=False

        )


############################################################

_metrics = Metrics()


def classification_metrics(

    y_true,

    y_pred,

    probabilities=None

):

    return _metrics.classification(

        y_true,

        y_pred,

        probabilities

    )


def regression_metrics(

    y_true,

    y_pred

):

    return _metrics.regression(

        y_true,

        y_pred

    )


def clustering_metrics(

    X,

    labels,

    model=None

):

    return _metrics.clustering(

        X,

        labels,

        model

    )


def anomaly_metrics(

    predictions

):

    return _metrics.anomaly(

        predictions

    )

