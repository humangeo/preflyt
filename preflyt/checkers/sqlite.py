"""Checks for SQLite data"""

import os

from preflyt.base import BaseChecker


class SqliteChecker(BaseChecker):
    """Verify that a SQLite3 DB exists and is readable."""

    checker_name = "sqlite"

    def __init__(self, path='db.sqlite3'):
        """Initialize the checker

        :param path: The path to the SQLite3 database.

        """
        super().__init__()
        self._path = path

    def check(self):
        if not os.path.exists(self._path):
            return False, "SQLite3 DB at path {} does not exist".format(self._path)

        with open(self._path, 'rb') as infile:
            header = infile.read(100)

        passed = header[:15] == b'SQLite format 3'
        if passed:
            return True, "The DB {} is present and valid.".format(self._path)
        return False, "The DB {} does not appear to be a \
                       valid SQLite3 file.".format(self._path)
