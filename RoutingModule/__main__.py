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
    from utils import (
                       CreateLogger,
                       CustomError,
                       IgnoreWarnings  
                      )
    from accelitas_microservices import (
                                            # run_ailift_microservice,
                                            # run_apim_microservice,
                                            # run_authorizer_microservice,
                                            # run_carl_v2_microservice,
                                            # run_datax_microservice,
                                            # run_pii_microservice, 
                                            # run_datawire_microservice ,
                                            # run_telecheck_mi_microservice,
                                       ) 



class RunModule(CreateLogger):
    @classmethod
    @IgnoreWarnings
    def run_module(cls):

        logger = super(RunModule).__get__(cls, None).create_logger()

        try:
            logger.info("Start Executing AI-Lift Microservice")
            print("Start Executing AI-Lift Microservice")
            run_ailift_microservice()
        except Exception as exc:
            logger.info(exc.__class__.__name__ + "-" + str(exc))
            print("Exception Occured, While Executing")
            pass
        finally:
            logger.info("Stop Executing AI-Lift Micoservice")
            print("Stop Executing AI-Lift Microservice")

        try:
            logger.info("Start Executing APIM Microservice")
            print("Start Executing APIM Microservice")
            run_apim_microservice()
        except Exception as exc:
            logger.info(exc.__class__.__name__ + "-" + str(exc))
            print("Exception Occured, While Executing")
            pass
        finally:
            logger.info("Stop Executing APIM Micoservice")
            print("Stop Executing APIM Microservice")

        try:
            logger.info("Start Executing Authorizer Microservice")
            print("Start Executing Authorizer Microservice")
            run_authorizer_microservice()
        except Exception as exc:
            logger.info(exc.__class__.__name__ + "-" + str(exc))
            print("Exception Occured, While Executing")
            pass
        finally:
            logger.info("Stop Executing Authorizer Micoservice")
            print("Stop Executing Authorizer Microservice")

        try:
            logger.info("Start Executing Carl V2 Microservice")
            print("Start Executing Carl V2 Microservice")
            run_carl_v2_microservice()
        except Exception as exc:
            logger.info(exc.__class__.__name__ + "-" + str(exc))
            print("Exception Occured, While Executing")
            pass
        finally:
            logger.info("Stop Executing Carl V2 Micoservice")
            print("Stop Executing Carl V2 Microservice")

        try:
            logger.info("Start Executing DATAX Microservice")
            print("Start Executing DATAX Microservice")
            run_datax_microservice()
        except Exception as exc:
            logger.info(exc.__class__.__name__ + "-" + str(exc))
            print("Exception Occured, While Executing")
            pass
        finally:
            logger.info("Stop Executing DATAX Micoservice")
            print("Stop Executing DATAX Microservice")

        try:
            logger.info("Start Executing PII Microservice")
            print("Start Executing PII Microservice")
            run_pii_microservice()
        except Exception as exc:
            logger.info(exc.__class__.__name__ + "-" + str(exc))
            print("Exception Occured, While Executing")
            pass
        finally:
            logger.info("Stop Executing PII Micoservice")
            print("Stop Executing PII Microservice")

        try:
            logger.info("Start Executing DATAWIRE Microservice")
            print("Start Executing DATAWIRE Microservice")
            run_datawire_microservice()
        except Exception as exc:
            logger.info(exc.__class__.__name__ + "-" + str(exc))
            print("Exception Occured, While Executing")
            pass
        finally:
            logger.info("Stop Executing DATAWIRE Micoservice")
            print("Stop Executing DATAWIRE Microservice")

        try:
            logger.info("Start Executing TeleCheck MI Microservice")
            print("Start Executing TeleCheck MI Microservice")
            run_telecheck_mi_microservice()
        except Exception as exc:
            logger.info(exc.__class__.__name__ + "-" + str(exc))
            print("Exception Occured, While Executing")
            pass
        finally:
            logger.info("Stop Executing TeleCheck MI Micoservice")
            print("Stop Executing TeleCheck MI Microservice")

        
if __name__ == "__main__":
    RunModule.run_module()

