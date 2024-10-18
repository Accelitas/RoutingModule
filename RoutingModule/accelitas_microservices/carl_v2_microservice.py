
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

class CarlV2Microservice:

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
                                  SELECT MAX(log_timestamp) as latest_time_stamp FROM dbo.carl_splunk;
                               """
                               )
                
                cls.latest_time_stamp = cursor.fetchone()[0]

                

    @classmethod
    def get_splunk_logs_through_rest_api(cls):

        rex = "(?P<carl_data>{.*})"

        reason_code ="AUDIT RECORD: CARL.backendResponse.responseBody.reason_codes{}"

        search_query = (
                        f'search index="accelitas_k8s_cus_prod" OR index = "accelitas_k8s_eus2_prod" sourcetype="kube:container:carl-v2"'
                        f'|rex field=_raw "{rex}"'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.transaction_id" output=transaction_id'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.clientId" output=client_id'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.repositoryResponse.customerDocument.servicer.name" output=servicer_name'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.repositoryResponse.customerDocument.customer.name" output=customer_name'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.repositoryResponse.customerDocument.customer.dba.name" output=customer_dba'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.repositoryResponse.customerDocument.customer.dba.service.credentials.type" output=credential_type'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.repositoryResponse.customerDocument.customer.dba.service.name" output=service'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.repositoryResponse.customerDocument.customer.dba.service.version" output=service_version'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.repositoryResponse.customerDocument.customer.dba.service.workflow.dataProviders.telecheckAVDataProvider.mid" output=mid'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.repositoryResponse.customerDocument.customer.dba.service.workflow.dataProviders.dataXDataProvider.businessRule" output=business_rule'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.repositoryResponse.customerDocument.customer.dba.service.workflow.scoringProviders.transformScoringProvider.model" output=model'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.signal" output=signal'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.signal_1" output=signal_1'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.signal_2" output=signal_2'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.signal_3" output=signal_3'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.score_aba" output=score_aba'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.score_aba" output=score_aba'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.score_acct" output=score_acct'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.score_act" output=score_act'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.score_conv" output=score_conv'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.score_fpd" output=score_fpd'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.valid_aba" output=valid_aba'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.valid_routing" output=valid_routing'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.status_message" output=status_message'
                        f'|spath input=carl_data path="{reason_code}" output=reason_code'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.reason_codes2" output=reason_code2'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.reason_codes3" output=reason_code3'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.reason_codes4" output=reason_code4'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.reason_codes5" output=reason_code5'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.correlationId" output=correlation_id'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.valid_institution" output=valid_institution'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.backendResponse.responseBody.valid_transit" output=valid_transit'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.auditTimeStamp" output=log_timestamp'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.repositoryResponse.customerDocument.customer.dba.service.workflow.threshold" output=signal_threshold'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.repositoryResponse.customerDocument.customer.dba.service.workflow.threshold" output=threshold_result'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.pipelineContext.requestReceivedTimestamp" output=timestamp'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.pipelineContext.requestElapsed" output=overall_time'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.carlRequest.requestHeaders.X-Azure-Clientip" output=client_ip'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.pipelineContext.deployment.region" output=region'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.carlRequest.requestHeaders.Authorization" output=authentication_type'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.authorizerResponse.is_authorized" output=authorized'
                        f'|spath input=carl_data path="AUDIT RECORD: CARL.authorizerResponse.Duration" output=authorizer_time'
                        f'|where log_timestamp > {cls.latest_time_stamp}'
                        f'|fields - _raw, carl_data'
                        f'|table transaction_id,client_id,servicer_name,customer_name,customer_dba,credential_type,service, service_version, mid, business_rule, model,signal,signal_1, signal_2, signal_3,score_aba,score_acct,score_act,score_conv,score_fpd,valid_aba,valid_routing,status_message,reason_code,reason_code2,reason_code3,reason_code4,reason_code5,correlation_id,valid_institution,valid_transit,log_timestamp,signal_threshold,threshold_result,timestamp,overall_time,client_ip,region,authentication_type,authorized,authorizer_time'

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
                
                df = pd.read_csv(io.StringIO(response.text))

                df.replace({np.NaN: None}, inplace=True)
                
                df["authentication_type"] = df["authentication_type"].apply(lambda x : x.split()[0])

                df["reason_code"] = df["reason_code"].apply(lambda x : str(x)) #converting reason_codes which are comma separated into string for easy DB operations

                cls.df = df


    @classmethod
    def push_splunk_logs_to_sql_database(cls):
        
        insert_query = "INSERT INTO dbo.carl_splunk ({}) VALUES ({})".format(",".join(cls.df.columns), ",".join(['?'] * len(cls.df.columns)))

        with pyodbc.connect(cls.connection_string, attrs_before = {cls.SQL_COPT_SS_ACCESS_TOKEN:cls.tokenstruct}) as connect:

            with connect.cursor() as cursor:

                for start in range(0, len(cls.df), cls.chunk_size):
                     
                    end = start + cls.chunk_size

                    chunk_amt = cls.df.iloc[start:end]
                    
                    cursor.executemany(insert_query, chunk_amt.values.tolist())

                connect.commit()

def run_carl_v2_microservice():

    #CarlV2Microservice.get_latest_time_stamp()
    # CarlV2Microservice.get_splunk_logs_through_rest_api()
    #CarlV2Microservice.push_splunk_logs_to_sql_database()
    pass




