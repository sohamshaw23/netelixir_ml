"""
shared/logger.py

Universal Logging Utility

Features
--------
✓ Console Logging
✓ File Logging
✓ Log Rotation
✓ Multiple Logger Support
✓ Singleton Logger
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from shared.constants import LOGS_DIR


class LoggerManager:

    def __init__(self):

        LOGS_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        self.loggers = {}

    ##########################################################

    def get_logger(

        self,

        name="MarketingAI",

        logfile=None,

        level=logging.INFO

    ):

        if name in self.loggers:

            return self.loggers[name]

        logger = logging.getLogger(name)

        logger.setLevel(level)

        logger.propagate = False

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",

            "%Y-%m-%d %H:%M:%S"

        )

        ##################################################
        # Console Handler
        ##################################################

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(

            formatter

        )

        logger.addHandler(

            console_handler

        )

        ##################################################
        # File Handler
        ##################################################

        if logfile is None:

            logfile = LOGS_DIR / f"{name.lower()}.log"

        else:

            logfile = Path(logfile)

        logfile.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        file_handler = RotatingFileHandler(

            logfile,

            maxBytes=5 * 1024 * 1024,

            backupCount=5,

            encoding="utf-8"

        )

        file_handler.setFormatter(

            formatter

        )

        logger.addHandler(

            file_handler

        )

        self.loggers[name] = logger

        return logger

    ##########################################################

    def training_logger(self):

        return self.get_logger(

            "Training",

            LOGS_DIR / "training.log"

        )

    ##########################################################

    def inference_logger(self):

        return self.get_logger(

            "Inference",

            LOGS_DIR / "inference.log"

        )

    ##########################################################

    def api_logger(self):

        return self.get_logger(

            "API",

            LOGS_DIR / "api.log"

        )

    ##########################################################

    def error_logger(self):

        return self.get_logger(

            "Error",

            LOGS_DIR / "error.log",

            logging.ERROR

        )


##############################################################

_logger_manager = LoggerManager()


def get_logger(

    name="MarketingAI",

    logfile=None,

    level=logging.INFO

):

    return _logger_manager.get_logger(

        name,

        logfile,

        level

    )


def training_logger():

    return _logger_manager.training_logger()


def inference_logger():

    return _logger_manager.inference_logger()


def api_logger():

    return _logger_manager.api_logger()


def error_logger():

    return _logger_manager.error_logger()

