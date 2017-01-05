"""Test the filesystem checker"""

# pylint: disable=missing-docstring,protected-access

from unittest.mock import patch

from nose.tools import ok_, eq_

from preflyt.checkers.network import PingChecker


LOCALHOST = '127.0.0.1'
INVALID_HOST = '333.333.666.666'

def test_ping_init():
    ping = PingChecker(LOCALHOST)
    eq_(PingChecker.checker_name, "ping")
    eq_(ping._host, LOCALHOST)
    ok_(ping._switch)

@patch("platform.system", return_value='Windows')
def test_ping_windows_switch(system):
    ping = PingChecker(LOCALHOST)
    eq_(ping._host, LOCALHOST)
    eq_(ping._switch, 'n')

@patch("platform.system", return_value='Linux')
def test_ping_linux_switch(system):
    ping = PingChecker(LOCALHOST)
    eq_(ping._host, LOCALHOST)
    eq_(ping._switch, 'c')

@patch("platform.system", return_value='MatrixOS')
def test_ping_other_switch(system):
    ping = PingChecker(LOCALHOST)
    eq_(ping._host, LOCALHOST)
    eq_(ping._switch, 'c')

@patch("subprocess.call", return_value=0)
def test_ping_localhost(call):
    ping = PingChecker(LOCALHOST)
    eq_(ping._host, LOCALHOST)
    result, message = ping.check()
    ok_(result)
    ok_('pingable' in message)

@patch("subprocess.call", return_value=1)
def test_ping_invalid_host(call):
    ping = PingChecker(INVALID_HOST)
    eq_(ping._host, INVALID_HOST)
    result, message = ping.check()
    ok_(not result)
    ok_("Cannot reach" in message)
