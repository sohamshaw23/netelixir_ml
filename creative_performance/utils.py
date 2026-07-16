import logging
import os


def get_logger(path):

    os.makedirs(

        os.path.dirname(path),

        exist_ok=True

    )

    logger = logging.getLogger(

        "CreativePerformance"

    )

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        handler = logging.FileHandler(path)

        formatter = logging.Formatter(

            "%(asctime)s"

            " - "

            "%(levelname)s"

            " - "

            "%(message)s"

        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger

