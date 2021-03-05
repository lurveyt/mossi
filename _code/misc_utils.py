""" Documentation for misc_utils
A collection of various useful function to be reused outside class"""

import datetime
import logging
from logging.handlers import RotatingFileHandler

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
