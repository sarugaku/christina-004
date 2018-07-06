=============
Christina 004
=============

An issue tracker maintenance bot for pypa/pipenv.

Christina is the Assistant. Lab member 004.


Setup
=====

Install dependencies
--------------------

::

    pipenv sync --dev


Configure logging
-----------------

Something like this::

    [loggers]
    keys = root

    [handlers]
    keys = console

    [formatters]
    keys = default

    [logger_root]
    level = NOTSET
    handlers = console

    [handler_console]
    level = NOTSET
    class = logging.StreamHandler
    formatter = default

    [formatter_default]
    format = %(asctime)s %(levelname).1s [%(name)s] %(message)s


Provide environment variables
-----------------------------

Create a ``.env`` file in the project root::

    # Which GitHub repository should this server maintain.
    FUTURE_GADGET_LAB='pypa/pipenv'

    # How the bot identifies herself (GitHub username).
    USERNAME='christina-004'

    # Where the log configuration file is.
    LOG_CONFIG='christina.cfg'

    # GitHub authentication.
    GITHUB_TOKEN=
    GITHUB_SECRET=

    # (Optional) What port should the web service run on.
    PORT=8000


Run the server
==============

::

    pipenv run christina
