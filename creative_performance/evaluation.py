"""
evaluation.py
-------------

Evaluation module for Creative Performance Prediction
"""

import json
import pandas as pd

from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score,

    roc_auc_score,

    confusion_matrix,

    classification_report

)

from .config import OUTPUT_DIR


class CreativeEvaluator:

    def __init__(self):

        OUTPUT_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

    ##############################################################

    def evaluate(

        self,

        y_true,

        y_pred,

        probabilities

    ):

        metrics = {

            "Accuracy":

                accuracy_score(

                    y_true,

                    y_pred

                ),

            "Precision":

                precision_score(

                    y_true,

                    y_pred

                ),

            "Recall":

                recall_score(

                    y_true,

                    y_pred

                ),

            "F1 Score":

                f1_score(

                    y_true,

                    y_pred

                ),

            "ROC AUC":

                roc_auc_score(

                    y_true,

                    probabilities

                )

        }

        return metrics

    ##############################################################

    def classification(

        self,

        y_true,

        y_pred

    ):

        report = classification_report(

            y_true,

            y_pred,

            output_dict=True

        )

        return pd.DataFrame(report).transpose()

    ##############################################################

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

    ##############################################################

    def creative_score(

        self,

        probabilities

    ):

        return (

            probabilities * 100

        ).round(2)

    ##############################################################

    def recommendation(

        self,

        scores

    ):

        recommendations = []

        for score in scores:

            if score >= 90:

                recommendations.append(

                    "Launch Immediately"

                )

            elif score >= 75:

                recommendations.append(

                    "Recommended"

                )

            elif score >= 60:

                recommendations.append(

                    "Needs Optimization"

                )

            else:

                recommendations.append(

                    "Redesign Creative"

                )

        return recommendations

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

            OUTPUT_DIR/

            "evaluation_metrics.csv",

            index=False

        )

    ##############################################################

    def save_report(

        self,

        report

    ):

        report.to_csv(

            OUTPUT_DIR/

            "classification_report.csv"

        )

    ##############################################################

    def save_confusion(

        self,

        confusion

    ):

        confusion.to_csv(

            OUTPUT_DIR/

            "confusion_matrix.csv"

        )

    ##############################################################

    def save_json(

        self,

        metrics

    ):

        with open(

            OUTPUT_DIR/

            "evaluation.json",

            "w"

        ) as file:

            json.dump(

                metrics,

                file,

                indent=4

            )

    ##############################################################

    def evaluate_all(

        self,

        y_true,

        y_pred,

        probabilities

    ):

        metrics = self.evaluate(

            y_true,

            y_pred,

            probabilities

        )

        report = self.classification(

            y_true,

            y_pred

        )

        confusion = self.confusion(

            y_true,

            y_pred

        )

        self.save_metrics(metrics)

        self.save_report(report)

        self.save_confusion(confusion)

        self.save_json(metrics)

        print()

        print("="*50)

        print("CREATIVE PERFORMANCE REPORT")

        print("="*50)

        for key, value in metrics.items():

            print(f"{key:<20}: {value:.4f}")

        print("="*50)

        return metrics
