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

class PIIMicroservice:

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
                                  SELECT MAX(log_timestamp) as latest_time_stamp FROM dbo.pii_splunk;
                               """
                               )
                
                cls.latest_time_stamp = cursor.fetchone()[0]

    @classmethod
    def get_splunk_logs_through_rest_api(cls):

        rex = "(?P<pii_data>{.*})"

        search_query = (
                        f'search index="accelitas_k8s_cus_prod" OR index = "accelitas_k8s_eus2_prod" sourcetype="kube:container:ailift"'
                        f'|rex field=_raw "{rex}"'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.account_number" output=account_number'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.address" output=address'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.address2" output=address2'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.city" output=city'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.correlationId" output=correlation_id'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.customer_transaction_id" output=customer_transaction_id'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.date_of_birth" output=date_of_birth'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.email" output=email'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.first_name" output=first_name'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.ip_address" output=ip_address'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.last_name" output=last_name'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.auditTimeStamp" output=log_timestamp'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.phone_number" output=phone_number'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.routing_number" output=routing_number'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.ssn_tin" output=ssn_tin'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.state" output=state'
                        f'|spath input=pii_data path="AUDIT RECORD: AI-LIFT.aiLiftRequest.zip_code" output=zip_code'
                        f'|where log_timestamp > "{cls.latest_time_stamp}"'
                        f'|fields - _raw, pii_data'
                        f'|table routing_number, account_number, ssn_tin, first_name, last_name, date_of_birth, address, address2, city, state, zip_code, phone_number, email, ip_address, customer_transaction_id, correlation_id, log_timestamp'
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

                df['account_number'] = df['account_number'].astype("Int64").astype(str)

                df['routing_number'] = df['routing_number'].astype("Int64").astype(str)

                df['ssn_tin'] = df['ssn_tin'].astype("Int64").astype(str)

                cls.df = df

                print(cls.df)


    @classmethod
    def push_splunk_logs_to_sql_database(cls):

        print("Insertion of data start")
        
        insert_query = "INSERT INTO dbo.pii_splunk ({}) VALUES ({})".format(",".join(cls.df.columns), ",".join(['?'] * len(cls.df.columns)))

        with pyodbc.connect(cls.connection_string, attrs_before = {cls.SQL_COPT_SS_ACCESS_TOKEN:cls.tokenstruct}) as connect:

            with connect.cursor() as cursor:

                for start in range(0, len(cls.df), cls.chunk_size):
                     
                    end = start + cls.chunk_size

                    chunk_amt = cls.df.iloc[start:end]
                    
                    cursor.executemany(insert_query, chunk_amt.values.tolist())

                connect.commit()

        print(f"No of rows inserted - {len(cls.df)}")

def run_pii_microservice():

    PIIMicroservice.get_latest_time_stamp()
    PIIMicroservice.get_splunk_logs_through_rest_api()
    PIIMicroservice.push_splunk_logs_to_sql_database()


