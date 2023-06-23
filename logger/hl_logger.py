# pylint: disable= R0903 #Too few public methods

"""Logger Module
"""

import logging
import os
from logging import Logger, config

from conflicts_check.config.hl_config import HLConfig


class HLLogger:
    """The HLLogger class is a logger class that initializes a logger instance and returns it."""

    @staticmethod
    def get_logger(logger_name: str) -> Logger:
        """Initializes a logger instance and returns it.

        :param logger_name: A string representing the name of the logger to be returned
        :type logger_name: str
        :return: An instance of the Logger class.
        :rtype: Logger
        """
        if not os.path.exists(HLConfig.LOGS_FOLDER_PATH):
            os.makedirs(HLConfig.LOGS_FOLDER_PATH)

        log_file_path: str = f"{HLConfig.LOGS_FOLDER_PATH}/{logger_name}.log"

        # Initialize the logging configuration
        config.fileConfig(HLConfig.LOG_CONFIG_PATH, defaults={"log_file_path": log_file_path})

        return logging.getLogger(logger_name)
