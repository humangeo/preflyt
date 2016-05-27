"""Checks for environment variables"""

import os

from preflyt.base import BaseChecker

class EnvironmentChecker(BaseChecker):
    """Verify that an environment variable is present and, if so, it has a specific value."""

    checker_name = "env"

    def __init__(self, name, value=None):
        """Initialize the checker

        :param name: The name of the environment variable to check
        :param value: The optional value of the variable.

        """
        super().__init__()
        self._name = name
        self._value = value

    def check(self):
        val = os.getenv(self._name)
        if val is None:
            return False, "The environment variable '{}' is not defined".format(self._name)
        elif self._value is not None:
            if self._value == val:
                return True, "The environment variable '{}' is defined with the correct value.".format(self._name)
            return False, "The environment variable '{}' is defined with the incorrect value.".format(self._name)
        return True, "The environment variable '{}' is defined.".format(self._name)
