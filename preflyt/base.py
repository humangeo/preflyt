"""The base situation checker structure"""

from preflyt import CHECKERS

class BaseMeta(type):
    """The base metaclass"""

    def __new__(mcs, name, bases, class_dict):
        """Intercept all new types"""
        cls = type.__new__(mcs, name, bases, class_dict)
        if cls.checker_name != "base":
            CHECKERS[cls.checker_name] = cls
        return cls

class BaseChecker(metaclass=BaseMeta):
    """The base checker"""
    checker_name = "base"

    def __init__(self):
        """Override this in the checker"""
        pass

    def check(self):
        """This does the checking thing
        :returns: A 2-Tuple containing a boolean for success, and a string containing the status message

        """
        raise NotImplementedError()
