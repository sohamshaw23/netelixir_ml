"""
inference.py
------------

Customer Segmentation Inference Pipeline

Loads trained KMeans model
Predicts customer segments
Generates dashboard-ready summary
"""

import pandas as pd

from .predict import CustomerSegmentPredictor


class CustomerSegmentationInference:

    def __init__(self):

        self.predictor = CustomerSegmentPredictor()

    ##############################################################

    def analyze(self, dataframe):

        result = self.predictor.predict(dataframe)

        summary = self.generate_summary(result)

        response = {

            "summary": summary,

            "segments": self.segment_summary(result),

            "top_customers": self.top_customers(result),

            "results": result.to_dict(
                orient="records"
            )

        }

        return response

    ##############################################################

    def generate_summary(self, dataframe):

        return {

            "total_customers": len(dataframe),

            "number_of_segments":

                dataframe["Cluster"].nunique(),

            "largest_segment":

                int(

                    dataframe["Cluster"]

                    .value_counts()

                    .idxmax()

                ),

            "smallest_segment":

                int(

                    dataframe["Cluster"]

                    .value_counts()

                    .idxmin()

                )

        }

    ##############################################################

    def segment_summary(self, dataframe):

        summary = []

        grouped = dataframe.groupby("Cluster")

        for cluster, group in grouped:

            summary.append({

                "cluster":

                    int(cluster),

                "label":

                    group["Business_Label"]

                    .iloc[0],

                "customers":

                    len(group),

                "average_revenue":

                    float(

                        group["Revenue"]

                        .mean()

                    ),

                "average_spend":

                    float(

                        group["Spend"]

                        .mean()

                    ),

                "average_roas":

                    float(

                        group["ROAS"]

                        .mean()

                    )

            })

        return summary

    ##############################################################

    def top_customers(self, dataframe):

        top = dataframe.sort_values(

            by="Revenue",

            ascending=False

        )

        return top.head(10).to_dict(

            orient="records"

        )


##############################################################


_inference = None


def segment_customers(df: pd.DataFrame):

    """
    Flask API Entry Point
    """

    global _inference

    if _inference is None:

        _inference = CustomerSegmentationInference()

    return _inference.analyze(df)


##############################################################

if __name__ == "__main__":

    sample = pd.read_csv(

        "../data/processed/test.csv"

    )

    result = segment_customers(sample)

    print(result["summary"])
