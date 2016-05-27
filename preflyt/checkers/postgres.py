"""Checks for Postgres data"""

import subprocess

from preflyt.base import BaseChecker

class PostgresChecker(BaseChecker):
    """Verify that a PostgresQL instance is available.

    This requires that the `pg_isready` shell script be reachable and invokable.
    """

    checker_name = "psql"

    def __init__(self, host="localhost", port=5432, dbname=None):
        """Initialize the checker

        :param host: The host of the postgres server
        :param port: The port for the postgres server
        :param dbname: The name of the database to connect to

        """
        super().__init__()
        self._host = host
        self._port = port
        self._dbname = dbname

    def check(self):
        args = [
            "pg_isready",
            "--host={}".format(self._host),
            "--port={}".format(self._port),
        ]
        if self._dbname:
            args.append("--dbname={}".format(self._dbname))

        status = 0
        try:
            output = subprocess.check_output(args)
        except subprocess.CalledProcessError as cpe:
            status = cpe.returncode
            output = cpe.output

        if status != 0:
            return False, "Postgres is not available: [{}] {}".format(status,
                                                                      output.decode("utf-8", "replace").rstrip())
        return True, "Postgres is available"
