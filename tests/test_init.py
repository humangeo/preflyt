"""Test the checkers"""
import os
from unittest.mock import call, Mock, patch

from nose.tools import ok_, eq_, raises

import preflyt

CHECKERS = [
    {"checker": "env", "name": "USER"}
]

BAD_CHECKERS = [
    {"checker": "env", "name": "USER1231342dhkfgjhk2394dv09324jk12039csdfg01231"}
]

@patch("pkgutil.iter_modules")
def test_load_checkers(iter_modules):
    """Test the load_checkers method"""
    iter_modules.return_value = [(Mock(), "mod{}".format(n), None) for n in range(3)]
    preflyt.load_checkers()
    iter_modules.assert_called_once_with([os.path.join(preflyt.__path__[0], "checkers")])
    for loader, name, _ in iter_modules.return_value:
        loader.find_module.assert_called_once_with(name)
        loader.find_module.return_value.load_module.assert_called_once_with(name)

def test_everything():
    """Test the check method."""
    good, results = preflyt.check(CHECKERS)
    ok_(good, results)
    eq_(len(results), 1)
    for field_name in ('check', 'success', 'message'):
        ok_(field_name in results[0])

def test_everything_failure():
    """Test the check method."""
    good, results = preflyt.check(BAD_CHECKERS)
    ok_(not good, results)
    eq_(len(results), 1)
    for field_name in ('check', 'success', 'message'):
        ok_(field_name in results[0])

@patch("preflyt.load_checkers")
def test_load_called(load_checkers):
    """Verify the load method is called"""
    checkers = preflyt.CHECKERS
    preflyt.CHECKERS = {}
    try:
        preflyt.check([])
        load_checkers.assert_called_once_with()
    finally:
        preflyt.CHECKERS = checkers

@patch("sys.stderr.write")
@patch("preflyt.pformat_check")
def test_everything_loud(pformat, stderr):
    """Eat up teh stderr stuff."""
    pformat.return_value = "item"
    preflyt.check(CHECKERS, loud=True)
    stderr.assert_has_calls([
        call("Preflyt Checklist\n=================\n"),
        call(" item\n")
    ])

@raises(preflyt.CheckerNotFoundError)
def test_missing_checker():
    preflyt.check([{"checker": "noop"}])
