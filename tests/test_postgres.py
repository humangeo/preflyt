"""Test the filesystem checker"""

# pylint: disable=missing-docstring,protected-access

from subprocess import CalledProcessError
from unittest.mock import patch

from nose.tools import ok_, eq_

from preflyt.checkers.postgres import PostgresChecker

HOST = "example.com"
PORT = 4242
DBNAME = "bobby_tables"

PSQL_UP = b"/var/run/postgresql:5432 - accepting connections\n"
PSQL_DOWN = b"/var/run/postgresql:5432 - no response\n"

def test_init():
    psql = PostgresChecker()
    eq_(PostgresChecker.checker_name, "psql")
    eq_(psql._host, "localhost")
    eq_(psql._port, 5432)
    eq_(psql._dbname, None)

def test_init_everything():
    psql = PostgresChecker(host=HOST, port=PORT, dbname=DBNAME)
    eq_(psql._host, HOST)
    eq_(psql._port, PORT)
    eq_(psql._dbname, DBNAME)

@patch("subprocess.check_output")
def test_check_defaults_ok(check_output):
    psql = PostgresChecker()
    check_output.return_value = PSQL_UP
    result, message = psql.check()
    check_output.assert_called_with(["pg_isready", "--host=localhost", "--port=5432"])
    ok_(result)
    ok_("is available" in message, message)

@patch("subprocess.check_output")
def test_check_everything_ok(check_output):
    psql = PostgresChecker(host=HOST, port=PORT, dbname=DBNAME)
    check_output.return_value = PSQL_UP
    result, message = psql.check()
    check_output.assert_called_with(["pg_isready",
                                     "--host={}".format(HOST),
                                     "--port={}".format(PORT),
                                     "--dbname={}".format(DBNAME)])
    ok_(result)
    ok_("is available" in message, message)

@patch("subprocess.check_output")
def test_check_defaults_failure(check_output):
    psql = PostgresChecker()
    check_output.return_value = PSQL_DOWN
    check_output.side_effect = CalledProcessError(2, ['pg_isready'], output=PSQL_DOWN)
    result, message = psql.check()
    check_output.assert_called_with(["pg_isready", "--host=localhost", "--port=5432"])
    ok_(not result, result)
    ok_("is not available" in message, message)
