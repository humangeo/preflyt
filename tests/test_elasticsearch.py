"""Test the escservice checker"""

# pylint: disable=missing-docstring,protected-access

from unittest.mock import MagicMock, patch
import urllib.error

from nose.tools import ok_, eq_

from preflyt.checkers.elasticsearch import ElasticsearchChecker

EXAMPLE_URL = "http://example.com"
REQUEST_URL = "http://example.com/_cluster/health"
RESPONSE_TEMPLATE = """
{{
  "cluster_name" : "testcluster",
  "status" : "{color}",
  "timed_out" : false,
  "number_of_nodes" : 2,
  "number_of_data_nodes" : 2,
  "active_primary_shards" : 5,
  "active_shards" : 10,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 100
}}
"""

def get_response(color):
    return RESPONSE_TEMPLATE.format(color=color).encode('utf-8')

def test_init():
    esc = ElasticsearchChecker(EXAMPLE_URL)
    eq_(ElasticsearchChecker.checker_name, "es")
    eq_(esc._url, REQUEST_URL)
    eq_(esc._colors, {"green"})


def test_init_colors():
    esc = ElasticsearchChecker(EXAMPLE_URL, colors=["red", "YELLOW"])
    eq_(ElasticsearchChecker.checker_name, "es")
    eq_(esc._url, REQUEST_URL)
    eq_(esc._colors, {"green", "red", "yellow"})

def test_init_prefixless():
    esc = ElasticsearchChecker("example.com")
    eq_(esc._url, REQUEST_URL)

@patch("urllib.request.urlopen")
def test_check_healthy(urlopen):
    esc = ElasticsearchChecker(EXAMPLE_URL)
    response_mock = MagicMock()
    response_mock.read.return_value = get_response("green")
    response_mock.__enter__.return_value = response_mock
    urlopen.return_value = response_mock
    result, message = esc.check()
    urlopen.assert_called_with(REQUEST_URL)
    ok_(result)
    ok_("status is 'green'" in message, message)

@patch("urllib.request.urlopen")
def test_check_unhealthy(urlopen):
    esc = ElasticsearchChecker(EXAMPLE_URL)
    response_mock = MagicMock()
    response_mock.read.return_value = get_response("yellow")
    response_mock.__enter__.return_value = response_mock
    urlopen.return_value = response_mock
    result, message = esc.check()
    urlopen.assert_called_with(REQUEST_URL)
    ok_(not result)
    ok_("status is 'yellow'" in message, message)

@patch("urllib.request.urlopen")
def test_check_additional_color(urlopen):
    esc = ElasticsearchChecker(EXAMPLE_URL, colors=["yellow"])
    response_mock = MagicMock()
    response_mock.read.return_value = get_response("yellow")
    response_mock.__enter__.return_value = response_mock
    urlopen.return_value = response_mock
    result, message = esc.check()
    urlopen.assert_called_with(REQUEST_URL)
    ok_(result)
    ok_("status is 'yellow'" in message, message)

@patch("urllib.request.urlopen")
def test_check_additional_color_base(urlopen):
    esc = ElasticsearchChecker(EXAMPLE_URL, colors=["yellow"])
    response_mock = MagicMock()
    response_mock.read.return_value = get_response("green")
    response_mock.__enter__.return_value = response_mock
    urlopen.return_value = response_mock
    result, message = esc.check()
    urlopen.assert_called_with(REQUEST_URL)
    ok_(result)
    ok_("status is 'green'" in message, message)

@patch("urllib.request.urlopen")
def test_check_httperror(urlopen):
    esc = ElasticsearchChecker(EXAMPLE_URL)
    urlopen.side_effect = urllib.error.HTTPError(EXAMPLE_URL, 420, "HTTP ERROR HAPPENED", None, None)
    result, message = esc.check()
    ok_(not result)
    ok_("[420]" in message)

@patch("urllib.request.urlopen")
def test_check_urlerror(urlopen):
    esc = ElasticsearchChecker(EXAMPLE_URL)
    urlopen.side_effect = urllib.error.URLError("URL ERROR HAPPENED")
    result, message = esc.check()
    ok_(not result)
    ok_("URL ERROR HAPPENED" in message)

@patch("urllib.request.urlopen")
def test_check_unhandled(urlopen):
    esc = ElasticsearchChecker(EXAMPLE_URL)
    urlopen.side_effect = IOError("Whoops")
    result, message = esc.check()
    ok_(not result)
    ok_("Unhandled error: " in message)
