"""Checks for Elasticsearch cluster health"""

import json
from urllib import request
import urllib.error

from preflyt.base import BaseChecker

class ElasticsearchChecker(BaseChecker):
    """Verify Elasticsearch is available and healthy"""

    checker_name = "es"

    def __init__(self, url, colors=None):
        """Initialize the checker

        :param name: The base URL of the Elasticsearch server
        :param colors: Acceptable cluster health colors (other than Green)

        """
        super().__init__()
        if not url.lower().startswith(("http://", "https://", "ftp://")):
            url = "http://" + url
        self._url = "{}/_cluster/health".format(url)
        self._colors = {color.lower() for color in colors or []}
        self._colors.add("green")

    def check(self):
        try:
            with request.urlopen(self._url) as response:
                body = response.read()
                response = json.loads(body.decode('utf-8'))
                if response["status"] in self._colors:
                    return True, "Cluster status is '{}'".format(response["status"])
                return False, "Cluster status is '{}'".format(response["status"])
        except urllib.error.HTTPError as httpe:
            return False, "[{}] {}".format(httpe.code, httpe.reason)
        except urllib.error.URLError as urle:
            return False, urle.reason
        except Exception as exc: # pylint: disable=broad-except
            return False, "Unhandled error: {}".format(exc)
