"""The checker subsystem"""

import os.path
import pkgutil
import sys

__author__ = "Aru Sahni"
__version__ = "0.1.0"
__licence__ = "MIT"

CHECKERS = {}

import preflyt.base # pylint: disable=wrong-import-position

def load_checkers():
    """Load the checkers"""
    for loader, name, _ in pkgutil.iter_modules([os.path.join(__path__[0], 'checkers')]):
        loader.find_module(name).load_module(name)

def check(operations):
    """Check all the things

    :param operations: The operations to check
    :returns: A tuple of overall success, and a detailed execution log for all the operations

    """
    if not CHECKERS:
        load_checkers()
    roll_call = []
    everything_ok = True
    for operation in operations:
        if operation.get('checker') not in CHECKERS:
            raise CheckerNotFoundError(operation)
        checker_cls = CHECKERS[operation['checker']]
        args = {k: v for k, v in operation.items() if k != 'checker'}
        checker = checker_cls(**args)
        success, message = checker.check()
        if not success:
            everything_ok = False
        roll_call.append({"checker": operation, "success": success, "message": message})
    return everything_ok, roll_call

class CheckerNotFoundError(Exception):
    """Couldn't find the checker."""
    pass
