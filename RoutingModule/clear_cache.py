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
    import pathlib
    import logging 
    import warnings 
    import contextlib 
    from functools import lru_cache, wraps
    from IPython.display import display 
except ImportError as error:
    raise Exception(f"{error}") from None 

class ClearPyCache:
    @classmethod
    def clear_py_cache(cls):

        for _cache in pathlib.Path('.').rglob('*.py[co]'):

            _cache.unlink()

        for _cache in pathlib.Path('.').rglob('__pycache__'):
            
            _cache.rmdir()

if __name__ == "__main__":
    ClearPyCache.clear_py_cache()
