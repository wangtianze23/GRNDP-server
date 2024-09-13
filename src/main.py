#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 19:32:11 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import config
from fastapi import FastAPI
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
    return service.optimize(option)
