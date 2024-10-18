#!/usr/bin/python
#-*- coding:utf-8 -*- 
#docstring style: Sphinx

from __future__ import (
                         absolute_import,
                         annotations
                       )

__status__ = None 
__author__ = "Nimit Gupta"
__version__ = None 
__license__ = "LICENSE.txt" 

try:
    import os 
    import sys 
    import json 
    import logging 
    import warnings 
    import contextlib 
    from functools import lru_cache, wraps
    from IPython.display import display 
except ImportError as error:
    raise Exception(f"{error}") from None 

class CreateLogger:
    @classmethod
    def create_logger(cls):

        logger = logging.getLogger(__name__)

        if not logger.handlers:

            logger.setLevel(level = logger.INFO)

            file_handler = logging.FileHandler(os.path.abspath(os.path.join(os.path.dirname(__file__), "logs", "logs.txt")))

            file_formater = logging.Formatter("%(asctime)s : %(message)s")

            file_handler.setFormatter(file_formater)

            logger.addHandler(file_handler)
            
        return logger