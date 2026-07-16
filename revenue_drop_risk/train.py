"""
train.py

Revenue Drop Risk Model Training
--------------------------------
1. Load dataset
2. Preprocess data
3. Feature Engineering
4. Split Train/Test
5. Train XGBoost
6. Evaluate
7. Save Model
"""

from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier

from .preprocess import preprocess
from .feature_engineering import create_features
from .evaluation import evaluate_model

from .config import (
    DATA_PATH,
    MODEL_DIR,
    TARGET_COLUMN,
    RANDOM_STATE,
    TEST_SIZE,
    FEATURE_COLUMNS
)



class RevenueRiskTrainer:

    def __init__(self):

        self.model = None

    # -----------------------------
    # Load Dataset
    # -----------------------------

    def load_dataset(self):

        print("Loading dataset...")

        df = pd.read_csv(DATA_PATH)

        print(f"Dataset Shape : {df.shape}")

        return df

    # -----------------------------
    # Data Preparation
    # -----------------------------

    def prepare_dataset(self, df):
        df = df[FEATURE_COLUMNS + [TARGET_COLUMN]]
        df = create_features(df)
        df = preprocess(df)
        X = df.drop(columns=[TARGET_COLUMN])
        y = df[TARGET_COLUMN]
        return X, y


    # -----------------------------
    # Split Dataset
    # -----------------------------

    def split_data(self, X, y):

        return train_test_split(

            X,
            y,

            test_size=TEST_SIZE,

            random_state=RANDOM_STATE,

            stratify=y

        )

    # -----------------------------
    # Build Model
    # -----------------------------

    def build_model(self):

        return XGBClassifier(

            n_estimators=500,

            learning_rate=0.03,

            max_depth=7,

            subsample=0.8,

            colsample_bytree=0.8,

            gamma=2,

            min_child_weight=3,

            objective="binary:logistic",

            eval_metric="logloss",

            random_state=RANDOM_STATE

        )

    # -----------------------------
    # Train
    # -----------------------------

    def train(self):

        df = self.load_dataset()

        X, y = self.prepare_dataset(df)

        (
            X_train,
            X_test,
            y_train,
            y_test

        ) = self.split_data(X, y)

        self.model = self.build_model()

        print("Training Model...\n")

        self.model.fit(

            X_train,

            y_train

        )

        print("Training Completed.\n")

        evaluate_model(

            self.model,

            X_train,

            X_test,

            y_test

        )

        self.save_model(X_train.columns)

    # -----------------------------
    # Save
    # -----------------------------

    def save_model(self, feature_columns):

        MODEL_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        joblib.dump(

            self.model,

            MODEL_DIR / "xgboost.pkl"

        )

        joblib.dump(

            list(feature_columns),

            MODEL_DIR / "feature_columns.pkl"

        )

        print("Model Saved Successfully.")

        print(MODEL_DIR/"xgboost.pkl")


def main():

    trainer = RevenueRiskTrainer()

    trainer.train()


if __name__ == "__main__":

    main()