"""
shared/validation.py

Universal Validation Utilities

Supports
--------
✓ File validation
✓ Dataset validation
✓ Required columns
✓ Missing values
✓ Duplicate detection
✓ Numeric range validation
✓ Data type validation
"""

from pathlib import Path

import pandas as pd

from shared.constants import (
    ALLOWED_EXTENSIONS,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES
)


class DataValidator:

    def __init__(self):
        pass

    ##########################################################
    # File Validation
    ##########################################################

    def validate_file(self, filepath):

        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(
                f"{filepath} does not exist."
            )

        extension = filepath.suffix.lower().replace(".", "")

        if extension not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return True

    ##########################################################
    # Empty Dataset
    ##########################################################

    def validate_dataset(self, dataframe):

        if dataframe is None:
            raise ValueError("Dataset is None.")

        if dataframe.empty:
            raise ValueError("Dataset is empty.")

        return True

    ##########################################################
    # Required Columns
    ##########################################################

    def validate_columns(

        self,

        dataframe,

        required_columns

    ):

        missing = [

            column

            for column in required_columns

            if column not in dataframe.columns

        ]

        if missing:

            raise ValueError(

                f"Missing columns: {missing}"

            )

        return True

    ##########################################################
    # Missing Values
    ##########################################################

    def missing_values(

        self,

        dataframe

    ):

        missing = dataframe.isnull().sum()

        return missing[missing > 0]

    ##########################################################
    # Duplicate Rows
    ##########################################################

    def duplicate_rows(

        self,

        dataframe

    ):

        return dataframe.duplicated().sum()

    ##########################################################
    # Data Types
    ##########################################################

    def validate_dtypes(

        self,

        dataframe

    ):

        numeric = [

            col

            for col in NUMERIC_FEATURES

            if col in dataframe.columns

        ]

        categorical = [

            col

            for col in CATEGORICAL_FEATURES

            if col in dataframe.columns

        ]

        errors = {}

        for column in numeric:

            if not pd.api.types.is_numeric_dtype(

                dataframe[column]

            ):

                errors[column] = "Expected Numeric"

        for column in categorical:

            if not (

                pd.api.types.is_string_dtype(

                    dataframe[column]

                )

                or

                pd.api.types.is_object_dtype(

                    dataframe[column]

                )

            ):

                errors[column] = "Expected String"

        return errors

    ##########################################################
    # Numeric Range Validation
    ##########################################################

    def validate_range(

        self,

        dataframe,

        column,

        minimum=None,

        maximum=None

    ):

        if column not in dataframe.columns:

            return False

        if minimum is not None:

            if (

                dataframe[column] < minimum

            ).any():

                return False

        if maximum is not None:

            if (

                dataframe[column] > maximum

            ).any():

                return False

        return True

    ##########################################################
    # Summary
    ##########################################################

    def summary(

        self,

        dataframe

    ):

        return {

            "Rows":

                len(dataframe),

            "Columns":

                len(dataframe.columns),

            "Missing Values":

                int(

                    dataframe

                    .isnull()

                    .sum()

                    .sum()

                ),

            "Duplicate Rows":

                int(

                    dataframe

                    .duplicated()

                    .sum()

                )

        }

    ##########################################################
    # Full Validation
    ##########################################################

    def validate_all(

        self,

        dataframe,

        required_columns=None

    ):

        self.validate_dataset(

            dataframe

        )

        if required_columns:

            self.validate_columns(

                dataframe,

                required_columns

            )

        dtype_errors = self.validate_dtypes(

            dataframe

        )

        report = {

            "summary":

                self.summary(dataframe),

            "missing":

                self.missing_values(

                    dataframe

                ).to_dict(),

            "duplicates":

                self.duplicate_rows(

                    dataframe

                ),

            "dtype_errors":

                dtype_errors

        }

        return report


##############################################################

_validator = DataValidator()


def validate_file(filepath):

    return _validator.validate_file(filepath)


def validate_dataset(dataframe):

    return _validator.validate_dataset(dataframe)


def validate_columns(

    dataframe,

    required_columns

):

    return _validator.validate_columns(

        dataframe,

        required_columns

    )


def validate_all(

    dataframe,

    required_columns=None

):

    return _validator.validate_all(

        dataframe,

        required_columns

    )

