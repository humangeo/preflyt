"""The checker subsystem"""

import os.path
import pkgutil
import sys

from preflyt.utils import pformat_check

__author__ = "Aru Sahni"
__version__ = "0.4.0"
__licence__ = "MIT"

CHECKERS = {}

import preflyt.base # pylint: disable=wrong-import-position

def load_checkers():
    """Load the checkers"""
    for loader, name, _ in pkgutil.iter_modules([os.path.join(__path__[0], 'checkers')]):
        loader.find_module(name).load_module(name)

def check(operations, loud=False):
    """Check all the things

    :param operations: The operations to check
    :param loud: `True` if checkers should prettyprint their status to stderr. `False` otherwise.
    :returns: A tuple of overall success, and a detailed execution log for all the operations

    """
    if not CHECKERS:
        load_checkers()
    roll_call = []
    everything_ok = True
    if loud and operations:
        title = "Preflyt Checklist"
        sys.stderr.write("{}\n{}\n".format(title, "=" * len(title)))
    for operation in operations:
        if operation.get('checker') not in CHECKERS:
            raise CheckerNotFoundError(operation)
        checker_cls = CHECKERS[operation['checker']]
        args = {k: v for k, v in operation.items() if k != 'checker'}
        checker = checker_cls(**args)
        success, message = checker.check()
        if not success:
            everything_ok = False
        roll_call.append({"check": operation, "success": success, "message": message})
        if loud:
            sys.stderr.write(" {}\n".format(pformat_check(success, operation, message)))
    return everything_ok, roll_call

def verify(operations, loud=False):
    """Check all the things and be assertive about it

    :param operations: THe operations to check
    :param loud: `True` if checkers should prettyprint their status to stderr. `False` otherwise.
    :returns: The detailed execution log for the operations.

    """
    everything_ok, roll_call = check(operations, loud=loud)
    if not everything_ok:
        raise CheckFailedException(roll_call)
    return roll_call

class CheckerNotFoundError(Exception):
    """Couldn't find the checker."""
    pass

class CheckFailedException(Exception):
    """One or more of the system checks failed"""

    def __init__(self, checks):
        super().__init__()
        self.checks = checks
