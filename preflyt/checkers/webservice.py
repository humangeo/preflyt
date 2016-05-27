"""Checks for web services"""

from urllib import request
import urllib.error

from preflyt.base import BaseChecker

class WebServiceChecker(BaseChecker):
    """Verify that a webservice is reachable"""

    checker_name = "web"

    def __init__(self, url, statuses=None):
        """Initialize the checker

        :param name: The URL of the endpoint to check
        :param statuses: Acceptable HTTP statuses (other than 200 OK)

        """
        super().__init__()
        if not url.lower().startswith(("http://", "https://", "ftp://")):
            url = "http://" + url
        self._url = url
        self._statuses = statuses or []

    def check(self):
        try:
            request.urlopen(self._url)
        except urllib.error.HTTPError as httpe:
            if httpe.code in self._statuses:
                return True, "{} is available, but with status: [{}] {}".format(
                    self._url, httpe.code, httpe.reason)
            return False, "[{}] {}".format(httpe.code, httpe.reason)
        except urllib.error.URLError as urle:
            return False, urle.reason
        except Exception as exc: # pylint: disable=broad-except
            return False, "Unhandled error: {}".format(exc)
        return True, "{} is available".format(self._url)
