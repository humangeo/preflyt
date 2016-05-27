"""Checks for filesystem data"""

import os.path

from preflyt.base import BaseChecker

class DirectoryChecker(BaseChecker):
    """Verify the presence (or absence) of a directory."""

    checker_name = "dir"

    def __init__(self, path, present=True):
        """Initialize the checker

        :param path: The path to the directory (absolute or relative)
        :param present: `False` if the directory should be absent. `True` by default.

        """
        super().__init__()
        self._path = path
        self._present = present

    def check(self):
        present = os.path.isdir(self._path)

        return (present is self._present,
                "The directory '{}' is {}present.".format(self._path, "" if present else "not "))


class FileChecker(BaseChecker):
    """Verify the presence (or absence of) a file"""

    checker_name = "file"

    def __init__(self, path, present=True):
        """Initialize the checker

        :param path: The path to the file (absolute or relative)
        :param present: `False` if the file should be absent. `True` by default.

        """
        super().__init__()
        self._path = path
        self._present = present

    def check(self):
        present = os.path.isfile(self._path)

        return (present is self._present,
                "The file '{}' is {}present.".format(self._path, "" if present else "not "))
