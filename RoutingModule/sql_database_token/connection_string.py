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

    from .use_access_token import UseToken
except ImportError as error:
    raise Exception(f"{error}") from None 

class ConnectionDBString:
    @classmethod
    def connection_db_string(cls):

        server_name = 'accelitas-sql-server-01-dev-wus.database.windows.net'

        database_name = 'accelitas-reporting-db-merged'

        SQL_COPT_SS_ACCESS_TOKEN = 1256

        tokenstruct = UseToken.use_token()

        connection_string='Driver={ODBC Driver 17 for SQL Server};server='+server_name+';database='+database_name+''
        
        return connection_string,  SQL_COPT_SS_ACCESS_TOKEN, tokenstruct