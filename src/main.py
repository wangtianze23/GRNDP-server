#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 19:32:11 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from fastapi import FastAPI
from fastapi.responses import Response
import urllib.request
import urllib.error
import config
from infrastructure.config.Service import BaseServiceConfig
from application.optimization import NetworkOptimization
from model.experiment.Resource import ExperimentResource
from model.experiment.Option import ExperimentOption
from model.experiment.Result import ExperimentResult


app = FastAPI()

@app.get("/option")
def getOption() -> ExperimentResource:
    serviceConfig = BaseServiceConfig(config.LOCAL_RESOURCE_ROOT)
    service = NetworkOptimization(serviceConfig)
    return service.getResource()

@app.post("/experiment")
def runExperiment(option: ExperimentOption) -> ExperimentResult:
    serviceConfig = BaseServiceConfig(config.LOCAL_RESOURCE_ROOT)
    service = NetworkOptimization(serviceConfig)
    result = service.optimize(option)
    if option.isAsynchronous():
        try:
            urllib.request.urlopen(config.EXPERIMENT_CALLBACK_URL, 
                                   result.model_dump_json().encode('utf-8'))
        except urllib.error.HTTPError:
            pass
        return Response()
    else:
        return result
