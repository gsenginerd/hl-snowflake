"""Snowflake Module"""
from typing import Any, Dict

# noinspection PyUnresolvedReferences
from snowflake.snowpark import Session

from conflicts_check.config.hl_config import HLConfig


class HLSnowflake:
    """The HLSnowflake class creates a new Snowflake session instance using provided configuration."""

    @staticmethod
    def create_session() -> Session:
        """Creates a new Snowflake session instance using the provided configuration.
        IMP: The password is read from the .env file for the key "SNOWFLAKE_USER_PWD". Ensure that you have a .env file with the entry.
        SNOWFLAKE_USER_PWD="password_text"
        :return: A Snowflake session instance.
        :rtype: Session
        """
        snowflake_config: Any = HLConfig.get_value("snowflake")

        connection_config: Dict[str, Any] = snowflake_config.get("connection")
        connection_config["account"] = HLConfig.get_environment_variable("SNOWFLAKE_ACCOUNT")
        connection_config["password"] = HLConfig.get_environment_variable("SNOWFLAKE_USER_PWD")

        return Session.builder.configs(connection_config).create()


if __name__ == "__main__":
    print(HLSnowflake.create_session())
