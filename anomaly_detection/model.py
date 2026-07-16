from sklearn.ensemble import IsolationForest

from .config import (
    RANDOM_STATE,
    CONTAMINATION
)


def build_model():

    model = IsolationForest(

        n_estimators=300,

        contamination=CONTAMINATION,

        max_samples="auto",

        random_state=RANDOM_STATE,

        bootstrap=False

    )

    return model

