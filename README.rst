.. image:: ./res/logo.png

*A lightweight application environment checker.*

*Python 3 only. The future is now.*

.. image:: https://travis-ci.org/humangeo/preflyt.svg
   :target: https://travis-ci.org/humangeo/preflyt

.. image:: https://coveralls.io/repos/github/humangeo/preflyt/badge.svg?branch=master
   :target: https://coveralls.io/github/humangeo/preflyt?branch=master

Getting started
--------------------

To use Preflyt, install it :code:`pip install preflyt`, and then invoke it:

.. code-block:: python

    import preflyt

    ok, results = preflyt.check([
        # Assert the presence and value of the $APP_ENV environment variable
        {"checker": "env", "name": "APP_ENV", "value": "production"},

        # Assert that a file at the given path exists
        {"checker": "file", "path": DATA_FILE},
    ])

    if ok:
        print("Preflyt checks passed.")
        run()
    else:
        print("Preflyt checks failed!")
        for result in results:
            if not result["success"]:
                print("{checker[checker]}: {message}".format(**result))


Checkers
---------

Out of the box, the following checkers are available.

+--------+---------------------------+----------------------------------------------------------------------------------------------------+
| Name   | Description               | Args                                                                                               |
+========+===========================+====================================================================================================+
| env    | Check environment state   | - **name**: Variable name.                                                                         |
|        |                           | - **value**: (optional) Variable value.                                                            |
+--------+---------------------------+----------------------------------------------------------------------------------------------------+
| es     | Check Elasticsearch state | - **url**: The Elasticsearch endpoint URL.                                                         |
|        |                           | - **colors**: (optional) A collection of acceptable cluster colors (aside from 'green').           |
+--------+---------------------------+----------------------------------------------------------------------------------------------------+
| dir    | Check directory state     | - **path**: Directory path.                                                                        |
|        |                           | - **present**: (optional, default=True) False if the directory should be absent.                   |
+--------+---------------------------+----------------------------------------------------------------------------------------------------+
| file   | Check file state          | - **path**: File path.                                                                             |
|        |                           | - **present**: (optional, default=True) False if the file should be absent.                        |
+--------+---------------------------+----------------------------------------------------------------------------------------------------+
| psql   | Check PostgreSQL state    | - **host**: (optional, default=localhost) Postgres hostname.                                       |
|        |                           | - **port**: (optional, default=5432) Postgres server port.                                         |
|        |                           | - **dbname**: (optional, default=None) The database name for which to test.                        |
+--------+---------------------------+----------------------------------------------------------------------------------------------------+
| sqlite | Check SQLite3 state       | - **path**: (optional, default=db.sqlite3) The path to the SQLite database.                        |
+--------+---------------------------+----------------------------------------------------------------------------------------------------+
| web    | Check web service state   | - **url**: The webservice URL                                                                      |
|        |                           | - **statuses**: (optional, default=None) A collection of acceptable status codes (aside from 200). |
+--------+---------------------------+----------------------------------------------------------------------------------------------------+

Future versions of Preflyt will add additional default checkers while allowing third parties to ship their own.

Philosophy
-------------------------

You know what sucks? Kicking off a long running data ingestion/processing task only to discover, near the end, that an external dependency (e.g. webservice, binary) is missing or otherwise inaccessible. "I know what I'll do!" you, the frustrated programmer, exclaims. Choose your own adventure:

* **"I'm going to manually verify things are as they should be before I kick off the task."**

  Congratulations, you just played yourself. Not only do you run the risk of forgetting a checklist item, but now you have to enforce this practice within your team.

* **"I'm going to programatically check things on script start."**

  Getting warm! Hopefully your solution is configuration driven. Even then, what are the odds you wind up with this boilerplate across your scripts?

  .. code-block:: python

      # settings.py
      if env_name == "production":
          ES_HOST = "http://example.com"
          POSTGRES_HOST = "10.0.1.120"
          ENABLE_DATA_DIR_CHECK = True
      else:
          ES_HOST = "localhost:9200"
          POSTGRES_HOST = "localhost"
          ENABLE_DATA_DIR_CHECK = False
      DATA_DIR = "/mnt/data/dir"
      DATA_FILE = "/mnt/data/dir/metadata.json"
      POSTGRES_PORT = 5432

      # run.py
      if not requests.get(settings.ES_HOST).status_ok: #Now you've got a requests dependency
          print("Elasticsearch is unreachable.")
          sys.exit(1)
      if settings.ENABLE_DATA_DIR_CHECK and not os.path.exists(settings.DATA_DIR): # Whoops, should have used `isdir`
          print("Can't access: ", settings.DATA_DIR)
          sys.exit(1)
      if not os.path.exists(settings.DATA_FILE): # Whoops, should have used `isfile`
          print("Can't access: ", settings.DATA_FILE)
          sys.exit(1)
      try:
          postgres.connect(settings.POSTGRES_HOST, settings.POSTGRES_PORT)
      except Exception as exe:
          print(exe)
          sys.exit(1)

  And so forth. You've now got a crazy-long series of if statements in your code, and changing the checks is a code change, not a configuration change. Also, you've generated boilerplate that should be abstracted and reused.

* **"I'm going to programatically check things on script start... with Preflyt!"**

  Bingo. That ugly series of code above?

  .. code-block:: python

    # settings.py
    CHECKS = [
        {"checker": "web", "url": ES_HOST},
        {"checker": "psql", "host": POSTGRES_HOST, "port": POSTGRES_PORT},
        {"checker": "file", "path": DATA_FILE},
    ]
    if ENVNAME == "production":
        CHECKS.append({"checker": "dir", "path": DATA_DIR})

    # run.py
    import preflyt
    ok, results = preflyt.check(settings.CHECKS)
    if not ok:
        print([result in results if not result["success"]])
        sys.exit(1)

  Now all the checks you're performing are defined in configuration, and no boilerplate!

Contributing
--------------

Additional checkers are more than welcome! The goal is to keep this package free of dependencies, so cleverness is appreciated :-)

Please write tests for whatever checkers you wish to submit. Preflyt uses nose. Development packages can be installed via :code:`pip install -e .[test]`, and tests can be run via :code:`nosetests .`.

License
--------

MIT, Copyright (c) 2016 The HumanGeo Group, LLC. See the LICENSE file for more information.
