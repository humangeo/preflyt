"""Test the filesystem checker"""

# pylint: disable=missing-docstring,protected-access

from unittest.mock import patch

from nose.tools import ok_, eq_

from preflyt.checkers.filesystem import DirectoryChecker, FileChecker

FILE_PATH = '/tmp/test.txt'
DIR_PATH = '/tmp/'

def test_file_init():
    fil = FileChecker(FILE_PATH)
    eq_(FileChecker.checker_name, "file")
    eq_(fil._path, FILE_PATH)
    eq_(fil._present, True)

def test_file_init_absent():
    fil = FileChecker(FILE_PATH, present=False)
    eq_(fil._path, FILE_PATH)
    eq_(fil._present, False)

@patch("os.path.isfile")
def test_file_check_present_present(isfile):
    fil = FileChecker(FILE_PATH)
    isfile.return_value = True
    result, message = fil.check()
    isfile.assert_called_with(FILE_PATH)
    ok_(result)
    ok_("is present" in message, message)

@patch("os.path.isfile")
def test_file_check_present_missing(isfile):
    fil = FileChecker(FILE_PATH)
    isfile.return_value = False
    result, message = fil.check()
    isfile.assert_called_with(FILE_PATH)
    ok_(not result, result)
    ok_("is not present" in message, message)

@patch("os.path.isfile")
def test_file_check_missing_missing(isfile):
    fil = FileChecker(FILE_PATH, present=False)
    isfile.return_value = False
    result, message = fil.check()
    isfile.assert_called_with(FILE_PATH)
    ok_(result, result)
    ok_("is not present" in message, message)

@patch("os.path.isfile")
def test_file_check_missing_present(isfile):
    fil = FileChecker(FILE_PATH, present=False)
    isfile.return_value = True
    result, message = fil.check()
    isfile.assert_called_with(FILE_PATH)
    ok_(not result, result)
    ok_("is present" in message, message)

def test_dir_init():
    directory = DirectoryChecker(DIR_PATH)
    eq_(DirectoryChecker.checker_name, "dir")
    eq_(directory._path, DIR_PATH)
    eq_(directory._present, True)

def test_dir_init_absent():
    directory = DirectoryChecker(DIR_PATH, present=False)
    eq_(directory._path, DIR_PATH)
    eq_(directory._present, False)

@patch("os.path.isdir")
def test_dir_check_present_present(isdir):
    directory = DirectoryChecker(DIR_PATH)
    isdir.return_value = True
    result, message = directory.check()
    isdir.assert_called_with(DIR_PATH)
    ok_(result)
    ok_("is present" in message, message)

@patch("os.path.isdir")
def test_dir_check_present_missing(isdir):
    directory = DirectoryChecker(DIR_PATH)
    isdir.return_value = False
    result, message = directory.check()
    isdir.assert_called_with(DIR_PATH)
    ok_(not result, result)
    ok_("is not present" in message, message)

@patch("os.path.isdir")
def test_dir_check_missing_missing(isdir):
    directory = DirectoryChecker(DIR_PATH, present=False)
    isdir.return_value = False
    result, message = directory.check()
    isdir.assert_called_with(DIR_PATH)
    ok_(result, result)
    ok_("is not present" in message, message)

@patch("os.path.isdir")
def test_dir_check_missing_present(isdir):
    directory = DirectoryChecker(DIR_PATH, present=False)
    isdir.return_value = True
    result, message = directory.check()
    isdir.assert_called_with(DIR_PATH)
    ok_(not result, result)
    ok_("is present" in message, message)
