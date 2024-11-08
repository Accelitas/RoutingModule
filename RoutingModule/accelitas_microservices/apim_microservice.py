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
    import io
    import sys 
    import json 
    import struct
    import pyodbc
    import pathlib
    import logging 
    import warnings 
    import requests
    import subprocess
    import contextlib 
    import urllib.parse
    import pandas as pd
    import numpy as np
    from functools import lru_cache, wraps
    from IPython.display import display     
except ImportError as error:
    raise Exception(f"{error}") from None 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

try:
    from sql_database_token import ConnectionDBString 
    from splunk_session_key import GetSplunkSessionKey
except ImportError as error:
    raise Exception(f"{error}") from None  

class ApimMicroservice:

    connection_string, SQL_COPT_SS_ACCESS_TOKEN, tokenstruct = ConnectionDBString.connection_db_string()

    session_key = GetSplunkSessionKey.get_splunk_session_key()

    base_url = "https://splunk-api.accelitas.io:8089"

    latest_time_stamp = None 

    chunk_size = 1000

    df = None

    @classmethod
    def get_latest_time_stamp(cls):

        with pyodbc.connect(cls.connection_string, attrs_before = {cls.SQL_COPT_SS_ACCESS_TOKEN:cls.tokenstruct}) as connect:

            with connect.cursor() as cursor:

                cursor.execute(
                               """
                                  SELECT MAX(log_timestamp) as latest_time_stamp FROM dbo.apim_splunk;
                               """
                               )
                
                cls.latest_time_stamp = cursor.fetchone()[0]

    @classmethod
    def get_splunk_logs_through_rest_api(cls):

        rex = "(?P<apim_data>{.*})"

        search_query = (
                        f'search index="accelitas_k8s_cus_prod" OR index = "accelitas_k8s_eus2_prod" sourcetype="kube:container:carl-v2"'
                        f'|rex field=_raw "{rex}"'
                        f'|spath input=apim_data path="AUDIT RECORD: CARL.overallTransactionDuration" output=overall_time'
                        f'|spath input=apim_data path="AUDIT RECORD: CARL.carlRequest.requestHeaders.X-Azure-Clientip" output=client_ip'
                        f'|spath input=apim_data path="AUDIT RECORD: CARL.pipelineContext.deployment.region" output=region'
                        f'|spath input=apim_data path="AUDIT RECORD: CARL.carlRequest.requestHeaders.Authorization" output=authentication_type'
                        f'|spath input=apim_data path="AUDIT RECORD: CARL.correlationId" output=correlation_id'
                        f'|spath input=apim_data path="AUDIT RECORD: CARL.pipelineContext.requestReceivedTimestamp" output=timestamp'
                        f'|where log_timestamp > "{cls.latest_time_stamp}"'
                        f'|fields - _raw, apim_data'
                        f'|table log_timestamp, overall_time, client_ip, region, authentication_type, correlation_id, timestamp'
                       )

        payload = {
                    "search" : search_query,
                    'output_mode': 'csv'
                    
                  }
        
        safe_payload = urllib.parse.urlencode(payload)

        with requests.Session() as session:

            with session.post(
                               url = cls.base_url + "/services/search/jobs/export",

                               headers = {
                                          "Authorization" : ('Splunk %s' %cls.session_key ),

                                          'Content-Type': 'application/json; charset=UTF-8'
                                         },

                               data = safe_payload,

                               verify = False

                             ) as response:
                
                
                df = pd.read_csv(io.StringIO(response.text), low_memory=False)

                df.dropna(subset = ["correlation_id"], inplace = True)
                
                df.replace({np.NaN: None}, inplace=True)

                df["authentication_type"] = df["authentication_type"].apply(lambda x : x.split()[0])

                cls.df = df

                print(cls.df)


    @classmethod
    def push_splunk_logs_to_sql_database(cls):

        print("Insertion of data start")
        
        insert_query = "INSERT INTO dbo.apim_splunk ({}) VALUES ({})".format(",".join(cls.df.columns), ",".join(['?'] * len(cls.df.columns)))

        with pyodbc.connect(cls.connection_string, attrs_before = {cls.SQL_COPT_SS_ACCESS_TOKEN:cls.tokenstruct}) as connect:

            with connect.cursor() as cursor:

                for index, row in cls.df.iterrows():
                     
                    cursor.execute(insert_query, tuple(row))

                connect.commit()

        print(f"No of rows inserted - {len(cls.df)}")

def run_apim_microservice():

    ApimMicroservice.get_latest_time_stamp()
    ApimMicroservice.get_splunk_logs_through_rest_api()
    ApimMicroservice.push_splunk_logs_to_sql_database()
    

