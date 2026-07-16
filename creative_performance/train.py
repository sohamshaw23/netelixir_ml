"""
train.py

Creative Performance Prediction

Pipeline

1. Load Dataset
2. Preprocess
3. Feature Engineering
4. Train CatBoost
5. Evaluate
6. SHAP Explainability
7. Visualization
8. Save Model
"""

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from .config import (
    DATA_PATH,
    MODEL_DIR,
    RANDOM_STATE,
    TEST_SIZE,
    TARGET_COLUMN,
    FEATURE_COLUMNS
)

from .preprocess import preprocess
from .feature_engineering import create_features

from .model import build_model

from .evaluation import CreativeEvaluator
from .visualization import CreativeVisualizer
from .feature_importance import FeatureImportance


class CreativeTrainer:

    def __init__(self):

        self.model = build_model()

        self.evaluator = CreativeEvaluator()

        self.visualizer = CreativeVisualizer()

    ###########################################################

    def load_dataset(self):

        print("Loading Dataset...")

        df = pd.read_csv(DATA_PATH)

        return df

    ###########################################################

    def prepare(self, dataframe):
        dataframe = dataframe[FEATURE_COLUMNS + [TARGET_COLUMN]]
        dataframe = create_features(dataframe)
        dataframe = preprocess(dataframe)
        X = dataframe.drop(columns=[TARGET_COLUMN])
        y = dataframe[TARGET_COLUMN]
        return X, y

    ###########################################################

    def train(self):

        df = self.load_dataset()

        X, y = self.prepare(df)

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=TEST_SIZE,

            random_state=RANDOM_STATE,

            stratify=y

        )

        print("Training CatBoost...")

        self.model.fit(

            X_train,

            y_train

        )

        MODEL_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        self.model.save_model(

            MODEL_DIR /

            "catboost.cbm"

        )

        joblib.dump(

            list(X.columns),

            MODEL_DIR /

            "feature_columns.pkl"

        )

        print("Model Saved.")

        predictions = self.model.predict(

            X_test

        )

        probabilities = self.model.predict_proba(

            X_test

        )[:,1]

        self.evaluator.evaluate_all(

            y_test,

            predictions,

            probabilities

        )

        self.visualizer.visualize_all(

            self.model,

            X_test,

            y_test,

            probabilities,

            predictions,

            X.columns

        )

        explain = FeatureImportance(

            self.model

        )

        explain.explain_all(

            X_test,

            X.columns

        )

        print()

        print("="*50)

        print("Creative Performance Training Completed")

        print("="*50)


############################################################


def main():

    trainer = CreativeTrainer()

    trainer.train()


############################################################

if __name__ == "__main__":

    main()

