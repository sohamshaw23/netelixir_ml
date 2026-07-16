import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

from .config import MODEL_DIR


def preprocess(df):

    df = df.copy()

    import numpy as np
    df = df.fillna(value=np.nan)

    numerical = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    categorical = df.select_dtypes(
        include=["object"]
    ).columns

    num_imp = SimpleImputer(strategy="median")

    cat_imp = SimpleImputer(strategy="most_frequent")

    df[numerical] = num_imp.fit_transform(
        df[numerical]
    )

    df[categorical] = cat_imp.fit_transform(
        df[categorical]
    )

    encoders = {}

    for col in categorical:

        encoder = LabelEncoder()

        df[col] = encoder.fit_transform(df[col])

        encoders[col] = encoder

    scaler = StandardScaler()

    df[numerical] = scaler.fit_transform(
        df[numerical]
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        scaler,
        MODEL_DIR / "scaler.pkl"
    )

    joblib.dump(
        encoders,
        MODEL_DIR / "encoders.pkl"
    )

    return df

