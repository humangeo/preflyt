"""Test the base module"""

from nose.tools import raises

from preflyt.base import BaseChecker

@raises(NotImplementedError)
def test_base_checker_check():
    """Verify the base checker cannot be used"""
    checker = BaseChecker()
    checker.check()
