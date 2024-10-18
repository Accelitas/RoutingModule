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
    import pathlib
    import logging 
    import warnings 
    import subprocess
    import contextlib 
    from functools import lru_cache, wraps
    from IPython.display import display 
except ImportError as error:
    raise Exception(f"{error}") from None 

class GetToken:
    @classmethod
    def get_token(cls):

        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "azure_sql_db.ps1"))
        # print(script_path)

        process = subprocess.Popen(['powershell', '-File', script_path], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        output, error = process.communicate()
        # print(output.decode('utf-8'))

        match_1 = re.search(r'access_token=([^;]+)',output.decode('utf-8'))

        access_token_1 = match_1.group(1)
        # print(access_token_1)

        match_2 = re.search(r'([A-Za-z0-9\.\-_]+)', access_token_1)

        access_token_2 = match_2.group(1) 
        # print(access_token_2)

        return access_token_2


    

    



                    

