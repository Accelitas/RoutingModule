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
    from IPython.display import display 
except ImportError as error:
    raise Exception(f"{error}") from None 

class CustomError(Exception):
    def __init__(self, message = "Custom Exception Occurs - Debugging Needed", *args, **kwargs):
        
        super(CustomError, self).__init__(message, *args, **kwargs)
