#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 19:32:11 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from fastapi import FastAPI
from model.resource import ExperimentResource
from model.experiment import OptimizationOption, OptimizationResult


app = FastAPI()

@app.get("/option")
def getOption() -> ExperimentResource:
    return ExperimentResource()

@app.post("/experiment")
def runExperiment(option: OptimizationOption) -> OptimizationResult:
    return OptimizationResult()
