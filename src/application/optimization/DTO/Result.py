#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 20:17:34 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel
from application.experiment.DTO.Result import \
    ExperimentResult, ExperimentResultBody
from application.optimization.DTO.Network import EdgeParameter
from application.optimization.DTO.Visualization import \
    VisualizedPath, VisualizedDensity


class OptimizedRegulation(BaseModel):
    index: int
    ID: str
    parameters:list[EdgeParameter]

class OptimizedTarget(BaseModel):
    index: int
    name: str
    description: str
    nodeIndexes: list[int]
    value: float

class OptimizationResultBody(ExperimentResultBody):
    optimizedEdgeList: list[OptimizedRegulation]
    optimizedTargetList: list[OptimizedTarget]
    visualizedPathList: list[VisualizedPath]
    visualizedDensityList: list[VisualizedDensity]

class OptimizationResult(ExperimentResult):
    data: OptimizationResultBody
