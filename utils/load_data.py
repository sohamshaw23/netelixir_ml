import pandas as pd
import sys
import os
import pandas as pd

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from config import (
    GOOGLE_DATA_PATH,
    META_DATA_PATH,
    BING_DATA_PATH
)

from utils.validate import validate_dataset


def load_data():
    google_df = pd.read_csv(GOOGLE_DATA_PATH)
    meta_df = pd.read_csv(META_DATA_PATH)
    bing_df = pd.read_csv(BING_DATA_PATH)

    return google_df, meta_df, bing_df


if __name__ == "__main__":
    google_df, meta_df, bing_df = load_data()

    validate_dataset(google_df, "GOOGLE")
    validate_dataset(meta_df, "META")
    validate_dataset(bing_df, "BING")