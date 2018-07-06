import os


USERNAME = os.environ['USERNAME']

FUTURE_GADGET_LAB = os.environ['FUTURE_GADGET_LAB']

CRT_WORKSHOP, _ = FUTURE_GADGET_LAB.split('/')

LOG_CONFIG = os.environ['LOG_CONFIG']

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
GITHUB_SECRET = os.environ['GITHUB_SECRET']

try:
    PORT = int(os.environ['PORT'])
except KeyError:
    PORT = None
