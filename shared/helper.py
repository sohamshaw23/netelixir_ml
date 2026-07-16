"""
shared/helper.py

Common Utility Functions

Features
--------
✓ JSON Read/Write
✓ Joblib Save/Load
✓ Directory Creation
✓ Timestamp
✓ UUID Generator
✓ File Size Formatter
✓ Timer Decorator
✓ Allowed File Validation
"""

import json
import uuid
import time
from pathlib import Path
from functools import wraps

import joblib

from shared.constants import ALLOWED_EXTENSIONS


##############################################################
# Directory
##############################################################

def ensure_directory(path):

    path = Path(path)

    path.mkdir(

        parents=True,

        exist_ok=True

    )

    return path


##############################################################
# JSON
##############################################################

def save_json(

    data,

    filepath

):

    filepath = Path(filepath)

    ensure_directory(

        filepath.parent

    )

    with open(

        filepath,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            data,

            file,

            indent=4

        )


def load_json(filepath):

    with open(

        filepath,

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(file)


##############################################################
# Joblib
##############################################################

def save_object(

    obj,

    filepath

):

    filepath = Path(filepath)

    ensure_directory(

        filepath.parent

    )

    joblib.dump(

        obj,

        filepath

    )


def load_object(filepath):

    return joblib.load(filepath)


##############################################################
# UUID
##############################################################

def generate_uuid():

    return str(

        uuid.uuid4()

    )


##############################################################
# Timestamp
##############################################################

def current_timestamp():

    return time.strftime(

        "%Y-%m-%d %H:%M:%S"

    )


##############################################################
# Allowed File
##############################################################

def allowed_file(filename):

    if "." not in filename:

        return False

    extension = (

        filename

        .rsplit(".", 1)[1]

        .lower()

    )

    return extension in ALLOWED_EXTENSIONS


##############################################################
# File Size
##############################################################

def readable_size(size):

    units = [

        "B",

        "KB",

        "MB",

        "GB",

        "TB"

    ]

    value = float(size)

    for unit in units:

        if value < 1024:

            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


##############################################################
# Timer Decorator
##############################################################

def timer(func):

    @wraps(func)

    def wrapper(

        *args,

        **kwargs

    ):

        start = time.time()

        result = func(

            *args,

            **kwargs

        )

        elapsed = time.time() - start

        print(

            f"{func.__name__}"

            f" completed in "

            f"{elapsed:.2f} sec"

        )

        return result

    return wrapper


##############################################################
# Execution Timer
##############################################################

class Timer:

    def __init__(self):

        self.start = None

    def __enter__(self):

        self.start = time.time()

        return self

    def __exit__(

        self,

        exc_type,

        exc_value,

        traceback

    ):

        elapsed = (

            time.time()

            -

            self.start

        )

        print(

            f"Execution Time: "

            f"{elapsed:.2f} sec"

        )


##############################################################
# Dictionary Merge
##############################################################

def merge_dicts(

    *dictionaries

):

    result = {}

    for dictionary in dictionaries:

        result.update(

            dictionary

        )

    return result


##############################################################
# Safe Float
##############################################################

def safe_float(

    value,

    default=0.0

):

    try:

        return float(value)

    except (

        TypeError,

        ValueError

    ):

        return default


##############################################################
# Safe Integer
##############################################################

def safe_int(

    value,

    default=0

):

    try:

        return int(value)

    except (

        TypeError,

        ValueError

    ):

        return default


##############################################################
# Percentage
##############################################################

def percentage(

    numerator,

    denominator

):

    if denominator == 0:

        return 0.0

    return round(

        numerator

        /

        denominator

        *

        100,

        2

    )

