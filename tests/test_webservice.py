"""Test the webservice checker"""

# pylint: disable=missing-docstring,protected-access

from unittest.mock import patch
import urllib.error

from nose.tools import ok_, eq_

from preflyt.checkers.webservice import WebServiceChecker

EXAMPLE_URL = "http://example.com"

def test_init():
    web = WebServiceChecker(EXAMPLE_URL)
    eq_(WebServiceChecker.checker_name, "web")
    eq_(web._url, EXAMPLE_URL)

def test_init_prefixless():
    web = WebServiceChecker("example.com")
    eq_(web._url, "http://example.com")

@patch("urllib.request.urlopen")
def test_check_ok(urlopen):
    web = WebServiceChecker(EXAMPLE_URL)
    urlopen.return_value = "FOO"
    result, message = web.check()
    urlopen.assert_called_with(EXAMPLE_URL)
    ok_(result)
    ok_("is available" in message)

@patch("urllib.request.urlopen")
def test_check_httperror(urlopen):
    web = WebServiceChecker(EXAMPLE_URL)
    urlopen.side_effect = urllib.error.HTTPError(EXAMPLE_URL, 420, "HTTP ERROR HAPPENED", None, None)
    result, message = web.check()
    ok_(not result)
    ok_("[420]" in message)

@patch("urllib.request.urlopen")
def test_check_urlerror(urlopen):
    web = WebServiceChecker(EXAMPLE_URL)
    urlopen.side_effect = urllib.error.URLError("URL ERROR HAPPENED")
    result, message = web.check()
    ok_(not result)
    ok_("URL ERROR HAPPENED" in message)

@patch("urllib.request.urlopen")
def test_check_unhandled(urlopen):
    web = WebServiceChecker(EXAMPLE_URL)
    urlopen.side_effect = IOError("Whoops")
    result, message = web.check()
    ok_(not result)
    ok_("Unhandled error: " in message)
