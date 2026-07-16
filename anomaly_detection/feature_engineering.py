import numpy as np


def create_features(df):

    df = df.copy()

    df["Revenue_per_Click"] = (

        df["Revenue"]

        /

        (df["Clicks"] + 1)

    )

    df["Conversion_Rate"] = (

        df["Conversions"]

        /

        (df["Clicks"] + 1)

    )

    df["Spend_per_Conversion"] = (

        df["Spend"]

        /

        (df["Conversions"] + 1)

    )

    df["Revenue_to_Spend"] = (

        df["Revenue"]

        /

        (df["Spend"] + 1)

    )

    df["CTR_ROAS"] = (

        df["CTR"]

        *

        df["ROAS"]

    )

    df["Log_Spend"] = np.log1p(df["Spend"])

    df["Log_Revenue"] = np.log1p(df["Revenue"])

    return df
