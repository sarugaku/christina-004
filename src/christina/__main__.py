import logging.config
import os

logging.config.fileConfig(os.environ['LOG_CONFIG'])

if __name__ == '__main__':
    from .web import run
    run()
