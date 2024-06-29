# misc utilities
import logging
import os
from enum import Enum


class Environment(Enum):
    DEVELOPMENT = 'development'
    TEST = 'test'
    PRODUCTION = 'production'


def get_environment():
    return Environment(os.environ['ENVIRONMENT'].lower())


def is_development():
    return get_environment() == Environment.DEVELOPMENT

def init_logging():
    # specify --log=DEBUG or --log=debug
    log_level_var = os.environ['LOG_LEVEL']
    log_level = log_level_var if log_level_var else 'INFO'

    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)

    logging.basicConfig(level=numeric_level)
