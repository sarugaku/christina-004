import logging.config

from .envs import LOG_CONFIG


logging.config.fileConfig(LOG_CONFIG)


if __name__ == '__main__':
    from .web import run
    run()
