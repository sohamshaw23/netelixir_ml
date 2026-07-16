import logging
import os


def get_logger(log_path):

    os.makedirs(
        os.path.dirname(log_path),
        exist_ok=True
    )

    logger = logging.getLogger("Anomaly")

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        handler = logging.FileHandler(log_path)

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

