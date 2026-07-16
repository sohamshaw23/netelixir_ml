"""
predict.py
----------

Creative Performance Prediction Module

Loads trained CatBoost model
Preprocesses new creative data
Predicts performance
Ranks creatives
Generates recommendations
"""

import joblib
import pandas as pd

from .preprocess import preprocess
from .feature_engineering import create_features

from .config import (
    MODEL_DIR,
    OUTPUT_DIR,
    FEATURE_COLUMNS
)


MODEL_PATH = MODEL_DIR / "catboost.cbm"


class CreativePerformancePredictor:

    def __init__(self):

        from catboost import CatBoostClassifier

        self.model = CatBoostClassifier()

        self.model.load_model(str(MODEL_PATH))



    ###############################################################

    def prepare(self, dataframe):
        dataframe = dataframe[FEATURE_COLUMNS]
        dataframe = create_features(dataframe)
        dataframe = preprocess(dataframe)
        return dataframe

    ###############################################################

    def predict(self, dataframe):

        processed = self.prepare(dataframe)

        predictions = self.model.predict(processed)

        probabilities = self.model.predict_proba(processed)[:, 1]

        scores = (probabilities * 100).round(2)

        result = dataframe.copy()

        result["Prediction"] = predictions

        result["Probability"] = probabilities

        result["Performance_Score"] = scores

        result["Recommendation"] = self.recommend(scores)

        result["Rank"] = (
            result["Performance_Score"]
            .rank(ascending=False, method="dense")
            .astype(int)
        )

        result = result.sort_values("Rank")

        return result

    ###############################################################

    def recommend(self, scores):

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

    ###############################################################

    def save(self, dataframe):

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        dataframe.to_csv(
            OUTPUT_DIR /
            "creative_scores.csv",
            index=False
        )

        print("Creative Scores Saved Successfully.")


###############################################################


if __name__ == "__main__":

    sample = pd.read_csv(
        "../data/processed/test.csv"
    )

    predictor = CreativePerformancePredictor()

    result = predictor.predict(sample)

    predictor.save(result)

    print(result.head())