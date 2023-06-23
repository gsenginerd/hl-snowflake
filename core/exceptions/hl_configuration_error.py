"""The module defines custom exception classes for various error scenarios."""


class HLConfigurationError(Exception):
    """The HLConfigurationError class is an exception that can be raised when an invalid key is provided or configuration cannot be read for the given key."""

    def __init__(self, key: str, message="Missing config for key {key}"):
        """Initializes an object with a configuration key and an error
        message.

        :param key: A string representing the configuration key
        :type key: str
        :param message: The error message to be displayed if the configuration key is missing. It is a
        string that can contain the placeholder %(key)s, which will be replaced with the actual key
        value, defaults to Missing config for key %(key)s (optional)
        """
        self.rule_key = key
        self.message = message.format(key=key)
        super().__init__(self.message)
