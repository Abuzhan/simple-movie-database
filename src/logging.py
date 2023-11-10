import logging
import sys


def initialize_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
