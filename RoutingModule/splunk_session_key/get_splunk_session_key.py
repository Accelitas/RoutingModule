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
    import urllib3
    import struct
    import pyodbc
    import pathlib
    import logging 
    import warnings 
    import requests
    import subprocess
    import contextlib 
    from xml.dom import minidom
    from dotenv import load_dotenv, find_dotenv
    from functools import lru_cache, wraps
    from IPython.display import display     
except ImportError as error:
    raise Exception(f"{error}") from None 


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GetSplunkSessionKey:    

    base_url = "https://splunk-api.accelitas.io:8089"

    load_dotenv(find_dotenv())

    @classmethod
    def get_splunk_session_key(cls):  

        payload = {
                   "username" : os.environ.get("splunk_username"),
                   "password" : os.environ.get("splunk_password")
                  }
        
        # print(payload)

        with requests.Session() as session:

            with session.get(
                             url = cls.base_url + "/servicesNS/admin/search/auth/login", 

                             headers= {"Content-Type" : "application/x-www-form-urlencoded"},

                             data = payload,

                             verify = False     

                            ) as response:
                # print(response.text)
                session_key = minidom.parseString(response.text).getElementsByTagName('sessionKey')[0].firstChild.nodeValue
                # print(session_key)
                return session_key

# GetSplunkSessionKey.get_splunk_session_key()

   