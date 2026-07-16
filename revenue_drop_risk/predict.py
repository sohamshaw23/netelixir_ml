"""
Revenue Drop Risk Prediction

Loads trained model
Preprocesses new data
Generates predictions
Exports results
"""

from pathlib import Path
import joblib
import pandas as pd

from .config import (
    MODEL_DIR,
    OUTPUT_DIR,
    FEATURE_COLUMNS
)


from .preprocess import preprocess
from .feature_engineering import create_features


MODEL_PATH = MODEL_DIR / "xgboost.pkl"


class RevenueRiskPredictor:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

    def prepare(self, dataframe):
        df = dataframe[FEATURE_COLUMNS]
        df = create_features(df)
        df = preprocess(df)
        return df

    def predict(self, dataframe):

        processed = self.prepare(dataframe)

        predictions = self.model.predict(processed)

        probability = self.model.predict_proba(processed)[:, 1]

        result = dataframe.copy()

        result["Revenue_Drop_Risk"] = predictions

        result["Risk_Probability"] = probability

        result["Risk_Level"] = probability_to_label(probability)

        return result


def probability_to_label(probability):

    labels = []

    for p in probability:

        if p >= 0.80:
            labels.append("Critical")

        elif p >= 0.60:
            labels.append("High")

        elif p >= 0.40:
            labels.append("Medium")

        else:
            labels.append("Low")

    return labels


def save_predictions(df):

    OUTPUT_DIR.mkdir(exist_ok=True)

    output_path = OUTPUT_DIR / "revenue_risk_predictions.csv"

    df.to_csv(output_path, index=False)

    print(f"Saved predictions to {output_path}")


if __name__ == "__main__":

    sample = pd.read_csv("../data/processed/test.csv")

    predictor = RevenueRiskPredictor()

    results = predictor.predict(sample)

    save_predictions(results)

    print(results.head())

