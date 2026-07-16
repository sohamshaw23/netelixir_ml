"""
shared/data_loader.py

Universal Data Loader

Supports:
- CSV
- Excel (.xlsx/.xls)
- Automatic file detection
- Dataset validation
- Train/Test Split
- Dataset summary
"""

from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split

from shared.constants import (

    RANDOM_STATE,

    TEST_SIZE

)


class DataLoader:

    def __init__(self):

        self.data = None

    ##########################################################

    def load(self, filepath):

        filepath = Path(filepath)

        if not filepath.exists():

            raise FileNotFoundError(

                f"{filepath} not found."

            )

        extension = filepath.suffix.lower()

        if extension == ".csv":

            self.data = pd.read_csv(filepath)

        elif extension in [".xlsx", ".xls"]:

            self.data = pd.read_excel(filepath)

        else:

            raise ValueError(

                "Unsupported file type."

            )

        return self.data

    ##########################################################

    def save(

        self,

        dataframe,

        filepath

    ):

        filepath = Path(filepath)

        filepath.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        extension = filepath.suffix.lower()

        if extension == ".csv":

            dataframe.to_csv(

                filepath,

                index=False

            )

        elif extension in [

            ".xlsx",

            ".xls"

        ]:

            dataframe.to_excel(

                filepath,

                index=False

            )

        else:

            raise ValueError(

                "Unsupported file type."

            )

    ##########################################################

    def summary(

        self,

        dataframe=None

    ):

        if dataframe is None:

            dataframe = self.data

        return {

            "rows":

                len(dataframe),

            "columns":

                len(dataframe.columns),

            "missing":

                int(

                    dataframe

                    .isnull()

                    .sum()

                    .sum()

                ),

            "duplicates":

                int(

                    dataframe

                    .duplicated()

                    .sum()

                ),

            "memory_mb":

                round(

                    dataframe.memory_usage(

                        deep=True

                    ).sum()

                    / 1024**2,

                    2

                )

        }

    ##########################################################

    def validate(

        self,

        dataframe,

        required_columns=None

    ):

        if dataframe.empty:

            raise ValueError(

                "Dataset is empty."

            )

        if required_columns:

            missing = [

                col

                for col in required_columns

                if col not in dataframe.columns

            ]

            if missing:

                raise ValueError(

                    f"Missing columns: {missing}"

                )

        return True

    ##########################################################

    def train_test(

        self,

        dataframe,

        target

    ):

        X = dataframe.drop(

            columns=[target]

        )

        y = dataframe[target]

        return train_test_split(

            X,

            y,

            test_size=TEST_SIZE,

            random_state=RANDOM_STATE,

            stratify=y

        )

    ##########################################################

    def numeric_columns(

        self,

        dataframe

    ):

        return list(

            dataframe.select_dtypes(

                include="number"

            ).columns

        )

    ##########################################################

    def categorical_columns(

        self,

        dataframe

    ):

        return list(

            dataframe.select_dtypes(

                exclude="number"

            ).columns

        )

    ##########################################################

    def info(

        self,

        dataframe=None

    ):

        if dataframe is None:

            dataframe = self.data

        print()

        print("=" * 60)

        print("DATASET INFORMATION")

        print("=" * 60)

        print(

            f"Rows : {len(dataframe)}"

        )

        print(

            f"Columns : {len(dataframe.columns)}"

        )

        print(

            f"Missing : {dataframe.isnull().sum().sum()}"

        )

        print(

            f"Duplicates : {dataframe.duplicated().sum()}"

        )

        print("=" * 60)


##############################################################

_loader = DataLoader()


def load_dataframe(filepath):

    return _loader.load(filepath)


def save_dataframe(

    dataframe,

    filepath

):

    _loader.save(

        dataframe,

        filepath

    )


def dataset_summary(

    dataframe

):

    return _loader.summary(

        dataframe

    )


def split_dataset(

    dataframe,

    target

):

    return _loader.train_test(

        dataframe,

        target

    )

