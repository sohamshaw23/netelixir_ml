"""
inference.py
------------

Creative Performance Inference Pipeline

Generates dashboard-ready JSON
"""

import pandas as pd

from .predict import CreativePerformancePredictor


class CreativePerformanceInference:

    def __init__(self):

        self.predictor = CreativePerformancePredictor()

    ##############################################################

    def analyze(self, dataframe):

        result = self.predictor.predict(dataframe)

        response = {

            "summary": self.summary(result),

            "recommendations": self.recommendation_summary(result),

            "top_creatives": self.top_creatives(result),

            "results": result.to_dict(
                orient="records"
            )

        }

        return response

    ##############################################################

    def summary(self, dataframe):

        return {

            "total_creatives": len(dataframe),

            "average_score":

                float(

                    dataframe["Performance_Score"]

                    .mean()

                ),

            "highest_score":

                float(

                    dataframe["Performance_Score"]

                    .max()

                ),

            "lowest_score":

                float(

                    dataframe["Performance_Score"]

                    .min()

                )

        }

    ##############################################################

    def recommendation_summary(

        self,

        dataframe

    ):

        grouped = (

            dataframe

            ["Recommendation"]

            .value_counts()

            .to_dict()

        )

        return grouped

    ##############################################################

    def top_creatives(

        self,

        dataframe

    ):

        top = dataframe.sort_values(

            by="Performance_Score",

            ascending=False

        )

        return top.head(10).to_dict(

            orient="records"

        )


##############################################################


_inference = None


def predict_creative_performance(

    df: pd.DataFrame

):

    """
    Flask API Entry Point
    """

    global _inference

    if _inference is None:

        _inference = CreativePerformanceInference()

    return _inference.analyze(df)


##############################################################

if __name__ == "__main__":

    sample = pd.read_csv(

        "../data/processed/test.csv"

    )

    response = predict_creative_performance(sample)

    print(response["summary"])
