"""Check machines with ping."""

from subprocess import run, PIPE
import platform

from preflyt.base import BaseChecker


class PingChecker(BaseChecker):
    """Verify that a machine responds to ping requests."""

    checker_name = "ping"

    def __init__(self, host):
        """Initialize the checker.

        :param host: the IP or hostname of the host to ping

        """
        if platform.system().lower() == 'windows':
            switch = "n"
        else:
            switch = "c"

        self._switch = switch
        self._host = host
        self._command = "ping -{} 1 {}".format(switch, host)


    def check(self):
        response = run(self._command, shell=True, stdout=PIPE, stderr=PIPE)
        if response.returncode == 0:
            return True, "{} is pingable".format(self._host)
        return False, "Cannot reach {}".format(self._host)
