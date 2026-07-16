"""
Model Evaluation Utilities

This module evaluates the Revenue Drop Risk model and
creates evaluation plots.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    RocCurveDisplay,
    PrecisionRecallDisplay,
)

from .config import OUTPUT_DIR


OUTPUT_DIR.mkdir(exist_ok=True)


class ModelEvaluator:

    def __init__(self, model):

        self.model = model

    def evaluate(self, X_test, y_test):

        y_pred = self.model.predict(X_test)

        y_prob = self.model.predict_proba(X_test)[:, 1]

        metrics = {

            "Accuracy": accuracy_score(y_test, y_pred),

            "Precision": precision_score(y_test, y_pred),

            "Recall": recall_score(y_test, y_pred),

            "F1 Score": f1_score(y_test, y_pred),

            "ROC AUC": roc_auc_score(y_test, y_prob)

        }

        print("\n========== Evaluation ==========\n")

        for key, value in metrics.items():

            print(f"{key:<15}: {value:.4f}")

        print("\nClassification Report\n")

        print(classification_report(y_test, y_pred))

        return metrics

    def confusion(self, X_test, y_test):

        y_pred = self.model.predict(X_test)

        cm = confusion_matrix(y_test, y_pred)

        fig, ax = plt.subplots(figsize=(5,5))

        ax.imshow(cm)

        ax.set_title("Confusion Matrix")

        ax.set_xlabel("Predicted")

        ax.set_ylabel("Actual")

        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):

                ax.text(
                    j,
                    i,
                    cm[i,j],
                    ha="center",
                    va="center"
                )

        plt.savefig(
            OUTPUT_DIR / "confusion_matrix.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

    def roc_curve(self, X_test, y_test):

        RocCurveDisplay.from_estimator(

            self.model,

            X_test,

            y_test

        )

        plt.savefig(

            OUTPUT_DIR/"roc_curve.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    def precision_recall(self, X_test, y_test):

        PrecisionRecallDisplay.from_estimator(

            self.model,

            X_test,

            y_test

        )

        plt.savefig(

            OUTPUT_DIR/"precision_recall_curve.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    def feature_importance(self, X_train):

        importance = self.model.feature_importances_

        names = X_train.columns

        order = importance.argsort()

        plt.figure(figsize=(10,8))

        plt.barh(

            names[order],

            importance[order]

        )

        plt.title("Feature Importance")

        plt.tight_layout()

        plt.savefig(

            OUTPUT_DIR/"feature_importance.png",

            dpi=300

        )

        plt.close()

    def save_metrics(self, metrics):

        import pandas as pd

        df = pd.DataFrame(

            metrics.items(),

            columns=["Metric","Value"]

        )

        df.to_csv(

            OUTPUT_DIR/"evaluation_metrics.csv",

            index=False

        )


def evaluate_model(

    model,

    X_train,

    X_test,

    y_test

):

    evaluator = ModelEvaluator(model)

    metrics = evaluator.evaluate(X_test, y_test)

    evaluator.confusion(X_test, y_test)

    evaluator.roc_curve(X_test, y_test)

    evaluator.precision_recall(X_test, y_test)

    evaluator.feature_importance(X_train)

    evaluator.save_metrics(metrics)

    print("\nEvaluation Completed Successfully.")
