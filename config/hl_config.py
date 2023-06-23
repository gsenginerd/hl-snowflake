"""
The HLConfig class is a configuration module that retrieves values for given keys from a configuration file.
and raises an exception if the key is invalid.
"""
# pylint: disable= R0903 #Too few public methods

import json
import os
from typing import Any, Optional

from dotenv import load_dotenv

import utils.file_util as hl_file_util
from exceptions.hl_configuration_error import HLConfigurationError


class HLConfig:
    """Configuration class"""

    _CONFIG_FILE: Optional[str] = None
    _CONFIG: Optional[dict] = None

    PROJECT_ROOT: str = hl_file_util.get_project_root(os.getcwd(), "hl-snowflake")
    _COMPARE_PACKAGE_FOLDER_PATH: str = os.path.join(PROJECT_ROOT, "compare")
    _SNOWFLAKE_PACKAGE_FOLDER_PATH: str = os.path.join(PROJECT_ROOT, "snowflake")
    _TESTS_FOLDER_PATH: str = os.path.join(PROJECT_ROOT, "tests")
    CSV_FILE_PATH: str = os.path.join(PROJECT_ROOT, "csv_files")
    CSV_DATA_SCHEMA_PATH: str = os.path.join(_SNOWFLAKE_PACKAGE_FOLDER_PATH, "etl/csv_import/schemas")
    LOGS_FOLDER_PATH: str = os.path.join(PROJECT_ROOT, "logs")
    LOG_CONFIG_PATH: str = os.path.join(PROJECT_ROOT, "logging.conf")
    TESTS_CONFIG_FOLDER_PATH: str = os.path.join(_TESTS_FOLDER_PATH, "config")
    TESTS_DM_FOLDER_PATH: str = os.path.join(_TESTS_FOLDER_PATH, "decision_matrix")
    TESTS_DATA_FOLDER_PATH: str = os.path.join(_TESTS_FOLDER_PATH, "test_data")

    # Load the environment variables
    load_dotenv()

    environment: str = os.getenv("ENVIRONMENT")

    load_dotenv(f"{PROJECT_ROOT}/.env.{environment}")

    config_file: str = os.path.join(PROJECT_ROOT, "config.json")

    # Check that specified config file exists
    assert os.path.exists(config_file)

    # Use singleton pattern to store config file location/load config once
    _CONFIG_FILE = config_file

    with open(config_file, "r", encoding="ascii") as f:
        _CONFIG = json.load(f)

    @staticmethod
    def get_value(key: str) -> Any:
        """
        Retrieves a value for a given key from a configuration file and raises an exception
        if the key is invalid.

        :param key: A string representing the key for which the value needs to be retrieved from the
        config file
        :type key: str
        :return: the value for a given key from a configuration file. The return type is a string.
        :raises ConfigurationError: if an invalid key is provided
        :rtype: Any
        """
        assert HLConfig._CONFIG

        if key not in HLConfig._CONFIG:
            raise HLConfigurationError(f"Please set the {key} variable in the config file {HLConfig._CONFIG_FILE}")

        return HLConfig._CONFIG.get(key)

    @staticmethod
    def get_environment_variable(name: str) -> str:
        """
        This function retrieves the value of an environment variable by its name.

        :param name: A string representing the name of the environment variable to retrieve
        :type name: str
        :return: The value of the environment variable with the given name.
        :rtype: str
        """

        return os.getenv(name)
