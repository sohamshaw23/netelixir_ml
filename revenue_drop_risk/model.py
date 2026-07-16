from xgboost import XGBClassifier


def build_model():

    model = XGBClassifier(

        n_estimators=400,

        learning_rate=0.05,

        max_depth=7,

        subsample=0.8,

        colsample_bytree=0.8,

        objective="binary:logistic",

        eval_metric="logloss",

        random_state=42

    )

    return model

