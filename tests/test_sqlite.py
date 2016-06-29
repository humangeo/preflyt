"""Test the checkers"""
import sqlite3
import os
from functools import wraps
import tempfile

from nose.tools import ok_, eq_

from preflyt.checkers.sqlite import SqliteChecker


def bootstrap_db(path):
    def wrapper(func):
        def create_table(path):
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE wet (stuntz text)')
            conn.commit()
            conn.close()

        def remove_table(path):
            os.remove(path)

        @wraps(func)
        def wrapped(*args, **kwargs):
            create_table(path)
            result = func(*args, **kwargs)
            remove_table(path)
            return result
        return wrapped
    return wrapper

def test_init():
    sqlite = SqliteChecker()
    eq_(SqliteChecker.checker_name, "sqlite")
    eq_(sqlite._path, "db.sqlite3")

def test_init_path():
    sqlite = SqliteChecker(path="test.db")
    eq_(sqlite._path, "test.db")

@bootstrap_db('db.sqlite3')
def test_exists():
    path = 'db.sqlite3'
    sqlite = SqliteChecker(path=path)
    eq_(sqlite._path, path)

def test_not_exists():
    path = 'db.sqliteeeee'
    sqlite = SqliteChecker(path=path)
    result, message = sqlite.check()
    ok_(not result)
    ok_("does not exist" in message, message)

@bootstrap_db('db.sqlite3')
def test_valid():
    path = 'db.sqlite3'
    sqlite = SqliteChecker(path=path)
    result, message = sqlite.check()
    ok_(result)
    ok_("present and valid" in message, message)

def test_invalid():
    filehandle, filepath = tempfile.mkstemp()
    try:
        os.write(filehandle, b'Not valid')
        os.close(filehandle)
        sqlite = SqliteChecker(path=filepath)
        result, message = sqlite.check()
    finally:
        os.remove(filepath)
    ok_(not result)
    ok_("does not appear" in message, message)
