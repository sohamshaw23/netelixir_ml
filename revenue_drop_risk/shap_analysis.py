"""
SHAP Explainability Module

Generates:
1. SHAP Summary Plot
2. SHAP Bar Plot
3. SHAP Waterfall Plot
4. SHAP Force Plot
5. SHAP Values CSV
"""

from pathlib import Path
import joblib
# pyrefly: ignore [missing-import]
import shap
import pandas as pd
import matplotlib.pyplot as plt

from .config import MODEL_DIR, OUTPUT_DIR


class SHAPAnalyzer:

    def __init__(self):

        self.model = joblib.load(
            MODEL_DIR / "xgboost.pkl"
        )

        self.explainer = shap.TreeExplainer(
            self.model
        )

    # ----------------------------------

    def compute(self, X):

        shap_values = self.explainer.shap_values(X)

        return shap_values

    # ----------------------------------

    def summary_plot(self, X):

        shap_values = self.compute(X)

        plt.figure()

        shap.summary_plot(

            shap_values,

            X,

            show=False

        )

        plt.savefig(

            OUTPUT_DIR / "shap_summary.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    # ----------------------------------

    def bar_plot(self, X):

        shap_values = self.compute(X)

        plt.figure()

        shap.summary_plot(

            shap_values,

            X,

            plot_type="bar",

            show=False

        )

        plt.savefig(

            OUTPUT_DIR / "shap_bar.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    # ----------------------------------

    def waterfall(self, X):

        shap_values = self.compute(X)

        explanation = shap.Explanation(

            values=shap_values[0],

            base_values=self.explainer.expected_value,

            data=X.iloc[0],

            feature_names=X.columns

        )

        plt.figure()

        shap.plots.waterfall(

            explanation,

            show=False

        )

        plt.savefig(

            OUTPUT_DIR / "waterfall.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    # ----------------------------------

    def save_values(self, X):

        shap_values = self.compute(X)

        df = pd.DataFrame(

            shap_values,

            columns=X.columns

        )

        df.to_csv(

            OUTPUT_DIR / "shap_values.csv",

            index=False

        )

    # ----------------------------------

    def feature_importance(self, X):

        shap_values = self.compute(X)

        importance = abs(shap_values).mean(axis=0)

        feature_df = pd.DataFrame({

            "Feature": X.columns,

            "Importance": importance

        })

        feature_df = feature_df.sort_values(

            "Importance",

            ascending=False

        )

        feature_df.to_csv(

            OUTPUT_DIR /

            "feature_importance.csv",

            index=False

        )

        return feature_df

    # ----------------------------------

    def explain(self, X):

        OUTPUT_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        self.summary_plot(X)

        self.bar_plot(X)

        self.waterfall(X)

        self.save_values(X)

        self.feature_importance(X)

        print("SHAP analysis completed.")

