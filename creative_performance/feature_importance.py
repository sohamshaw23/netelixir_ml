# pyrefly: ignore [missing-import]
"""
feature_importance.py
---------------------

Feature Importance & SHAP Explainability
"""

import pandas as pd
import numpy as np
# pyrefly: ignore [missing-import]
import shap
import matplotlib.pyplot as plt

from .config import OUTPUT_DIR


class FeatureImportance:

    def __init__(self, model):

        self.model = model

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.explainer = shap.TreeExplainer(model)

    ###############################################################

    def catboost_importance(
        self,
        feature_names
    ):

        importance = self.model.get_feature_importance()

        df = pd.DataFrame({

            "Feature": feature_names,

            "Importance": importance

        })

        df = df.sort_values(

            "Importance",

            ascending=False

        )

        df.to_csv(

            OUTPUT_DIR/

            "feature_importance.csv",

            index=False

        )

        return df

    ###############################################################

    def shap_values(

        self,

        X

    ):

        values = self.explainer.shap_values(X)

        return values

    ###############################################################

    def shap_summary(

        self,

        X

    ):

        values = self.shap_values(X)

        plt.figure()

        shap.summary_plot(

            values,

            X,

            show=False

        )

        plt.savefig(

            OUTPUT_DIR/

            "shap_summary.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    ###############################################################

    def shap_bar(

        self,

        X

    ):

        values = self.shap_values(X)

        plt.figure()

        shap.summary_plot(

            values,

            X,

            plot_type="bar",

            show=False

        )

        plt.savefig(

            OUTPUT_DIR/

            "shap_bar.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    ###############################################################

    def waterfall(

        self,

        X

    ):

        values = self.shap_values(X)

        explanation = shap.Explanation(

            values=values[0],

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

            OUTPUT_DIR/

            "waterfall.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    ###############################################################

    def save_shap_values(

        self,

        X

    ):

        values = self.shap_values(X)

        df = pd.DataFrame(

            values,

            columns=X.columns

        )

        df.to_csv(

            OUTPUT_DIR/

            "shap_values.csv",

            index=False

        )

    ###############################################################

    def top_features(

        self,

        feature_names,

        top_n=10

    ):

        importance = self.model.get_feature_importance()

        df = pd.DataFrame({

            "Feature": feature_names,

            "Importance": importance

        })

        df = df.sort_values(

            "Importance",

            ascending=False

        )

        return df.head(top_n)

    ###############################################################

    def explain_all(

        self,

        X,

        feature_names

    ):

        print("Generating Feature Importance...")

        self.catboost_importance(

            feature_names

        )

        print("Generating SHAP Summary...")

        self.shap_summary(X)

        print("Generating SHAP Bar...")

        self.shap_bar(X)

        print("Generating Waterfall Plot...")

        self.waterfall(X)

        print("Saving SHAP Values...")

        self.save_shap_values(X)

        print("Explainability Completed.")

