"""
Documentation for misc_utils
A collection of various useful functions
"""

import logging
import logging.config
import datetime
from logging.handlers import RotatingFileHandler

def configure_logger(default_level='DEBUG', **kwargs):
    """
    generic logger - https://docs.python.org/3/library/logging.html

    * CRITICAL    - 50
    * ERROR       - 40
    * WARNING     - 30
    * INFO        - 20
    * DEBUG       - 10
    * NOTSET      - 0

    :param str default_level: level of logging
    :type default_level: str, int

    :keyword console_level: [str, int] level of logging for console
    :keyword file_level: [str, int] level of logging for file
    :keyword log_file: [str] log file, default="log_file.log"

    :return: The logger oject
    :rtype: logging.Logger
    """

    DEFAULT_LOG_FILE = "log_file.log"

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - '
                                  '%(levelname)s -'
                                  '%(filename)s.%(funcName)s():%(lineno)d - '
                                  '%(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S'}
        },
        'handlers': {
            'console': {
                'level': kwargs.get('console_level', default_level),
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': kwargs.get('file_level', default_level),
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': kwargs.get('log_file', DEFAULT_LOG_FILE),
                'maxBytes': 1024,
            }
        },
        'loggers': {
            'default': {
                'level': default_level,
                'handlers': ['console', 'file']
            }
        },
        'disable_existing_loggers': False
    })
    return logging.getLogger('default')



class funcLogger():
    """This is a class to manage file logging"""
    _func_count = {}

    def __init__(self, filename="timings.txt", level=logging.INFO):
        self.log = logging.getLogger("func_logger")
        self.handler = RotatingFileHandler(filename=filename, backupCount=5)
        self.log.addHandler(self.handler)
        self.log.setLevel(level=level)

    def count_up(self, function_name):
        self._func_count.update({function_name: self._func_count.get(function_name, 0) + 1})

    @property
    def counts(self):
        return self._func_count

flog = funcLogger()

def func_timer(func):
    """time a function, record how many times called"""
    def inner(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now() - start
        flog.count_up(function_name=func.__name__)
        flog.log.info(f"TIMER: {func.__name__}() -> {end} | "
                      f"COUNT: {flog.counts.get(func.__name__)}")
        return result
    return inner
