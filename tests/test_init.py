"""Test the checkers"""
from nose.tools import ok_

from preflyt import check

CHECKERS = [
    {"checker": "env", "name": "USER"}
]

def test_everything():
    """Test the check method."""
    good, results = check(CHECKERS)
    ok_(good, results)
