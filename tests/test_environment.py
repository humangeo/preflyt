"""Test the environment checker"""

# pylint: disable=missing-docstring,protected-access

from unittest.mock import patch

from nose.tools import ok_, eq_

from preflyt.checkers.environment import EnvironmentChecker

def test_init_basic():
    env = EnvironmentChecker("VAR_NAME")
    eq_(env.checker_name, "env")
    eq_(env._name, "VAR_NAME")
    eq_(env._value, None)

def test_init_value():
    env = EnvironmentChecker("VAR_NAME", "FOO")
    eq_(env._name, "VAR_NAME")
    eq_(env._value, "FOO")

@patch('os.getenv')
def test_check_exists(getenv):
    getenv.return_value = ""
    checker = EnvironmentChecker("VAR_NAME")
    result, message = checker.check()
    getenv.assert_called_with("VAR_NAME")
    ok_(result)
    ok_("is defined" in message)

@patch('os.getenv')
def test_check_not_exists(getenv):
    getenv.return_value = None
    checker = EnvironmentChecker("VAR_NAME")
    result, message = checker.check()
    getenv.assert_called_with("VAR_NAME")
    ok_(not result, "Result is {}".format(result))
    ok_("is not defined" in message, message)

@patch('os.getenv')
def test_check_value(getenv):
    getenv.return_value = "FOO"
    checker = EnvironmentChecker("VAR_NAME", value="FOO")
    result, message = checker.check()
    getenv.assert_called_with("VAR_NAME")
    ok_(result, "Result is {}".format(result))
    ok_(" correct " in message, message)

@patch('os.getenv')
def test_check_wrong_value(getenv):
    getenv.return_value = "BAR"
    checker = EnvironmentChecker("VAR_NAME", value="FOO")
    result, message = checker.check()
    getenv.assert_called_with("VAR_NAME")
    ok_(not result, "Result is {}".format(result))
    ok_("incorrect" in message, message)
