"""
train.py
---------

Training script for Isolation Forest

Pipeline

1. Load Dataset
2. Preprocess
3. Feature Engineering
4. Train Isolation Forest
5. Save Model
6. Evaluate
7. Generate Visualizations
"""

import joblib
import pandas as pd

from .preprocess import preprocess
from .feature_engineering import create_features

from .model import build_model

from .evaluation import AnomalyEvaluator

from .visualization import AnomalyVisualizer

from .config import (

    DATA_PATH,

    MODEL_DIR,

    FEATURE_COLUMNS

)


class AnomalyTrainer:

    def __init__(self):

        self.model = build_model()

    ######################################################

    def load_dataset(self):

        print("Loading Dataset...")

        df = pd.read_csv(DATA_PATH)

        print(df.shape)

        return df

    ######################################################

    def prepare(self, dataframe):
        dataframe = dataframe[FEATURE_COLUMNS]
        dataframe = create_features(dataframe)
        dataframe = preprocess(dataframe)
        return dataframe

    ######################################################

    def train(self):

        df = self.load_dataset()

        processed = self.prepare(df)

        print("Training Isolation Forest...")

        self.model.fit(processed)

        print("Training Completed.")

        MODEL_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        joblib.dump(

            self.model,

            MODEL_DIR /

            "isolation_forest.pkl"

        )

        joblib.dump(

            list(processed.columns),

            MODEL_DIR /

            "feature_columns.pkl"

        )

        print("Model Saved.")

        labels = self.model.predict(

            processed

        )

        scores = self.model.decision_function(

            processed

        )

        evaluator = AnomalyEvaluator()

        evaluator.evaluate_all(

            processed,

            labels,

            scores

        )

        visualizer = AnomalyVisualizer()

        visualizer.visualize_all(

            processed,

            scores,

            labels

        )

        print(

            "\nAnomaly Detection Pipeline Completed."

        )


###########################################################


def main():

    trainer = AnomalyTrainer()

    trainer.train()


###########################################################

if __name__ == "__main__":

    main()

