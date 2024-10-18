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

class IgnoreWarnings:
    def __init__(self):

        self.category = [
                          Warning,
                          RuntimeWarning,
                          FutureWarning,
                          SyntaxWarning,
                          DeprecationWarning,
                          PendingDeprecationWarning
                        ]
        
    def __call__(self, decorated_function):

        @wraps(decorated_function)

        def wrapper_function(*args, **kwargs):

            with contextlib.suppress(
                                      IndexError,
                                      AttributeError
                                    ):
                
                with warnings.catch_warnings(record = True):

                    for _category in self.category:

                        warnings.filterwarnings(
                                                action = "ignore",
                                                category = _category
                                               )
                        
                    return decorated_function(*args, **kwargs)
                
        return wrapper_function
