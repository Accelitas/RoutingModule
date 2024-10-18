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
    import atexit
    import logging 
    import warnings 
    import contextlib 
    from functools import lru_cache, wraps
    from IPython.display import display 
except ImportError as error:
    raise Exception(f"{error}") from None 

def must_be_called(decorated_function):

    decorated_function.called = False 

    def wrapper_function(*args, **kwargs):

        decorated_function.called = True 

        return decorated_function(*args, **kwargs)
    
    atexit.register(lambda:check_call(decorated_function))

def check_call(decorated_function):

    if not decorated_function.called:
        
        raise RuntimeError(f"{decorated_function.__name__} was not called")