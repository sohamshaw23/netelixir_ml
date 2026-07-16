# pyrefly: ignore [missing-import]
from catboost import CatBoostClassifier

from .config import RANDOM_STATE


def build_model():

    model = CatBoostClassifier(

        iterations=500,

        learning_rate=0.05,

        depth=8,

        loss_function="Logloss",

        eval_metric="AUC",

        random_seed=RANDOM_STATE,

        verbose=False

    )

    return model

