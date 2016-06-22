"""Test the checkers"""
from nose.tools import ok_, eq_

from preflyt import check

CHECKERS = [
    {"checker": "env", "name": "PATH"}
]

BAD_CHECKERS = [
    {"checker": "env", "name": "PATH1231342dhkfgjhk2394dv09324jk12039csdfg01231"}
]

def test_everything():
    """Test the check method."""
    good, results = check(CHECKERS)
    ok_(good, results)
    eq_(len(results), 1)
    for field_name in ('check', 'success', 'message'):
        ok_(field_name in results[0])

def test_everything_failure():
    """Test the check method."""
    good, results = check(BAD_CHECKERS)
    ok_(not good, results)
    eq_(len(results), 1)
    for field_name in ('check', 'success', 'message'):
        ok_(field_name in results[0])
