"""
Inference Pipeline
"""

import pandas as pd

from .predict import RevenueRiskPredictor


predictor = None


def predict_revenue_risk(df: pd.DataFrame):

    global predictor

    if predictor is None:

        predictor = RevenueRiskPredictor()

    results = predictor.predict(df)


    summary = {

        "total_campaigns": len(results),

        "high_risk": int(
            (results["Risk_Level"] == "High").sum()
        ),

        "critical_risk": int(
            (results["Risk_Level"] == "Critical").sum()
        ),

        "average_probability":
            float(results["Risk_Probability"].mean()),

        "results":
            results.to_dict(orient="records")

    }

    return summary

