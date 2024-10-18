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
    import re
    import sys 
    import json 
    import struct
    import pathlib
    import logging 
    import warnings 
    import subprocess
    import contextlib 
    from functools import lru_cache, wraps
    from IPython.display import display 

    from .get_access_token import GetToken
except ImportError as error:
    raise Exception(f"{error}") from None 

class UseToken:
    @classmethod
    def use_token(cls):

        rcv_token = GetToken.get_token()
        # print(rcv_token)

        exptoken = b''

        for i in bytes(rcv_token, "UTF-8"):

            exptoken += bytes({i})

            exptoken += bytes(1)
            
        tokenstruct = struct.pack("=i", len(exptoken)) + exptoken
        # print(tokenstruct)

        return tokenstruct


