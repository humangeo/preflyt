"""Test the utils"""
from nose.tools import ok_, eq_

from preflyt import utils

SAMPLE_CHECK = {"checker": "env"}

def test_pformat_check_success():
    string = utils.pformat_check(True, SAMPLE_CHECK, "message")
    eq_('✓', string[1])
    ok_(SAMPLE_CHECK['checker'] + ": " in string)
    ok_(string.endswith("message"))

def test_pformat_check_failure():
    string = utils.pformat_check(False, SAMPLE_CHECK, "message")
    eq_('✗', string[1])
    ok_(SAMPLE_CHECK['checker'] + ": " in string)
    ok_(string.endswith("message"))
